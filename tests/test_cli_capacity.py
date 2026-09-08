from __future__ import annotations

import json
import unittest
from unittest.mock import patch

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

    def test_claude_live_probe_accepts_event_list_output(self) -> None:
        events = [
            {"type": "system", "session_id": "private"},
            {"type": "result", "is_error": False, "result": "PONG", "session_id": "private"},
        ]
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(
                 cli_capacity,
                 "run",
                 side_effect=[
                     (0, json.dumps({"loggedIn": True})),
                     (0, json.dumps(events)),
                 ],
             ):
            probe = cli_capacity._probe_claude(True)
        self.assertEqual("ready", probe["status"])
        self.assertEqual("credentials declared", probe["declared_detail"])
        self.assertEqual("PONG", probe["live_detail"])
        self.assertNotIn("private", probe["live_detail"])

    def test_claude_failed_auth_redacts_provider_output(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(
                 cli_capacity,
                 "run",
                 return_value=(1, "account private@example.invalid token-adjacent detail"),
             ) as run_mock:
            probe = cli_capacity._probe_claude(True)
        self.assertEqual(1, run_mock.call_count)
        self.assertEqual("auth-missing", probe["status"])
        self.assertEqual("credentials unavailable", probe["declared_detail"])
        self.assertNotIn("private", probe["declared_detail"])

    def test_simple_live_probe_redacts_provider_metadata(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(
                 cli_capacity,
                 "run",
                 side_effect=[
                     (0, "logged in"),
                     (0, 'PONG {"requestId":"private-id","usage":{"input_tokens":50000}}'),
                 ],
             ):
            probe = cli_capacity._probe_simple(
                "grok", True, ["grok", "probe"], ["grok", "models"]
            )
        self.assertEqual("ready", probe["status"])
        self.assertEqual("PONG", probe["live_detail"])
        self.assertEqual("credentials declared", probe["declared_detail"])
        self.assertNotIn("private", probe["declared_detail"])

    def test_metered_probe_redacts_declared_provider_metadata(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(
                 cli_capacity,
                 "run",
                 return_value=(0, "configured account private@example.invalid"),
             ):
            probe = cli_capacity._probe_metered_dcode()
        self.assertEqual("credentials declared", probe["declared_detail"])
        self.assertNotIn("private", probe["declared_detail"])

    def test_codex_probe_is_neutral_and_redacts_provider_metadata(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.dict(cli_capacity.os.environ, {"TEMP": "C:/Temp"}), \
             patch.object(
                 cli_capacity,
                 "run",
                 side_effect=[
                     (0, "Logged in using ChatGPT"),
                     (0, "PONG session id: private-id"),
                 ],
             ) as run_mock:
            probe = cli_capacity._probe_codex(True, "C:/repo", "gpt-test")
        command = run_mock.call_args_list[1].args[0]
        self.assertIn("--skip-git-repo-check", command)
        self.assertEqual("C:/Temp", command[command.index("-C") + 1])
        self.assertEqual("credentials declared", probe["declared_detail"])
        self.assertEqual("PONG", probe["live_detail"])

    def test_codex_failed_auth_redacts_provider_output(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(
                 cli_capacity,
                 "run",
                 return_value=(1, "account private@example.invalid token-adjacent detail"),
             ):
            probe = cli_capacity._probe_codex(False, "C:/repo", "gpt-test")
        self.assertEqual("credentials unavailable", probe["declared_detail"])
        self.assertNotIn("private", probe["declared_detail"])

    def test_grok_probe_uses_minimal_neutral_context(self) -> None:
        with patch.dict(cli_capacity.os.environ, {"TEMP": "C:/Temp"}):
            command = cli_capacity.grok_probe_command()
        self.assertEqual("C:/Temp", command[command.index("--cwd") + 1])
        self.assertIn("--verbatim", command)
        self.assertIn("--system-prompt-override", command)

    def test_gemini_live_probe_redacts_provider_metadata(self) -> None:
        with patch.object(cli_capacity, "_version", return_value=(True, "v1")), \
             patch.object(cli_capacity.Path, "is_file", return_value=True), \
             patch.object(
                 cli_capacity,
                 "run",
                 return_value=(0, 'PONG {"session_id":"private"}'),
             ) as run_mock:
            probe = cli_capacity._probe_gemini(True)
        command = run_mock.call_args.args[0]
        self.assertIn("--approval-mode", command)
        self.assertEqual("plan", command[command.index("--approval-mode") + 1])
        self.assertIn("--sandbox=true", command)
        self.assertEqual("ready", probe["status"])
        self.assertEqual("PONG", probe["live_detail"])

    def test_resource_pressure_blocks_new_agent_launches(self) -> None:
        gate = cli_capacity.resource_gate(disk_free_gb=80, memory_percent=91)
        self.assertFalse(gate["launch_allowed"])
        self.assertIn("memory", gate["blockers"])

    def test_healthy_resources_allow_bounded_launches(self) -> None:
        gate = cli_capacity.resource_gate(disk_free_gb=90, memory_percent=60)
        self.assertTrue(gate["launch_allowed"])
        self.assertEqual([], gate["blockers"])

    def test_report_inventories_all_cli_surfaces_and_keeps_metered_lane_closed(self) -> None:
        ready = {"status": "ready", "installed": True}
        disk = type("Disk", (), {"free": 100 * 1024**3})()
        with patch.object(cli_capacity.shutil, "disk_usage", return_value=disk), \
             patch.object(cli_capacity, "memory_percent", return_value=40), \
             patch.object(cli_capacity, "_probe_claude", return_value=ready), \
             patch.object(cli_capacity, "_probe_codex", return_value=ready), \
             patch.object(cli_capacity, "_probe_gemini", return_value=ready), \
             patch.object(cli_capacity, "_probe_simple", return_value=ready), \
             patch.object(
                 cli_capacity,
                 "_probe_metered_dcode",
                 return_value={"status": "metered-disabled", "installed": True},
             ):
            report = cli_capacity.build_report(
                machine="yoga-book", live=True, repo="C:/repo", codex_model="gpt-5.6-terra"
            )
        self.assertEqual(
            {
                "claude-max", "openai-codex-max", "gemini-ultra", "opencode",
                "grok-heavy", "agy", "dcode-metered",
            },
            set(report["subscription_clis"]),
        )
        self.assertNotIn("dcode-metered", report["ready_lanes"])

    def test_live_probe_can_be_scoped_to_selected_cli(self) -> None:
        ready = {"status": "ready", "installed": True}
        disk = type("Disk", (), {"free": 100 * 1024**3})()
        with patch.object(cli_capacity.shutil, "disk_usage", return_value=disk), \
             patch.object(cli_capacity, "memory_percent", return_value=40), \
             patch.object(cli_capacity, "_probe_claude", return_value=ready) as claude_probe, \
             patch.object(cli_capacity, "_probe_codex", return_value=ready) as codex_probe, \
             patch.object(cli_capacity, "_probe_gemini", return_value=ready), \
             patch.object(cli_capacity, "_probe_simple", return_value=ready), \
             patch.object(cli_capacity, "_probe_metered_dcode", return_value=ready):
            cli_capacity.build_report(
                machine="yoga-book",
                live=True,
                repo="C:/repo",
                codex_model="gpt-5.6-terra",
                live_clis={"codex"},
            )
        claude_probe.assert_called_once_with(False)
        codex_probe.assert_called_once_with(True, "C:/repo", "gpt-5.6-terra")


if __name__ == "__main__":
    unittest.main()
