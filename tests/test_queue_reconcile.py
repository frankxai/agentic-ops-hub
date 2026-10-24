from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from scripts.queue_reconcile import (
    is_retired,
    item_is_expired,
    heartbeat_is_fresh,
    move_active_to_historical,
    source_pr_blocks_active,
    validate_queue_document,
)


class QueueReconcileTests(unittest.TestCase):
    def test_source_pr_merged_blocks_active_item(self) -> None:
        item = {"id": "BOOK-CLI-20260717", "status": "queued", "source_pr": 326}
        self.assertTrue(source_pr_blocks_active(item, "MERGED"))
        self.assertTrue(source_pr_blocks_active(item, "closed"))
        self.assertFalse(source_pr_blocks_active(item, "OPEN"))
        self.assertFalse(source_pr_blocks_active({**item, "status": "delivered"}, "MERGED"))

    def test_validate_rejects_active_item_with_closed_source_pr(self) -> None:
        doc = {
            "active": [
                {
                    "id": "BOOK-CLI-20260717",
                    "status": "queued",
                    "source_pr": 326,
                }
            ],
            "historical": [],
        }
        errors = validate_queue_document(doc, pr_states={326: "CLOSED"})
        self.assertTrue(any("source_pr #326 is CLOSED" in e for e in errors))

    def test_validate_rejects_stale_peer_for_remote_dispatch(self) -> None:
        now = datetime(2026, 8, 7, 15, 0, tzinfo=timezone.utc)
        doc = {"active": [{"id": "X", "status": "queued"}], "historical": []}
        stale = {
            "machine_id": "yoga-book",
            "status": "live",
            "at": (now - timedelta(days=20)).isoformat(),
        }
        errors = validate_queue_document(
            doc,
            peer_heartbeat=stale,
            require_fresh_peer_for_remote=True,
            now=now,
            max_age_hours=24,
        )
        self.assertTrue(any("remote dispatch blocked" in e for e in errors))
        self.assertFalse(heartbeat_is_fresh(stale, now=now, max_age_hours=24))

    def test_move_active_to_historical_is_idempotent_on_ids(self) -> None:
        doc = {
            "version": 2,
            "active": [
                {
                    "id": "C940-CLI-MAX-20260717",
                    "status": "in-progress",
                    "branch": "agent/c940/cli-fleet-maximize",
                }
            ],
            "historical": [{"id": "B1", "status": "delivered", "evidence": "d10d81c"}],
        }
        out = move_active_to_historical(
            doc,
            "C940-CLI-MAX-20260717",
            terminal_status="integrated",
            evidence="PR #19 merged as 455b4e1",
            updated_at="2026-08-07T15:45:00+00:00",
        )
        self.assertEqual([], out["active"])
        ids = [h["id"] for h in out["historical"]]
        self.assertEqual(1, ids.count("C940-CLI-MAX-20260717"))
        self.assertIn("B1", ids)
        errors = validate_queue_document(out, pr_states={})
        self.assertEqual([], errors)

    def test_duplicate_ids_are_rejected(self) -> None:
        doc = {
            "active": [{"id": "A", "status": "queued"}],
            "historical": [{"id": "A", "status": "delivered", "evidence": "x"}],
        }
        errors = validate_queue_document(doc)
        self.assertTrue(any("duplicate queue_item_id: A" in e for e in errors))


    def test_is_retired_requires_status_and_time(self) -> None:
        self.assertFalse(is_retired(None))
        self.assertFalse(is_retired({"status": "live"}))
        self.assertFalse(is_retired({"status": "retired"}))  # Missing time
        self.assertFalse(is_retired({"status": "retired", "retired_at": "invalid"}))
        self.assertTrue(is_retired({"status": "retired", "retired_at": "2026-08-01T12:00:00Z"}))
        self.assertTrue(is_retired({"status": "decommissioned", "retired_at": "2026-08-01T12:00:00Z"}))

    def test_item_is_expired_with_expires_at(self) -> None:
        now = datetime(2026, 8, 7, 15, 0, tzinfo=timezone.utc)
        self.assertFalse(item_is_expired({"expires_at": "2026-08-08T15:00:00Z"}, now=now))
        self.assertTrue(item_is_expired({"expires_at": "2026-08-06T15:00:00Z"}, now=now))

    def test_item_is_expired_with_ttl_hours(self) -> None:
        now = datetime(2026, 8, 7, 15, 0, tzinfo=timezone.utc)
        self.assertFalse(item_is_expired({}, now=now))  # No TTL info
        # Anchor updated_at
        self.assertFalse(item_is_expired({"updated_at": "2026-08-07T10:00:00Z", "ttl_hours": 24}, now=now))
        self.assertTrue(item_is_expired({"updated_at": "2026-08-06T10:00:00Z", "ttl_hours": 24}, now=now))
        # Anchor issued_at
        self.assertFalse(item_is_expired({"issued_at": "2026-08-07T10:00:00Z", "ttl_hours": 24}, now=now))
        self.assertTrue(item_is_expired({"issued_at": "2026-08-06T10:00:00Z", "ttl_hours": 24}, now=now))
        # Unparseable ttl counts as expired
        self.assertTrue(item_is_expired({"updated_at": "2026-08-07T10:00:00Z", "ttl_hours": "invalid"}, now=now))

    def test_move_active_to_historical_raises_on_missing_item(self) -> None:
        doc = {"active": [], "historical": []}
        with self.assertRaises(KeyError):
            move_active_to_historical(doc, "MISSING", terminal_status="delivered", evidence="x")

    def test_move_active_to_historical_raises_on_invalid_status(self) -> None:
        doc = {"active": [{"id": "A", "status": "queued"}], "historical": []}
        with self.assertRaises(ValueError):
            move_active_to_historical(doc, "A", terminal_status="active", evidence="x")

if __name__ == "__main__":
    unittest.main()
