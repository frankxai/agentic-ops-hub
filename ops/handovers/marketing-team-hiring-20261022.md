---
id: marketing-team-hiring-20261022
what: Marketing team: land the review-passed PRs, get PR 73's signup link merged, run hire 2 (AI visibility baseline)
where: prompt below
owner: claude
status: open
note: plan page https://claude.ai/artifact/GyC5jHyRJG5Yec6Fjsp2cP; team brain is local-only at starlight/scratch/marketing-brain/.marketing/ until Frank picks a private repo
updated: 2026-10-22
---

## Prompt

Continue the marketing team built on 2026-10-22 (session log `ops/sessions/2026-10-22.md`). Read the plan page first: https://claude.ai/artifact/GyC5jHyRJG5Yec6Fjsp2cP.

1. Get the skills-library signup link live. frankxai/claude-skills-library#73 was blocked by Codex (comment 6347490124): the README promises a price question the frankx.ai `/waitlist` page does not ask (`askDemand` defaults to false). Apply the copy fix in that comment on the PR's own worktree (`starlight/worktrees/csl-capture-cta`, check no other session is writing there first), then get a fresh Codex review. Codex must post the sign-off itself; its workspace-write sandbox could not read the gh config, so give it a sandbox that can, or run `pr-gate.mjs signoff` from a Codex session that has gh.
2. Different-provider review and sign-off, then merge in order: Starlight-Intelligence/marketing-intelligence #3 (skills), #4 (team plugin v0.2 plus eval cases, head c7a69a1), #5 (skills wave 2). #3 and #4 share an identical AGENTS.md. Merging is first publication of the public pack: Frank's call. Licence for the repo is open (Frank).
3. Agent cards: frankxai/starlight-agent-army-architecture#5 merges after codex PR #4 there (the schema and `cards/` exist only on #4). Registry: branch `agent/claude/marketing-team-registry` in frankxai/agentic-ops is pushed without a PR (over budget); fold it into an open registry PR or open one when under budget.
4. Hire 2, ai-visibility: build a 10-question panel from real buyer language for the skills library and Kernel, run 2 assistants x 3 runs, log rows to `.marketing/memory/ai-visibility.jsonl`, summarise with `visibility.mjs`. One Codex or other CLI process at a time; RAM was under 1 GB on 2026-10-22.
5. Readout 2026-W44 (hire 1): same sources as the W43 baseline plus Vercel Web Analytics (enabled by Frank on 2026-10-22 for frankx-ai-vercel-website and starlightintelligence-ai; it still returned "not found" an hour later, likely until the next deploy) and waitlist sign-ups if PR 73 is live.
6. The three LinkedIn drafts (hire 4) are on hold until each has a result to show; Codex critique on file. Frank posts; nothing is scheduled.

Blockers that are Frank's: waitlist store env (`KV_REST_API_URL`, `KV_REST_API_TOKEN`, `RESEND_API_KEY`, `RESEND_AUDIENCE_ID`), a private home for the team brain, first publication of the marketing-intelligence PRs, repo licence, and the Marketing Agent Benchmark decision.
