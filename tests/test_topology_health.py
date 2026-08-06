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


class TopologyHealthTests(unittest.TestCase):
    def test_script_runs_and_emits_schema(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "receipt.json"
            p = subprocess.run(
                [sys.executable, str(SCRIPT), "--write", str(out)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertIn(p.returncode, (0, 2), msg=p.stdout + p.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data.get("schema"), "topology-health/v1")
            self.assertIn(data.get("status"), {"GREEN", "YELLOW", "RED"})
            self.assertIn("planes", data)
            self.assertIn("findings", data)
            self.assertIn("cron", data["planes"])
            self.assertIn("mcp", data["planes"])


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

    def test_candidate_ok(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "r.json"
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


if __name__ == "__main__":
    unittest.main()
