#!/usr/bin/env python3
"""Starlight Token Planner: outcome routing, manifest checks, and night UX."""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import urlparse


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


def _repo_path(mission: dict[str, Any], value: str) -> Path:
    if mission.get("objective_id"):
        return _portable_repo_path(str(mission["repo"]), value, f"mission {mission['id']}")
    path = Path(value)
    return path if path.is_absolute() else Path(mission["repo"]) / path


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

    def quota_health(self, agent: str, usage: dict[str, Any]) -> tuple[bool, str]:
        gate = self.config.get("subscription_gates", {}).get(agent)
        if not gate or gate.get("mode") == "unmetered":
            return True, "quota gate not required"
        record = usage.get(agent)
        if not record:
            if gate.get("allow_unmeasured", False):
                return True, "quota is not measured"
            return False, f"{agent} quota is unavailable"
        remaining = float(record.get("remaining_percent", 0))
        floor = float(gate.get("minimum_remaining_percent", 0))
        if remaining < floor:
            return False, f"{agent} quota has {remaining:g}% remaining below {floor:g}% floor"
        return True, f"{agent} quota has {remaining:g}% remaining"

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
        declared = float(manifest.get("total_budget_usd", 0))
        cap = float(self.config["night_cap_usd"])
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
        wave_totals: dict[int, float] = {}
        for mission in missions:
            mission_id = str(mission.get("id", ""))
            if not mission_id or mission_id in ids:
                raise PlannerError("mission ids must be non-empty and unique")
            ids.add(mission_id)
            mission_by_id[mission_id] = mission
            branch = str(mission.get("branch", ""))
            allowed_prefixes = ("night/",) if mode == "night" else ("night/", "agent/")
            if not branch.startswith(allowed_prefixes):
                raise PlannerError(
                    f"mission {mission_id} branch must start with {' or '.join(allowed_prefixes)}"
                )
            for key in ("agent", "repo", "task", "report"):
                if not mission.get(key):
                    raise PlannerError(f"mission {mission_id} missing {key}")
            task = str(mission["task"])
            for pattern, label in _PROHIBITED_TASK_PATTERNS.items():
                if re.search(pattern, task, flags=re.IGNORECASE):
                    raise PlannerError(f"mission {mission_id} task contains prohibited operation: {label}")
            if version >= 2:
                if not mission.get("receipt"):
                    raise PlannerError(f"mission {mission_id} missing receipt")
                checks = mission.get("acceptance_commands")
                if not isinstance(checks, list) or not checks:
                    raise PlannerError(f"mission {mission_id} requires acceptance_commands")
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
                for key in ("outcome", "receipt", "role", "quota_pool"):
                    if not mission.get(key):
                        raise PlannerError(f"mission {mission_id} missing {key}")
                role = str(mission["role"])
                if role not in {"maker", "verifier", "integrator", "researcher"}:
                    raise PlannerError(f"mission {mission_id} has unsupported role")
                if mission["quota_pool"] != mission["agent"]:
                    raise PlannerError(f"mission {mission_id} quota_pool must match agent")
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
            budget = float(mission.get("budget_usd", 0))
            if budget < 0:
                raise PlannerError(f"mission {mission_id} budget cannot be negative")
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
            for wave_number, spent in wave_totals.items():
                cap_value = declared_wave_budgets.get(str(wave_number))
                if cap_value is None:
                    raise PlannerError(f"campaign wave {wave_number} has no budget")
                if spent > float(cap_value):
                    raise PlannerError(
                        f"campaign wave {wave_number} missions ${spent:g} exceed wave budget "
                        f"${float(cap_value):g}"
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
            contract += ["", "ACCEPTANCE COMMANDS (run and record exact exit codes):"]
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
        receipt = _repo_path(mission, str(receipt_value))
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
        if mission.get("objective_id"):
            if payload.get("schema_version") != 1:
                return "invalid-receipt", "schema_version must be 1"
            if payload.get("objective_id") != mission.get("objective_id"):
                return "invalid-receipt", "objective_id mismatch"
            if payload.get("role") != mission.get("role"):
                return "invalid-receipt", "role mismatch"
            outcome = str(payload.get("outcome_status", "FAILED")).upper()
            if outcome in {"HOLD", "BLOCKED", "FAILED"}:
                return outcome.lower(), f"outcome_status={outcome}"
            receipt_agent = str(payload.get("agent", ""))
            if receipt_agent != str(mission["agent"]):
                return "invalid-receipt", "verified receipt agent does not match the committed manifest route"
            if payload.get("execution_status") != "ok" or outcome != "VERIFIED":
                return "unverified", "execution or outcome status is not verified"
        if payload.get("status") not in {"verified", "delivered"}:
            return "unverified", "status is not verified/delivered"
        commit = str(payload.get("commit", ""))
        if not commit:
            return "unverified", "commit missing"
        if mission.get("objective_id"):
            commit_valid, commit_detail = self._commit_state(mission, commit)
            if not commit_valid:
                return "invalid-receipt", commit_detail
        checks = payload.get("verification")
        if not isinstance(checks, list) or not checks:
            return "unverified", "verification missing"
        if any(int(check.get("exit_code", 1)) != 0 for check in checks):
            return "failed-verification", "acceptance command failed"
        if mission.get("objective_id"):
            declared_artifacts = {str(item) for item in payload.get("artifacts", [])}
            for artifact in mission["required_artifacts"]:
                if artifact not in declared_artifacts:
                    return "unverified", f"receipt missing artifact: {artifact}"
                resolved = _repo_path(mission, str(artifact))
                if not resolved.is_file() or resolved.stat().st_size == 0:
                    return "unverified", f"artifact missing: {artifact}"
                matches_commit, artifact_detail = self._artifact_commit_state(
                    mission, commit, str(artifact)
                )
                if not matches_commit:
                    return "invalid-receipt", artifact_detail
            expected_checks = dict(
                zip(mission["verification_ids"], mission["acceptance_commands"], strict=True)
            )
            recorded_checks: dict[str, str] = {}
            for check in checks:
                check_id = str(check.get("id", ""))
                command = str(check.get("command", ""))
                if check_id in recorded_checks:
                    return "invalid-receipt", f"duplicate verification id: {check_id}"
                if expected_checks.get(check_id) != command:
                    return "invalid-receipt", f"verification command mismatch: {check_id}"
                if check.get("status") != "passed" or int(check.get("exit_code", 1)) != 0:
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
        if not payload.get("completed_at"):
            return "unverified", "completed_at missing"
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
