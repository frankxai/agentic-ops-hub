import io
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from scripts.fleet_watch import (
    LAST_SWEEP_RE,
    build_comment_body,
    fingerprint_findings,
    fingerprint_from_comment_body,
    fingerprint_marker,
    last_automated_fingerprint,
    main,
    parse_paginated_json_arrays,
    should_comment,
    stabilize_text,
)
from scripts.queue_reconcile import item_is_expired, validate_queue_document

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


class LedgerHeaderTests(unittest.TestCase):
    def test_last_sweep_regex_matches_ledger_format(self) -> None:
        line = "**Last sweep:** 2026-08-10T00:35+02:00 (Queen 10h wave-2 start)"
        match = LAST_SWEEP_RE.search(line)
        assert match is not None
        parsed = datetime.fromisoformat(match.group(1))
        self.assertEqual(2026, parsed.year)


class FingerprintTests(unittest.TestCase):
    def test_sorted_and_timestamps_excluded(self) -> None:
        first = [
            "ops/OPS-LEDGER.md: Last sweep 2026-08-10T00:35+02:00 is older than 72h",
            "fleet/bus/heartbeats/c940.json: stale (at=2026-08-25T01:27:57+00:00, max_age_hours=24)",
        ]
        second = [
            "fleet/bus/heartbeats/c940.json: stale (at=2026-09-01T00:00:00+00:00, max_age_hours=24)",
            "ops/OPS-LEDGER.md: Last sweep 2026-09-01T00:00:00Z is older than 72h",
        ]
        self.assertEqual(fingerprint_findings(first), fingerprint_findings(second))

    def test_run_ids_excluded(self) -> None:
        self.assertEqual(
            fingerprint_findings(["failed /actions/runs/111"]),
            fingerprint_findings(["failed /actions/runs/222"]),
        )

    def test_added_finding_changes_fingerprint(self) -> None:
        self.assertNotEqual(
            fingerprint_findings(["ledger stale"]),
            fingerprint_findings(["ledger stale", "queue expired"]),
        )

    def test_empty_findings_have_stable_hash(self) -> None:
        self.assertEqual(fingerprint_findings([]), fingerprint_findings(["", "  "]))
        self.assertEqual(
            fingerprint_findings([]),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )


class DedupeDecisionTests(unittest.TestCase):
    def test_identical_findings_comment_once(self) -> None:
        findings = ["ledger stale"]
        first = should_comment(findings, None)
        second = should_comment(findings, fingerprint_findings(findings))
        self.assertTrue(first)
        self.assertFalse(second)

    def test_changed_finding_comments_again(self) -> None:
        previous = fingerprint_findings(["ledger stale"])
        self.assertTrue(should_comment(["ledger stale", "heartbeat stale"], previous))

    def test_all_clear_comments_once_then_stays_quiet(self) -> None:
        last = fingerprint_findings(["ledger stale"])
        self.assertTrue(should_comment([], last))
        self.assertFalse(should_comment([], fingerprint_findings([])))

    def test_all_clear_without_prior_issue_does_not_comment(self) -> None:
        self.assertFalse(should_comment([], None))

    def test_legacy_comment_without_marker_is_reconstructed(self) -> None:
        body = (
            "Scheduled fleet-watch run failed: "
            "https://github.com/frankxai/agentic-ops-hub/actions/runs/35007919885\n\n"
            "```\n"
            "fleet-watch: 1 stale/failing signal(s) as of 2026-09-15T18:30:38+00:00\n"
            "- ops/OPS-LEDGER.md: Last sweep 2026-08-10T00:35+02:00 is older than 72h "
            "against the declared daily cadence\n"
            "```\n"
        )
        findings = [
            "ops/OPS-LEDGER.md: Last sweep 2026-09-15T00:00:00+00:00 is older than 72h "
            "against the declared daily cadence"
        ]
        extracted = fingerprint_from_comment_body(body)
        self.assertEqual(extracted, fingerprint_findings(findings))
        self.assertFalse(should_comment(findings, extracted))

    def test_embedded_marker_wins(self) -> None:
        fingerprint = fingerprint_findings(["x"])
        body = f"{fingerprint_marker(fingerprint)}\nnoise 2026-09-15T18:30:38+00:00"
        self.assertEqual(fingerprint_from_comment_body(body), fingerprint)

    def test_last_automated_comment_skips_human_replies(self) -> None:
        findings = ["ledger stale"]
        bot = build_comment_body(findings, fingerprint_findings(findings), run_url="https://example/actions/runs/1")
        human = "I restarted the host."
        self.assertEqual(
            last_automated_fingerprint([bot, human]),
            fingerprint_findings(findings),
        )

    def test_stabilize_strips_timestamps_and_run_ids(self) -> None:
        text = stabilize_text(
            "as of 2026-09-15T18:30:38+00:00 /actions/runs/35007919885"
        )
        self.assertEqual(text, "as of <ts> /actions/runs/<id>")

    def test_paginated_json_arrays_concatenate(self) -> None:
        raw = '[{"body": "a"}]\n[{"body": "b"}]'
        items = parse_paginated_json_arrays(raw)
        self.assertEqual([item["body"] for item in items], ["a", "b"])


class DryRunCliTests(unittest.TestCase):
    def _run(self, argv: list[str]) -> tuple[int, str]:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(argv)
        return code, buf.getvalue()

    def test_two_identical_runs_comment_once(self) -> None:
        findings = ["ledger stale", "heartbeat stale"]
        first_code, first_out = self._run(
            [
                "--dry-run",
                "--finding",
                findings[0],
                "--finding",
                findings[1],
            ]
        )
        self.assertEqual(first_code, 1)
        self.assertIn("DECISION=comment", first_out)
        fingerprint = fingerprint_findings(findings)
        prior = build_comment_body(
            findings,
            fingerprint,
            run_url="https://github.com/frankxai/agentic-ops-hub/actions/runs/1",
        )
        second_code, second_out = self._run(
            [
                "--dry-run",
                "--finding",
                findings[0],
                "--finding",
                findings[1],
                "--last-comment-body",
                prior,
            ]
        )
        self.assertEqual(second_code, 1)
        self.assertIn("DECISION=skip", second_out)
        self.assertIn("WOULD_COMMENT=false", second_out)

    def test_changed_finding_comments_again(self) -> None:
        previous = build_comment_body(
            ["ledger stale"],
            fingerprint_findings(["ledger stale"]),
        )
        code, out = self._run(
            [
                "--dry-run",
                "--finding",
                "ledger stale",
                "--finding",
                "queue expired",
                "--last-comment-body",
                previous,
            ]
        )
        self.assertEqual(code, 1)
        self.assertIn("DECISION=comment", out)
        self.assertIn("WOULD_COMMENT=true", out)

    def test_all_clear_after_findings_comments_then_exits_zero(self) -> None:
        previous = build_comment_body(
            ["ledger stale"],
            fingerprint_findings(["ledger stale"]),
        )
        code, out = self._run(
            [
                "--dry-run",
                "--skip-live-checks",
                "--last-comment-body",
                previous,
            ]
        )
        self.assertEqual(code, 0)
        self.assertIn("DECISION=comment", out)
        self.assertIn("all liveness signals fresh", out)


if __name__ == "__main__":
    unittest.main()
