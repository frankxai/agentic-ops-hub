#!/usr/bin/env python3
"""Safe unattended launcher for validated Starlight night manifests."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fleet.token_planner import Planner, PlannerError, load_json


class RunnerError(RuntimeError):
    pass


@dataclass
class NightRunner:
    planner: Planner
    state_dir: Path
    minimum_free_gb: float = 40.0

    def current_branch(self, repo: str) -> str:
        result = subprocess.run(
            ["git", "-C", repo, "branch", "--show-current"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        if result.returncode:
            raise RunnerError(f"cannot read git branch for {repo}: {result.stderr.strip()}")
        return result.stdout.strip()

    def disk_free_gb(self, path: str) -> float:
        return shutil.disk_usage(path).free / (1024 ** 3)

    def agent_health(self, agent: str) -> dict[str, Any]:
        binary = {"claude": "claude", "codex": "codex", "gemini": "gemini", "opencode": "opencode"}.get(agent)
        if not binary:
            return {"ready": False, "detail": f"unsupported unattended agent: {agent}"}
        resolved = shutil.which(binary)
        if not resolved:
            return {"ready": False, "detail": f"{binary} not found in PATH"}
        if agent == "claude":
            result = subprocess.run(
                [resolved, "-p", "Reply with exactly: pong", "--max-turns", "1", "--output-format", "json"],
                capture_output=True, text=True, timeout=30, check=False,
            )
            try:
                payload = json.loads(result.stdout.splitlines()[0])
            except (json.JSONDecodeError, IndexError):
                return {"ready": False, "detail": (result.stdout or result.stderr).strip()[:300]}
            if payload.get("is_error"):
                return {"ready": False, "detail": str(payload.get("result", "Claude preflight failed"))}
            return {"ready": result.returncode == 0, "detail": "Claude authenticated"}
        result = subprocess.run([resolved, "--version"], capture_output=True, text=True, timeout=15, check=False)
        return {"ready": result.returncode == 0, "detail": (result.stdout or result.stderr).strip()}

    def prepare(self, manifest: dict[str, Any]) -> dict[str, Any]:
        validation = self.planner.validate_manifest(manifest)
        rows = []
        checked_agents: dict[str, dict[str, Any]] = {}
        for mission in manifest["missions"]:
            repo = str(mission["repo"])
            if self.disk_free_gb(repo) < self.minimum_free_gb:
                raise RunnerError(f"disk below {self.minimum_free_gb:g}GB safety gate for {repo}")
            actual = self.current_branch(repo)
            expected = mission["branch"]
            if actual != expected:
                raise RunnerError(f"branch mismatch for {mission['id']}: expected {expected}, got {actual}")
            agent = mission["agent"]
            if agent not in checked_agents:
                checked_agents[agent] = self.agent_health(agent)
            health = checked_agents[agent]
            if not health["ready"]:
                raise RunnerError(f"{agent} preflight failed: {health['detail']}")
            report = Path(mission["report"])
            action = "skip-complete" if report.is_file() and report.stat().st_size else "would-launch"
            rows.append({
                "id": mission["id"], "agent": agent, "action": action,
                "budget_usd": mission["budget_usd"], "branch": expected,
                "command": self.planner.command_for(mission),
            })
        return {"ready": True, "validation": validation, "agents": checked_agents, "missions": rows}

    def launch(self, manifest: dict[str, Any]) -> dict[str, Any]:
        self.prepare(manifest)
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.state_dir / run_id
        logs = run_dir / "logs"
        logs.mkdir(parents=True, exist_ok=False)
        launched = []
        for mission in manifest["missions"]:
            report = Path(mission["report"])
            if report.is_file() and report.stat().st_size:
                launched.append({"id": mission["id"], "status": "skipped-complete", "report": str(report)})
                continue
            command = self.planner.command_for(mission)
            log_path = logs / f"{mission['id']}.log"
            log_handle = log_path.open("w", encoding="utf-8")
            try:
                process = subprocess.Popen(
                    ["bash", "-lc", command], cwd=mission["repo"],
                    stdout=log_handle, stderr=subprocess.STDOUT,
                    creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
                    start_new_session=os.name != "nt",
                )
            finally:
                log_handle.close()
            launched.append({
                "id": mission["id"], "agent": mission["agent"], "pid": process.pid,
                "status": "running", "budget_usd": mission["budget_usd"],
                "log": str(log_path), "report": str(report),
            })
        state = {
            "run_id": run_id, "started_at": datetime.now(timezone.utc).isoformat(),
            "declared_budget_usd": manifest["total_budget_usd"], "missions": launched,
        }
        state_path = run_dir / "state.json"
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        return {"run_id": run_id, "state_file": str(state_path), "missions": launched}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Starlight night manifest")
    parser.add_argument("manifest")
    parser.add_argument("--execute", action="store_true", help="launch after all safety checks")
    parser.add_argument("--config", default=str(Path(__file__).with_name("model-routing.json")))
    parser.add_argument("--state-dir", default=str(Path(__file__).with_name("runs")))
    args = parser.parse_args()
    runner = NightRunner(Planner.from_file(args.config), Path(args.state_dir))
    try:
        manifest = load_json(args.manifest)
        result = runner.launch(manifest) if args.execute else runner.prepare(manifest)
        print(json.dumps(result, indent=2))
        return 0
    except (PlannerError, RunnerError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ready": False, "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
