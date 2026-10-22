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

The provider block is built here, never copied: the user's global `provider.vercel` can carry
`options.baseURL`, `api`, `npm` or per-model overrides that send prompts elsewhere (Codex round 13),
so only the API key is taken from it, and it travels in the child's environment, not on disk.
OpenCode is executed as the native binary with shell=False and a `--` before the task: the npm
`.cmd` shim is run by cmd.exe on Windows, which would interpret `&` and quotes in task text.

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
import signal
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
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


def gateway_provider_block() -> dict[str, Any]:
    """The only provider block a launch config carries: a fixed gateway block that reads the key from
    the environment. No baseURL, api, npm or model overrides, and no secret on disk."""
    return {"options": {"apiKey": "{env:%s}" % GATEWAY_KEY_ENV}}


def gateway_key(env: Mapping[str, str] | None = None, config_path: Path | None = None) -> str | None:
    """The gateway key to hand the child through its environment, or None when the caller's
    environment already has it. Fallback: only `provider.vercel.options.apiKey` from the global
    config; every other field of that block is ignored. Neither available: refuse."""
    env = os.environ if env is None else env
    if env.get(GATEWAY_KEY_ENV):
        return None
    path = config_path or global_config_path(env)
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LaunchError(f"no gateway credentials: set {GATEWAY_KEY_ENV} or configure provider.{GATEWAY_PROVIDER} "
                          f"in {path} ({type(exc).__name__})") from exc
    block = (data.get("provider") or {}).get(GATEWAY_PROVIDER) if isinstance(data, dict) else None
    key = ((block or {}).get("options") or {}).get("apiKey") if isinstance(block, dict) else None
    if not isinstance(key, str) or not key.strip() or key.lstrip().startswith("{"):
        raise LaunchError(f"no gateway credentials: provider.{GATEWAY_PROVIDER}.options.apiKey is missing in {path}")
    return key


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


def launch_env(directory: Path, base_env: Mapping[str, str] | None = None, key: str | None = None) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    for name in _STRIPPED_ENV:
        env.pop(name, None)
    if key:
        env[GATEWAY_KEY_ENV] = key
    env[CONFIG_DIR_ENV] = str(directory)
    return env


def resolve_opencode(found: str | None = None, windows: bool | None = None) -> str:
    """The native OpenCode executable. On Windows PATH usually yields the npm `.cmd` shim, which
    cmd.exe parses (task text with `&` would run commands), so the real exe next to it is used
    instead. No safe binary: refuse, never fall back to the shim."""
    windows = os.name == "nt" if windows is None else windows
    found = found if found is not None else shutil.which("opencode")
    if not found:
        raise LaunchError("opencode was not found on PATH")
    path = Path(found)
    if not windows or path.suffix.lower() == ".exe":
        return found
    for pattern in ("node_modules/*/cli/bin/opencode.exe", "node_modules/opencode-ai/**/opencode.exe",
                    "node_modules/*/bin/opencode.exe"):
        hits = sorted(path.parent.glob(pattern))
        if hits:
            return str(hits[0])
    raise LaunchError(f"found only the batch shim {path.name}; refusing to run it through cmd.exe. "
                      "Install a native opencode.exe or put it on PATH")


def opencode_argv(model_ref: str, task: str, binary: str = "opencode") -> list[str]:
    # `--standalone` is required: the managed service ignores the client's environment.
    # The variant stays inside -m (`provider/model#variant`): the installed `opencode run --help`
    # documents that format and lists no --variant flag.
    return [binary, "run", "--standalone", "-m", model_ref, "--", task]  # `--`: task text is never an option


def wrapper_argv(route_class: str, task: str, *, allow_free: bool = False) -> list[str]:
    """A self-contained command: a manifest or night runner can run it without knowing the config."""
    argv = ["python", "-B", str(Path(__file__).resolve()), "--class", route_class]
    if allow_free:
        argv.append("--allow-free")
    return argv + ["--", task]


class _TreeGuard:
    """Ends the child's whole process tree. Windows: a kill-on-close Job object, so the tree also
    dies if this wrapper is killed (falls back to `taskkill /T`). POSIX: a new session/process
    group, killed on exit paths of this wrapper; a SIGKILL of the wrapper itself leaves the child."""

    def __init__(self, proc: subprocess.Popen) -> None:
        self.proc, self.job, self._k = proc, None, None
        if os.name == "nt":
            with contextlib.suppress(Exception):
                self._k, self.job = _windows_job(proc)

    def kill(self) -> None:
        if os.name == "nt":
            if self.job is not None and self._k.TerminateJobObject(self.job, 1):
                return
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.proc.pid)], capture_output=True)
            return
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(self.proc.pid, signal.SIGKILL)

    def close(self) -> None:
        if self.job is not None:
            self._k.CloseHandle(self.job)  # KILL_ON_JOB_CLOSE ends any straggler
            self.job = None


def _windows_job(proc: subprocess.Popen):
    import ctypes
    from ctypes import wintypes
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.restype = wintypes.HANDLE
    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k.CloseHandle.argtypes = [wintypes.HANDLE]

    class IoCounters(ctypes.Structure):
        _fields_ = [(n, ctypes.c_ulonglong) for n in ("r_ops", "w_ops", "o_ops", "r_bytes", "w_bytes", "o_bytes")]

    class Basic(ctypes.Structure):
        _fields_ = [("per_process_time", ctypes.c_int64), ("per_job_time", ctypes.c_int64),
                    ("flags", wintypes.DWORD), ("min_ws", ctypes.c_size_t), ("max_ws", ctypes.c_size_t),
                    ("active_limit", wintypes.DWORD), ("affinity", ctypes.c_size_t),
                    ("priority", wintypes.DWORD), ("scheduling", wintypes.DWORD)]

    class Extended(ctypes.Structure):
        _fields_ = [("basic", Basic), ("io", IoCounters), ("process_mem", ctypes.c_size_t),
                    ("job_mem", ctypes.c_size_t), ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]

    job = k.CreateJobObjectW(None, None)
    if not job:
        raise OSError("CreateJobObject failed")
    info = Extended()
    info.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)) \
            or not k.AssignProcessToJobObject(job, int(proc._handle)):  # type: ignore[attr-defined]
        k.CloseHandle(job)
        raise OSError("job setup failed")
    return k, job


def supervised_run(argv: list[str], env: Mapping[str, str] | None = None, timeout: float | None = None) -> Any:
    """Run argv (shell=False) and always end its process tree: on normal exit, timeout, Ctrl-C or
    any error in this wrapper. Raises subprocess.TimeoutExpired after the kill on timeout."""
    kwargs: dict[str, Any] = {"start_new_session": True} if os.name != "nt" else {}
    proc = subprocess.Popen(argv, env=None if env is None else dict(env), shell=False, **kwargs)
    guard = _TreeGuard(proc)
    try:
        code = proc.wait(timeout=timeout)
    except BaseException:
        guard.kill()
        proc.wait()
        raise
    finally:
        if os.name != "nt":
            guard.kill()  # stragglers in the group; the child already exited
        guard.close()
    return SimpleNamespace(returncode=code)


def run(route_class: str, task: str, *, allow_free: bool = False, env: Mapping[str, str] | None = None,
        config_path: Path | None = None, binary: str | None = None, timeout: float | None = None,
        runner: Callable[..., Any] = supervised_run) -> int:
    try:
        from fleet.token_planner import pinned_opencode_model
    except ImportError:  # executed as a script from the fleet directory
        from token_planner import pinned_opencode_model  # type: ignore[no-redef]
    model_ref = pinned_opencode_model(route_class, allow_free=allow_free)  # raises PlannerError when unresolved
    key = gateway_key(env, config_path)
    config = build_launch_config(model_ref, allow_free=allow_free, provider_block=gateway_provider_block())
    exe = binary or resolve_opencode()
    extra = {"timeout": timeout} if timeout else {}
    with launch_dir(config) as directory:
        result = runner(opencode_argv(model_ref, task, exe), env=launch_env(directory, env, key), **extra)
    return int(getattr(result, "returncode", 0) or 0)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run opencode under a generated, provider-restricted config.")
    ap.add_argument("--class", dest="route_class", required=True, help="routing.schema.json task class")
    ap.add_argument("--allow-free", action="store_true",
                    help="also allow opencode/*-free models (outside the ZDR gateway guarantee)")
    ap.add_argument("--timeout", type=float, default=None, help="seconds; the whole OpenCode process tree is killed")
    ap.add_argument("task", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    task = " ".join(a for a in args.task if a != "--").strip()
    if not task:
        print("error: no task given", file=sys.stderr)
        return 2
    try:
        return run(args.route_class, task, allow_free=args.allow_free, timeout=args.timeout)
    except ValueError as exc:  # LaunchError and PlannerError are both ValueError
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print("error: timed out; the OpenCode process tree was killed", file=sys.stderr)
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
