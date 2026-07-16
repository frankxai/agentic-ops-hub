#!/usr/bin/env python3
"""Append-only fleet activity log + day calendar (multi-agent shared visibility)."""
from __future__ import annotations

import argparse
import socket
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACT = ROOT / "fleet" / "activity"
LOG = ACT / "ACTIVITY-LOG.md"
CAL = ACT / "calendar"

MACHINE_MAP = {"DESKTOP-1B4ICID": "c940"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def detect_machine() -> str:
    h = socket.gethostname()
    for hint, mid in MACHINE_MAP.items():
        if hint.lower() in h.lower():
            return mid
    hl = h.lower()
    if "yoga" in hl or "book" in hl:
        return "yoga-book"
    return "unknown"


def ensure_log_header() -> None:
    ACT.mkdir(parents=True, exist_ok=True)
    CAL.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text(
            "# Fleet ACTIVITY-LOG (append-only)\n\n"
            "Newest entries at the **bottom**. Do not rewrite history.\n"
            "See `fleet/activity/README.md`.\n\n",
            encoding="utf-8",
        )


def append_entry(
    *,
    machine: str,
    agent: str,
    did: str,
    evidence: str = "",
    nxt: str = "",
    queue: str = "none",
) -> str:
    ensure_log_header()
    now = utc_now()
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    block = (
        f"### {ts} · {machine} · {agent} · event\n"
        f"- **Did:** {did}\n"
        f"- **Evidence:** {evidence or '—'}\n"
        f"- **Proposed next:** {nxt or '—'}\n"
        f"- **Queue impact:** {queue}\n\n"
    )
    with LOG.open("a", encoding="utf-8") as f:
        f.write(block)

    day = CAL / f"{now.date().isoformat()}.md"
    if not day.exists():
        day.write_text(
            f"# Calendar · {now.date().isoformat()}\n\n"
            f"## Timeline (UTC)\n\n",
            encoding="utf-8",
        )
    with day.open("a", encoding="utf-8") as f:
        f.write(f"- `{now.strftime('%H:%M')}Z` **{machine}/{agent}**: {did}")
        if evidence:
            f.write(f" → `{evidence}`")
        f.write("\n")
    return ts


def cmd_log(args: argparse.Namespace) -> int:
    mid = args.machine or detect_machine()
    ts = append_entry(
        machine=mid,
        agent=args.agent,
        did=args.did,
        evidence=args.evidence or "",
        nxt=args.next or "",
        queue=args.queue or "none",
    )
    print(f"logged {ts} machine={mid}")
    return 0


def cmd_tail(args: argparse.Namespace) -> int:
    ensure_log_header()
    lines = LOG.read_text(encoding="utf-8").splitlines()
    n = max(1, args.n)
    # print last n entry headers roughly
    print("\n".join(lines[-n:]))
    return 0


def cmd_today(_: argparse.Namespace) -> int:
    ensure_log_header()
    day = CAL / f"{utc_now().date().isoformat()}.md"
    if day.exists():
        print(day.read_text(encoding="utf-8"))
    else:
        print(f"(no calendar file yet for {day.name})")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Fleet shared activity log")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("log", help="Append a timestamped activity entry")
    s.add_argument("--machine", default=None)
    s.add_argument("--agent", required=True)
    s.add_argument("--did", required=True)
    s.add_argument("--evidence", default="")
    s.add_argument("--next", dest="next", default="")
    s.add_argument("--queue", default="none")
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("tail", help="Show end of ACTIVITY-LOG")
    s.add_argument("-n", type=int, default=40)
    s.set_defaults(func=cmd_tail)

    s = sub.add_parser("today", help="Show today's calendar file")
    s.set_defaults(func=cmd_today)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
