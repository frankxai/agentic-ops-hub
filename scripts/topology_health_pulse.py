#!/usr/bin/env python3
"""No-agent pulse: write latest receipt; stdout only on non-GREEN or --force.

Hermes no_agent semantics: empty stdout = silent success; non-empty stdout =
deliver alert with success=True; non-zero exit is treated as *script failure*
(not a health finding). Always exit 0 after a successful receipt build so RED
surfaces as a clean alert, matching peer watchdogs (disk/travel/sentinel).
CLI gating (exit 2 on RED) stays on topology_health.py --write only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topology_health import assert_safe_write_path, build_receipt, hermes_home  # type: ignore


def main() -> int:
    home = hermes_home()
    out = home / "state" / "topology-health-latest.json"
    # Prefer repo-relative mirrors only when parent already exists (no mkdir climb).
    mirrors = [
        Path(__file__).resolve().parents[1] / "fleet" / "reports" / "topology-health-latest.json",
        Path(r"C:/Users/frank/agentic-ops/fleet/reports/topology-health-latest.json"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-night-loops-20260806/fleet/reports/topology-health-latest.json"),
    ]
    receipt = build_receipt(write_path=out)
    mirror_errors: list[str] = []
    for m in mirrors:
        if not m.parent.is_dir():
            continue
        try:
            safe = assert_safe_write_path(m, home)
            safe.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        except (OSError, ValueError) as exc:
            mirror_errors.append(f"{m}: {exc}")
    force = "--force" in sys.argv
    if receipt.get("status") == "GREEN" and not force and not mirror_errors:
        return 0
    compact = {
        "status": receipt.get("status"),
        "disk_free_gb": receipt.get("planes", {}).get("disk_free_gb"),
        "gateways_running": receipt.get("planes", {}).get("gateways_running"),
        "findings": receipt.get("findings", [])[:8],
        "next_actions": receipt.get("next_actions", [])[:5],
        "written_to": str(out),
        "mirror_errors": mirror_errors[:5],
    }
    print(json.dumps(compact, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
