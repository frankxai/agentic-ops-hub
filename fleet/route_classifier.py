#!/usr/bin/env python3
"""Starlight routing classifier: task prompt -> task class.

Regex and word lists only; there is no LLM call. LLM_PROMPT below is kept for a
future free-model classifier.

Fail closed, by a closed grammar and not a blacklist. A request may reach a free,
non-ZDR class only when ALL of these hold:
  (a) it opens with a word from READ_ONLY_VERBS;
  (b) it has at most MAX_FREE_WORDS words;
  (c) every other word is in the closed vocabulary (function words and plain
      nouns, no verbs) or is a file name or path whose extension we know (see
      _data_token). Joined words (a-b, a_b) must have every part in the vocabulary;
  (d) it uses only letters, digits, spaces and . / _ - (one trailing ? or . is
      ignored). Quotes are not allowed: quoted text is never routed free;
  (e) it names nothing sensitive (SENSITIVE substrings, matched anywhere).
Any unknown word means ZDR. A verb nobody listed ("erase", "unlink", "nuke") is
unknown, so it cannot reach a free model. The cost is Token Pass credit for
requests that are harmless but use a word we do not know.

This is a cost heuristic, not the security boundary. Rounds 4-6 of review kept
finding phrasings a word list misses. The guarantee that ZDR work cannot reach a
non-ZDR provider is a gateway key that can only reach ZDR providers.
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
    "package", "packages", "repo", "repos", "repository", "codebase", "text", "document",
    "documents", "doc", "docs", "readme", "plan", "script", "scripts", "error", "errors", "log",
    "logs", "output", "outputs", "suite", "config", "configuration", "setting",
    "settings", "schema", "schemas", "field", "fields", "name", "names", "line",
    "lines", "word", "words", "variable", "variables", 
    "dependency", "dependencies", "endpoint", "endpoints", "handler", "logic",
    "flow", "chain", "diff", "pr", "style", "rules", "rule", "layout", "structure", "size",
    "number", "src", "lib", "app", "bin", "root", "branch", "branches", "reason", "cause",
    "difference", "purpose", "meaning", "usage", "example", "examples", 
    "version", "date", "time", "history", "table", "tables", "column", "columns", "row", "rows",
    "api", "cli", "command", "commands", "option", "options", "argument",
    "arguments", "parameter", "parameters", "value", "values", "result", "results", "task", "tasks",
    "dataset", "service", "services", "server", "component", "components", "page", "pages", "site",
    "dashboard", "model", "models", "provider", "providers", "receipt", "receipts", "ledger",
    "budget", "cost", "ceiling", "cap", "screenshot", "screenshots", "screencast", "screencasts",
    "video", "videos", "image", "images", "photo", "photos", "picture", "pictures", "mockup",
    "mockups", "chart", "thumbnail", "python", "javascript", "typescript", "json", "yaml",
    "markdown", "sql", "list", 
})
# Nouns that are also everyday commands ("code a login", "test it", "route it") stay out
# of NOUNS, so they cannot hide an action behind a read-only opening.
VOCABULARY = FUNCTION_WORDS | NOUNS
EXTENSIONS = frozenset({"py", "js", "ts", "tsx", "jsx", "md", "json", "yaml", "yml", "toml", "txt", "csv", "html", "css"})
# (e) Anything that smells of a credential goes to ZDR, matched as a substring of the
# whole request, case-insensitively: ".env", "api_key", "passwords.txt", "id_rsa".
SENSITIVE = ("env", "key", "token", "secret", "password", "passwd", "credential", "cred", "pem", "ssh",
             "auth", "cert", "private", "wallet", "seed", "mnemonic", "bearer", "jwt", "rsa", "gpg")

# A token made of letters/digits joined by . / _ - with no separator at either end (a leading
# ./ ../ ~/ or . is fine). Whether it is data is decided by _data_token, not by this shape.
IDENTIFIER = re.compile(r"[./~]{0,2}[A-Za-z0-9]+(?:[./_-][A-Za-z0-9]+)*")
ALLOWED_CHARS = re.compile(r"[A-Za-z0-9 ./_-]+")
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


def _piece_ok(piece: str, bare: bool) -> bool:
    return piece.lower() in VOCABULARY or any(c.isdigit() for c in piece) or not bare


def _data_token(token: str) -> bool:
    """A file name or path is data, but joined words are not: "then-delete-it" and "wipe_disk"
    must have every part in the vocabulary. A lone word counts as data only inside a path or
    file name, and a dotted name must end in a known extension (or carry a digit, like v1.2)."""
    if not IDENTIFIER.fullmatch(token):
        return False
    body = token.lstrip("./~")
    in_path = "/" in body or "." in body
    for seg in body.split("/"):
        stem, dot, ext = seg.rpartition(".")
        if not dot:
            stem = seg
        elif ext.lower() not in EXTENSIONS and not any(c.isdigit() for c in seg):
            return False
        for part in stem.split("."):
            pieces = [p for p in re.split(r"[_-]", part) if p]
            if not all(_piece_ok(p, bare=not in_path or len(pieces) > 1) for p in pieces):
                return False
    return True


def is_short_read_only(task: str) -> bool:
    """The closed grammar for free routing. See the module docstring."""
    text = task.strip()
    if text.endswith(("?", ".")):
        text = text[:-1].rstrip()
    if not text or len(text.split()) > MAX_FREE_WORDS or not ALLOWED_CHARS.fullmatch(text):
        return False
    if any(word in text.lower() for word in SENSITIVE):
        return False
    tokens = text.split()
    if tokens[0].lower() not in READ_ONLY_VERBS:
        return False
    return all(t.lower() in VOCABULARY or _data_token(t) for t in tokens[1:])


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
