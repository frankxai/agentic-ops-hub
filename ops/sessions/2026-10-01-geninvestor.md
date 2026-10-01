# 2026-10-01 — GenInvestor open-source build and cloud handover

Claude (Sonnet 5.5), YogaBook. Two days of work turned the investor tooling into an open-source product with a movement around it. Nothing is merged. No independent review has run.

## Repos

| Role | Repo | State |
| :--- | :--- | :--- |
| Product (public) | `frankxai/GenInvestor` | [PR 1](https://github.com/frankxai/GenInvestor/pull/1) draft, `agent/claude/initial-import`, head `f34ffd5`. CI green on Node 22.18 and 24 across Linux, macOS, Windows. |
| Skills (public) | `frankxai/geninvestor-skills` | [PR 1](https://github.com/frankxai/geninvestor-skills/pull/1) draft, head `22c53d9`. Four skills and a validator. |
| Catalogue (public) | `frankxai/awesome-investor-agent-skills` | [PR 8](https://github.com/frankxai/awesome-investor-agent-skills/pull/8) draft, weekly harvester. Its main checkout belongs to another agent. |
| Incubator (private) | `frankxai/starlight-investor-portal` | [PR 1](https://github.com/frankxai/starlight-investor-portal/pull/1) draft, branch `worktree-agent-claude-geninvestor-evals`, head `dccf345`. Source of truth, plans, export tool. |
| Estate | `frankxai/starlight-estate` | Issues #9 and #10. |

Trackers in the incubator: product epic #30 (#7 to #29), movement epic #40 (#31 to #39). The build brief for the next agent is `docs/geninvestor/CLOUD-AGENT-BRIEF.md` on the incubator branch.

## Decisions

- Name is GenInvestor. Apache-2.0. Open source, local-first, no hosted service. No new brand; Assaybook is a reserve name only. "Starlight Investor" was rejected as a platform name (collides with Starlight Investments, Canada's largest landlord).
- Do not sell the software. Sell learning later, gated by the waitlist trigger and counsel. Tool-only affiliates, no broker referrals.
- Publishing only through `tools/export-public.mjs`. Public commits use the noreply identity.

## Built and verified

Evidence ledger, claims audit, workflow graph, ECB provider (live), daily brief, mandate, SEC opportunity scout with rule-based skeptic, calibration ledger, masking, CLI, 7-tool read-only MCP server, Python simulation engine. 148 TypeScript tests (2 opt-in live skips) and 90 Python tests. Planted-error corpus in CI: 124/124 numbers, 85/85 links, 6/6 sources, 39/39 citations, 8/8 quotes, zero false alarms. Building it exposed two audit holes; both fixed.

## Not done, plainly

- SEC live path unverified: one HTTP 403 on the first request, not retried. Needs the user's own contact identity.
- No cross-provider review: `pp preflight --workload build` was HOLD all session (RAM 1.4 to 2.9 GB against 8 GB), so no Grok gate and no Next.js build.
- No model-written analyst or skeptic, no Form 4 or 13F, no price data, no dashboard.
- On 2026-10-01 the auto-mode classifier denied `gh api` and `gh pr checks` calls for the repo Actions setting and PR status. Not retried.

## Mistakes disclosed

Overwrote a `.gitignore` without reading it (caught in the diff, restored). Tried to put Frank's personal email in an SEC User-Agent; it failed locally on formatting and nothing was sent. Claimed the GenInvestor repo was empty and that no deployment existed; both wrong (one initial commit; `geninvestor-research.vercel.app` is live). A research agent's claim that ai-hedge-fund anonymises tickers was false.

## Frank-owned

Merge the three public PRs after review. Enable "Allow GitHub Actions to create pull requests" on the awesome repo. Supply an SEC contact for the live run. TRUTH section 2 ruling on live group sessions. Vercel site ownership (#38). Counsel brief (#25). Trademark search before commercial use. TradingView sign-in.

## Location of this file

Branch `agent/claude/geninvestor-handover` from `origin/main` `065456a`, worktree `agentic-ops-hub/.worktrees/claude-geninvestor-handover`. The primary hub checkout stays on `agent/hermes/fleet-task-contract-v1`.
