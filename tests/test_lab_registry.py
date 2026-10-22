import copy
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("build_lab", Path(__file__).resolve().parents[1] / "lab" / "build_lab.py")
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = lab.load()

    def mutated(self, fn):
        data = copy.deepcopy(self.data)
        fn(data)
        return lab.validate(data)

    def test_shipped_registry_is_valid(self):
        self.assertEqual(lab.validate(self.data), [])

    def test_verifier_must_differ_from_owner(self):
        problems = self.mutated(lambda d: d["experiments"][0].update(verifier=d["experiments"][0]["owner"]))
        self.assertTrue(any("different actor" in p for p in problems))

    def test_unknown_blocker_is_rejected(self):
        problems = self.mutated(lambda d: d["experiments"][0]["blocked_by"].append("nope"))
        self.assertTrue(any("nope" in p for p in problems))

    def test_blocked_status_needs_an_unresolved_blocker(self):
        def resolve(d):
            for g in d["gates"]["items"]:
                g["status"] = "done"
            for e in d["experiments"]:
                if e["status"] == "blocked":
                    e["blocked_by"] = [b for b in e["blocked_by"] if not b.startswith("EXP-")]
        problems = self.mutated(resolve)
        self.assertTrue(any("nothing unresolved" in p for p in problems))

    def test_running_experiment_past_ttl_is_flagged(self):
        def run(d):
            e = d["experiments"][4]
            e["status"] = "running"
            e["blocked_by"] = []
            e["clock"]["started"] = "2026-01-01"
        data = copy.deepcopy(self.data)
        run(data)
        problems = lab.validate(data, today=dt.date(2026, 10, 21))
        self.assertTrue(any("time to live" in p for p in problems))

    def test_caps_cannot_exceed_allocation(self):
        problems = self.mutated(lambda d: d["experiments"][0]["budget"].update(token_pass_usd_cap=999))
        self.assertTrue(any("exceed lab allocation" in p for p in problems))

    def test_kill_rule_is_required(self):
        problems = self.mutated(lambda d: d["experiments"][0].update(kill="  "))
        self.assertTrue(any("kill is empty" in p for p in problems))


class ReceiptTests(unittest.TestCase):
    def summary(self, lines):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "routing.jsonl"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return lab.summarize_receipts(path, now=dt.datetime(2026, 10, 21, tzinfo=dt.timezone.utc))

    def test_missing_file_reports_no_data_not_zero(self):
        s = lab.summarize_receipts(Path("does-not-exist.jsonl"))
        self.assertFalse(s["exists"])
        self.assertEqual(s["used"], 0)

    def test_synthetic_and_malformed_lines_are_not_counted(self):
        good = json.dumps({"task_class": "code", "used": "m", "success": True, "cost_usd": 0.5, "provider": "token-pass", "ts": "2026-10-02T00:00:00Z"})
        s = self.summary([
            good,
            json.dumps({"task_class": "code", "used": "m", "success": True, "cost_usd": 9, "synthetic": True}),
            "{not json",
            json.dumps({"task_class": [], "used": "m"}),
            json.dumps({"task_class": "code", "used": "m", "cost_usd": float("nan")}),
        ])
        self.assertEqual(s["used"], 1)
        self.assertEqual(s["synthetic"], 1)
        self.assertEqual(s["skipped"], 3)
        self.assertAlmostEqual(s["token_pass_month_usd"], 0.5)

    def test_experiment_spend_is_grouped(self):
        rec = {"task_class": "code", "used": "m", "success": False, "cost_usd": 0.25, "experiment": "EXP-001"}
        s = self.summary([json.dumps(rec), json.dumps(rec)])
        self.assertAlmostEqual(s["by_experiment"]["EXP-001"], 0.5)


class RenderTests(unittest.TestCase):
    def test_page_escapes_and_states_empty_receipts(self):
        data = lab.load()
        data["experiments"][0]["title"] = "<script>alert(1)</script>"
        summary = lab.summarize_receipts(Path("none.jsonl"))
        page = lab.render(data, summary)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("No real routing receipts yet", page)
        self.assertTrue(page.startswith("<!doctype html>"))

    def test_fragment_has_no_document_wrapper(self):
        fragment = lab.render(lab.load(), lab.summarize_receipts(Path("none.jsonl")), fragment=True)
        self.assertNotIn("<!doctype", fragment)
        self.assertIn("<title>Starlight Lab</title>", fragment)


class HarnessAndPackTests(unittest.TestCase):
    def setUp(self):
        self.data = lab.load()

    def mutated(self, fn):
        import copy
        data = copy.deepcopy(self.data)
        fn(data)
        return lab.validate(data)

    def test_the_four_layers_are_registered(self):
        ids = {h["id"] for h in self.data["harnesses"]["items"]}
        self.assertTrue({"now", "oms", "starlight-ai-harness", "opencode-bare"} <= ids)

    def test_unknown_layer_is_rejected(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"][0].update(layer="L9"))
        self.assertTrue(any("layer" in p for p in problems))

    def test_a_measured_claim_needs_n_and_a_source(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"][0].update(measured={"accepted_rate": 0.9}))
        self.assertTrue(any("measured" in p for p in problems))

    def test_measured_claim_below_the_sample_floor_is_rejected(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"][0].update(
            measured={"n": 3, "accepted_rate": 0.9, "source": "lab/results/EXP-008.md"}))
        self.assertTrue(any("sample floor" in p for p in problems))

    def test_duplicate_harness_id_is_rejected(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"].append(dict(d["harnesses"]["items"][0])))
        self.assertTrue(any("duplicate" in p and "harness" in p for p in problems))

    def test_a_pack_cannot_be_more_than_half_judged(self):
        def judge_all(d):
            for t in d["packs"]["items"][0]["tasks"]:
                t["judged"] = True
                t["verifier"]["type"] = "blind-judge"
        problems = self.mutated(judge_all)
        self.assertEqual([p for p in problems if "judged flag" in p], [])
        self.assertTrue(any("tasks are judged" in p for p in problems))

    def test_the_judged_share_test_depends_on_the_limit(self):
        def judge_all(d):
            for t in d["packs"]["items"][0]["tasks"]:
                t["judged"] = True
                t["verifier"]["type"] = "blind-judge"
        original = lab.MAX_JUDGED_SHARE
        lab.MAX_JUDGED_SHARE = 1.0
        try:
            self.assertEqual(self.mutated(judge_all), [])
        finally:
            lab.MAX_JUDGED_SHARE = original

    def test_blind_judge_tasks_count_even_when_not_flagged_judged(self):
        def hide(d):
            for t in d["packs"]["items"][0]["tasks"]:
                t["judged"] = False
                t["verifier"]["type"] = "blind-judge"
        problems = self.mutated(hide)
        self.assertTrue(any("tasks are judged" in p for p in problems))
        self.assertTrue(any("judged flag" in p for p in problems))
        hidden = {"tasks": [{"verifier": {"type": "blind-judge", "check": "x"}, "judged": False}]}
        self.assertEqual(lab.pack_judged_share(hidden), 1.0)

    def test_every_task_needs_a_checker(self):
        problems = self.mutated(lambda d: d["packs"]["items"][0]["tasks"][0]["verifier"].update(check=""))
        self.assertTrue(any("checker" in p for p in problems))

    def test_judged_task_must_use_a_blind_judge(self):
        def bad(d):
            for pack in d["packs"]["items"]:
                for t in pack["tasks"]:
                    if t["judged"]:
                        t["verifier"]["type"] = "script"
                        return
        problems = self.mutated(bad)
        self.assertTrue(any("blind-judge" in p for p in problems))

    def test_experiments_that_name_a_pack_use_a_registered_one(self):
        packs = {p["id"] for p in self.data["packs"]["items"]}
        for exp in self.data["experiments"]:
            if exp["id"] in ("EXP-008", "EXP-009"):
                self.assertTrue(any(pid in exp["suite"] for pid in packs), exp["id"])

    def test_page_shows_harnesses_and_packs(self):
        page = lab.render(self.data, lab.summarize_receipts(Path("none.jsonl")))
        self.assertIn("starlight-ai-harness", page)
        self.assertIn("web-v0", page)
        self.assertIn("not measured", page)


class ReviewHardeningTests(unittest.TestCase):
    """Codex review of PR 379: validators must not be bypassable."""

    def setUp(self):
        self.data = lab.load()

    def mutated(self, fn, today=None):
        data = copy.deepcopy(self.data)
        fn(data)
        return lab.validate(data, today=today) if today else lab.validate(data)

    def test_sample_floor_must_be_an_integer_of_at_least_ten(self):
        for bad in (0, 1, 9, -5, 10.5, True, "<img src=x onerror=alert(1)>", None):
            problems = self.mutated(lambda d, b=bad: d["packs"].update(sample_floor_per_cell=b))
            self.assertTrue(any("sample_floor_per_cell" in p for p in problems), repr(bad))

    def test_sample_floor_cannot_disable_the_measured_check(self):
        def sneaky(d):
            d["packs"]["sample_floor_per_cell"] = 0
            d["harnesses"]["items"][0]["measured"] = {"n": 0, "source": "missing"}
        problems = self.mutated(sneaky)
        self.assertTrue(any("sample_floor_per_cell" in p for p in problems))
        self.assertTrue(any("sample floor" in p for p in problems))

    def test_measured_n_of_zero_is_rejected_even_with_a_source(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"][0].update(measured={"n": 0, "source": "lab/results/x.md"}))
        self.assertTrue(any("sample floor" in p for p in problems))

    def test_rendering_escapes_a_hostile_floor_and_other_numbers(self):
        data = copy.deepcopy(self.data)
        data["packs"]["sample_floor_per_cell"] = "<img src=x onerror=alert(1)>"
        data["experiments"][0]["budget"]["frank_hours"] = "<b>x</b>"
        page = lab.render(data, lab.summarize_receipts(Path("none.jsonl")))
        self.assertNotIn("<img src=x", page)
        self.assertNotIn("<b>x</b>", page)

    def test_json_nan_and_infinity_are_rejected_at_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "budget.json"
            for literal in ("NaN", "Infinity", "-Infinity"):
                path.write_text('{"lab_allocation_usd": %s}' % literal, encoding="utf-8")
                with self.assertRaises(ValueError, msg=literal):
                    lab.read_json(path)

    def test_non_finite_allocation_cannot_let_a_huge_cap_through(self):
        def nan_budget(d):
            d["budget"]["token_pass"]["lab_allocation_usd"] = float("nan")
            d["experiments"][0]["budget"]["token_pass_usd_cap"] = 999
        problems = self.mutated(nan_budget)
        self.assertTrue(any("finite non-negative" in p for p in problems))

    def test_duplicate_pillar_project_and_task_ids_are_rejected(self):
        self.assertTrue(any("pillars: duplicate" in p for p in self.mutated(
            lambda d: d["goals"]["pillars"].append(dict(d["goals"]["pillars"][0])))))
        self.assertTrue(any("projects: duplicate" in p for p in self.mutated(
            lambda d: d["goals"]["projects"].append(dict(d["goals"]["projects"][0])))))
        self.assertTrue(any("task ids" in p for p in self.mutated(
            lambda d: d["packs"]["items"][0]["tasks"].append(dict(d["packs"]["items"][0]["tasks"][0])))))
        self.assertTrue(any("task ids" in p for p in self.mutated(
            lambda d: d["packs"]["items"][0]["tasks"][0].update(id=" "))))

    def test_a_future_start_date_is_rejected_for_every_status(self):
        today = dt.date(2026, 10, 22)
        for status in ("running", "blocked", "ready"):
            def future(d, st=status):
                e = d["experiments"][4]
                e["status"] = st
                e["clock"]["started"] = "2099-01-01"
                if st == "running":
                    e["blocked_by"] = []
            problems = self.mutated(future, today=today)
            self.assertTrue(any("in the future" in p for p in problems), status)

    def test_an_unparseable_start_date_is_rejected_even_when_not_running(self):
        problems = self.mutated(lambda d: d["experiments"][0]["clock"].update(started="soon"), today=dt.date(2026, 10, 22))
        self.assertTrue(any("not a date" in p for p in problems))

    def test_tier_one_and_above_never_runs_on_the_laptop(self):
        def laptop(d):
            d["experiments"][0]["tier"] = "T1"
            d["experiments"][0]["runs_on"] = [{"where": "local-c940", "why": "x"}]
        self.assertTrue(any("never go on the laptop" in p for p in self.mutated(laptop)))

    def test_shipped_t1_experiments_run_on_a_cloud_worker(self):
        by_id = {e["id"]: e for e in self.data["experiments"]}
        for eid in ("EXP-001", "EXP-006", "EXP-008", "EXP-009"):
            self.assertIn(by_id[eid].get("tier"), ("T1", "T2"), eid)
            self.assertEqual([r["where"] for r in by_id[eid]["runs_on"]], ["railway"], eid)
            self.assertIn("worker-phase-0", by_id[eid]["blocked_by"], eid)

    def test_free_only_experiment_has_no_paid_arm_and_no_token_pass_cap(self):
        exp = next(e for e in self.data["experiments"] if e["id"] == "EXP-006")
        self.assertEqual(exp["budget"]["token_pass_usd_cap"], 0)
        for arm in exp["arms"]:
            self.assertNotIn("vercel/", arm["model"])
            self.assertNotIn("paid", arm["role"])
            self.assertNotIn("EXP-001", arm["model"])

    def test_stock_omo_is_its_own_control_arm(self):
        harnesses = {h["id"]: h for h in self.data["harnesses"]["items"]}
        self.assertFalse(harnesses["omo-stock"]["governed_by_routing_brain"])
        self.assertTrue(harnesses["now"]["governed_by_routing_brain"])
        exp = next(e for e in self.data["experiments"] if e["id"] == "EXP-008")
        arms = {a["harness"]: a for a in exp["arms"]}
        self.assertEqual(set(arms), {"opencode-bare", "omo-stock", "now", "oms"})
        self.assertTrue(set(arms) <= set(harnesses))
        self.assertNotIn("stock OmO", arms["now"]["role"])

    def test_receipt_columns_do_not_claim_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "routing.jsonl"
            rec = {"task_class": "code", "used": "m", "success": True, "cost_usd": 0.5,
                   "provider": "token-pass", "ts": "2026-10-02T00:00:00Z"}
            path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
            page = lab.render(self.data, lab.summarize_receipts(path))
        self.assertIn("Call success", page)
        self.assertIn("Cost per successful call", page)
        self.assertNotIn("Per accepted", page)
        self.assertNotIn("<th>Accepted</th>", page)

    def test_plan_doc_totals_match_the_registry(self):
        tp = sum(e["budget"]["token_pass_usd_cap"] for e in self.data["experiments"])
        infra = sum(e["budget"]["infra_usd_cap"] for e in self.data["experiments"])
        doc = Path(__file__).resolve().parents[1] / "ops" / "plans" / "2026-10-21-research-lab-and-cloud-workers.md"
        want = f"Committed caps: ${tp:g} of the $30 Token Pass lab allocation, ${infra:g} of the proposed $20 Railway cap"
        self.assertIn(want, doc.read_text(encoding="utf-8"))


class PassTwoHardeningTests(unittest.TestCase):
    """Codex pass 2 of PR 379: every finding gets a test that fails on the previous validators."""

    def setUp(self):
        self.data = lab.load()

    def mutated(self, fn):
        data = copy.deepcopy(self.data)
        fn(data)
        return lab.validate(data)

    def exp(self, d, eid):
        return next(e for e in d["experiments"] if e["id"] == eid)

    # 3: routing rows need real booleans and an explicit cost
    def summary(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "routing.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
            return lab.summarize_receipts(path, now=dt.datetime(2026, 10, 21, tzinfo=dt.timezone.utc))

    def test_a_row_is_not_a_measurement_without_real_booleans_and_an_explicit_cost(self):
        base = {"task_class": "code", "used": "m", "success": True, "cost_usd": 0.5}
        bad_rows = [
            {**base, "synthetic": 1, "success": "false"},
            {**base, "success": "false"},
            {**base, "success": 1},
            {k: v for k, v in base.items() if k != "cost_usd"},
            {**base, "cost_usd": "0.5"},
            {**base, "cost_usd": True},
            {**base, "cost_usd": -1},
            {k: v for k, v in base.items() if k != "success"},
        ]
        s = self.summary(bad_rows + [base])
        self.assertEqual(s["used"], 1)
        self.assertEqual(s["skipped"], len(bad_rows))
        self.assertEqual(s["synthetic"], 0)

    # 4: checker types are classified
    def test_relabelling_a_judge_cannot_hide_it_from_the_share(self):
        def relabel(d):
            for t in d["packs"]["items"][0]["tasks"]:
                t["judged"] = False
                t["verifier"]["type"] = "human-review"
        problems = self.mutated(relabel)
        self.assertTrue(any("tasks are judged" in p for p in problems))

    def test_unknown_checker_types_are_an_error_and_count_as_judged(self):
        def unknown(d):
            for t in d["packs"]["items"][0]["tasks"]:
                t["judged"] = False
                t["verifier"]["type"] = "vibes"
        problems = self.mutated(unknown)
        self.assertTrue(any("checker type 'vibes'" in p for p in problems))
        self.assertTrue(any("tasks are judged" in p for p in problems))
        self.assertEqual(lab.pack_judged_share({"tasks": [{"verifier": {"type": "vibes", "check": "x"}, "judged": False}]}), 1.0)

    def test_judged_must_be_a_real_boolean(self):
        problems = self.mutated(lambda d: d["packs"]["items"][0]["tasks"][0].update(judged="no"))
        self.assertTrue(any("real boolean" in p for p in problems))

    # 5: required fields never reach the renderer as a KeyError
    def test_missing_dashboard_fields_are_validation_errors_not_render_crashes(self):
        cases = {
            "harness name": lambda d: d["harnesses"]["items"][0].pop("name"),
            "harness id": lambda d: d["harnesses"]["items"][0].update(id=" "),
            "pack id": lambda d: d["packs"]["items"][0].update(id="  "),
            "pack title": lambda d: d["packs"]["items"][0].pop("title"),
            "gate id": lambda d: d["gates"]["items"][0].pop("id"),
            "gate status": lambda d: d["gates"]["items"][0].update(status="maybe"),
            "gate kind": lambda d: d["gates"]["items"][0].pop("kind"),
            "pillar name": lambda d: d["goals"]["pillars"][0].pop("name"),
        }
        for label, fn in cases.items():
            self.assertTrue(self.mutated(fn), label)

    # 6: measured claims need a real evidence file
    def test_a_measured_claim_needs_an_existing_evidence_file(self):
        for source in (True, "", "  ", "lab/results/does-not-exist.md", "../outside.md", "C:/Windows/win.ini", "lab"):
            problems = self.mutated(lambda d, s=source: d["harnesses"]["items"][0].update(
                measured={"n": 10, "source": s, "accepted_rate": 1}))
            self.assertTrue(any("measured" in p for p in problems), repr(source))

    def test_a_measured_claim_with_an_existing_source_passes(self):
        problems = self.mutated(lambda d: d["harnesses"]["items"][0].update(
            measured={"n": 10, "source": "lab/budget.json", "accepted_rate": 1}))
        self.assertEqual(problems, [])

    # 7: every experiment declares its tier
    def test_every_experiment_has_a_tier(self):
        for exp in self.data["experiments"]:
            self.assertIn(exp["tier"], lab.TIERS, exp["id"])
        problems = self.mutated(lambda d: self.exp(d, "EXP-008").pop("tier"))
        self.assertTrue(any("explicit tier" in p for p in problems))

    def test_a_t2_experiment_cannot_run_on_the_laptop(self):
        def move(d):
            self.exp(d, "EXP-008")["runs_on"] = [{"where": "local-c940", "why": "x"}]
        problems = self.mutated(move)
        self.assertTrue(any("never go on the laptop" in p for p in problems))

    # 8: actor ids are normalised
    def test_owner_and_verifier_variants_are_the_same_actor(self):
        for variant in (" CLAUDE ", "Claude", "claude\t"):
            problems = self.mutated(lambda d, v=variant: self.exp(d, "EXP-001").update(owner="claude", verifier=v))
            self.assertTrue(any("different actor" in p for p in problems), repr(variant))

    def test_blank_actor_ids_are_rejected(self):
        problems = self.mutated(lambda d: self.exp(d, "EXP-001").update(owner=" ", verifier=" "))
        self.assertTrue(any("non-empty actor" in p for p in problems))

    # 9: arms name registered harnesses
    def test_an_arm_must_name_a_registered_harness(self):
        problems = self.mutated(lambda d: self.exp(d, "EXP-008")["arms"][0].update(harness="does-not-exist"))
        self.assertTrue(any("not in lab/harnesses.json" in p for p in problems))

    def test_every_shipped_arm_is_registered_or_explicitly_pending(self):
        registered = {h["id"] for h in self.data["harnesses"]["items"]}
        for exp in self.data["experiments"]:
            for arm in exp["arms"]:
                self.assertTrue(arm.get("harness") in registered or arm.get("harness_pending"), (exp["id"], arm))
                self.assertFalse("harness" in arm and "harness_pending" in arm, (exp["id"], arm))

    def test_an_arm_cannot_be_both_registered_and_pending_or_neither(self):
        both = self.mutated(lambda d: self.exp(d, "EXP-008")["arms"][0].update(harness_pending="x"))
        self.assertTrue(any("both harness and harness_pending" in p for p in both))
        neither = self.mutated(lambda d: self.exp(d, "EXP-008")["arms"][0].pop("harness"))
        self.assertTrue(any("needs a registered harness" in p for p in neither))

    def test_pending_arms_are_shown_as_to_be_decided(self):
        page = lab.render(self.data, lab.summarize_receipts(Path("none.jsonl")))
        self.assertIn("TBD: best harness from EXP-002", page)

    # 10: sub-floor designs are directional pilots
    def test_a_sub_floor_design_must_declare_no_decision_effect(self):
        def one_run(d):
            self.exp(d, "EXP-001")["design"] = {"runs_per_cell": 1, "decision_effect": "routing"}
        problems = self.mutated(one_run)
        self.assertTrue(any("below the sample floor" in p for p in problems))

    def test_exp_001_and_006_are_labelled_directional_pilots(self):
        for eid in ("EXP-001", "EXP-006"):
            exp = next(e for e in self.data["experiments"] if e["id"] == eid)
            self.assertEqual(exp["design"]["runs_per_cell"], 1, eid)
            self.assertEqual(exp["design"]["decision_effect"], "none", eid)
            self.assertIn("Directional", exp["kill"], eid)
            self.assertIn("Directional", exp["success_rule"], eid)

    def test_runs_per_cell_must_be_a_positive_integer(self):
        for bad in (0, -1, 1.5, True, "10", None):
            problems = self.mutated(lambda d, b=bad: self.exp(d, "EXP-001").update(design={"runs_per_cell": b, "decision_effect": "none"}))
            self.assertTrue(any("runs_per_cell" in p for p in problems), repr(bad))


if __name__ == "__main__":
    unittest.main()
