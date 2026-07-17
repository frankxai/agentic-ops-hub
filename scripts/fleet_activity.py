#!/usr/bin/env python3
"""Append-only fleet activity log + day calendar (multi-agent shared visibility).

Cross-machine rule: private Telegram DMs are invisible to peer machines.
Mirror proposals with:  python scripts/fleet_activity.py propose ...
"""
from __future__ import annotations

import argparse
import json
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACT = ROOT / "fleet" / "activity"
LOG = ACT / "ACTIVITY-LOG.md"
CAL = ACT / "calendar"
PROPOSALS = ACT / "proposals.jsonl"
QUEUES = ROOT / "fleet" / "bus" / "queues"

MACHINE_MAP = {"DESKTOP-1B4ICID": "c940", "Starlight": "yoga-book"}


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
    kind: str = "event",
) -> str:
    ensure_log_header()
    now = utc_now()
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    block = (
        f"### {ts} · {machine} · {agent} · {kind}\n"
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
        tag = "proposal" if kind == "proposal" else "event"
        f.write(f"- `{now.strftime('%H:%M')}Z` **{machine}/{agent}** [{tag}]: {did}")
        if evidence:
            f.write(f" → `{evidence}`")
        f.write("\n")
    return ts


def append_proposal_jsonl(record: dict) -> None:
    ACT.mkdir(parents=True, exist_ok=True)
    with PROPOSALS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def maybe_queue_peer(to: str, item: dict) -> str:
    """Append a proposal ticket into fleet/bus/queues/to-<peer>.json if present."""
    if to not in ("c940", "book", "yoga-book"):
        return "none"
    peer = "book" if to in ("book", "yoga-book") else "c940"
    path = QUEUES / f"to-{peer}.json"
    if not path.exists():
        return f"queue file missing: {path.name}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return f"queue read error: {e}"
    items = data.setdefault("items", [])
    items.append(item)
    data["updated_at"] = utc_now().isoformat()
    data.setdefault("from_proposals", [])
    if isinstance(data["from_proposals"], list):
        data["from_proposals"].append(item.get("id"))
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return f"queued {item.get('id')} → {path.name}"


def cmd_log(args: argparse.Namespace) -> int:
    mid = args.machine or detect_machine()
    ts = append_entry(
        machine=mid,
        agent=args.agent,
        did=args.did,
        evidence=args.evidence or "",
        nxt=args.next or "",
        queue=args.queue or "none",
        kind=args.kind or "event",
    )
    print(f"logged {ts} machine={mid} kind={args.kind or 'event'}")
    return 0


def cmd_propose(args: argparse.Namespace) -> int:
    """Mirror a private-DM proposal so peer machines can see it after git pull."""
    mid = args.machine or detect_machine()
    agent = args.agent or ("hermes-book" if mid in ("yoga-book", "unknown") else "hermes-lenovo")
    source = args.source or "private-dm"
    proposal_id = args.id or f"P-{utc_now().strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:6]}"
    title = args.title.strip()
    body = (args.body or "").strip()
    evidence = args.evidence or f"source={source}"
    nxt = args.next or title
    queue_to = (args.queue_to or "").strip().lower()

    did = f"[DM-MIRROR] {title}"
    if body:
        did = f"[DM-MIRROR] {title} — {body}"

    queue_impact = "none"
    item = {
        "id": proposal_id,
        "title": title,
        "body": body,
        "from_machine": mid,
        "from_agent": agent,
        "source": source,
        "at": utc_now().isoformat(),
        "kind": "proposal",
    }
    if queue_to:
        queue_impact = maybe_queue_peer(queue_to, item)

    ts = append_entry(
        machine=mid,
        agent=agent,
        did=did,
        evidence=evidence,
        nxt=nxt,
        queue=queue_impact,
        kind="proposal",
    )
    record = {
        **item,
        "ts": ts,
        "evidence": evidence,
        "proposed_next": nxt,
        "queue_impact": queue_impact,
    }
    append_proposal_jsonl(record)
    print(json.dumps({"ok": True, "ts": ts, "id": proposal_id, "machine": mid, "queue": queue_impact}, indent=2))
    print(
        "\nNEXT: git add fleet/activity scripts/fleet_activity.py "
        f"{'fleet/bus/queues' if queue_to else ''} && git commit -m "
        f"\"activity(book): mirror DM proposal {proposal_id}\" && git push",
        flush=True,
    )
    return 0


def cmd_tail(args: argparse.Namespace) -> int:
    ensure_log_header()
    lines = LOG.read_text(encoding="utf-8").splitlines()
    n = max(1, args.n)
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


def cmd_proposals(args: argparse.Namespace) -> int:
    """Show recent mirrored proposals (JSONL)."""
    if not PROPOSALS.exists():
        print("(no proposals.jsonl yet)")
        return 0
    lines = [ln for ln in PROPOSALS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    n = max(1, args.n)
    for ln in lines[-n:]:
        print(ln)
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
    s.add_argument("--kind", default="event", choices=["event", "proposal", "handoff", "block"])
    s.set_defaults(func=cmd_log)

    s = sub.add_parser(
        "propose",
        help="Mirror a private-DM proposal into ACTIVITY-LOG + proposals.jsonl (cross-machine)",
    )
    s.add_argument("--machine", default=None, help="c940 | yoga-book (default: detect)")
    s.add_argument("--agent", default=None, help="default hermes-book on Book / hermes-lenovo on c940")
    s.add_argument("--title", required=True, help="One-line proposal title")
    s.add_argument("--body", default="", help="Optional detail (keep short; no secrets)")
    s.add_argument("--evidence", default="", help="path / SHA / ticket id")
    s.add_argument("--next", dest="next", default="", help="Proposed next action")
    s.add_argument("--source", default="private-dm", help="private-dm | swarm | human | other")
    s.add_argument("--id", default=None, help="Optional stable proposal id")
    s.add_argument(
        "--queue-to",
        default="",
        help="Optional: c940 | book — also append ticket into fleet/bus/queues/to-*.json",
    )
    s.set_defaults(func=cmd_propose)

    s = sub.add_parser("tail", help="Show end of ACTIVITY-LOG")
    s.add_argument("-n", type=int, default=40)
    s.set_defaults(func=cmd_tail)

    s = sub.add_parser("today", help="Show today's calendar file")
    s.set_defaults(func=cmd_today)

    s = sub.add_parser("proposals", help="Show recent entries from proposals.jsonl")
    s.add_argument("-n", type=int, default=20)
    s.set_defaults(func=cmd_proposals)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
