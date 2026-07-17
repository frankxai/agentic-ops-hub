#!/usr/bin/env python3
"""Safe unattended launcher for validated Starlight night manifests."""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from fleet.token_planner import Planner, PlannerError, load_json


class RunnerError(RuntimeError):
    pass


DEFAULT_QUEUE_PATH = "fleet/bus/queues/to-c940.json"
QueueLoader = Callable[[], dict[str, Any]]


def load_origin_main_queue(
    repo_root: str | Path,
    relative_path: str = DEFAULT_QUEUE_PATH,
) -> dict[str, Any]:
    """Fetch origin/main and read the durable queue without checkout/reset."""
    root = Path(repo_root)
    fetch = subprocess.run(
        ["git", "-C", str(root), "fetch", "origin", "main", "--quiet"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if fetch.returncode:
        raise RunnerError(f"git fetch origin main failed: {(fetch.stderr or fetch.stdout).strip()}")
    shown = subprocess.run(
        ["git", "-C", str(root), "show", f"origin/main:{relative_path}"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if shown.returncode:
        raise RunnerError(
            f"cannot read origin/main:{relative_path}: {(shown.stderr or shown.stdout).strip()}"
        )
    try:
        data = json.loads(shown.stdout)
    except json.JSONDecodeError as exc:
        raise RunnerError(f"invalid queue JSON at origin/main:{relative_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError("queue payload must be a JSON object")
    data = dict(data)
    data["source_ref"] = f"origin/main:{relative_path}"
    return data


@dataclass
class NightRunner:
    planner: Planner
    state_dir: Path
    minimum_free_gb: float = 50.0
    maximum_ram_percent: float = 90.0
    minimum_available_ram_gb: float = 2.0
    max_concurrent_missions: int = 1
    queue_loader: QueueLoader | None = None
    queue_repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])

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

    def disk_free_gb(self, path: str) -> float:
        return shutil.disk_usage(path).free / (1024 ** 3)

    def ram_health(self) -> dict[str, Any]:
        """Return a fail-closed RAM gate without requiring a project dependency."""
        try:
            import psutil  # type: ignore

            memory = psutil.virtual_memory()
            percent = float(memory.percent)
            available_gb = float(memory.available) / (1024 ** 3)
        except ImportError:
            if os.name != "nt":
                return {"ready": False, "percent": 100.0, "available_gb": 0.0, "detail": "RAM probe unavailable"}

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("length", ctypes.c_ulong),
                    ("memory_load", ctypes.c_ulong),
                    ("total_phys", ctypes.c_ulonglong),
                    ("avail_phys", ctypes.c_ulonglong),
                    ("total_page_file", ctypes.c_ulonglong),
                    ("avail_page_file", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong),
                    ("avail_virtual", ctypes.c_ulonglong),
                    ("avail_extended_virtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.length = ctypes.sizeof(MemoryStatus)
            if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return {"ready": False, "percent": 100.0, "available_gb": 0.0, "detail": "RAM probe failed"}
            percent = float(status.memory_load)
            available_gb = float(status.avail_phys) / (1024 ** 3)

        ready = percent <= self.maximum_ram_percent and available_gb >= self.minimum_available_ram_gb
        return {
            "ready": ready,
            "percent": round(percent, 1),
            "available_gb": round(available_gb, 2),
            "detail": (
                "RAM healthy"
                if ready
                else f"RAM pressure {percent:.1f}% used, {available_gb:.2f}GiB available"
            ),
        }

    def is_linked_worktree(self, repo: str) -> bool:
        """A linked worktree has a .git pointer file, unlike a primary checkout."""
        root = Path(repo)
        if not root.is_dir() or not (root / ".git").is_file():
            return False
        result = subprocess.run(
            ["git", "-C", repo, "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"

    def load_queue(self) -> dict[str, Any]:
        if self.queue_loader is not None:
            data = self.queue_loader()
            if not isinstance(data, dict):
                raise RunnerError("queue_loader must return a dict")
            return data
        return load_origin_main_queue(self.queue_repo_root)

    def ensure_queue_item(self, mission: dict[str, Any], queue: dict[str, Any]) -> dict[str, Any]:
        queue_item_id = str(mission.get("queue_item_id") or "").strip()
        if not queue_item_id:
            raise RunnerError(f"mission {mission.get('id')} missing queue_item_id")

        target = str(queue.get("to") or "").lower()
        if target and target not in {"c940", "all"}:
            raise RunnerError(f"queue target {target!r} is not c940")

        claimed_by = str(queue.get("claimed_by") or "").lower()
        if claimed_by and claimed_by not in {"c940", "command-center", "none", "unclaimed"}:
            raise RunnerError(f"queue claimed by peer {claimed_by!r}; refusing mission {mission.get('id')}")

        results = queue.get("results") or {}
        if not isinstance(results, dict):
            raise RunnerError("queue results must be an object")
        prior = results.get(queue_item_id)
        if prior is not None and str(prior).strip():
            raise RunnerError(f"queue item {queue_item_id} already complete: {prior}")

        items = queue.get("items") or []
        if not isinstance(items, list):
            raise RunnerError("queue items must be a list")
        match = next((item for item in items if str(item.get("id")) == queue_item_id), None)
        if match is None:
            raise RunnerError(f"queue item {queue_item_id} not present in origin/main C940 queue")
        return match

    def agent_health(self, agent: str) -> dict[str, Any]:
        binary = {
            "claude": "claude",
            "codex": "codex",
            "gemini": "gemini",
            "opencode": "opencode",
        }.get(agent)
        if not binary:
            return {"ready": False, "detail": f"unsupported unattended agent: {agent}"}
        resolved = shutil.which(binary)
        if not resolved:
            return {"ready": False, "detail": f"{binary} not found in PATH"}

        if agent == "claude":
            result = subprocess.run(
                [resolved, "-p", "Reply with exactly: pong", "--max-turns", "1", "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            try:
                payload = json.loads(result.stdout.splitlines()[0])
            except (json.JSONDecodeError, IndexError):
                return {"ready": False, "detail": (result.stdout or result.stderr).strip()[:300]}
            if payload.get("is_error"):
                return {"ready": False, "detail": str(payload.get("result", "Claude preflight failed"))}
            return {"ready": result.returncode == 0, "detail": "Claude authenticated"}

        if agent == "codex":
            with tempfile.TemporaryDirectory(prefix="starlight-codex-preflight-") as tmp:
                result = subprocess.run(
                    [
                        resolved,
                        "exec",
                        "--sandbox",
                        "read-only",
                        "--ephemeral",
                        "--skip-git-repo-check",
                        "Reply with exactly: pong",
                    ],
                    cwd=tmp,
                    capture_output=True,
                    text=True,
                    timeout=45,
                    check=False,
                )
            output = (result.stdout or result.stderr).strip()
            ready = result.returncode == 0 and "pong" in output.lower()
            return {"ready": ready, "detail": "Codex authenticated read-only probe" if ready else output[:300]}

        result = subprocess.run(
            [resolved, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return {"ready": result.returncode == 0, "detail": (result.stdout or result.stderr).strip()}

    @staticmethod
    def budget_enforcement(agent: str) -> str:
        return "hard-cli" if agent == "claude" else "advisory-timeout"

    def prepare(self, manifest: dict[str, Any]) -> dict[str, Any]:
        validation = self.planner.validate_manifest(manifest)
        ram = self.ram_health()
        if not ram["ready"]:
            raise RunnerError(f"RAM safety gate failed: {ram['detail']}")

        queue = self.load_queue()
        status_rows = {row["id"]: row for row in self.planner.status(manifest)["missions"]}
        pending = [mission for mission in manifest["missions"] if status_rows[mission["id"]]["status"] != "complete"]
        if len(pending) > self.max_concurrent_missions:
            raise RunnerError(
                f"only one pending mission may launch at a time; found {len(pending)}. "
                "Split the manifest or verify earlier receipts first"
            )

        rows = []
        checked_agents: dict[str, dict[str, Any]] = {}
        for mission in manifest["missions"]:
            receipt_status = status_rows[mission["id"]]["status"]
            if receipt_status == "complete":
                rows.append(
                    {
                        "id": mission["id"],
                        "queue_item_id": mission.get("queue_item_id"),
                        "agent": mission["agent"],
                        "action": "skip-complete",
                        "budget_usd": mission["budget_usd"],
                        "budget_enforcement": self.budget_enforcement(mission["agent"]),
                        "branch": mission["branch"],
                    }
                )
                continue

            queue_item = self.ensure_queue_item(mission, queue)
            repo = str(mission["repo"])
            if self.disk_free_gb(repo) < self.minimum_free_gb:
                raise RunnerError(f"disk below {self.minimum_free_gb:g}GiB safety gate for {repo}")
            if not self.is_linked_worktree(repo):
                raise RunnerError(f"mission {mission['id']} must run in a linked worktree: {repo}")
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
            rows.append(
                {
                    "id": mission["id"],
                    "queue_item_id": mission.get("queue_item_id"),
                    "queue_title": queue_item.get("title"),
                    "queue_source": queue.get("source_ref", "origin/main"),
                    "agent": agent,
                    "action": "would-launch",
                    "receipt_status": receipt_status,
                    "budget_usd": mission["budget_usd"],
                    "budget_enforcement": self.budget_enforcement(agent),
                    "branch": expected,
                    "command": self.planner.command_for(mission),
                }
            )
        return {
            "ready": True,
            "validation": validation,
            "resources": {"ram": ram, "minimum_free_disk_gb": self.minimum_free_gb},
            "queue_source": queue.get("source_ref", "origin/main"),
            "agents": checked_agents,
            "missions": rows,
        }

    def launch(self, manifest: dict[str, Any]) -> dict[str, Any]:
        prepared = self.prepare(manifest)
        action_by_id = {row["id"]: row for row in prepared.get("missions", [])}
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.state_dir / run_id
        logs = run_dir / "logs"
        logs.mkdir(parents=True, exist_ok=False)
        launched = []
        for mission in manifest["missions"]:
            prepared_row = action_by_id.get(mission["id"], {})
            report = Path(mission["report"])
            if prepared_row.get("action") == "skip-complete":
                launched.append(
                    {
                        "id": mission["id"],
                        "queue_item_id": mission.get("queue_item_id"),
                        "status": "skipped-complete",
                        "report": str(report),
                    }
                )
                continue
            command = self.planner.command_for(mission)
            log_path = logs / f"{mission['id']}.log"
            log_handle = log_path.open("w", encoding="utf-8")
            try:
                process = subprocess.Popen(
                    ["bash", "-lc", command],
                    cwd=mission["repo"],
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
                    start_new_session=os.name != "nt",
                )
            finally:
                log_handle.close()
            launched.append(
                {
                    "id": mission["id"],
                    "queue_item_id": mission.get("queue_item_id"),
                    "agent": mission["agent"],
                    "pid": process.pid,
                    "status": "running",
                    "budget_usd": mission["budget_usd"],
                    "budget_enforcement": self.budget_enforcement(mission["agent"]),
                    "log": str(log_path),
                    "report": str(report),
                }
            )
        state = {
            "run_id": run_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "declared_budget_usd": manifest["total_budget_usd"],
            "queue_source": prepared.get("queue_source"),
            "missions": launched,
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
    defaults = Planner.from_file(args.config)
    gates = defaults.config.get("defaults", {})
    runner = NightRunner(
        defaults,
        Path(args.state_dir),
        minimum_free_gb=float(gates.get("minimum_free_disk_gb", 50)),
        maximum_ram_percent=float(gates.get("maximum_ram_percent", 90)),
        minimum_available_ram_gb=float(gates.get("minimum_available_ram_gb", 2)),
        max_concurrent_missions=int(gates.get("max_concurrent_missions", 1)),
    )
    try:
        manifest = load_json(args.manifest)
        result = runner.launch(manifest) if args.execute else runner.prepare(manifest)
        print(json.dumps(result, indent=2))
        return 0
    except (PlannerError, RunnerError, OSError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"ready": False, "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
