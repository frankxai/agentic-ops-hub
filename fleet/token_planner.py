#!/usr/bin/env python3
"""Starlight Token Planner: outcome routing, manifest checks, and night UX."""
from __future__ import annotations

import argparse
import json
import shlex
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


class PlannerError(ValueError):
    pass


@dataclass
class Planner:
    config: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path | str) -> "Planner":
        with Path(path).open(encoding="utf-8") as handle:
            return cls(json.load(handle))

    def recommend(self, job_class: str, complexity: int = 5, unattended: bool = False) -> dict[str, Any]:
        routes = self.config["routes"]
        if job_class not in routes:
            if complexity >= 7:
                job_class = "deep-backend"
            elif complexity <= 3:
                job_class = "low-stakes"
            else:
                job_class = "refactor"
        decision = {"job_class": job_class, **routes[job_class]}
        decision["complexity"] = complexity
        decision["unattended"] = unattended
        return decision

    def validate_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        if manifest.get("mode") != "night":
            raise PlannerError("manifest mode must be night")
        declared = float(manifest.get("total_budget_usd", 0))
        cap = float(self.config["night_cap_usd"])
        if declared > cap:
            raise PlannerError(f"declared budget ${declared:g} exceeds night cap ${cap:g}")
        missions = manifest.get("missions")
        if not isinstance(missions, list) or not missions:
            raise PlannerError("manifest requires at least one mission")
        ids: set[str] = set()
        total = 0.0
        version = int(manifest.get("version", 1))
        for mission in missions:
            mission_id = str(mission.get("id", ""))
            if not mission_id or mission_id in ids:
                raise PlannerError("mission ids must be non-empty and unique")
            ids.add(mission_id)
            branch = str(mission.get("branch", ""))
            if not branch.startswith("night/"):
                raise PlannerError(f"mission {mission_id} branch must start with night/")
            for key in ("agent", "repo", "task", "report"):
                if not mission.get(key):
                    raise PlannerError(f"mission {mission_id} missing {key}")
            if version >= 2:
                if not mission.get("receipt"):
                    raise PlannerError(f"mission {mission_id} missing receipt")
                checks = mission.get("acceptance_commands")
                if not isinstance(checks, list) or not checks:
                    raise PlannerError(f"mission {mission_id} requires acceptance_commands")
            budget = float(mission.get("budget_usd", 0))
            if budget < 0:
                raise PlannerError(f"mission {mission_id} budget cannot be negative")
            total += budget
            if mission["agent"] == "claude" and not mission.get("max_turns"):
                raise PlannerError(f"mission {mission_id} Claude requires max_turns")
            if int(mission.get("timeout_minutes", 60)) > 180:
                raise PlannerError(f"mission {mission_id} timeout exceeds 180 minutes")
        if total > declared:
            raise PlannerError(f"mission budgets ${total:g} exceed declared budget ${declared:g}")
        return {"valid": True, "mission_count": len(missions), "budget_usd": total, "cap_usd": cap}

    def _task_contract(self, mission: dict[str, Any]) -> str:
        rules = (
            "HARD RULES: Work only in the exact current branch/worktree. No main push. "
            "No force-push. No git reset --hard. No secrets. Never widen sandbox or approvals."
        )
        acceptance = mission.get("acceptance_commands") or []
        receipt = mission.get("receipt")
        contract = [rules, "", str(mission["task"])]
        if acceptance:
            contract += ["", "ACCEPTANCE COMMANDS (run and record exact exit codes):"]
            contract += [f"- {command}" for command in acceptance]
        if receipt:
            contract += [
                "",
                f"Write machine-readable receipt JSON to: {receipt}",
                "Receipt fields: mission_id, status=verified|delivered, branch, commit, "
                "verification[{command,exit_code}], integration_state, completed_at.",
                f"Also write the human report to: {mission['report']}",
            ]
        return "\n".join(contract)

    def command_args(self, mission: dict[str, Any], *, sandbox: str = "workspace-write") -> list[str]:
        task = self._task_contract(mission)
        agent = str(mission["agent"])
        if agent == "claude":
            return [
                "claude",
                "-p",
                task,
                "--model",
                str(mission.get("model", "sonnet")),
                "--max-budget-usd",
                f"{float(mission['budget_usd']):g}",
                "--max-turns",
                str(int(mission["max_turns"])),
                "--permission-mode",
                "acceptEdits",
                "--output-format",
                "json",
            ]
        if agent == "codex":
            return [
                "codex",
                "exec",
                "-C",
                str(mission["repo"]),
                "--sandbox",
                sandbox,
                "-m",
                str(mission.get("model", "gpt-5.6-terra")),
                "-c",
                f"model_reasoning_effort={mission.get('reasoning_effort', 'high')}",
                task,
            ]
        if agent == "opencode":
            return ["opencode", "run", task]
        if agent == "gemini":
            return ["gemini", "-p", task]
        raise PlannerError(f"agent {agent!r} has no unattended launcher")

    def command_for(self, mission: dict[str, Any]) -> str:
        return shlex.join(self.command_args(mission))

    def _receipt_state(self, mission: dict[str, Any]) -> tuple[str, str]:
        receipt_value = mission.get("receipt")
        if not receipt_value:
            return "missing-receipt", "manifest has no receipt path"
        receipt = Path(receipt_value)
        if not receipt.is_file():
            return "missing-receipt", str(receipt)
        try:
            payload = json.loads(receipt.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return "invalid-receipt", str(exc)
        if payload.get("mission_id") != mission.get("id"):
            return "invalid-receipt", "mission_id mismatch"
        if payload.get("branch") != mission.get("branch"):
            return "invalid-receipt", "branch mismatch"
        if payload.get("status") not in {"verified", "delivered"}:
            return "unverified", "status is not verified/delivered"
        if not payload.get("commit"):
            return "unverified", "commit missing"
        checks = payload.get("verification")
        if not isinstance(checks, list) or not checks:
            return "unverified", "verification missing"
        if any(int(check.get("exit_code", 1)) != 0 for check in checks):
            return "failed-verification", "acceptance command failed"
        if payload.get("integration_state") not in {
            "pr_open",
            "merged",
            "delivered",
            "rejected",
            "hold",
        }:
            return "unverified", "integration_state missing"
        if not payload.get("completed_at"):
            return "unverified", "completed_at missing"
        return str(payload["status"]), "receipt accepted"

    def status(self, manifest: dict[str, Any]) -> dict[str, Any]:
        rows = []
        complete = 0
        for mission in manifest.get("missions", []):
            state, detail = self._receipt_state(mission)
            is_complete = state in {"verified", "delivered"}
            complete += int(is_complete)
            rows.append(
                {
                    "id": mission["id"],
                    "agent": mission["agent"],
                    "status": state,
                    "detail": detail,
                    "report": str(mission["report"]),
                    "receipt": str(mission.get("receipt", "")),
                }
            )
        return {"complete": complete, "missing": len(rows) - complete, "missions": rows}

    def debrief(self, manifest: dict[str, Any]) -> str:
        state = self.status(manifest)
        lines = [
            f"# Night debrief — {manifest.get('date', 'unknown')}",
            "",
            f"Budget envelope: ${float(manifest.get('total_budget_usd', 0)):g}",
            f"Missions: {state['complete']} verified/delivered · {state['missing']} incomplete",
            "",
            "| Mission | Agent | Status | Receipt |",
            "|---------|-------|--------|---------|",
        ]
        for row in state["missions"]:
            lines.append(f"| {row['id']} | {row['agent']} | {row['status']} | `{row['receipt']}` |")
        lines += [
            "",
            "**Human review required.** No unattended merge, main push, or production deploy.",
        ]
        return "\n".join(lines) + "\n"


_WEEKDAYS = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
_TIER_ORDER = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}


def parse_timestamp(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


@dataclass
class PlanLimits:
    """Claude subscription allowance plane: weekly model-time, not USD.

    Anthropic meters paid plans in hours of model use (a weekly limit with a
    fixed per-account reset, plus a 5-hour session window), so the USD
    envelopes elsewhere in this file do not apply to subscription-metered runs.
    There is NO public API endpoint for subscription usage: consumption is
    estimated from local Claude Code session JSONL (see fleet/usage_ingest.py),
    and `/usage` inside a Claude Code session is the authoritative human
    cross-check. Internal unit: STE (Sonnet-5-token-equivalents) - tokens
    weighted per kind by API price ratio, then per model so Sonnet 5 = 1.0.
    Numbers in plan_limits.json carry provenance/confidence; estimates are
    calibration priors, never contract values.
    """

    config: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path | str) -> "PlanLimits":
        with Path(path).open(encoding="utf-8") as handle:
            return cls(json.load(handle))

    def facts_expired(self, now: datetime) -> list[str]:
        """Names of dated facts whose valid_until has passed. Any expired fact
        makes the whole computation uncalibrated - stale facts are loud."""
        now = parse_timestamp(now)
        stale = []
        for name, spec in self.config.items():
            if isinstance(spec, dict) and "valid_until" in spec:
                if now >= parse_timestamp(spec["valid_until"]):
                    stale.append(name)
        for name, spec in self.config.get("buckets", {}).items():
            if isinstance(spec, dict) and "valid_until" in spec:
                if now >= parse_timestamp(spec["valid_until"]):
                    stale.append(f"buckets.{name}")
        return sorted(stale)

    def reset_anchor_verified(self) -> bool:
        """The weekly reset day/time is per-account. It has no defensible
        default: an unverified anchor is an error state, not a fallback."""
        return self.config["weekly_reset"].get("confidence") == "verified"

    def observations(self) -> list[dict[str, Any]]:
        return list(self.config.get("calibration", {}).get("observations", []))

    def calibration_status(self, now: datetime) -> dict[str, Any]:
        """Calibrated requires BOTH a verified reset anchor AND enough human
        /usage observations spanning at least one reset boundary. Absent
        either, every number this module emits is uncalibrated and advisory."""
        calib = self.config["calibration"]
        minimum = int(calib["minimum_observations"])
        obs = self.observations()
        reasons = []
        if not self.reset_anchor_verified():
            reasons.append("weekly_reset anchor is not verified - read it from Settings -> Usage")
        if len(obs) < minimum:
            reasons.append(f"{len(obs)}/{minimum} human /usage observations recorded")
        spans_reset = False
        if obs:
            windows = {self.weekly_window(parse_timestamp(o["observed_at"]))[0]
                       for o in obs} if self.reset_anchor_verified() else set()
            spans_reset = len(windows) > 1
            if not spans_reset:
                reasons.append("observations do not span a reset boundary")
        stale = self.facts_expired(now)
        if stale:
            reasons.append(f"expired facts: {', '.join(stale)}")
        return {"calibrated": not reasons, "blockers": reasons,
                "observations": len(obs), "spans_reset": spans_reset}

    def weekly_window(self, now: datetime) -> tuple[datetime, datetime]:
        if not self.reset_anchor_verified():
            raise PlannerError(
                "weekly_reset anchor is not verified; refusing to compute a window. "
                "Read the real reset day/time from Settings -> Usage, set it in "
                "plan_limits.json, and mark confidence 'verified'."
            )
        reset = self.config["weekly_reset"]
        local = parse_timestamp(now).astimezone(ZoneInfo(reset["timezone"]))
        anchor = local.replace(hour=int(reset["hour"]), minute=0, second=0, microsecond=0)
        while anchor.weekday() != _WEEKDAYS[str(reset["weekday"]).lower()] or anchor > local:
            anchor -= timedelta(days=1)
        return anchor, anchor + timedelta(days=7)

    def session_window(
        self, now: datetime, records: Iterable[dict[str, Any]] = ()
    ) -> tuple[datetime, datetime]:
        """Current 5-hour block: starts at the top of the hour of the first
        activity after the previous block ends (same anchoring ccusage uses)."""
        hours = int(self.config["session_window_hours"]["value"])
        now = parse_timestamp(now)
        start = None
        for record in sorted(records, key=lambda item: parse_timestamp(item["timestamp"])):
            when = parse_timestamp(record["timestamp"])
            if when > now:
                break
            if start is None or when >= start + timedelta(hours=hours):
                start = when.replace(minute=0, second=0, microsecond=0)
        if start is None or now >= start + timedelta(hours=hours):
            start = now.replace(minute=0, second=0, microsecond=0)
        return start, start + timedelta(hours=hours)

    def boost_multiplier(self, now: datetime) -> float:
        boost = self.config["boost"]
        active = parse_timestamp(now) < parse_timestamp(boost["expires"])
        return float(boost["multiplier"]) if active else 1.0

    def weight_for(self, model: str) -> float:
        weights = self.config["weights"]
        for name, value in weights.items():
            if name in {"$comment", "provenance", "confidence", "default", "valid_until"}:
                continue
            if name in model:
                return float(value)
        return float(weights["default"])

    def weighted_tokens(self, record: dict[str, Any]) -> float:
        kinds = self.config["token_kind_multipliers"]
        raw = (
            float(record.get("input_tokens", 0)) * float(kinds["input"])
            + float(record.get("output_tokens", 0)) * float(kinds["output"])
            + float(record.get("cache_creation_input_tokens", 0)) * float(kinds["cache_creation"])
            + float(record.get("cache_read_input_tokens", 0)) * float(kinds["cache_read"])
        )
        return raw * self.weight_for(str(record.get("model", "")))

    def _bucket_matches(self, bucket: str, model: str) -> bool:
        patterns = self.config["buckets"][bucket]["match"]
        return "*" in patterns or any(pattern in model for pattern in patterns)

    def bucket_activity(self, records: Iterable[dict[str, Any]], now: datetime) -> dict[str, Any]:
        """Local activity index per bucket: locally-observed STE divided by an
        ESTIMATED capacity. This is NOT remaining allowance and NOT a reading of
        the real plan. The index rises with use; 1.0 means local activity has
        reached the midpoint capacity estimate. The interval comes from the
        published hour range - a wide band, honestly reported.
        """
        now = parse_timestamp(now)
        start, end = self.weekly_window(now)
        boost = self.boost_multiplier(now)
        per_hour = float(self.config["calibration"]["sonnet_tokens_per_hour"])
        status = self.calibration_status(now)
        consumed = {name: 0.0 for name in self.config["buckets"]}
        for record in records:
            when = parse_timestamp(record["timestamp"])
            if when < start or when > now:
                continue
            burn = self.weighted_tokens(record)
            model = str(record.get("model", ""))
            for name in consumed:
                if self._bucket_matches(name, model):
                    consumed[name] += burn
        buckets = {}
        for name, spec in self.config["buckets"].items():
            low_h, high_h = (float(v) for v in spec["published_range_hours"])
            mid_h = float(spec["weekly_hours_planning"])

            def index(hours: float) -> float:
                cap = hours * per_hour * boost
                return round(consumed[name] / cap, 4) if cap else float("inf")

            buckets[name] = {
                "observed_ste": consumed[name],
                # More hours of capacity -> lower index. Interval ends swap.
                "activity_index": index(mid_h),
                "activity_index_interval": [index(high_h), index(low_h)],
                "capacity_estimate_hours": {"low": low_h, "mid": mid_h, "high": high_h},
                "is_measurement": False,
            }
        return {
            "window": {"start": start.isoformat(), "end": end.isoformat()},
            "boost_multiplier": boost,
            "calibration": status,
            "buckets": buckets,
            "disclaimer": (
                "Local activity index derived from local session tokens and estimated "
                "capacity. NOT remaining plan allowance. Cross-check /usage."
            ),
        }

    def binding_index(self, activity: dict[str, Any], model: str) -> float:
        """Highest activity index among the buckets this model draws from
        (all_models always; plus the model-specific bucket)."""
        return max(
            bucket["activity_index"]
            for name, bucket in activity["buckets"].items()
            if self._bucket_matches(name, model)
        )

    def normal_model(self, job_class: str) -> str:
        models = self.config["advice"]["normal_models"]
        return str(models.get(job_class, models["default"]))

    def advise(
        self,
        activity_index: float,
        job_class: str,
        critical: bool = False,
        calibrated: bool = False,
    ) -> dict[str, Any]:
        """Suggest a Claude-lane model for a job class given the local activity
        index. ADVISORY ONLY unless `calibrated` is True: an uncalibrated call
        returns `auto_route: False` and no caller may act on it automatically.
        Index rises with use, so higher means scarcer."""
        advice = self.config["advice"]
        thresholds = advice["thresholds"]
        normal = self.normal_model(job_class)
        if activity_index < float(thresholds["normal_below"]):
            posture = "normal"
        elif activity_index < float(thresholds["watch_below"]):
            posture = "watch"
        elif activity_index < float(thresholds["conserve_below"]):
            posture = "conserve"
        else:
            posture = "floor"
        model = normal
        if critical:
            reason = f"critical flag set: {normal} kept regardless of {posture} posture"
        elif posture == "normal":
            reason = "local activity low: normal routing suggested"
        elif posture == "watch":
            reason = "local activity rising: normal routing still suggested; prefer cheaper tiers where quality allows"
        elif posture == "conserve":
            if job_class in advice["needs_expensive"]:
                reason = f"{job_class} measurably needs its tier: {normal} reserved"
            elif _TIER_ORDER.get(normal, 1) > _TIER_ORDER["sonnet"]:
                model = "sonnet"
                reason = "local activity high: non-critical work suggested at sonnet"
            else:
                reason = f"local activity high: {normal} already at or below sonnet"
        else:
            model = str(advice["floor_models"].get(job_class, advice["floor_models"]["default"]))
            reason = "local activity at or past the capacity estimate: cheapest passing tier suggested"
        if not calibrated:
            reason = f"ADVISORY ONLY (uncalibrated): {reason}"
        return {
            "job_class": job_class,
            "activity_index": activity_index,
            "posture": posture,
            "model": model,
            "critical": critical,
            "advisory_only": not calibrated,
            "auto_route": bool(calibrated),
            "reason": reason,
        }


def load_json(path: str) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Starlight Token Planner")
    parser.add_argument("--config", default=str(Path(__file__).with_name("model-routing.json")))
    sub = parser.add_subparsers(dest="command", required=True)
    recommend = sub.add_parser("recommend")
    recommend.add_argument("job_class")
    recommend.add_argument("--complexity", type=int, default=5)
    recommend.add_argument("--unattended", action="store_true")
    for name in ("validate", "commands", "status", "debrief"):
        cmd = sub.add_parser(name)
        cmd.add_argument("manifest")
    args = parser.parse_args()
    planner = Planner.from_file(args.config)
    try:
        if args.command == "recommend":
            result = planner.recommend(args.job_class, args.complexity, args.unattended)
        else:
            manifest = load_json(args.manifest)
            if args.command == "validate":
                result = planner.validate_manifest(manifest)
            elif args.command == "status":
                result = planner.status(manifest)
            elif args.command == "debrief":
                print(planner.debrief(manifest), end="")
                return 0
            else:
                planner.validate_manifest(manifest)
                result = {m["id"]: planner.command_for(m) for m in manifest["missions"]}
        print(json.dumps(result, indent=2))
        return 0
    except (PlannerError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
