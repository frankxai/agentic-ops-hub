import json
import re
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "studio"


class ContentStudioContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((STUDIO / "content-studio.manifest.json").read_text(encoding="utf-8"))
        self.data = json.loads((STUDIO / "studio-data.json").read_text(encoding="utf-8"))
        self.html = (STUDIO / "index.html").read_text(encoding="utf-8")

    def test_manifest_keeps_the_studio_draft_only(self):
        self.assertEqual("draft_only", self.manifest["lifecycle"])
        self.assertIn("publish", self.manifest["prohibited_actions"])
        self.assertIn("schedule", self.manifest["prohibited_actions"])
        self.assertIn("oauth", self.manifest["prohibited_actions"])
        self.assertEqual(0, self.data["metrics"]["external_actions"])

    def test_research_records_have_provenance_and_bounded_decisions(self):
        allowed = {"adopt", "pilot", "watch", "reject", "research_only"}
        for record in self.data["research"]:
            for key in ("source_url", "source_kind", "retrieved_at", "confidence", "rights_state", "decision", "constraint"):
                self.assertTrue(record.get(key), f"{record['id']} is missing {key}")
            datetime.fromisoformat(record["retrieved_at"].replace("Z", "+00:00"))
            self.assertIn(record["decision"], allowed)

    def test_drafts_are_original_and_trace_to_known_research(self):
        research_ids = {record["id"] for record in self.data["research"]}
        draft_ids = [draft["id"] for draft in self.data["drafts"]]
        self.assertEqual(len(draft_ids), len(set(draft_ids)))
        for draft in self.data["drafts"]:
            self.assertEqual("draft", draft["status"])
            self.assertTrue(draft["draft_body"])
            self.assertTrue(draft["claims"])
            self.assertTrue(draft["accessibility"])
            self.assertIn("Original", draft["rights"])
            self.assertTrue(set(draft["source_refs"]).issubset(research_ids))

    def test_static_ui_has_local_data_and_accessible_operating_controls(self):
        self.assertIn('fetch(\'./studio-data.json\'', self.html)
        self.assertIn('<main id="workspace"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('aria-label="Search content studio"', self.html)
        self.assertIn('.sr-only {', self.html)
        self.assertIn('prefers-reduced-motion: reduce', self.html)
        self.assertIn('Copy draft text', self.html)
        self.assertNotRegex(self.html, r"https?://[^\"]+(?:api|oauth|publish|schedule)")


if __name__ == "__main__":
    unittest.main()
