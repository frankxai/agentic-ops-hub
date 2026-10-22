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
        command = cli_capacity.opencode_probe_command()
        self.assertEqual(command[:4], ["opencode", "run", "-m", "vercel/deepseek/deepseek-v4.1-flash"])
        free = cli_capacity.opencode_probe_command(allow_free=True)
        self.assertTrue(free[3].startswith("opencode/"), free[:4])


if __name__ == "__main__":
    unittest.main()
