#!/usr/bin/env python3
"""Generate the OmO config (~/.omo/omo.jsonc) from routing.schema.json (single source of truth).

Run after editing routing.schema.json to keep OmO config in sync:

    python gen_omo_config.py --dry-run          # print, write nothing
    python gen_omo_config.py --out PATH         # write somewhere else
    python gen_omo_config.py                    # write ~/.omo/omo.jsonc, backing up the old file
    python gen_omo_config.py --allow-free-agents  # keep opencode/*-free models (outside the ZDR gateway key)

By default no slot uses an opencode/* free model. Those calls go to OpenCode's own
endpoint, not through the Vercel gateway, so a ZDR-only gateway key cannot cover them.
Free-class slots (scout, review, vision) are mapped to the cheapest ZDR model in the
schema's token_pass.models instead, through route_executor.effective_route(), the same
function the executor admits and records calls with. That costs Token Pass credit and a text-only model
stands in for vision until a ZDR vision model is listed in the schema.

Every agent and category gets an explicit model list built from the schema's
chains. OmO falls back to its own built-in chains (which name paid openai,
anthropic and google models) for any slot without a list, so no slot may be
left bare, including the built-in ones that are not in the maps below.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from route_executor import cheapest_zdr_model, effective_route  # noqa: E402,F401

SCHEMA = HERE / "routing.schema.json"
OMO = Path.home() / ".omo" / "omo.jsonc"

# OmO agent -> schema task class. Only agents that never edit (explore, librarian,
# multimodal-looker, momus) sit on free chains; anything that can execute work, the
# junior executor included, is on a ZDR class.
AGENT_MAP = {
    "sisyphus": "code",
    "sisyphus-junior": "code",
    "hephaestus": "code",
    "oracle": "hard-reasoning",
    "prometheus": "hard-reasoning",
    "metis": "ultrabrain",
    "atlas": "code",
    "librarian": "scout",
    "explore": "scout",
    "multimodal-looker": "vision",
    "momus": "review",
}

# OmO category -> schema task class. Includes built-in categories that must not
# reach OmO's own paid chains (deep-high, artistry, deep-low).
CATEGORY_MAP = {
    "visual-engineering": "code",
    "ultrabrain": "ultrabrain",
    "deep": "hard-reasoning",
    "deep-low": "code",
    "deep-high": "hard-reasoning",
    "artistry": "code",
    "quick": "code",
    "unspecified-low": "code",
    "unspecified-high": "code",
    "writing": "code",
    "research": "hard-reasoning",
    "bulk-extraction": "bulk",
    "code-review": "review",
}

# OmO refuses non-GPT models for these agents unless told otherwise.
ALLOW_NON_GPT = ("hephaestus",)


def _entry(model: str, variant: str | None) -> object:
    return {"model": model, "reasoning": variant} if variant else model


def build(schema: dict, allow_free_agents: bool = False) -> dict:
    classes = schema["task_classes"]

    def zdr_only(cls: str) -> bool:
        return classes[cls]["zdr_required"] or not allow_free_agents

    def models_for(cls: str) -> list:
        chain = effective_route(schema, cls, allow_free=allow_free_agents)["chain"]
        variant = classes[cls]["variant"]
        return [_entry(chain[0], variant)] + chain[1:]

    agents = {}
    for agent, cls in AGENT_MAP.items():
        agents[agent] = {"models": models_for(cls)}
        if agent in ALLOW_NON_GPT:
            agents[agent]["allow_non_gpt_model"] = True

    categories = {}
    for cat, cls in CATEGORY_MAP.items():
        ms = models_for(cls)
        first = ms[0]
        entry = {"model": first["model"] if isinstance(first, dict) else first}
        if isinstance(first, dict):
            entry["reasoning"] = first["reasoning"]
        # Always explicit and, for a ZDR class, never empty. A category without the
        # key inherits the fallbacks of the delegating agent. OmO's
        # applyDisabledProviders() also turns [] into undefined, which makes the
        # category inherit them again, and those are free models. A singleton ZDR
        # chain therefore repeats its own primary as the only fallback.
        fallbacks = ms[1:]
        if not fallbacks and zdr_only(cls):
            fallbacks = [entry["model"]]
        entry["fallback_models"] = fallbacks
        categories[cat] = entry

    return {
        "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/omo.schema.json",
        "[opencode]": {
            "agents": agents,
            "categories": categories,
            "model_fallback": True,
        },
        "_migrations": schema.get("_migrations", []),
    }


def render(out: dict, allow_free_agents: bool = False) -> str:
    head = "// OMO configuration — GENERATED from routing.schema.json (do not hand-edit)\n"
    if allow_free_agents:
        head += ("// --allow-free-agents: opencode/* free models are in use. Those calls go to OpenCode's endpoint,\n"
                 "// outside the Vercel gateway key, so the ZDR guarantee does not cover them.\n"
                 "// Use only in repos with nothing confidential.\n")
    else:
        head += "// ZDR mode: every slot uses a gateway model; no opencode/* free model is configured.\n"
    return head + json.dumps(out, indent=2) + "\n"


def _backup(path: Path) -> Path:
    """Copy path to a backup name that cannot collide, never replacing an existing backup."""
    for _ in range(100):
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S-%fZ")
        backup = path.with_name(f"{path.name}.bak.{stamp}-{os.urandom(3).hex()}")
        try:
            with open(path, "rb") as src, open(backup, "xb") as dst:
                shutil.copyfileobj(src, dst)
        except FileExistsError:
            continue
        shutil.copystat(path, backup)
        return backup
    raise RuntimeError(f"could not create a unique backup name for {path}")


def _install(out: Path, text: str) -> None:
    """Write text to out through a temp file only this invocation owns, so two runs
    can never install each other's output."""
    fd, name = tempfile.mkstemp(prefix=out.name + ".", suffix=".tmp", dir=out.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        for attempt in range(50):
            try:
                tmp.replace(out)
                break
            except PermissionError:  # Windows: another invocation is replacing the same target right now
                if attempt == 49:
                    raise
                time.sleep(0.01)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OMO, help="Output path (default ~/.omo/omo.jsonc)")
    ap.add_argument("--dry-run", action="store_true", help="Print the config, write nothing")
    ap.add_argument("--allow-free-agents", action="store_true",
                    help="Keep opencode/* free models for scout, review and vision (outside the ZDR gateway key)")
    args = ap.parse_args(argv)

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    text = render(build(schema, args.allow_free_agents), args.allow_free_agents)
    if args.dry_run:
        print(text, end="")
        return
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        backup = _backup(args.out)
        print(f"Backed up {args.out} -> {backup}")
    _install(args.out, text)
    print(f"Wrote {args.out}")
    print("Restart OpenCode/OmO to pick up changes.")


if __name__ == "__main__":
    main()
