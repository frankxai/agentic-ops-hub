from __future__ import annotations

import unittest

from scripts import cli_capacity


class CliCapacityTests(unittest.TestCase):
    def test_declared_auth_is_not_reported_as_live_ready(self) -> None:
        status = cli_capacity.classify_probe(
            installed=True,
            auth_declared=True,
            live_checked=False,
            live_ok=False,
        )
        self.assertEqual("auth-declared-unverified", status)

    def test_live_failure_overrides_declared_auth(self) -> None:
        status = cli_capacity.classify_probe(
            installed=True,
            auth_declared=True,
            live_checked=True,
            live_ok=False,
        )
        self.assertEqual("blocked-live-auth", status)

    def test_resource_pressure_blocks_new_agent_launches(self) -> None:
        gate = cli_capacity.resource_gate(disk_free_gb=80, memory_percent=91)
        self.assertFalse(gate["launch_allowed"])
        self.assertIn("memory", gate["blockers"])

    def test_healthy_resources_allow_bounded_launches(self) -> None:
        gate = cli_capacity.resource_gate(disk_free_gb=90, memory_percent=60)
        self.assertTrue(gate["launch_allowed"])
        self.assertEqual([], gate["blockers"])

    def test_opencode_live_probe_is_pinned_and_never_ambient(self) -> None:
        command = cli_capacity.opencode_probe_command(allowance_usd=0.01)
        self.assertEqual(command[0], "python")
        self.assertEqual(command[command.index("--class") + 1], "scout")
        self.assertNotIn("--allow-free", command)
        free = cli_capacity.opencode_probe_command(allow_free=True)
        self.assertIn("--allow-free", free)

    def test_paid_opencode_probe_refuses_without_explicit_allowance(self):
        for bad in (None, 0, -1, float("nan"), float("inf"), True):
            with self.assertRaisesRegex(ValueError, "allowance"):
                cli_capacity.opencode_probe_command(allowance_usd=bad)
        argv = cli_capacity.opencode_probe_command(allowance_usd=0.01)
        self.assertEqual(argv[argv.index("--allowance-usd") + 1], "0.01")


if __name__ == "__main__":
    unittest.main()
