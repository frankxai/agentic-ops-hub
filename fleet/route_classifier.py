#!/usr/bin/env python3
"""Starlight routing classifier: task prompt -> task class.

Regex and word lists only; there is no LLM call. LLM_PROMPT below is kept for a
future free-model classifier.

Fail closed, by a closed grammar and not a blacklist. A request may reach a free,
non-ZDR class only when ALL of these hold:
  (a) it opens with a word from READ_ONLY_VERBS;
  (b) it has at most MAX_FREE_WORDS words;
  (c) every other word is in the closed vocabulary (function words and plain
      nouns, no verbs) or is path/identifier-like (see IDENTIFIER) or is quoted;
  (d) it uses only letters, digits, spaces and . / _ - ' " (one trailing ? or .
      is ignored).
Any unknown word means ZDR. A verb nobody listed ("erase", "unlink", "nuke") is
unknown, so it cannot reach a free model. The cost is Token Pass credit for
requests that are harmless but use a word we do not know, never a leak.
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

# (a) The only words a free-routed request may open with. All read-only.
# "check" is absent on purpose: "check and fix" starts as a read and ends as an edit.
READ_ONLY_VERBS = frozenset({
    "read", "list", "show", "summarise", "summarize", "explain", "find", "search", "describe",
    "map", "count", "print", "review", "audit", "lint", "analyze", "analyse", "inspect", "locate",
    "where", "what", "how", "why",
})

# (c) Closed vocabulary: function words and plain nouns. No verbs that change or run anything.
FUNCTION_WORDS = frozenset({
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "from", "with", "by", "about", "this", "that",
    "these", "those", "it", "its", "my", "our", "your", "me", "us", "is", "are", "was", "were", "does",
    "do", "did", "all", "each", "every", "any", "some", "many", "most", "first", "last", "top", "main",
    "public", "current", "new", "old", "whole", "entire", "which", "there", "here",
})
NOUNS = frozenset({
    "file", "files", "folder", "folders", "directory", "directories", "dir", "path", "paths",
    "function", "functions", "class", "classes", "method", "methods", "module", "modules",
    "package", "packages", "repo", "repos", "repository", "codebase", "code", "text", "document",
    "documents", "doc", "docs", "readme", "plan", "script", "scripts", "error", "errors", "log",
    "logs", "output", "outputs", "test", "tests", "suite", "config", "configuration", "setting",
    "settings", "schema", "schemas", "key", "keys", "field", "fields", "name", "names", "line",
    "lines", "word", "words", "type", "types", "variable", "variables", "import", "imports",
    "dependency", "dependencies", "endpoint", "endpoints", "route", "routes", "handler", "logic",
    "flow", "order", "chain", "diff", "pr", "style", "rules", "rule", "layout", "structure", "size",
    "number", "src", "lib", "app", "bin", "root", "branch", "branches", "reason", "cause",
    "difference", "purpose", "meaning", "usage", "example", "examples", "comment", "comments",
    "version", "date", "time", "history", "table", "tables", "column", "columns", "row", "rows",
    "api", "cli", "command", "commands", "option", "options", "flag", "flags", "argument",
    "arguments", "parameter", "parameters", "value", "values", "result", "results", "task", "tasks",
    "dataset", "service", "services", "server", "component", "components", "page", "pages", "site",
    "dashboard", "model", "models", "provider", "providers", "receipt", "receipts", "ledger",
    "budget", "cost", "ceiling", "cap", "screenshot", "screenshots", "screencast", "screencasts",
    "video", "videos", "image", "images", "photo", "photos", "picture", "pictures", "mockup",
    "mockups", "chart", "thumbnail", "python", "javascript", "typescript", "json", "yaml",
    "markdown", "sql", "list", "map", "count", "print",
})
VOCABULARY = FUNCTION_WORDS | NOUNS

# (c) Identifier or path: letters/digits joined by . / _ - with no separator at either end
# (a leading ./ ../ ~/ or . is fine), or a token that contains a digit. "erase." and "-rf"
# are not identifiers; "settings.json", "src/app.py", "wipe_disk" and "v2" are.
IDENTIFIER = re.compile(r"[./~]{0,2}[A-Za-z0-9]+(?:[./_-][A-Za-z0-9]+)*")
QUOTED = re.compile(r"\"[^\"]*\"|'[^']*'")
ALLOWED_CHARS = re.compile(r"[A-Za-z0-9 ./_'\"-]+")
MAX_FREE_WORDS = 15

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


def _identifier_like(token: str) -> bool:
    if not IDENTIFIER.fullmatch(token):
        return False
    return any(c in token for c in "./_-") or any(c.isdigit() for c in token)


def is_short_read_only(task: str) -> bool:
    """The closed grammar for free routing. See the module docstring."""
    text = task.strip()
    if text.endswith(("?", ".")):
        text = text[:-1].rstrip()
    if not text or len(text.split()) > MAX_FREE_WORDS or not ALLOWED_CHARS.fullmatch(text):
        return False
    tokens = QUOTED.sub(" 0 ", text).split()  # a quoted span is data, like an identifier
    if not tokens or tokens[0].lower() not in READ_ONLY_VERBS:
        return False
    return all(t.lower() in VOCABULARY or _identifier_like(t) for t in tokens[1:])


def fast_classify(task: str) -> str | None:
    for cls, pat in STRONG_RULES:
        if pat.search(task):
            return cls
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
