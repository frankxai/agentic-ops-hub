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

    def test_claude_live_probe_accepts_json_result_list(self) -> None:
        output = '[{"type":"result","subtype":"success","is_error":false,"result":"PONG"}]'
        self.assertTrue(cli_capacity.claude_live_ok(0, output))

    def test_claude_live_probe_accepts_warning_before_json_result(self) -> None:
        output = 'warning: plugin unavailable\n[{"type":"result","is_error":false,"result":"PONG"}]'
        self.assertTrue(cli_capacity.claude_live_ok(0, output))

    def test_claude_live_probe_rejects_unstructured_pong_noise(self) -> None:
        self.assertFalse(cli_capacity.claude_live_ok(0, "warning: expected PONG but received nothing"))
        self.assertFalse(cli_capacity.claude_live_ok(0, ""))
        self.assertFalse(cli_capacity.claude_live_ok(1, '{"type":"result","result":"PONG"}'))

    def test_live_detail_is_structured_and_never_carries_raw_output(self) -> None:
        self.assertEqual(
            {"status": "verified", "reason": "pong-verified"},
            cli_capacity.structured_live_detail(checked=True, ok=True, exit_code=0),
        )
        self.assertEqual(
            {"status": "failed", "reason": "probe-exit-7"},
            cli_capacity.structured_live_detail(checked=True, ok=False, exit_code=7),
        )
        self.assertEqual(
            {"status": "not-run", "reason": "live-check-not-admitted"},
            cli_capacity.structured_live_detail(checked=False, ok=False),
        )


if __name__ == "__main__":
    unittest.main()
