#!/usr/bin/env python3
"""Ingest local Claude Code session usage into plan-allowance terms.

Primary input: the session JSONL Claude Code writes under
~/.claude/projects/**/*.jsonl (per-message token counts and model ids), parsed
natively so there is no dependency. Alternative input: `ccusage daily --json`
output (ryoppippi's ccusage; tokscale covers the same files across CLIs).
There is no public API endpoint for subscription usage - `/usage` inside a
Claude Code session is the authoritative cross-check for everything printed
here. Absent session data (a fresh container or machine) is expected, not a
bug: the CLI says so and exits non-zero.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from fleet.token_planner import PlanLimits, parse_timestamp
except ImportError:  # run as a script, fleet/ itself is on sys.path
    from token_planner import PlanLimits, parse_timestamp

_USAGE_KEYS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def records_from_jsonl(root: Path) -> list[dict[str, Any]]:
    """Parse per-message usage out of Claude Code session JSONL under root.

    Streamed retries repeat a (message id, request id) pair; the last
    occurrence carries the final counts, so later lines replace earlier ones.
    """
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    unkeyed: list[dict[str, Any]] = []
    for path in sorted(root.glob("**/*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = entry.get("message") or {}
            usage = message.get("usage")
            model = str(message.get("model", ""))
            if not isinstance(usage, dict) or not model or model == "<synthetic>" or not entry.get("timestamp"):
                continue
            record: dict[str, Any] = {"timestamp": str(entry["timestamp"]), "model": model}
            for key in _USAGE_KEYS:
                record[key] = int(usage.get(key) or 0)
            dedup = (str(message.get("id", "")), str(entry.get("requestId", "")))
            if dedup == ("", ""):
                unkeyed.append(record)
            else:
                latest[dedup] = record
    return unkeyed + list(latest.values())


def records_from_ccusage(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept `ccusage daily --json` output: daily entries with modelBreakdowns.

    Day granularity only, so each day is attributed to noon UTC; near a weekly
    reset boundary prefer the raw JSONL path, which keeps real timestamps.
    """
    records: list[dict[str, Any]] = []
    for day in payload.get("daily", []):
        stamp = f"{day.get('date')}T12:00:00+00:00"
        breakdowns = day.get("modelBreakdowns") or [
            {
                "modelName": ",".join(day.get("modelsUsed", [])) or "unknown",
                "inputTokens": day.get("inputTokens", 0),
                "outputTokens": day.get("outputTokens", 0),
                "cacheCreationTokens": day.get("cacheCreationTokens", 0),
                "cacheReadTokens": day.get("cacheReadTokens", 0),
            }
        ]
        for item in breakdowns:
            records.append(
                {
                    "timestamp": stamp,
                    "model": str(item.get("modelName", "unknown")),
                    "input_tokens": int(item.get("inputTokens") or 0),
                    "output_tokens": int(item.get("outputTokens") or 0),
                    "cache_creation_input_tokens": int(item.get("cacheCreationTokens") or 0),
                    "cache_read_input_tokens": int(item.get("cacheReadTokens") or 0),
                }
            )
    return records


def report(limits: PlanLimits, records: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    now = parse_timestamp(now)
    usage = limits.bucket_activity(records, now)
    window_start = parse_timestamp(usage["window"]["start"])
    session_start, session_end = limits.session_window(now, records)
    per_model: dict[str, dict[str, Any]] = {}
    session_ste = 0.0
    for record in records:
        when = parse_timestamp(record["timestamp"])
        if when < window_start or when > now:
            continue
        row = per_model.setdefault(record["model"], dict.fromkeys(_USAGE_KEYS, 0) | {"weighted_ste": 0.0})
        for key in _USAGE_KEYS:
            row[key] += record[key]
        burn = limits.weighted_tokens(record)
        row["weighted_ste"] = round(row["weighted_ste"] + burn, 1)
        if session_start <= when < session_end:
            session_ste += burn
    return {
        "plan": limits.config.get("plan"),
        "records": len(records),
        "weekly_window": usage["window"],
        "boost_multiplier": usage["boost_multiplier"],
        "buckets": usage["buckets"],
        "per_model": {name: per_model[name] for name in sorted(per_model)},
        "session_window": {"start": session_start.isoformat(), "end": session_end.isoformat()},
        "session_consumed_ste": round(session_ste, 1),
        "session_note": "no session-window capacity is published; /usage is the live check",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Claude plan-allowance usage ingest")
    parser.add_argument("--projects-root", default=str(Path.home() / ".claude" / "projects"))
    parser.add_argument("--ccusage", help="path to `ccusage daily --json` output instead of raw JSONL")
    parser.add_argument("--limits", default=str(Path(__file__).with_name("plan_limits.json")))
    parser.add_argument("--now", help="ISO timestamp override for window math (default: current UTC)")
    parser.add_argument("--advise", metavar="JOB_CLASS", help="append a routing recommendation for this job class")
    parser.add_argument("--critical", action="store_true", help="flag the advised work as critical (never down-tiered)")
    args = parser.parse_args(argv)
    limits = PlanLimits.from_file(args.limits)
    now = parse_timestamp(args.now) if args.now else datetime.now(timezone.utc)
    if args.ccusage:
        try:
            records = records_from_ccusage(json.loads(Path(args.ccusage).read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"cannot read ccusage JSON {args.ccusage}: {exc}", file=sys.stderr)
            return 2
    else:
        records = records_from_jsonl(Path(args.projects_root).expanduser())
    if not records:
        print(
            f"no Claude Code session data under {args.projects_root} - "
            "expected on a fresh container or machine, not a bug. Run sessions first "
            "or pass --ccusage FILE; /usage inside a session is the authoritative read.",
            file=sys.stderr,
        )
        return 2
    result = report(limits, records, now)
    if args.advise:
        index = limits.binding_index(result, limits.normal_model(args.advise))
        calibrated = bool(result["calibration"]["calibrated"])
        result["advice"] = limits.advise(
            index, args.advise, critical=args.critical, calibrated=calibrated
        )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
