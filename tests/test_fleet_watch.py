import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from scripts import fleet_watch
from scripts.fleet_watch import LAST_SWEEP_RE
from scripts.queue_reconcile import is_retired, item_is_expired, validate_queue_document

NOW = datetime(2026, 8, 14, 12, 0, tzinfo=timezone.utc)


class ItemTtlTests(unittest.TestCase):
    def test_expires_at_in_past_is_expired(self) -> None:
        self.assertTrue(item_is_expired({"expires_at": "2026-08-01T00:00:00Z"}, now=NOW))

    def test_expires_at_in_future_is_not_expired(self) -> None:
        self.assertFalse(item_is_expired({"expires_at": "2026-09-01T00:00:00Z"}, now=NOW))

    def test_unparseable_expires_at_fails_closed(self) -> None:
        self.assertTrue(item_is_expired({"expires_at": "not-a-time"}, now=NOW))

    def test_ttl_hours_with_fresh_anchor_is_not_expired(self) -> None:
        item = {"ttl_hours": 48, "issued_at": (NOW - timedelta(hours=12)).isoformat()}
        self.assertFalse(item_is_expired(item, now=NOW))

    def test_ttl_hours_past_anchor_is_expired(self) -> None:
        item = {"ttl_hours": 6, "issued_at": (NOW - timedelta(hours=12)).isoformat()}
        self.assertTrue(item_is_expired(item, now=NOW))

    def test_ttl_hours_without_anchor_fails_closed(self) -> None:
        self.assertTrue(item_is_expired({"ttl_hours": 6}, now=NOW))

    def test_no_ttl_fields_is_not_expired_here(self) -> None:
        # Absence of TTL is judged by require_ttl in validate, not here.
        self.assertFalse(item_is_expired({"id": "X"}, now=NOW))


class ValidateTtlTests(unittest.TestCase):
    def test_require_ttl_flags_missing_ttl(self) -> None:
        doc = {"active": [{"id": "A", "status": "queued"}], "historical": []}
        errors = validate_queue_document(doc, require_ttl=True, now=NOW)
        self.assertTrue(any("missing ttl" in e for e in errors), errors)

    def test_require_ttl_off_keeps_prior_behavior(self) -> None:
        doc = {"active": [{"id": "A", "status": "queued"}], "historical": []}
        self.assertEqual([], validate_queue_document(doc, now=NOW))

    def test_expired_active_item_is_an_error_even_without_require_ttl(self) -> None:
        doc = {
            "active": [
                {"id": "A", "status": "queued", "expires_at": "2026-08-01T00:00:00Z"}
            ],
            "historical": [],
        }
        errors = validate_queue_document(doc, now=NOW)
        self.assertTrue(any("ttl expired" in e for e in errors), errors)

    def test_fresh_ttl_item_passes_with_require_ttl(self) -> None:
        doc = {
            "active": [
                {
                    "id": "A",
                    "status": "queued",
                    "ttl_hours": 72,
                    "issued_at": (NOW - timedelta(hours=1)).isoformat(),
                }
            ],
            "historical": [],
        }
        self.assertEqual([], validate_queue_document(doc, require_ttl=True, now=NOW))


class RetiredHeartbeatTests(unittest.TestCase):
    def test_retired_machine_is_retired(self) -> None:
        beat = {"status": "retired", "retired_at": "2026-09-19T00:00:00Z"}
        self.assertTrue(is_retired(beat))

    def test_decommissioned_is_also_retired(self) -> None:
        beat = {"status": "decommissioned", "retired_at": "2026-09-19T00:00:00Z"}
        self.assertTrue(is_retired(beat))

    def test_retired_without_stamp_is_not_retired(self) -> None:
        # Silence must not retire a machine: without a declared retired_at the
        # dead-man's switch keeps watching it.
        self.assertFalse(is_retired({"status": "retired"}))

    def test_live_machine_is_not_retired(self) -> None:
        beat = {"status": "live", "at": "2026-09-19T00:00:00Z"}
        self.assertFalse(is_retired(beat))

    def test_retired_machine_is_skipped_by_heartbeat_check(self) -> None:
        with tempfile.TemporaryDirectory(dir=fleet_watch.REPO_ROOT) as tmp:
            beats = Path(tmp)
            (beats / "retired-box.json").write_text(
                json.dumps(
                    {
                        "machine_id": "retired-box",
                        "status": "retired",
                        "retired_at": "2026-08-16T00:00:00Z",
                        "at": "2026-08-16T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(fleet_watch, "HEARTBEAT_DIR", beats):
                self.assertEqual([], fleet_watch.check_heartbeats(NOW, 24))

    def test_stale_live_machine_is_still_flagged(self) -> None:
        with tempfile.TemporaryDirectory(dir=fleet_watch.REPO_ROOT) as tmp:
            beats = Path(tmp)
            (beats / "dark-box.json").write_text(
                json.dumps(
                    {
                        "machine_id": "dark-box",
                        "status": "live",
                        "at": "2026-08-01T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(fleet_watch, "HEARTBEAT_DIR", beats):
                findings = fleet_watch.check_heartbeats(NOW, 24)
            self.assertTrue(any("dark-box" in f for f in findings), findings)


class LedgerHeaderTests(unittest.TestCase):
    def test_last_sweep_regex_matches_ledger_format(self) -> None:
        line = "**Last sweep:** 2026-08-10T00:35+02:00 (Queen 10h wave-2 start)"
        match = LAST_SWEEP_RE.search(line)
        assert match is not None
        parsed = datetime.fromisoformat(match.group(1))
        self.assertEqual(2026, parsed.year)


if __name__ == "__main__":
    unittest.main()
