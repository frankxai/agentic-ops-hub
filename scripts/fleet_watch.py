#!/usr/bin/env python3
"""Off-machine fleet liveness watch — the dead-man's switch.

Every existing liveness signal (topology-health-pulse, host-watchdog, the 6h
Telegram pulse) executes ON the machine it watches, so an offline C940
silences its own alarms and event-driven CI simply stops running. This script
inverts that: run it from a SCHEDULED GitHub Actions workflow so the absence
of fleet signals causes a failure instead of suppressing one.

Checks, all read-only against git-versioned state:
  1. Every machine with a non-retired "liveness" block in
     fleet/clone-manifest.json has a pulse/<machine> branch whose
     heartbeat.json is live and fresher than its max_age_hours (fallback
     --heartbeat-max-age-hours, default 24). Heartbeats live on unprotected
     per-machine branches, not main: main is protected and PR-only, so a
     machine can never land a daily heartbeat there. The workflow fetches
     refs/heads/pulse/* into refs/remotes/origin/pulse/* before this runs.
     A pulse branch for a machine not in the registry is a warning only.
  2. ops/OPS-LEDGER.md's "Last sweep:" timestamp is fresher than
     --ledger-max-age-hours (default 336 = 14 days). The ledger is swept by
     hand through PRs, in bursts days to weeks apart; a daily threshold made
     this watch permanently red. 14 days still catches a ledger nobody tends.
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

from scripts.fleet_bus import PULSE_PREFIX, read_pulse_heartbeats
from scripts.queue_reconcile import (
    heartbeat_is_fresh,
    is_retired,
    validate_queue_document,
)

MANIFEST_PATH = REPO_ROOT / "fleet" / "clone-manifest.json"
PULSE_REMOTE = "origin"
LEDGER_PATH = REPO_ROOT / "ops" / "OPS-LEDGER.md"
QUEUE_PATHS = (
    REPO_ROOT / "fleet" / "bus" / "queues" / "to-c940.json",
    REPO_ROOT / "fleet" / "bus" / "queues" / "to-book.json",
)
LAST_SWEEP_RE = re.compile(r"\*\*Last sweep:\*\*\s*([0-9][0-9T:.+\-]+)")


def check_heartbeats(
    now: datetime,
    max_age_hours: float,
    remote: str = PULSE_REMOTE,
    repo: Path = REPO_ROOT,
) -> tuple[list[str], list[str]]:
    """Return (findings, warnings) for registered machines vs fetched pulse branches."""
    rel = MANIFEST_PATH.relative_to(REPO_ROOT)
    try:
        machines = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")).get("machines", {})
    except (OSError, json.JSONDecodeError) as err:
        return [f"{rel}: unreadable machine registry ({err})"], []
    watched = {
        mid: meta["liveness"]
        for mid, meta in machines.items()
        if isinstance(meta, dict) and isinstance(meta.get("liveness"), dict)
    }
    if not watched:
        return [f"{rel}: no machine declares a liveness block"], []

    findings: list[str] = []
    pulses = read_pulse_heartbeats(remote, repo)
    for mid, liveness in sorted(watched.items()):
        if is_retired(liveness):
            # A machine deliberately taken out of the fleet has no liveness
            # duty. Retirement must be declared in the registry with a
            # retired_at stamp, so a machine cannot retire itself by going quiet.
            continue
        branch = f"{PULSE_PREFIX}{mid}"
        beat = pulses.get(mid)
        if beat is None:
            findings.append(f"{branch}: machine {mid} is registered but has no pulse branch")
            continue
        if isinstance(beat, str):
            findings.append(f"{branch}: {beat}")
            continue
        if beat.get("machine_id") != mid:
            findings.append(
                f"{branch}: heartbeat claims machine_id={beat.get('machine_id')!r}, expected {mid!r}"
            )
            continue
        limit = float(liveness.get("max_age_hours", max_age_hours))
        if not heartbeat_is_fresh(beat, max_age_hours=limit, now=now):
            findings.append(
                f"{branch}: machine {mid} heartbeat stale or not-live "
                f"(at={beat.get('at', 'missing')}, status={beat.get('status', 'missing')}, "
                f"max_age_hours={limit:g})"
            )
    warnings = [
        f"{PULSE_PREFIX}{mid}: pulse branch for unregistered machine {mid} "
        f"(add a liveness block in {rel} or delete the branch)"
        for mid in sorted(set(pulses) - set(watched))
    ]
    return findings, warnings


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
            f"{rel}: Last sweep {raw} is older than {max_age_hours:g}h; run /ops-sweep"
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
    parser.add_argument("--ledger-max-age-hours", type=float, default=336)
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    heartbeat_findings, warnings = check_heartbeats(now, args.heartbeat_max_age_hours)
    findings = (
        heartbeat_findings
        + check_ledger(now, args.ledger_max_age_hours)
        + check_queues(now)
    )
    for warning in warnings:
        print(f"warning: {warning}")
    if not findings:
        print("fleet-watch: all liveness signals fresh")
        return 0
    print(f"fleet-watch: {len(findings)} stale/failing signal(s) as of {now.isoformat(timespec='seconds')}")
    for finding in findings:
        print(f"- {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
