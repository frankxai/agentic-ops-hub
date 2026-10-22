#!/usr/bin/env python3
"""Launch an unattended OpenCode run under a generated, provider-restricted config.

`opencode run -m <model>` pins only the primary model. OpenCode also makes side calls (titles via
`small_model`, subagents) that follow the merged config, and OpenCode v2 hands every run to a
long-lived managed background service that already holds the user's own config. Both were
checked on the installed opencode 2.1.2 (see ops/sessions/2026-10-21-routing-brain-hardening.md,
"Round 12"):

  * Without `--standalone` the client's environment never reaches the service, so a per-launch
    config is ignored. This module always passes `--standalone`.
  * With `--standalone`, a config directory named by OPENCODE_CONFIG_DIR outranks the global
    opencode.json, an OPENCODE_CONFIG file, OPENCODE_CONFIG_CONTENT and a project-level
    opencode.json: `opencode models --standalone` lists only gateway models under all four
    hostile settings. The directory REPLACES the global config, so it must carry the gateway
    provider block itself.

Scope of the guarantee: calls started through this module are limited to the gateway provider
(or, with allow_free, the gateway plus opencode/*-free models, which run outside the ZDR
gateway key). A person typing `opencode` directly uses their own config and is outside it.
`small_model` and `model` are pinned in the same file; the effective small_model value could
not be read back without a model call, so that part rests on the provider restriction plus the
file precedence shown above, not on a direct read.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping

GATEWAY_PROVIDER = "vercel"
CONFIG_DIR_ENV = "OPENCODE_CONFIG_DIR"
GATEWAY_KEY_ENV = "AI_GATEWAY_API_KEY"
GLOBAL_CONFIG_ENV = "OPENCODE_GLOBAL_CONFIG"  # test and CI override for the global config path
# Providers that must stay off in strict mode even if a file somewhere enables them.
DISABLED_PROVIDERS = ("opencode", "omniroute")
# Overrides that other tools might leave in the environment. They do not outrank the launch
# directory, but a launch removes them anyway so the effective config has one source.
_STRIPPED_ENV = ("OPENCODE_CONFIG", "OPENCODE_CONFIG_CONTENT")


class LaunchError(ValueError):
    pass


def global_config_path(env: Mapping[str, str] | None = None) -> Path:
    env = os.environ if env is None else env
    if env.get(GLOBAL_CONFIG_ENV):
        return Path(env[GLOBAL_CONFIG_ENV])
    base = env.get("XDG_CONFIG_HOME") or str(Path(env.get("USERPROFILE") or env.get("HOME") or "~").expanduser() / ".config")
    return Path(base) / "opencode" / "opencode.json"


def gateway_provider_block(env: Mapping[str, str] | None = None, config_path: Path | None = None) -> dict[str, Any]:
    """The provider block the launch config needs so the gateway still authenticates.

    Preferred: an `{env:AI_GATEWAY_API_KEY}` reference, so no secret is written to disk.
    Fallback: copy `provider.vercel` from the user's global config. Neither available: refuse."""
    env = os.environ if env is None else env
    if env.get(GATEWAY_KEY_ENV):
        return {"options": {"apiKey": "{env:%s}" % GATEWAY_KEY_ENV}}
    path = config_path or global_config_path(env)
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LaunchError(f"no gateway credentials: set {GATEWAY_KEY_ENV} or configure provider.{GATEWAY_PROVIDER} "
                          f"in {path} ({type(exc).__name__})") from exc
    block = (data.get("provider") or {}).get(GATEWAY_PROVIDER) if isinstance(data, dict) else None
    key = ((block or {}).get("options") or {}).get("apiKey") if isinstance(block, dict) else None
    if not isinstance(key, str) or not key.strip():
        raise LaunchError(f"no gateway credentials: provider.{GATEWAY_PROVIDER}.options.apiKey is missing in {path}")
    return copy.deepcopy(block)


def _base_model(model_ref: str) -> str:
    """`provider/model#variant` -> `provider/model` (a config file takes no variant suffix)."""
    return model_ref.split("#", 1)[0]


def build_launch_config(model_ref: str, *, allow_free: bool, provider_block: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(model_ref, str) or "/" not in model_ref:
        raise LaunchError(f"pinned model must look like provider/model, got {model_ref!r}")
    model = _base_model(model_ref)
    if not allow_free and not model.startswith(GATEWAY_PROVIDER + "/"):
        raise LaunchError(f"strict mode only launches {GATEWAY_PROVIDER}/* models, got {model!r}")
    config: dict[str, Any] = {
        "model": model,
        "small_model": model,
        "provider": {GATEWAY_PROVIDER: copy.deepcopy(dict(provider_block))},
    }
    if allow_free:
        # Outside the ZDR gateway guarantee: opencode/*-free models run on OpenCode's own endpoint.
        config["enabled_providers"] = [GATEWAY_PROVIDER, "opencode"]
    else:
        config["enabled_providers"] = [GATEWAY_PROVIDER]
        config["disabled_providers"] = list(DISABLED_PROVIDERS)
    return config


@contextlib.contextmanager
def launch_dir(config: Mapping[str, Any]) -> Iterator[Path]:
    """A private directory holding the generated opencode.json, removed on exit."""
    root = Path(tempfile.mkdtemp(prefix="starlight-oc-"))
    try:
        with contextlib.suppress(OSError):
            os.chmod(root, 0o700)
        fd = os.open(root / "opencode.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(config, handle)
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def launch_env(directory: Path, base_env: Mapping[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    for name in _STRIPPED_ENV:
        env.pop(name, None)
    env[CONFIG_DIR_ENV] = str(directory)
    return env


def opencode_argv(model_ref: str, task: str, binary: str = "opencode") -> list[str]:
    # `--standalone` is required: the managed service ignores the client's environment.
    # The variant stays inside -m (`provider/model#variant`): the installed `opencode run --help`
    # documents that format and lists no --variant flag.
    return [binary, "run", "--standalone", "-m", model_ref, task]


def wrapper_argv(route_class: str, task: str, *, allow_free: bool = False) -> list[str]:
    """A self-contained command: a manifest or night runner can run it without knowing the config."""
    argv = ["python", "-B", str(Path(__file__).resolve()), "--class", route_class]
    if allow_free:
        argv.append("--allow-free")
    return argv + ["--", task]


def run(route_class: str, task: str, *, allow_free: bool = False, env: Mapping[str, str] | None = None,
        config_path: Path | None = None,
        runner: Callable[..., Any] = subprocess.run) -> int:
    try:
        from fleet.token_planner import pinned_opencode_model
    except ImportError:  # executed as a script from the fleet directory
        from token_planner import pinned_opencode_model  # type: ignore[no-redef]
    model_ref = pinned_opencode_model(route_class, allow_free=allow_free)  # raises PlannerError when unresolved
    block = gateway_provider_block(env, config_path)
    config = build_launch_config(model_ref, allow_free=allow_free, provider_block=block)
    binary = shutil.which("opencode") or "opencode"
    with launch_dir(config) as directory:
        result = runner(opencode_argv(model_ref, task, binary), env=launch_env(directory, env))
    return int(getattr(result, "returncode", 0) or 0)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run opencode under a generated, provider-restricted config.")
    ap.add_argument("--class", dest="route_class", required=True, help="routing.schema.json task class")
    ap.add_argument("--allow-free", action="store_true",
                    help="also allow opencode/*-free models (outside the ZDR gateway guarantee)")
    ap.add_argument("task", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    task = " ".join(a for a in args.task if a != "--").strip()
    if not task:
        print("error: no task given", file=sys.stderr)
        return 2
    try:
        return run(args.route_class, task, allow_free=args.allow_free)
    except ValueError as exc:  # LaunchError and PlannerError are both ValueError
        print(f"refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
