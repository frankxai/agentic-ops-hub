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
from unittest.mock import Mock, patch

FLEET = Path(__file__).resolve().parents[1] / "fleet"
sys.path.insert(0, str(FLEET))

import gen_omo_config  # noqa: E402
import route_classifier  # noqa: E402
import route_executor  # noqa: E402
import weekly_routing_review as review  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from routing_corpus import MAY_BE_FREE, MUST_BE_ZDR  # noqa: E402

SCHEMA = json.loads((FLEET / "routing.schema.json").read_text(encoding="utf-8"))
PAID_PREFIXES = ("openai/", "anthropic/", "google/", "groq/", "openrouter/", "xai/")


def _write_worker(args):
    d, n = args
    os.environ["STARLIGHT_RECEIPTS_DIR"] = d
    for _ in range(n):
        route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True,
                                      synthetic=True, allow_free=True)


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
        r = route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0.0001, 5, True, allow_free=True)
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
            route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", 0, allow_free=True)


class ZdrEnforcement(unittest.TestCase):
    def test_zdr_required_classes_exclude_free_fallbacks(self):
        for cls, d in SCHEMA["task_classes"].items():
            if d["zdr_required"]:
                chain = route_executor.route(cls, allow_free=True)["chain"]
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
            for m in route_executor.route(cls, allow_free=True)["chain"]:
                self.assertTrue(m.startswith("opencode/"), (cls, m))

    def test_pick_next_returns_none_when_exhausted(self):
        chain = route_executor.route("scout", allow_free=True)["chain"]
        self.assertIsNone(route_executor.pick_next(chain, "scout", allow_free=True))


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
        route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True, allow_free=True)
        self.assertNotIn(b"\r", self.ledger.read_bytes())

    def test_receipt_timestamp_is_utc(self):
        r = route_executor.record_receipt("scout", "opencode/mimo-v2.6-flash-free", False, 0, 5, True, allow_free=True)
        self.assertEqual(datetime.fromisoformat(r["ts"]).utcoffset(), timedelta(0))


class Classifier(unittest.TestCase):
    CASES = {
        "where is the plan file": "scout",
        "search the repo for the word 'complex'": "code",   # quoted text is never routed free (option A)
        "find the reason for the error": "scout",
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
            review.main([])
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
            json.loads("".join(l for l in out.read_text(encoding="utf-8").splitlines(True) if not l.startswith("//")))

    def test_two_runs_in_one_second_keep_the_original_backup(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "omo.jsonc"
            out.write_text("// my hand-tuned config\n", encoding="utf-8")
            for _ in range(3):
                gen_omo_config.main(["--out", str(out)])
            backups = list(Path(d).glob("omo.jsonc.bak.*"))
            self.assertEqual(len(backups), 3)
            self.assertEqual(len({b.name for b in backups}), 3)
            self.assertIn("my hand-tuned config", "".join(b.read_text(encoding="utf-8") for b in backups))

    def test_backup_never_overwrites_an_existing_file(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "omo.jsonc"
            out.write_text("original", encoding="utf-8")
            with patch.object(gen_omo_config.os, "urandom", Mock(return_value=b"\x00\x00\x01")), \
                    patch.object(gen_omo_config, "datetime") as dt:
                dt.now.return_value = datetime(2026, 10, 22, 1, 2, 3, 4, tzinfo=timezone.utc)
                first = gen_omo_config._backup(out)
                out.write_text("changed", encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    gen_omo_config._backup(out)
            self.assertEqual(first.read_text(encoding="utf-8"), "original")


def _config_body(path: Path) -> str:
    return "".join(l for l in path.read_text(encoding="utf-8").splitlines(True) if not l.startswith("//"))


class FreeAgentsMode(unittest.TestCase):
    @staticmethod
    def _models(cfg):
        names = []
        for slot in list(cfg["agents"].values()) + list(cfg["categories"].values()):
            for m in slot.get("models", []) + slot.get("fallback_models", []) + [slot.get("model")]:
                if m:
                    names.append(m["model"] if isinstance(m, dict) else m)
        return names

    def test_default_output_has_no_opencode_free_model(self):
        names = self._models(gen_omo_config.build(SCHEMA)["[opencode]"])
        self.assertTrue(names)
        self.assertEqual([n for n in names if n.startswith("opencode/")], [])

    def test_default_maps_free_classes_to_the_cheapest_zdr_model(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        cheapest = gen_omo_config.cheapest_zdr_model(SCHEMA)
        self.assertIn(cheapest, route_executor.zdr_models(SCHEMA))
        for agent in ("explore", "librarian", "momus", "multimodal-looker"):
            first = cfg["agents"][agent]["models"][0]
            self.assertEqual(first["model"] if isinstance(first, dict) else first, cheapest)
        self.assertEqual(cfg["categories"]["code-review"]["model"], cheapest)
        self.assertTrue(cfg["categories"]["code-review"]["fallback_models"])

    def test_allow_free_agents_keeps_free_models_and_says_so_in_the_header(self):
        cfg = gen_omo_config.build(SCHEMA, allow_free_agents=True)["[opencode]"]
        self.assertTrue(any(n.startswith("opencode/") for n in self._models(cfg)))
        text = gen_omo_config.render(gen_omo_config.build(SCHEMA, True), True)
        self.assertIn("outside the Vercel gateway key", text)
        self.assertIn("nothing confidential", text)

    def test_cli_flag_switches_mode(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.jsonc", Path(d) / "b.jsonc"
            gen_omo_config.main(["--out", str(a)])
            gen_omo_config.main(["--out", str(b), "--allow-free-agents"])
            self.assertNotIn("opencode/", _config_body(a))
            self.assertIn("opencode/", _config_body(b))


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

    def test_month_is_judged_in_utc_not_in_the_receipt_offset(self):
        # 2026-11-01 00:30 at +01:00 is 2026-10-31 23:30 UTC: October spend.
        rows = [{"ts": "2026-11-01T00:30:00+01:00", "id": "a", "used": self.GLM, "task_class": "code",
                 "cost_usd": 0.50, "latency_ms": 1, "success": True, "over_ceiling": False},
                {"ts": "2026-10-31T23:30:00-05:00", "id": "b", "used": self.GLM, "task_class": "code",
                 "cost_usd": 0.25, "latency_ms": 1, "success": True, "over_ceiling": False},
                {"ts": "2026-10-15T12:00:00", "id": "c", "used": self.GLM, "task_class": "code",
                 "cost_usd": 1.00, "latency_ms": 1, "success": True, "over_ceiling": False}]
        self.ledger.write_text("".join(json.dumps(r) + chr(10) for r in rows), encoding="utf-8")
        october = datetime(2026, 10, 31, 23, 45, tzinfo=timezone.utc)
        november = datetime(2026, 11, 1, 0, 15, tzinfo=timezone.utc)
        # Row b is 2026-11-01 04:30 UTC, so it is November; a and c are October.
        self.assertAlmostEqual(route_executor.month_paid_spend(october), 1.50)
        self.assertAlmostEqual(route_executor.month_paid_spend(november), 0.25)
        # The same instant expressed with an offset still lands in the same month.
        self.assertAlmostEqual(route_executor.month_paid_spend(october.astimezone(timezone(timedelta(hours=9)))), 1.50)

    def test_stale_reservation_keeps_counting_until_reconciled(self):
        res = route_executor.reserve("code", self.GLM, 0.20)
        later = datetime.now(timezone.utc) + timedelta(seconds=route_executor.RESERVATION_TTL_S + 5)
        self.assertAlmostEqual(route_executor.reserved_usd(now=later), 0.20)
        states = {r["id"]: r["status"] for r in route_executor.reservations(now=later)}
        self.assertEqual(states[res["reservation_id"]], "expired-unsettled")
        route_executor.release_reservation(res["reservation_id"], "caller confirmed the call never ran")
        self.assertEqual(route_executor.reserved_usd(now=later), 0.0)

    def test_free_models_reserve_nothing(self):
        res = route_executor.reserve("scout", "opencode/mimo-v2.6-flash-free", None, allow_free=True)
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
        route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", None, allow_free=True)

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
        "find the reason for the error": "scout",
        "explain the error log": "scout",
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


class OptionAHardening(unittest.TestCase):
    """Mechanical hardening after Codex round 6. The classifier is a cost heuristic; the ZDR-only gateway key is the guarantee."""

    def zdr(self, task):
        return route_classifier.classify(task)["zdr_required"]

    def test_verb_like_nouns_are_not_in_the_vocabulary(self):
        for word in ("code", "test", "tests", "build", "run", "set", "patch", "change", "update", "fix",
                     "import", "route", "flag", "order", "print", "map", "count", "type", "key", "keys"):
            self.assertNotIn(word, route_classifier.VOCABULARY, word)

    def test_no_vocabulary_word_or_extension_is_sensitive(self):
        for word in route_classifier.VOCABULARY | route_classifier.EXTENSIONS:
            self.assertFalse(any(bad in word for bad in route_classifier.SENSITIVE), word)

    def test_sensitive_names_are_zdr_in_any_case_and_inside_identifiers(self):
        for task in ("Read .env", "Read .ENV", "Print API_KEY", "Show id_rsa", "Show passwords.txt", "List cert.pem",
                     "Read ~/.ssh/config", "Show the Credentials", "Find the seed phrase"):
            self.assertTrue(self.zdr(task), task)

    def test_joined_words_need_every_part_in_the_vocabulary(self):
        self.assertTrue(self.zdr("Show the file then-delete-it"))
        self.assertTrue(self.zdr("Show the file then_delete_it"))
        self.assertFalse(self.zdr("Read error-log"))
        self.assertFalse(self.zdr("Read src/app.py"))

    def test_quoted_text_is_never_free(self):
        for task in ("Read 'settings.json'", 'Read "the file"', "Read file 'and' 'erase' it"):
            self.assertTrue(self.zdr(task), task)


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
                                          reservation_id=res["reservation_id"], allow_free=True)
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.FLASH, True, 0.01, 5, True,
                                          reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)
        self.assertFalse(self.ledger.exists())

    def test_unknown_and_already_settled_ids_are_refused(self):
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.01, 5, True, reservation_id="nope")
        res = route_executor.reserve("code", self.GLM, 0.50)
        first = route_executor.record_receipt("code", self.GLM, False, 0.10, 5, True,
                                              reservation_id=res["reservation_id"])
        again = route_executor.record_receipt("code", self.GLM, False, 0.10, 5, True,
                                              reservation_id=res["reservation_id"])
        self.assertEqual(again["id"], first["id"])
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)

    def test_spend_plus_holds_never_pass_the_cap_after_a_mismatch_attempt(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        with patch.object(route_executor, "month_paid_spend", return_value=cap - 0.50):
            res = route_executor.reserve("code", self.GLM, 0.50)
            with self.assertRaises(ValueError):
                route_executor.record_receipt("scout", self.FREE, False, 0, 5, True,
                                              reservation_id=res["reservation_id"], allow_free=True)
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
            free = route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", None, allow_free=True)
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


class Round3(TmpLedger):
    GLM = "vercel/zai/glm-5.3"

    def test_only_a_leading_read_only_verb_can_reach_a_free_class(self):
        for task in ("code a search function", "correct the lint configuration",
                     "repair the audit endpoint", "resolve the screenshot upload failure",
                     "please explain and then patch the parser"):
            self.assertTrue(route_classifier.classify(task)["zdr_required"], task)
        for task in ("find the reason for the error", "what is the cost ceiling",
                     "review this PR for style", "analyze this screenshot"):
            self.assertFalse(route_classifier.classify(task)["zdr_required"], task)

    def test_omo_slots_that_execute_edits_are_all_zdr(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        safe = route_executor.zdr_models(SCHEMA)
        read_only_agents = {"explore", "librarian", "multimodal-looker", "momus"}
        read_only_categories = {"code-review"}

        def names(entry):
            ms = entry.get("models") or [entry["model"], *entry.get("fallback_models", [])]
            return [m["model"] if isinstance(m, dict) else m for m in ms]

        for agent, entry in cfg["agents"].items():
            if agent not in read_only_agents:
                for m in names(entry):
                    self.assertIn(m, safe, agent)
        for cat, entry in cfg["categories"].items():
            if cat not in read_only_categories:
                for m in names(entry):
                    self.assertIn(m, safe, cat)

    def test_disabling_any_provider_never_resolves_a_zdr_category_to_a_free_model(self):
        cfg = gen_omo_config.build(SCHEMA)["[opencode]"]
        safe = route_executor.zdr_models(SCHEMA)
        for disabled in ([], ["vercel"], ["openai"], ["opencode"], ["vercel", "opencode"]):
            def keep(models):
                return [m for m in models if m.split("/")[0] not in disabled]

            for cat, cls in gen_omo_config.CATEGORY_MAP.items():
                if not SCHEMA["task_classes"][cls]["zdr_required"]:
                    continue
                entry = cfg["categories"][cat]
                own = keep([m["model"] if isinstance(m, dict) else m for m in entry["fallback_models"]])
                for agent, a in cfg["agents"].items():
                    if agent in ("explore", "librarian", "multimodal-looker", "momus"):
                        continue
                    inherited = keep([m["model"] if isinstance(m, dict) else m for m in a["models"]])
                    resolved = own or inherited
                    for m in resolved:
                        self.assertIn(m, safe, (disabled, cat, agent))

    def test_settling_a_tiny_cost_still_counts_it(self):
        for _ in range(3):
            res = route_executor.reserve("code", self.GLM, 0.0000004)
            r = route_executor.record_receipt("code", self.GLM, False, 0.0000004, 5, True,
                                              reservation_id=res["reservation_id"])
            self.assertGreaterEqual(r["cost_usd"], 0.000001)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.000003, places=9)

    def test_extreme_finite_numbers_are_rejected_not_crashes(self):
        with self.assertRaises(ValueError):
            route_executor.preflight("code", self.GLM, 1e308)
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 1e308, 5, True)
        p = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"), "implement auth",
                            "--preflight", "--est-cost", "1e308", "--no-reserve"],
                           capture_output=True, text=True,
                           env={**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name})
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_huge_integer_receipts_do_not_crash_the_readers(self):
        huge = '{"ts": "%s", "task_class": "code", "used": "%s", "success": true, "latency_ms": 5, ' \
               '"cost_usd": 1%s}' % (datetime.now(timezone.utc).isoformat(), self.GLM, "0" * 5000)
        self.ledger.write_text(huge + "\n", encoding="utf-8")
        self.assertEqual(route_executor.month_paid_spend(), 0.0)
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(got, [])
        self.assertEqual(skipped["malformed"], 1)

    def test_unhashable_used_field_does_not_block_paid_admission(self):
        self.ledger.write_text('{"ts": "%s", "used": [], "cost_usd": 0.1}\n'
                               % datetime.now(timezone.utc).isoformat(), encoding="utf-8")
        route_executor.preflight("code", self.GLM, 0.1)


class Round4(TmpLedger):
    GLM = "vercel/zai/glm-5.3"

    def test_the_two_codex_repros_are_zdr(self):
        for task in MUST_BE_ZDR[:2]:
            c = route_classifier.classify(task)
            self.assertTrue(c["zdr_required"], (task, c["class"]))

    def test_corpus_has_200_prompts(self):
        self.assertGreaterEqual(len(MUST_BE_ZDR), 100)
        self.assertEqual(len(MAY_BE_FREE), 100)

    def test_no_mutating_or_multi_clause_prompt_leaks_to_a_free_class(self):
        leaks = [(t, route_classifier.classify(t)["class"]) for t in MUST_BE_ZDR
                 if not route_classifier.classify(t)["zdr_required"]]
        self.assertEqual(leaks, [])

    def test_free_hit_rate_on_natural_read_only_prompts_stays_above_the_floor(self):
        """A cost measure, not a safety check. Measured 41 of 100 on 2026-10-21. The closed
        grammar sends any prompt with an unknown word to ZDR, so most natural questions pay."""
        free = [t for t in MAY_BE_FREE if not route_classifier.classify(t)["zdr_required"]]
        self.assertGreaterEqual(len(free), 35, f"free hit rate fell to {len(free)} of {len(MAY_BE_FREE)}")

    # finding 2: an unterminated tail must not swallow the next paid receipt
    def test_torn_ledger_tail_does_not_swallow_the_next_receipt(self):
        self.ledger.write_text('{"ts":', encoding="utf-8")
        res = route_executor.reserve("code", self.GLM, 0.50)
        route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                      reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.50)
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.0)

    def test_torn_tail_cannot_let_spend_reach_the_cap_unseen(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        route_executor.record_receipt("code", self.GLM, False, cap - 0.50, 5, True)
        with open(self.ledger, "ab") as f:
            f.write(b'{"ts":')
        res = route_executor.reserve("code", self.GLM, 0.50)
        route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                      reservation_id=res["reservation_id"])
        with self.assertRaises(route_executor.BudgetError):
            route_executor.reserve("code", self.GLM, 0.50)

    def test_reservation_stays_open_when_the_receipt_cannot_be_verified(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        with patch.object(route_executor, "_receipt_is_last_line", return_value=False):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                              reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)

    # finding 3: a retry after an interrupted settle must not count the call twice
    def test_retrying_an_interrupted_settlement_counts_the_call_once(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        real = route_executor._append_unlocked

        def flaky(path, line):
            if '"settle"' in line:
                raise OSError("disk full")
            return real(path, line)

        with patch.object(route_executor, "_append_unlocked", side_effect=flaky):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", self.GLM, False, 0.20, 5, True,
                                              reservation_id=res["reservation_id"])
        again = route_executor.record_receipt("code", self.GLM, False, 0.20, 5, True,
                                              reservation_id=res["reservation_id"])
        self.assertEqual(again["reservation_id"], res["reservation_id"])
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.20)
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.0)

    # findings 4 and 5: readers bound and reject out-of-range latency and cost
    def _write(self, rows):
        lines = []
        for cost, latency in rows:
            lines.append(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "task_class": "code",
                                     "used": self.GLM, "success": True, "cost_usd": cost,
                                     "latency_ms": latency}))
        self.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_huge_latencies_are_malformed_and_the_report_still_writes(self):
        self._write([(0.1, 10 ** 308), (0.1, 10 ** 308)])
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(got, [])
        self.assertEqual(skipped["malformed"], 2)
        out = Path(self.tmp.name) / "proposals"
        with patch.object(review, "PROPOSALS", out):
            review.main([])
        self.assertTrue(list(out.glob("*.json")))

    def test_negative_cost_and_latency_are_malformed(self):
        self._write([(-1.0, 5), (0.1, -5)])
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(got, [])
        self.assertEqual(skipped["malformed"], 2)

    def test_negative_costs_cannot_drive_a_proposal(self):
        self._write([(0.1, 5)] * 10 + [(-1.0, 5)] * 10)
        got, _ = review.load_receipts(self.ledger)
        self.assertEqual(len(got), 10)

    def test_recording_a_receipt_rejects_an_absurd_latency(self):
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.1, 10 ** 308, True)


class Round6Grammar(unittest.TestCase):
    """Free routing uses a closed grammar, not a verb blacklist (Codex round 5, finding 1)."""

    def zdr(self, task):
        return route_classifier.classify(task)["zdr_required"]

    def test_coordinator_repros_are_zdr(self):
        for task in ("Read settings.json or erase backups", "List files | xargs unlink",
                     "Show me the file and delete it"):
            self.assertTrue(self.zdr(task), task)

    def test_unknown_verbs_are_zdr_because_they_are_unknown(self):
        for verb in ("erase", "unlink", "truncate", "wipe", "drop", "purge", "overwrite", "nuke", "shred",
                     "zap", "obliterate", "defenestrate"):
            self.assertTrue(self.zdr(f"Show the file {verb} it"), verb)
            self.assertTrue(self.zdr(f"{verb} the file"), verb)

    def test_an_unknown_word_decides_it_deterministically(self):
        self.assertTrue(self.zdr("Explain the retry logic"))        # "retry" is not in the vocabulary
        self.assertFalse(self.zdr("Explain the error log"))         # every word is
        self.assertFalse(self.zdr("Explain the retry logic of the error log".replace("retry ", "")))

    def test_the_first_word_must_be_a_read_only_verb(self):
        for task in ("check the file", "check and fix the file", "fix the file", "the file", "please show the file"):
            self.assertTrue(self.zdr(task), task)
        for task in ("read the file", "list the files", "show the file", "summarise the log", "describe the module"):
            self.assertFalse(self.zdr(task), task)

    def test_word_cap_is_15(self):
        ok = "Explain " + " ".join(["the file"] * 7)       # 15 words
        self.assertFalse(self.zdr(ok))
        self.assertTrue(self.zdr(ok + " file"))             # 16 words

    def test_only_a_closed_character_set_is_allowed(self):
        for ch in "|&;<>$`,(){}[]=+*#@!~%^:" + chr(10) + chr(9) + chr(92):
            self.assertTrue(self.zdr(f"Show the file {ch} log"), repr(ch))
        for ok in ("Show the file.", "Show the file?", "Show src/app.py"):
            self.assertFalse(self.zdr(ok), ok)
        for quoted in ("Show 'the file'", 'Show "the file"', "Read file 'and' 'erase' it"):   # option A: quotes are never free
            self.assertTrue(self.zdr(quoted), quoted)

    def test_identifiers_and_quoted_text_are_data_but_bare_or_broken_tokens_are_not(self):
        for ok in ("Read settings.json", "Read ./src/app.py", "Show v2", "Read src/erase.py", "Read error-log"):
            self.assertFalse(self.zdr(ok), ok)
        for bad in ("Show erase.", "Show the file erase.", "Show -rf", "Show the file. erase.", "Show erase",
                    "Read wipe_disk", "Read wipe_disk.py", "Show the file then-delete-it", "Read 'erase everything'",
                    'Read "erase everything"'):
            self.assertTrue(self.zdr(bad), bad)

    def test_the_vocabulary_holds_no_verb_that_changes_or_runs_anything(self):
        mutating = {"delete", "remove", "erase", "unlink", "truncate", "wipe", "drop", "purge", "overwrite", "nuke",
                    "shred", "write", "save", "store", "run", "execute", "send", "post", "upload", "copy", "move",
                    "rename", "update", "change", "fix", "patch", "edit", "create", "add", "build", "deploy",
                    "install", "commit", "push", "pull", "merge", "release", "publish", "restart", "kill",
                    "and", "or", "then", "also", "next", "before", "after", "while", "once", "plus", "not", "private",
                    "secret", "secrets", "password", "passwords", "token", "credential", "credentials"}
        self.assertEqual(route_classifier.VOCABULARY & mutating, set())
        self.assertEqual(route_classifier.READ_ONLY_VERBS & mutating, set())

    def test_media_and_review_classes_still_come_from_the_grammar(self):
        self.assertEqual(route_classifier.classify("analyze this screenshot")["class"], "vision")
        self.assertEqual(route_classifier.classify("what is in the screenshot")["class"], "vision")
        self.assertEqual(route_classifier.classify("audit the dependency list")["class"], "review")
        self.assertEqual(route_classifier.classify("find the reason for the error")["class"], "scout")

    def test_strong_rules_still_route_to_their_zdr_classes_first(self):
        self.assertEqual(route_classifier.classify("find the root cause of the crash")["class"], "hard-reasoning")
        self.assertTrue(self.zdr("extract all emails from every log"))


class Round5Mechanical(TmpLedger):
    """Codex round 5, findings 2 to 7 (finding 1 is the open classifier policy)."""
    GLM = "vercel/zai/glm-5.3"

    def test_structural_connectors_keep_a_request_off_free_classes(self):
        for task in ("Read settings.json or erase backups", "List files | xargs unlink",
                     "Show the file > out.txt", "Read $(whoami)"):
            self.assertTrue(route_classifier.classify(task)["zdr_required"], task)

    # 3: a short write must not lose a receipt
    def test_a_short_write_is_completed_not_lost(self):
        real = os.write
        calls = []

        def short(fd, data):
            calls.append(len(data))
            return real(fd, bytes(data[:25])) if len(calls) == 1 else real(fd, data)

        with patch.object(route_executor.os, "write", side_effect=short):
            route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True)
        self.assertGreater(len(calls), 1)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.50)

    # 2: the retry must make the receipt durable before it closes the hold
    def test_retry_syncs_the_receipt_before_closing_the_hold(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        real = os.fsync
        n = {"i": 0}

        def flaky(fd):
            n["i"] += 1
            if n["i"] == 1:
                raise OSError("fsync failed")
            return real(fd)

        with patch.object(route_executor.os, "fsync", side_effect=flaky):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                              reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)
        with patch.object(route_executor, "_sync_file", wraps=route_executor._sync_file) as spy:
            got = route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                                reservation_id=res["reservation_id"])
        self.assertIn(self.ledger, [c.args[0] for c in spy.call_args_list])
        self.assertEqual(got["reservation_id"], res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.0)

    # 5: a retry after a completed (but errored) settlement returns the receipt
    def test_retry_after_a_settlement_that_errored_after_writing_is_idempotent(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        real = os.fsync
        n = {"i": 0}

        def flaky(fd):
            n["i"] += 1
            if n["i"] == 2:  # receipt synced, settle bytes written, settle fsync fails
                raise OSError("fsync failed")
            return real(fd)

        with patch.object(route_executor.os, "fsync", side_effect=flaky):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", self.GLM, False, 0.20, 5, True,
                                              reservation_id=res["reservation_id"])
        got = route_executor.record_receipt("code", self.GLM, False, 0.20, 5, True,
                                            reservation_id=res["reservation_id"])
        self.assertEqual(got["reservation_id"], res["reservation_id"])
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.20)

    def test_a_retry_with_another_class_or_model_is_still_refused(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        route_executor.record_receipt("code", self.GLM, False, 0.20, 5, True,
                                      reservation_id=res["reservation_id"])
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", "vercel/deepseek/deepseek-v4.1-flash", True, 0.01, 5, True,
                                          reservation_id=res["reservation_id"])

    # 4: a relative override gives every working directory its own budget
    def test_relative_receipts_dir_refuses_paid_admission_but_not_free(self):
        with patch.dict(os.environ, {"STARLIGHT_RECEIPTS_DIR": "receipts"}):
            self.assertFalse(route_executor.shared_root_usable())
            with self.assertRaises(route_executor.BudgetError):
                route_executor.preflight("code", self.GLM, 0.10)
            route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", allow_free=True)

    # 6: an absurd reservation estimate is malformed, not a crash
    def test_absurd_reservation_estimate_does_not_crash_admission(self):
        (Path(self.tmp.name) / "reservations.jsonl").write_text(json.dumps(
            {"kind": "reserve", "id": "x", "ts": datetime.now(timezone.utc).isoformat(), "model": self.GLM,
             "task_class": "code", "est_cost_usd": 1e308}) + "\n", encoding="utf-8")
        route_executor.preflight("code", self.GLM, 0.10)
        self.assertEqual(route_executor.reserved_usd(), 0.0)

    # 7: a torn multi-byte tail must not stop recovery
    def test_torn_utf8_tail_does_not_block_admission_or_the_review(self):
        self.ledger.write_bytes(b'{"ts":"torn-\xe2\x82')
        route_executor.preflight("code", self.GLM, 0.10)
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(got, [])
        self.assertEqual(skipped["malformed"], 1)
        route_executor.record_receipt("code", self.GLM, False, 0.10, 5, True)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.10)


class Round6Recovery(TmpLedger):
    """Codex round 6, finding 3: a retry must not settle a hold against a receipt that cannot be counted."""
    GLM = "vercel/zai/glm-5.3"

    def _interrupt_settlement(self, res):
        real = route_executor._append_unlocked

        def flaky(path, line):
            if '"settle"' in line:
                raise OSError("disk full")
            return real(path, line)

        with patch.object(route_executor, "_append_unlocked", side_effect=flaky):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                              reservation_id=res["reservation_id"])

    def test_a_corrupted_prior_receipt_does_not_close_the_hold(self):
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        route_executor.record_receipt("code", self.GLM, False, cap - 0.50, 5, True)
        res = route_executor.reserve("code", self.GLM, 0.50)
        self._interrupt_settlement(res)
        rows = [json.loads(line) for line in self.ledger.read_text().splitlines()]
        rows[-1]["ts"] = "garbage"
        self.ledger.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                          reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)
        with self.assertRaises(route_executor.BudgetError):
            route_executor.reserve("code", self.GLM, 0.50)

    def test_an_incomplete_prior_receipt_is_refused_and_the_cli_does_not_crash(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        with open(self.ledger, "a", encoding="utf-8") as f:
            f.write(json.dumps({"task_class": "code", "used": self.GLM,
                                "reservation_id": res["reservation_id"]}) + "\n")
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                          reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)
        p = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"), "implement auth",
                            "--record", "success", "--used", self.GLM, "--cost", "0.50", "--latency", "5",
                            "--reservation", res["reservation_id"]],
                           capture_output=True, text=True,
                           env={**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name})
        self.assertNotIn("Traceback", p.stderr)
        self.assertNotEqual(p.returncode, 0)

    def test_a_complete_prior_receipt_still_makes_the_retry_idempotent(self):
        res = route_executor.reserve("code", self.GLM, 0.50)
        self._interrupt_settlement(res)
        got = route_executor.record_receipt("code", self.GLM, False, 0.50, 5, True,
                                            reservation_id=res["reservation_id"])
        self.assertEqual(got["reservation_id"], res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.0)
        self.assertAlmostEqual(route_executor.month_paid_spend(), 0.50)


class Round8FreeOptIn(TmpLedger):
    """Codex round 8: free routing is opt-in at every entry point, and one function owns the effective route."""
    FLASH = "vercel/deepseek/deepseek-v4.1-flash"

    def run_cli(self, *args):
        env = {**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name}
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "route_task.py"), *args],
                              capture_output=True, text=True, env=env)

    def test_library_default_never_returns_a_non_gateway_model(self):
        for cls in ("scout", "review", "vision"):
            r = route_executor.route(cls)
            self.assertTrue(all(m in route_executor.zdr_models(SCHEMA) for m in r["chain"]), (cls, r["chain"]))
            self.assertGreater(r["cost_ceiling_usd"], 0)
            self.assertTrue(r["free_replaced"])
            free = route_executor.route(cls, allow_free=True)
            self.assertTrue(any(m.startswith("opencode/") for m in free["chain"]))
            self.assertEqual(free["cost_ceiling_usd"], 0)

    def test_cli_read_only_request_goes_to_the_gateway_by_default(self):
        p = self.run_cli("Read notes.txt", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["class"], "scout")
        self.assertEqual(out["chain"], [self.FLASH])
        self.assertTrue(out["free_replaced"])

    def test_cli_allow_free_is_the_only_way_to_a_free_model(self):
        p = self.run_cli("Read notes.txt", "--json", "--allow-free")
        out = json.loads(p.stdout)
        self.assertTrue(out["primary"].startswith("opencode/"))
        self.assertFalse(out["free_replaced"])

    def test_replacement_is_admitted_and_recorded_with_a_positive_ceiling(self):
        for cls in ("scout", "review", "vision"):
            r = route_executor.route(cls)
            status = route_executor.preflight(cls, self.FLASH, r["cost_ceiling_usd"] / 2)
            self.assertEqual(status["model"], self.FLASH)
            rec = route_executor.record_receipt(cls, self.FLASH, False, r["cost_ceiling_usd"] / 2, 5, True)
            self.assertFalse(rec["over_ceiling"])
            with self.assertRaises(route_executor.BudgetError):
                route_executor.preflight(cls, self.FLASH, r["cost_ceiling_usd"] * 2)
        with self.assertRaises(ValueError):
            route_executor.preflight("scout", "opencode/mimo-v2.6-flash-free", 0)

    def test_every_model_in_the_generated_config_passes_executor_admission(self):
        for allow_free in (False, True):
            cfg = gen_omo_config.build(SCHEMA, allow_free)["[opencode]"]
            slots = [(a, gen_omo_config.AGENT_MAP[a], v) for a, v in cfg["agents"].items()]
            slots += [(c, gen_omo_config.CATEGORY_MAP[c], v) for c, v in cfg["categories"].items()]
            for name, cls, slot in slots:
                models = [m["model"] if isinstance(m, dict) else m
                          for m in slot.get("models", []) + slot.get("fallback_models", []) + [slot.get("model")] if m]
                for m in models:
                    r = route_executor.route(cls, allow_free=allow_free)
                    self.assertIn(m, r["chain"], (name, cls, m, allow_free))
                    est = None if not route_executor.is_paid(m, SCHEMA) else r["cost_ceiling_usd"] / 2
                    route_executor.preflight(cls, m, est, allow_free=allow_free)
                    route_executor.record_receipt(cls, m, False, 0, 1, True, allow_free=allow_free, synthetic=True)

    def test_a_class_without_a_zdr_ceiling_is_refused_not_given_zero(self):
        schema = json.loads(json.dumps(SCHEMA))
        del schema["task_classes"]["scout"]["zdr_cost_ceiling_usd"]
        with self.assertRaises(ValueError):
            route_executor.effective_route(schema, "scout")

    def test_concurrent_generations_do_not_cross_install(self):
        import threading
        out = Path(self.tmp.name) / "omo.jsonc"
        texts = {i: f"// run {i}" + chr(10) + "x" * 5000 for i in range(12)}
        errors = []

        def go(i):
            try:
                gen_omo_config._install(out, texts[i])
            except Exception as e:  # noqa: BLE001
                errors.append(e)

        threads = [threading.Thread(target=go, args=(i,)) for i in texts]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(errors, [])
        self.assertIn(out.read_text(encoding="utf-8"), texts.values())
        self.assertEqual([p.name for p in Path(self.tmp.name).glob("*.tmp")], [])

    def test_each_invocation_gets_its_own_temp_file(self):
        names = []
        real = tempfile.mkstemp

        def spy(*a, **k):
            fd, name = real(*a, **k)
            names.append(name)
            return fd, name

        out = Path(self.tmp.name) / "omo.jsonc"
        with patch.object(gen_omo_config.tempfile, "mkstemp", side_effect=spy):
            gen_omo_config._install(out, "a")
            gen_omo_config._install(out, "b")
        self.assertEqual(len(set(names)), 2)

    def test_overflowing_timestamp_is_not_countable_and_keeps_the_hold(self):
        glm = "vercel/zai/glm-5.3"
        self.assertFalse(route_executor._countable_receipt(
            {"ts": "0001-01-01T00:00:00+01:00", "id": "a", "used": glm, "task_class": "code", "cost_usd": 0.5,
             "latency_ms": 5, "success": True, "over_ceiling": False}))
        cap = SCHEMA["token_pass"]["hard_cap_usd"]
        route_executor.record_receipt("code", glm, False, cap - 0.50, 5, True)
        res = route_executor.reserve("code", glm, 0.50)
        real = route_executor._append_unlocked

        def flaky(path, line):
            if '"settle"' in line:
                raise OSError("disk full")
            return real(path, line)

        with patch.object(route_executor, "_append_unlocked", side_effect=flaky):
            with self.assertRaises(OSError):
                route_executor.record_receipt("code", glm, False, 0.50, 5, True, reservation_id=res["reservation_id"])
        rows = [json.loads(line) for line in self.ledger.read_text().splitlines()]
        rows[-1]["ts"] = "0001-01-01T00:00:00+01:00"
        self.ledger.write_text(chr(10).join(json.dumps(r) for r in rows) + chr(10), encoding="utf-8")
        with self.assertRaises(ValueError):
            route_executor.record_receipt("code", glm, False, 0.50, 5, True, reservation_id=res["reservation_id"])
        self.assertAlmostEqual(route_executor.reserved_usd(), 0.50)


class Round9Consistency(TmpLedger):
    FREE_SCOUT = "opencode/mimo-v2.6-flash-free"
    GATEWAY = "vercel/deepseek/deepseek-v4.1-flash"
    TS = "2026-10-21T10:00:00+00:00"

    def _run_cli(self, script, *argv):
        out = subprocess.run([sys.executable, "-B", str(FLEET / script), *argv], capture_output=True, text=True,
                             env={**os.environ, "STARLIGHT_RECEIPTS_DIR": self.tmp.name}, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout

    def test_classifier_cli_default_never_emits_a_free_model(self):
        c = json.loads(self._run_cli("route_classifier.py", "Read notes.txt", "--json"))
        self.assertEqual(c["class"], "scout")
        self.assertEqual(c["primary"], self.GATEWAY)
        self.assertEqual(c["chain"], [self.GATEWAY])
        self.assertEqual(c["cost_ceiling_usd"], 0.02)
        everything = c["chain"] + c["fallbacks"] + [c["primary"]]
        self.assertFalse(any(m.startswith("opencode/") for m in everything))

    def test_classifier_cli_free_is_an_explicit_opt_in(self):
        c = json.loads(self._run_cli("route_classifier.py", "Read notes.txt", "--json", "--allow-free"))
        self.assertEqual(c["primary"], self.FREE_SCOUT)
        self.assertEqual(c["cost_ceiling_usd"], 0)
        self.assertTrue(c["allow_free"])

    def test_classify_matches_the_executor(self):
        for free in (False, True):
            want = route_executor.effective_route(SCHEMA, "scout", allow_free=free)
            got = route_classifier.classify("Read notes.txt", allow_free=free)
            for k in ("primary", "fallbacks", "chain", "cost_ceiling_usd", "zdr_required"):
                self.assertEqual(got[k], want[k], (free, k))

    def test_route_task_cli_and_classifier_cli_agree(self):
        a = json.loads(self._run_cli("route_task.py", "Read notes.txt", "--json"))
        b = json.loads(self._run_cli("route_classifier.py", "Read notes.txt", "--json"))
        for k in ("primary", "fallbacks", "chain", "cost_ceiling_usd"):
            self.assertEqual(a[k], b[k], k)

    def _legacy_free_receipts(self):
        rows = []
        for _ in range(10):
            rows.append({"ts": self.TS, "task_class": "scout", "used": self.FREE_SCOUT, "success": False,
                         "cost_usd": 0.0, "latency_ms": 5})
        for _ in range(15):
            rows.append({"ts": self.TS, "task_class": "scout", "used": "opencode/beam-free", "success": True,
                         "cost_usd": 0.0, "latency_ms": 5})
        return rows

    def test_strict_review_filters_legacy_free_receipts_and_proposes_nothing(self):
        kept, other = review.filter_mode(self._legacy_free_receipts(), SCHEMA, allow_free=False)
        self.assertEqual((kept, other), ([], 25))
        self.assertEqual(review.propose(review.analyze(kept, SCHEMA), SCHEMA, allow_free=False), [])

    def test_free_mode_review_still_sees_free_receipts(self):
        kept, other = review.filter_mode(self._legacy_free_receipts(), SCHEMA, allow_free=True)
        self.assertEqual((len(kept), other), (25, 0))
        chain = route_executor.effective_route(SCHEMA, "scout", allow_free=True)["chain"]
        for p in review.propose(review.analyze(kept, SCHEMA), SCHEMA, allow_free=True):
            self.assertIn(p["to"], chain)

    def test_review_respects_the_recorded_allow_free_flag(self):
        row = {"ts": self.TS, "task_class": "scout", "used": self.GATEWAY, "success": True,
               "cost_usd": 0.001, "latency_ms": 5}
        self.assertTrue(review.in_mode({**row, "allow_free": False}, SCHEMA, False))
        self.assertFalse(review.in_mode({**row, "allow_free": True}, SCHEMA, False))

    def test_strict_review_never_proposes_a_free_model(self):
        rows = []
        for model, ok in ((self.GATEWAY, False), ("vercel/zai/glm-5.3", True)):
            for _ in range(25):
                rows.append({"ts": self.TS, "task_class": "scout", "used": model, "success": ok,
                             "cost_usd": 0.001, "latency_ms": 5})
        kept, _ = review.filter_mode(rows, SCHEMA, allow_free=False)
        for p in review.propose(review.analyze(kept, SCHEMA), SCHEMA, allow_free=False):
            self.assertFalse(p["to"].startswith("opencode/"))

    def test_new_receipts_record_the_mode(self):
        r = route_executor.record_receipt("scout", self.GATEWAY, False, 0.001, 5, True, synthetic=True)
        self.assertIs(r["allow_free"], False)
        r = route_executor.record_receipt("scout", self.FREE_SCOUT, False, 0, 5, True, synthetic=True, allow_free=True)
        self.assertIs(r["allow_free"], True)

    def test_schema_rules_describe_strict_by_default(self):
        text = " ".join(SCHEMA["routing_rules"]).lower()
        self.assertNotIn("default to free tier", text)
        self.assertNotIn("never use token pass for scout", text)
        self.assertIn("strict by default", text)
        self.assertIn("--allow-free", text)
        self.assertIn("allow_free", SCHEMA["receipts"]["fields"])


class Round9NoDirectSchemaReads(unittest.TestCase):
    """Only route_executor reads a class's own model fields. Every other module takes the route
    from effective_route(); a direct read would bring the free default back."""
    # (file, stripped line) -> why a read of task_classes there is safe.
    ALLOWED = {
        ("gen_omo_config.py", 'classes = schema["task_classes"]'): "class names, variant and zdr_required only",
        ("weekly_routing_review.py", 'known = schema["task_classes"]'): "class-name membership check",
        ("weekly_routing_review.py", 'if cls not in schema["task_classes"]:'): "class-name membership check",
    }

    def test_no_module_outside_the_executor_reads_task_classes_unreviewed(self):
        offenders = []
        for path in sorted(FLEET.glob("*.py")):
            if path.name == "route_executor.py":
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                code = line.strip()
                if "task_classes" in code and not code.startswith("#") and (path.name, code) not in self.ALLOWED:
                    offenders.append(f"{path.name}:{n}: {code}")
        self.assertEqual(offenders, [], "read model fields through route_executor.effective_route()")

    def test_allow_list_entries_still_exist(self):
        for name, code in self.ALLOWED:
            self.assertIn(code, (FLEET / name).read_text(encoding="utf-8"), (name, code))

    def test_allowed_gen_omo_reads_touch_no_model_field(self):
        src = (FLEET / "gen_omo_config.py").read_text(encoding="utf-8")
        for field in ("primary", "fallbacks", "cost_ceiling_usd"):
            self.assertNotIn(f'classes[cls]["{field}"]', src)

class Round10WeeklyReviewModes(TmpLedger):
    def _line(self, **kw):
        base = {"ts": datetime.now(timezone.utc).isoformat(), "task_class": "code",
                "used": "vercel/zai/glm-5.3", "success": True, "cost_usd": 0.1, "latency_ms": 5}
        return json.dumps({**base, **kw})

    def test_a_string_allow_free_is_malformed_and_in_neither_review(self):
        lines = [self._line(allow_free="false"), self._line(allow_free=0), self._line(allow_free=False)]
        self.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        got, skipped = review.load_receipts(self.ledger)
        self.assertEqual(len(got), 1)
        self.assertIs(got[0]["allow_free"], False)
        self.assertEqual(skipped["malformed"], 2)
        strict, _ = review.filter_mode(got, SCHEMA, allow_free=False)
        free, _ = review.filter_mode(got, SCHEMA, allow_free=True)
        self.assertEqual((len(strict), len(free)), (1, 0))

    def test_strict_and_free_proposals_do_not_overwrite_each_other(self):
        self.ledger.write_text(self._line() + "\n", encoding="utf-8")
        out = Path(self.tmp.name) / "proposals"
        with patch.object(review, "PROPOSALS", out):
            review.main([])
            review.main(["--allow-free"])
        names = sorted(p.name for p in out.glob("*.json"))
        self.assertEqual(len(names), 2, names)
        self.assertTrue(any(n.endswith("-strict-zdr.json") for n in names))
        self.assertTrue(any(n.endswith("-allow-free.json") for n in names))
        modes = {json.loads(p.read_text())["mode"] for p in out.glob("*.json")}
        self.assertEqual(modes, {"strict-zdr", "allow-free"})



# `variant` is a reasoning-effort label, not a route choice, so reading it cannot bring back a free model.
MODEL_FIELDS = frozenset({"primary", "fallbacks", "fallback", "cost_ceiling_usd", "zdr_cost_ceiling_usd"})


def model_field_reads(source: str) -> list[str]:
    """Reads of a class's own model fields in `source`, whatever the quoting or access form.

    Flags subscripts and .get() calls with a model-field key whose base expression comes from
    task_classes, including through a name assigned from such an expression."""
    import ast
    tree = ast.parse(source)
    tainted: set[str] = set()
    changed = True

    def from_classes(node: ast.AST) -> bool:
        return any((isinstance(n, ast.Constant) and n.value == "task_classes")
                   or (isinstance(n, ast.Name) and n.id in tainted) for n in ast.walk(node))

    while changed:
        changed = False
        for n in ast.walk(tree):
            targets, value = [], None
            if isinstance(n, ast.Assign):
                targets, value = n.targets, n.value
            elif isinstance(n, (ast.AnnAssign, ast.NamedExpr)) and n.value is not None:
                targets, value = [n.target], n.value
            elif isinstance(n, (ast.For, ast.comprehension)):
                targets, value = [n.target], n.iter
            if value is not None and from_classes(value):
                for tgt in targets:
                    for name in ast.walk(tgt):
                        if isinstance(name, ast.Name) and name.id not in tainted:
                            tainted.add(name.id)
                            changed = True
    found = []
    for n in ast.walk(tree):
        key = base = None
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant):
            key, base = n.slice.value, n.value
        elif (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("get", "setdefault", "pop")
              and n.args and isinstance(n.args[0], ast.Constant)):
            key, base = n.args[0].value, n.func.value
        if key in MODEL_FIELDS and from_classes(base):
            found.append(f"line {n.lineno}: {ast.unparse(n)}")
    return found


class Round10ModelFieldScan(unittest.TestCase):
    MUTATIONS = {
        "double quotes": 'x = schema["task_classes"][cls]["primary"]',
        "single quotes": "x = schema['task_classes'][cls]['primary']",
        "get call": 'x = schema["task_classes"][cls].get("fallbacks", [])',
        "alias name": """d = schema["task_classes"][cls]
y = d['cost_ceiling_usd']""",
        "loop alias": """for name, d in schema["task_classes"].items():
    y = d.get("primary")""",
        "nested alias": """classes = schema["task_classes"]
x = classes[cls]["fallbacks"]""",
        "walrus": """if (d := schema["task_classes"][cls]):
    y = d["zdr_cost_ceiling_usd"]""",
    }

    def test_scanner_catches_every_access_form(self):
        for name, source in self.MUTATIONS.items():
            self.assertTrue(model_field_reads(source), f"scanner missed: {name}")

    def test_scanner_ignores_effective_route_results_and_class_names(self):
        for source in ("""r = effective_route(schema, cls)
x = r["primary"]""",
                       """classes = schema["task_classes"]
ok = cls in classes""",
                       'x = receipt["task_class"]'):
            self.assertEqual(model_field_reads(source), [], source)

    def test_no_fleet_module_outside_the_executor_reads_model_fields(self):
        offenders = []
        for path in sorted(FLEET.glob("*.py")):
            if path.name == "route_executor.py":
                continue
            offenders += [f"{path.name}: {hit}" for hit in model_field_reads(path.read_text(encoding="utf-8"))]
        self.assertEqual(offenders, [], "take model fields from route_executor.effective_route()")


if __name__ == "__main__":
    unittest.main()
