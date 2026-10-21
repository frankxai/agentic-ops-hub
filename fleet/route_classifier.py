#!/usr/bin/env python3
"""Starlight routing classifier: task prompt -> task class.

Regex rules only; there is no LLM call. LLM_PROMPT below is kept for a future
free-model classifier.

Fail closed: only an explicit read-only request (find, list, explain, review,
analyze this screenshot ...) may reach a free, non-ZDR class. A request that
changes something, and any request with no recognised signal, goes to a ZDR
class, because the text may carry code or data that must not leave on a free
model. The cost of a wrong guess is Token Pass credit, never a leak.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "routing.schema.json"

# Strong signals, first match wins. All ZDR classes.
STRONG_RULES = [
    ("ultrabrain",    re.compile(r"\b(ultrabrain|deep think|research-grade|greenfield|from scratch)\b", re.I)),
    ("hard-reasoning",re.compile(r"\b(root[- ]cause|multi[- ]?step|deep codegen|long[- ]context|hard[- ]reasoning|plan the (migration|rollout|architecture)|reason (about|through))\b", re.I)),
    ("bulk",          re.compile(r"\b((extract|classify|summari[sz]e) (all|many|every|bulk)|bulk|batch)\b", re.I)),
]

# Any word that starts one of these changes something. It beats every read-only
# signal, so "update the screenshot upload handler" can never look like vision.
MUTATION = re.compile(
    r"\b(implement|refactor|edit|fix|write|add|remove|delete|drop|rename|change|update|patch|modify|"
    r"create|build|migrate|replace|rewrite|port|install|deploy|merge|revert|commit|push|apply|insert|"
    r"append|improve|optimi[sz]e|clean|bump|upgrade|wire|make|generate|configure|tweak|move|handle|"
    r"support|enable|disable|set up|correct|repair|resolve|adjust|rework|address)\w*",
    re.I,
)

# Free-eligible only when the request OPENS with a read-only verb or question word.
# A keyword anywhere else is not enough ("code a search function").
READ_ONLY = re.compile(
    r"^\W*(?:(?:please|can you|could you|just)\s+)*"
    r"(?:find|search|locate|list|explore|scout|map (?:the )?codebase|where is|show|read|summari[sz]e|"
    r"what|how|why|explain|describe|review|lint|audit|best practices?|style guide|"
    r"analy[sz]e|inspect|look (?:up|at))\b",
    re.I,
)

# Looking at media: a read-only verb directly in front of the media noun, and the
# noun not the head of a code phrase ("screenshot upload handler").
VISION = re.compile(
    r"\b(analy[sz]e|describe|inspect|look at|read|explain|review|summari[sz]e|what(?:'s| is) in)\s+"
    r"(?:(?:this|the|that|my|these|attached)\s+)?"
    r"(?:screenshots?|screencasts?|videos?|images?|photos?|pictures?|ui mock(?:up)?s?)\b"
    r"(?!\s+(?:upload|handler|parser|validation|bug|code|function|module|endpoint|player|component|"
    r"pipeline|processor|encoder|decoder|api|service|test|tests|logic|renderer|worker))",
    re.I,
)
REVIEW = re.compile(r"\b(review|lint|audit|best practices?|style guide)\b", re.I)

# Whole words that change something or run something, on top of MUTATION above.
# "code" only counts as a verb ("code a login function"), not in "review the code".
ACTION_WORDS = re.compile(
    r"\b(?:save|store|run|execute|exec|send|post|upload|copy|export|dump|overwrite|truncate|kill|"
    r"restart|launch|publish|release|ship|sync|pull|clone|download|mount|pipe|redirect|tee|touch|"
    r"chmod|sudo|rm|mv|cp)(?:s|es|d|ed|ing)?\b"
    r"|\bcode\s+(?:a|an|the|up|me|it|that|this|new|some)\b",
    re.I,
)

# Anything that joins or chains requests. One short question has none of these.
CLAUSE_BREAK = re.compile(
    r"\b(?:and|or|then|also|next|afterwards?|after that|before|once|plus|while)\b"
    r"|[;&+\n`|<>$]|->|=>|[,:]\s|[.!?]\s+\S",
    re.I,
)

MAX_FREE_WORDS = 30  # a longer request is not a short single question

DEFAULT_CLASS = "code"  # ZDR; no recognised signal means do not send it to a free model

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


def is_short_read_only(task: str) -> bool:
    """True only for one short clause that opens with a read-only verb and holds
    no mutation or action word anywhere. Everything else stays on a ZDR class."""
    text = task.strip()
    if not text or len(text.split()) > MAX_FREE_WORDS:
        return False
    if CLAUSE_BREAK.search(text) or MUTATION.search(text) or ACTION_WORDS.search(text):
        return False
    return bool(READ_ONLY.search(text))


def fast_classify(task: str) -> str | None:
    for cls, pat in STRONG_RULES:
        if pat.search(task):
            return cls
    if MUTATION.search(task):
        return "code"
    if not is_short_read_only(task):
        return None
    if VISION.search(task):
        return "vision"
    if REVIEW.search(task):
        return "review"
    return "scout"


def classify(task: str) -> dict:
    cls = fast_classify(task)
    source = "fast-path"
    if cls is None:
        cls, source = DEFAULT_CLASS, "default-zdr"
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
