#!/usr/bin/env python3
"""Off-machine fleet liveness watch — the dead-man's switch.

Every existing liveness signal (topology-health-pulse, host-watchdog, the 6h
Telegram pulse) executes ON the machine it watches, so an offline C940
silences its own alarms and event-driven CI simply stops running. This script
inverts that: run it from a SCHEDULED GitHub Actions workflow so the absence
of fleet signals causes a failure instead of suppressing one.

Checks, all read-only against git-versioned state:
  1. Every heartbeat in fleet/bus/heartbeats/*.json is live and fresher than
     --heartbeat-max-age-hours (default 24, matching queue_reconcile's gate).
  2. ops/OPS-LEDGER.md's "Last sweep:" timestamp is fresher than
     --ledger-max-age-hours (default 72 against the declared daily cadence).
  3. Both queue documents validate, including TTL enforcement on active items
     (require_ttl=True per the to-c940.json coordination contract).

Exit 0 with no output sections means healthy. Exit 1 prints one finding per
line; the workflow turns that into a durable GitHub issue (never report-only,
per the durable-output-sink law).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.queue_reconcile import heartbeat_is_fresh, validate_queue_document

HEARTBEAT_DIR = REPO_ROOT / "fleet" / "bus" / "heartbeats"
LEDGER_PATH = REPO_ROOT / "ops" / "OPS-LEDGER.md"
QUEUE_PATHS = (
    REPO_ROOT / "fleet" / "bus" / "queues" / "to-c940.json",
    REPO_ROOT / "fleet" / "bus" / "queues" / "to-book.json",
)
LAST_SWEEP_RE = re.compile(r"\*\*Last sweep:\*\*\s*([0-9][0-9T:.+\-]+)")


def check_heartbeats(now: datetime, max_age_hours: float) -> list[str]:
    findings: list[str] = []
    beats = sorted(HEARTBEAT_DIR.glob("*.json")) if HEARTBEAT_DIR.is_dir() else []
    if not beats:
        return [f"no heartbeat files found under {HEARTBEAT_DIR.relative_to(REPO_ROOT)}"]
    for path in beats:
        rel = path.relative_to(REPO_ROOT)
        try:
            beat = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            findings.append(f"{rel}: unreadable heartbeat ({err})")
            continue
        if not heartbeat_is_fresh(beat, max_age_hours=max_age_hours, now=now):
            findings.append(
                f"{rel}: machine {beat.get('machine_id', '?')} heartbeat stale or "
                f"not-live (at={beat.get('at', 'missing')}, max_age_hours={max_age_hours:g})"
            )
    return findings


def check_ledger(now: datetime, max_age_hours: float) -> list[str]:
    rel = LEDGER_PATH.relative_to(REPO_ROOT)
    try:
        head = LEDGER_PATH.read_text(encoding="utf-8")[:4000]
    except OSError as err:
        return [f"{rel}: unreadable ({err})"]
    match = LAST_SWEEP_RE.search(head)
    if not match:
        return [f"{rel}: no 'Last sweep:' timestamp found in header"]
    raw = match.group(1).rstrip(".")
    try:
        swept = datetime.fromisoformat(raw)
    except ValueError:
        return [f"{rel}: unparseable Last sweep timestamp {raw!r}"]
    if swept.tzinfo is None:
        swept = swept.replace(tzinfo=timezone.utc)
    if swept < now - timedelta(hours=max_age_hours):
        return [
            f"{rel}: Last sweep {raw} is older than {max_age_hours:g}h against the "
            "declared daily cadence"
        ]
    return []


def check_queues(now: datetime) -> list[str]:
    findings: list[str] = []
    for path in QUEUE_PATHS:
        rel = path.relative_to(REPO_ROOT)
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            findings.append(f"{rel}: unreadable queue document ({err})")
            continue
        for error in validate_queue_document(doc, require_ttl=True, now=now):
            findings.append(f"{rel}: {error}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--heartbeat-max-age-hours", type=float, default=24)
    parser.add_argument("--ledger-max-age-hours", type=float, default=72)
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    findings = (
        check_heartbeats(now, args.heartbeat_max_age_hours)
        + check_ledger(now, args.ledger_max_age_hours)
        + check_queues(now)
    )
    if not findings:
        print("fleet-watch: all liveness signals fresh")
        return 0
    print(f"fleet-watch: {len(findings)} stale/failing signal(s) as of {now.isoformat(timespec='seconds')}")
    for finding in findings:
        print(f"- {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
