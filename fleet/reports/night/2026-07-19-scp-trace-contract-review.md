# SCP trace-contract overnight branch review

**Date:** 2026-07-19
**Verdict:** **blocked**
**Requested branch:** `agent/c940/ai-trace-contract` in `frankxai/starlight-memory`
**Review baseline:** `origin/main` = `fd6b2373a1a167be7faecee59e423683b99a992e`

## Result

The requested remote branch was not present after a pruned fetch. Consequently, there is no reviewed commit, no branch diff against `origin/main`, and no honest basis to approve or request code changes. This report deliberately does not infer an implementation from the dirty primary `C:/Users/frank/starlight-memory` checkout.

A clean detached review worktree was created at `C:/Users/frank/.worktrees/starlight-memory-ai-trace-review` at the baseline SHA above. It is detached and clean; no files were modified in the source checkout or review worktree.

## Exact commands and results

| Command | Result |
|---|---|
| `git -C C:/Users/frank/starlight-memory fetch origin --prune` | Completed successfully. |
| `git -C C:/Users/frank/starlight-memory rev-parse origin/main` | `fd6b2373a1a167be7faecee59e423683b99a992e` |
| `git -C C:/Users/frank/starlight-memory rev-parse --verify refs/remotes/origin/agent/c940/ai-trace-contract` | Failed with `fatal: Needed a single revision` (exit 128): remote-tracking branch is absent. |
| `git -C C:/Users/frank/starlight-memory branch -a \| grep -F ai-trace-contract` | No matching local or remote ref. |
| `git -C C:/Users/frank/starlight-memory worktree add --detach C:/Users/frank/.worktrees/starlight-memory-ai-trace-review origin/main` | Created clean detached worktree at `fd6b2373a1a167be7faecee59e423683b99a992e`. |
| `git -C C:/Users/frank/.worktrees/starlight-memory-ai-trace-review status --short` | No output (clean). |
| `git -C C:/Users/frank/.worktrees/starlight-memory-ai-trace-review branch --show-current` | No output (detached HEAD). |
| Branch-focused tests, `npm run verify`, package export/build checks, and branch `git diff --check` | Not run: there is no target commit/diff to test or inspect. Running baseline-only checks would not establish branch correctness or distinguish regressions. |

The primary `C:/Users/frank/starlight-memory` checkout was already dirty when inspected (`package.json`, `package-lock.json`, `src/index.ts`, `src/mem0-remote-provider.ts`, plus untracked local-core/cache/test files). It was never used for test execution, staging, or modification.

## Required invariant review

Not assessable without the requested branch diff:

- `local_core` / SIS first-write canonical authority;
- non-export of `secret` and default `regulated` traces;
- explicit, testable export policy;
- absence of raw prompt/payload persistence and implicit provider-network dependencies;
- no per-agent runtime addition; and
- coherent public package exports.

## Critical findings, ranked

1. **P0 — review input unavailable:** `origin/agent/c940/ai-trace-contract` does not exist after `fetch --prune`. There is no commit beyond `origin/main` to inspect, test, or integrate.
2. **P1 — source checkout is dirty:** reviewing that checkout would mix uncommitted work with the requested overnight result and could falsely attribute changes. The detached baseline worktree prevents that contamination.

No code-level security or logic finding is claimed because no target branch content was available.

## Integration recommendation

**Do not merge or integrate anything.** The branch owner should push `agent/c940/ai-trace-contract` to `origin` with at least one commit beyond `origin/main`. Re-run this review from the detached worktree after the ref is visible; only then run the focused trace-contract tests, `npm run verify`, `git diff --check`, and package export/build checks with a baseline comparison.
