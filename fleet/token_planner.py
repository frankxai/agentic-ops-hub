#!/usr/bin/env python3
"""Starlight Token Planner: model assignment, hard manifest checks, and night UX."""
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

    def command_for(self, mission: dict[str, Any]) -> str:
        task = (
            "HARD RULES: Current branch only. No main push. No force-push. "
            "No git reset --hard. No secrets. Write the required report.\n\n"
            + str(mission["task"])
        )
        quoted = shlex.quote(task)
        agent = mission["agent"]
        timeout = int(mission.get("timeout_minutes", 60))
        if agent == "claude":
            model = shlex.quote(str(mission.get("model", "sonnet")))
            budget = float(mission["budget_usd"])
            budget_text = f"{budget:g}"
            turns = int(mission["max_turns"])
            return (
                f"claude -p {quoted} --model {model} --max-budget-usd {budget_text} "
                f"--max-turns {turns} --permission-mode acceptEdits --output-format json"
            )
        if agent == "codex":
            return f"timeout {timeout}m codex exec --sandbox danger-full-access {quoted}"
        if agent == "opencode":
            return f"timeout {timeout}m opencode run {quoted}"
        if agent == "gemini":
            return f"timeout {timeout}m gemini -p {quoted}"
        raise PlannerError(f"agent {agent!r} has no unattended launcher")

    def status(self, manifest: dict[str, Any]) -> dict[str, Any]:
        rows = []
        complete = 0
        for mission in manifest.get("missions", []):
            report = Path(mission["report"])
            state = "complete" if report.is_file() and report.stat().st_size > 0 else "missing"
            complete += state == "complete"
            rows.append({"id": mission["id"], "agent": mission["agent"], "status": state, "report": str(report)})
        return {"complete": complete, "missing": len(rows) - complete, "missions": rows}

    def debrief(self, manifest: dict[str, Any]) -> str:
        state = self.status(manifest)
        lines = [
            f"# Night debrief — {manifest.get('date', 'unknown')}",
            "",
            f"Budget envelope: ${float(manifest.get('total_budget_usd', 0)):g}",
            f"Missions: {state['complete']} complete · {state['missing']} missing",
            "",
            "| Mission | Agent | Status | Report |",
            "|---------|-------|--------|--------|",
        ]
        for row in state["missions"]:
            lines.append(f"| {row['id']} | {row['agent']} | {row['status']} | `{row['report']}` |")
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
