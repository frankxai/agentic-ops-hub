import json
import tempfile
import unittest
from pathlib import Path

from fleet.token_planner import Planner, PlannerError


class TokenPlannerTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.planner = Planner.from_file(self.root / "fleet" / "model-routing.json")

    def test_recommends_claude_for_deep_backend_with_reason_and_budget(self):
        decision = self.planner.recommend("deep-backend", complexity=8, unattended=True)
        self.assertEqual(decision["agent"], "claude")
        self.assertEqual(decision["model"], "sonnet")
        self.assertEqual(decision["budget_usd"], 20)
        self.assertIn("multi-file", decision["why"].lower())

    def test_recommends_codex_for_mechanical_refactor(self):
        decision = self.planner.recommend("refactor", complexity=4, unattended=True)
        self.assertEqual(decision["agent"], "codex")
        self.assertEqual(decision["budget_usd"], 20)

    def test_rejects_manifest_over_night_cap(self):
        manifest = {
            "date": "2026-07-17",
            "mode": "night",
            "total_budget_usd": 41,
            "missions": [],
        }
        with self.assertRaisesRegex(PlannerError, "night cap"):
            self.planner.validate_manifest(manifest)

    def test_rejects_main_branch_and_missing_report(self):
        manifest = {
            "date": "2026-07-17",
            "mode": "night",
            "total_budget_usd": 40,
            "missions": [{
                "id": "N1", "agent": "claude", "repo": "C:/repo",
                "branch": "main", "budget_usd": 40, "max_turns": 20,
                "task": "fix backend", "report": ""
            }],
        }
        with self.assertRaisesRegex(PlannerError, "night/"):
            self.planner.validate_manifest(manifest)

    def test_rejects_mission_sum_above_declared_budget(self):
        manifest = {
            "date": "2026-07-17", "mode": "night", "total_budget_usd": 30,
            "missions": [self._mission(budget=40)],
        }
        with self.assertRaisesRegex(PlannerError, "mission budgets"):
            self.planner.validate_manifest(manifest)

    def test_rejects_mission_without_queue_item(self):
        mission = self._mission()
        mission.pop("queue_item_id")
        manifest = {
            "date": "2026-07-17", "mode": "night", "total_budget_usd": 40,
            "missions": [mission],
        }
        with self.assertRaisesRegex(PlannerError, "queue_item_id"):
            self.planner.validate_manifest(manifest)

    def test_claude_command_has_hard_budget_and_turn_caps(self):
        command = self.planner.command_for(self._mission(agent="claude", budget=25))
        self.assertIn("--max-budget-usd 25", command)
        self.assertIn("--max-turns 20", command)
        self.assertIn("--model sonnet", command)
        self.assertNotIn("push origin main", command)

    def test_codex_command_uses_workspace_write_sandbox(self):
        command = self.planner.command_for(self._mission(agent="codex", budget=30))
        self.assertIn("--sandbox workspace-write", command)
        self.assertNotIn("danger-full-access", command)
        self.assertNotIn("dangerously-bypass", command)
        self.assertIn("timeout", command.lower())

    def test_status_requires_fresh_verified_report_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "n1.md"
            mission = self._mission(report=str(report))
            report.write_text("# done", encoding="utf-8")
            status = self.planner.status({"missions": [mission]})
            self.assertEqual(status["complete"], 0)
            self.assertEqual(status["missions"][0]["status"], "unverified")
            report.write_text(
                "# N1\n\nStatus: PASS\nCommit: abc1234\nTests: 12 passed\n",
                encoding="utf-8",
            )
            status = self.planner.status({"missions": [mission]})
            self.assertEqual(status["complete"], 1)
            self.assertEqual(status["missions"][0]["status"], "complete")

    def test_status_marks_reports_complete_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "n1.md"
            m1 = self._mission(report=str(report))
            m2 = self._mission(report=str(Path(tmp) / "n2.md"))
            m2["id"] = "N2"
            report.write_text("# done\n\nStatus: PASS\nCommit: abc1234\nTests: 1 passed\n", encoding="utf-8")
            status = self.planner.status({"missions": [m1, m2]})
            self.assertEqual(status["complete"], 1)
            self.assertEqual(status["missing"], 1)
            self.assertEqual(status["missions"][0]["status"], "complete")

    def test_debrief_contains_budget_and_mission_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "n1.md"
            report.write_text("# N1\n\nResult: PASS.\n", encoding="utf-8")
            manifest = {
                "date": "2026-07-17", "total_budget_usd": 30,
                "missions": [self._mission(report=str(report), budget=30)],
            }
            text = self.planner.debrief(manifest)
            self.assertIn("Budget envelope: $30", text)
            self.assertIn("N1", text)
            self.assertIn("complete", text)
            self.assertIn("Human review required", text)

    def _mission(self, agent="claude", budget=40, report="C:/reports/n1.md"):
        return {
            "id": "N1", "queue_item_id": "B1", "agent": agent, "model": "sonnet" if agent == "claude" else "default",
            "repo": "C:/repo", "branch": "night/2026-07-17-test",
            "budget_usd": budget, "max_turns": 20, "timeout_minutes": 60,
            "task": "Fix backend safely", "why": "fit", "report": report,
        }


if __name__ == "__main__":
    unittest.main()
