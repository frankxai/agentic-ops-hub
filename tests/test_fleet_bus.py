"""Safety regressions for the Git-backed fleet task contract CLI."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fleet_bus.py"
SPEC = importlib.util.spec_from_file_location("fleet_bus", SCRIPT)
assert SPEC and SPEC.loader
fleet_bus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fleet_bus)


def valid_contract(**overrides: object) -> dict:
    contract = {
        "schema_version": "1.0.0",
        "task_id": "safe-task-1",
        "title": "Safe task",
        "description": "Bounded regression fixture.",
        "issuer": "yoga-book",
        "issued_at": "2026-08-28T00:00:00+00:00",
        "machine_owner": "yoga-book",
        "repo_path_allowlist": ["agentic-ops-hub/fleet"],
        "resource_budget": {
            "max_tokens": 1000,
            "max_minutes": 10,
            "max_cost_usd": 0.1,
            "models_allowed": ["test-model"],
        },
        "expiry": "2099-01-01T00:00:00+00:00",
        "done_condition": {"type": "and", "conditions": [{"type": "file_exists", "path": "fleet/report.md"}]},
        "priority": "P1",
        "constraints": ["no force push"],
        "source": "tests",
        "execution_status": "issued",
        "outcome_status": None,
        "claimed_by": None,
        "claimed_at": None,
        "evidence_refs": [],
    }
    contract.update(overrides)
    return contract


class FleetBusSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.old_bus_root = fleet_bus.BUS_ROOT
        self.old_legacy_bus_root = fleet_bus.LEGACY_BUS_ROOT
        self.old_detect_machine = fleet_bus.detect_machine
        fleet_bus.BUS_ROOT = self.root / "fleet" / "bus"
        fleet_bus.LEGACY_BUS_ROOT = self.root / "legacy" / "bus"
        fleet_bus.detect_machine = lambda: "yoga-book"

    def tearDown(self) -> None:
        fleet_bus.BUS_ROOT = self.old_bus_root
        fleet_bus.LEGACY_BUS_ROOT = self.old_legacy_bus_root
        fleet_bus.detect_machine = self.old_detect_machine
        self.temp_dir.cleanup()

    def test_contract_schema_is_present_and_requires_ownership_fields(self) -> None:
        schema_path = Path(__file__).resolve().parents[1] / "fleet" / "schemas" / "task-contract.v1.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertTrue(schema["additionalProperties"] is True)
        self.assertTrue({"machine_owner", "repo_path_allowlist", "resource_budget", "expiry", "done_condition"}.issubset(schema["required"]))

    def test_runtime_rejects_missing_schema_required_fields(self) -> None:
        for field in ("title", "description", "issuer", "priority", "source", "constraints", "evidence_refs"):
            with self.subTest(field=field):
                contract = valid_contract()
                contract.pop(field)
                with self.assertRaisesRegex(ValueError, field):
                    fleet_bus.validate_task_contract(contract)

    def test_valid_contract_round_trips(self) -> None:
        contract = valid_contract()
        fleet_bus.write_task_contract(contract)
        self.assertEqual(fleet_bus.load_task_contract(contract["task_id"]), contract)

    def test_contract_rejects_absolute_or_traversing_allowlist(self) -> None:
        for allowlist in (["C:/outside"], ["fleet/../outside"]):
            with self.subTest(allowlist=allowlist):
                with self.assertRaisesRegex(ValueError, "relative non-traversing"):
                    fleet_bus.validate_task_contract(valid_contract(repo_path_allowlist=allowlist))

    def test_contract_rejects_unsafe_task_id_before_writing(self) -> None:
        with self.assertRaisesRegex(ValueError, "task_id"):
            fleet_bus.write_task_contract(valid_contract(task_id="../escape"))
        self.assertFalse((self.root / "escape.json").exists())

    def test_lease_refuses_foreign_issuer_without_writing(self) -> None:
        source = self.root / "foreign-contract.json"
        source.write_text(json.dumps(valid_contract(issuer="c940")), encoding="utf-8")
        args = argparse.Namespace(task_id="safe-task-1", file=str(source))
        self.assertEqual(fleet_bus.cmd_task_lease(args), 2)
        self.assertFalse((fleet_bus.BUS_ROOT / "contracts" / "safe-task-1.json").exists())

    def test_claim_and_receipt_refuse_foreign_owner_without_writing(self) -> None:
        contract = valid_contract(machine_owner="c940")
        contract_path = fleet_bus._task_contract_path(contract["task_id"])
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        claim = argparse.Namespace(task_id=contract["task_id"])
        receipt = argparse.Namespace(task_id=contract["task_id"], outcome="success", summary="x", evidence="report.md")
        self.assertEqual(fleet_bus.cmd_task_claim(claim), 2)
        self.assertEqual(fleet_bus.cmd_task_receipt(receipt), 3)
        self.assertFalse((fleet_bus.BUS_ROOT / "receipts").exists())


if __name__ == "__main__":
    unittest.main()
