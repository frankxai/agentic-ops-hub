# L1 — GitHub estate health (frankxai), 2026-09-15

Lane L1, read-only. Every value below came from `gh repo view`, `gh run list`, `gh pr list`, `gh api .../protection`, `.../rulesets`, `.../dependabot/alerts` and `.../actions/workflows`, run on 2026-09-15 (around 18:30 UTC). Raw JSON is in `./raw/`.

## How the names resolved

| Asked for | Resolved to | Evidence |
|---|---|---|
| Arcanea | `frankxai/arcanea-ai-app`, which is the remote of the local `~/Arcanea` and deploys arcanea.ai. `frankxai/arcanea` (the public OSS repo) is also covered below. | `git remote get-url origin` in `~/Arcanea` |
| frankx-prod-sync | **Not a GitHub repo.** It is a local clone whose origin is `frankxai/frankx.ai-vercel-website`, so it is covered by that row. | GraphQL "Could not resolve"; search returned nothing; local `git remote` |
| AnimeLegends.ai | `frankxai/AnimeLegends` | `gh search repos` |
| vibeclubs.ai | `frankxai/vibeclubs` | `gh search repos` |

## Health table

Legend:
- **CI (main)**: result of the latest non-Dependabot run on `main`. Red means the latest run failed.
- **Protection**: classic branch protection. `checks` = required status checks, `rev` = required approvals, `adm` = enforce_admins.
- **PRs**: open / conflicting / with failing checks (draft PRs are counted), plus the oldest PR's age.
- **Dependabot**: open alerts. "disabled" means the API returned 403 "Dependabot alerts are disabled".

| Repo | Vis | Pushed | CI (main) | Workflows | Protection / rulesets | PRs open/conf/fail (oldest) | Dependabot |
|---|---|---|---|---|---|---|---|
| FrankX | private | 09-15 | GREEN: CI + Tracked secret guard push 09-11 pass. Last Dependabot run (toml, 09-04) failed. | 14 | protected; checks none, rev 0, adm on; ruleset Copilot | 19 / 2 / 0 (#54, 97d) | **39** (2 crit, 23 high, 12 med, 2 low) |
| frankx.ai-vercel-website (+ frankx-prod-sync) | public | 09-15 | AMBER: push CI green 09-15 03:03. **intelligence-refresh failed 4 runs in a row (08-31 → 09-15)** | 19 | protected; checks CI, Contract Guard, Media Guard, Merge Gate, design-contract, Vercel; strict; rev 0; adm on | 9 / 1 / 1 (#650, 11d) | **14** (4 high, 8 med, 2 low) |
| arcanea-ai-app (arcanea.ai prod) | private | 09-15 | GREEN: CI, CodeQL, World access policy pass 09-15 15:41 | 33 | protected; checks Build, Lint, TypeScript, CI Status; rev 0; **adm off**; 2 rulesets **disabled** | **31 / 9 / 8** (#231, 43d) | disabled |
| arcanea (OSS) | public | 09-14 | GREEN: Quality Gate + Secret literal guard 09-14 | 20 | protected; **no required checks, no PR rule**; adm on; ruleset "x" active | 11 / 4 / 7 (#75, 86d) | disabled |
| arcanea-platform | private | 09-04 | **RED**: every push workflow failed on 03-01 (Quality Gate, Deploy, MVP CI/CD, Test Suite). Cross-Repository Synchronization failed daily until its last run on 08-20. | 9 (all active, including Deploy and Publish Packages) | **NONE** (404, no rulesets) | 1 / 0 / 0 (#32, 11d) | disabled |
| gencreator.ai | private | 09-15 | GREEN: CI 09-15 15:31 | 6 | protected; checks CI Status; rev 0; **adm off**; ruleset Copilot | 3 / 0 / **3** (#69, 1d) | disabled |
| AnimeLegends | private | 09-15 | GREEN: CI 09-15 00:28 | 8 | protected; no required checks; rev 0; adm off | 2 / 0 (1 UNKNOWN) / 0 (#16, 3d) | disabled |
| vibeclubs | public | 09-15 | GREEN: CI + Voice audit 09-13 | 8 | protected; **no checks, no PR rule**; adm off | 4 / 1 / 2 (#9, 18d) | disabled |
| Starlight-Intelligence-System | public | 09-15 | GREEN: Harness check, Loop kernel, Capability Foundry 09-14/15 | 21 | protected; **no checks, no PR rule**; adm off; ruleset Copilot | 5 / 3 / 0 (#132, 11d) | disabled |
| library-os | public | 09-02 | **NO CI**: the only workflow is Copilot (dynamic); no runs on main | 1 | protected; no checks, no PR rule | 0 | disabled |
| agentic-creator-os | public | 09-14 | AMBER: Health Check green 09-15. **Ecosystem Monitor failed 4 weekly runs in a row (08-24 → 09-14).** | 12 | protected; no checks; rev 0; adm on; ruleset Copilot | 5 / **4** / 1 (#32, 65d) | disabled |
| agentic-ops-hub | public | 09-15 | **RED**: Fleet watch failed on all of the last 100 runs (back to at least 08-22) and none of the last 400 succeeded. Push CI green 08-25. | 4 | protected; rev 1; adm on | 8 / 1 / 1 (#48, 28d) | disabled |
| starlight-token-tracker | private | 09-15 | GREEN: CI 09-15 13:50 | 1 | **NONE** | 0 | disabled |
| starlight-memory | public | 09-09 | GREEN: CI 09-08 | 2 | **NONE** (Copilot ruleset only) | 3 / 1 / 0 (#10, 49d) | disabled |
| agentic-life-os | private | 09-11 | GREEN: Public runtime verification 09-09 | 2 | **NONE** | 4 / 3 / 0 (#1, 85d) | disabled |
| claude-code-config | private | 09-15 | **NO CI**: Copilot workflow only | 1 | **NONE** (Copilot ruleset only) | 1 / 0 / 0 (#7, 6d) | disabled |

None of these repos is archived. Default branch is `main` for all of them.

**Totals:**
- Red default branches: 3 (arcanea-platform, agentic-ops-hub, frankx.ai-vercel-website).
- Scheduled workflows failing for 4 weeks while push CI stays green: 2 (vercel-website, ACOS).
- No CI at all: 2 (library-os, claude-code-config).
- Open PRs: 106. Conflicting: 29. With failing checks: 23.
- Dependabot alerts are disabled on 14 of 16 repos.

## Key failure evidence

- **frankx.ai-vercel-website, intelligence-refresh** (run 34989235329): the "Open snapshot PR" step fails with `##[error]GitHub Actions is not permitted to create or approve pull requests.` This has a knock-on effect. The required **Merge Gate** check on PR #702 (run 34988776301) fails with `snapshot-stale: data/intelligence/external.json was generated 15 days ago (limit 14)`. Any PR that runs that Merge Gate step will now fail a required check.
- **agentic-creator-os, Ecosystem Monitor** (run 34822849888) fails the same way: `pull request create failed: GitHub Actions is not permitted to create or approve pull requests`.
- **agentic-ops-hub, Fleet watch** (run 35007919885) reports:
  - c940 heartbeat stale since 2026-08-25
  - yoga-book heartbeat stale since 2026-08-16
  - OPS-LEDGER last sweep 2026-08-10
  - to-book queue item BOOK-HEARTBEAT-20260825 has an expired TTL
- **FrankX critical alerts**: #224 vitest (`packages/euipo-mcp/package.json`) and #7 vitest (`agentic-creator-os-npm/package-lock.json`), both from 2026-08-04.
- **Vercel-site high alerts**: #148 and #128 extract-zip; #143 and #142 toml.

## Top 10 fixes (ranked by production risk)

| # | Repo | Evidence | Risk | Proposed action | Agent can do it alone? |
|---|---|---|---|---|---|
| 1 | frankx.ai-vercel-website | intelligence-refresh failed 4 weeks running (run 34989235329, "Actions not permitted to create PRs"). Merge Gate on PR #702 fails because the snapshot is stale (run 34988776301). Snapshot PR #708 is open. | **prod** (required check blocks PRs to the frankx.ai prod repo) | Short term: merge #708 to refresh `external.json`. Durable fix: let the workflow open PRs, either by turning on "Allow GitHub Actions to create and approve pull requests" or by giving it a GitHub App / PAT token. | **Needs Frank**: merge to prod, plus a settings or credential change |
| 2 | FrankX | 39 open alerts: 2 critical (vitest #224, #7) and 23 high. Deps PR #151 is a draft with conflicts; Dependabot PR #173 has conflicts. | security | Rebase or regenerate the deps PR to clear the critical and high alerts. Close stale Dependabot PRs once superseded. | Yes, to prepare the PR. Merge and close need Frank. |
| 3 | frankx.ai-vercel-website | 14 alerts, 4 high (extract-zip #148/#128, toml #143/#142). Dependabot update run 34900733234 failed. | security (public prod repo) | Open a PR with the bumps or overrides and let the required checks run. | Yes (PR). Merge needs Frank (prod deploy). |
| 4 | Estate (14 repos, including prod arcanea-ai-app and gencreator.ai) | `dependabot/alerts` returns 403 "disabled" | security | Turn on Dependabot alerts and security updates for Tier 1 and 2 repos. | **Needs Frank** (settings; low risk, reversible) |
| 5 | arcanea-ai-app (arcanea.ai) | 31 open PRs: 9 conflicting, 8 with failing checks. Security-relevant drafts have conflicts: #409 (customer API keys across providers) and #333 (Supabase binding hardening). enforce_admins is off and both rulesets are disabled. | prod + security | Triage: rebase #409 and #333 first, then close superseded PRs. Consider turning enforce_admins on. | Rebasing and fixing CI on branches: yes. Merges, closes and settings: needs Frank. |
| 6 | arcanea-platform | No protection and no rulesets. Every push workflow failed on 2026-03-01 (runs 22554055424 and others). Cross-repo sync failed daily until 08-20. Deploy and Publish Packages workflows are still active. | prod/security hygiene (unguarded deploy/publish path) | Decide whether to archive the repo or restore it. At minimum, disable the deploy and publish workflows and add protection. | **Needs Frank** (destructive/settings) |
| 7 | agentic-creator-os | Ecosystem Monitor failed 4 weeks running (run 34822849888, same Actions-PR permission error). 4 of 5 PRs conflict, including v12 #32 (65 days old). | hygiene | Same permission or token fix as #1. Rebase or close #32, #46, #53, #54. | Token/setting: needs Frank. Rebases: yes. |
| 8 | agentic-ops-hub | Fleet watch failed on all of the last 100 runs (run 35007919885). Heartbeats are 3–4 weeks stale and a queue item TTL has expired. | ops/hygiene (alert fatigue hides real outages) | Either restore the heartbeat publishers on c940 and yoga-book, or mark those machines retired. Expire the queue item and update the ledger through a PR. | Queue and ledger PR: yes. Heartbeat restore on the machines: needs Frank. |
| 9 | Protection gaps | No protection at all: arcanea-platform, starlight-token-tracker, starlight-memory, agentic-life-os, claude-code-config. Protected but no required checks: FrankX, arcanea, SIS, library-os, ACOS, AnimeLegends, vibeclubs. enforce_admins off: arcanea-ai-app, gencreator.ai. | security | Apply a baseline ruleset to all of these: no force-push, no deletion, the repo's CI as a required check. | **Needs Frank** (settings) |
| 10 | library-os, claude-code-config | No CI workflows (Copilot dynamic only). One repo is public OSS; the other governs the global Claude hooks. | hygiene | Add a minimal CI PR (`pnpm build` for library-os; a JSON/settings lint for claude-code-config). | Yes (PR only) |

Also noted:
- **agentic-life-os #9** ("fix(security): update js-yaml to patched 4.3.2") is a draft but mergeable. Quick security win; the merge needs Frank.
- **arcanea (OSS)**: 7 of 11 PRs have failing checks and the oldest is 86 days (#75). Needs a PR triage pass.
