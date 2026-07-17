# CLI-Max Swarm Operating Model

**Objective:** maximize **verified, integrated outcomes per wall-clock hour** from Frank's flat Max/Ultra/Heavy subscriptions. Token conservation is not the goal. Token burn without an accepted artifact is also not the goal.

## Hard audit conclusion (2026-07-17)

The earlier swarm underperformed for structural reasons:

1. **Configuration was counted as progress.** Thirteen cron definitions, queue entries, and non-empty reports were treated as outcomes even when no artifact, tests, commit, PR, or acceptance decision existed.
2. **The launcher optimized for activity, not delivery.** It launched detached processes, recorded PIDs, and considered any report file “complete.” It did not wait, enforce timeout itself, validate tests, or prove integration.
3. **Unsafe Codex widening hid gateway problems.** `danger-full-access` was used to bypass Hermes/Windows sandbox friction. The new rule is exact worktree + `workspace-write`; failure blocks instead of silently widening permissions.
4. **Declared auth was mistaken for usable capacity.** Claude reported `loggedIn: true` while a one-turn model call returned OAuth 401. OpenCode had zero credentials. A binary/version check is not a live lane.
5. **Local Git state hid the YogaBook.** C940's dirty/diverged checkout had no local Book heartbeat while `origin/main` had a fresh self-written YogaBook heartbeat. Status now reconciles local and fetched remote truth by timestamp.
6. **Parallelism ignored machine limits.** C940 has 16 GB RAM. Multiple heavy local agents caused pressure and shallow/failed work. We parallelize **across C940 + YogaBook**, but run one coding CLI at a time per 16 GB node.
7. **The same vague goal was delegated repeatedly.** Multiple analyses produced status theater. Lanes now have one owner, one bounded deliverable, one integration path, and an independent verifier.

## Subscription lanes

| Capacity pool | Primary work | Secondary work | Proof before use |
|---|---|---|---|
| **OpenAI Codex Max** | implementation, refactors, test repair | independent diff/test review | one-turn `codex exec` on exact repo/model |
| **Claude Max** | deep multi-file backend/TDD, architecture | independent review | one-turn `claude -p`; declared login is insufficient |
| **Gemini Ultra** | long-context mapping, research/visual synthesis | review packet | one-turn `gemini -p`; prefer Gemini 3.5 |
| **xAI Heavy via Hermes** | Queen orchestration, adversarial challenge, current web/X research, media | escalation/fallback | provider/profile live preflight |

Use flat subscriptions aggressively for real deliverables. Do **not** create duplicate speculative analyses merely to consume quota.

## Fleet topology

| Node | Ownership | Local concurrency | Default CLI |
|---|---|---:|---|
| **C940** | backend, SIS/ACOS, Railway, agentic-ops, integration | 1 heavy coding CLI | Claude Opus or Codex Terra-high |
| **YogaBook** | production frontend, UX/browser QA, product innovation | 1 heavy coding CLI | Codex Terra-high; Gemini 3.5 mapping/review |
| **Across fleet** | parallel independent owners | 2 total | one mission per node |

Hard launch gates on each node:

- dedicated clean worktree and exact expected branch;
- free disk >= 50 GB;
- memory <= 85%;
- successful live model preflight using the exact repo/model;
- no second writer in the same worktree;
- no `danger-full-access`, `--yolo`, force push, main push, or production deploy.

## Outcome lifecycle

```text
queued -> claimed -> artifact-produced -> tested -> integrated -> verified -> delivered
```

A mission is complete only when its receipt JSON proves:

```json
{
  "mission_id": "...",
  "status": "verified",
  "branch": "agent/<machine>/<scope>",
  "commit": "<sha>",
  "verification": [{"command": "<exact command>", "exit_code": 0}],
  "integration_state": "pr_open|merged|delivered|rejected|hold",
  "completed_at": "<ISO-8601>"
}
```

A Markdown report alone is never completion. A cron entry alone is never an outcome. A running PID is never an outcome.

## Dispatch contract

Every CLI mission must include:

1. **Owner:** one machine and one primary CLI.
2. **Outcome:** a user/business result, not “analyze repository.”
3. **Scope:** exact repo, clean worktree, branch, allowed files.
4. **Acceptance:** exact commands plus product checks.
5. **Artifact:** report and machine-readable receipt paths.
6. **Integration:** PR, merge decision, or explicit hold/rejection owner.
7. **Verifier:** a different CLI or deterministic CI.
8. **Timeout:** 45–180 minutes; no orphan process.

Preferred two-agent pattern:

- **Primary implementer:** Claude or Codex on one owned worktree.
- **Independent verifier:** the other subscription reviews diff/tests and records findings; it does not rewrite the same task from scratch.
- **Queen:** resolves conflicts, integrates, and reports the delivered result.

## Commands

```bash
# Reconcile local + origin/main peer truth
python scripts/fleet_bus.py status --fetch

# Honest CLI inventory (declared auth only)
python scripts/cli_capacity.py --machine c940

# Live one-turn capacity proof (does consume subscription capacity)
python scripts/cli_capacity.py --machine c940 --live --codex-model gpt-5.6-terra

# Version-2 manifest only; validates resource/auth/worktree gates
python -m fleet.night_runner fleet/night/YYYY-MM-DD.json
python -m fleet.night_runner fleet/night/YYYY-MM-DD.json --execute

# Full control-plane tests
python -m unittest discover -s tests -p 'test_*.py' -v
```

Run the same capacity command on YogaBook with `--machine yoga-book`, commit only the redacted JSON report/receipt, and never commit credentials or raw auth output.

## Scoreboard

Track weekly:

| Metric | Target |
|---|---:|
| Verified/delivered outcomes | rising week over week |
| Queued -> PR cycle time | < 1 working day for bounded work |
| PRs with zero-exit acceptance evidence | 100% |
| Orphan agent processes | 0 |
| Report-only false completions | 0 |
| Duplicate owners on same branch/worktree | 0 |
| Fresh peer heartbeats | < 24 h |

Tokens used are diagnostic capacity, not the success KPI.
