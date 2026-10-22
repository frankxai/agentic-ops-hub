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
        self.assertEqual(decision["model"], "opus")
        self.assertEqual(decision["budget_usd"], 40)
        self.assertIn("multi-file", decision["why"].lower())

    def test_recommends_codex_for_mechanical_refactor(self):
        decision = self.planner.recommend("refactor", complexity=4, unattended=True)
        self.assertEqual(decision["agent"], "codex")
        self.assertEqual(decision["budget_usd"], 30)

    def test_rejects_manifest_over_night_cap(self):
        manifest = {"date": "2026-07-17", "mode": "night", "total_budget_usd": 111, "missions": []}
        with self.assertRaisesRegex(PlannerError, "night cap"):
            self.planner.validate_manifest(manifest)

    def test_rejects_main_branch_and_missing_report(self):
        manifest = {
            "version": 2, "date": "2026-07-17", "mode": "night", "total_budget_usd": 40,
            "missions": [{
                "id": "N1", "agent": "claude", "repo": "C:/repo", "branch": "main",
                "budget_usd": 40, "max_turns": 20, "task": "fix backend", "report": ""
            }],
        }
        with self.assertRaisesRegex(PlannerError, "night/"):
            self.planner.validate_manifest(manifest)

    def test_rejects_mission_sum_above_declared_budget(self):
        manifest = {
            "version": 2, "date": "2026-07-17", "mode": "night", "total_budget_usd": 30,
            "missions": [self._mission(budget=40)],
        }
        with self.assertRaisesRegex(PlannerError, "mission budgets"):
            self.planner.validate_manifest(manifest)

    def test_claude_command_has_hard_budget_and_turn_caps(self):
        command = self.planner.command_for(self._mission(agent="claude", budget=25))
        self.assertIn("--max-budget-usd 25", command)
        self.assertIn("--max-turns 20", command)
        self.assertIn("--model sonnet", command)
        self.assertNotIn("push origin main", command)

    def test_codex_command_is_repo_scoped_without_sandbox_widening(self):
        command = self.planner.command_for(self._mission(agent="codex", budget=30))
        self.assertIn("--sandbox workspace-write", command)
        self.assertIn("-C C:/repo", command)
        self.assertNotIn("danger-full-access", command)

    def test_sandbox_cannot_be_widened_by_caller(self):
        for widened in ("danger-full-access", "DANGER-FULL-ACCESS", "full"):
            with self.assertRaisesRegex(PlannerError, "sandbox"):
                self.planner.command_args(self._mission(agent="codex", budget=30), sandbox=widened)

    def test_read_only_sandbox_is_allowed(self):
        args = self.planner.command_args(self._mission(agent="codex", budget=30), sandbox="read-only")
        self.assertIn("read-only", args)

    def test_no_launcher_emits_a_bypass_flag(self):
        for agent in ("claude", "codex", "opencode", "gemini"):
            mission = self._mission(agent=agent, budget=30)
            mission["route_class"] = "code"
            task = self.planner._task_contract(mission)
            flags = [a.lower() for a in self.planner.command_args(mission) if a != task]
            for token in ("danger-full-access", "--dangerously-skip-permissions",
                          "--dangerously-bypass-approvals-and-sandbox", "--yolo"):
                self.assertFalse(any(token in a for a in flags), f"{agent} launcher leaks {token}")

    def test_boundary_rejects_bypass_flag_but_not_task_prose(self):
        with self.assertRaisesRegex(PlannerError, "forbidden"):
            Planner._assert_launch_safe(["codex", "exec", "--yolo", "task"], task="task")
        mission = self._mission(agent="codex", budget=30)
        mission["task"] = "Explain why danger-full-access and --yolo are never used"
        self.planner.command_args(mission)  # prose that mentions a token must not be rejected

    def test_status_requires_verified_receipt_not_only_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "n1.md"
            receipt = Path(tmp) / "n1.json"
            m1 = self._mission(report=str(report), receipt=str(receipt))
            m2 = self._mission(report=str(Path(tmp) / "n2.md"), receipt=str(Path(tmp) / "n2.json"))
            m2["id"] = "N2"
            report.write_text("# done", encoding="utf-8")
            receipt.write_text(json.dumps({
                "mission_id": "N1", "status": "verified", "branch": m1["branch"],
                "commit": "abc1234",
                "verification": [{"command": "python -m unittest", "exit_code": 0}],
                "integration_state": "pr_open", "completed_at": "2026-07-17T13:00:00+00:00",
            }), encoding="utf-8")
            status = self.planner.status({"missions": [m1, m2]})
            self.assertEqual(status["complete"], 1)
            self.assertEqual(status["missing"], 1)
            self.assertEqual(status["missions"][0]["status"], "verified")

    def test_debrief_contains_budget_and_incomplete_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "n1.md"
            report.write_text("# N1\n\nResult: PASS.\n", encoding="utf-8")
            manifest = {
                "date": "2026-07-17", "total_budget_usd": 30,
                "missions": [self._mission(report=str(report), receipt=str(Path(tmp) / "n1.json"), budget=30)],
            }
            text = self.planner.debrief(manifest)
            self.assertIn("Budget envelope: $30", text)
            self.assertIn("N1", text)
            self.assertIn("incomplete", text)
            self.assertIn("Human review required", text)

    def test_opencode_launch_is_pinned_to_the_gateway_model_for_its_class(self):
        mission = self._mission(agent="opencode", budget=30)
        mission["route_class"] = "scout"
        args = self.planner.command_args(mission)
        # The command is the launch wrapper: it builds the provider-restricted config, then runs
        # `opencode run --standalone -m <pinned model>` (see tests/test_opencode_launch.py).
        self.assertEqual(args[0], "python")
        self.assertEqual(args[args.index("--class") + 1], "scout")
        self.assertNotIn("--allow-free", args)
        self.assertEqual(args[-2], "--")

    def test_opencode_launch_keeps_the_class_variant(self):
        mission = self._mission(agent="opencode", budget=30)
        mission["route_class"] = "code"
        from fleet import opencode_launch
        from fleet.token_planner import pinned_opencode_model
        self.assertEqual(pinned_opencode_model("code"), "vercel/zai/glm-5.3#medium")
        self.assertEqual(opencode_launch.opencode_argv("vercel/zai/glm-5.3#medium", "t", "oc")[3:5],
                         ["-m", "vercel/zai/glm-5.3#medium"])

    def test_opencode_launch_refuses_without_a_resolvable_class(self):
        for bad in (None, "", "nonsense", 7):
            mission = self._mission(agent="opencode", budget=30)
            if bad is not None:
                mission["route_class"] = bad
            with self.assertRaisesRegex(PlannerError, "route_class|cannot resolve"):
                self.planner.command_args(mission)

    def test_allow_free_changes_the_pinned_model_only_when_asked(self):
        mission = self._mission(agent="opencode", budget=30)
        mission["route_class"] = "scout"
        free = Planner(self.planner.config, allow_free=True).command_args(mission)
        self.assertIn("--allow-free", free)
        self.assertNotIn("--allow-free", self.planner.command_args(mission))
        from fleet.token_planner import pinned_opencode_model
        self.assertTrue(pinned_opencode_model("scout", allow_free=True).startswith("opencode/"))
        self.assertTrue(pinned_opencode_model("scout").startswith("vercel/"))

    def _mission(self, agent="claude", budget=40, report="C:/reports/n1.md", receipt="C:/reports/n1.json"):
        return {
            "id": "N1", "agent": agent,
            "model": "sonnet" if agent == "claude" else "gpt-5.6-terra",
            "repo": "C:/repo", "branch": "night/2026-07-17-test",
            "budget_usd": budget, "max_turns": 20, "timeout_minutes": 60,
            "task": "Fix backend safely", "why": "fit", "report": report,
            "receipt": receipt, "acceptance_commands": ["python -m unittest discover -v"],
        }


class PinnedModelIgnoresFilteredPrimary(unittest.TestCase):
    def test_excluded_raw_primary_is_never_pinned(self):
        import json
        from unittest.mock import patch
        from fleet import route_executor
        from fleet.token_planner import pinned_opencode_model

        schema = json.loads(route_executor.SCHEMA_PATH.read_text(encoding="utf-8"))
        schema["task_classes"]["code"]["primary"] = "opencode/beam-free"
        with patch.object(route_executor, "load_schema", return_value=schema):
            pinned = pinned_opencode_model("code")
            argv = ["opencode", "run", "--standalone", "-m", pinned, "task"]
        self.assertNotIn("opencode/beam-free", " ".join(argv))
        self.assertTrue(pinned.startswith("vercel/"), pinned)

    def test_class_with_no_safe_model_refuses_to_launch(self):
        import json
        from unittest.mock import patch
        from fleet import route_executor
        from fleet.token_planner import pinned_opencode_model

        schema = json.loads(route_executor.SCHEMA_PATH.read_text(encoding="utf-8"))
        schema["task_classes"]["code"]["primary"] = "opencode/beam-free"
        schema["task_classes"]["code"]["fallbacks"] = ["opencode/minimax-m3.1-flash-free"]
        with patch.object(route_executor, "load_schema", return_value=schema):
            with self.assertRaises(PlannerError):
                pinned_opencode_model("code")


if __name__ == "__main__":
    unittest.main()
