from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from scripts.queue_reconcile import (
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


if __name__ == "__main__":
    unittest.main()
