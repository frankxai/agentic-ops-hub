import copy
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("receipt_bridge", ROOT / "lab" / "receipt_bridge.py")
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)

SIS = Path(os.environ.get("SIS_REPO", r"C:\Users\frank\Starlight-Intelligence-System"))
VENDORED = ROOT / "lab" / "vendor" / "run-receipt.v1.schema.json"
SHA = "a" * 64
FX = 0.9


def call(i=0, ok=True, usd=0.01, ts="2026-10-21T10:00:05+00:00", **extra):
    rec = {"ts": ts, "id": f"c{i}", "task_class": "code", "primary": "vercel/zai/glm-5.3", "used": "vercel/zai/glm-5.3",
           "fallback_used": False, "cost_usd": usd, "latency_ms": 5000, "success": ok, "provider": "token-pass",
           "machine": "c940", "over_ceiling": False, "zdr_override": False, "synthetic": False}
    rec.update(extra)
    return rec


def build(calls=None, passed=True, actor="codex", host="opencode-bare", **kw):
    return bridge.build_receipt(
        calls if calls is not None else [call()],
        run={"id": "run_1", "kind": "lab.core-v0.pr-replay-fix", "host": host, "correlation_id": "EXP-008:t1"},
        subject={"name": "patch.diff", "sha256": SHA},
        verifier={"actor": actor, "checker": "pytest", "passed": passed, "at": "2026-10-21T10:00:30+00:00",
                  "evidence_ref": "results/t1/pytest.txt", "evidence_sha256": SHA},
        fx_eur_per_usd=FX,
        evidence=[{"kind": "routing-detail", "ref": "results/t1/routing.jsonl", "sha256": SHA}],
        now="2026-10-21T10:01:00+00:00", **kw)


class ShapeTests(unittest.TestCase):
    def test_validates_against_the_vendored_v1_schema(self):
        import jsonschema
        schema = json.loads(VENDORED.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(build())

    def test_cost_is_converted_with_the_stated_rate_and_kept_in_usd_in_the_note(self):
        r = build([call(usd=0.10)])
        self.assertAlmostEqual(r["stages"][0]["costEur"], 0.09)
        self.assertIn("usd=0.1", r["stages"][0]["note"])
        self.assertIn("fx=0.9", r["stages"][0]["note"])

    def test_totals_are_never_below_the_stage_sums(self):
        r = build([call(0, usd=0.01), call(1, usd=0.02, ts="2026-10-21T10:00:12+00:00")])
        self.assertGreaterEqual(r["totals"]["costEur"] + 1e-12, sum(s.get("costEur", 0) for s in r["stages"]))
        self.assertGreaterEqual(r["totals"]["latencyMs"], max(s.get("latencyMs", 0) for s in r["stages"]))

    def test_synthetic_calls_are_refused(self):
        with self.assertRaises(ValueError):
            build([call(synthetic=True)])

    def test_fx_rate_is_required(self):
        with self.assertRaises(ValueError):
            bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": SHA},
                                 verifier={"actor": "codex", "checker": "t", "passed": True, "at": "2026-10-21T10:00:30+00:00"},
                                 fx_eur_per_usd=None, evidence=[], now="2026-10-21T10:01:00+00:00")

    def test_evidence_needs_a_sha256(self):
        with self.assertRaises(ValueError):
            bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": SHA},
                                 verifier={"actor": "codex", "checker": "t", "passed": True, "at": "2026-10-21T10:00:30+00:00"},
                                 fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": "nope"}],
                                 now="2026-10-21T10:01:00+00:00")


class AcceptanceTests(unittest.TestCase):
    def test_clean_pass_is_pass_and_accepted(self):
        r = build()
        self.assertEqual(r["verdict"], "PASS")
        self.assertTrue(bridge.accepted(r))

    def test_fallback_walk_is_partial_but_still_accepted(self):
        r = build([call(0, ok=False, usd=0.0), call(1, ok=True, ts="2026-10-21T10:00:12+00:00", fallback_used=True)])
        self.assertEqual(r["verdict"], "PARTIAL")
        self.assertTrue(bridge.accepted(r))

    def test_failed_checker_is_not_accepted(self):
        r = build(passed=False)
        self.assertFalse(bridge.accepted(r))
        self.assertNotEqual(r["verdict"], "PASS")

    def test_all_stages_failed_is_fail(self):
        r = build([call(ok=False)], passed=False)
        self.assertEqual(r["verdict"], "FAIL")

    def test_maker_cannot_be_its_own_verifier(self):
        r = build(actor="opencode-bare", host="opencode-bare")
        self.assertTrue(any("maker" in p for p in bridge.separation_problems(r)))
        self.assertFalse(bridge.accepted(r))

    def test_different_actor_passes_separation(self):
        self.assertEqual(bridge.separation_problems(build()), [])

    def test_a_receipt_without_an_accept_decision_is_not_accepted(self):
        r = build()
        r = copy.deepcopy(r)
        r["decisions"] = [d for d in r["decisions"] if d["gate"] != "accept"]
        self.assertFalse(bridge.accepted(r))

    def test_zdr_override_is_recorded_as_a_decision(self):
        r = build([call(zdr_override=True)])
        zdr = [d for d in r["decisions"] if d["gate"] == "zdr"]
        self.assertEqual(zdr[0]["outcome"], "rejected")


class StrictInputTests(unittest.TestCase):
    """Codex review of PR 379: malformed input must be refused, never coerced into a successful receipt."""

    def test_truthy_non_boolean_synthetic_is_refused(self):
        for bad in (1, "yes", "false", [1]):
            with self.assertRaises(ValueError, msg=repr(bad)):
                build([call(synthetic=bad)])

    def test_string_booleans_are_not_success(self):
        with self.assertRaises(ValueError):
            build([call(ok="false")])
        with self.assertRaises(ValueError):
            build(passed="false")
        with self.assertRaises(ValueError):
            build([call(fallback_used="no")])

    def test_bad_numbers_are_refused(self):
        for field, bad in (("latency_ms", -1), ("latency_ms", float("nan")), ("cost_usd", True), ("cost_usd", -0.1),
                           ("input_tokens", -3), ("input_tokens", 1.5), ("output_tokens", True)):
            with self.assertRaises(ValueError, msg=f"{field}={bad!r}"):
                build([call(**{field: bad})])

    def test_bad_verifier_latency_is_refused(self):
        for bad in (-5, float("nan"), float("inf")):
            with self.assertRaises(ValueError, msg=repr(bad)):
                bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": SHA},
                                     verifier={"actor": "codex", "checker": "t", "passed": True, "latency_ms": bad,
                                               "at": "2026-10-21T10:00:30+00:00"},
                                     fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA}],
                                     now="2026-10-21T10:01:00+00:00")

    def test_subject_digest_must_be_a_sha256(self):
        for bad in ("nope", "A" * 64, "a" * 63, None):
            with self.assertRaises(ValueError, msg=repr(bad)):
                bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": bad},
                                     verifier={"actor": "codex", "checker": "t", "passed": True, "at": "2026-10-21T10:00:30+00:00"},
                                     fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA}],
                                     now="2026-10-21T10:01:00+00:00")

    def test_evidence_with_extra_keys_is_refused(self):
        with self.assertRaises(ValueError):
            bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": SHA},
                                 verifier={"actor": "codex", "checker": "t", "passed": True, "at": "2026-10-21T10:00:30+00:00"},
                                 fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA, "extra": 1}],
                                 now="2026-10-21T10:01:00+00:00")

    def test_note_delimiters_cannot_be_injected(self):
        for field in ("primary", "used", "task_class", "id"):
            for bad in ("x;usd=0;fx=0", "a=b", "line\nbreak", "tab\tbed"):
                with self.assertRaises(ValueError, msg=f"{field}={bad!r}"):
                    build([call(**{field: bad})])

    def test_checker_name_cannot_carry_delimiters(self):
        with self.assertRaises(ValueError):
            bridge.build_receipt([call()], run={"id": "r", "kind": "k", "host": "h"}, subject={"name": "x", "sha256": SHA},
                                 verifier={"actor": "codex", "checker": "pytest;provenance=verified", "passed": True,
                                           "at": "2026-10-21T10:00:30+00:00"},
                                 fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA}],
                                 now="2026-10-21T10:01:00+00:00")

    def test_returned_receipt_is_always_schema_valid(self):
        import jsonschema
        schema = json.loads(VENDORED.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        for receipt in (build(), build(passed=False), build([call(0, ok=False), call(1, ts="2026-10-21T10:00:12+00:00")])):
            self.assertEqual(list(validator.iter_errors(receipt)), [])


class IdentityAndBindingTests(unittest.TestCase):
    def test_actor_comparison_ignores_case_and_whitespace(self):
        for actor in ("OpenCode-Bare", "opencode-bare ", "  OPENCODE-BARE"):
            r = build(actor=actor, host="opencode-bare")
            self.assertTrue(any("maker" in p for p in bridge.separation_problems(r)), actor)
            self.assertFalse(bridge.accepted(r), actor)

    def test_a_decoy_checker_stage_cannot_launder_a_failed_check(self):
        r = copy.deepcopy(build(passed=False))
        r["stages"].insert(0, {"name": "verify:decoy", "status": "ok"})
        self.assertFalse(bridge.accepted(r))
        self.assertTrue(any("exactly one checker" in p for p in bridge.separation_problems(r)))

    def test_accept_decision_must_name_the_checker_stage(self):
        r = copy.deepcopy(build())
        next(d for d in r["decisions"] if d["gate"] == "accept")["note"] = "checker=other;provenance=self-asserted"
        self.assertTrue(any("does not name" in p for p in bridge.separation_problems(r)))
        self.assertFalse(bridge.accepted(r))

    def test_two_accept_decisions_are_ambiguous(self):
        r = copy.deepcopy(build())
        r["decisions"].append(copy.deepcopy(next(d for d in r["decisions"] if d["gate"] == "accept")))
        self.assertFalse(bridge.accepted(r))

    def test_accept_decision_is_labelled_self_asserted(self):
        r = build()
        accept = next(d for d in r["decisions"] if d["gate"] == "accept")
        self.assertIn("provenance=self-asserted", accept["note"])

    def test_a_schema_invalid_receipt_is_never_accepted(self):
        r = copy.deepcopy(build())
        r["stages"][0]["latencyMs"] = -1
        self.assertFalse(bridge.accepted(r))

    def test_human_approval_needs_a_real_reference(self):
        for bad in ("urn:fake", "", None, "http://insecure.example/x", "trust me"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                bridge.build_receipt(
                    [call()], run={"id": "r", "kind": "k", "host": "opencode-bare"}, subject={"name": "x", "sha256": SHA},
                    verifier={"actor": "frank", "checker": "review", "passed": True, "decided_by": "human",
                              "approval_ref": bad, "at": "2026-10-21T10:00:30+00:00"},
                    fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA}], now="2026-10-21T10:01:00+00:00")

    def test_human_approval_accepts_https_and_github_references(self):
        for ref, expected in (("https://github.com/frankxai/agentic-ops-hub/pull/377", "https://github.com/frankxai/agentic-ops-hub/pull/377"),
                              ("frankxai/agentic-ops-hub#377", "gh:frankxai/agentic-ops-hub#377"),
                              ("gh:frankxai/agentic-ops-hub@bc7427b", "gh:frankxai/agentic-ops-hub@bc7427b")):
            r = bridge.build_receipt(
                [call()], run={"id": "r", "kind": "k", "host": "opencode-bare"}, subject={"name": "x", "sha256": SHA},
                verifier={"actor": "frank", "checker": "review", "passed": True, "decided_by": "human",
                          "approval_ref": ref, "at": "2026-10-21T10:00:30+00:00"},
                fx_eur_per_usd=FX, evidence=[{"kind": "k", "ref": "r", "sha256": SHA}], now="2026-10-21T10:01:00+00:00")
            accept = next(d for d in r["decisions"] if d["gate"] == "accept")
            self.assertEqual(accept["approvalRef"], expected)
            self.assertTrue(bridge.accepted(r))


@unittest.skipUnless((SIS / "protocol" / "run-receipt.v1.schema.json").exists(), "SIS checkout not present")
class ConformanceTests(unittest.TestCase):
    def test_vendored_schema_matches_sis(self):
        self.assertEqual(VENDORED.read_bytes(), (SIS / "protocol" / "run-receipt.v1.schema.json").read_bytes())

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_sis_own_validator_accepts_the_receipt(self):
        script = ("import { readFileSync } from 'node:fs';\nimport { receiptProblems } from %s;\n"
                  "const r = JSON.parse(readFileSync(process.argv[2], 'utf8'));\nconsole.log(JSON.stringify(receiptProblems(r)));\n"
                  % json.dumps((SIS / "src" / "run-receipt.ts").as_uri()))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "check.mts"
            path.write_text(script, encoding="utf-8")
            data = Path(tmp) / "receipt.json"
            data.write_text(json.dumps(build()), encoding="utf-8")
            out = subprocess.run(["node", "--experimental-strip-types", str(path), str(data)],
                                 capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr[-400:])
        self.assertEqual(json.loads(out.stdout.strip().splitlines()[-1]), [])


if __name__ == "__main__":
    unittest.main()
