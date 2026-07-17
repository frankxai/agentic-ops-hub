import json
import subprocess
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

    def test_agy_command_uses_mission_timeout_and_safe_repo_scope(self):
        command = self.planner.command_for(self._mission(agent="agy", budget=10))
        self.assertIn("--print-timeout 60m0s", command)
        self.assertIn("WINDOWS PHONE LINK PATH BAN", command)
        self.assertIn("exact repo leaf C:/repo", command)
        self.assertIn("Do not clone", command)

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

    def test_campaign_requires_distinct_maker_and_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            manifest["missions"][1]["agent"] = "codex"
            manifest["missions"][1]["quota_pool"] = "codex"
            with self.assertRaisesRegex(PlannerError, "must differ"):
                self.planner.validate_manifest(manifest)

    def test_campaign_rejects_nonportable_receipt_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            manifest["missions"][0]["receipt"] = str(Path(tmp) / "receipt.json")
            with self.assertRaisesRegex(PlannerError, "portable"):
                self.planner.validate_manifest(manifest)

    def test_campaign_rejects_windows_rooted_and_drive_relative_paths(self):
        for bad_path in (r"\outside\receipt.json", r"C:outside\receipt.json"):
            with tempfile.TemporaryDirectory() as tmp:
                manifest = self._campaign(tmp)
                manifest["missions"][0]["receipt"] = bad_path
                with self.assertRaisesRegex(PlannerError, "repo-relative"):
                    self.planner.validate_manifest(manifest)

    def test_campaign_rejects_objective_registry_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            manifest["objectives"][0]["success_metric"] = "invented metric"
            with self.assertRaisesRegex(PlannerError, "canonical registry"):
                self.planner.validate_manifest(manifest)

    def test_campaign_rejects_attacker_owned_same_name_control_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            subprocess.run(
                ["git", "remote", "set-url", "origin", "https://github.com/attacker/agentic-ops-hub.git"],
                cwd=tmp,
                check=True,
            )
            with self.assertRaisesRegex(PlannerError, "canonical frankxai control repository"):
                self.planner.validate_manifest(manifest)

    def test_campaign_rejects_attacker_owned_same_name_mission_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            attacker = Path(tmp) / "attacker-repo"
            attacker.mkdir()
            subprocess.run(
                ["git", "init", "-b", "agent/hermes/test"],
                cwd=attacker,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/attacker/agentic-ops-hub.git"],
                cwd=attacker,
                check=True,
            )
            for mission in manifest["missions"]:
                mission["repo"] = str(attacker)
            with self.assertRaisesRegex(PlannerError, "repo does not match objective"):
                self.planner.validate_manifest(manifest)

    def test_campaign_rejects_same_wave_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            manifest["missions"][1]["wave"] = 1
            manifest["wave_budgets_usd"]["1"] = 30
            with self.assertRaisesRegex(PlannerError, "after maker wave"):
                self.planner.validate_manifest(manifest)

    def test_blocked_maker_never_advances_to_verifier_wave(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            maker = manifest["missions"][0]
            receipt = Path(tmp) / maker["receipt"]
            receipt.parent.mkdir(parents=True)
            receipt.write_text(json.dumps({
                "schema_version": 1,
                "mission_id": maker["id"],
                "objective_id": maker["objective_id"],
                "role": maker["role"],
                "agent": maker["agent"],
                "outcome_status": "BLOCKED",
                "branch": maker["branch"],
            }), encoding="utf-8")
            status = self.planner.status(manifest)
            self.assertEqual(status["missions"][0]["status"], "blocked")
            status_by_id = {row["id"]: row["status"] for row in status["missions"]}
            self.assertEqual(
                self.planner.dependency_state(manifest["missions"][1], status_by_id),
                "blocked",
            )
            self.assertIsNone(self.planner.active_wave(manifest))

    def test_campaign_rejects_prohibited_task_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            manifest["missions"][0]["task"] = "Run git push origin main"
            with self.assertRaisesRegex(PlannerError, "prohibited operation"):
                self.planner.validate_manifest(manifest)

    def test_quota_depletion_routes_to_healthy_fallback(self):
        decision = self.planner.recommend(
            "deep-backend",
            usage={
                "claude": {"remaining_percent": 2},
                "opencode": {"remaining_percent": 100},
            },
        )
        self.assertEqual(decision["agent"], "opencode")
        self.assertEqual(decision["original_agent"], "claude")

    def test_campaign_receipt_requires_schema_artifacts_and_verification_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._campaign(tmp)
            mission = manifest["missions"][0]
            artifact = root / mission["required_artifacts"][0]
            artifact.parent.mkdir(parents=True)
            artifact.write_text("artifact", encoding="utf-8")
            subprocess.run(
                ["git", "add", mission["required_artifacts"][0]],
                cwd=tmp,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "add artifact"],
                cwd=tmp,
                capture_output=True,
                check=True,
            )
            commit = subprocess.run(
                ["git", "-C", tmp, "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            receipt = root / mission["receipt"]
            receipt.parent.mkdir(parents=True)
            receipt.write_text(json.dumps({
                "schema_version": 1,
                "mission_id": mission["id"],
                "objective_id": mission["objective_id"],
                "role": mission["role"],
                "agent": mission["agent"],
                "execution_status": "ok",
                "outcome_status": "VERIFIED",
                "status": "verified",
                "branch": mission["branch"],
                "commit": commit,
                "artifacts": mission["required_artifacts"],
                "verification": [{
                    "id": mission["verification_ids"][0],
                    "command": "python -m unittest",
                    "exit_code": 0,
                    "status": "passed",
                }],
                "integration_state": "pr_open",
                "completed_at": "2026-07-17T18:00:00+00:00",
            }), encoding="utf-8")
            state = self.planner.status(manifest)
            self.assertEqual(state["missions"][0]["status"], "verified")
            self.assertEqual(state["missions"][1]["status"], "missing-receipt")
            self.assertEqual(self.planner.active_wave(manifest), 2)
            artifact.write_text("changed after receipt commit", encoding="utf-8")
            self.assertEqual(
                self.planner.status(manifest)["missions"][0]["status"],
                "invalid-receipt",
            )
            artifact.write_text("artifact", encoding="utf-8")
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            payload["verification"][0]["command"] = "true"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                self.planner.status(manifest)["missions"][0]["status"],
                "invalid-receipt",
            )
            payload["verification"][0]["command"] = mission["acceptance_commands"][0]
            payload["agent"] = "claude"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                self.planner.status(manifest)["missions"][0]["status"],
                "invalid-receipt",
            )
            payload["agent"] = mission["agent"]
            payload["commit"] = "deadbeef"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                self.planner.status(manifest)["missions"][0]["status"],
                "invalid-receipt",
            )

    def test_launcher_rejects_known_sandbox_bypass(self):
        with self.assertRaisesRegex(PlannerError, "sandbox bypass"):
            self.planner._assert_launch_safe(["codex", "--yolo"])

    def _campaign(self, tmp: str):
        root = Path(tmp)
        canonical_objective = {
            "id": "OBJ-1",
            "repo": "agentic-ops-hub",
            "executive_owner": "CTO",
            "outcome": "working artifact",
            "success_metric": "artifact verified",
        }
        (root / "objectives-registry.json").write_text(
            json.dumps({"schema_version": 1, "objectives": [canonical_objective]}),
            encoding="utf-8",
        )
        (root / "seed.txt").write_text("seed", encoding="utf-8")
        subprocess.run(
            ["git", "init", "-b", "agent/hermes/test"],
            cwd=tmp,
            capture_output=True,
            check=True,
        )
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp, check=True)
        subprocess.run(
            ["git", "remote", "add", "origin", "https://github.com/frankxai/agentic-ops-hub.git"],
            cwd=tmp,
            check=True,
        )
        subprocess.run(["git", "add", "seed.txt", "objectives-registry.json"], cwd=tmp, check=True)
        subprocess.run(
            ["git", "commit", "-m", "seed"],
            cwd=tmp,
            capture_output=True,
            check=True,
        )
        maker = {
            "id": "C1-M", "objective_id": "OBJ-1", "role": "maker", "wave": 1,
            "agent": "codex", "quota_pool": "codex", "model": "gpt-5.6-terra",
            "repo": tmp, "branch": "agent/hermes/test", "budget_usd": 20,
            "max_turns": 20, "timeout_minutes": 60, "task": "Build safely",
            "outcome": "working artifact", "report": "reports/maker.md",
            "receipt": "receipts/maker.json", "required_artifacts": ["artifacts/output.txt"],
            "verification_ids": ["unit"], "acceptance_commands": ["python -m unittest"],
        }
        verifier = {
            **maker,
            "id": "C1-V", "role": "verifier", "wave": 2,
            "depends_on": ["C1-M"],
            "agent": "claude", "quota_pool": "claude", "model": "opus",
            "budget_usd": 10, "report": "reports/verifier.md",
            "receipt": "receipts/verifier.json", "required_artifacts": ["reports/verifier.md"],
        }
        return {
            "version": 3, "date": "2026-07-17", "campaign_id": "campaign-test",
            "mode": "campaign", "control_repo": tmp,
            "objective_registry": "objectives-registry.json",
            "total_budget_usd": 30, "max_concurrency": 1,
            "minimum_verified_outcomes": 1, "wave_budgets_usd": {"1": 20, "2": 10},
            "stop_conditions": ["test failure"],
            "objectives": [canonical_objective],
            "missions": [maker, verifier],
        }

    def _mission(self, agent="claude", budget=40, report="C:/reports/n1.md", receipt="C:/reports/n1.json"):
        return {
            "id": "N1", "agent": agent,
            "model": "sonnet" if agent == "claude" else "gpt-5.6-terra",
            "repo": "C:/repo", "branch": "night/2026-07-17-test",
            "budget_usd": budget, "max_turns": 20, "timeout_minutes": 60,
            "task": "Fix backend safely", "why": "fit", "report": report,
            "receipt": receipt, "acceptance_commands": ["python -m unittest discover -v"],
        }


if __name__ == "__main__":
    unittest.main()
