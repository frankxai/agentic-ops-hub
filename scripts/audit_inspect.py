"""Read-only config inspector for the agent setup audit (ops/plans/2026-10-22-audit-runbook.md).

Usage: python -I scripts/audit_inspect.py <config.json> [...]
"""
import json
import re
import sys
import urllib.parse as up

# Read-only. Prints JSON pointers, value CLASSES and hostnames. Never prints a secret value.
SECRET_KEYS = re.compile(r"(api[_-]?key|token|secret|password|authorization|bearer)", re.I)
ENDPOINT_KEYS = {"baseurl", "api", "npm"}

def cls(v):
    if not isinstance(v, str): return type(v).__name__
    if re.fullmatch(r"\{env:[A-Z0-9_]+\}", v) or re.fullmatch(r"\$\{?[A-Z0-9_]+\}?", v): return "env-reference"
    return "LITERAL(not shown)"

def host(v):
    try: return up.urlparse(v).hostname or "unparsed"
    except Exception: return "unparsed"

def walk(n, p=""):
    if isinstance(n, dict):
        for k, v in n.items():
            q = f"{p}/{k}"
            lk = k.lower()
            if SECRET_KEYS.search(k) and not isinstance(v, (dict, list)):
                print(f"SECRET-FIELD {q}: {cls(v)}")
            elif lk == "baseurl" and isinstance(v, str):
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
    for f in argv:
        print(f"== {f.replace(chr(92), '/').rsplit('/', 1)[-1]}")
        with open(f, encoding="utf-8") as fh:
            walk(json.load(fh))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
