#!/usr/bin/env python3
"""Generate the OmO config (~/.omo/omo.jsonc) from routing.schema.json (single source of truth).

Run after editing routing.schema.json to keep OmO config in sync:

    python gen_omo_config.py --dry-run          # print, write nothing
    python gen_omo_config.py --out PATH         # write somewhere else
    python gen_omo_config.py                    # write ~/.omo/omo.jsonc, backing up the old file

Every agent and category gets an explicit model list built from the schema's
chains. OmO falls back to its own built-in chains (which name paid openai,
anthropic and google models) for any slot without a list, so no slot may be
left bare, including the built-in ones that are not in the maps below.
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from route_executor import zdr_safe_chain  # noqa: E402

SCHEMA = HERE / "routing.schema.json"
OMO = Path.home() / ".omo" / "omo.jsonc"

# OmO agent -> schema task class. Free-class agents are the scout/review/vision chains.
AGENT_MAP = {
    "sisyphus": "code",
    "sisyphus-junior": "scout",
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
    "visual-engineering": "vision",
    "ultrabrain": "ultrabrain",
    "deep": "hard-reasoning",
    "deep-low": "code",
    "deep-high": "hard-reasoning",
    "artistry": "scout",
    "quick": "scout",
    "unspecified-low": "scout",
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


def build(schema: dict) -> dict:
    classes = schema["task_classes"]

    def models_for(cls: str) -> list:
        chain = zdr_safe_chain(schema, cls)
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
        if len(ms) > 1:
            entry["fallback_models"] = ms[1:]
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


def render(out: dict) -> str:
    return "// OMO configuration — GENERATED from routing.schema.json (do not hand-edit)\n" + json.dumps(out, indent=2) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OMO, help="Output path (default ~/.omo/omo.jsonc)")
    ap.add_argument("--dry-run", action="store_true", help="Print the config, write nothing")
    args = ap.parse_args(argv)

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    text = render(build(schema))
    if args.dry_run:
        print(text, end="")
        return
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        backup = args.out.with_name(f"{args.out.name}.bak.{stamp}")
        shutil.copy2(args.out, backup)
        print(f"Backed up {args.out} -> {backup}")
    tmp = args.out.with_name(args.out.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(args.out)
    print(f"Wrote {args.out}")
    print("Restart OpenCode/OmO to pick up changes.")


if __name__ == "__main__":
    main()
