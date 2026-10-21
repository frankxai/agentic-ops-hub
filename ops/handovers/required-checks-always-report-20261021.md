---
id: required-checks-always-report-20261021
what: Land frankx.ai-vercel-website PR 1083 so Merge Gate and Contract Guard report on every pull request, then unblock PR 1029
where: https://github.com/frankxai/frankx.ai-vercel-website/pull/1083
owner: unclaimed (author harness claude; the checker must be another harness)
status: open
note: draft, not merged; needs ready, a non-Claude sign-off on the exact head, then update-branch on PR 1029
evidence: https://github.com/frankxai/frankx.ai-vercel-website/pull/1083
updated: 2026-10-21
---

## Prompt

Finish frankxai/frankx.ai-vercel-website PR 1083 (branch `agent/claude/required-checks-always-report`, draft).

The problem: Merge Gate and Contract Guard are required checks and had a `pull_request` `paths:` filter, so a pull request touching only unlisted files never got a result and could not merge. PR 1029 (`.nvmrc` only) is the live case. The filter had been patched seven times.

What the PR does: removes both filters, pins both trigger blocks and job names in `scripts/tests/required-checks-always-report-contract.test.mjs`, registers that test in `test:build-integrity`. It does not add a detect step; the reasons are in the PR body (fails open, and one of the last 120 pull requests missed the old filter).

To finish:

1. Mark the PR ready (`gh pr ready 1083`). Heavy CI fires on ready; the repo is over its 10-PR budget, so do not open other PRs for this.
2. A different harness than Claude reviews the exact head and signs off through `node tools/pr-gate.mjs signoff` (head moves after the Codex fix commit `1d30bca`; a sign-off binds to the SHA it read).
3. Merge through `node tools/pr-gate.mjs merge`. Do not use `--admin`; do not edit branch protection.
4. Update-branch PR 1029 (it is `BEHIND`, and `strict` is on) and confirm Merge Gate and Contract Guard now appear on it. That is the live proof; the dry runs in the PR body are the only proof so far.

Decide separately (Frank): CODEOWNERS on `.github/workflows/**` (0 required approvals today, so a pull request can edit and approve itself); the design-contract retarget gap (needs a rule change in starlight-design-intelligence); the Review Gate status on fork pull requests (unverified); and estate guidance that recommends `[skip ci]` for docs-only commits, which leaves every required `pull_request` check unreported on a PR head.
