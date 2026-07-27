import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from smis.cli import main
from smis.control_plane import MediaControlPlane, PolicyBlocked, _REQUIRED_GATES


class StageZeroPolicyTests(unittest.TestCase):
    def test_stage_zero_blocks_scheduling_even_with_all_required_evidence(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))

            with self.assertRaises(PolicyBlocked) as blocked:
                control_plane.preflight_publication(
                    mode="schedule",
                    evidence={
                        "source_provenance": True,
                        "rights_and_reuse": True,
                        "brand_voice": True,
                        "accessibility": True,
                        "platform_policy": True,
                        "human_approval": True,
                        "idempotency": True,
                        "cost_or_quota": True,
                    },
                )

        self.assertEqual(blocked.exception.reason, "autonomy_stage_0_draft_only")

    def test_pre_registered_experiment_creates_a_hash_linked_receipt(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            experiment = control_plane.create_experiment(
                experiment_id="smis-exp-001",
                hypothesis="A source-backed brief improves first-pass approval.",
                brand_id="frankx",
                primary_metric="first_pass_acceptance_rate",
                guardrails=["rights_clear"],
                decision_rule="adopt when the treatment beats the baseline",
            )
            events = control_plane.read_events()

        self.assertEqual(experiment["id"], "smis-exp-001")
        self.assertEqual(events[0]["event_type"], "experiment.created")
        self.assertIsNone(events[0]["previous_event_hash"])
        self.assertEqual(len(events[0]["event_hash"]), 64)

    def test_content_package_starts_as_draft_with_a_provenance_reference(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            package = control_plane.create_content_package(
                package_id="smis-cp-001",
                brand_id="frankx",
                thesis="Creators need an evidence-first AI tool stack.",
                source_packet_ids=["source-creator-radar-001"],
            )
            events = control_plane.read_events()

        self.assertEqual(package["status"], "draft")
        self.assertEqual(package["source_packet_ids"], ["source-creator-radar-001"])
        self.assertEqual(events[0]["event_type"], "content_package.created")

    def test_event_chain_verification_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            control_plane.create_experiment(
                experiment_id="smis-exp-integrity-001",
                hypothesis="Receipts must be tamper evident.",
                brand_id="frankx",
                primary_metric="first_pass_acceptance_rate",
                guardrails=["rights_clear"],
                decision_rule="reject when integrity is broken",
            )
            control_plane.create_content_package(
                package_id="smis-cp-integrity-001",
                brand_id="frankx",
                thesis="Integrity must be checked before learning.",
                source_packet_ids=["source-integrity-001"],
            )
            self.assertTrue(control_plane.verify_event_chain())

            events = control_plane.read_events()
            events[0]["entity_id"] = "tampered"
            control_plane.events_path.write_text(
                "\n".join(json.dumps(event) for event in events) + "\n",
                encoding="utf-8",
            )

            self.assertFalse(control_plane.verify_event_chain())

    def test_receipts_minimize_content_and_identify_the_entity(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            control_plane.create_content_package(
                package_id="smis-cp-receipt-001",
                brand_id="frankx",
                thesis="Private editorial thesis must not be copied into the receipt.",
                source_packet_ids=["source-receipt-001"],
            )
            receipt = control_plane.read_events()[0]

        self.assertEqual(receipt["entity_id"], "smis-cp-receipt-001")
        self.assertEqual(receipt["entity_type"], "content_package")
        self.assertEqual(receipt["sequence"], 1)
        self.assertTrue(receipt["event_id"].startswith("smis_evt_"))
        self.assertEqual(len(receipt["payload_hash"]), 64)
        self.assertNotIn("Private editorial thesis", json.dumps(receipt))

    def test_tampered_chain_blocks_creation_of_a_new_record(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            control_plane.create_experiment(
                experiment_id="smis-exp-block-001",
                hypothesis="A corrupted chain must halt new writes.",
                brand_id="frankx",
                primary_metric="first_pass_acceptance_rate",
                guardrails=["rights_clear"],
                decision_rule="block when chain validation fails",
            )
            events = control_plane.read_events()
            events[0]["entity_id"] = "tampered"
            control_plane.events_path.write_text(
                "\n".join(json.dumps(event) for event in events) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError) as blocked:
                control_plane.create_content_package(
                    package_id="smis-cp-block-001",
                    brand_id="frankx",
                    thesis="This write should not occur.",
                    source_packet_ids=["source-block-001"],
                )

            record_exists = (
                Path(temporary_directory) / "records" / "content-packages" / "smis-cp-block-001.json"
            ).exists()

        self.assertEqual(blocked.exception.args[0], "event chain verification failed")
        self.assertFalse(record_exists)

    def test_concurrent_same_id_writes_leave_one_matching_record_and_receipt(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            start = threading.Barrier(16)

            def create_package(index: int):
                start.wait()
                try:
                    return control_plane.create_content_package(
                        package_id="smis-cp-concurrent-001",
                        brand_id="frankx",
                        thesis=f"Concurrent thesis {index}",
                        source_packet_ids=["source-concurrent-001"],
                    )
                except ValueError as error:
                    return error

            with ThreadPoolExecutor(max_workers=16) as executor:
                outcomes = list(executor.map(create_package, range(16)))

            successful = [outcome for outcome in outcomes if isinstance(outcome, dict)]
            failures = [outcome for outcome in outcomes if isinstance(outcome, ValueError)]
            record_path = (
                Path(temporary_directory) / "records" / "content-packages" / "smis-cp-concurrent-001.json"
            )
            record = json.loads(record_path.read_text(encoding="utf-8"))
            receipts = [
                event
                for event in control_plane.read_events()
                if event["entity_id"] == "smis-cp-concurrent-001"
            ]

        self.assertEqual(len(successful), 1)
        self.assertEqual(len(failures), 15)
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["payload_hash"], control_plane._hash(record))
        self.assertTrue(control_plane.verify_event_chain())

    def test_existing_record_id_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            control_plane.create_content_package(
                package_id="smis-cp-immutable-001",
                brand_id="frankx",
                thesis="Original thesis.",
                source_packet_ids=["source-immutable-001"],
            )

            with self.assertRaises(ValueError) as blocked:
                control_plane.create_content_package(
                    package_id="smis-cp-immutable-001",
                    brand_id="frankx",
                    thesis="Replacement thesis.",
                    source_packet_ids=["source-immutable-001"],
                )

        self.assertEqual(blocked.exception.args[0], "record already exists: smis-cp-immutable-001")

    def test_dry_run_requires_every_governance_gate(self):
        all_evidence = {
            "source_provenance": True,
            "rights_and_reuse": True,
            "brand_voice": True,
            "accessibility": True,
            "platform_policy": True,
            "human_approval": True,
            "idempotency": True,
            "cost_or_quota": True,
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))

            with self.assertRaises(PolicyBlocked) as blocked:
                control_plane.preflight_publication(
                    mode="dry_run",
                    evidence={**all_evidence, "rights_and_reuse": False},
                )

            allowed = control_plane.preflight_publication(mode="dry_run", evidence=all_evidence)

        self.assertEqual(blocked.exception.reason, "missing_evidence:rights_and_reuse")
        self.assertEqual(allowed["decision"], "eligible_draft_only")
        self.assertEqual(allowed["mode"], "dry_run")

    def test_stage_zero_cannot_be_overridden_by_constructor_argument(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(TypeError):
                MediaControlPlane(Path(temporary_directory), autonomy_stage=1)

    def test_preflight_requires_literal_true_for_every_gate(self):
        all_evidence = {gate: True for gate in _REQUIRED_GATES}
        invalid_values = ["false", 1, [], None]
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            for invalid_value in invalid_values:
                evidence = dict(all_evidence)
                evidence["rights_and_reuse"] = invalid_value
                with self.assertRaises(PolicyBlocked) as blocked:
                    control_plane.preflight_publication(mode="dry_run", evidence=evidence)
                self.assertEqual(blocked.exception.reason, "missing_evidence:rights_and_reuse")

    def test_preflight_rejects_unexpected_evidence_keys(self):
        evidence = {gate: True for gate in _REQUIRED_GATES}
        evidence["unreviewed_override"] = True
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            with self.assertRaises(PolicyBlocked) as blocked:
                control_plane.preflight_publication(mode="dry_run", evidence=evidence)

        self.assertEqual(blocked.exception.reason, "unexpected_evidence:unreviewed_override")

    def test_blocked_preflight_creates_a_sanitized_receipt(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            control_plane = MediaControlPlane(Path(temporary_directory))
            with self.assertRaises(PolicyBlocked):
                control_plane.preflight_publication(mode="dry_run", evidence={})
            receipt = control_plane.read_events()[0]

        self.assertEqual(receipt["event_type"], "preflight.blocked")
        self.assertEqual(receipt["entity_type"], "preflight")
        self.assertNotIn("evidence", json.dumps(receipt))

    def test_cli_initializes_a_stage_zero_store(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["init", "--store", temporary_directory])

            metadata_exists = (Path(temporary_directory) / "control-plane.json").exists()

        self.assertEqual(exit_code, 0)
        self.assertTrue(metadata_exists)
        self.assertIn('"autonomy_stage": 0', output.getvalue())

    def test_cli_registers_an_experiment_and_appends_a_receipt(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "experiment",
                        "--store",
                        temporary_directory,
                        "--id",
                        "smis-exp-cli-001",
                        "--hypothesis",
                        "A documented recipe improves review quality.",
                        "--brand",
                        "frankx",
                        "--metric",
                        "first_pass_acceptance_rate",
                        "--guardrail",
                        "rights_clear",
                        "--decision-rule",
                        "adopt when accepted output improves",
                    ]
                )
            events = [
                json.loads(line)
                for line in (Path(temporary_directory) / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(exit_code, 0)
        self.assertEqual(events[0]["event_type"], "experiment.created")
        self.assertIn('"id": "smis-exp-cli-001"', output.getvalue())

    def test_cli_reports_a_stage_zero_block_without_publishing(self):
        evidence = {
            "source_provenance": True,
            "rights_and_reuse": True,
            "brand_voice": True,
            "accessibility": True,
            "platform_policy": True,
            "human_approval": True,
            "idempotency": True,
            "cost_or_quota": True,
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            evidence_path = Path(temporary_directory) / "evidence.json"
            evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "preflight",
                        "--store",
                        temporary_directory,
                        "--mode",
                        "schedule",
                        "--evidence-file",
                        str(evidence_path),
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertIn('"reason": "autonomy_stage_0_draft_only"', output.getvalue())

    def test_cli_creates_a_draft_content_package(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "package",
                        "--store",
                        temporary_directory,
                        "--id",
                        "smis-cp-cli-001",
                        "--brand",
                        "frankx",
                        "--thesis",
                        "Evidence-first creator tools beat novelty chasing.",
                        "--source-packet",
                        "source-creator-radar-001",
                    ]
                )
            package = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(package["status"], "draft")
        self.assertEqual(package["source_packet_ids"], ["source-creator-radar-001"])


if __name__ == "__main__":
    unittest.main()
