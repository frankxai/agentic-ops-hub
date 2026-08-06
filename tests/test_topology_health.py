#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "topology_health.py"
MISSION = ROOT / "scripts" / "mission_envelope.py"
PULSE = ROOT / "scripts" / "topology_health_pulse.py"


class TopologyHealthTests(unittest.TestCase):
    def test_script_runs_and_emits_schema(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            # allowlist only fleet/receipts etc — write into worktree reports via --write under allowlist
            out = ROOT / "fleet" / "reports" / "_test_topology_receipt.json"
            p = subprocess.run(
                [sys.executable, str(SCRIPT), "--write", str(out)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertIn(p.returncode, (0, 1, 2), msg=p.stdout + p.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data.get("schema"), "topology-health/v1")
            self.assertIn(data.get("status"), {"GREEN", "YELLOW", "RED"})
            self.assertIn("planes", data)
            self.assertIn("findings", data)
            # no raw MCP command args
            for m in data.get("planes", {}).get("mcp", []) or []:
                self.assertNotIn("command", m)
            try:
                out.unlink()
            except OSError:
                pass

    def test_write_outside_allowlist_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "evil.json"
            p = subprocess.run(
                [sys.executable, str(SCRIPT), "--write", str(bad)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(bad.exists())


class MissionEnvelopeTests(unittest.TestCase):
    def test_verified_requires_evaluator(self) -> None:
        p = subprocess.run(
            [
                sys.executable,
                str(MISSION),
                "receipt",
                "--envelope-id",
                "env_test",
                "--status",
                "verified",
                "--summary",
                "should fail",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(p.returncode, 0)

    def test_verified_rejects_self_evaluator(self) -> None:
        out = ROOT / "fleet" / "receipts" / "_test_self_verified.json"
        p = subprocess.run(
            [
                sys.executable,
                str(MISSION),
                "receipt",
                "--envelope-id",
                "env_test",
                "--status",
                "verified",
                "--evaluator",
                "self",
                "--summary",
                "should fail",
                "--out",
                str(out),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        self.assertFalse(out.exists())

    def test_candidate_ok(self) -> None:
        out = ROOT / "fleet" / "receipts" / "_test_candidate.json"
        p = subprocess.run(
            [
                sys.executable,
                str(MISSION),
                "receipt",
                "--envelope-id",
                "env_test",
                "--status",
                "candidate",
                "--summary",
                "worker done",
                "--out",
                str(out),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "candidate")
        v = subprocess.run(
            [sys.executable, str(MISSION), "validate", str(out)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(v.returncode, 0, msg=v.stdout + v.stderr)
        # tamper hash
        data["summary"] = "tampered"
        out.write_text(json.dumps(data), encoding="utf-8")
        v2 = subprocess.run(
            [sys.executable, str(MISSION), "validate", str(out)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(v2.returncode, 0)
        try:
            out.unlink()
        except OSError:
            pass

    def test_out_outside_allowlist_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "x.json"
            p = subprocess.run(
                [
                    sys.executable,
                    str(MISSION),
                    "receipt",
                    "--envelope-id",
                    "env_test",
                    "--status",
                    "candidate",
                    "--out",
                    str(bad),
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(bad.exists())


class PulseExitTests(unittest.TestCase):
    def test_pulse_exits_zero_even_on_red(self) -> None:
        if not PULSE.is_file():
            self.skipTest("pulse missing")
        p = subprocess.run(
            [sys.executable, str(PULSE), "--force"],
            capture_output=True,
            text=True,
            timeout=180,
        )
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
