#!/usr/bin/env python3
"""Starlight Token Planner: outcome routing, manifest checks, and night UX."""
from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
