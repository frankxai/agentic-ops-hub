#!/usr/bin/env python3
"""No-agent pulse: write latest receipt; stdout only on non-GREEN or --force."""
from __future__ import annotations
import json
import sys
from pathlib import Path

# allow import from same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from topology_health import build_receipt, hermes_home  # type: ignore

def main() -> int:
    home = hermes_home()
    out = home / "state" / "topology-health-latest.json"
    # also mirror into agentic-ops if present
    mirrors = [
        Path(r"C:/Users/frank/agentic-ops/fleet/reports/topology-health-latest.json"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-night-loops-20260806/fleet/reports/topology-health-latest.json"),
    ]
    receipt = build_receipt(write_path=out)
    for m in mirrors:
        try:
            m.parent.mkdir(parents=True, exist_ok=True)
            m.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        except OSError:
            pass
    force = "--force" in sys.argv
    if receipt.get("status") == "GREEN" and not force:
        return 0
    # compact changed-only stdout for telegram/local delivery
    compact = {
        "status": receipt.get("status"),
        "disk_free_gb": receipt.get("planes", {}).get("disk_free_gb"),
        "gateways_running": receipt.get("planes", {}).get("gateways_running"),
        "findings": receipt.get("findings", [])[:8],
        "next_actions": receipt.get("next_actions", [])[:5],
        "written_to": str(out),
    }
    print(json.dumps(compact, indent=2))
    return 0 if receipt.get("status") != "RED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
