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

    def test_budget_amounts_reject_nonfinite_boolean_and_nonnumeric_values(self):
        invalid_values = [float("nan"), float("inf"), float("-inf"), True, "10"]
        for value in invalid_values:
            with self.subTest(scope="declared", value=value):
                manifest = {
                    "version": 2,
                    "date": "2026-07-17",
                    "mode": "night",
                    "total_budget_usd": value,
                    "missions": [self._mission()],
                }
                with self.assertRaises(PlannerError):
                    self.planner.validate_manifest(manifest)
            with self.subTest(scope="mission", value=value):
                manifest = {
                    "version": 2,
                    "date": "2026-07-17",
                    "mode": "night",
                    "total_budget_usd": 30,
                    "missions": [self._mission(budget=value)],
                }
                with self.assertRaises(PlannerError):
                    self.planner.validate_manifest(manifest)
        with tempfile.TemporaryDirectory() as tmp:
            campaign = self._campaign(tmp)
            for value in invalid_values:
                with self.subTest(scope="wave", value=value):
                    manifest = json.loads(json.dumps(campaign))
                    manifest["wave_budgets_usd"]["unused"] = value
                    with self.assertRaises(PlannerError):
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
        mission = self._mission(agent="claude", budget=25)
        command = self.planner.command_for(mission)
        self.assertIn("--max-budget-usd 25", command)
        self.assertIn("--max-turns 20", command)
        self.assertIn("--model sonnet", command)
        argv = self.planner.command_args(mission)
        allowed_tools = argv[argv.index("--allowedTools") + 1]
        self.assertIn("Bash(python -m unittest discover -v)", allowed_tools)
        self.assertIn("PowerShell(python -m unittest discover -v)", allowed_tools)
        self.assertNotIn("push origin main", command)

    def test_claude_shell_allowlist_ignores_undeclared_command_families(self):
        mission = self._mission(agent="claude", budget=25)
        mission["acceptance_commands"] = ["rm -rf C:/"]
        argv = self.planner.command_args(mission)
        allowed_tools = argv[argv.index("--allowedTools") + 1]
        self.assertNotIn("rm -rf", allowed_tools)

    def test_manifest_rejects_shell_injection_in_acceptance_commands(self):
        attacks = [
            "python -m unittest discover -v; git push origin main",
            "python -m unittest discover -v && git push origin main",
            "python -m unittest discover -v | powershell",
            "python -m unittest discover -v > result.txt",
            "python -m unittest discover -v $(git status)",
            "python -m unittest discover -v\ngit push origin main",
        ]
        for attack in attacks:
            with self.subTest(attack=attack):
                mission = self._mission(agent="claude", budget=25)
                mission["acceptance_commands"] = [attack]
                manifest = {
                    "version": 2,
                    "date": "2026-07-17",
                    "mode": "night",
                    "total_budget_usd": 25,
                    "missions": [mission],
                }
                with self.assertRaisesRegex(PlannerError, "acceptance command"):
                    self.planner.validate_manifest(manifest)

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

    def test_grok_command_is_scoped_capped_and_never_bypasses_permissions(self):
        mission = self._mission(agent="grok", budget=15)
        mission["model"] = "grok-4.5"
        argv = self.planner.command_args(mission)
        self.assertIn("--cwd", argv)
        self.assertIn("workspace-write", argv)
        self.assertIn("--max-turns", argv)
        self.assertIn("--no-memory", argv)
        self.assertNotIn("--always-approve", argv)
        self.assertNotIn("bypassPermissions", argv)

    def test_dcode_launcher_fails_closed_without_enforceable_spend_cap(self):
        mission = self._mission(agent="dcode", budget=10)
        mission["timeout_minutes"] = 45
        mission["metered_spend_approval"] = {
            "approval_id": "human:approval-003",
            "approved": True,
            "provider": "dcode",
            "quota_pool": "metered-api",
            "currency": "USD",
            "max_spend_usd": 10,
            "expires_at": "2099-01-01T00:00:00+00:00",
        }
        with self.assertRaisesRegex(PlannerError, "no enforceable hard spend cap"):
            self.planner.command_args(mission)

    def test_dcode_is_rejected_outside_an_explicit_campaign(self):
        manifest = {
            "version": 2,
            "date": "2026-07-17",
            "mode": "night",
            "total_budget_usd": 10,
            "missions": [self._mission(agent="dcode", budget=10)],
        }
        with self.assertRaisesRegex(PlannerError, "require an explicitly approved campaign"):
            self.planner.validate_manifest(manifest)

    def test_generic_receipt_requires_bound_commit_artifacts_agent_and_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "night/2026-07-17-test"], cwd=tmp, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp, check=True)
            artifact = root / "artifacts" / "output.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("verified artifact", encoding="utf-8")
            subprocess.run(["git", "add", "artifacts/output.txt"], cwd=tmp, check=True)
            subprocess.run(["git", "commit", "-m", "verified artifact"], cwd=tmp, capture_output=True, check=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp, text=True).strip()
            mission = self._mission()
            mission["repo"] = tmp
            (root / "reports").mkdir()
            (root / "reports" / "n1.md").write_text("# done", encoding="utf-8")
            (root / "receipts").mkdir()
            receipt = root / mission["receipt"]
            payload = {
                "schema_version": 1,
                "mission_id": mission["id"],
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
                    "command": mission["acceptance_commands"][0],
                    "exit_code": 0,
                    "status": "passed",
                }],
                "integration_state": "pr_open",
                "completed_at": "2026-07-17T13:00:00+00:00",
            }
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            status = self.planner.status({"missions": [mission]})
            self.assertEqual("verified", status["missions"][0]["status"])
            payload["agent"] = "gemini"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                "invalid-receipt",
                self.planner.status({"missions": [mission]})["missions"][0]["status"],
            )
            payload["agent"] = mission["agent"]
            payload["verification"][0]["command"] = "true"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                "invalid-receipt",
                self.planner.status({"missions": [mission]})["missions"][0]["status"],
            )
            payload["verification"][0]["command"] = mission["acceptance_commands"][0]
            payload["artifacts"] = []
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                "unverified",
                self.planner.status({"missions": [mission]})["missions"][0]["status"],
            )
            payload["artifacts"] = mission["required_artifacts"]
            payload["commit"] = "deadbeef"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            forged = self.planner.status({"missions": [mission]})
            self.assertEqual("invalid-receipt", forged["missions"][0]["status"])

    def test_metered_receipt_requires_current_enforceable_admission(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            branch = "night/2026-07-17-metered"
            subprocess.run(["git", "init", "-b", branch], cwd=tmp, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp, check=True)
            artifact = root / "artifacts" / "output.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("verified", encoding="utf-8")
            subprocess.run(["git", "add", "artifacts/output.txt"], cwd=tmp, check=True)
            subprocess.run(["git", "commit", "-m", "verified"], cwd=tmp, capture_output=True, check=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp, text=True).strip()
            mission = self._mission(agent="dcode", budget=10)
            mission.update({
                "repo": tmp,
                "branch": branch,
                "quota_pool": "metered-api",
                "metered_spend_approval": {
                    "approval_id": "human:metered-test",
                    "approved": True,
                    "provider": "dcode",
                    "quota_pool": "metered-api",
                    "currency": "USD",
                    "max_spend_usd": 10,
                    "expires_at": "2099-01-01T00:00:00+00:00",
                },
            })
            receipt = root / mission["receipt"]
            receipt.parent.mkdir(parents=True)
            receipt.write_text(json.dumps({
                "schema_version": 1,
                "mission_id": mission["id"],
                "role": mission["role"],
                "agent": mission["agent"],
                "execution_status": "ok",
                "outcome_status": "VERIFIED",
                "status": "verified",
                "branch": branch,
                "commit": commit,
                "artifacts": mission["required_artifacts"],
                "verification": [{
                    "id": "unit",
                    "command": mission["acceptance_commands"][0],
                    "exit_code": 0,
                    "status": "passed",
                }],
                "integration_state": "pr_open",
                "completed_at": "2026-07-17T13:00:00+00:00",
            }), encoding="utf-8")
            blocked = self.planner.status({"missions": [mission]})
            self.assertEqual("blocked-admission", blocked["missions"][0]["status"])
            self.assertEqual(0, blocked["complete"])

            dcode = self.planner.config["cli_pools"]["dcode"]
            dcode["hard_spend_cap_supported"] = True
            dcode["hard_spend_cap_arg"] = "--max-spend-usd"
            mission["metered_spend_approval"]["expires_at"] = "2000-01-01T00:00:00+00:00"
            expired = self.planner.status({"missions": [mission]})
            self.assertEqual("blocked-admission", expired["missions"][0]["status"])
            mission["metered_spend_approval"]["expires_at"] = "2099-01-01T00:00:00+00:00"
            admitted = self.planner.status({"missions": [mission]})
            self.assertEqual("verified", admitted["missions"][0]["status"])
            self.assertEqual(1, admitted["complete"])

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

    def test_campaign_requires_bounded_metered_approval_for_dcode(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            mission = manifest["missions"][0]
            mission.update({"agent": "dcode", "quota_pool": "metered-api", "model": "openai"})
            with self.assertRaisesRegex(PlannerError, "explicit approval object"):
                self.planner.validate_manifest(manifest)

    def test_campaign_accepts_dcode_mapped_pool_only_with_bounded_approval_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            mission = manifest["missions"][0]
            mission.update({
                "agent": "dcode",
                "quota_pool": "metered-api",
                "model": "openai",
                "metered_spend_approval": {
                    "approval_id": "human:approval-001",
                    "approved": True,
                    "provider": "dcode",
                    "quota_pool": "metered-api",
                    "currency": "USD",
                    "max_spend_usd": 10,
                    "expires_at": "2099-01-01T00:00:00+00:00",
                },
            })
            self.assertTrue(self.planner.validate_manifest(manifest)["valid"])
            mission["metered_spend_approval"]["max_spend_usd"] = 21
            with self.assertRaisesRegex(PlannerError, "exceeds the mission budget"):
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
                "machine": maker["machine"],
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

    def test_nonfinite_and_out_of_range_quota_fail_closed(self):
        invalid_values = [float("nan"), float("inf"), float("-inf"), -1, 101, True, "not-a-number"]
        for value in invalid_values:
            with self.subTest(value=value):
                ready, detail = self.planner.quota_health(
                    "claude", {"claude": {"remaining_percent": value}}
                )
                self.assertFalse(ready)
                self.assertIn("invalid", detail)
                normalized = self.planner.normalize_quota_payload({
                    "providers": [{"provider": "Claude", "remaining_percent": value}]
                })
                self.assertNotIn("claude", normalized)

    def test_campaign_requires_machine_compatible_with_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._campaign(tmp)
            incompatible = json.loads(json.dumps(manifest))
            del manifest["missions"][0]["machine"]
            with self.assertRaisesRegex(PlannerError, "missing machine"):
                self.planner.validate_manifest(manifest)

            incompatible["missions"][0]["machine"] = "unknown-machine"
            with self.assertRaisesRegex(PlannerError, "not configured for machine"):
                self.planner.validate_manifest(incompatible)

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
                "machine": mission["machine"],
                "execution_status": "ok",
                "outcome_status": "VERIFIED",
                "status": "verified",
                "branch": mission["branch"],
                "commit": commit,
                "artifacts": mission["required_artifacts"],
                "verification": [{
                    "id": mission["verification_ids"][0],
                    "command": mission["acceptance_commands"][0],
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
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            payload["machine"] = "c940"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                self.planner.status(manifest)["missions"][0]["status"],
                "invalid-receipt",
            )
            payload["machine"] = mission["machine"]
            receipt.write_text(json.dumps(payload), encoding="utf-8")
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
            "id": "C1-M", "objective_id": "OBJ-1", "role": "maker", "job_class": "refactor", "wave": 1,
            "agent": "codex", "machine": "yoga-book", "quota_pool": "codex", "model": "gpt-5.6-terra",
            "repo": tmp, "branch": "agent/hermes/test", "budget_usd": 20,
            "max_turns": 20, "timeout_minutes": 60, "task": "Build safely",
            "outcome": "working artifact", "report": "reports/maker.md",
            "receipt": "receipts/maker.json", "required_artifacts": ["artifacts/output.txt"],
            "verification_ids": ["unit"], "acceptance_commands": ["python -m unittest discover -v"],
        }
        verifier = {
            **maker,
            "id": "C1-V", "role": "verifier", "wave": 2,
            "depends_on": ["C1-M"],
            "agent": "claude", "machine": "c940", "quota_pool": "claude", "model": "opus",
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

    def _mission(self, agent="claude", budget=40, report="reports/n1.md", receipt="receipts/n1.json"):
        return {
            "id": "N1", "agent": agent, "role": "maker",
            "model": "sonnet" if agent == "claude" else "gpt-5.6-terra",
            "repo": "C:/repo", "branch": "night/2026-07-17-test",
            "budget_usd": budget, "max_turns": 20, "timeout_minutes": 60,
            "task": "Fix backend safely", "why": "fit", "report": report,
            "receipt": receipt, "required_artifacts": ["artifacts/output.txt"],
            "verification_ids": ["unit"],
            "acceptance_commands": ["python -m unittest discover -v"],
        }


if __name__ == "__main__":
    unittest.main()
