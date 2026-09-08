from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
import tempfile
from pathlib import Path

from fleet.token_planner import Planner, PlannerError


class DailyTokenPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.planner = Planner.from_file(root / "fleet" / "model-routing.json")
        self.registry = {
            "policy": {"max_top_level_objectives_per_campaign": 3},
            "objectives": [
                {
                    "id": "OBJ-FLEET-DELIVERY",
                    "repo": "agentic-ops-hub",
                    "priority": "tier-0",
                    "executive_owner": "CIO",
                    "outcome": "Repeatable governed agent delivery",
                    "success_metric": "A campaign yields objective-linked verified receipts.",
                }
            ],
        }

    def _request(self) -> dict:
        return {
            "date": "2026-07-17",
            "timezone": "Europe/Amsterdam",
            "machine_status": {"yoga-book": "online", "c940": "online"},
            "cli_health": {
                "claude": "ready",
                "codex": "ready",
                "gemini": "ready",
                "grok": "ready",
                "agy": "ready",
                "opencode": "blocked-live-auth",
                "dcode": "ready",
            },
            "objectives": [
                {
                    "id": "OBJ-FLEET-DELIVERY",
                    "job_class": "deep-backend",
                    "priority_score": 100,
                    "maker_minutes": 60,
                    "verifier_minutes": 30,
                    "artifact_contract": "tested planner plus machine-readable daily plan",
                }
            ],
        }

    @staticmethod
    def _usage() -> dict:
        return {
            "claude": {"remaining_percent": 80, "reset_at": "2026-07-18T08:00:00+02:00"},
            "codex": {"remaining_percent": 75, "reset_at": "2026-07-18T09:00:00+02:00"},
            "gemini": {"remaining_percent": 70},
            "grok": {"remaining_percent": 60},
        }

    def test_daily_plan_starts_from_objective_and_separates_verifier(self) -> None:
        plan = self.planner.plan_day(
            self._request(), self.registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        self.assertEqual(2, len(plan["lanes"]))
        maker, verifier = plan["lanes"]
        self.assertEqual("OBJ-FLEET-DELIVERY", maker["objective_id"])
        self.assertEqual("maker", maker["role"])
        self.assertEqual("claude", maker["agent"])
        self.assertEqual("verifier", verifier["role"])
        self.assertEqual("codex", verifier["agent"])
        self.assertNotEqual(maker["agent"], verifier["agent"])
        self.assertGreaterEqual(verifier["start_at"], maker["end_at"])
        self.assertEqual("compile into a version-3 campaign mission before execution", maker["next_contract"])

    def test_capacity_summary_includes_every_cli_and_keeps_reserve(self) -> None:
        summary = self.planner.capacity_summary(self._usage())
        self.assertEqual(
            {"codex", "claude", "gemini", "grok", "agy", "opencode", "dcode", "hermes"},
            set(summary),
        )
        self.assertEqual(65.0, summary["claude"]["usable_percent"])
        self.assertEqual(55.25, summary["claude"]["target_spend_percent"])
        self.assertEqual("control-only", summary["hermes"]["status"])
        self.assertEqual("metered-blocked", summary["dcode"]["status"])

    def test_capacity_summary_rejects_nonfinite_quota(self):
        for value in (float("nan"), float("inf"), float("-inf"), -1, 101):
            with self.subTest(value=value):
                summary = self.planner.capacity_summary(
                    {"claude": {"remaining_percent": value}}
                )
                self.assertEqual(summary["claude"]["status"], "invalid")
                self.assertIsNone(summary["claude"]["remaining_percent"])
                self.assertIsNone(summary["claude"]["target_spend_percent"])

    def test_low_quota_pool_is_not_scheduled_below_reserve(self) -> None:
        request = self._request()
        request["objectives"][0]["job_class"] = "refactor"
        usage = self._usage()
        usage["codex"]["remaining_percent"] = 16
        plan = self.planner.plan_day(
            request, self.registry, usage, [], now="2026-07-17T08:00:00+02:00"
        )
        makers = [lane for lane in plan["lanes"] if lane["role"] == "maker"]
        self.assertTrue(makers)
        self.assertNotEqual("codex", makers[0]["agent"])
        self.assertEqual(0.85, plan["capacity"]["codex"]["target_spend_percent"])

    def test_forecast_learns_only_from_verified_artifact_receipts(self) -> None:
        history = [
            self._observation(10, 6, 40, "VERIFIED", 4),
            self._observation(20, 12, 80, "VERIFIED", 3),
            self._observation(30, 24, 60, "VERIFIED", 2),
            self._observation(40, 20, 10, "FAILED", 0),
        ]
        forecast = self.planner.capacity_forecast(
            history, agent="codex", job_class="refactor", role="maker"
        )
        self.assertEqual(3, forecast["sample_count"])
        self.assertEqual(3, forecast["verified_count"])
        self.assertEqual(1.0, forecast["success_rate"])
        self.assertEqual(6.0, forecast["predicted_quota_delta_percent"])
        self.assertEqual(60, forecast["predicted_duration_minutes"])
        self.assertEqual("medium", forecast["confidence"])

    def test_normalized_quota_keeps_reset_but_drops_identity(self) -> None:
        payload = [{
            "provider": "Claude",
            "plan": "Max",
            "email": "private@example.com",
            "metrics": [
                {"remaining_percent": 90, "reset_at": "2026-07-18T09:00:00Z"},
                {"remaining_percent": 65, "reset_at": "2026-07-18T08:00:00Z"},
            ],
        }]
        usage = self.planner.normalize_quota_payload(payload)
        self.assertEqual(65, usage["claude"]["remaining_percent"])
        self.assertEqual("2026-07-18T08:00:00Z", usage["claude"]["reset_at"])
        self.assertNotIn("email", usage["claude"])

    def test_cli_capacity_report_maps_directly_into_planner_health(self) -> None:
        report = {
            "resource_gate": {"launch_allowed": True},
            "subscription_clis": {
                "claude-max": {"status": "ready"},
                "openai-codex-max": {"status": "blocked-live-auth"},
                "gemini-ultra": {"status": "auth-missing"},
                "grok-heavy": {"status": "ready"},
                "agy": {"status": "auth-declared-unverified"},
                "opencode": {"status": "auth-missing"},
                "dcode-metered": {"status": "metered-disabled"},
            },
        }
        health = self.planner.normalize_cli_health(report)
        self.assertEqual("ready", health["claude"])
        self.assertEqual("blocked-live-auth", health["codex"])
        self.assertEqual("ready", health["grok"])
        self.assertEqual("control-ready", health["hermes"])

    def test_machine_capacity_reports_apply_resource_gate_per_machine(self) -> None:
        blocked = {
            "machine_id": "yoga-book",
            "resource_gate": {"launch_allowed": False},
            "subscription_clis": {"claude-max": {"status": "ready"}},
        }
        ready = {
            "machine_id": "c940",
            "resource_gate": {"launch_allowed": True},
            "subscription_clis": {"claude-max": {"status": "ready"}},
        }
        health = self.planner.normalize_cli_health_by_machine([blocked, ready])
        self.assertEqual("blocked-resource", health["yoga-book"]["claude"])
        self.assertEqual("ready", health["c940"]["claude"])

    def test_private_identity_is_rejected_from_learning_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, observation = self._verified_observation_context(tmp)
            observation["email"] = "private@example.com"
            with self.assertRaisesRegex(PlannerError, "private identity"):
                self.planner.validate_observation(observation, manifest)

    def test_observation_schema_requires_bound_receipt_and_rejects_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, observation = self._verified_observation_context(tmp)
            receipt_id = observation.pop("receipt_id")
            with self.assertRaisesRegex(PlannerError, "receipt_id"):
                self.planner.validate_observation(observation, manifest)
            observation["receipt_id"] = receipt_id
            observation["session_id"] = "private"
            with self.assertRaisesRegex(PlannerError, "unsupported fields"):
                self.planner.validate_observation(observation, manifest)

    def test_observation_rejects_unbound_or_forged_receipt_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, observation = self._verified_observation_context(tmp)
            with self.assertRaisesRegex(PlannerError, "verified campaign manifest"):
                self.planner.validate_observation(observation)
            observation["job_class"] = "orchestration"
            with self.assertRaisesRegex(PlannerError, "job_class does not match"):
                self.planner.validate_observation(observation, manifest)
            observation["job_class"] = "refactor"
            observation["receipt_sha256"] = "0" * 64
            observation["receipt_id"] = f"sha256:{'0' * 64}"
            with self.assertRaisesRegex(PlannerError, "does not match receipt bytes"):
                self.planner.validate_observation(observation, manifest)

    def test_observation_recording_is_idempotent_by_verified_receipt_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, observation = self._verified_observation_context(tmp)
            path = Path(tmp) / "history.jsonl"
            first = self.planner.record_observation(path, observation, manifest)
            second = self.planner.record_observation(path, observation, manifest)
            self.assertTrue(first["recorded"])
            self.assertFalse(second["recorded"])
            self.assertEqual(1, len(path.read_text(encoding="utf-8").splitlines()))

    def test_duplicate_objective_ids_are_rejected(self) -> None:
        request = self._request()
        request["objectives"].append(dict(request["objectives"][0]))
        with self.assertRaisesRegex(PlannerError, "duplicate"):
            self.planner.plan_day(request, self.registry, self._usage(), [])

    def test_same_repo_writer_lanes_are_serialized(self) -> None:
        registry = dict(self.registry)
        registry["objectives"] = [
            self.registry["objectives"][0],
            {**self.registry["objectives"][0], "id": "OBJ-FLEET-SECOND"},
        ]
        request = self._request()
        request["objectives"].append({
            **request["objectives"][0],
            "id": "OBJ-FLEET-SECOND",
            "job_class": "refactor",
        })
        plan = self.planner.plan_day(
            request, registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        repo_lanes = sorted(plan["lanes"], key=lambda lane: lane["start_at"])
        self.assertEqual(4, len(repo_lanes))
        for previous, current in zip(repo_lanes, repo_lanes[1:]):
            self.assertGreaterEqual(current["start_at"], previous["end_at"])

    def test_fallback_respects_cli_role_constraints(self) -> None:
        request = self._request()
        request["objectives"][0]["job_class"] = "current-signal"
        request["cli_health"] = {"gemini": "ready", "agy": "ready"}
        self.planner.config["fallbacks"]["grok"] = ["gemini", "agy"]
        plan = self.planner.plan_day(
            request, self.registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        maker = next(lane for lane in plan["lanes"] if lane["role"] == "maker")
        self.assertEqual("agy", maker["agent"])

    def test_machine_specific_health_does_not_cross_machine_boundaries(self) -> None:
        request = self._request()
        request.pop("cli_health")
        request["cli_health_by_machine"] = {
            "yoga-book": {"claude": "ready"},
            "c940": {},
        }
        plan = self.planner.plan_day(
            request, self.registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        self.assertEqual("yoga-book", plan["lanes"][0]["machine"])
        request["cli_health_by_machine"] = {
            "yoga-book": {},
            "c940": {"claude": "ready", "codex": "ready"},
        }
        admitted = self.planner.plan_day(
            request, self.registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        self.assertEqual("claude", admitted["lanes"][0]["agent"])
        self.assertEqual("c940", admitted["lanes"][0]["machine"])

    def test_unhealthy_cli_is_visible_but_not_admitted(self) -> None:
        request = self._request()
        request["cli_health"] = {}
        plan = self.planner.plan_day(
            request, self.registry, self._usage(), [], now="2026-07-17T08:00:00+02:00"
        )
        self.assertEqual([], plan["lanes"])
        self.assertTrue(plan["blocked"])
        self.assertIn("grok", plan["capacity"])
        self.assertIn("after every mission receipt", plan["replan_triggers"])

    def _verified_observation_context(self, tmp: str) -> tuple[dict, dict]:
        root = Path(tmp)
        branch = "agent/hermes/observation"
        subprocess.run(
            ["git", "init", "-b", branch],
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
        objective = {
            "id": "OBJ-OBSERVATION",
            "repo": "agentic-ops-hub",
            "executive_owner": "CTO",
            "outcome": "Verified capacity evidence",
            "success_metric": "A receipt-bound observation is recorded.",
        }
        (root / "objectives-registry.json").write_text(
            json.dumps({"schema_version": 1, "objectives": [objective]}),
            encoding="utf-8",
        )
        artifact = root / "artifacts" / "output.txt"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("verified output", encoding="utf-8")
        subprocess.run(
            ["git", "add", "artifacts/output.txt", "objectives-registry.json"],
            cwd=tmp,
            check=True,
        )
        subprocess.run(["git", "commit", "-m", "verified output"], cwd=tmp, capture_output=True, check=True)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp, text=True).strip()
        maker = {
            "id": "OBS-M1",
            "objective_id": objective["id"],
            "agent": "codex",
            "machine": "yoga-book",
            "quota_pool": "codex",
            "role": "maker",
            "job_class": "refactor",
            "wave": 1,
            "model": "gpt-5.6-terra",
            "repo": tmp,
            "branch": branch,
            "budget_usd": 10,
            "max_turns": 10,
            "timeout_minutes": 30,
            "task": "Produce the verified observation artifact safely.",
            "outcome": objective["outcome"],
            "report": "reports/observation.md",
            "receipt": "receipts/observation.json",
            "required_artifacts": ["artifacts/output.txt"],
            "verification_ids": ["unit"],
            "acceptance_commands": ["python -m unittest discover -v"],
        }
        verifier = {
            **maker,
            "id": "OBS-V1",
            "agent": "claude",
            "machine": "c940",
            "quota_pool": "claude",
            "role": "verifier",
            "wave": 2,
            "depends_on": [maker["id"]],
            "budget_usd": 5,
            "report": "reports/verifier.md",
            "receipt": "receipts/verifier.json",
            "required_artifacts": ["reports/verifier.md"],
        }
        manifest = {
            "version": 3,
            "date": "2026-07-17",
            "campaign_id": "observation-test",
            "mode": "campaign",
            "control_repo": tmp,
            "objective_registry": "objectives-registry.json",
            "total_budget_usd": 15,
            "max_concurrency": 1,
            "minimum_verified_outcomes": 1,
            "wave_budgets_usd": {"1": 10, "2": 5},
            "stop_conditions": ["test failure"],
            "objectives": [objective],
            "missions": [maker, verifier],
        }
        (root / "reports").mkdir()
        (root / "reports" / "observation.md").write_text("verified", encoding="utf-8")
        (root / "receipts").mkdir()
        receipt = root / maker["receipt"]
        receipt.write_text(json.dumps({
            "schema_version": 1,
            "mission_id": maker["id"],
            "objective_id": objective["id"],
            "role": maker["role"],
            "agent": maker["agent"],
            "machine": maker["machine"],
            "execution_status": "ok",
            "outcome_status": "VERIFIED",
            "status": "verified",
            "branch": maker["branch"],
            "commit": commit,
            "artifacts": maker["required_artifacts"],
            "verification": [{
                "id": "unit",
                "command": maker["acceptance_commands"][0],
                "exit_code": 0,
                "status": "passed",
            }],
            "integration_state": "pr_open",
            "completed_at": "2026-07-17T12:00:00+00:00",
        }), encoding="utf-8")
        digest = hashlib.sha256(receipt.read_bytes()).hexdigest()
        observation = self._observation(30, 24, 60, "VERIFIED", 3)
        observation.update({
            "mission_id": maker["id"],
            "receipt_path": maker["receipt"],
            "receipt_sha256": digest,
            "receipt_id": f"sha256:{digest}",
        })
        return manifest, observation

    @staticmethod
    def _observation(before: float, after: float, duration: int, status: str, score: int) -> dict:
        return {
            "observed_at": "2026-07-17T12:00:00Z",
            "agent": "codex",
            "job_class": "refactor",
            "role": "maker",
            "duration_minutes": duration,
            "outcome_status": status,
            "artifact_score": score,
            "quota_before_percent": before,
            "quota_after_percent": after,
            "receipt_id": "receipt-example",
        }


if __name__ == "__main__":
    unittest.main()
