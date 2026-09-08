#!/usr/bin/env python3
"""Starlight Token Planner: outcome routing, manifest checks, and night UX."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import statistics
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo


class PlannerError(ValueError):
    pass


_PROHIBITED_TASK_PATTERNS = {
    r"\bgit\s+push\b": "git push",
    r"\bgit\s+reset\s+--hard\b": "git reset --hard",
    r"\brm\s+-rf\b": "rm -rf",
    r"\b(?:vercel|railway)\b[^\n]*(?:--prod|\bup\b)": "production deployment",
    r"--force(?:-with-lease)?\b": "force push",
}

_FORBIDDEN_LAUNCH_TOKENS = {
    "danger-full-access",
    "--dangerously-skip-permissions",
    "--dangerously-bypass-approvals-and-sandbox",
    "--yolo",
}

_CANONICAL_GITHUB_HOST = "github.com"
_CANONICAL_GITHUB_OWNER = "frankxai"
_CANONICAL_CONTROL_REPO = "agentic-ops-hub"
_PRIVATE_OBSERVATION_KEYS = {
    "account",
    "account_id",
    "auth",
    "credential",
    "email",
    "key",
    "secret",
    "token",
}
_OBSERVATION_FIELDS = {
    "observed_at",
    "agent",
    "job_class",
    "role",
    "duration_minutes",
    "outcome_status",
    "artifact_score",
    "quota_before_percent",
    "quota_after_percent",
    "receipt_id",
    "mission_id",
    "receipt_path",
    "receipt_sha256",
}
_SHELL_META_RE = re.compile(r"[;&|<>`$()\r\n]")
_METERED_APPROVAL_FIELDS = {
    "approval_id",
    "approved",
    "provider",
    "quota_pool",
    "currency",
    "max_spend_usd",
    "expires_at",
}


def _repo_path(mission: dict[str, Any], value: str) -> Path:
    return _portable_repo_path(str(mission["repo"]), value, f"mission {mission['id']}")


def _bounded_percent(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("percentage must be numeric")
    result = float(value)
    if not math.isfinite(result) or not 0 <= result <= 100:
        raise ValueError("percentage must be finite and between 0 and 100")
    return result


def _bounded_money(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PlannerError(f"{label} must be a numeric amount")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise PlannerError(f"{label} must be finite and non-negative")
    return result


def _positive_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PlannerError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise PlannerError(f"{label} must be finite and positive")
    return result


def _portable_repo_path(repo: str, value: str, owner: str) -> Path:
    windows = PureWindowsPath(value)
    posix = PurePosixPath(value)
    if (
        windows.anchor
        or windows.root
        or windows.drive
        or posix.is_absolute()
        or ".." in windows.parts
        or ".." in posix.parts
    ):
        raise PlannerError(f"{owner} path must be repo-relative and portable: {value}")
    root = Path(repo).resolve()
    resolved = (root / Path(value)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise PlannerError(f"{owner} path escapes repo: {value}") from exc
    return resolved


def _require_portable_path(mission: dict[str, Any], key: str, value: str) -> None:
    _portable_repo_path(str(mission["repo"]), value, f"mission {mission['id']} {key}")


def _safe_acceptance_command(value: Any) -> bool:
    """Allow fixed, repo-scoped validation command families without shell syntax."""
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    if _SHELL_META_RE.search(value):
        return False
    try:
        argv = shlex.split(value, posix=True)
    except ValueError:
        return False
    if argv == ["git", "diff", "--check"]:
        return True

    def safe_relative(token: str, *, suffix: str | None = None) -> bool:
        windows = PureWindowsPath(token)
        posix = PurePosixPath(token)
        return bool(
            token
            and not windows.anchor
            and not windows.root
            and not windows.drive
            and not posix.is_absolute()
            and ".." not in windows.parts
            and ".." not in posix.parts
            and re.fullmatch(r"[A-Za-z0-9_./*?\[\]-]+", token)
            and (suffix is None or token.endswith(suffix))
        )

    if argv[:4] == ["python", "-m", "unittest", "discover"]:
        args = argv[4:]
        index = 0
        while index < len(args):
            flag = args[index]
            if flag == "-v":
                index += 1
                continue
            if flag in {"-s", "-t", "-p"} and index + 1 < len(args):
                argument = args[index + 1]
                if flag == "-s" and argument != "tests":
                    return False
                if flag == "-t" and argument != ".":
                    return False
                if flag == "-p" and not (
                    safe_relative(argument, suffix=".py") and argument.startswith("test")
                ):
                    return False
                index += 2
                continue
            return False
        return True
    if argv[:3] == ["python", "-m", "json.tool"]:
        return len(argv) == 4 and safe_relative(argv[3], suffix=".json")
    if argv[:4] == ["python", "-m", "fleet.token_planner", "validate"]:
        return len(argv) == 5 and safe_relative(argv[4], suffix=".json")
    if argv[:3] == ["python", "-m", "fleet.night_runner"]:
        return len(argv) == 4 and safe_relative(argv[3], suffix=".json")
    return False


def _git_repo_identity(repo: str) -> tuple[str, str, str]:
    result = subprocess.run(
        ["git", "-C", repo, "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if result.returncode:
        raise PlannerError("campaign mission repo must have a readable origin")
    origin = result.stdout.strip().replace("\\", "/").rstrip("/")
    scp = re.fullmatch(r"(?:[^@]+@)?([^:]+):(.+)", origin) if "://" not in origin else None
    if scp:
        host, path = scp.group(1), scp.group(2)
    else:
        parsed = urlparse(origin)
        host, path = parsed.hostname or "", parsed.path
    parts = [part for part in path.strip("/").split("/") if part]
    if len(parts) < 2 or not host:
        raise PlannerError("campaign mission origin is not a canonical repository URL")
    owner, name = parts[-2], parts[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return host.lower(), owner.lower(), name.lower()


@dataclass
class Planner:
    config: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path | str) -> "Planner":
        with Path(path).open(encoding="utf-8") as handle:
            return cls(json.load(handle))

    def recommend(
        self,
        job_class: str,
        complexity: int = 5,
        unattended: bool = False,
        usage: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
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
        if usage is not None:
            preferred = str(decision["agent"])
            ready, reason = self.quota_health(preferred, usage)
            if not ready:
                for fallback in self.config.get("fallbacks", {}).get(preferred, []):
                    fallback_ready, _ = self.quota_health(fallback, usage)
                    defaults = self.config.get("agent_defaults", {}).get(fallback)
                    if fallback_ready and defaults:
                        decision.update(defaults)
                        decision.update({
                            "agent": fallback,
                            "original_agent": preferred,
                            "fallback_reason": reason,
                        })
                        break
                else:
                    raise PlannerError(f"no quota-safe fallback for {preferred}: {reason}")
        return decision

    def metered_approval_health(
        self,
        agent: str,
        approval: Any,
        budget_usd: Any,
        *,
        now: datetime | None,
        require_enforceable_cap: bool,
    ) -> tuple[bool, str]:
        pool = self.config.get("cli_pools", {}).get(agent, {})
        quota_pool = str(pool.get("quota_pool") or agent)
        if not isinstance(approval, dict):
            return False, f"{agent} metered capacity requires an explicit approval object"
        unsupported = set(approval) - _METERED_APPROVAL_FIELDS
        missing = _METERED_APPROVAL_FIELDS - set(approval)
        if missing or unsupported:
            return False, f"{agent} metered approval has an invalid field contract"
        if approval.get("approved") is not True:
            return False, f"{agent} metered approval is not approved"
        if str(approval.get("provider")) != agent:
            return False, f"{agent} metered approval names a different provider"
        if str(approval.get("quota_pool")) != quota_pool:
            return False, f"{agent} metered approval names a different quota pool"
        if str(approval.get("currency")) != "USD":
            return False, f"{agent} metered approval currency must be USD"
        approval_id = str(approval.get("approval_id") or "")
        if not re.fullmatch(r"[A-Za-z0-9._:-]{8,128}", approval_id):
            return False, f"{agent} metered approval requires a bounded approval_id"
        if isinstance(approval["max_spend_usd"], bool) or isinstance(budget_usd, bool):
            return False, f"{agent} metered approval spend cap is invalid"
        try:
            cap = float(approval["max_spend_usd"])
            budget = float(budget_usd)
        except (TypeError, ValueError):
            return False, f"{agent} metered approval spend cap is invalid"
        if cap != cap or cap in {float("inf"), float("-inf")} or cap <= 0 or budget <= 0:
            return False, f"{agent} metered approval spend cap must be positive and finite"
        if cap > budget:
            return False, f"{agent} metered approval exceeds the mission budget"
        try:
            expires_at = datetime.fromisoformat(
                str(approval["expires_at"]).replace("Z", "+00:00")
            )
        except ValueError:
            return False, f"{agent} metered approval expiry is invalid"
        if expires_at.tzinfo is None:
            return False, f"{agent} metered approval expiry must include a timezone"
        if now is not None and expires_at <= now.astimezone(expires_at.tzinfo):
            return False, f"{agent} metered approval is expired"
        cap_arg = pool.get("hard_spend_cap_arg")
        if require_enforceable_cap and (
            not pool.get("hard_spend_cap_supported", False)
            or not isinstance(cap_arg, str)
            or not cap_arg.startswith("--")
        ):
            return False, f"{agent} launcher has no enforceable hard spend cap"
        return True, f"{agent} metered spend is explicitly approved up to ${cap:g} USD"

    def quota_health(
        self,
        agent: str,
        usage: dict[str, Any],
        *,
        metered_approval: Any = None,
        budget_usd: Any = 0,
        now: datetime | None = None,
    ) -> tuple[bool, str]:
        pool = self.config.get("cli_pools", {}).get(agent, {})
        quota_pool = str(pool.get("quota_pool") or agent)
        gate = self.config.get("subscription_gates", {}).get(
            quota_pool, self.config.get("subscription_gates", {}).get(agent)
        )
        mode = str(pool.get("mode") or (gate or {}).get("mode") or "measured")
        if mode == "metered":
            return self.metered_approval_health(
                agent,
                metered_approval,
                budget_usd,
                now=now or datetime.now(timezone.utc),
                require_enforceable_cap=True,
            )
        if mode == "control-only":
            return False, f"{agent} is control-only"
        if not gate or mode == "unmetered":
            return True, "quota gate not required"
        record = usage.get(quota_pool, usage.get(agent))
        if not record:
            if gate.get("allow_unmeasured", False):
                return True, "quota is not measured"
            return False, f"{quota_pool} quota is unavailable"
        try:
            remaining = _bounded_percent(record.get("remaining_percent"))
        except (TypeError, ValueError):
            return False, f"{quota_pool} quota is invalid or unavailable"
        floor = float(gate.get("minimum_remaining_percent", 0))
        if remaining <= 0:
            return False, f"{quota_pool} quota has 0% remaining"
        if remaining < floor:
            return False, f"{quota_pool} quota has {remaining:g}% remaining below {floor:g}% floor"
        return True, f"{quota_pool} quota has {remaining:g}% remaining"

    def normalize_quota_payload(self, payload: Any) -> dict[str, dict[str, Any]]:
        """Reduce provider telemetry to routing-safe fields only."""
        providers = payload if isinstance(payload, list) else payload.get("providers", [])
        provider_map = self.config.get("quota_providers", {})
        usage: dict[str, dict[str, Any]] = {}
        for provider in providers if isinstance(providers, list) else []:
            if not isinstance(provider, dict):
                continue
            label = str(provider.get("provider") or provider.get("label") or "")
            agent = provider_map.get(label)
            if not agent:
                continue
            metrics = provider.get("metrics") or provider.get("windows") or []
            if isinstance(metrics, dict):
                metrics = list(metrics.values())
            remaining_values: list[float] = []
            reset_values: list[str] = []
            invalid_remaining = False
            for metric in metrics if isinstance(metrics, list) else []:
                if not isinstance(metric, dict):
                    continue
                if "remaining_percent" in metric:
                    try:
                        remaining_values.append(_bounded_percent(metric["remaining_percent"]))
                    except (TypeError, ValueError):
                        invalid_remaining = True
                        break
                reset = metric.get("reset_at") or metric.get("resets_at")
                if reset:
                    reset_values.append(str(reset))
            if "remaining_percent" in provider:
                try:
                    remaining_values.append(_bounded_percent(provider["remaining_percent"]))
                except (TypeError, ValueError):
                    invalid_remaining = True
            if invalid_remaining or not remaining_values:
                continue
            usage[agent] = {
                "provider": label,
                "plan": str(provider.get("plan") or provider.get("tier") or "unknown"),
                "remaining_percent": min(remaining_values),
                "reset_at": min(reset_values) if reset_values else provider.get("reset_at"),
            }
        return usage

    def normalize_cli_health(self, payload: dict[str, Any]) -> dict[str, str]:
        probes = payload.get("subscription_clis", {})
        mapping = self.config.get("cli_capacity_keys", {})
        launch_allowed = bool(payload.get("resource_gate", {}).get("launch_allowed"))
        health = {
            agent: (
                str(probes.get(report_key, {}).get("status", "unknown"))
                if launch_allowed
                else "blocked-resource"
            )
            for agent, report_key in mapping.items()
        }
        health["hermes"] = "control-ready" if launch_allowed else "blocked-resource"
        return health

    def normalize_cli_health_by_machine(
        self, payloads: list[dict[str, Any]]
    ) -> dict[str, dict[str, str]]:
        health_by_machine: dict[str, dict[str, str]] = {}
        for payload in payloads:
            machine = str(payload.get("machine_id") or "").strip()
            if not machine:
                raise PlannerError("CLI capacity report is missing machine_id")
            if machine in health_by_machine:
                raise PlannerError(f"duplicate CLI capacity report for machine: {machine}")
            health_by_machine[machine] = self.normalize_cli_health(payload)
        return health_by_machine

    @staticmethod
    def _observation_is_private(value: Any) -> bool:
        if isinstance(value, dict):
            for key, item in value.items():
                if str(key).lower() in _PRIVATE_OBSERVATION_KEYS:
                    return True
                if Planner._observation_is_private(item):
                    return True
        elif isinstance(value, list):
            return any(Planner._observation_is_private(item) for item in value)
        return False

    def validate_observation(
        self,
        observation: dict[str, Any],
        manifest: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        required = {
            "observed_at",
            "agent",
            "job_class",
            "role",
            "duration_minutes",
            "outcome_status",
            "artifact_score",
            "receipt_id",
            "mission_id",
            "receipt_path",
            "receipt_sha256",
        }
        missing = sorted(required - set(observation))
        if missing:
            raise PlannerError(f"capacity observation missing: {', '.join(missing)}")
        if manifest is None:
            raise PlannerError("capacity observation requires its verified campaign manifest")
        if manifest.get("mode") != "campaign" or int(manifest.get("version", 0)) < 3:
            raise PlannerError("capacity observation learning requires a verified version-3 campaign")
        if self._observation_is_private(observation):
            raise PlannerError("capacity observation contains private identity or credential fields")
        unsupported = sorted(set(observation) - _OBSERVATION_FIELDS)
        if unsupported:
            raise PlannerError(f"capacity observation has unsupported fields: {', '.join(unsupported)}")
        if str(observation["agent"]) not in self.config.get("cli_pools", {}):
            raise PlannerError("capacity observation agent is not in cli_pools")
        if str(observation["role"]) not in {"maker", "verifier", "researcher", "integrator"}:
            raise PlannerError("capacity observation role is unsupported")
        if str(observation["outcome_status"]).upper() != "VERIFIED":
            raise PlannerError("capacity observation outcome_status must be VERIFIED")
        _positive_number(
            observation["duration_minutes"],
            "capacity observation duration_minutes",
        )
        score_value = observation["artifact_score"]
        if isinstance(score_value, bool) or not isinstance(score_value, int):
            raise PlannerError("capacity observation artifact_score must be an integer")
        score = score_value
        if not 0 <= score <= 4:
            raise PlannerError("capacity observation artifact_score must be between 0 and 4")
        before = observation.get("quota_before_percent")
        after = observation.get("quota_after_percent")
        if (before is None) != (after is None):
            raise PlannerError("capacity observation requires both quota before and after")
        if before is not None:
            try:
                _bounded_percent(before)
                _bounded_percent(after)
            except (TypeError, ValueError) as exc:
                raise PlannerError(
                    "capacity observation quota percentages must be finite and between 0 and 100"
                ) from exc

        self.validate_manifest(manifest)
        mission_id = str(observation["mission_id"])
        missions = [mission for mission in manifest.get("missions", []) if str(mission.get("id")) == mission_id]
        if len(missions) != 1:
            raise PlannerError("capacity observation mission_id must uniquely map to the manifest")
        mission = missions[0]
        if str(observation["agent"]) != str(mission.get("agent")):
            raise PlannerError("capacity observation agent does not match verified mission")
        if str(observation["role"]) != str(mission.get("role")):
            raise PlannerError("capacity observation role does not match verified mission")
        if str(observation["job_class"]) != str(mission.get("job_class")):
            raise PlannerError("capacity observation job_class does not match verified mission")
        receipt_path = str(observation["receipt_path"])
        if receipt_path.replace("\\", "/") != str(mission.get("receipt", "")).replace("\\", "/"):
            raise PlannerError("capacity observation receipt_path does not match mission receipt")
        receipt = _repo_path(mission, receipt_path)
        try:
            receipt_bytes = receipt.read_bytes()
        except OSError as exc:
            raise PlannerError(f"capacity observation receipt is unavailable: {exc}") from exc
        digest = hashlib.sha256(receipt_bytes).hexdigest()
        supplied_digest = str(observation["receipt_sha256"]).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", supplied_digest) or supplied_digest != digest:
            raise PlannerError("capacity observation receipt_sha256 does not match receipt bytes")
        if str(observation["receipt_id"]) != f"sha256:{digest}":
            raise PlannerError("capacity observation receipt_id must equal sha256:<receipt_sha256>")
        receipt_state, receipt_detail = self._receipt_state(mission)
        if receipt_state not in {"verified", "delivered"}:
            raise PlannerError(f"capacity observation receipt is not verified: {receipt_detail}")
        if hashlib.sha256(receipt.read_bytes()).hexdigest() != digest:
            raise PlannerError("capacity observation receipt changed during validation")
        return {key: observation[key] for key in _OBSERVATION_FIELDS if key in observation}

    def record_observation(
        self,
        history_path: Path | str,
        observation: dict[str, Any],
        manifest: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        validated = self.validate_observation(observation, manifest)
        path = Path(history_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = path.with_name(f"{path.name}.lock")
        deadline = time.monotonic() + 5
        lock_fd: int | None = None
        while lock_fd is None:
            try:
                lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise PlannerError(f"capacity history is locked: {path}")
                time.sleep(0.05)
        temp_path: Path | None = None
        try:
            records = load_json_records(path) if path.exists() else []
            if any(item.get("receipt_id") == validated["receipt_id"] for item in records):
                return {"recorded": False, "duplicate": True, "receipt_id": validated["receipt_id"]}
            records.append(validated)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temp_path = Path(handle.name)
                for item in records:
                    handle.write(json.dumps(item, separators=(",", ":")) + "\n")
            os.replace(temp_path, path)
            temp_path = None
            return {"recorded": True, "duplicate": False, "receipt_id": validated["receipt_id"]}
        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()
            os.close(lock_fd)
            lock_path.unlink(missing_ok=True)

    def capacity_forecast(
        self,
        history: list[dict[str, Any]],
        *,
        agent: str,
        job_class: str,
        role: str,
    ) -> dict[str, Any]:
        planning = self.config.get("daily_planning", {})
        matching = []
        for item in history:
            if (
                item.get("agent") != agent
                or item.get("job_class") != job_class
                or item.get("role") != role
                or str(item.get("outcome_status", "")).upper() != "VERIFIED"
            ):
                continue
            score = item.get("artifact_score")
            if isinstance(score, bool) or not isinstance(score, int) or score < 1 or score > 4:
                continue
            try:
                _positive_number(item.get("duration_minutes"), "history duration_minutes")
                before = item.get("quota_before_percent")
                after = item.get("quota_after_percent")
                if (before is None) != (after is None):
                    continue
                if before is not None:
                    _bounded_percent(before)
                    _bounded_percent(after)
            except (PlannerError, TypeError, ValueError):
                continue
            matching.append(item)
        successful = matching
        quota_deltas = [
            max(0.0, float(item["quota_before_percent"]) - float(item["quota_after_percent"]))
            for item in successful
            if item.get("quota_before_percent") is not None
            and item.get("quota_after_percent") is not None
        ]
        durations = [float(item["duration_minutes"]) for item in successful]
        default_delta = float(planning.get("default_quota_delta_percent", {}).get(role, 0))
        default_duration = float(planning.get("default_duration_minutes", {}).get(role, 60))
        sample_count = len(matching)
        success_rate = len(successful) / sample_count if sample_count else None
        return {
            "sample_count": sample_count,
            "verified_count": len(successful),
            "success_rate": round(success_rate, 3) if success_rate is not None else None,
            "predicted_quota_delta_percent": round(
                statistics.median(quota_deltas) if quota_deltas else default_delta, 2
            ),
            "predicted_duration_minutes": round(
                statistics.median(durations) if durations else default_duration
            ),
            "confidence": "high" if sample_count >= 8 else "medium" if sample_count >= 3 else "low",
        }

    def capacity_summary(
        self,
        usage: dict[str, Any],
        history: list[dict[str, Any]] | None = None,
    ) -> dict[str, dict[str, Any]]:
        planning = self.config.get("daily_planning", {})
        target_ratio = float(planning.get("target_usable_capacity_ratio", 0.85))
        summary: dict[str, dict[str, Any]] = {}
        for agent, pool in self.config.get("cli_pools", {}).items():
            quota_pool = str(pool.get("quota_pool") or agent)
            gate = self.config.get("subscription_gates", {}).get(
                quota_pool, self.config.get("subscription_gates", {}).get(agent, {})
            )
            mode = str(pool.get("mode") or gate.get("mode") or "measured")
            record = usage.get(quota_pool, usage.get(agent, {}))
            remaining = record.get("remaining_percent")
            floor = float(gate.get("minimum_remaining_percent", 0))
            if mode == "control-only":
                status, usable, target = "control-only", 0.0, 0.0
            elif mode == "metered":
                status, usable, target = "metered-blocked", None, None
            elif mode == "unmetered":
                status, usable, target = "unmetered", None, None
            elif remaining is None:
                status = "unmeasured" if gate.get("allow_unmeasured") else "unknown"
                usable, target = None, None
            else:
                try:
                    remaining = _bounded_percent(remaining)
                except (TypeError, ValueError):
                    status, remaining, usable, target = "invalid", None, None, None
                else:
                    usable = max(0.0, remaining - floor)
                    target = round(usable * target_ratio, 2)
                    status = "healthy" if usable > 0 else "reserve-only"
            summary[agent] = {
                "kind": pool.get("kind", "cli"),
                "quota_pool": quota_pool,
                "mode": mode,
                "status": status,
                "remaining_percent": remaining,
                "reserve_floor_percent": floor if mode == "measured" else None,
                "usable_percent": usable,
                "target_spend_percent": target,
                "reset_at": record.get("reset_at"),
                "machines": list(pool.get("machines", [])),
                "roles": list(pool.get("roles", [])),
                "history_samples": sum(1 for item in (history or []) if item.get("agent") == agent),
            }
        return summary

    def _daily_route_candidates(self, job_class: str) -> list[str]:
        route = self.config.get("routes", {}).get(
            job_class, self.config.get("routes", {}).get("refactor", {})
        )
        preferred = str(route.get("agent", ""))
        return [preferred, *self.config.get("fallbacks", {}).get(preferred, [])]

    @staticmethod
    def _parse_datetime(value: str | datetime, tz: ZoneInfo) -> datetime:
        parsed = value if isinstance(value, datetime) else datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        return parsed.astimezone(tz)

    @staticmethod
    def _day_part(moment: datetime) -> str:
        if 6 <= moment.hour < 12:
            return "morning"
        if 12 <= moment.hour < 18:
            return "afternoon"
        if 18 <= moment.hour < 23:
            return "evening"
        return "overnight"

    def plan_day(
        self,
        request: dict[str, Any],
        registry: dict[str, Any],
        usage: dict[str, Any],
        history: list[dict[str, Any]],
        *,
        now: str | datetime | None = None,
    ) -> dict[str, Any]:
        """Compile objective demand into quota-, evidence-, and machine-bounded daily lanes."""
        planning = self.config.get("daily_planning", {})
        tz = ZoneInfo(str(request.get("timezone") or planning.get("timezone", "UTC")))
        start = self._parse_datetime(now or datetime.now(tz), tz)
        horizon = start + timedelta(hours=float(planning.get("planning_horizon_hours", 24)))
        requested = request.get("objectives")
        if not isinstance(requested, list) or not requested:
            raise PlannerError("daily plan requires objectives")
        max_objectives = int(
            registry.get("policy", {}).get("max_top_level_objectives_per_campaign", 3)
        )
        if len(requested) > max_objectives:
            raise PlannerError(f"daily plan supports at most {max_objectives} objectives")
        requested_ids = [str(item.get("id", "")) for item in requested]
        duplicate_ids = sorted({item for item in requested_ids if requested_ids.count(item) > 1})
        if duplicate_ids:
            raise PlannerError(f"daily plan contains duplicate objective IDs: {', '.join(duplicate_ids)}")
        registry_by_id = {
            str(item.get("id")): item
            for item in registry.get("objectives", [])
            if item.get("id")
        }
        priority_rank = {"tier-0": 0, "now": 1, "next": 2, "later": 3}
        objective_rows: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for item in requested:
            objective_id = str(item.get("id", ""))
            canonical = registry_by_id.get(objective_id)
            if not canonical:
                raise PlannerError(f"daily objective {objective_id!r} is not in the canonical registry")
            if not item.get("job_class"):
                raise PlannerError(f"daily objective {objective_id} missing job_class")
            objective_rows.append((item, canonical))
        objective_rows.sort(
            key=lambda pair: (
                priority_rank.get(str(pair[1].get("priority", "later")), 9),
                -int(pair[0].get("priority_score", 50)),
                str(pair[0]["id"]),
            )
        )

        capacity = self.capacity_summary(usage, history)
        quota_left: dict[str, float] = {}
        for row in capacity.values():
            if row["target_spend_percent"] is not None:
                quota_left.setdefault(
                    str(row["quota_pool"]), float(row["target_spend_percent"])
                )
        lane_slots = {
            agent: int(planning.get("unmetered_lane_cap", 4))
            if row["status"] == "unmetered"
            else int(planning.get("unmeasured_lane_cap", 1))
            if row["status"] == "unmeasured"
            else 10_000
            for agent, row in capacity.items()
        }
        health = request.get("cli_health", {})
        health_by_machine = request.get("cli_health_by_machine", {})
        machine_status = request.get("machine_status", {})
        online_machines = {
            machine
            for machine, state in machine_status.items()
            if state is True or str(state).lower() in {"online", "ready", "live"}
        }
        machine_available = {machine: start for machine in online_machines}
        repo_writer_available: dict[str, datetime] = {}
        lanes: list[dict[str, Any]] = []
        blocked: list[dict[str, Any]] = []
        replan_at: set[str] = set()

        def select_route(
            job_class: str,
            role: str,
            excluded: set[str],
        ) -> tuple[dict[str, Any] | None, list[str]]:
            failures: list[str] = []
            route_template = self.config.get("routes", {}).get(
                job_class, self.config.get("routes", {}).get("refactor", {})
            )
            for agent in self._daily_route_candidates(job_class):
                if not agent or agent in excluded:
                    if agent:
                        failures.append(f"{agent}: excluded by maker/verifier separation")
                    continue
                pool = self.config.get("cli_pools", {}).get(agent)
                if not pool or pool.get("mode") == "control-only":
                    failures.append(f"{agent}: not an executable CLI pool")
                    continue
                supported_roles = set(pool.get("roles", []))
                if supported_roles and role not in supported_roles:
                    failures.append(f"{agent}: role {role} is unsupported")
                    continue
                machines = [machine for machine in pool.get("machines", []) if machine in online_machines]
                required_machine = route_template.get("machine")
                if required_machine:
                    machines = [machine for machine in machines if machine == required_machine]
                if health_by_machine:
                    machines = [
                        machine
                        for machine in machines
                        if str(health_by_machine.get(machine, {}).get(agent, "unknown")) == "ready"
                    ]
                elif str(health.get(agent, "unknown")) != "ready":
                    machines = []
                if not machines:
                    failures.append(f"{agent}: no live-ready admitted machine")
                    continue
                forecast = self.capacity_forecast(
                    history, agent=agent, job_class=job_class, role=role
                )
                predicted = float(forecast["predicted_quota_delta_percent"])
                row = capacity[agent]
                quota_pool = str(row["quota_pool"])
                if row["status"] in {"unknown", "reserve-only", "metered-blocked"}:
                    failures.append(f"{agent}: {row['status']}")
                    if row.get("reset_at"):
                        replan_at.add(str(row["reset_at"]))
                    continue
                if quota_left.get(quota_pool) is not None and predicted > float(quota_left[quota_pool]):
                    failures.append(f"{agent}: target quota envelope exhausted")
                    if row.get("reset_at"):
                        replan_at.add(str(row["reset_at"]))
                    continue
                if lane_slots.get(agent, 0) <= 0:
                    failures.append(f"{agent}: daily lane cap exhausted")
                    continue
                defaults = self.config.get("agent_defaults", {}).get(agent, {})
                return {
                    "route": {**route_template, **defaults, "agent": agent},
                    "forecast": forecast,
                    "machines": machines,
                    "predicted_quota_delta_percent": predicted,
                }, failures
            return None, failures

        def schedule_lane(
            *,
            objective: dict[str, Any],
            canonical: dict[str, Any],
            role: str,
            job_class: str,
            excluded: set[str],
            dependency_end: datetime | None = None,
        ) -> dict[str, Any] | None:
            selected, failures = select_route(job_class, role, excluded)
            if not selected:
                blocked.append({
                    "objective_id": canonical["id"],
                    "role": role,
                    "job_class": job_class,
                    "reasons": failures,
                })
                return None
            route = selected["route"]
            agent = str(route["agent"])
            machine = min(
                selected["machines"],
                key=lambda name: max(machine_available[name], dependency_end or start),
            )
            repo = str(canonical["repo"])
            repo_key = str(PureWindowsPath(repo)).replace("\\", "/").rstrip("/").casefold()
            writer_ready = repo_writer_available.get(repo_key, start)
            lane_start = max(machine_available[machine], dependency_end or start, writer_ready)
            duration = int(
                objective.get(f"{role}_minutes")
                or objective.get("estimated_minutes")
                or selected["forecast"]["predicted_duration_minutes"]
            )
            lane_end = lane_start + timedelta(minutes=duration)
            if lane_end > horizon:
                blocked.append({
                    "objective_id": canonical["id"],
                    "role": role,
                    "job_class": job_class,
                    "reasons": ["lane exceeds planning horizon"],
                })
                return None
            machine_available[machine] = lane_end
            repo_writer_available[repo_key] = lane_end
            predicted = selected["predicted_quota_delta_percent"]
            quota_pool = str(capacity[agent]["quota_pool"])
            if quota_left.get(quota_pool) is not None:
                quota_left[quota_pool] = round(float(quota_left[quota_pool]) - predicted, 2)
            lane_slots[agent] -= 1
            lane = {
                "lane_id": f"{canonical['id']}-{role}",
                "objective_id": canonical["id"],
                "executive_owner": canonical["executive_owner"],
                "outcome": canonical["outcome"],
                "success_metric": canonical["success_metric"],
                "repo": canonical["repo"],
                "role": role,
                "job_class": job_class,
                "agent": agent,
                "quota_pool": quota_pool,
                "model": route.get("model"),
                "machine": machine,
                "start_at": lane_start.isoformat(),
                "end_at": lane_end.isoformat(),
                "day_part": self._day_part(lane_start),
                "estimated_duration_minutes": duration,
                "estimated_quota_delta_percent": predicted,
                "forecast_confidence": selected["forecast"]["confidence"],
                "admission_state": "planned-live-ready",
                "artifact_contract": objective.get("artifact_contract"),
                "next_contract": "compile into a version-3 campaign mission before execution",
            }
            lanes.append(lane)
            return lane

        for objective, canonical in objective_rows:
            maker = schedule_lane(
                objective=objective,
                canonical=canonical,
                role="maker",
                job_class=str(objective["job_class"]),
                excluded=set(),
            )
            if maker and bool(objective.get("independent_verifier", True)):
                schedule_lane(
                    objective=objective,
                    canonical=canonical,
                    role="verifier",
                    job_class="independent-review",
                    excluded={str(maker["agent"])},
                    dependency_end=self._parse_datetime(maker["end_at"], tz),
                )

        lanes.sort(key=lambda lane: (lane["start_at"], lane["machine"], lane["lane_id"]))
        for wave, lane in enumerate(lanes, start=1):
            lane["wave"] = wave
        allocated_agents = {lane["agent"] for lane in lanes}
        unallocated = {
            agent: {
                "status": row["status"],
                "remaining_target_percent": quota_left.get(str(row["quota_pool"])),
                "reason": (
                    "no additional objective lane admitted; synthetic burn is forbidden"
                    if agent not in allocated_agents
                    else "capacity remains for the next receipt-triggered replan"
                ),
            }
            for agent, row in capacity.items()
        }
        return {
            "schema_version": 1,
            "plan_date": str(request.get("date") or start.date()),
            "timezone": str(tz),
            "generated_at": start.isoformat(),
            "horizon_end": horizon.isoformat(),
            "optimization_objective": self.config.get("optimization_objective"),
            "capacity": capacity,
            "lanes": lanes,
            "blocked": blocked,
            "unallocated_capacity": unallocated,
            "replan_at": sorted(replan_at),
            "replan_triggers": [
                "after every mission receipt",
                "after quota reset or a changed remaining-percent reading",
                "after CLI health, machine heartbeat, or resource posture changes",
                f"every {int(planning.get('replan_interval_minutes', 90))} minutes while objective demand remains",
            ],
            "policy": {
                "reserve_is_preserved": True,
                "one_writer_per_repo": True,
                "independent_verifier": True,
                "tokens_are_capacity_not_outcomes": True,
                "tracker_is_sensor_not_orchestrator": True,
            },
        }

    def validate_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        mode = manifest.get("mode")
        if mode not in {"night", "campaign"}:
            raise PlannerError("manifest mode must be night or campaign")
        version = int(manifest.get("version", 1))
        if mode == "campaign" and version < 3:
            raise PlannerError("campaign manifests require version 3")
        objective_ids: set[str] = set()
        if mode == "campaign":
            if not manifest.get("campaign_id"):
                raise PlannerError("campaign manifest requires campaign_id")
            control_repo = str(manifest.get("control_repo", ""))
            registry_value = str(manifest.get("objective_registry", ""))
            if not control_repo or not registry_value:
                raise PlannerError("campaign manifest requires control_repo and objective_registry")
            canonical_control = (
                _CANONICAL_GITHUB_HOST,
                _CANONICAL_GITHUB_OWNER,
                _CANONICAL_CONTROL_REPO,
            )
            if _git_repo_identity(control_repo) != canonical_control:
                raise PlannerError("campaign control_repo is not the canonical frankxai control repository")
            registry_path = _portable_repo_path(
                control_repo, registry_value, "campaign objective_registry"
            )
            try:
                registry_payload = json.loads(registry_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise PlannerError(f"cannot load objective registry: {exc}") from exc
            registry_by_id = {
                str(item.get("id")): item
                for item in registry_payload.get("objectives", [])
                if item.get("id")
            }
            stop_conditions = manifest.get("stop_conditions")
            if not isinstance(stop_conditions, list) or not stop_conditions:
                raise PlannerError("campaign manifest requires stop_conditions")
            objectives = manifest.get("objectives")
            if not isinstance(objectives, list) or not objectives:
                raise PlannerError("campaign manifest requires objectives")
            if len(objectives) > 3:
                raise PlannerError("campaign supports at most three objectives")
            for objective in objectives:
                objective_id = str(objective.get("id", ""))
                if not objective_id or objective_id in objective_ids:
                    raise PlannerError("objective ids must be non-empty and unique")
                if not objective.get("success_metric"):
                    raise PlannerError(f"objective {objective_id} missing success_metric")
                canonical = registry_by_id.get(objective_id)
                if not canonical:
                    raise PlannerError(f"objective {objective_id} is not in the canonical registry")
                for key in ("repo", "executive_owner", "outcome", "success_metric"):
                    if objective.get(key) != canonical.get(key):
                        raise PlannerError(
                            f"objective {objective_id} {key} does not match the canonical registry"
                        )
                objective_ids.add(objective_id)
            max_concurrency = int(manifest.get("max_concurrency", 1))
            if max_concurrency != 1:
                raise PlannerError("campaign max_concurrency must be 1 for the sequential runner")
        declared = _bounded_money(
            manifest.get("total_budget_usd", 0), "declared budget"
        )
        cap = _bounded_money(self.config["night_cap_usd"], "night cap")
        if declared > cap:
            raise PlannerError(f"declared budget ${declared:g} exceeds night cap ${cap:g}")
        missions = manifest.get("missions")
        if not isinstance(missions, list) or not missions:
            raise PlannerError("manifest requires at least one mission")
        ids: set[str] = set()
        mission_by_id: dict[str, dict[str, Any]] = {}
        total = 0.0
        objective_roles: dict[str, dict[str, set[str]]] = {
            objective_id: {"maker": set(), "verifier": set()} for objective_id in objective_ids
        }
        writer_leases: set[tuple[str, int]] = set()
        metered_approval_ids: set[str] = set()
        wave_totals: dict[int, float] = {}
        for mission in missions:
            mission_id = str(mission.get("id", ""))
            if not mission_id or mission_id in ids:
                raise PlannerError("mission ids must be non-empty and unique")
            ids.add(mission_id)
            mission_by_id[mission_id] = mission
            budget = _bounded_money(
                mission.get("budget_usd", 0), f"mission {mission_id} budget"
            )
            branch = str(mission.get("branch", ""))
            allowed_prefixes = ("night/",) if mode == "night" else ("night/", "agent/")
            if not branch.startswith(allowed_prefixes):
                raise PlannerError(
                    f"mission {mission_id} branch must start with {' or '.join(allowed_prefixes)}"
                )
            for key in ("agent", "repo", "task", "report"):
                if not mission.get(key):
                    raise PlannerError(f"mission {mission_id} missing {key}")
            mission_pool = self.config.get("cli_pools", {}).get(str(mission["agent"]), {})
            if str(mission_pool.get("mode")) == "metered" and mode != "campaign":
                raise PlannerError(
                    f"mission {mission_id} metered agents require an explicitly approved campaign"
                )
            task = str(mission["task"])
            for pattern, label in _PROHIBITED_TASK_PATTERNS.items():
                if re.search(pattern, task, flags=re.IGNORECASE):
                    raise PlannerError(f"mission {mission_id} task contains prohibited operation: {label}")
            if version >= 2:
                if not mission.get("receipt"):
                    raise PlannerError(f"mission {mission_id} missing receipt")
                role = str(mission.get("role", ""))
                if role not in {"maker", "verifier", "researcher", "integrator"}:
                    raise PlannerError(f"mission {mission_id} requires a supported role")
                checks = mission.get("acceptance_commands")
                if not isinstance(checks, list) or not checks:
                    raise PlannerError(f"mission {mission_id} requires acceptance_commands")
                for check in checks:
                    if not _safe_acceptance_command(check):
                        raise PlannerError(
                            f"mission {mission_id} has unsafe or unsupported acceptance command"
                        )
                verification_ids = mission.get("verification_ids")
                if (
                    not isinstance(verification_ids, list)
                    or len(verification_ids) != len(checks)
                    or len(set(map(str, verification_ids))) != len(verification_ids)
                ):
                    raise PlannerError(
                        f"mission {mission_id} verification_ids must uniquely map to acceptance_commands"
                    )
                artifacts = mission.get("required_artifacts")
                if not isinstance(artifacts, list) or not artifacts:
                    raise PlannerError(f"mission {mission_id} requires required_artifacts")
                _portable_repo_path(str(mission["repo"]), str(mission["report"]), f"mission {mission_id}")
                _portable_repo_path(str(mission["repo"]), str(mission["receipt"]), f"mission {mission_id}")
                for artifact in artifacts:
                    _portable_repo_path(str(mission["repo"]), str(artifact), f"mission {mission_id}")
            if mode == "campaign":
                objective_id = str(mission.get("objective_id", ""))
                if objective_id not in objective_ids:
                    raise PlannerError(f"mission {mission_id} has unknown objective_id")
                canonical_repo = str(registry_by_id[objective_id]["repo"])
                expected_identity = (
                    _CANONICAL_GITHUB_HOST,
                    _CANONICAL_GITHUB_OWNER,
                    canonical_repo.lower(),
                )
                if _git_repo_identity(str(mission["repo"])) != expected_identity:
                    raise PlannerError(
                        f"mission {mission_id} repo does not match objective {objective_id}"
                    )
                for key in ("outcome", "receipt", "role", "quota_pool", "machine"):
                    if not mission.get(key):
                        raise PlannerError(f"mission {mission_id} missing {key}")
                role = str(mission["role"])
                if role not in {"maker", "verifier", "integrator", "researcher"}:
                    raise PlannerError(f"mission {mission_id} has unsupported role")
                job_class = str(mission.get("job_class", ""))
                if not job_class or job_class not in self.config.get("routes", {}):
                    raise PlannerError(f"campaign mission {mission_id} has unsupported job_class")
                agent = str(mission["agent"])
                pool = self.config.get("cli_pools", {}).get(agent)
                if not pool:
                    raise PlannerError(f"mission {mission_id} has unsupported agent")
                expected_quota_pool = str(pool.get("quota_pool") or agent)
                if str(mission["quota_pool"]) != expected_quota_pool:
                    raise PlannerError(
                        f"mission {mission_id} quota_pool must match configured pool {expected_quota_pool}"
                    )
                supported_roles = set(pool.get("roles", []))
                if supported_roles and role not in supported_roles:
                    raise PlannerError(f"mission {mission_id} agent does not support role {role}")
                machine = str(mission["machine"])
                if machine not in set(map(str, pool.get("machines", []))):
                    raise PlannerError(
                        f"mission {mission_id} agent is not configured for machine {machine}"
                    )
                approval = mission.get("metered_spend_approval")
                if str(pool.get("mode")) == "metered":
                    approval_ready, approval_detail = self.metered_approval_health(
                        agent,
                        approval,
                        mission.get("budget_usd"),
                        now=None,
                        require_enforceable_cap=False,
                    )
                    if not approval_ready:
                        raise PlannerError(f"mission {mission_id}: {approval_detail}")
                    approval_id = str(approval["approval_id"])
                    if approval_id in metered_approval_ids:
                        raise PlannerError("metered approval_id must be unique per mission")
                    metered_approval_ids.add(approval_id)
                elif approval is not None:
                    raise PlannerError(
                        f"mission {mission_id} has metered approval for a non-metered agent"
                    )
                wave = int(mission.get("wave", 0))
                if wave < 1:
                    raise PlannerError(f"mission {mission_id} wave must be positive")
                artifacts = mission.get("required_artifacts")
                verification_ids = mission.get("verification_ids")
                if not isinstance(artifacts, list) or not artifacts:
                    raise PlannerError(f"mission {mission_id} requires required_artifacts")
                if not isinstance(verification_ids, list) or not verification_ids:
                    raise PlannerError(f"mission {mission_id} requires verification_ids")
                if len(verification_ids) != len(checks) or len(set(verification_ids)) != len(verification_ids):
                    raise PlannerError(
                        f"mission {mission_id} verification_ids must uniquely map to acceptance_commands"
                    )
                _require_portable_path(mission, "report", str(mission["report"]))
                _require_portable_path(mission, "receipt", str(mission["receipt"]))
                for artifact in artifacts:
                    _require_portable_path(mission, "required_artifact", str(artifact))
                if role in {"maker", "verifier"}:
                    objective_roles[objective_id][role].add(str(mission["agent"]))
                if role in {"maker", "integrator"}:
                    lease = (str(Path(mission["repo"]).resolve()), wave)
                    if lease in writer_leases:
                        raise PlannerError(
                            f"mission {mission_id} duplicates a writer lease for repo and wave"
                        )
                    writer_leases.add(lease)
            total += budget
            if mode == "campaign":
                wave_totals[wave] = wave_totals.get(wave, 0.0) + budget
            if mission["agent"] == "claude" and not mission.get("max_turns"):
                raise PlannerError(f"mission {mission_id} Claude requires max_turns")
            if int(mission.get("timeout_minutes", 60)) > 180:
                raise PlannerError(f"mission {mission_id} timeout exceeds 180 minutes")
        if mode == "campaign":
            for mission in missions:
                if mission.get("role") != "verifier":
                    continue
                mission_id = str(mission["id"])
                maker_ids = {
                    str(other["id"])
                    for other in missions
                    if other.get("objective_id") == mission.get("objective_id")
                    and other.get("role") == "maker"
                }
                dependencies = mission.get("depends_on")
                if not isinstance(dependencies, list) or set(dependencies) != maker_ids:
                    raise PlannerError(
                        f"mission {mission_id} depends_on must name every maker for its objective"
                    )
                for dependency_id in dependencies:
                    dependency = mission_by_id.get(str(dependency_id))
                    if not dependency or dependency.get("role") != "maker":
                        raise PlannerError(f"mission {mission_id} has invalid maker dependency")
                    if int(dependency["wave"]) >= int(mission["wave"]):
                        raise PlannerError(
                            f"mission {mission_id} verifier wave must be after maker wave"
                        )
        if total > declared:
            raise PlannerError(f"mission budgets ${total:g} exceed declared budget ${declared:g}")
        if mode == "campaign":
            declared_wave_budgets = manifest.get("wave_budgets_usd")
            if not isinstance(declared_wave_budgets, dict) or not declared_wave_budgets:
                raise PlannerError("campaign manifest requires wave_budgets_usd")
            bounded_wave_budgets = {
                str(wave_number): _bounded_money(
                    value, f"campaign wave {wave_number} budget"
                )
                for wave_number, value in declared_wave_budgets.items()
            }
            for wave_number, spent in wave_totals.items():
                cap_value = bounded_wave_budgets.get(str(wave_number))
                if cap_value is None:
                    raise PlannerError(f"campaign wave {wave_number} has no budget")
                if spent > cap_value:
                    raise PlannerError(
                        f"campaign wave {wave_number} missions ${spent:g} exceed wave budget "
                        f"${cap_value:g}"
                    )
            for objective_id, roles in objective_roles.items():
                if not roles["maker"] or not roles["verifier"]:
                    raise PlannerError(
                        f"objective {objective_id} requires maker and verifier missions"
                    )
                if roles["maker"] & roles["verifier"]:
                    raise PlannerError(
                        f"objective {objective_id} maker and verifier agents must differ"
                    )
            minimum = int(manifest.get("minimum_verified_outcomes", len(objective_ids)))
            if not 1 <= minimum <= len(objective_ids):
                raise PlannerError("minimum_verified_outcomes must fit the objective count")
        return {
            "valid": True,
            "mode": mode,
            "mission_count": len(missions),
            "objective_count": len(objective_ids),
            "budget_usd": total,
            "cap_usd": cap,
        }

    def _task_contract(self, mission: dict[str, Any]) -> str:
        rules = (
            "HARD RULES: Work only in the exact current branch/worktree. No main push. "
            "No force-push. No git reset --hard. No secrets. Never widen sandbox or approvals. "
            "WINDOWS PHONE LINK PATH BAN: Never recursively search C:/, C:/Users/frank, home, ~, "
            "Desktop, Documents, Downloads, OneDrive, This PC, or phone/MTP paths; search only the "
            f"exact repo leaf {mission['repo']}. STORAGE GATE: Do not clone, add worktrees, bulk-install "
            "dependencies, or generate media in this mission."
        )
        acceptance = mission.get("acceptance_commands") or []
        receipt = mission.get("receipt")
        contract = [rules, "", str(mission["task"])]
        if mission.get("objective_id"):
            contract = [
                rules,
                "",
                f"OBJECTIVE: {mission['objective_id']}",
                f"ROLE: {mission['role']}",
                f"REQUIRED OUTCOME: {mission['outcome']}",
                f"REQUIRED ARTIFACTS: {', '.join(mission['required_artifacts'])}",
                f"VERIFICATION IDS: {', '.join(mission['verification_ids'])}",
                "",
                str(mission["task"]),
            ]
        if acceptance:
            contract += [
                "",
                "ACCEPTANCE COMMANDS (run exactly from the current repo working directory; do not "
                "prepend cd, append wrappers, or substitute a different shell; record exact exit codes):",
            ]
            contract += [f"- {command}" for command in acceptance]
        if receipt:
            contract += [
                "",
                f"Write machine-readable receipt JSON to: {receipt}",
                "Receipt fields: schema_version=1, mission_id, objective_id when present, role, "
                "agent, execution_status=ok|error|skipped, outcome_status=VERIFIED|HOLD|BLOCKED|FAILED, "
                "status=verified|delivered, branch, commit, artifacts, "
                "verification[{id,command,exit_code,status}], integration_state, completed_at.",
                f"Also write the human report to: {mission['report']}",
            ]
        return "\n".join(contract)

    def command_args(self, mission: dict[str, Any], *, sandbox: str = "workspace-write") -> list[str]:
        task = self._task_contract(mission)
        agent = str(mission["agent"])
        if agent == "claude":
            allowed_tools = ["Read", "Glob", "Grep", "Write", "Edit"]
            for command in mission.get("acceptance_commands") or []:
                if _safe_acceptance_command(command):
                    allowed_tools.extend((f"Bash({command})", f"PowerShell({command})"))
            return self._assert_launch_safe([
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
                "--allowedTools",
                ",".join(allowed_tools),
            ])
        if agent == "codex":
            selected_sandbox = "read-only" if mission.get("read_only") else sandbox
            return self._assert_launch_safe([
                "codex",
                "exec",
                "-C",
                str(mission["repo"]),
                "--sandbox",
                selected_sandbox,
                "-m",
                str(mission.get("model", "gpt-5.6-terra")),
                "-c",
                f"model_reasoning_effort={mission.get('reasoning_effort', 'high')}",
                task,
            ])
        if agent == "opencode":
            return self._assert_launch_safe(["opencode", "run", task])
        if agent == "gemini":
            return self._assert_launch_safe(["gemini", "-p", task])
        if agent == "agy":
            timeout_minutes = int(mission.get("timeout_minutes", 60))
            return self._assert_launch_safe([
                "agy",
                "--print-timeout",
                f"{timeout_minutes}m0s",
                "-p",
                task,
            ])
        if agent == "grok":
            return self._assert_launch_safe([
                "grok", "--single", task,
                "--cwd", str(mission["repo"]),
                "--model", str(mission.get("model", "grok-4.5")),
                "--max-turns", str(int(mission["max_turns"])),
                "--output-format", "json",
                "--permission-mode", "acceptEdits",
                "--sandbox", "workspace-write",
                "--no-memory", "--no-subagents", "--check",
            ])
        if agent == "dcode":
            approval_ready, approval_detail = self.metered_approval_health(
                agent,
                mission.get("metered_spend_approval"),
                mission.get("budget_usd", 0),
                now=datetime.now(timezone.utc),
                require_enforceable_cap=True,
            )
            if not approval_ready:
                raise PlannerError(approval_detail)
            pool = self.config["cli_pools"][agent]
            spend_cap = mission["metered_spend_approval"]["max_spend_usd"]
            timeout_seconds = int(mission.get("timeout_minutes", 60)) * 60
            return self._assert_launch_safe([
                "dcode", "--non-interactive", task,
                "--model", str(mission.get("model", "gpt-5.5")),
                "--max-turns", str(int(mission["max_turns"])),
                "--timeout", str(timeout_seconds),
                str(pool["hard_spend_cap_arg"]), str(spend_cap),
                "--no-mcp", "--json",
            ])
        raise PlannerError(f"agent {agent!r} has no unattended launcher")

    @staticmethod
    def _assert_launch_safe(args: list[str]) -> list[str]:
        lowered = {item.lower() for item in args}
        forbidden = sorted(lowered & _FORBIDDEN_LAUNCH_TOKENS)
        if forbidden:
            raise PlannerError(f"launcher contains prohibited sandbox bypass: {', '.join(forbidden)}")
        return args

    def command_for(self, mission: dict[str, Any]) -> str:
        return shlex.join(self.command_args(mission))

    @staticmethod
    def _commit_state(mission: dict[str, Any], commit: str) -> tuple[bool, str]:
        repo = str(mission["repo"])
        exists = subprocess.run(
            ["git", "-C", repo, "cat-file", "-e", f"{commit}^{{commit}}"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if exists.returncode:
            return False, "commit does not exist in mission repo"
        branch = str(mission["branch"])
        for ref in (branch, f"origin/{branch}"):
            resolved = subprocess.run(
                ["git", "-C", repo, "rev-parse", "--verify", ref],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if resolved.returncode:
                continue
            ancestor = subprocess.run(
                ["git", "-C", repo, "merge-base", "--is-ancestor", commit, ref],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if ancestor.returncode == 0:
                return True, "commit is reachable from expected branch"
        return False, "commit is not reachable from expected branch"

    @staticmethod
    def _artifact_commit_state(
        mission: dict[str, Any], commit: str, artifact: str
    ) -> tuple[bool, str]:
        repo = str(mission["repo"])
        tracked = subprocess.run(
            ["git", "-C", repo, "cat-file", "-e", f"{commit}:{artifact}"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if tracked.returncode:
            return False, f"artifact is not present at receipt commit: {artifact}"
        unchanged = subprocess.run(
            ["git", "-C", repo, "diff", "--quiet", commit, "--", artifact],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if unchanged.returncode:
            return False, f"artifact differs from receipt commit: {artifact}"
        return True, "artifact matches receipt commit"

    def _receipt_state(self, mission: dict[str, Any]) -> tuple[str, str]:
        receipt_value = mission.get("receipt")
        if not receipt_value:
            return "missing-receipt", "manifest has no receipt path"
        try:
            receipt = _repo_path(mission, str(receipt_value))
        except PlannerError as exc:
            return "invalid-receipt", str(exc)
        if not receipt.is_file():
            return "missing-receipt", str(receipt)
        try:
            payload = json.loads(receipt.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return "invalid-receipt", str(exc)
        if not isinstance(payload, dict):
            return "invalid-receipt", "receipt must be a JSON object"
        if payload.get("schema_version") != 1:
            return "invalid-receipt", "schema_version must be 1"
        if payload.get("mission_id") != mission.get("id"):
            return "invalid-receipt", "mission_id mismatch"
        if payload.get("branch") != mission.get("branch"):
            return "invalid-receipt", "branch mismatch"
        if mission.get("objective_id") and payload.get("objective_id") != mission.get("objective_id"):
            return "invalid-receipt", "objective_id mismatch"
        if payload.get("role") != mission.get("role"):
            return "invalid-receipt", "role mismatch"
        if mission.get("machine") and payload.get("machine") != mission.get("machine"):
            return "invalid-receipt", "machine mismatch"
        outcome = str(payload.get("outcome_status", "FAILED")).upper()
        if outcome in {"HOLD", "BLOCKED", "FAILED"}:
            return outcome.lower(), f"outcome_status={outcome}"
        if str(payload.get("agent", "")) != str(mission.get("agent", "")):
            return "invalid-receipt", "verified receipt agent does not match the committed manifest route"
        if payload.get("execution_status") != "ok" or outcome != "VERIFIED":
            return "unverified", "execution or outcome status is not verified"
        if payload.get("status") not in {"verified", "delivered"}:
            return "unverified", "status is not verified/delivered"
        commit = str(payload.get("commit", ""))
        if not commit:
            return "unverified", "commit missing"
        commit_valid, commit_detail = self._commit_state(mission, commit)
        if not commit_valid:
            return "invalid-receipt", commit_detail
        checks = payload.get("verification")
        if not isinstance(checks, list) or not checks:
            return "unverified", "verification missing"
        required_artifacts = mission.get("required_artifacts")
        verification_ids = mission.get("verification_ids")
        acceptance_commands = mission.get("acceptance_commands")
        if not isinstance(required_artifacts, list) or not required_artifacts:
            return "invalid-receipt", "manifest required_artifacts missing"
        if (
            not isinstance(verification_ids, list)
            or not isinstance(acceptance_commands, list)
            or len(verification_ids) != len(acceptance_commands)
            or len(set(map(str, verification_ids))) != len(verification_ids)
        ):
            return "invalid-receipt", "manifest verification contract missing"
        declared_artifacts = {str(item) for item in payload.get("artifacts", [])}
        for artifact in required_artifacts:
            if str(artifact) not in declared_artifacts:
                return "unverified", f"receipt missing artifact: {artifact}"
            try:
                resolved = _repo_path(mission, str(artifact))
            except PlannerError as exc:
                return "invalid-receipt", str(exc)
            if not resolved.is_file() or resolved.stat().st_size == 0:
                return "unverified", f"artifact missing: {artifact}"
            matches_commit, artifact_detail = self._artifact_commit_state(
                mission, commit, str(artifact)
            )
            if not matches_commit:
                return "invalid-receipt", artifact_detail
        expected_checks = dict(zip(map(str, verification_ids), map(str, acceptance_commands), strict=True))
        recorded_checks: dict[str, str] = {}
        for check in checks:
            if not isinstance(check, dict):
                return "invalid-receipt", "verification entry must be an object"
            check_id = str(check.get("id", ""))
            command = str(check.get("command", ""))
            if check_id in recorded_checks:
                return "invalid-receipt", f"duplicate verification id: {check_id}"
            if expected_checks.get(check_id) != command:
                return "invalid-receipt", f"verification command mismatch: {check_id}"
            try:
                exit_code = int(check.get("exit_code", 1))
            except (TypeError, ValueError):
                return "invalid-receipt", f"verification exit code is invalid: {check_id}"
            if check.get("status") != "passed" or exit_code != 0:
                return "failed-verification", f"verification failed: {check_id}"
            recorded_checks[check_id] = command
        missing_ids = set(expected_checks) - set(recorded_checks)
        if missing_ids:
            return "unverified", f"verification ids missing: {','.join(sorted(missing_ids))}"
        if payload.get("integration_state") not in {
            "pr_open",
            "merged",
            "delivered",
            "rejected",
            "hold",
        }:
            return "unverified", "integration_state missing"
        completed_at = payload.get("completed_at")
        if not isinstance(completed_at, str) or "T" not in completed_at:
            return "unverified", "completed_at missing or invalid"
        agent = str(mission.get("agent", ""))
        pool = self.config.get("cli_pools", {}).get(agent, {})
        if str(pool.get("mode", "")) == "metered":
            admitted, admission_detail = self.metered_approval_health(
                agent,
                mission.get("metered_spend_approval"),
                mission.get("budget_usd", 0),
                now=datetime.now(timezone.utc),
                require_enforceable_cap=True,
            )
            if not admitted:
                return "blocked-admission", admission_detail
        return str(payload["status"]), "receipt accepted"

    def recorded_agent(self, mission: dict[str, Any]) -> str | None:
        receipt_value = mission.get("receipt")
        if not receipt_value:
            return None
        receipt = _repo_path(mission, str(receipt_value))
        try:
            payload = json.loads(receipt.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        agent = payload.get("agent")
        return str(agent) if agent else None

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
        result: dict[str, Any] = {
            "complete": complete,
            "missing": len(rows) - complete,
            "missions": rows,
        }
        if manifest.get("mode") == "campaign":
            objective_states = {}
            for objective in manifest.get("objectives", []):
                objective_id = str(objective["id"])
                states = [
                    row["status"]
                    for row, mission in zip(rows, manifest["missions"], strict=True)
                    if mission.get("objective_id") == objective_id
                ]
                if states and all(state in {"verified", "delivered"} for state in states):
                    objective_states[objective_id] = "VERIFIED"
                elif any(state in {"failed-verification", "failed", "invalid-receipt"} for state in states):
                    objective_states[objective_id] = "FAILED"
                elif any(state == "blocked" for state in states):
                    objective_states[objective_id] = "BLOCKED"
                elif any(state == "hold" for state in states):
                    objective_states[objective_id] = "HOLD"
                else:
                    objective_states[objective_id] = "MISSING"
            result["objectives"] = objective_states
            result["verified_objectives"] = sum(
                state == "VERIFIED" for state in objective_states.values()
            )
        return result

    def active_wave(self, manifest: dict[str, Any]) -> int | None:
        if manifest.get("mode") != "campaign":
            return None
        status_by_id = {row["id"]: row["status"] for row in self.status(manifest)["missions"]}
        terminal = {
            "verified",
            "delivered",
            "hold",
            "blocked",
            "failed",
            "failed-verification",
            "invalid-receipt",
        }
        pending_waves = [
            int(mission["wave"])
            for mission in manifest["missions"]
            if status_by_id[mission["id"]] not in terminal
            and self.dependency_state(mission, status_by_id) == "ready"
        ]
        return min(pending_waves) if pending_waves else None

    @staticmethod
    def dependency_state(mission: dict[str, Any], status_by_id: dict[str, str]) -> str:
        dependencies = mission.get("depends_on") or []
        if not dependencies:
            return "ready"
        states = [status_by_id.get(str(dependency), "missing-receipt") for dependency in dependencies]
        if all(state in {"verified", "delivered"} for state in states):
            return "ready"
        if any(
            state in {"hold", "blocked", "failed", "failed-verification", "invalid-receipt"}
            for state in states
        ):
            return "blocked"
        return "waiting"

    def debrief(self, manifest: dict[str, Any]) -> str:
        state = self.status(manifest)
        title = "Campaign" if manifest.get("mode") == "campaign" else "Night"
        lines = [
            f"# {title} debrief — {manifest.get('date', 'unknown')}",
            "",
            f"Budget envelope: ${float(manifest.get('total_budget_usd', 0)):g}",
            f"Missions: {state['complete']} verified/delivered · {state['missing']} incomplete",
            "",
            "| Mission | Agent | Status | Receipt |",
            "|---------|-------|--------|---------|",
        ]
        for row in state["missions"]:
            lines.append(f"| {row['id']} | {row['agent']} | {row['status']} | `{row['receipt']}` |")
        if manifest.get("mode") == "campaign":
            lines += [
                "",
                f"Verified objectives: {state['verified_objectives']} / {len(state['objectives'])}",
            ]
        lines += [
            "",
            "**Human review required.** No unattended merge, main push, or production deploy.",
        ]
        return "\n".join(lines) + "\n"


def load_json(path: str) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_json_records(path: str | None) -> list[dict[str, Any]]:
    if not path or not Path(path).exists():
        return []
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        payload = json.loads(text)
        if not isinstance(payload, list):
            raise PlannerError("history JSON must be a list")
        return [item for item in payload if isinstance(item, dict)]
    records = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PlannerError(f"invalid history JSONL at line {line_number}: {exc}") from exc
        if not isinstance(item, dict):
            raise PlannerError(f"history JSONL line {line_number} is not an object")
        records.append(item)
    return records


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
    daily = sub.add_parser("daily-plan")
    daily.add_argument("request")
    daily.add_argument(
        "--registry",
        default=str(Path(__file__).resolve().parents[1] / "objectives-registry.json"),
    )
    daily.add_argument("--quota", default=None, help="sanitized map or raw Tokscale JSON snapshot")
    daily.add_argument(
        "--cli-capacity",
        action="append",
        default=None,
        help="redacted cli_capacity.py report; repeat once per machine",
    )
    daily.add_argument("--history", default=None, help="private JSON or JSONL capacity observations")
    daily.add_argument("--now", default=None, help="deterministic ISO-8601 planning timestamp")
    daily.add_argument("--output", default=None)
    observe = sub.add_parser("record-observation")
    observe.add_argument("observation")
    observe.add_argument("--history", required=True)
    observe.add_argument("--manifest", required=True)
    args = parser.parse_args()
    planner = Planner.from_file(args.config)
    try:
        if args.command == "recommend":
            result = planner.recommend(args.job_class, args.complexity, args.unattended)
        elif args.command == "daily-plan":
            quota_payload = load_json(args.quota) if args.quota else {}
            usage = (
                quota_payload
                if any(key in planner.config.get("cli_pools", {}) for key in quota_payload)
                else planner.normalize_quota_payload(quota_payload)
            )
            request = load_json(args.request)
            if args.cli_capacity:
                capacity_reports = [load_json(path) for path in args.cli_capacity]
                request["cli_health_by_machine"] = planner.normalize_cli_health_by_machine(
                    capacity_reports
                )
            result = planner.plan_day(
                request,
                load_json(args.registry),
                usage,
                load_json_records(args.history),
                now=args.now,
            )
            if args.output:
                output = Path(args.output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        elif args.command == "record-observation":
            observation = load_json(args.observation)
            result = planner.record_observation(
                args.history,
                observation,
                load_json(args.manifest),
            )
            result["history"] = str(Path(args.history))
            result["agent"] = observation.get("agent")
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
