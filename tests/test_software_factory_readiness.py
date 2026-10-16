"""Evidence-gap checks are deliberately separate from live release attestation."""
import copy
import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.software_factory_readiness import assess_site, assess_capacity, make_packet, main, QUALITY_GATES


NOW = datetime(2026, 10, 16, 1, 0, tzinfo=timezone.utc)
SHA = "a" * 40
SITE = {"domain": "example.org", "repository": "example/site", "customer_result": "An editable, recoverable artifact", "team": "creation"}


def proof():
    receipt = {"result": "pass", "revision": SHA, "observed_at": NOW.isoformat(), "uri": "https://github.com/example/site/actions/runs/1"}
    checks = {gate: dict(receipt) for gate in QUALITY_GATES}
    checks["independent_review"].update(provider="review-provider", evaluator="reviewer")
    checks["cost"].update(actual_cost_usd=0.03)
    return {"source_revision": SHA, "builder": "maker", "builder_provider": "build-provider", "checks": checks,
            "deployment": {"state": "READY", "target": "production", "revision": SHA, "url": "https://example.org", "observed_at": NOW.isoformat()},
            "production_journey": dict(receipt)}


class FactoryReadinessTests(unittest.TestCase):
    def test_empty_receipts_cannot_be_green(self):
        result = assess_site(SITE, {}, NOW)
        self.assertEqual(result["supplied_evidence_state"], "incomplete")
        self.assertGreater(len(result["missing_or_invalid"]), 5)

    def test_complete_fixture_remains_unattested(self):
        result = assess_site(SITE, proof(), NOW)
        self.assertEqual(result["supplied_evidence_state"], "complete")
        self.assertEqual(result["production_verification"], "not_performed_by_this_tool")
        self.assertEqual(result["dispatch_state"], "not_dispatched")

    def test_preview_ready_is_not_production(self):
        data = proof()
        data["deployment"]["target"] = "preview"
        self.assertIn("production deployment", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_revision_change_invalidates_existing_review(self):
        data = proof()
        data["checks"]["independent_review"]["revision"] = "b" * 40
        self.assertIn("independent_review", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_deployed_revision_must_match_source(self):
        data = proof()
        data["deployment"]["revision"] = "b" * 40
        self.assertIn("production deployment", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_same_provider_review_does_not_meet_independent_provider_gate(self):
        data = proof()
        data["checks"]["independent_review"]["provider"] = data["builder_provider"]
        self.assertIn("independent provider identity", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_self_evaluation_does_not_meet_gate(self):
        for name in ("maker", "self", "worker", "queen", "unknown"):
            with self.subTest(name=name):
                data = proof()
                data["checks"]["independent_review"]["evaluator"] = name
                self.assertIn("independent evaluator identity", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_evaluator_object_is_not_an_identity(self):
        data = proof()
        data["checks"]["independent_review"]["evaluator"] = {"name": "reviewer"}
        self.assertIn("independent evaluator identity", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_skipped_ci_cannot_satisfy_release(self):
        data = proof()
        data["checks"]["ci"]["result"] = "skipped"
        self.assertIn("ci", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_missing_cost_is_unknown_not_zero(self):
        data = proof()
        data["checks"]["cost"].pop("actual_cost_usd")
        self.assertIn("measured cost", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_stale_future_and_naive_timestamps_refuse(self):
        for stamp in ((NOW - timedelta(hours=25)).isoformat(), (NOW + timedelta(minutes=2)).isoformat(), "2026-10-16T01:00:00"):
            with self.subTest(stamp=stamp):
                data = proof()
                data["checks"]["workflow"]["observed_at"] = stamp
                self.assertIn("workflow", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_credential_bearing_evidence_url_refuses(self):
        data = proof()
        data["checks"]["workflow"]["uri"] = "https://token@example.org/proof"
        self.assertIn("workflow", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_wrong_domain_journey_refuses(self):
        data = proof()
        data["production_journey"]["domain"] = "other.org"
        self.assertIn("production customer journey", assess_site(SITE, data, NOW)["missing_or_invalid"])

    def test_supplied_evidence_is_not_mutated(self):
        data = proof()
        before = copy.deepcopy(data)
        assess_site(SITE, data, NOW)
        self.assertEqual(data, before)

    def test_capacity_honors_disk_even_when_pp_reports_allow(self):
        report = {"timestamp": NOW.isoformat(), "decision": "allow", "disk_free_pct": 7.36, "disk_free_gib": 70}
        self.assertEqual(assess_capacity(report, NOW)["state"], "hold")

    def test_capacity_ignores_expired_allow(self):
        report = {"timestamp": (NOW - timedelta(minutes=16)).isoformat(), "decision": "allow", "disk_free_pct": 12, "disk_free_gib": 114}
        self.assertEqual(assess_capacity(report, NOW)["state"], "unknown")

    def test_packet_uses_existing_mission_envelope_and_is_held(self):
        packet = make_packet(SITE)
        self.assertEqual(packet["schema"], "run-envelope/v1")
        self.assertEqual(packet["status"], "held")
        self.assertEqual(packet["budget"]["metered_usd_cap"], 0)
        self.assertEqual(packet["scope"]["path_scope"], [])
        self.assertIsNone(packet["autonomy"]["effective"])
        self.assertIn("no execution authority", packet["stop_conditions"])

    def test_capacity_rejects_impossible_percentage(self):
        data = {"timestamp": NOW.isoformat(), "decision": "allow", "disk_free_pct": 101, "disk_free_gib": 114}
        self.assertEqual(assess_capacity(data, NOW)["state"], "unknown")

    def test_cli_rejects_bad_and_duplicate_catalogs(self):
        for content in ("{broken", '{"sites":[]}', json.dumps({"sites": [SITE, SITE]})):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "catalog.json"
                path.write_text(content, encoding="utf-8")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(["--catalog", str(path)])
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(output.getvalue())["state"], "unknown")

    def test_cli_never_runs_unknown_domain_packet(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps({"sites": [SITE]}), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["--catalog", str(path), "--packet", "other.org"])
            self.assertEqual(code, 2)
            self.assertIn("not in the inspected catalog", output.getvalue())


if __name__ == "__main__":
    unittest.main()
