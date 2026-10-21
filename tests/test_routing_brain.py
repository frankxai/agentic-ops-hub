import json
import math
import multiprocessing
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

FLEET = Path(__file__).resolve().parents[1] / "fleet"
sys.path.insert(0, str(FLEET))

import gen_omo_config  # noqa: E402
import route_classifier  # noqa: E402
import route_executor  # noqa: E402
import weekly_routing_review as review  # noqa: E402

SCHEMA = json.loads((FLEET / "routing.schema.json").read_text(encoding="utf-8"))
PAID_PREFIXES = ("openai/", "anthropic/", "google/", "groq/", "openrouter/", "xai/")


def _write_worker(args):
    d, n = args
    os.environ["STARLIGHT_RECEIPTS_DIR"] = d
    for _ in range(n):
        route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True,
                                      synthetic=True)


class TmpLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": self.tmp.name})
        p.start()
        self.addCleanup(p.stop)
        self.ledger = Path(self.tmp.name) / "routing.jsonl"


class CostGuards(TmpLedger):
    def test_nan_and_inf_costs_are_rejected(self):
        for bad in (float("nan"), float("inf"), -1.0):
            with self.assertRaises(ValueError):
                route_executor.record_receipt("code", "vercel/zai/glm-5.3", False, bad, 10, True)
        self.assertFalse(self.ledger.exists())

    def test_over_ceiling_is_recorded_and_flagged(self):
        r = route_executor.record_receipt("code", "vercel/zai/glm-5.3", False, 3.75, 10, False)
        self.assertTrue(r["over_ceiling"])
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)

    def test_free_class_ceiling_is_zero(self):
        r = route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0.0001, 5, True)
        self.assertTrue(r["over_ceiling"])

    def test_off_chain_model_rejected(self):
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", "openai/gpt-6-luna", False, 0.1, 5, True)

    def test_preflight_blocks_over_ceiling_estimate(self):
        with self.assertRaises(route_executor.BudgetError):
            route_executor.preflight("code", "vercel/zai/glm-5.3", 0.51)

    def test_preflight_rejects_nan_estimate(self):
        with self.assertRaises(ValueError):
            route_executor.preflight("code", "vercel/zai/glm-5.3", float("nan"))

    def test_hard_cap_blocks_paid_but_not_free(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        with patch.object(route_executor, "month_paid_spend", return_value=cap - 0.01):
            with self.assertRaises(route_executor.BudgetError):
                route_executor.preflight("code", "vercel/zai/glm-5.3", 0.05)
            route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", 0)


class ZdrEnforcement(unittest.TestCase):
    def test_zdr_required_classes_exclude_free_fallbacks(self):
        for cls, d in SCHEMA["task_classes"].items():
            if d["zdr_required"]:
                chain = route_executor.route(cls)["chain"]
                self.assertTrue(all(m.startswith("vercel/") for m in chain), (cls, chain))

    def test_override_restores_free_fallbacks_and_is_stamped(self):
        r = route_executor.route("code", allow_non_zdr=True)
        self.assertIn("opencode/beam-free", r["chain"])
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": d}):
            rec = route_executor.record_receipt("code", "opencode/beam-free", True, 0, 5, True,
                                                allow_non_zdr=True)
            self.assertTrue(rec["zdr_override"])
            with self.assertRaises(ValueError):
                route_executor.record_receipt("code", "opencode/beam-free", True, 0, 5, True)

    def test_free_classes_never_resolve_to_paid_models(self):
        for cls in ("scout", "review", "vision"):
            for m in route_executor.route(cls)["chain"]:
                self.assertTrue(m.startswith("opencode/"), (cls, m))

    def test_pick_next_returns_none_when_exhausted(self):
        chain = route_executor.route("scout")["chain"]
        self.assertIsNone(route_executor.pick_next(chain, "scout"))


class Ledger(TmpLedger):
    def test_concurrent_writers_lose_nothing(self):
        procs, per = 6, 60
        with multiprocessing.Pool(procs) as pool:
            pool.map(_write_worker, [(self.tmp.name, per)] * procs)
        lines = self.ledger.read_bytes().splitlines()
        self.assertEqual(len(lines), procs * per)
        for ln in lines:
            json.loads(ln)

    def test_lf_line_endings(self):
        route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True)
        self.assertNotIn(b"\r", self.ledger.read_bytes())

    def test_receipt_timestamp_is_utc(self):
        r = route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True)
        self.assertEqual(datetime.fromisoformat(r["ts"]).utcoffset(), timedelta(0))


class Classifier(unittest.TestCase):
    CASES = {
        "where is the plan file": "scout",
        "search the repo for the word complex": "scout",
        "find the reason this import fails": "scout",
        "list all files in src": "scout",
        "summarize README": "scout",
        "hello there": "code",
        "write a novel caching layer": "code",
        "refactor the auth module": "code",
        "review this PR for style": "review",
        "extract all emails from every log": "bulk",
        "analyze this screenshot": "vision",
        "find the root cause of the crash": "hard-reasoning",
        "build a greenfield app from scratch": "ultrabrain",
    }

    def test_ordinary_phrasings(self):
        for task, want in self.CASES.items():
            self.assertEqual(route_classifier.classify(task)["class"], want, task)

    def test_unmatched_text_defaults_to_a_zdr_class(self):
        c = route_classifier.classify("zzz qqq")
        self.assertEqual(c["source"], "default-zdr")
        self.assertTrue(SCHEMA["task_classes"][c["class"]]["zdr_required"])


class WeeklyReview(TmpLedger):
    def _line(self, **kw):
        base = {"ts": datetime.now(timezone.utc).isoformat(), "task_class": "code",
                "used": "vercel/zai/glm-5.3", "success": True, "cost_usd": 0.1, "latency_ms": 5}
        return json.dumps({**base, **kw})

    def test_malformed_incomplete_synthetic_and_nan_lines_are_skipped(self):
        lines = [self._line(), '{"ts": "torn', json.dumps({"ts": "x"}), self._line(synthetic=True),
                 self._line().replace("0.1", "NaN")]
        self.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(len(got), 1)
        self.assertEqual(skipped, {"malformed": 1, "incomplete": 1, "synthetic": 1, "non_finite": 1})

    def test_unknown_class_does_not_crash(self):
        got = [{"task_class": "nonsense", "used": "x", "success": True, "cost_usd": 0.0, "latency_ms": 1.0}] * 30
        self.assertEqual(review.analyze(got, SCHEMA), {})

    def _receipts(self, model, n, ok):
        return [{"ts": "2026-10-21T00:00:00+00:00", "task_class": "code", "used": model, "success": ok,
                 "cost_usd": 0.1, "latency_ms": 5.0}] * n

    def test_no_proposal_from_a_single_sample_primary(self):
        rs = self._receipts("vercel/zai/glm-5.3", 1, False) + self._receipts("vercel/deepseek/deepseek-v4.1-flash", 19, True)
        self.assertEqual(review.propose(review.analyze(rs, SCHEMA), SCHEMA), [])

    def test_proposal_target_must_be_zdr_safe(self):
        rs = self._receipts("vercel/zai/glm-5.3", 10, False) + self._receipts("opencode/beam-free", 15, True)
        self.assertEqual(review.propose(review.analyze(rs, SCHEMA), SCHEMA), [])

    def test_valid_proposal_is_made(self):
        rs = self._receipts("vercel/zai/glm-5.3", 10, False) + self._receipts("vercel/deepseek/deepseek-v4.1-flash", 15, True)
        props = review.propose(review.analyze(rs, SCHEMA), SCHEMA)
        self.assertEqual(props[0]["to"], "vercel/deepseek/deepseek-v4.1-flash")

    def test_report_is_strict_json_and_utc(self):
        with tempfile.TemporaryDirectory() as d, patch.object(review, "PROPOSALS", Path(d)):
            review.main()
            report = json.loads(next(Path(d).iterdir()).read_text(), parse_constant=lambda c: self.fail(c))
            self.assertEqual(datetime.fromisoformat(report["generated"]).utcoffset(), timedelta(0))


class OmoGenerator(unittest.TestCase):
    def test_no_slot_is_bare_or_paid_outside_the_schema(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        known = set(route_executor.zdr_models(SCHEMA)) | {
            m for d in SCHEMA["task_classes"].values() for m in [d["primary"], *d["fallbacks"]]}

        def names(models):
            return [m["model"] if isinstance(m, dict) else m for m in models]

        for agent, v in cfg["agents"].items():
            for m in names(v["models"]):
                self.assertIn(m, known, (agent, m))
                self.assertFalse(m.startswith(PAID_PREFIXES), (agent, m))
        for cat, v in cfg["categories"].items():
            for m in [v["model"], *names(v.get("fallback_models", []))]:
                self.assertIn(m, known, (cat, m))

    def test_builtin_paid_slots_are_covered(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        for agent in ("sisyphus-junior",):
            self.assertIn(agent, cfg["agents"])
        for cat in ("deep-high", "deep-low", "artistry"):
            self.assertIn(cat, cfg["categories"])

    def test_hephaestus_allows_non_gpt(self):
        self.assertTrue(gen_omo_config.build(SCHEMA)["[opencode]"]["agents"]["hephaestus"]["allow_non_gpt_model"])

    def test_zdr_agents_have_no_free_fallback(self):
        agents = gen_omo_config.build(SCHEMA)["[opencode]"]["agents"]
        for m in agents["sisyphus"]["models"]:
            name = m["model"] if isinstance(m, dict) else m
            self.assertTrue(name.startswith("vercel/"), name)

    def test_dry_run_and_out_do_not_touch_home(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "omo.jsonc"
            gen_omo_config.main(["--out", str(out)])
            gen_omo_config.main(["--out", str(out)])
            self.assertTrue(out.exists())
            self.assertEqual(len(list(Path(d).glob("omo.jsonc.bak.*"))), 1)
            json.loads(out.read_text().split("\n", 1)[1])


class Cli(TmpLedger):
    def run_cli(self, *args):
        env = {**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name}
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"), *args],
                              capture_output=True, text=True, env=env)

    def test_over_ceiling_exits_3_but_records(self):
        p = self.run_cli("refactor the auth module", "--record", "success", "--used", "vercel/zai/glm-5.3",
                         "--cost", "0.9", "--latency", "10", "--synthetic")
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)

    def test_nan_cost_exits_2(self):
        p = self.run_cli("refactor the auth module", "--record", "success", "--used", "vercel/zai/glm-5.3",
                         "--cost", "nan", "--latency", "10")
        self.assertEqual(p.returncode, 2)
        self.assertFalse(self.ledger.exists())

    def test_preflight_ok(self):
        p = self.run_cli("refactor the auth module", "--preflight", "--est-cost", "0.1")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["class"], "code")


def _reserve_worker(args):
    d, est = args
    os.environ["STARLIGHT_RECEIPTS_DIR"] = d
    try:
        route_executor.reserve("code", "vercel/zai/glm-5.3", est)
        return True
    except route_executor.BudgetError:
        return False


class BudgetReservation(TmpLedger):
    GLM = "vercel/zai/glm-5.3"

    def test_second_admission_cannot_pass_the_cap(self):
        with patch.object(route_executor, "month_paid_spend", return_value=79.70):
            route_executor.reserve("code", self.GLM, 0.20)
            with self.assertRaises(route_executor.BudgetError):
                route_executor.reserve("code", self.GLM, 0.20)

    def test_settling_releases_the_reservation(self):
        res = route_executor.reserve("code", self.GLM, 0.20)
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.20)
        route_executor.record_receipt("code", self.GLM, False, 0.05, 10, True,
                                      reservation_id=res["reservation_id"])
        self.assertEqual(route_executor.reserved_usd(), 0.0)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.05)

    def test_stale_reservation_keeps_counting_until_reconciled(self):
        res = route_executor.reserve("code", self.GLM, 0.20)
        later = datetime.now(timezone.utc) + timedelta(seconds=route_executor.RESERVATION_TTL_S + 5)
        self.assertAlmostEqual(route_executor.reserved_usd(now=later), 0.20)
        states = {r["id"]: r["status"] for r in route_executor.reservations(now=later)}
        self.assertEqual(states[res["reservation_id"]], "expired-unsettled")
        route_executor.release_reservation(res["reservation_id"], "caller confirmed the call never ran")
        self.assertEqual(route_executor.reserved_usd(now=later), 0.0)

    def test_free_models_reserve_nothing(self):
        res = route_executor.reserve("scout", "opencode/mimo-v2.6-flash-free", None)
        self.assertIsNone(res["reservation_id"])
        self.assertFalse((Path(self.tmp.name) / "reservations.jsonl").exists())

    def test_concurrent_reservations_never_exceed_the_cap(self):
        route_executor.record_receipt("code", self.GLM, False, 79.0, 10, True, synthetic=True)
        with multiprocessing.Pool(6) as pool:
            admitted = pool.map(_reserve_worker, [(self.tmp.name, 0.5)] * 6)
        self.assertEqual(sum(admitted), 2)

    def test_missing_or_zero_estimate_is_refused_for_paid_models(self):
        for est in (None, 0, 0.0):
            with self.assertRaises(ValueError):
                route_executor.preflight("code", self.GLM, est)
        route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", None)

    def test_paid_admission_stops_once_the_cap_is_reached(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        with patch.object(route_executor, "month_paid_spend", return_value=cap):
            with self.assertRaises(route_executor.BudgetError):
                route_executor.preflight("code", self.GLM, 0.0001)

    def test_cli_preflight_reserves_and_record_settles(self):
        env = {**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name}

        def run(*a):
            return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"), *a],
                                  capture_output=True, text=True, env=env)

        no_est = run("refactor the auth module", "--preflight")
        self.assertEqual(no_est.returncode, 2, no_est.stderr)
        pre = run("refactor the auth module", "--preflight", "--est-cost", "0.2")
        self.assertEqual(pre.returncode, 0, pre.stderr)
        rid = json.loads(pre.stdout)["reservation_id"]
        self.assertTrue(rid)
        rec = run("refactor the auth module", "--record", "success", "--used", self.GLM, "--cost", "0.05",
                  "--latency", "10", "--reservation", rid, "--synthetic")
        self.assertEqual(rec.returncode, 0, rec.stderr)
        with patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": self.tmp.name}):
            self.assertEqual(route_executor.reserved_usd(), 0.0)


class SharedLedgerRoot(unittest.TestCase):
    def test_default_follows_schema_root_not_the_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            schema = {**SCHEMA, "receipts": {**SCHEMA["receipts"], "root": d}}
            env = {k: v for k, v in os.environ.items() if k != "STARLIGHT_RECEIPTS_DIR"}
            with patch.dict(os.environ, env, clear=True), patch.object(route_executor, "load_schema",
                                                                        return_value=schema):
                self.assertEqual(route_executor.receipts_dir(), Path(d))

    def test_env_override_wins(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": d}):
            self.assertEqual(route_executor.receipts_dir(), Path(d))

    def test_unusable_root_falls_back_to_checkout(self):
        schema = {**SCHEMA, "receipts": {"root": "relative/or/foreign"}}
        env = {k: v for k, v in os.environ.items() if k != "STARLIGHT_RECEIPTS_DIR"}
        with patch.dict(os.environ, env, clear=True), patch.object(route_executor, "load_schema",
                                                                    return_value=schema):
            self.assertEqual(route_executor.receipts_dir(), route_executor.DEFAULT_RECEIPTS_DIR)


class ClassifierZdrPrecedence(unittest.TestCase):
    CODING = [
        "fix the screenshot upload bug",
        "implement the audit logging module",
        "update the function that handles video uploads",
        "refactor the lint config",
        "add a test for the multimodal parser",
    ]

    def test_coding_requests_never_land_in_a_non_zdr_class(self):
        for task in self.CODING:
            c = route_classifier.classify(task)
            self.assertTrue(c["zdr_required"], (task, c["class"]))

    def test_plain_vision_and_review_stay_free(self):
        self.assertEqual(route_classifier.classify("analyze this screenshot")["class"], "vision")
        self.assertEqual(route_classifier.classify("review this PR for style")["class"], "review")


class ReviewTypeSafety(TmpLedger):
    def _line(self, **kw):
        base = {"ts": datetime.now(timezone.utc).isoformat(), "task_class": "code",
                "used": "vercel/zai/glm-5.3", "success": True, "cost_usd": 0.1, "latency_ms": 5}
        return json.dumps({**base, **kw})

    def test_wrongly_typed_fields_are_skipped_not_fatal(self):
        bad = [self._line(task_class=[]), self._line(used={"a": 1}), self._line(success="yes"),
               self._line(task_class=None)]
        self.ledger.write_text("\n".join([self._line(), *bad]) + "\n", encoding="utf-8")
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(len(got), 1)
        self.assertEqual(skipped["malformed"], len(bad))
        review.analyze(got, SCHEMA)

    def test_analyze_tolerates_unhashable_class_directly(self):
        rs = [{"task_class": [], "used": "x", "success": True, "cost_usd": 0.0, "latency_ms": 1.0}]
        self.assertEqual(review.analyze(rs, SCHEMA), {})


class OmoSlotCoverage(unittest.TestCase):
    AGENTS = {"sisyphus", "sisyphus-junior", "hephaestus", "oracle", "prometheus", "metis", "atlas",
              "librarian", "explore", "multimodal-looker", "momus"}
    CATEGORIES = {"visual-engineering", "ultrabrain", "deep", "deep-low", "deep-high", "artistry", "quick",
                  "unspecified-low", "unspecified-high", "writing", "research", "bulk-extraction",
                  "code-review"}

    def test_generated_slots_match_the_expected_set_exactly(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        self.assertEqual(set(cfg["agents"]), self.AGENTS)
        self.assertEqual(set(cfg["categories"]), self.CATEGORIES)

    def test_every_category_pins_its_fallbacks_explicitly(self):
        cats = gen_omo_config.build(SCHEMA)["[opencode]"]["categories"]
        for cat, v in cats.items():
            self.assertIn("fallback_models", v, cat)
        # Never empty for a ZDR class: OmO turns [] into undefined and then inherits
        # the delegating agent's (free) fallbacks. A singleton chain repeats its primary.
        self.assertEqual(cats["bulk-extraction"]["fallback_models"], [cats["bulk-extraction"]["model"]])

    def test_zdr_categories_never_list_a_non_zdr_fallback(self):
        cats = gen_omo_config.build(SCHEMA)["[opencode]"]["categories"]
        safe = route_executor.zdr_models(SCHEMA)
        for cat, cls in gen_omo_config.CATEGORY_MAP.items():
            if SCHEMA["task_classes"][cls]["zdr_required"]:
                for m in [cats[cat]["model"], *cats[cat]["fallback_models"]]:
                    name = m["model"] if isinstance(m, dict) else m
                    self.assertIn(name, safe, (cat, name))


class OmoNormalizationCollapse(unittest.TestCase):
    """OmO's applyDisabledProviders() turns an empty fallback_models list into undefined,
    and resolution then inherits the delegating agent's fallbacks (free models)."""

    @staticmethod
    def _collapse(fallbacks):
        return fallbacks if fallbacks else None

    def test_no_zdr_category_can_collapse_to_inherited_free_fallbacks(self):
        cats = gen_omo_config.build(SCHEMA)["[opencode]"]["categories"]
        safe = route_executor.zdr_models(SCHEMA)
        for cat, cls in gen_omo_config.CATEGORY_MAP.items():
            if not SCHEMA["task_classes"][cls]["zdr_required"]:
                continue
            kept = self._collapse(cats[cat]["fallback_models"])
            self.assertIsNotNone(kept, cat)
            for m in kept:
                self.assertIn(m["model"] if isinstance(m, dict) else m, safe, (cat, m))


class ClassifierFailClosed(unittest.TestCase):
    CODING = [
        "update the screenshot upload handler",
        "patch the video parser",
        "add screenshot upload validation",
        "remove the audit endpoint",
        "add a screenshot test",
        "patch the video audit",
        "delete the lint step from the pipeline",
        "the upload handler crashes on large screenshots",
        "migrate the audit table",
    ]
    READ_ONLY = {
        "analyze this screenshot": "vision",
        "review this PR for style": "review",
        "audit the dependency list": "review",
        "find the reason this import fails": "scout",
        "explain the multimodal parser": "scout",
    }

    def test_coding_requests_with_media_or_audit_nouns_stay_zdr(self):
        for task in self.CODING:
            c = route_classifier.classify(task)
            self.assertTrue(c["zdr_required"], (task, c["class"]))

    def test_explicit_read_only_requests_may_use_free_classes(self):
        for task, want in self.READ_ONLY.items():
            self.assertEqual(route_classifier.classify(task)["class"], want, task)

    def test_text_with_no_signal_is_zdr(self):
        self.assertTrue(route_classifier.classify("zzz qqq")["zdr_required"])


class ReservationBinding(TmpLedger):
    GLM = "vercel/zai/glm-5.3"
    FLASH = "vercel/deepseek/deepseek-v4.1-flash"
    FREE = "opencode/mimo-v2.6-flash-free"

    def _age_reservations(self, seconds):
        path = Path(self.tmp.name) / "reservations.jsonl"
        out = []
        for line in path.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e.get("kind") == "reserve":
                e["ts"] = (datetime.fromisoformat(e["ts"]) - timedelta(seconds=seconds)).isoformat()
            out.append(json.dumps(e))
        path.write_text("\n".join(out) + "\n", encoding="utf-8")

    def test_expiry_does_not_release_budget_for_a_possibly_running_call(self):
        with patch.object(route_executor, "month_paid_spend", return_value=79.50):
            route_executor.reserve("code", self.GLM, 0.50)
            self._age_reservations(route_executor.RESERVATION_TTL_S)
            with self.assertRaises(route_executor.BudgetError):
                route_executor.reserve("code", self.GLM, 0.50)

    def test_late_settle_replaces_the_hold_and_never_adds(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        self._age_reservations(route_executor.RESERVATION_TTL_S + 60)
        route_executor.record_receipt("code", self.GLM, False, 0.30, 10, True,
                                      reservation_id=res["reservation_id"])
        self.assertEqual(route_executor.reserved_usd(), 0.0)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.30)

    def test_unrelated_receipt_cannot_settle_a_reservation(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        with self.assertRaises(ValueError):
            route_executor.record_receipt("scout", self.FREE, False, 0, 5, True,
                                          reservation_id=res["reservation_id"])
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.FLASH, True, 0.01, 5, True,
                                          reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)
        self.assertFalse(self.ledger.exists())

    def test_unknown_and_already_settled_ids_are_refused(self):
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.01, 5, True, reservation_id="nope")
        res = route_executor.reserve("code", self.GLM, 0.50)
        route_executor.record_receipt("code", self.GLM, False, 0.10, 5, True,
                                      reservation_id=res["reservation_id"])
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.10, 5, True,
                                          reservation_id=res["reservation_id"])

    def test_spend_plus_holds_never_pass_the_cap_after_a_mismatch_attempt(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        with patch.object(route_executor, "month_paid_spend", return_value=cap - 0.50):
            res = route_executor.reserve("code", self.GLM, 0.50)
            with self.assertRaises(ValueError):
                route_executor.record_receipt("scout", self.FREE, False, 0, 5, True,
                                              reservation_id=res["reservation_id"])
            with self.assertRaises(route_executor.BudgetError):
                route_executor.reserve("code", self.GLM, 0.50)


class SubMicroEstimates(TmpLedger):
    GLM = "vercel/zai/glm-5.3"

    def test_tiny_estimates_are_rounded_up_and_still_consume_headroom(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        admitted = 0
        with patch.object(route_executor, "month_paid_spend", return_value=cap - 0.000001):
            for _ in range(10):
                try:
                    route_executor.reserve("code", self.GLM, 0.0000004)
                    admitted += 1
                except route_executor.BudgetError:
                    pass
            self.assertEqual(admitted, 1)
            self.assertAlmostEqual(route_executor.reserved_usd(), 0.000001, places=9)


class UnusableSharedRoot(unittest.TestCase):
    GLM = "vercel/zai/glm-5.3"

    def _env(self):
        return {k: v for k, v in os.environ.items() if k != "STARLIGHT_RECEIPTS_DIR"}

    def test_paid_admission_is_refused_but_free_calls_still_work(self):
        schema = {**SCHEMA, "receipts": {"root": "C:/not/absolute/on/this/os/../relative"}}
        schema["receipts"]["root"] = "relative/or/foreign"
        with patch.dict(os.environ, self._env(), clear=True), \
                patch.object(route_executor, "load_schema", return_value=schema):
            for fn in (route_executor.preflight, route_executor.reserve):
                with self.assertRaises(route_executor.BudgetError) as cm:
                    fn("code", self.GLM, 0.1)
                self.assertIn("shared", str(cm.exception).lower())
            free = route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", None)
            self.assertEqual(free["model"], "opencode/mimo-v2.6-flash-free")

    def test_env_override_counts_as_a_usable_root(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": d}):
            self.assertTrue(route_executor.shared_root_usable())


class LockContention(TmpLedger):
    GLM = "vercel/zai/glm-5.3"

    def test_reserve_turns_a_lock_timeout_into_a_budget_error(self):
        import contextlib

        @contextlib.contextmanager
        def busy(_path):
            raise TimeoutError("could not lock")
            yield

        with patch.object(route_executor, "_locked", busy):
            with self.assertRaises(route_executor.BudgetError):
                route_executor.reserve("code", self.GLM, 0.1)

    def test_cli_exits_2_without_a_traceback_when_the_ledger_is_busy(self):
        self.tmp_ledger = Path(self.tmp.name) / "routing.jsonl"
        env = {**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name, "STARLIGHT_LOCK_TIMEOUT_S": "0.3"}
        with route_executor._locked(self.tmp_ledger):
            p = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"),
                                "refactor the auth module", "--preflight", "--est-cost", "0.2"],
                               capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertNotIn("Traceback", p.stderr)


class OverflowingCosts(TmpLedger):
    def test_weekly_review_counts_an_overflowing_cost_as_malformed(self):
        base = {"ts": datetime.now(timezone.utc).isoformat(), "task_class": "code",
                "used": "vercel/zai/glm-5.3", "success": True, "latency_ms": 5}
        lines = [json.dumps({**base, "cost_usd": 0.1}),
                 '{"ts": "%s", "task_class": "code", "used": "vercel/zai/glm-5.3", "success": true, '
                 '"latency_ms": 5, "cost_usd": 1%s}' % (base["ts"], "0" * 309),
                 json.dumps({**base, "cost_usd": 1e12})]
        self.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(len(got), 1)
        self.assertEqual(skipped["malformed"], 2)

    def test_spend_scan_and_receipts_survive_an_overflowing_cost(self):
        self.ledger.write_text('{"ts": "%s", "used": "vercel/zai/glm-5.3", "cost_usd": 1%s}\n'
                               % (datetime.now(timezone.utc).isoformat(), "0" * 309), encoding="utf-8")
        self.assertEqual(route_executor.month_paid_spend(), 0.0)
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", "vercel/zai/glm-5.3", False, 10 ** 309, 5, True)


if __name__ == "__main__":
    unittest.main()
