#!/usr/bin/env python3
"""Estate CI watch — no default branch stays red unnoticed.

The 2026-09-27 sweep found four repos whose main had been red for two to three
months, and private-repo CI silently blocked by an exhausted Actions budget
while public repos (billed at zero) kept looking healthy. Nothing alerted,
because each repo's CI only reports inside that repo.

This script runs from a scheduled workflow in this PUBLIC repo, so a budget
block on private repos cannot silence it. For every active, non-archived repo
owned by --owner it reads the default branch's recent workflow runs and flags:
  1. A workflow whose current failure streak began more than --max-red-hours
     ago (measured from the oldest run in the unbroken streak, so a workflow
     that fails every hour is still caught).
  2. Failed jobs that never started (no steps, no runner) — the signature of
     an Actions budget or billing block rather than a code failure.

Needs ESTATE_READ_TOKEN: a fine-grained token with read access to Actions and
Metadata on all repos of the owner. Exit 1 prints one finding per line; the
workflow files them as a durable issue (durable-output-sink law).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
RED = {"failure", "timed_out", "startup_failure"}


def parse_ts(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def red_streak_start(runs: list[dict]) -> datetime | None:
    """Oldest run of the unbroken failure streak, given one workflow's runs newest-first.

    Returns None when the newest completed run is not red. Runs still in
    progress are skipped: they neither extend nor break a streak.
    """
    start: datetime | None = None
    for run in runs:
        if run.get("status") != "completed":
            continue
        if run.get("conclusion") in RED:
            start = parse_ts(run["created_at"])
            continue
        if run.get("conclusion") in ("cancelled", "skipped", "neutral"):
            continue
        break
    return start


def never_started(jobs: list[dict]) -> list[str]:
    return [
        job["name"]
        for job in jobs
        if job.get("conclusion") == "failure" and not job.get("steps") and not job.get("runner_name")
    ]


def workflow_key(run: dict) -> str:
    # Dependabot names each update run uniquely ("npm_and_yarn in / for qs - Update #123"),
    # so a later successful update would never clear an earlier failure. Judge them
    # per ecosystem: directory lists change when dependabot.yml is regrouped, which
    # would otherwise leave a key that can never run again.
    # Everything else is keyed by workflow_id: a workflow whose YAML failed to parse
    # runs under its file path, then under its real name once fixed, so a name key
    # would keep the broken era's red run alive forever.
    name = run.get("name") or ""
    if run.get("event") == "dynamic" and " in " in name:
        return "Dependabot " + name.split(" in ", 1)[0]
    return str(run.get("workflow_id") or name)


def find_findings(
    repo: str,
    runs: list[dict],
    now: datetime,
    max_red_hours: float,
    live_workflow_ids: set[int] | None = None,
) -> tuple[list[str], list[int]]:
    """Return (red-streak findings, run ids whose jobs should be checked for a budget block).

    A deleted workflow file drops out of the repo's workflow list but its last red run
    stays in history forever, so when live_workflow_ids is given, runs of workflows that
    no longer exist are ignored. Dependabot runs (event "dynamic") are always judged.
    """
    if live_workflow_ids is not None:
        runs = [r for r in runs if r.get("event") == "dynamic" or r.get("workflow_id") in live_workflow_ids]
    by_workflow: dict[str, list[dict]] = {}
    for run in sorted(runs, key=lambda r: r["created_at"], reverse=True):
        by_workflow.setdefault(workflow_key(run), []).append(run)

    findings: list[str] = []
    suspects: list[int] = []
    for key, wf_runs in sorted(by_workflow.items()):
        start = red_streak_start(wf_runs)
        if start is None:
            continue
        latest_red = next(r for r in wf_runs if r.get("conclusion") in RED)
        name = key if key.startswith("Dependabot ") else (wf_runs[0].get("name") or key)
        suspects.append(latest_red["id"])
        if start < now - timedelta(hours=max_red_hours):
            days = (now - start).total_seconds() / 86400
            findings.append(
                f"{repo}: '{name}' red on default branch for {days:.1f}d "
                f"(since {start.date().isoformat()}) — {latest_red.get('html_url', '')}"
            )
    return findings, suspects


def get(path: str, token: str) -> dict | list:
    req = urllib.request.Request(
        API + path,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def active_repos(owner: str, token: str, active_days: int, now: datetime) -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        batch = get(f"/users/{owner}/repos?type=owner&per_page=100&page={page}", token)
        if not batch:
            break
        repos.extend(batch)
        page += 1
    cutoff = now - timedelta(days=active_days)
    return [
        r
        for r in repos
        if not r.get("archived") and not r.get("fork") and parse_ts(r["pushed_at"]) >= cutoff
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="frankxai")
    parser.add_argument("--max-red-hours", type=float, default=24)
    parser.add_argument("--active-days", type=int, default=60)
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    token = os.environ.get("ESTATE_READ_TOKEN", "")
    if not token:
        print("estate-ci-watch: 1 finding")
        print("- ESTATE_READ_TOKEN secret is not configured; the estate is unwatched")
        return 1

    findings: list[str] = []
    blocked: list[str] = []
    repos = active_repos(args.owner, token, args.active_days, now)
    for repo in repos:
        full = repo["full_name"]
        branch = repo["default_branch"]
        try:
            runs = get(f"/repos/{full}/actions/runs?branch={branch}&per_page=100", token)["workflow_runs"]
            workflows = get(f"/repos/{full}/actions/workflows?per_page=100", token)["workflows"]
        except urllib.error.HTTPError as err:
            findings.append(f"{full}: could not read workflow runs (HTTP {err.code})")
            continue
        live_ids = {w["id"] for w in workflows}
        repo_findings, suspects = find_findings(full, runs, now, args.max_red_hours, live_ids)
        findings.extend(repo_findings)
        for run_id in suspects:
            jobs = get(f"/repos/{full}/actions/runs/{run_id}/jobs", token)["jobs"]
            for name in never_started(jobs):
                blocked.append(f"{full}: job '{name}' never started (run {run_id})")

    if blocked:
        findings.insert(
            0,
            f"{len(blocked)} failed job(s) never started — likely the Actions budget/spending "
            "limit, not code: " + "; ".join(blocked[:10]) + (" …" if len(blocked) > 10 else ""),
        )
    if not findings:
        print(f"estate-ci-watch: {len(repos)} active repos, all default branches green or recovering")
        return 0
    print(f"estate-ci-watch: {len(findings)} finding(s) across {len(repos)} active repos as of {now.isoformat(timespec='seconds')}")
    for finding in findings:
        print(f"- {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
