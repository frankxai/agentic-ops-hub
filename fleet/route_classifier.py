#!/usr/bin/env python3
"""Starlight routing classifier: task prompt -> task class.

Regex rules only. Unmatched text defaults to the free scout class; there is no
LLM call. LLM_PROMPT below is kept for a future free-model classifier.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "routing.schema.json"

# Keyword rules, first match wins. Paid classes need an explicit multi-word or
# unambiguous signal; a single common word ("plan", "complex", "novel") must
# never lift a task out of the free tier.
FAST_RULES = [
    ("vision",        re.compile(r"\b(screenshots?|screencasts?|video|multimodal|looker|ui mock(up)?s?|analy[sz]e (the |this )?(image|photo|picture))\b", re.I)),
    ("ultrabrain",    re.compile(r"\b(ultrabrain|deep think|research-grade|greenfield|from scratch)\b", re.I)),
    ("hard-reasoning",re.compile(r"\b(root[- ]cause|multi[- ]?step|deep codegen|long[- ]context|hard[- ]reasoning|plan the (migration|rollout|architecture)|reason (about|through))\b", re.I)),
    ("bulk",          re.compile(r"\b((extract|classify|summari[sz]e) (all|many|every|bulk)|bulk|batch)\b", re.I)),
    ("review",        re.compile(r"\b(review|lint|audit|best practices?|style guide)\b", re.I)),
    ("code",          re.compile(r"\b(implement|refactor|edit|fix|write|add (a )?(feature|test|function)|rename|change|update (the )?(file|function|module)|create|build)\b", re.I)),
    ("scout",         re.compile(r"\b(find|search|locate|list|explore|scout|map (the )?codebase|where is|show|read|summari[sz]e|what|how|why|explain|describe)\b", re.I)),
]

DEFAULT_CLASS = "scout"  # free; "Default to free tier" is a schema routing rule

LLM_PROMPT = """Classify the following task into exactly one of these classes:
scout, review, bulk, code, hard-reasoning, vision, ultrabrain.

Definitions:
- scout: fast exploration, file search, codebase mapping
- review: code review, lint, style, best-practice
- bulk: high-volume extraction, classification, summaries
- code: everyday coding, edits, refactoring, docs
- hard-reasoning: complex multi-step reasoning, deep codegen, planning
- vision: image/video/multimodal analysis
- ultrabrain: hardest tasks, max reasoning

Task: {task}

Reply with ONLY the class name, nothing else."""


def fast_classify(task: str) -> str | None:
    for cls, pat in FAST_RULES:
        if pat.search(task):
            return cls
    return None


def classify(task: str) -> dict:
    cls = fast_classify(task)
    source = "fast-path"
    if cls is None:
        cls, source = DEFAULT_CLASS, "default-free"
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    route = schema["task_classes"][cls]
    return {
        "task": task,
        "class": cls,
        "source": source,
        "primary": route["primary"],
        "variant": route["variant"],
        "fallbacks": route["fallbacks"],
        "cost_ceiling_usd": route["cost_ceiling_usd"],
        "zdr_required": route["zdr_required"],
    }


def main():
    ap = argparse.ArgumentParser(description="Classify a task into a routing class.")
    ap.add_argument("task", nargs="+", help="Task description")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()
    task = " ".join(args.task)
    result = classify(task)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"class={result['class']}  source={result['source']}  primary={result['primary']}  variant={result['variant']}")


if __name__ == "__main__":
    main()
