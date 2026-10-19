---
id: si-lab-front-door-20261019
what: starlightintelligence.ai as the lab's front door: Kernel waitlist, sourced landscape, lab notes, discovery JSON
where: frankxai/starlightintelligence.ai PR 172 (agent/claude/si-lab-front-door), worktree C:/Users/frank/starlight/worktrees/starlightintelligence-lab-front-door
owner: Claude (maker); Codex or Grok (checker); Frank (surface-approved label, kv-env click)
status: open
evidence: https://github.com/frankxai/starlightintelligence.ai/pull/172
updated: 2026-10-19
---

## Prompt

Continue the starlightintelligence.ai front door from 19 October. Read PR 172 and its comments first, then
this file. Week 43 plan Track 3 (C:/Users/frank/.claude/plans/god-mode-on-plan-bubbly-otter.md).

State on 19 October, 14:30 local:

- PR 172 is a draft at `eb9b6e4`: the build (`39492f5`), a second pass answering a Codex (OpenAI) code review
  and an Antigravity (Google) buyer critique (`015ed5a`), and two small fixes from Codex re-reviews (`cc1c3bc`,
  `eb9b6e4`). Codex passed every head it reviewed (verdicts relayed on the PR). The Vercel previews built green,
  including the homepage browser gate (7/7 checks) that `vercel.json` runs on every build.
- On the preview: `/waitlist` 200 with the standard capture (`productId: starlight-kernel`, priceBand and
  the step-two questions); `/.well-known/starlight.json` 200 (`starlight.discovery.v1`, `installable: false`);
  the landscape renders server-side with eight sourced rows; `/api/v1/landscape` 200.
- Craft receipt validates: `queen/reports/craft/starlightintelligence-2026-10-19.md` in the estate root
  (`node tools/craft-receipt.mjs --product starlight-kernel --receipt ...`), with both critiques beside it.
- The Kernel is blessed (Decision Desk ruling `freeze-exceptions`) but private, `"private": true` and
  UNLICENSED, so the primary CTA is its waitlist, not an install.
- `main` has not deployed to production all day: every build fails `image-inventory --check` because evidence
  PNGs under `docs/commons/releases/2026-10-12/` were merged without regenerating `design/image-manifest.json`.
  PR 172 regenerates it.

Next, in order:

1. Frank: add the `surface-approved` label to PR 172 (`/waitlist` is a first-time publication), and do the
   one-time click `kv-env` (production `/api/waitlist` answers `open: false` until KV env exists).
2. A non-Claude harness reviews the exact head and signs off:
   `node tools/pr-gate.mjs signoff --repo frankxai/starlightintelligence.ai --pr 172 --harness codex --verdict pass`,
   then `gh pr ready 172` and `node tools/pr-gate.mjs merge --repo frankxai/starlightintelligence.ai --pr 172 --squash`
   only after the label. Any new commit voids the sign-off.
3. If the label waits, unblock production separately: one PR on `main` that only runs
   `node scripts/image-inventory.mjs --write`; it will conflict with PR 172 on that one file, so regenerate again after.
4. Estate root (on Grok's `agent/grok/jev-fail-closed`, never pushed): `graph/products.graph.json` holds two
   uncommitted edits from this lane: the new `starlight-kernel` row and a corrected `starlight-knowledge-tree`
   gate (its "G1 PASS 2026-09-09" has no receipt). The root's owner commits them; the receipt files too.
5. Weekly: after the intel feed refreshes, `pnpm sync:lab-feed` in the repo and replace `data/lab-notes.v1.json`
   with the new week (at least one first-party note). Re-read every figure from its source.

Follow-ups noticed, not done here:

- The feed has no Cloudflare or Supabase source, so the "long-lived agents" and "data" rows show no signals.
  Add them to the intel feed sources.
- `/build-challenge`, `/founders`, `/teams` and `/community` still use `mailto:` as their CTA (bespoke capture
  under AGENTS.md §5c.3).
- `pnpm lint` on `main` fails on pre-existing warnings in `app/missions/artifact-review-workbench.tsx`.
- `tools/verify-lane.mjs` blocks on its own caller's lane: it re-detects a different session id per process.
- The INTEL-BRIEF cites an Arena round 6 receipt (`2026-10-14-r6-gemini-4-argon-proving-ground.json`) that is
  not on disk; the page does not repeat its claims.
- The Kernel worktree (`starlight-kernel/.claude/worktrees/agent+claude+kernel-slice`) has empty junk files from
  the Edit hook (names like `const`, `try`, `prompt`).

Do not promote to production without the label, and do not push the estate root.
