# Objective Retrofit Independent Verification — HOLD

**Date:** 2026-07-17
**Objective:** `OBJ-FLEET-DELIVERY`
**Mission:** `retrofit-verifier`
**Branch:** `agent/hermes/objective-campaign-v2-20260717`
**Reviewed commit:** `19873b33b8648c79f5476cd1aa6eae75b05ba745`
**Verdict:** **HOLD — deterministic gates pass, but the required independent model review did not complete.**

## Verifier execution evidence

The campaign correctly excluded the Codex maker and routed the verifier away from depleted pools:

- Claude was last observed at 9% session remaining, below the 15% floor.
- Codex was healthy at 70%, but remained excluded because Codex produced the maker artifact.
- Grok Build was at 2%, below the 10% floor.
- OpenCode had no admitted credential route; bounded V0 smoke attempts returned `Not Found`.
- AGY passed the planner's `PONG` health probe and was admitted as the unmeasured fallback.

AGY run `20260717T173751Z` exited `1` without producing a report or receipt. Its log ended with `Error: timeout waiting for response`; the runner recorded `receipt_status: missing-receipt`. No AGY PASS is claimed.

## Concrete repair shipped

The failed run exposed a launcher mismatch: the mission allowed 60 minutes, while `agy -p` retained AGY's five-minute print default. Commit `19873b33b8648c79f5476cd1aa6eae75b05ba745` now:

1. passes `--print-timeout 60m0s` from the mission timeout;
2. injects the Windows Phone Link search ban into every generated task contract;
3. injects the storage gate forbidding clones, worktrees, bulk installs, and media generation;
4. adds a regression test for the timeout and safety contract.

The repaired dry-run returned `ready: true`, active wave `2`, AGY `would-launch`, timeout `60m0s`, and both safety gates present. The verifier was not retried again in this wave after the failed AGY run and failed OpenCode smoke; that preserves the one-retry/fallback stop rule.

## Deterministic verification

| ID | Command | Exit | Result |
|---|---|---:|---|
| full-unit-suite | `python -m unittest discover -s tests -p 'test_*.py' -v` | 0 | 39 tests passed |
| json-contracts | `python -m json.tool objectives-registry.json && python -m json.tool fleet/campaigns/2026-07-17-objective-retrofit.json` | 0 | Passed |
| campaign-validate | `python -m fleet.token_planner validate fleet/campaigns/2026-07-17-objective-retrofit.json` | 0 | Valid campaign, 2 missions, 1 objective |
| diff-check | `git diff --check` | 0 | Passed |
| cloud-ci | GitHub Actions `verify` on PR #22 | 0 | Passed |

These checks establish deterministic correctness only. They do **not** substitute for the required independent code-review verdict.

## Integration state

Draft PR: https://github.com/frankxai/agentic-ops-hub/pull/22
Head: `19873b33b8648c79f5476cd1aa6eae75b05ba745`
GitHub state at receipt: `MERGEABLE` / `CLEAN`; `verify` and CodeRabbit status green; PR remains draft.

## Next bounded handoff

After a distinct verifier route is above its quota floor or AGY reliability is restored, run exactly one read-only independent review against commit `19873b33b8648c79f5476cd1aa6eae75b05ba745`, record the three declared verification IDs, and replace this HOLD receipt only if that review genuinely passes. Do not merge while the independent gate is missing.
