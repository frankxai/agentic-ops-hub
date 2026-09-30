import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from scripts import fleet_bus, fleet_watch
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


GIT_ENV = {
    "GIT_AUTHOR_NAME": "fleet-watch-test",
    "GIT_AUTHOR_EMAIL": "fleet-watch-test@example.invalid",
    "GIT_COMMITTER_NAME": "fleet-watch-test",
    "GIT_COMMITTER_EMAIL": "fleet-watch-test@example.invalid",
}


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class PulseBranchTests(unittest.TestCase):
    """End to end: publish_pulse -> bare remote -> fetch -> check_heartbeats."""

    def setUp(self) -> None:
        env = mock.patch.dict(os.environ, GIT_ENV)
        env.start()
        self.addCleanup(env.stop)
        tmp = tempfile.TemporaryDirectory(dir=fleet_watch.REPO_ROOT)
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.remote = self.root / "remote.git"
        self.work = self.root / "work"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        subprocess.run(["git", "init", "-q", str(self.work)], check=True)
        _git(self.work, "remote", "add", "origin", str(self.remote))
        self.manifest = self.root / "clone-manifest.json"
        manifest = mock.patch.object(fleet_watch, "MANIFEST_PATH", self.manifest)
        manifest.start()
        self.addCleanup(manifest.stop)

    def register(self, machines: dict) -> None:
        self.manifest.write_text(json.dumps({"machines": machines}), encoding="utf-8")

    def publish(self, machine_id: str, at: datetime, status: str = "live") -> None:
        beat = {"machine_id": machine_id, "status": status, "at": at.isoformat()}
        fleet_bus.publish_pulse(beat, remote="origin", repo=self.work)

    def check(self) -> tuple[list[str], list[str]]:
        _git(self.work, "fetch", "-q", "origin", "+refs/heads/pulse/*:refs/remotes/origin/pulse/*")
        return fleet_watch.check_heartbeats(NOW, 24, remote="origin", repo=self.work)

    def test_fresh_pulse_is_healthy(self) -> None:
        self.register({"box": {"liveness": {"status": "active", "max_age_hours": 24}}})
        self.publish("box", NOW - timedelta(hours=2))
        self.assertEqual(([], []), self.check())

    def test_pulse_is_a_single_parentless_commit(self) -> None:
        self.register({"box": {"liveness": {"status": "active"}}})
        self.publish("box", NOW - timedelta(hours=3))
        self.publish("box", NOW - timedelta(hours=1))
        self.check()
        count = subprocess.run(
            ["git", "-C", str(self.work), "rev-list", "--count", "origin/pulse/box"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual("1", count)

    def test_stale_pulse_is_a_finding(self) -> None:
        self.register({"box": {"liveness": {"status": "active", "max_age_hours": 24}}})
        self.publish("box", NOW - timedelta(hours=30))
        findings, warnings = self.check()
        self.assertEqual([], warnings)
        self.assertEqual(1, len(findings), findings)
        self.assertIn("pulse/box", findings[0])
        self.assertIn("stale", findings[0])

    def test_registry_max_age_overrides_default(self) -> None:
        self.register({"box": {"liveness": {"status": "active", "max_age_hours": 48}}})
        self.publish("box", NOW - timedelta(hours=30))
        self.assertEqual(([], []), self.check())

    def test_not_live_status_is_a_finding(self) -> None:
        self.register({"box": {"liveness": {"status": "active"}}})
        self.publish("box", NOW - timedelta(hours=1), status="degraded")
        findings, _ = self.check()
        self.assertTrue(any("not-live" in f for f in findings), findings)

    def test_registered_machine_without_branch_is_a_finding(self) -> None:
        self.register({"box": {"liveness": {"status": "active"}}})
        findings, warnings = self.check()
        self.assertEqual([], warnings)
        self.assertEqual(["pulse/box: machine box is registered but has no pulse branch"], findings)

    def test_unregistered_branch_is_a_warning_not_a_finding(self) -> None:
        self.register({"box": {"liveness": {"status": "active"}}})
        self.publish("box", NOW - timedelta(hours=1))
        self.publish("stray", NOW - timedelta(hours=1))
        findings, warnings = self.check()
        self.assertEqual([], findings)
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("pulse/stray", warnings[0])

    def test_heartbeat_for_another_machine_is_a_finding(self) -> None:
        self.register({"box": {"liveness": {"status": "active"}}})
        beat = {"machine_id": "other", "status": "live", "at": NOW.isoformat()}
        blob = subprocess.run(
            ["git", "-C", str(self.work), "hash-object", "-w", "--stdin"],
            input=json.dumps(beat).encode(),
            check=True,
            capture_output=True,
        ).stdout.decode().strip()
        tree = subprocess.run(
            ["git", "-C", str(self.work), "mktree"],
            input=f"100644 blob {blob}\theartbeat.json\n".encode(),
            check=True,
            capture_output=True,
        ).stdout.decode().strip()
        commit = subprocess.run(
            ["git", "-C", str(self.work), "commit-tree", tree, "-m", "forged"],
            check=True,
            capture_output=True,
        ).stdout.decode().strip()
        _git(self.work, "push", "-q", "origin", f"{commit}:refs/heads/pulse/box")
        findings, _ = self.check()
        self.assertTrue(any("claims machine_id='other'" in f for f in findings), findings)

    def test_retired_machine_is_skipped(self) -> None:
        self.register(
            {
                "old": {
                    "liveness": {"status": "retired", "retired_at": "2026-08-01T00:00:00Z"}
                }
            }
        )
        self.assertEqual(([], []), self.check())

    def test_retired_without_stamp_is_still_watched(self) -> None:
        # Silence must not retire a machine: without a declared retired_at the
        # dead-man's switch keeps watching it.
        self.register({"old": {"liveness": {"status": "retired"}}})
        findings, _ = self.check()
        self.assertEqual(1, len(findings), findings)

    def test_machine_without_liveness_block_is_not_watched(self) -> None:
        self.register(
            {
                "box": {"liveness": {"status": "active"}},
                "future": {"role": "expandable-slot"},
            }
        )
        self.publish("box", NOW - timedelta(hours=1))
        self.assertEqual(([], []), self.check())

    def test_live_manifest_declares_c940(self) -> None:
        manifest = json.loads(
            (fleet_watch.REPO_ROOT / "fleet" / "clone-manifest.json").read_text(encoding="utf-8")
        )
        liveness = manifest["machines"]["c940"]["liveness"]
        self.assertEqual("active", liveness["status"])
        self.assertFalse(is_retired(liveness))


class LedgerHeaderTests(unittest.TestCase):
    def test_last_sweep_regex_matches_ledger_format(self) -> None:
        line = "**Last sweep:** 2026-08-10T00:35+02:00 (Queen 10h wave-2 start)"
        match = LAST_SWEEP_RE.search(line)
        assert match is not None
        parsed = datetime.fromisoformat(match.group(1))
        self.assertEqual(2026, parsed.year)

    def _ledger_findings(self, swept: datetime) -> list[str]:
        with tempfile.TemporaryDirectory(dir=fleet_watch.REPO_ROOT) as tmp:
            ledger = Path(tmp) / "OPS-LEDGER.md"
            ledger.write_text(f"**Last sweep:** {swept.isoformat()} (test)\n", encoding="utf-8")
            with mock.patch.object(fleet_watch, "LEDGER_PATH", ledger):
                return fleet_watch.check_ledger(NOW, 336)

    def test_ledger_ten_days_old_is_within_cadence(self) -> None:
        self.assertEqual([], self._ledger_findings(NOW - timedelta(days=10)))

    def test_ledger_fifteen_days_old_is_a_finding(self) -> None:
        self.assertEqual(1, len(self._ledger_findings(NOW - timedelta(days=15))))


if __name__ == "__main__":
    unittest.main()
