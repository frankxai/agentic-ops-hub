import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fleet import usage_ingest
from fleet.token_planner import PlanLimits


class PlanLimitsTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.limits = PlanLimits.from_file(self.root / "fleet" / "plan_limits.json")

    def test_weekly_window_computed_across_reset_boundary(self):
        limits = self._pinned()  # anchor pinned to Monday 09:00 Europe/Berlin
        start, end = limits.weekly_window(datetime.fromisoformat("2026-08-24T08:59:00+02:00"))
        self.assertEqual(start.isoformat(), "2026-08-17T09:00:00+02:00")
        self.assertEqual(end.isoformat(), "2026-08-24T09:00:00+02:00")
        start, end = limits.weekly_window(datetime.fromisoformat("2026-08-24T09:00:00+02:00"))
        self.assertEqual(start.isoformat(), "2026-08-24T09:00:00+02:00")
        self.assertEqual(end - start, timedelta(days=7))

    def test_bucket_activity_excludes_records_before_weekly_reset(self):
        limits = self._pinned()
        now = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        stale = self._record("2026-08-24T08:00:00+02:00", "claude-sonnet-5-20260203", output_tokens=1000)
        fresh = self._record("2026-08-25T10:00:00+02:00", "claude-sonnet-5-20260203", output_tokens=1000)
        usage = limits.bucket_activity([stale, fresh], now)
        self.assertEqual(usage["buckets"]["sonnet"]["observed_ste"], 5000.0)  # output x5, sonnet weight 1.0
        self.assertEqual(usage["buckets"]["all_models"]["observed_ste"], 5000.0)
        self.assertEqual(usage["buckets"]["opus"]["observed_ste"], 0.0)

    def test_boost_multiplier_expires_after_2026_08_31(self):
        boosted_at = datetime(2026, 8, 28, 12, tzinfo=timezone.utc)
        flat_at = datetime(2026, 9, 2, 12, tzinfo=timezone.utc)
        self.assertEqual(self.limits.boost_multiplier(boosted_at), 1.5)
        self.assertEqual(self.limits.boost_multiplier(flat_at), 1.0)
        limits = self._pinned()
        rec = [self._record("2026-08-24T12:00:00+02:00", "claude-opus-5", output_tokens=100_000)]
        boosted = limits.bucket_activity(rec, boosted_at)["buckets"]["opus"]["activity_index"]
        rec = [self._record("2026-08-31T12:00:00+02:00", "claude-opus-5", output_tokens=100_000)]
        flat = limits.bucket_activity(rec, flat_at)["buckets"]["opus"]["activity_index"]
        self.assertAlmostEqual(boosted, flat / 1.5, places=4)  # more capacity -> lower index

    def test_weights_follow_output_price_ratios_normalized_to_sonnet(self):
        self.assertEqual(self.limits.weight_for("claude-haiku-4-5-20251001"), 0.5)
        self.assertEqual(self.limits.weight_for("claude-sonnet-5-20260203"), 1.0)
        self.assertEqual(self.limits.weight_for("claude-opus-5-20260115"), 2.5)
        self.assertEqual(self.limits.weight_for("claude-fable-5"), 5.0)
        self.assertEqual(self.limits.weight_for("claude-fable-5"), 2 * self.limits.weight_for("claude-opus-5"))

    def test_advise_honors_normal_routing_at_low_activity(self):
        decision = self.limits.advise(0.2, "deep-backend")
        self.assertEqual(decision["model"], "opus")
        self.assertEqual(decision["posture"], "normal")

    def test_advise_downtiers_noncritical_at_high_activity(self):
        self.assertEqual(self.limits.advise(0.5, "deep-backend")["model"], "opus")  # watch band still honors routing
        self.assertEqual(self.limits.advise(0.8, "deep-backend")["model"], "opus")  # class measurably needs its tier
        self.assertEqual(self.limits.advise(0.8, "refactor")["model"], "sonnet")
        self.assertEqual(self.limits.advise(0.8, "low-stakes")["model"], "haiku")
        stripped = self._pinned()
        stripped.config["advice"]["needs_expensive"] = []
        self.assertEqual(stripped.advise(0.8, "deep-backend")["model"], "sonnet")

    def test_advise_floors_everything_noncritical_at_capacity(self):
        self.assertEqual(self.limits.advise(0.95, "refactor")["model"], "haiku")
        self.assertEqual(self.limits.advise(0.95, "deep-backend")["model"], "sonnet")
        critical = self.limits.advise(0.95, "deep-backend", critical=True)
        self.assertEqual(critical["model"], "opus")
        self.assertEqual(critical["posture"], "floor")

    def test_session_window_is_five_hours_anchored_to_first_activity(self):
        limits = self._pinned()
        records = [self._record("2026-08-25T10:12:00+00:00", "claude-sonnet-5-20260203", output_tokens=1)]
        start, end = limits.session_window(datetime.fromisoformat("2026-08-25T13:00:00+00:00"), records)
        self.assertEqual(start.isoformat(), "2026-08-25T10:00:00+00:00")
        self.assertEqual(end - start, timedelta(hours=5))
        start, _ = limits.session_window(datetime.fromisoformat("2026-08-25T18:30:00+00:00"), records)
        self.assertEqual(start.isoformat(), "2026-08-25T18:00:00+00:00")  # previous block expired

    def test_ingest_parses_jsonl_dedups_and_weights_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proj" / "s1.jsonl"
            path.parent.mkdir()
            sonnet = self._jsonl_line("msg_1", "req_1", "claude-sonnet-5-20260203", 100, 10)
            fable = self._jsonl_line("msg_2", "req_2", "claude-fable-5", 0, 10)
            noise = [json.dumps({"type": "user", "message": {"role": "user", "content": "hi"}}), "not json {"]
            path.write_text("\n".join([sonnet, sonnet, fable] + noise), encoding="utf-8")
            records = usage_ingest.records_from_jsonl(Path(tmp))
            self.assertEqual(len(records), 2)  # duplicate (msg_1, req_1) collapsed
            usage = self._pinned().bucket_activity(records, datetime.fromisoformat("2026-08-25T12:00:00+02:00"))
            self.assertEqual(usage["buckets"]["sonnet"]["observed_ste"], 150.0)  # (100 + 10*5) * 1.0
            self.assertEqual(usage["buckets"]["opus"]["observed_ste"], 250.0)  # (10*5) * 5.0 - fable meters here
            self.assertEqual(usage["buckets"]["all_models"]["observed_ste"], 400.0)

    def test_ingest_accepts_ccusage_daily_json(self):
        payload = {"daily": [{"date": "2026-08-25", "modelBreakdowns": [{
            "modelName": "claude-opus-5-20260115", "inputTokens": 10, "outputTokens": 2,
            "cacheCreationTokens": 4, "cacheReadTokens": 100,
        }]}]}
        records = usage_ingest.records_from_ccusage(payload)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["model"], "claude-opus-5-20260115")
        self.assertEqual(records[0]["cache_read_input_tokens"], 100)
        self.assertTrue(records[0]["timestamp"].startswith("2026-08-25"))

    def test_ingest_absent_session_data_exits_nonzero_with_plain_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = usage_ingest.main(["--projects-root", tmp])
            self.assertEqual(code, 2)
            self.assertIn("expected on a fresh container", stderr.getvalue())

    def test_unverified_reset_anchor_refuses_to_compute(self):
        from fleet.token_planner import PlannerError
        now = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        # the shipped file carries a placeholder anchor, never a usable default
        self.assertFalse(self.limits.reset_anchor_verified())
        with self.assertRaises(PlannerError) as ctx:
            self.limits.weekly_window(now)
        self.assertIn("Settings -> Usage", str(ctx.exception))

    def test_expired_model_facts_force_uncalibrated(self):
        limits = self._pinned()
        fresh = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        self.assertEqual(limits.facts_expired(fresh), [])
        stale_at = datetime.fromisoformat("2027-01-01T12:00:00+02:00")
        self.assertIn("weights", limits.facts_expired(stale_at))
        self.assertFalse(limits.calibration_status(stale_at)["calibrated"])

    def test_uncalibrated_state_is_advisory_only_and_never_auto_routes(self):
        limits = self._pinned()
        now = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        status = limits.calibration_status(now)
        self.assertFalse(status["calibrated"])  # zero observations recorded
        self.assertTrue(any("observations" in r for r in status["blockers"]))
        decision = limits.advise(0.2, "deep-backend", calibrated=status["calibrated"])
        self.assertTrue(decision["advisory_only"])
        self.assertFalse(decision["auto_route"])
        self.assertIn("ADVISORY ONLY", decision["reason"])

    def test_activity_index_carries_an_interval_matching_published_range_width(self):
        limits = self._pinned()
        now = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        rec = [self._record("2026-08-25T10:00:00+02:00", "claude-opus-5", output_tokens=10_000_000)]
        opus = limits.bucket_activity(rec, now)["buckets"]["opus"]
        low, high = opus["activity_index_interval"]
        self.assertLess(low, opus["activity_index"])
        self.assertGreater(high, opus["activity_index"])
        # interval ends come from the 24-40 h/week published range
        self.assertAlmostEqual(high / low, 40 / 24, places=2)
        self.assertFalse(opus["is_measurement"])

    def test_report_never_claims_remaining_allowance(self):
        limits = self._pinned()
        now = datetime.fromisoformat("2026-08-26T12:00:00+02:00")
        blob = json.dumps(limits.bucket_activity([], now)).lower()
        for banned in ("remaining_fraction", "remaining allowance", "percent remaining"):
            self.assertNotIn(banned, blob)
        self.assertIn("not remaining plan allowance", blob)

    def _pinned(self):
        config = json.loads((self.root / "fleet" / "plan_limits.json").read_text(encoding="utf-8"))
        config["weekly_reset"] = {
            "weekday": "monday", "hour": 9, "timezone": "Europe/Berlin",
            "confidence": "verified",
        }
        return PlanLimits(config)

    def _record(self, timestamp, model, input_tokens=0, output_tokens=0, cache_creation=0, cache_read=0):
        return {
            "timestamp": timestamp, "model": model,
            "input_tokens": input_tokens, "output_tokens": output_tokens,
            "cache_creation_input_tokens": cache_creation, "cache_read_input_tokens": cache_read,
        }

    def _jsonl_line(self, message_id, request_id, model, input_tokens, output_tokens):
        return json.dumps({
            "type": "assistant", "timestamp": "2026-08-25T09:00:00.000Z", "requestId": request_id,
            "message": {"id": message_id, "model": model, "usage": {
                "input_tokens": input_tokens, "output_tokens": output_tokens,
                "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
            }},
        })


if __name__ == "__main__":
    unittest.main()
