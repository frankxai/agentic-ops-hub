import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fleet.night_runner import NightRunner, RunnerError
from fleet.token_planner import Planner


class NightRunnerTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.planner = Planner.from_file(root / "fleet" / "model-routing.json")

    @staticmethod
    def _queue():
        return {
            "to": "c940",
            "status": "active",
            "claimed_by": "c940",
            "items": [{"id": "B1", "title": "test mission"}],
            "results": {},
            "source_ref": "origin/main",
        }

    def healthy_resources(self, runner):
        return (
            patch.object(runner, "disk_free_gb", return_value=80.0),
            patch.object(
                runner,
                "ram_health",
                return_value={"ready": True, "percent": 50.0, "available_gb": 8.0},
            ),
            patch.object(runner, "is_linked_worktree", return_value=True),
        )

    def test_prepare_is_dry_run_and_writes_no_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._manifest(tmp)
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            disk, ram, worktree = self.healthy_resources(runner)
            with disk, ram, worktree, \
                 patch.object(runner, "current_branch", return_value="night/2026-07-17-test"), \
                 patch.object(runner, "agent_health", return_value={"ready": True, "detail": "codex test"}):
                result = runner.prepare(manifest)
            self.assertTrue(result["ready"])
            self.assertFalse((Path(tmp) / "state").exists())
            self.assertEqual(result["missions"][0]["action"], "would-launch")

    def test_prepare_blocks_wrong_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            disk, ram, worktree = self.healthy_resources(runner)
            with disk, ram, worktree, \
                 patch.object(runner, "current_branch", return_value="main"), \
                 patch.object(runner, "agent_health", return_value={"ready": True, "detail": "ok"}):
                with self.assertRaisesRegex(RunnerError, "branch mismatch"):
                    runner.prepare(self._manifest(tmp))

    def test_prepare_blocks_low_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            with patch.object(runner, "disk_free_gb", return_value=20.0), \
                 patch.object(
                     runner,
                     "ram_health",
                     return_value={"ready": True, "percent": 50.0, "available_gb": 8.0, "detail": "RAM healthy"},
                 ):
                with self.assertRaisesRegex(RunnerError, "disk"):
                    runner.prepare(self._manifest(tmp))

    def test_prepare_blocks_high_ram_pressure(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            with patch.object(runner, "disk_free_gb", return_value=80.0), \
                 patch.object(
                     runner,
                     "ram_health",
                     return_value={
                         "ready": False,
                         "percent": 96.0,
                         "available_gb": 0.6,
                         "detail": "RAM pressure 96.0% used, 0.60GiB available",
                     },
                 ):
                with self.assertRaisesRegex(RunnerError, "RAM"):
                    runner.prepare(self._manifest(tmp))

    def test_prepare_requires_linked_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            with patch.object(runner, "disk_free_gb", return_value=80.0), \
                 patch.object(
                     runner,
                     "ram_health",
                     return_value={"ready": True, "percent": 50.0, "available_gb": 8.0},
                 ), \
                 patch.object(runner, "is_linked_worktree", return_value=False):
                with self.assertRaisesRegex(RunnerError, "linked worktree"):
                    runner.prepare(self._manifest(tmp))

    def test_prepare_allows_only_one_pending_mission_per_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._manifest(tmp)
            second = dict(manifest["missions"][0])
            second["id"] = "N2"
            second["report"] = str(Path(tmp) / "n2.md")
            second["budget_usd"] = 10
            manifest["missions"].append(second)
            manifest["total_budget_usd"] = 40
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            disk, ram, worktree = self.healthy_resources(runner)
            with disk, ram, worktree, \
                 patch.object(runner, "current_branch", return_value="night/2026-07-17-test"), \
                 patch.object(runner, "agent_health", return_value={"ready": True, "detail": "ok"}):
                with self.assertRaisesRegex(RunnerError, "one pending mission"):
                    runner.prepare(manifest)

    def test_prepare_blocks_completed_queue_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = self._queue()
            queue["results"] = {"B1": "DONE abc1234"}
            runner = NightRunner(self.planner, queue_loader=lambda: queue, state_dir=Path(tmp) / "state")
            disk, ram, worktree = self.healthy_resources(runner)
            with disk, ram, worktree:
                with self.assertRaisesRegex(RunnerError, "already complete"):
                    runner.prepare(self._manifest(tmp))

    def test_launch_records_pid_log_and_budget_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path(tmp) / "state")
            fake_process = type("P", (), {"pid": 4242})()
            with patch.object(runner, "prepare", return_value={"ready": True}), \
                 patch("fleet.night_runner.subprocess.Popen", return_value=fake_process):
                result = runner.launch(self._manifest(tmp))
            state = json.loads(Path(result["state_file"]).read_text(encoding="utf-8"))
            self.assertEqual(state["missions"][0]["pid"], 4242)
            self.assertEqual(state["missions"][0]["budget_usd"], 30)
            self.assertEqual(state["missions"][0]["budget_enforcement"], "advisory-timeout")
            self.assertTrue(Path(state["missions"][0]["log"]).parent.is_dir())

    def test_claude_health_detects_expired_oauth(self):
        runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path("state"))
        failed = type("R", (), {"returncode": 0, "stdout": '{"is_error":true,"result":"401 OAuth expired"}', "stderr": ""})()
        with patch("fleet.night_runner.subprocess.run", return_value=failed):
            health = runner.agent_health("claude")
        self.assertFalse(health["ready"])
        self.assertIn("401", health["detail"])

    def test_codex_health_runs_read_only_live_probe(self):
        runner = NightRunner(self.planner, queue_loader=self._queue, state_dir=Path("state"))
        passed = type("R", (), {"returncode": 0, "stdout": "pong", "stderr": ""})()
        with patch("fleet.night_runner.shutil.which", return_value="C:/bin/codex"), \
             patch("fleet.night_runner.subprocess.run", return_value=passed) as run:
            health = runner.agent_health("codex")
        self.assertTrue(health["ready"])
        args = run.call_args.args[0]
        self.assertIn("read-only", args)
        self.assertIn("--ephemeral", args)

    def _manifest(self, tmp: str):
        return {
            "date": "2026-07-17", "mode": "night", "total_budget_usd": 30,
            "missions": [{
                "id": "N1", "queue_item_id": "B1", "agent": "codex", "model": "default",
                "repo": tmp, "branch": "night/2026-07-17-test",
                "budget_usd": 30, "max_turns": 20, "timeout_minutes": 60,
                "task": "Fix safely", "why": "mechanical",
                "report": str(Path(tmp) / "n1.md")
            }]
        }


if __name__ == "__main__":
    unittest.main()
