---
id: build-fix-loop-20261020
what: Get a non-Claude sign-off on starlight-agent-config PR 133, merge it, install the skill and prove the unproven harnesses
where: frankxai/starlight-agent-config PR 133 (branch agent/claude/build-fix-loop, head 0559aa8)
owner: unclaimed (checker must not be Claude)
status: open
updated: 2026-10-20
---

Author: Claude (Opus 5.5), 20 October 2026. Review state: Codex read-only review PASS at 0559aa8.

## What shipped

A Starlight equivalent of Claude Code's "write tests, run them, fix the failures" loop that any harness
can run through one driver. Draft PR: https://github.com/frankxai/starlight-agent-config/pull/133

- `core/tools/starlight_fix.py`: the bounded test-run-fix driver, with a run ledger under
  `~/.starlight/fix-runs` and a guard that flags tests weakened to go green.
- `core/skills/starlight-build-fix/SKILL.md`: the skill, with a per-harness one-shot table.
- `/starlight-fix` command, and `docs/claude-code-parity.md`.
- `installers/install.ps1` and `starlight-agent-config.json` register the skill (9 files, +1,716 / -6).

The PR was opened over the repo's 10-PR budget with Frank's approval.

## Verified state at 0559aa8

- Codex (`codex --profile review`, read-only) returned PASS after seven review rounds. The last fix
  made Go require per-test evidence rather than a package `ok` line.
- Locally: 61 driver tests and 14 census tests pass.
- CI has not run. All four checks (`release-control`, `evaluate`, `PowerShell regression and contracts`,
  `windows-hook-security`) report failure after 1-3 s with 0 steps; the annotation reads "The job was
  not started because an Actions budget is preventing further use". The repo is private under the
  personal account, which is the known Actions budget block, so these are not test failures.
- No different-provider sign-off is recorded through `tools/pr-gate.mjs` yet. The Codex PASS was a
  review, not a gate signoff bound to the SHA.
- Harness proof, from the skill's table: Codex proven (wrote 14 tests; ledger and guard worked).
  Grok, Gemini CLI and OpenCode are unproven. Grok in `plan` and `dontAsk` modes stopped after one
  message with no tool calls.

## Product issue

PR 133 has no product issue and links none. The slice is still open, so the estate rule says open
one in `frankxai/starlight-agent-config` before or at merge; this handover did not open it.

## Found in passing

- `core/skills/bless` tests fail on this machine. They create throwaway git repos and commit inside
  them, and the global starlight-ops commit hook blocks those commits. Fix candidates: run the test
  repos with `core.hooksPath` pointed at an empty dir, or teach the hook to skip temp directories.
  Not touched in PR 133.
- `tools/lane.mjs` (estate root) reports two sibling files in one folder as overlapping, so two lanes
  that each claim one file in the same directory collide (exit 3). Cause not yet traced in the glob
  matcher; until fixed, a harness hitting this needs `--force` after checking the other lane.

## Prompt

You pick up the Starlight build-fix loop, frankxai/starlight-agent-config PR 133 (draft, branch
`agent/claude/build-fix-loop`, last reviewed head 0559aa8). Claude wrote it, so the checker must be
another provider. Work from `C:\Users\frank\starlight\worktrees\starlight-agent-config-build-fix` or a
fresh worktree; never commit on the author's branch from another harness.

1. Confirm the head is still 0559aa8 (`gh pr view 133 --repo frankxai/starlight-agent-config --json headRefOid`).
   If it moved, review the new commits first.
2. Run the tests locally: the driver suite (61) and census suite (14). CI cannot start on this private
   repo while the Actions budget is exhausted; say so in the signoff rather than calling CI green.
3. From `C:\Users\frank\starlight`, gate it with a non-Claude harness:
   `node tools/pr-gate.mjs verify --repo frankxai/starlight-agent-config --pr 133`, then
   `node tools/pr-gate.mjs signoff --repo frankxai/starlight-agent-config --pr 133 --harness <codex|grok|gemini> --verdict pass`.
   Mark the PR ready with `gh pr ready 133 --repo frankxai/starlight-agent-config`. That repo needs one
   approving review with no admin bypass, so the merge itself waits for Frank.
4. Before merge, open the product issue for the slice in starlight-agent-config and link it from the PR.
5. After merge, run `installers/install.ps1` from the merged checkout. Check the skill resolves under
   `~/.claude`, `~/.codex` and `~/.grok`.
6. Prove the three unproven one-shots from the SKILL.md table on a small throwaway module, each in its
   own worktree:
   - Grok: `grok -p "Use the starlight-build-fix skill: ..." --permission-mode acceptEdits`
   - Gemini CLI: `gemini -p "Use the starlight-build-fix skill: ..." --approval-mode auto_edit`
   - OpenCode: `opencode run "Use the starlight-build-fix skill: ..."`
   A harness counts as proven only when its run writes a ledger entry under `~/.starlight/fix-runs`
   and the guard ran. Update the table's "State" column in a follow-up PR with the evidence paths.
7. Close this handover: `node scripts/handover.mjs process build-fix-loop-20261020 --evidence <merged PR URL>`.

Done means PR 133 merged with a non-Claude signoff, the skill installed in three harness homes, and
each of Grok, Gemini CLI and OpenCode marked proven or failed with its evidence.
