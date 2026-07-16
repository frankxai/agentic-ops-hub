#!/usr/bin/env python3
"""Lightweight fleet bus helpers for multi-machine coordination.

SSOT dirs: agentic-ops/fleet/bus/{identity,heartbeats,inbox,queues}
Only write heartbeats for THIS machine (never forge peer heartbeats).
"""
from __future__ import annotations

import argparse
import json
import platform
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

BUS_ROOT = Path(__file__).resolve().parents[1] / "bus"
MACHINE_MAP = {
    "DESKTOP-1B4ICID": "c940",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def detect_machine() -> str:
    host = socket.gethostname()
    node = platform.node()
    for hint, mid in MACHINE_MAP.items():
        if hint.lower() in host.lower() or hint.lower() in node.lower():
            return mid
    # yoga-book: only if hostname contains yoga/book (set on first boot)
    h = f"{host} {node}".lower()
    if "yoga" in h or "book" in h:
        return "yoga-book"
    return "unknown"


def cmd_identity(_: argparse.Namespace) -> int:
    mid = detect_machine()
    payload = {
        "machine_id": mid,
        "hostname": socket.gethostname(),
        "node": platform.node(),
        "platform": platform.platform(),
        "at": utc_now(),
    }
    path = BUS_ROOT / "identity" / f"{mid}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if mid == "unknown":
        print("WARN: hostname not mapped — update MACHINE_MAP / clone-manifest", file=sys.stderr)
        return 2
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    mid = args.machine or detect_machine()
    if mid == "unknown":
        print("REFUSE: unknown machine — will not write heartbeat", file=sys.stderr)
        return 2
    # Never forge: only self
    self_id = detect_machine()
    if mid != self_id:
        print(f"REFUSE: cannot write heartbeat for {mid} from host mapped as {self_id}", file=sys.stderr)
        return 3
    payload = {
        "machine_id": mid,
        "hostname": socket.gethostname(),
        "status": args.status,
        "role": "always-on-backend-content-ops" if mid == "c940" else "frontend-innovation",
        "telegram_bot": "@lenovostarlightbot" if mid == "c940" else "@Hermesyogabookbot",
        "notes": args.notes or "",
        "at": utc_now(),
    }
    path = BUS_ROOT / "heartbeats" / f"{mid}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    mid = detect_machine()
    beats = sorted((BUS_ROOT / "heartbeats").glob("*.json")) if (BUS_ROOT / "heartbeats").exists() else []
    out = {"self": mid, "heartbeats": []}
    for p in beats:
        try:
            out["heartbeats"].append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            out["heartbeats"].append({"file": p.name, "error": str(e)})
    print(json.dumps(out, indent=2))
    return 0


def cmd_swarm_line(_: argparse.Namespace) -> int:
    """One-line bulletin suitable for hermes send (stdout only)."""
    mid = detect_machine()
    host = socket.gethostname()
    beat_path = BUS_ROOT / "heartbeats" / f"{mid}.json"
    status = "unknown"
    if beat_path.exists():
        try:
            status = json.loads(beat_path.read_text(encoding="utf-8")).get("status", "unknown")
        except Exception:
            pass
    print(f"[{mid}] host={host} status={status} at={utc_now()} · bus=fleet/bus · driver=fleet/STARLIGHT-SWARM-DRIVER.md")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Fleet bus (lightweight)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("identity", help="Write identity file for this host")
    s.set_defaults(func=cmd_identity)

    s = sub.add_parser("heartbeat", help="Write self heartbeat only")
    s.add_argument("--machine", default=None, help="Must match self; default=detect")
    s.add_argument("--status", default="live")
    s.add_argument("--notes", default="")
    s.set_defaults(func=cmd_heartbeat)

    s = sub.add_parser("status", help="Show self + all heartbeats")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("swarm-line", help="One-line status for Telegram bus")
    s.set_defaults(func=cmd_swarm_line)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
