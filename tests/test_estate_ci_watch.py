import unittest
from datetime import datetime, timezone

from scripts.estate_ci_watch import find_findings, never_started, red_streak_start

NOW = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)


def run(run_id: int, day: int, conclusion: str | None, name: str = "CI", status: str = "completed") -> dict:
    return {
        "id": run_id,
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "created_at": f"2026-09-{day:02d}T06:00:00Z",
        "html_url": f"https://example/runs/{run_id}",
    }


class RedStreakTests(unittest.TestCase):
    def test_green_latest_has_no_streak(self) -> None:
        self.assertIsNone(red_streak_start([run(2, 27, "success"), run(1, 26, "failure")]))

    def test_streak_starts_at_oldest_consecutive_failure(self) -> None:
        runs = [run(3, 27, "failure"), run(2, 20, "failure"), run(1, 10, "success")]
        self.assertEqual(datetime(2026, 9, 20, 6, 0, tzinfo=timezone.utc), red_streak_start(runs))

    def test_in_progress_and_cancelled_runs_do_not_break_streak(self) -> None:
        runs = [
            run(4, 28, None, status="in_progress"),
            run(3, 27, "cancelled"),
            run(2, 25, "failure"),
            run(1, 1, "success"),
        ]
        self.assertEqual(datetime(2026, 9, 25, 6, 0, tzinfo=timezone.utc), red_streak_start(runs))


class FindingsTests(unittest.TestCase):
    def test_hourly_failing_workflow_is_caught_by_streak_age(self) -> None:
        runs = [run(3, 28, "failure"), run(2, 27, "failure"), run(1, 1, "failure")]
        findings, suspects = find_findings("o/r", runs, NOW, max_red_hours=24)
        self.assertEqual(1, len(findings))
        self.assertIn("since 2026-09-01", findings[0])
        self.assertEqual([3], suspects)

    def test_fresh_failure_is_suspect_but_not_yet_a_finding(self) -> None:
        findings, suspects = find_findings("o/r", [run(1, 28, "failure")], NOW, max_red_hours=24)
        self.assertEqual([], findings)
        self.assertEqual([1], suspects)

    def test_workflows_are_judged_independently(self) -> None:
        runs = [run(2, 27, "success", name="CI"), run(1, 1, "failure", name="Link Checker")]
        findings, _ = find_findings("o/r", runs, NOW, max_red_hours=24)
        self.assertEqual(1, len(findings))
        self.assertIn("'Link Checker'", findings[0])


    def test_later_dependabot_success_clears_earlier_uniquely_named_failure(self) -> None:
        failed = run(1, 1, "failure", name="npm_and_yarn in / for qs - Update #111")
        passed = run(2, 27, "success", name="npm_and_yarn in /site for sharp - Update #222")
        for r in (failed, passed):
            r["event"] = "dynamic"
        findings, suspects = find_findings("o/r", [failed, passed], NOW, max_red_hours=24)
        self.assertEqual(([], []), (findings, suspects))


    def test_fixed_yaml_rename_clears_path_named_failure(self) -> None:
        broken = run(1, 1, "failure", name=".github/workflows/ci.yml")
        fixed = run(2, 27, "success", name="ci")
        for r in (broken, fixed):
            r["workflow_id"] = 42
        self.assertEqual(([], []), find_findings("o/r", [broken, fixed], NOW, max_red_hours=24))


    def test_deleted_workflow_red_run_is_ignored(self) -> None:
        gone = run(1, 1, "failure", name="Deploy")
        gone["workflow_id"] = 7
        live = run(2, 1, "failure", name="CI")
        live["workflow_id"] = 8
        dependabot = run(3, 1, "failure", name="npm_and_yarn in / for qs - Update #1")
        dependabot.update(event="dynamic", workflow_id=99)
        findings, _ = find_findings("o/r", [gone, live, dependabot], NOW, max_red_hours=24, live_workflow_ids={8})
        self.assertEqual(2, len(findings))
        self.assertFalse(any("'Deploy'" in f for f in findings))


class NeverStartedTests(unittest.TestCase):
    def test_budget_blocked_job_has_no_steps_and_no_runner(self) -> None:
        jobs = [
            {"name": "verify", "conclusion": "failure", "steps": [], "runner_name": None},
            {"name": "lint", "conclusion": "failure", "steps": [{"name": "x"}], "runner_name": "gh-1"},
        ]
        self.assertEqual(["verify"], never_started(jobs))


if __name__ == "__main__":
    unittest.main()
