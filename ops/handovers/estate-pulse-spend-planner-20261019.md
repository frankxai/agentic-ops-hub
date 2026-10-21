---
id: estate-pulse-spend-planner-20261019
what: Land the estate pulse, spend planner, starlight extension dispatch and frankx.ai analytics fix
where: prompt below
owner: claude
status: open
note: focus window to 20 Nov: only item 1 (frankx.ai-vercel-website#1068, a bug fix in a spine repository) may proceed, and only as preparation until the drain reaches step 3 of ops/plans/estate-convergence-2026-10-21.md, when it may merge; items 2-5 are outside the spine or a feature in a hold repository; five PRs in review on 2026-10-19; two need gates only Frank's seats can satisfy
evidence: https://github.com/frankxai/frankx.ai-vercel-website/pull/1068
updated: 2026-10-21
---

## Prompt

Continue the 2026-10-18/19 estate-pulse slice. Read each PR's latest pr-gate comment and checks before acting.

1. frankx.ai-vercel-website#1068: beforeSend sent bare paths since 2026-07-11, so Vercel Web Analytics recorded zero pageviews for frankx.ai. Prepare it now; once the drain reaches step 3 of `ops/plans/estate-convergence-2026-10-21.md`, after a different-harness PASS and green checks, merge with `node tools/pr-gate.mjs merge --squash`, then confirm `vercel api /v1/query/web-analytics/visits/count` for the frankx.ai project turns non-zero within a day.
2. Starlight-Intelligence/starlight-token-tracker#21: npm package `@starlight-intelligence/token-tracker` with `starlight-spend` and `starlight-plan` (money in integer cents, decimal strings). Merge after review. It complements open #7, #8 and #20 from other harnesses; do not overwrite their files. Follow-up: add a release workflow copied from SIS `npm-ecosystem-release.yml` (main-only dispatch, verify job, `npm-production` environment, OIDC). Publishing stays the owner's decision; the first publish is manual.
3. frankxai/Starlight-Intelligence-System#462: `starlight <name>` runs an installed `starlight-<name>` command (Windows .cmd shims resolved to their script, no shell). SIS requires a `STARLIGHT-INDEPENDENT-REVIEW-V1` receipt posted through the Codex or Cursor GitHub App, plus a CTO pass because `.github/` changed. Codex was asked on the PR. Grok signoffs do not satisfy this repository.
4. frankxai/agentic-ops#283: Registry records the token tracker as owner of `artifact_agent_spend_planner` and registers starlight-command-center. `validate_registry.py` passes locally; hosted checks did not start (zero steps, consistent with the private Actions budget).
5. Starlight-Intelligence/starlight-command-center#81: `pnpm collect-pulse` (GitHub, npm, skills.sh, machine rows under `~/.starlight/pulse/latest`).

Local, not in any repo yet: the terminal pulse release `~/.starlight/startup/releases/terminal-pulse-20261018` (reach, tokens-first money panel, spend view, deploys, `pulse spend set|topup`). Its owner is unregistered; propose a Registry placement before moving it.

Lessons: read the agentic-ops Registry before placing a new tool (SIS is substrate, not product runtime); SIS `package.json` is Foundry-locked, so use dedicated workflows; pnpm 11 needs `allowBuilds` for esbuild.
