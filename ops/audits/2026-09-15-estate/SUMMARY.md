# Estate Audit + Council — 2026-09-15 (c940)

Mission (Frank): coordinate the fleet across cloud, local CLIs and the Yoga Book; make git ops, PR review and production green and protected; heal installs; decide local vs cloud and subscriptions vs API workers. Agents own review/merge/cleanup; escalate only true blockers.

## Method
Four read-only audit lanes (handoff contract per `agentic-ops` skill), reports in this folder:
- `L1-github.md` — CI, open PRs, branch protection, Dependabot across Tier 1/2 repos
- `L2-runtime.md` — local CLIs, Hermes crons, scheduled tasks, MCP services, hooks, disk
- `L3-fleet.md` — fleet bus, heartbeats, pulse, Book branches, cloud agent workflows
- `L4-economics.md` — subscription value vs price, metered paths, routing policy

## Key findings
- **Production gate stuck:** frankx.ai `intelligence-refresh` failed 4 weeks (Actions not permitted to create PRs) → stale snapshot → required Merge Gate fails (#708 pending). Same permission error in ACOS Ecosystem Monitor.
- **Security:** FrankX 39 Dependabot alerts (2 critical, 23 high); Dependabot alerts disabled on 14 of 16 key repos; arcanea-platform unprotected with live deploy/publish workflows.
- **PR backlog:** 106 open PRs, 29 conflicting, 23 failing (arcanea-ai-app worst).
- **Fleet coordination broken:** three task buses with dead queues; Fleet watch failed 40/40 runs and spammed issue #43 (~130 comments); Book heartbeat 30 days old; 257 stale agent branches; 5 stranded Book branches.
- **Stranded cloud work:** Codex Cloud tasks never harvested (SIS 2026-09-12: capability control plane, crypto routing — both now conflict with main; loop kernel superseded by #156); Copilot drafts stale in mind-intelligence-systems.
- **Economics:** fixed plans + Railway ≈ $793/mo (~46% over the €499 envelope); Claude weekly ~1.8x sustainable pace with most usage off c940; Codex/Grok strong value; Copilot premium 0/7000 used; Railway $83/mo for deploys failing since August; revoked OpenAI key, malformed Gemini key, Hermes Anthropic fallback first without credential.
- **Runtime:** 7 skills without YAML frontmatter broke Codex skill loading; Codex skills budget overflow (335 dropped); Obsidian REST and SIS Operator down; Hermes Nous Portal refresh token invalid.

## Council verdicts (AGENT-COUNCIL.md)
1. Subscriptions vs API — **ship** pacing + gated on-demand worker policy (#67); Codex co-primary (reverses 2026-08-30 correction) **deferred to Frank**; Hermes fallback order, Railway, dead keys, plan right-sizing **escalated**.
2. Local vs cloud — **decided after evidence:** c940 cannot host build-heavy lanes (harness OOM-kills at commit-charge pressure even with RAM guards). Heavy install/build/deps lanes → **Copilot coding agent** (`gh agent-task create`, uses idle premium pool) or Codex Cloud (needs env IDs); light JSON/doc/CI lanes → local lean Codex/Grok (max 2); reviews → in-process Claude subagents (different family, no extra processes).
3. Buses — **split:** agentic-ops-hub `fleet/bus` + `pulse/<machine>` branches as single source of truth; freezing the other two buses needs Frank.
4. Fleet watch noise — **ship** dedupe (#68).
5. Stale branches — **report only**; deletion needs Frank.
6. Production PR gate / Actions permissions — **escalated**.

## Delivered (PRs; every merge preceded by a different-family review)
| Repo | PR | What | State at write time |
|---|---|---|---|
| starlight-token-tracker | #3, #4, #5 | Fleet Pulse v1, normal task priority, v2 change-gated pulse + Telegram alerts | merged |
| claude-code-config | #9 | CI validator (JSON/py/sh/ps1/hooks/secrets incl. sk-ant/sk-proj/github_pat), ACOS hook timeouts, untrack 34 MB WIP patches + vendored node_modules | merged (88e27ad); Actions disabled on repo, validator passes locally |
| agentic-ops-hub | #65 | queue Book pulse install; expire stale BOOK-HEARTBEAT (fixes repo-wide CI red) | reviewed, auto-merge armed, needs 1 approval |
| agentic-ops-hub | #67 | subscription pacing + on-demand API worker policy | 2 reviews → MERGE after #65, auto-merge armed |
| agentic-ops-hub | #68 | Fleet watch comments only on changed findings | 2 review rounds, fixes pushed (70/70 tests), auto-merge armed after #65 |
| FrankX | #200, #202, #204, #203 | Copilot setup steps (frees ~20 GB runner disk, pre-installs deps), removal of an orphaned submodule gitlink that broke checkout, then critical vitest alerts #224/#7 (vitest ^3.2.6). Attempts #199 (ENOSPC) and #201 (30-min timeout, out-of-scope edits) closed | merged (#203 17751f9) |
| library-os | #5 | green CI with lockfile, type-check, build (Copilot cloud; supersedes #4, closed) | merged (ac86a90), CI green |
| frankx.ai-vercel-website | #709 | removes unused `remark-mdx-frontmatter`, resolving toml alerts #142/#143 (extract-zip has no patched release) | merged (79008d6): `gh pr merge --auto` merged immediately because all checks were green and no approval is enforced, instead of waiting for Frank; 9/9 checks green, Vercel production READY, frankx.ai HTTP 200 |

Local healing: codex 0.154.0, gemini 0.59.0, opencode 1.18.31; `ccusage`/`tokscale` in `%APPDATA%\npm`; 7 skills frontmatter fixed (Codex load errors 21 → 0); Hermes gateway restarted onto updated code; `StarlightFleetPulse` at priority 4 with alerts.

## Lessons (also in Claude memory `reference_headless_agent_lanes`)
- Grok headless needs stdin `/dev/null`; Codex lanes must disable per-server MCP (`-c mcp_servers.<name>.enabled=false`) — `mcp_servers={}` does not work; harness task kills leave child processes alive.
- Windows Task Scheduler default priority 7 made `ccusage` exceed 180 s; priority 4 = 11 s.
- Copilot coding agent PRs open as drafts with CI held (`action_required`; the approve API is fork-only): a maintainer push triggers CI, and draft-gated workflows need a push after marking ready.
- `gh pr merge --auto` merges immediately when requirements are already met (production #709).
- Incident: a CI-trigger commit made from a `git worktree add --no-checkout` checkout recorded an empty tree on FrankX #203's branch; review caught it before merge and the branch was restored with a lease-protected force push. Trigger commits now use the Git Data API with the parent's tree.
- FrankX `ci.yml` is path-filtered and `main` requires no checks or reviews, so subproject-only PRs (e.g. #203) merge with only the key-guard check: a coverage gap.
- Different-family reviews caught real defects in 3 of 5 PRs (#67 pacing contradiction + unusable approval waiver, #68 silent exit 0 + duplicate comment on new issue, #9 secret regex missing modern key formats).

## 2026-09-16 follow-up (proactive pass)

- **Fleet complete:** Frank installed the pulse on the Book; `pulse/c940` and `pulse/yogabook` both report. This resolved the opening question: the Book is the Codex-heavy machine (30 codex processes; +14 Codex quota points and 33 M tokens in 12 h), so the earlier "unattributed Codex burn" was the Book, not claude.ai. Quota 04:30 CEST: Claude weekly 71 % (over the 45 % Wednesday pace target), Fable 75 %, Codex 32 %, Grok 60 %, Copilot premium 7 %.
- **New audit artifacts in this folder:** `stale-branches.md` (236 agent-lane branches, 14+ days, no open PR), `pr-backlog.md` (92 open PRs with age, draft, mergeability, failing checks), `pr-recommendations.md` (Codex triage of arcanea + ACOS: 0 MERGE / 3 REBASE / 2 CLOSE / 11 ASK FRANK - report only; closing or rebasing Frank-authored drafts needs his approval).
- **#67 hardened twice:** the Codex weekly window is now derived explicitly (tokscale reports the UPCOMING reset, so window start = `resets_at - 168 h`) and the floor formula reuses `cap_percent`; a reviewer finding to revert the config version to 2 was rejected (the PR intentionally publishes v5; `token_planner` requires only >= 2).
- **Cloud agent network limit found:** the Copilot cloud lane for the stale frankx.ai intelligence snapshot ran the fixture tests and licence check, then stopped because `models.dev` fails DNS inside GitHub's agent network. It refused to fabricate data, so the empty PR (#711) was closed and the refresh moved to a machine with normal network access. To use cloud lanes for this job later, `models.dev` must be allowlisted for the Copilot agent.
- **Copilot enablement extended:** `copilot-setup-steps.yml` (free disk + pre-install) merged in FrankX (#200, #202) and proposed for the 1.4 GB pnpm workspace `arcanea-ai-app` (#431), which holds the largest backlog (29 open PRs) and the two stale security drafts.

### 2026-09-16 merges and incidents

| Repo | PR | Result |
|---|---|---|
| arcanea-ai-app | #431 | Copilot setup steps (free disk + corepack pnpm 8.15 + frozen install) - merged 542f8ec, all required checks green; cloud lanes now possible on the largest backlog repo |
| frankx.ai-vercel-website | #712 | External intelligence snapshot refreshed locally (the scheduled workflow cannot open PRs) - merged 3290b93, 9/9 checks incl. Merge Gate, Vercel production READY, frankx.ai 200. Clears the stale-snapshot Merge Gate failure repo-wide |
| frankx.ai-vercel-website | #711 | Cloud attempt at the same refresh - closed: models.dev fails DNS inside GitHub's agent network; the agent correctly refused to fabricate data |
| FrankX | #208 | 13 high-severity alerts fixed in new-landing-page-backup (sharp, flatted, glob, minimatch x6, picomatch x2) - merged 9775597, one file changed |
| FrankX | issue #215 | Decision opened: move FrankX to Node 22 or stay on puppeteer 24.x (puppeteer 25 requires Node >= 22.12, repo pins 20) |

**Incidents on the #208 branch, both caught by review or verification and repaired before merge:**
1. The lane raised `postcss` to `^8.5.10` in the backup lockfile metadata without the matching manifest change, which breaks `npm ci`'s in-sync requirement; restored to `^8`.
2. A maintainer tree built through the Git Data API used abbreviated commit SHAs (the API rejects them), so empty blob references **deleted** both root `package.json` and `package-lock.json` instead of restoring them; repaired with main's exact blobs and verified by diffing against main before the ref moved.

**Corrections to the lane's claims:** `toml` alerts #371/#370 do have patched versions (4.2.0 / 4.1.2), so "no patched version" was wrong - the blocker is the `remark-mdx-frontmatter` dependency path; `extract-zip` #377/#352 were only cleared by the puppeteer bump that is now split out.

### FrankX security end state (2026-09-16)

**Critical 0 - High 19 -> 4** across the day: #203 (both criticals, vitest ^3.2.6), #208 (13 backup-folder alerts), #216 (runtime `toml` #371/#370, by removing `remark-mdx-frontmatter`, its sole parent and unused in the MDX pipeline - verified independently: `toml` and the package gone from the lockfile, `remark-gfm`/`remark-frontmatter` retained, 1686 -> 1682 packages, manifest and lock in sync).

The 4 remaining highs are deliberate, each with a named blocker:
- `extract-zip` #377, #352 - development scope, **no patched release exists**; they clear only with puppeteer 25, which needs Node >= 22.12 (decision: FrankX issue #215).
- nested `postcss` #66, #65 - runtime scope in `new-landing-page-backup/`, pinned by `next@15.5.25`; only a Next major moves it.

## True blockers for Frank
1. Approve agentic-ops-hub **#65** (unblocks CI and auto-merge for #67, #68 and this ledger PR).
2. On the Yoga Book: run `install-fleet-pulse-book.cmd` from Downloads (no remote shell exists).
3. frankx.ai production: merge **#708**; allow GitHub Actions to create PRs (fixes intelligence-refresh + ACOS monitor). Decide whether production `main` should enforce the 1-approval rule (it did not block #709).
4. Enable GitHub Actions on claude-code-config (or keep local-only validation).
5. Money/credentials: Railway stack ($83/mo, failing), revoked OpenAI key, malformed Gemini key, Hermes fallback order, Hermes Nous Portal re-auth, plan right-sizing; Codex co-primary routing nod.
6. Settings/destructive: enable Dependabot alerts on Tier 1/2 repos; baseline protection ruleset (arcanea-platform first); delete old Hermes `.bak` (8.7 GB) and Claude `vm_bundles` (10 GB); approve deletion list for 257 stale agent branches.
7. Optional: look up Codex Cloud environment IDs once (`codex cloud`) to enable Codex Cloud lanes.
