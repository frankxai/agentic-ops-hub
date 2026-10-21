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
        problems = self.mutated(judge_all)
        self.assertTrue(any("judged" in p for p in problems))

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


if __name__ == "__main__":
    unittest.main()
