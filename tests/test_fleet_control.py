from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fleet.night_runner import NightRunner, RunnerError
from fleet.token_planner import Planner
from scripts import fleet_bus


class PlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.planner = Planner(
            {
                "night_cap_usd": 110,
                "routes": {},
                "fallbacks": {},
            }
        )

    def mission(self, root: Path) -> dict:
        return {
            "id": "N1",
            "agent": "codex",
            "model": "gpt-5.6-terra",
            "reasoning_effort": "high",
            "repo": str(root),
            "branch": "night/2026-07-17-test",
            "budget_usd": 30,
            "timeout_minutes": 45,
            "task": "Implement the named outcome.",
            "report": str(root / "report.md"),
            "receipt": str(root / "receipt.json"),
            "acceptance_commands": ["python -m unittest discover -v"],
        }

    def test_codex_command_is_repo_scoped_and_never_widens_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            command = self.planner.command_for(self.mission(Path(tmp)))
        self.assertIn("--sandbox workspace-write", command)
        self.assertIn("-C", command)
        self.assertIn("gpt-5.6-terra", command)
        self.assertIn("model_reasoning_effort=high", command)
        self.assertNotIn("danger-full-access", command)
        self.assertNotIn("--yolo", command)

    def test_nonempty_report_is_not_completion_without_verified_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission = self.mission(root)
            Path(mission["report"]).write_text("looks done", encoding="utf-8")
            status = self.planner.status({"missions": [mission]})
        self.assertEqual(0, status["complete"])
        self.assertEqual("missing-receipt", status["missions"][0]["status"])

    def test_verified_receipt_requires_commit_tests_and_integration_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission = self.mission(root)
            Path(mission["receipt"]).write_text(
                json.dumps(
                    {
                        "mission_id": "N1",
                        "status": "verified",
                        "branch": mission["branch"],
                        "commit": "abc1234",
                        "verification": [{"command": "python -m unittest discover -v", "exit_code": 0}],
                        "integration_state": "pr_open",
                        "completed_at": "2026-07-17T13:00:00+00:00",
                    }
                ),
                encoding="utf-8",
            )
            status = self.planner.status({"missions": [mission]})
        self.assertEqual(1, status["complete"])
        self.assertEqual("verified", status["missions"][0]["status"])


class NightRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.planner = Planner({"night_cap_usd": 110, "routes": {}, "fallbacks": {}})

    def manifest(self, repo: Path) -> dict:
        mission = PlannerTests.mission(self, repo)
        return {
            "version": 2,
            "mode": "night",
            "total_budget_usd": 30,
            "missions": [mission],
        }

    def test_prepare_blocks_when_ram_is_above_hard_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runner = NightRunner(self.planner, root / "runs")
            with (
                patch.object(runner, "disk_free_gb", return_value=100),
                patch.object(runner, "memory_percent", return_value=91),
                patch.object(runner, "current_branch", return_value="night/2026-07-17-test"),
                patch.object(runner, "is_clean", return_value=True),
            ):
                with self.assertRaisesRegex(RunnerError, "RAM"):
                    runner.prepare(self.manifest(root))

    def test_prepare_live_preflight_is_mission_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runner = NightRunner(self.planner, root / "runs")
            with (
                patch.object(runner, "disk_free_gb", return_value=100),
                patch.object(runner, "memory_percent", return_value=40),
                patch.object(runner, "current_branch", return_value="night/2026-07-17-test"),
                patch.object(runner, "is_clean", return_value=True),
                patch.object(runner, "agent_health", return_value={"ready": True, "detail": "PONG"}) as health,
            ):
                result = runner.prepare(self.manifest(root))
            health.assert_called_once()
            self.assertEqual("would-launch", result["missions"][0]["action"])


class FleetBusTests(unittest.TestCase):
    def test_remote_newer_heartbeat_overrides_stale_local_copy(self) -> None:
        local = {
            "yoga-book": {
                "machine_id": "yoga-book",
                "status": "live",
                "at": "2026-07-16T18:00:00+00:00",
            }
        }
        remote = {
            "yoga-book": {
                "machine_id": "yoga-book",
                "status": "live",
                "at": "2026-07-17T03:41:53+00:00",
            }
        }
        merged = fleet_bus.reconcile_heartbeats(local, remote)
        self.assertEqual("remote", merged["yoga-book"]["source"])
        self.assertTrue(fleet_bus.peer_is_fresh(merged["yoga-book"], max_age_hours=24, now="2026-07-17T13:00:00+00:00"))


if __name__ == "__main__":
    unittest.main()
