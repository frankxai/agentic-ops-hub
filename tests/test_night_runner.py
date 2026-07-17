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

    def _safe_prepare_mocks(self, runner):
        return (
            patch.object(runner, "current_branch", return_value="night/2026-07-17-test"),
            patch.object(runner, "disk_free_gb", return_value=60.0),
            patch.object(runner, "memory_percent", return_value=50.0),
            patch.object(runner, "is_clean", return_value=True),
            patch.object(runner, "agent_health", return_value={"ready": True, "detail": "codex test"}),
        )

    def test_prepare_is_dry_run_and_writes_no_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            mocks = self._safe_prepare_mocks(runner)
            with mocks[0], mocks[1], mocks[2], mocks[3], mocks[4]:
                result = runner.prepare(self._manifest(tmp))
            self.assertTrue(result["ready"])
            self.assertFalse((Path(tmp) / "state").exists())
            self.assertEqual(result["missions"][0]["action"], "would-launch")

    def test_prepare_blocks_wrong_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            with patch.object(runner, "current_branch", return_value="main"), \
                 patch.object(runner, "disk_free_gb", return_value=60.0), \
                 patch.object(runner, "memory_percent", return_value=50.0), \
                 patch.object(runner, "is_clean", return_value=True):
                with self.assertRaisesRegex(RunnerError, "branch mismatch"):
                    runner.prepare(self._manifest(tmp))

    def test_prepare_blocks_low_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            with patch.object(runner, "disk_free_gb", return_value=20.0), \
                 patch.object(runner, "memory_percent", return_value=50.0):
                with self.assertRaisesRegex(RunnerError, "disk"):
                    runner.prepare(self._manifest(tmp))

    def test_launch_records_bounded_exit_and_receipt_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            prepared = {"ready": True, "missions": [{"action": "would-launch"}]}
            fake_result = type("R", (), {"returncode": 0})()
            with patch.object(runner, "prepare", return_value=prepared), \
                 patch.object(runner, "enforce_resources"), \
                 patch("fleet.night_runner.subprocess.run", return_value=fake_result):
                result = runner.launch(self._manifest(tmp))
            state = json.loads(Path(result["state_file"]).read_text(encoding="utf-8"))
            self.assertEqual(state["missions"][0]["exit_code"], 0)
            self.assertEqual(state["missions"][0]["status"], "failed-unverified")
            self.assertEqual(state["missions"][0]["receipt_status"], "missing-receipt")
            self.assertTrue(Path(state["missions"][0]["log"]).parent.is_dir())

    def test_claude_health_detects_expired_oauth(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        failed = type("R", (), {
            "returncode": 0,
            "stdout": '{"is_error":true,"result":"401 OAuth expired"}',
            "stderr": "",
        })()
        with patch("fleet.night_runner.subprocess.run", return_value=failed), \
             patch("fleet.night_runner.shutil.which", return_value="C:/bin/claude"):
            health = runner.agent_health({"agent": "claude", "model": "sonnet", "repo": "C:/repo"})
        self.assertFalse(health["ready"])
        self.assertIn("401", health["detail"])

    def test_codex_health_requires_installed_cli(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        with patch("fleet.night_runner.shutil.which", return_value=None):
            health = runner.agent_health({"agent": "codex", "model": "gpt-5.6-terra", "repo": "C:/repo"})
        self.assertFalse(health["ready"])
        self.assertIn("not found", health["detail"])

    def _manifest(self, tmp: str):
        return {
            "version": 2, "date": "2026-07-17", "mode": "night", "total_budget_usd": 30,
            "missions": [{
                "id": "N1", "agent": "codex", "model": "gpt-5.6-terra",
                "repo": tmp, "branch": "night/2026-07-17-test",
                "budget_usd": 30, "max_turns": 20, "timeout_minutes": 60,
                "task": "Fix safely", "why": "mechanical",
                "report": str(Path(tmp) / "n1.md"),
                "receipt": str(Path(tmp) / "n1.json"),
                "acceptance_commands": ["python -m unittest discover -v"],
            }],
        }


if __name__ == "__main__":
    unittest.main()
