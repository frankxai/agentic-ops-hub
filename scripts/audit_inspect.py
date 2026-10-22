"""Read-only config inspector for the agent setup audit (ops/plans/2026-10-22-audit-runbook.md).

Usage: python -I scripts/audit_inspect.py <config.json|config.jsonc> [...]

Reads JSON and JSONC (comments and trailing commas). It does NOT read TOML (Codex) or YAML:
those files are reported as UNREADABLE and must be inspected by hand under the runbook's evidence rules.
"""
import json
import re
import sys
import urllib.parse as up

# Read-only. Prints JSON pointers, value CLASSES and hostnames. Never prints a secret value.
SECRET_KEYS = re.compile(r"(api[_-]?key|token|secret|password|authorization|bearer)", re.I)
ENDPOINT_KEYS = {"baseurl", "api", "npm"}


def is_base_url_name(lk):
    # baseURL, base_url, ANTHROPIC_BASE_URL, OPENAI_BASE_URL, OPENAI_API_BASE ...
    return lk == "baseurl" or lk.endswith("base_url") or lk.endswith("_api_base")


def cls(v):
    if not isinstance(v, str): return type(v).__name__
    if re.fullmatch(r"\{env:[A-Z0-9_]+\}", v) or re.fullmatch(r"\$\{?[A-Z0-9_]+\}?", v): return "env-reference"
    return "LITERAL(not shown)"


def host(v):
    try: return up.urlparse(v).hostname or "unparsed"
    except Exception: return "unparsed"


def strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas, leaving string contents untouched."""
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1]); i += 2; continue
            if c == '"': in_str = False
            i += 1; continue
        if c == '"':
            in_str = True; out.append(c); i += 1; continue
        if c == "/" and text[i:i + 2] == "//":
            while i < n and text[i] not in "\r\n": i += 1
            continue
        if c == "/" and text[i:i + 2] == "/*":
            end = text.find("*/", i + 2)
            i = n if end < 0 else end + 2
            continue
        out.append(c); i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def walk(n, p=""):
    if isinstance(n, dict):
        for k, v in n.items():
            q = f"{p}/{k}"
            lk = k.lower()
            if SECRET_KEYS.search(k) and not isinstance(v, (dict, list)):
                print(f"SECRET-FIELD {q}: {cls(v)}")
            elif is_base_url_name(lk) and isinstance(v, str):
                print(f"ENDPOINT {q}: host={host(v)}")
            elif lk in ENDPOINT_KEYS:
                print(f"ENDPOINT-FIELD {q}: present")
            elif lk in {"enabled_providers", "disabled_providers"}:
                print(f"{lk.upper()} {q}: {json.dumps(v)}")
            elif lk in {"model", "small_model"} and isinstance(v, str):
                print(f"MODEL {q}: provider-prefix={v.split('/')[0]}")
            elif lk == "fallback_models" and isinstance(v, list):
                print(f"FALLBACKS {q}: prefixes={[str(x).split('/')[0] for x in v]}")
            walk(v, q)
    elif isinstance(n, list):
        for i, v in enumerate(n): walk(v, f"{p}/{i}")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    status = 0
    for f in argv:
        print(f"== {f.replace(chr(92), '/').rsplit('/', 1)[-1]}")
        try:
            with open(f, encoding="utf-8") as fh:
                data = json.loads(strip_jsonc(fh.read()))
        except (OSError, ValueError):
            # Never echo the parser message: it can quote file content.
            print("UNREADABLE: not JSON or JSONC (TOML and YAML are not supported); inspect by hand")
            status = 1
            continue
        walk(data)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
