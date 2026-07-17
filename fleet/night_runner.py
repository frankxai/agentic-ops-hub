#!/usr/bin/env python3
"""Safety-gated unattended launcher for version-2 Starlight night manifests."""
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
    minimum_free_gb: float = 50.0
    maximum_memory_percent: float = 85.0

    def current_branch(self, repo: str) -> str:
        result = subprocess.run(
            ["git", "-C", repo, "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode:
            raise RunnerError(f"cannot read git branch for {repo}: {result.stderr.strip()}")
        return result.stdout.strip()

    def is_clean(self, repo: str) -> bool:
        result = subprocess.run(
            ["git", "-C", repo, "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode:
            raise RunnerError(f"cannot read git status for {repo}: {result.stderr.strip()}")
        return not result.stdout.strip()

    def disk_free_gb(self, path: str) -> float:
        return shutil.disk_usage(path).free / (1024**3)

    def subscription_usage(self) -> dict[str, Any]:
        binary = shutil.which("tokscale")
        if not binary:
            return {}
        result = subprocess.run(
            [binary, "usage", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode:
            return {}
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}
        providers = payload if isinstance(payload, list) else payload.get("providers", [])
        provider_map = self.planner.config.get("quota_providers", {})
        usage = {}
        for provider in providers:
            label = str(provider.get("provider") or provider.get("label", ""))
            agent = provider_map.get(label)
            if not agent:
                continue
            remaining = [
                float(metric["remaining_percent"])
                for metric in provider.get("metrics", [])
                if metric.get("remaining_percent") is not None
            ]
            if remaining:
                usage[agent] = {
                    "provider": label,
                    "plan": provider.get("plan", "unknown"),
                    "remaining_percent": min(remaining),
                }
        return usage

    def memory_percent(self) -> float:
        try:
            import psutil  # type: ignore

            return float(psutil.virtual_memory().percent)
        except ImportError:
            if os.name == "nt":
                import ctypes

                class MemoryStatus(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]

                status = MemoryStatus()
                status.dwLength = ctypes.sizeof(status)
                if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                    raise RunnerError("cannot read Windows memory pressure")
                return float(status.dwMemoryLoad)
            pages = os.sysconf("SC_PHYS_PAGES")
            available = os.sysconf("SC_AVPHYS_PAGES")
            return 100.0 * (1.0 - available / pages)

    def enforce_resources(self, repo: str) -> None:
        free = self.disk_free_gb(repo)
        if free < self.minimum_free_gb:
            raise RunnerError(f"disk below {self.minimum_free_gb:g}GB safety gate for {repo}: {free:.1f}GB")
        memory = self.memory_percent()
        if memory > self.maximum_memory_percent:
            raise RunnerError(
                f"RAM pressure {memory:.1f}% exceeds {self.maximum_memory_percent:g}% hard gate"
            )

    def agent_health(self, mission: dict[str, Any]) -> dict[str, Any]:
        agent = str(mission["agent"])
        binary = {
            "claude": "claude",
            "codex": "codex",
            "gemini": "gemini",
            "agy": "agy",
            "opencode": "opencode",
        }.get(agent)
        if not binary:
            return {"ready": False, "detail": f"unsupported unattended agent: {agent}"}
        resolved = shutil.which(binary)
        if not resolved:
            return {"ready": False, "detail": f"{binary} not found in PATH"}
        if agent == "claude":
            command = [
                resolved,
                "-p",
                "Reply with exactly: PONG",
                "--model",
                str(mission.get("model", "sonnet")),
                "--max-turns",
                "1",
                "--output-format",
                "json",
            ]
        elif agent == "codex":
            command = [
                resolved,
                "exec",
                "-C",
                str(mission["repo"]),
                "--sandbox",
                "read-only",
                "-m",
                str(mission.get("model", "gpt-5.6-terra")),
                "-c",
                "model_reasoning_effort=low",
                "Reply exactly PONG. Do not inspect or modify files.",
            ]
        elif agent in {"gemini", "agy"}:
            command = [resolved, "-p", "Reply exactly PONG."]
        else:
            auth = subprocess.run(
                [resolved, "auth", "list"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            detail = (auth.stdout or auth.stderr).strip()[:500]
            ready = auth.returncode == 0 and "0 credentials" not in detail.lower()
            return {"ready": ready, "detail": detail or "OpenCode auth not verified"}
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        detail = (result.stdout or result.stderr).strip()[:1000]
        if agent == "claude":
            try:
                payload = json.loads(result.stdout.splitlines()[0])
            except (json.JSONDecodeError, IndexError):
                return {"ready": False, "detail": detail}
            if payload.get("is_error"):
                return {"ready": False, "detail": str(payload.get("result", "Claude preflight failed"))}
        ready = result.returncode == 0 and "PONG" in (result.stdout + result.stderr).upper()
        return {"ready": ready, "detail": detail}

    def _route_mission(
        self,
        mission: dict[str, Any],
        usage: dict[str, Any],
        excluded_agents: set[str],
        health_cache: dict[tuple[str, str, str], dict[str, Any]],
    ) -> tuple[dict[str, Any], str, dict[str, Any]]:
        preferred = str(mission["agent"])
        candidates = [preferred, *self.planner.config.get("fallbacks", {}).get(preferred, [])]
        failures = []
        for candidate in candidates:
            if candidate in excluded_agents:
                failures.append(f"{candidate}: reserved for maker/checker separation")
                continue
            routed = dict(mission)
            if candidate != preferred:
                defaults = self.planner.config.get("agent_defaults", {}).get(candidate)
                if not defaults:
                    failures.append(f"{candidate}: no launcher defaults")
                    continue
                routed.update({key: value for key, value in defaults.items() if key != "budget_usd"})
                routed["agent"] = candidate
                routed["quota_pool"] = candidate
                routed["routed_from"] = preferred
            quota_ready, quota_detail = self.planner.quota_health(candidate, usage)
            if not quota_ready:
                failures.append(f"{candidate}: {quota_detail}")
                continue
            key = (candidate, str(routed.get("model", "")), str(routed["repo"]))
            if key not in health_cache:
                health_cache[key] = self.agent_health(routed)
            health = health_cache[key]
            if health["ready"]:
                return routed, quota_detail, health
            failures.append(f"{candidate}: {health['detail']}")
        raise RunnerError(
            f"no healthy route for {mission['id']} ({preferred}): {'; '.join(failures)}"
        )

    def prepare(self, manifest: dict[str, Any]) -> dict[str, Any]:
        if int(manifest.get("version", 1)) < 2:
            raise RunnerError("runner requires manifest version 2 with acceptance commands and receipts")
        validation = self.planner.validate_manifest(manifest)
        rows = []
        checked_agents: dict[tuple[str, str, str], dict[str, Any]] = {}
        usage = self.subscription_usage()
        campaign_status = self.planner.status(manifest)
        status_by_id = {row["id"]: row["status"] for row in campaign_status["missions"]}
        active_wave = self.planner.active_wave(manifest)
        for mission in manifest["missions"]:
            state = status_by_id[mission["id"]]
            if state in {"verified", "delivered"}:
                rows.append({
                    "id": mission["id"],
                    "agent": mission["agent"],
                    "action": "skip-verified",
                    "receipt": mission["receipt"],
                })
                continue
            if state in {"hold", "blocked", "failed", "failed-verification", "invalid-receipt"}:
                rows.append({
                    "id": mission["id"],
                    "agent": mission["agent"],
                    "action": "skip-terminal",
                    "receipt_status": state,
                })
                continue
            dependency_state = self.planner.dependency_state(mission, status_by_id)
            if dependency_state != "ready":
                rows.append({
                    "id": mission["id"],
                    "agent": mission["agent"],
                    "action": "blocked-upstream" if dependency_state == "blocked" else "queued-dependency",
                    "dependencies": mission.get("depends_on", []),
                })
                continue
            if manifest.get("mode") == "campaign" and int(mission["wave"]) != active_wave:
                rows.append({
                    "id": mission["id"],
                    "agent": mission["agent"],
                    "action": "queued-wave",
                    "wave": mission["wave"],
                })
                continue
            repo = str(mission["repo"])
            self.enforce_resources(repo)
            actual = self.current_branch(repo)
            expected = str(mission["branch"])
            if actual != expected:
                raise RunnerError(f"branch mismatch for {mission['id']}: expected {expected}, got {actual}")
            if not self.is_clean(repo):
                raise RunnerError(f"mission {mission['id']} repo is dirty; use a clean dedicated worktree")
            excluded_agents: set[str] = set()
            if mission.get("role") == "verifier":
                for other in manifest["missions"]:
                    if (
                        other.get("objective_id") == mission.get("objective_id")
                        and other.get("role") == "maker"
                    ):
                        excluded_agents.add(
                            self.planner.recorded_agent(other) or str(other["agent"])
                        )
            routed, quota_detail, health = self._route_mission(
                mission, usage, excluded_agents, checked_agents
            )
            argv = self.planner.command_args(routed)
            rows.append(
                {
                    "id": mission["id"],
                    "agent": routed["agent"],
                    "requested_agent": mission["agent"],
                    "action": "would-launch",
                    "budget_usd": mission["budget_usd"],
                    "branch": expected,
                    "wave": mission.get("wave"),
                    "quota": quota_detail,
                    "health": health,
                    "command": self.planner.command_for(routed),
                    "argv": argv,
                }
            )
        agents = {"|".join(key): value for key, value in checked_agents.items()}
        return {
            "ready": True,
            "validation": validation,
            "active_wave": active_wave,
            "subscription_usage": usage,
            "agents": agents,
            "missions": rows,
        }

    def _write_state(self, path: Path, state: dict[str, Any]) -> None:
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def launch(self, manifest: dict[str, Any]) -> dict[str, Any]:
        prepared = self.prepare(manifest)
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.state_dir / run_id
        logs = run_dir / "logs"
        logs.mkdir(parents=True, exist_ok=False)
        state_path = run_dir / "state.json"
        state: dict[str, Any] = {
            "run_id": run_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "declared_budget_usd": manifest["total_budget_usd"],
            "mode": "sequential-bounded",
            "active_wave": prepared.get("active_wave"),
            "subscription_usage": prepared.get("subscription_usage", {}),
            "missions": [],
        }
        self._write_state(state_path, state)

        for mission, row in zip(manifest["missions"], prepared["missions"], strict=True):
            if row["action"] in {
                "skip-verified",
                "skip-terminal",
                "queued-wave",
                "queued-dependency",
                "blocked-upstream",
            }:
                state["missions"].append(
                    {
                        "id": mission["id"],
                        "status": row["action"],
                        "receipt": mission.get("receipt"),
                    }
                )
                self._write_state(state_path, state)
                continue
            try:
                self.enforce_resources(str(mission["repo"]))
            except RunnerError as exc:
                state["missions"].append({"id": mission["id"], "status": "blocked-resource", "error": str(exc)})
                self._write_state(state_path, state)
                break
            log_path = logs / f"{mission['id']}.log"
            started = datetime.now(timezone.utc).isoformat()
            try:
                with log_path.open("w", encoding="utf-8") as log_handle:
                    result = subprocess.run(
                        row["argv"],
                        cwd=str(mission["repo"]),
                        stdout=log_handle,
                        stderr=subprocess.STDOUT,
                        timeout=int(mission.get("timeout_minutes", 60)) * 60,
                        check=False,
                    )
                exit_code = result.returncode
                run_status = "exited" if exit_code == 0 else "failed-exit"
            except subprocess.TimeoutExpired:
                exit_code = 124
                run_status = "timeout"
            effective_mission = dict(mission)
            effective_mission["agent"] = row["agent"]
            effective_mission["quota_pool"] = row["agent"]
            receipt_state = self.planner.status(
                {"missions": [effective_mission]}
            )["missions"][0]
            recorded_agent = self.planner.recorded_agent(mission)
            if recorded_agent and recorded_agent != row["agent"]:
                receipt_state = {
                    **receipt_state,
                    "status": "invalid-receipt",
                    "detail": "receipt agent does not match effective runtime route",
                }
            if run_status == "exited" and receipt_state["status"] not in {"verified", "delivered"}:
                run_status = "failed-unverified"
            state["missions"].append(
                {
                    "id": mission["id"],
                    "agent": row["agent"],
                    "requested_agent": mission["agent"],
                    "status": run_status,
                    "exit_code": exit_code,
                    "started_at": started,
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "log": str(log_path),
                    "report": str(mission["report"]),
                    "receipt": str(mission["receipt"]),
                    "receipt_status": receipt_state["status"],
                }
            )
            self._write_state(state_path, state)
            if run_status not in {"exited"}:
                break
        state["finished_at"] = datetime.now(timezone.utc).isoformat()
        self._write_state(state_path, state)
        return {"run_id": run_id, "state_file": str(state_path), "missions": state["missions"]}


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
