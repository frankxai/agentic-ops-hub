import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.merge_steward import (
    PolicyError,
    classify,
    decide,
    digest,
    glob_to_regex,
    normalize_verdict,
    parse_dependency_bump,
    parse_policy_text,
)

TEMPLATE = (Path(__file__).resolve().parents[1] / "templates" / "merge-policy.yml").read_text(encoding="utf-8")

APPROVE = json.dumps({"verdict": "approve", "summary": "clean", "issues": []})
REJECT = json.dumps({"verdict": "request_changes", "summary": "bug", "issues": []})


def f(name: str, patch: str | None = "@@ -1 +1 @@\n-a\n+b", status: str = "modified") -> dict:
    return {"filename": name, "status": status, "patch": patch}


def tier(files, title="docs: tweak", labels=(), policy=TEMPLATE, **kw) -> str:
    return classify(files, title, list(labels), policy, **kw)["tier"]


class PolicyParsingTests(unittest.TestCase):
    def test_template_parses(self) -> None:
        policy = parse_policy_text(TEMPLATE)
        self.assertEqual(1, policy["version"])
        self.assertIn("contracts/**", policy["human"])
        self.assertEqual(10, policy["daily_merge_cap"])

    def test_nested_mapping_inline_list_and_comments(self) -> None:
        policy = parse_policy_text("a: 1 # note\nb:\n  c: 'x # y'\n  d: [p, q]\ne:\n- one\n- two\n")
        self.assertEqual({"a": 1, "b": {"c": "x # y", "d": ["p", "q"]}, "e": ["one", "two"]}, policy)

    def test_unsupported_syntax_raises(self) -> None:
        with self.assertRaises(PolicyError):
            parse_policy_text("a: {b: 1}\n")
        with self.assertRaises(PolicyError):
            parse_policy_text("just a string\n")


class GlobTests(unittest.TestCase):
    def test_single_star_stays_in_directory(self) -> None:
        self.assertTrue(glob_to_regex("docs/*.md").match("docs/a.md"))
        self.assertFalse(glob_to_regex("docs/*.md").match("docs/sub/a.md"))

    def test_double_star_crosses_directories_and_matches_root(self) -> None:
        self.assertTrue(glob_to_regex("**/*.md").match("README.md"))
        self.assertTrue(glob_to_regex("**/*.md").match("a/b/c.md"))
        self.assertTrue(glob_to_regex("contracts/**").match("contracts/src/Token.sol"))


class PathTierTests(unittest.TestCase):
    def test_docs_only_is_auto(self) -> None:
        self.assertEqual("auto", tier([f("docs/guide.md"), f("README.md")]))

    def test_tests_only_is_auto(self) -> None:
        self.assertEqual("auto", tier([f("tests/test_x.py"), f("e2e/foo.spec.ts")]))

    def test_colocated_test_under_review_glob_is_review(self) -> None:
        # Most restrictive match wins: src/** (review) beats **/*.test.* (auto).
        self.assertEqual("review", tier([f("src/foo.test.ts")]))

    def test_application_code_is_review(self) -> None:
        self.assertEqual("review", tier([f("docs/a.md"), f("app/page.tsx")]))

    def test_unmatched_file_uses_default_tier(self) -> None:
        self.assertEqual("review", tier([f("weird/place.bin")]))

    def test_contracts_are_human(self) -> None:
        self.assertEqual("human", tier([f("contracts/Token.sol"), f("docs/a.md")]))

    def test_human_glob_beats_auto_glob(self) -> None:
        # CLAUDE.md matches both `**/*.md` (auto) and `CLAUDE.md` (human).
        self.assertEqual("human", tier([f("CLAUDE.md")]))

    def test_payments_auth_secrets_infra_are_human(self) -> None:
        for path in ("app/api/stripe/webhook.ts", "lib/auth/session.ts", "vercel.json", "infra/main.tf", "LICENSE"):
            with self.subTest(path=path):
                self.assertEqual("human", tier([f(path)]))

    def test_policy_file_and_steward_workflow_are_builtin_human(self) -> None:
        permissive = "version: 1\ndefault_tier: auto\nauto:\n  - '**'\n"
        self.assertEqual("human", tier([f(".github/merge-policy.yml")], policy=permissive))
        self.assertEqual("human", tier([f(".github/workflows/merge-steward.yml", patch="@@\n+# c")], policy=permissive))
        self.assertEqual("human", tier([f("web/.env.production")], policy=permissive))

    def test_rename_out_of_human_path_is_still_human(self) -> None:
        entry = f("docs/moved.md")
        entry["previous_filename"] = "contracts/Token.sol"
        self.assertEqual("human", tier([entry]))

    def test_label_forces_human(self) -> None:
        self.assertEqual("human", tier([f("docs/a.md")], labels=["steward:hold"]))

    def test_too_many_files_is_human(self) -> None:
        self.assertEqual("human", tier([f(f"docs/{i}.md") for i in range(301)]))

    def test_steward_authored_pr_is_human(self) -> None:
        self.assertEqual("human", tier([f("docs/a.md")], author="frankx-steward[bot]", steward_login="frankx-steward[bot]"))


class FailClosedTests(unittest.TestCase):
    def test_missing_policy_is_human(self) -> None:
        result = classify([f("docs/a.md")], "docs", [], None)
        self.assertEqual("human", result["tier"])
        self.assertIn("fail closed", result["reasons"][0])

    def test_unparseable_policy_is_human(self) -> None:
        self.assertEqual("human", tier([f("docs/a.md")], policy="version: 1\nauto: {x: 1}\n"))

    def test_wrong_version_is_human(self) -> None:
        self.assertEqual("human", tier([f("docs/a.md")], policy="version: 2\n"))

    def test_no_files_is_human(self) -> None:
        self.assertEqual("human", tier([]))


class DependencyBumpTests(unittest.TestCase):
    def test_parse_dependabot_patch_and_minor(self) -> None:
        self.assertEqual("patch", parse_dependency_bump("Bump next from 15.1.2 to 15.1.4")["level"])
        self.assertEqual("minor", parse_dependency_bump("chore(deps-dev): bump @types/node from 20.1.0 to 20.2.0 in /web")["level"])

    def test_parse_major_and_zero_minor_are_major(self) -> None:
        self.assertEqual("major", parse_dependency_bump("Bump react from 18.3.1 to 19.0.0")["level"])
        self.assertEqual("major", parse_dependency_bump("Bump zod from 0.9.1 to 0.10.0")["level"])

    def test_grouped_and_renovate_without_level_are_unknown(self) -> None:
        self.assertEqual("unknown", parse_dependency_bump("Bump the npm_and_yarn group across 1 directory with 3 updates")["level"])
        self.assertEqual("unknown", parse_dependency_bump("Update dependency next to v15.1.4")["level"])

    def test_non_bump_title(self) -> None:
        self.assertIsNone(parse_dependency_bump("feat: add pricing page"))

    def test_patch_bump_on_manifest_and_lockfile_is_auto(self) -> None:
        files = [f("package.json"), f("pnpm-lock.yaml")]
        self.assertEqual("auto", tier(files, title="Bump next from 15.1.2 to 15.1.4"))

    def test_major_bump_is_review(self) -> None:
        files = [f("package.json"), f("pnpm-lock.yaml")]
        self.assertEqual("review", tier(files, title="Bump react from 18.3.1 to 19.0.0"))

    def test_bump_title_with_code_change_is_not_auto(self) -> None:
        files = [f("package.json"), f("pnpm-lock.yaml"), f("app/page.tsx")]
        self.assertEqual("review", tier(files, title="Bump next from 15.1.2 to 15.1.4"))

    def test_lockfile_change_without_bump_title_is_review(self) -> None:
        self.assertEqual("review", tier([f("pnpm-lock.yaml")], title="chore: refresh lockfile"))


class WorkflowTests(unittest.TestCase):
    def test_non_security_workflow_edit_follows_policy(self) -> None:
        patch = "@@ -10 +10 @@\n-          node-version: 20\n+          node-version: 22"
        self.assertEqual("auto", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_permissions_change_is_human(self) -> None:
        patch = "@@ -1,3 +1,4 @@\n permissions:\n-  contents: read\n+  contents: write"
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_new_permissions_block_is_human(self) -> None:
        patch = "@@ -1 +1,3 @@\n+permissions:\n+  issues: read"
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_secrets_reference_is_human(self) -> None:
        patch = "@@\n+          API_KEY: ${{ secrets.OPENAI_API_KEY }}"
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_privileged_trigger_is_human(self) -> None:
        patch = "@@\n on:\n-  pull_request:\n+  pull_request_target:"
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_action_swap_is_review(self) -> None:
        patch = "@@\n-      - uses: actions/checkout@v4\n+      - uses: someone/checkout@v1"
        self.assertEqual("review", tier([f(".github/workflows/ci.yml", patch=patch)]))

    def test_missing_patch_or_deleted_workflow_is_human(self) -> None:
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", patch=None)]))
        self.assertEqual("human", tier([f(".github/workflows/ci.yml", status="removed")]))

    def test_context_lines_do_not_trigger(self) -> None:
        # Unchanged context mentioning permissions must not escalate a harmless edit.
        patch = "@@\n permissions:\n   contents: read\n-  name: CI\n+  name: CI checks"
        self.assertEqual("auto", tier([f(".github/workflows/ci.yml", patch=patch)]))


class VerdictTests(unittest.TestCase):
    def test_malformed_verdicts_block(self) -> None:
        for raw in (None, "", "not json", "{}", json.dumps({"verdict": "lgtm"})):
            with self.subTest(raw=raw):
                self.assertEqual("block", normalize_verdict(raw)["verdict"])

    def test_approve_with_high_severity_issue_is_downgraded(self) -> None:
        raw = {"verdict": "approve", "issues": [{"severity": "high", "note": "sql injection"}]}
        self.assertEqual("request_changes", normalize_verdict(raw)["verdict"])


class DecideTests(unittest.TestCase):
    def test_kill_switch_skips_everything(self) -> None:
        self.assertEqual("skip", decide("auto", "live", "off", APPROVE)["action"])

    def test_human_tier_never_merges(self) -> None:
        self.assertEqual("human", decide("human", "live", "", APPROVE, APPROVE)["action"])

    def test_shadow_mode_only_comments(self) -> None:
        result = decide("auto", "shadow", "", APPROVE)
        self.assertEqual(("comment", "merge"), (result["action"], result["would"]))

    def test_unset_mode_is_shadow(self) -> None:
        self.assertEqual("comment", decide("auto", "", "", APPROVE)["action"])

    def test_live_auto_merges_on_primary_approve(self) -> None:
        self.assertEqual("merge", decide("auto", "live", "", APPROVE)["action"])

    def test_review_tier_needs_both_reviews(self) -> None:
        self.assertEqual("hold", decide("review", "live", "", APPROVE, REJECT)["action"])
        self.assertEqual("hold", decide("review", "live", "", APPROVE, None)["action"])
        self.assertEqual("merge", decide("review", "live", "", APPROVE, APPROVE)["action"])

    def test_guards_hold_eligible_merges(self) -> None:
        self.assertEqual("hold", decide("auto", "live", "", APPROVE, merged_today=10, daily_cap=10)["action"])
        self.assertEqual("hold", decide("auto", "live", "", APPROVE, open_incidents=1)["action"])
        self.assertEqual("hold", decide("auto", "live", "", APPROVE, secrets_ok=False)["action"])

    def test_unknown_tier_fails_closed(self) -> None:
        self.assertEqual("human", decide("yolo", "live", "", APPROVE)["action"])


class DigestTests(unittest.TestCase):
    def test_lists_only_human_items_with_stats(self) -> None:
        now = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
        open_prs = [
            {"number": 1, "title": "Change payouts", "createdAt": "2026-09-29T12:00:00Z", "url": "u1", "labels": [{"name": "steward:needs-human"}]},
            {"number": 2, "title": "Docs", "createdAt": "2026-09-30T10:00:00Z", "url": "u2", "labels": []},
        ]
        merged = [{"number": 3, "labels": [{"name": "steward:merged"}]}]
        text = digest(open_prs, merged, [], 0.0, now=now)
        self.assertIn("#1 Change payouts", text)
        self.assertNotIn("#2 Docs", text)
        self.assertIn("| merged by steward | 1 |", text)
        self.assertIn("| human queue | 1 |", text)


if __name__ == "__main__":
    unittest.main()
