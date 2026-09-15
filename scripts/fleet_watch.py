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
line; --notify files a durable GitHub issue comment only when the finding
fingerprint changes (never report-only, per the durable-output-sink law).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Sequence

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
ISSUE_TITLE = "Fleet liveness watch: stale signals"
ISSUE_SEARCH = "Fleet liveness watch in:title"
FINGERPRINT_MARKER_RE = re.compile(
    r"<!--\s*fleet-watch-fingerprint:\s*([0-9a-f]{64})\s*-->",
    re.IGNORECASE,
)
ISO_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T[0-9:.+\-Z]+")
RUN_ID_RE = re.compile(r"/actions/runs/\d+")
ALL_CLEAR_RE = re.compile(r"all clear|all liveness signals fresh", re.IGNORECASE)


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


def collect_findings(now: datetime, heartbeat_max_age_hours: float, ledger_max_age_hours: float) -> list[str]:
    return (
        check_heartbeats(now, heartbeat_max_age_hours)
        + check_ledger(now, ledger_max_age_hours)
        + check_queues(now)
    )


def stabilize_text(text: str) -> str:
    """Drop run-local noise so identical problems hash the same."""
    text = RUN_ID_RE.sub("/actions/runs/<id>", text)
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    return text.strip()


def fingerprint_findings(findings: Sequence[str]) -> str:
    lines = sorted(stabilize_text(item) for item in findings if item.strip())
    return sha256("\n".join(lines).encode("utf-8")).hexdigest()


def fingerprint_marker(fingerprint: str) -> str:
    return f"<!-- fleet-watch-fingerprint: {fingerprint} -->"


def is_automated_fleet_watch_comment(body: str) -> bool:
    if not body:
        return False
    if FINGERPRINT_MARKER_RE.search(body):
        return True
    if "Scheduled fleet-watch run failed" in body:
        return True
    if "fleet-watch:" in body:
        return True
    return bool(re.search(r"Fleet watch all clear", body, re.IGNORECASE))


def extract_finding_bullets(body: str) -> list[str]:
    bullets: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def fingerprint_from_comment_body(body: str) -> str | None:
    """Prefer the hidden marker; otherwise reconstruct from prior bot comments."""
    if not body:
        return None
    match = FINGERPRINT_MARKER_RE.search(body)
    if match:
        return match.group(1).lower()
    if not is_automated_fleet_watch_comment(body):
        return None
    bullets = extract_finding_bullets(body)
    if bullets:
        return fingerprint_findings(bullets)
    if ALL_CLEAR_RE.search(body):
        return fingerprint_findings([])
    return None


def last_automated_fingerprint(comment_bodies: Sequence[str]) -> str | None:
    for body in reversed(comment_bodies):
        if not is_automated_fleet_watch_comment(body):
            continue
        fingerprint = fingerprint_from_comment_body(body)
        if fingerprint:
            return fingerprint
    return None


def should_comment(findings: Sequence[str], last_fingerprint: str | None) -> bool:
    current = fingerprint_findings(findings)
    if last_fingerprint is None:
        # No tracker history: only open/comment when there is a problem.
        return bool(findings)
    return current != last_fingerprint


def format_report(findings: Sequence[str], now: datetime) -> str:
    if not findings:
        return "fleet-watch: all liveness signals fresh"
    header = (
        f"fleet-watch: {len(findings)} stale/failing signal(s) as of "
        f"{now.isoformat(timespec='seconds')}"
    )
    body = "\n".join(f"- {item}" for item in findings)
    return f"{header}\n{body}"


def build_comment_body(
    findings: Sequence[str],
    fingerprint: str,
    *,
    run_url: str = "",
    now: datetime | None = None,
) -> str:
    marker = fingerprint_marker(fingerprint)
    current = now or datetime.now(timezone.utc)
    if not findings:
        lines = [marker, "Fleet watch all clear: all liveness signals are fresh."]
        if run_url:
            lines.append(f"Run: {run_url}")
        return "\n".join(lines) + "\n"
    parts = [marker]
    if run_url:
        parts.append(f"Scheduled fleet-watch run failed: {run_url}")
        parts.append("")
    parts.extend(["```", format_report(findings, current), "```"])
    return "\n".join(parts) + "\n"


def _run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"gh {' '.join(args)} failed: {err}")
    return result.stdout


def _gh_repo_args() -> list[str]:
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    return ["-R", repo] if repo else []


def parse_paginated_json_arrays(raw: str) -> list[Any]:
    text = raw.strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        items: list[Any] = []
        idx = 0
        while idx < len(text):
            while idx < len(text) and text[idx].isspace():
                idx += 1
            if idx >= len(text):
                break
            obj, end = decoder.raw_decode(text, idx)
            if isinstance(obj, list):
                items.extend(obj)
            else:
                items.append(obj)
            idx = end
        return items


def find_open_tracking_issue() -> int | None:
    raw = _run_gh(
        [
            "issue",
            "list",
            *_gh_repo_args(),
            "--search",
            ISSUE_SEARCH,
            "--state",
            "open",
            "--json",
            "number",
            "--jq",
            ".[0].number",
        ]
    ).strip()
    if not raw or raw == "null":
        return None
    return int(raw)


def fetch_issue_comment_bodies(issue: int) -> list[str]:
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not repo:
        raise RuntimeError("GITHUB_REPOSITORY is not set")
    raw = _run_gh(
        [
            "api",
            "--paginate",
            f"repos/{repo}/issues/{issue}/comments?per_page=100",
        ]
    )
    bodies: list[str] = []
    for item in parse_paginated_json_arrays(raw):
        if not isinstance(item, dict):
            continue
        body = item.get("body") or ""
        if body:
            bodies.append(str(body))
    return bodies


def publish_tracking_comment(issue: int | None, body: str) -> None:
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, suffix=".md"
    )
    try:
        handle.write(body)
        handle.close()
        if issue is None:
            _run_gh(
                [
                    "issue",
                    "create",
                    *_gh_repo_args(),
                    "--title",
                    ISSUE_TITLE,
                    "--body-file",
                    handle.name,
                ]
            )
        else:
            _run_gh(
                [
                    "issue",
                    "comment",
                    *_gh_repo_args(),
                    str(issue),
                    "--body-file",
                    handle.name,
                ]
            )
    finally:
        Path(handle.name).unlink(missing_ok=True)


def lookup_last_fingerprint(
    *,
    dry_run: bool,
    last_comment_body: str | None,
) -> tuple[int | None, str | None, bool]:
    """Return (issue_number, last_fingerprint, lookup_ok)."""
    if last_comment_body is not None:
        return None, fingerprint_from_comment_body(last_comment_body), True
    if dry_run:
        return None, None, True
    try:
        issue = find_open_tracking_issue()
    except RuntimeError as err:
        print(f"fleet-watch: issue lookup failed ({err}); not commenting", file=sys.stderr)
        return None, None, False
    if issue is None:
        return None, None, True
    try:
        bodies = fetch_issue_comment_bodies(issue)
    except RuntimeError as err:
        print(f"fleet-watch: comment lookup failed ({err}); not commenting", file=sys.stderr)
        return issue, None, False
    return issue, last_automated_fingerprint(bodies), True


def maybe_notify(
    findings: Sequence[str],
    *,
    now: datetime,
    dry_run: bool,
    last_comment_body: str | None,
    run_url: str,
) -> str:
    fingerprint = fingerprint_findings(findings)
    issue, last_fingerprint, lookup_ok = lookup_last_fingerprint(
        dry_run=dry_run,
        last_comment_body=last_comment_body,
    )
    post = lookup_ok and should_comment(findings, last_fingerprint)
    decision = "comment" if post else "skip"
    if dry_run:
        print(f"DECISION={decision}")
        print(f"FINGERPRINT={fingerprint}")
        print(f"LAST_FINGERPRINT={last_fingerprint or ''}")
        print(f"FINDINGS={len(findings)}")
        print(f"WOULD_COMMENT={'true' if post else 'false'}")
        return decision
    if not lookup_ok:
        return "skip"
    if not post:
        print("fleet-watch: comment skipped (fingerprint unchanged)")
        return decision
    body = build_comment_body(findings, fingerprint, run_url=run_url, now=now)
    if not findings and issue is None:
        print("fleet-watch: all clear with no open tracking issue; not creating one")
        return "skip"
    try:
        publish_tracking_comment(issue, body)
    except RuntimeError as err:
        print(f"fleet-watch: failed to post comment ({err})", file=sys.stderr)
        return "error"
    print("fleet-watch: comment posted")
    return decision


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--heartbeat-max-age-hours", type=float, default=24)
    parser.add_argument("--ledger-max-age-hours", type=float, default=72)
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Create or comment on the tracking issue when the fingerprint changes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute the comment decision without calling the GitHub API.",
    )
    parser.add_argument(
        "--last-comment-body",
        default=None,
        help="Prior automated comment body used in --dry-run (skips GitHub lookup).",
    )
    parser.add_argument(
        "--skip-live-checks",
        action="store_true",
        help="Do not read heartbeats/ledger/queues; use --finding values instead.",
    )
    parser.add_argument(
        "--finding",
        action="append",
        dest="forced_findings",
        default=None,
        help="Force a finding line (repeatable). Skips live heartbeat/ledger/queue checks.",
    )
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    if args.skip_live_checks or args.forced_findings is not None:
        findings = list(args.forced_findings or [])
    else:
        findings = collect_findings(
            now, args.heartbeat_max_age_hours, args.ledger_max_age_hours
        )

    print(format_report(findings, now))

    if args.notify or args.dry_run:
        run_url = os.environ.get("FLEET_WATCH_RUN_URL", "").strip()
        maybe_notify(
            findings,
            now=now,
            dry_run=args.dry_run,
            last_comment_body=args.last_comment_body,
            run_url=run_url,
        )

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
