import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts import audit_inspect

SECRET = "sk-test-DO-NOT-PRINT-0123456789abcdef0123456789"


def run(config):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "opencode.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = audit_inspect.main([str(path)])
    return code, out.getvalue()


class AuditInspectTests(unittest.TestCase):
    def test_never_prints_a_secret_value(self):
        _, out = run({"provider": {"vercel": {"options": {"apiKey": SECRET, "token": SECRET}}}})
        self.assertNotIn(SECRET, out)
        self.assertIn("LITERAL(not shown)", out)

    def test_env_reference_is_not_flagged_as_literal(self):
        _, out = run({"provider": {"vercel": {"options": {"apiKey": "{env:AI_GATEWAY_API_KEY}"}}}})
        self.assertIn("env-reference", out)
        self.assertNotIn("LITERAL", out)

    def test_reports_host_only_for_endpoint_override(self):
        _, out = run({"provider": {"vercel": {"options": {"baseURL": "https://nongateway.example/v1?k=" + SECRET}}}})
        self.assertIn("host=nongateway.example", out)
        self.assertNotIn(SECRET, out)

    def test_reports_provider_prefixes_for_models_and_fallbacks(self):
        _, out = run({"model": "opencode/beam-free", "agents": {"a": {"fallback_models": ["vercel/x/y", "opencode/z"]}}})
        self.assertIn("provider-prefix=opencode", out)
        self.assertIn("prefixes=['vercel', 'opencode']", out)

    def test_reads_jsonc_comments_trailing_commas_and_keeps_urls_in_strings(self):
        text = '{\n // a comment\n "model": "vercel/a/b", /* block */\n "u": "https://x.example/a//b",\n "env": {"ANTHROPIC_BASE_URL": "https://proxy.example/v1",},\n}\n'
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "omo.jsonc"
            path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = audit_inspect.main([str(path)])
        self.assertEqual(code, 0)
        self.assertIn("provider-prefix=vercel", out.getvalue())
        self.assertIn("ENDPOINT /env/ANTHROPIC_BASE_URL: host=proxy.example", out.getvalue())

    def test_reports_anthropic_base_url_host_only(self):
        _, out = run({"env": {"ANTHROPIC_BASE_URL": "https://u:" + SECRET + "@gw.example/v1", "ANTHROPIC_AUTH_TOKEN": SECRET}})
        self.assertIn("host=gw.example", out)
        self.assertNotIn(SECRET, out)

    def test_unreadable_file_is_reported_without_echoing_content(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "config.toml"
            path.write_text('api_key = "' + SECRET + '"\n', encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = audit_inspect.main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("UNREADABLE", out.getvalue())
        self.assertNotIn(SECRET, out.getvalue())

    def test_no_arguments_prints_usage_and_exits_2(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(audit_inspect.main([]), 2)


if __name__ == "__main__":
    unittest.main()
