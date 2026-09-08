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
            patch.object(runner, "subscription_usage", return_value={
                "codex": {"remaining_percent": 70},
                "claude": {"remaining_percent": 70},
            }),
        )

    def test_prepare_is_dry_run_and_writes_no_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            mocks = self._safe_prepare_mocks(runner)
            with mocks[0], mocks[1], mocks[2], mocks[3], mocks[4], mocks[5]:
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
            prepared = {
                "ready": True,
                "missions": [{
                    "action": "would-launch",
                    "agent": "codex",
                    "argv": ["codex", "exec", "test"],
                }],
            }
            fake_result = type("R", (), {"returncode": 0})()
            with patch.object(runner, "prepare", return_value=prepared), \
                 patch.object(runner, "_revalidate_for_launch", return_value=prepared["missions"][0]), \
                 patch.object(runner, "enforce_resources"), \
                 patch("fleet.night_runner.subprocess.run", return_value=fake_result):
                result = runner.launch(self._manifest(tmp))
            state = json.loads(Path(result["state_file"]).read_text(encoding="utf-8"))
            self.assertEqual(state["missions"][0]["exit_code"], 0)
            self.assertEqual(state["missions"][0]["status"], "failed-unverified")
            self.assertEqual(state["missions"][0]["receipt_status"], "missing-receipt")
            self.assertTrue(Path(state["missions"][0]["log"]).parent.is_dir())

    def test_launch_rechecks_receipt_after_lease_and_skips_stale_prepared_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            prepared = {
                "ready": True,
                "missions": [{
                    "action": "would-launch",
                    "agent": "codex",
                    "argv": ["codex", "exec", "stale"],
                }],
            }
            verified = {"missions": [{"id": "N1", "status": "verified"}]}
            with patch.object(runner, "prepare", return_value=prepared), \
                 patch.object(self.planner, "validate_manifest", return_value={"valid": True}), \
                 patch.object(self.planner, "status", return_value=verified), \
                 patch("fleet.night_runner.Path.home", return_value=Path(tmp)), \
                 patch("fleet.night_runner.subprocess.run") as run_mock:
                result = runner.launch(self._manifest(tmp))
            self.assertEqual(result["missions"][0]["status"], "skip-verified")
            run_mock.assert_not_called()

    def test_post_lease_revalidation_blocks_changed_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = NightRunner(self.planner, state_dir=Path(tmp) / "state")
            manifest = self._manifest(tmp)
            missing = {"missions": [{"id": "N1", "status": "missing-receipt"}]}
            with patch.object(self.planner, "validate_manifest", return_value={"valid": True}), \
                 patch.object(self.planner, "status", return_value=missing), \
                 patch.object(self.planner, "dependency_state", return_value="ready"), \
                 patch.object(runner, "current_branch", return_value=manifest["missions"][0]["branch"]), \
                 patch.object(runner, "is_clean", return_value=False), \
                 patch.object(runner, "_route_mission") as route_mock:
                with self.assertRaisesRegex(RunnerError, "repo is dirty"):
                    runner._revalidate_for_launch(manifest, manifest["missions"][0])
            route_mock.assert_not_called()

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
        self.assertEqual("claude preflight failed (exit 0)", health["detail"])
        self.assertNotIn("401", health["detail"])

    def test_claude_health_accepts_event_list_without_leaking_metadata(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        response = [
            {"type": "system", "session_id": "private-session"},
            {"type": "result", "is_error": False, "result": "PONG", "session_id": "private-session"},
        ]
        succeeded = type("R", (), {
            "returncode": 0,
            "stdout": json.dumps(response),
            "stderr": "",
        })()
        with patch("fleet.night_runner.subprocess.run", return_value=succeeded), \
             patch("fleet.night_runner.shutil.which", return_value="C:/bin/claude"):
            health = runner.agent_health({"agent": "claude", "model": "opus", "repo": "C:/repo"})
        self.assertTrue(health["ready"])
        self.assertEqual(health["detail"], "PONG")
        self.assertNotIn("private-session", health["detail"])

    def test_codex_health_requires_installed_cli(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        with patch("fleet.night_runner.shutil.which", return_value=None):
            health = runner.agent_health({"agent": "codex", "model": "gpt-5.6-terra", "repo": "C:/repo"})
        self.assertFalse(health["ready"])
        self.assertIn("not found", health["detail"])

    def test_non_claude_health_redacts_provider_output(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        succeeded = type("R", (), {
            "returncode": 0,
            "stdout": 'PONG {"requestId":"private-id"}',
            "stderr": "",
        })()
        with patch("fleet.night_runner.subprocess.run", return_value=succeeded), \
             patch("fleet.night_runner.shutil.which", return_value="C:/bin/grok"):
            health = runner.agent_health({"agent": "grok", "model": "grok-4.5", "repo": "C:/repo"})
        self.assertTrue(health["ready"])
        self.assertEqual("PONG", health["detail"])

    def test_gemini_health_probe_is_read_only_and_never_yolo(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        succeeded = type("R", (), {"returncode": 0, "stdout": "PONG", "stderr": ""})()
        with patch("fleet.night_runner.subprocess.run", return_value=succeeded) as run_mock, \
             patch("fleet.night_runner.shutil.which", return_value="C:/bin/gemini"):
            health = runner.agent_health(
                {"agent": "gemini", "model": "gemini-2.5-pro", "repo": "C:/repo"}
            )
        command = run_mock.call_args.args[0]
        self.assertNotIn("--yolo", command)
        self.assertIn("--approval-mode", command)
        self.assertEqual("plan", command[command.index("--approval-mode") + 1])
        self.assertIn("--sandbox=true", command)
        self.assertTrue(health["ready"])

    def test_subscription_usage_accepts_list_root_and_strips_identity(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        payload = [{
            "provider": "Claude",
            "plan": "Max 20x",
            "email": "private@example.com",
            "metrics": [
                {"label": "Session", "remaining_percent": 91},
                {"label": "Weekly", "remaining_percent": 68},
            ],
        }]
        result = type("R", (), {
            "returncode": 0,
            "stdout": json.dumps(payload),
            "stderr": "",
        })()
        with patch("fleet.night_runner.shutil.which", return_value="C:/bin/tokscale"), \
             patch("fleet.night_runner.subprocess.run", return_value=result):
            usage = runner.subscription_usage()
        self.assertEqual(usage["claude"]["remaining_percent"], 68)
        self.assertNotIn("email", usage["claude"])

    def test_route_mission_falls_back_when_preferred_quota_is_depleted(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        mission = self._manifest("C:/repo")["missions"][0]
        with patch.object(
            runner,
            "agent_health",
            return_value={"ready": True, "detail": "live"},
        ):
            routed, detail, _ = runner._route_mission(
                mission,
                {
                    "codex": {"remaining_percent": 2},
                    "claude": {"remaining_percent": 70},
                },
                set(),
                {},
            )
        self.assertEqual(routed["agent"], "claude")
        self.assertEqual(routed["routed_from"], "codex")
        self.assertIn("70", detail)

    def test_campaign_fallback_requires_committed_manifest_reroute(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        manifest = self._manifest("C:/repo")
        manifest["mode"] = "campaign"
        mission = manifest["missions"][0]
        mission.update({
            "objective_id": "OBJ-1",
            "role": "verifier",
            "wave": 1,
            "machine": "yoga-book",
            "quota_pool": "codex",
        })
        status = {"missions": [{"id": mission["id"], "status": "missing-receipt"}]}
        with patch.object(self.planner, "validate_manifest", return_value={"valid": True}), \
             patch.object(self.planner, "status", return_value=status), \
             patch.object(self.planner, "active_wave", return_value=1), \
             patch.object(runner, "local_machine_id", return_value="yoga-book"), \
             patch.object(runner, "current_branch", return_value=mission["branch"]), \
             patch.object(runner, "disk_free_gb", return_value=60.0), \
             patch.object(runner, "memory_percent", return_value=50.0), \
             patch.object(runner, "is_clean", return_value=True), \
             patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}), \
             patch.object(runner, "subscription_usage", return_value={
                 "codex": {"remaining_percent": 2},
                 "claude": {"remaining_percent": 70},
             }):
            result = runner.prepare(manifest)
        row = result["missions"][0]
        self.assertEqual(row["action"], "requires-manifest-reroute")
        self.assertEqual(row["agent"], "codex")
        self.assertEqual(row["recommended_agent"], "claude")
        self.assertNotIn("argv", row)

    def test_version_two_fallback_requires_committed_manifest_reroute(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        manifest = self._manifest("C:/repo")
        mission = manifest["missions"][0]
        status = {"missions": [{"id": mission["id"], "status": "missing-receipt"}]}
        with patch.object(self.planner, "validate_manifest", return_value={"valid": True}), \
             patch.object(self.planner, "status", return_value=status), \
             patch.object(self.planner, "active_wave", return_value=1), \
             patch.object(runner, "current_branch", return_value=mission["branch"]), \
             patch.object(runner, "disk_free_gb", return_value=60.0), \
             patch.object(runner, "memory_percent", return_value=50.0), \
             patch.object(runner, "is_clean", return_value=True), \
             patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}), \
             patch.object(runner, "subscription_usage", return_value={
                 "codex": {"remaining_percent": 2},
                 "claude": {"remaining_percent": 70},
             }):
            result = runner.prepare(manifest)
        row = result["missions"][0]
        self.assertEqual(row["action"], "requires-manifest-reroute")
        self.assertEqual(row["agent"], "codex")
        self.assertEqual(row["recommended_agent"], "claude")
        self.assertNotIn("argv", row)

    def test_execution_leases_block_concurrent_machine_or_worktree_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = NightRunner(self.planner, state_dir=Path(tmp) / "state-1")
            second = NightRunner(self.planner, state_dir=Path(tmp) / "state-2")
            machine = f"test-{Path(tmp).name.lower()}"
            with patch("fleet.night_runner.Path.home", return_value=Path(tmp)):
                with first.execution_leases(machine, tmp):
                    with self.assertRaisesRegex(RunnerError, "execution lease unavailable"):
                        with second.execution_leases(machine, tmp):
                            self.fail("concurrent runner acquired an active lease")
                with second.execution_leases(machine, tmp):
                    pass

    def test_campaign_mission_is_queued_on_wrong_machine(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        manifest = self._manifest("C:/repo")
        manifest["mode"] = "campaign"
        mission = manifest["missions"][0]
        mission.update({
            "objective_id": "OBJ-1",
            "role": "maker",
            "wave": 1,
            "machine": "c940",
            "quota_pool": "codex",
        })
        status = {"missions": [{"id": mission["id"], "status": "missing-receipt"}]}
        with patch.object(self.planner, "validate_manifest", return_value={"valid": True}), \
             patch.object(self.planner, "status", return_value=status), \
             patch.object(self.planner, "active_wave", return_value=1), \
             patch.object(runner, "local_machine_id", return_value="yoga-book"), \
             patch.object(runner, "subscription_usage", return_value={}):
            result = runner.prepare(manifest)
        row = result["missions"][0]
        self.assertEqual(row["action"], "queued-machine")
        self.assertEqual(row["machine"], "c940")
        self.assertEqual(row["local_machine"], "yoga-book")

    def test_verifier_route_excludes_effective_maker_agent(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        mission = self._manifest("C:/repo")["missions"][0]
        mission.update({"agent": "claude", "quota_pool": "claude", "model": "opus"})
        with patch.object(
            runner,
            "agent_health",
            return_value={"ready": True, "detail": "live"},
        ):
            routed, _, _ = runner._route_mission(
                mission,
                {"claude": {"remaining_percent": 70}},
                {"claude"},
                {},
            )
        self.assertEqual(routed["agent"], "agy")
        self.assertNotEqual(routed["agent"], "claude")

    def test_dcode_is_blocked_without_metered_approval(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        self.planner.config["fallbacks"]["dcode"] = []
        mission = self._manifest("C:/repo")["missions"][0]
        mission.update({"agent": "dcode", "quota_pool": "metered-api", "model": "openai"})
        with patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}):
            with self.assertRaisesRegex(RunnerError, "explicit approval"):
                runner._route_mission(mission, {}, set(), {})

    def test_dcode_approval_still_fails_closed_without_enforceable_hard_cap(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        self.planner.config["fallbacks"]["dcode"] = []
        mission = self._manifest("C:/repo")["missions"][0]
        mission.update({
            "agent": "dcode",
            "quota_pool": "metered-api",
            "model": "openai",
            "metered_spend_approval": {
                "approval_id": "human:approval-002",
                "approved": True,
                "provider": "dcode",
                "quota_pool": "metered-api",
                "currency": "USD",
                "max_spend_usd": 10,
                "expires_at": "2099-01-01T00:00:00+00:00",
            },
        })
        with patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}):
            with self.assertRaisesRegex(RunnerError, "no enforceable hard spend cap"):
                runner._route_mission(mission, {}, set(), {})

    def test_zero_percent_measured_quota_is_blocked(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        self.planner.config["fallbacks"]["gemini"] = []
        mission = self._manifest("C:/repo")["missions"][0]
        mission.update({
            "agent": "gemini",
            "quota_pool": "gemini",
            "model": "gemini-2.5-pro",
            "role": "verifier",
        })
        usage = {"gemini": {"remaining_percent": 0}}
        with patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}):
            with self.assertRaisesRegex(RunnerError, "0% remaining"):
                runner._route_mission(mission, usage, set(), {})

    def test_runner_fallback_respects_role_constraints(self):
        runner = NightRunner(self.planner, state_dir=Path("state"))
        mission = self._manifest("C:/repo")["missions"][0]
        mission.update({"agent": "grok", "quota_pool": "grok", "model": "grok-4.5", "role": "maker"})
        with patch.object(runner, "agent_health", return_value={"ready": True, "detail": "live"}):
            routed, _, _ = runner._route_mission(
                mission,
                {"grok": {"remaining_percent": 70}, "claude": {"remaining_percent": 70}},
                {"grok", "claude"},
                {},
            )
        self.assertEqual("agy", routed["agent"])

    def _manifest(self, tmp: str):
        return {
            "version": 2, "date": "2026-07-17", "mode": "night", "total_budget_usd": 30,
            "missions": [{
                "id": "N1", "agent": "codex", "role": "maker", "model": "gpt-5.6-terra",
                "repo": tmp, "branch": "night/2026-07-17-test",
                "budget_usd": 30, "max_turns": 20, "timeout_minutes": 60,
                "task": "Fix safely", "why": "mechanical",
                "report": "reports/n1.md",
                "receipt": "receipts/n1.json",
                "required_artifacts": ["artifacts/output.txt"],
                "verification_ids": ["unit"],
                "acceptance_commands": ["python -m unittest discover -v"],
            }],
        }


if __name__ == "__main__":
    unittest.main()
