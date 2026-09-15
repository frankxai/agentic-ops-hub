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
| FrankX | #199 | critical/high Dependabot fixes (Copilot cloud agent) | in progress |
| library-os | #5 | green CI with lockfile, type-check, build (Copilot cloud; supersedes #4) | in progress |
| frankx.ai-vercel-website | #709 | high-severity transitive dependency patches (Copilot cloud; PR only) | in progress; prod merge is Frank's |

Local healing: codex 0.154.0, gemini 0.59.0, opencode 1.18.31; `ccusage`/`tokscale` in `%APPDATA%\npm`; 7 skills frontmatter fixed (Codex load errors 21 → 0); Hermes gateway restarted onto updated code; `StarlightFleetPulse` at priority 4 with alerts.

## Lessons (also in Claude memory `reference_headless_agent_lanes`)
- Grok headless needs stdin `/dev/null`; Codex lanes must disable per-server MCP (`-c mcp_servers.<name>.enabled=false`) — `mcp_servers={}` does not work; harness task kills leave child processes alive.
- Windows Task Scheduler default priority 7 made `ccusage` exceed 180 s; priority 4 = 11 s.
- Different-family reviews caught real defects in 3 of 5 PRs (#67 pacing contradiction + unusable approval waiver, #68 silent exit 0 + duplicate comment on new issue, #9 secret regex missing modern key formats).

## True blockers for Frank
1. Approve agentic-ops-hub **#65** (unblocks CI and auto-merge for #67, #68 and this ledger PR).
2. On the Yoga Book: run `install-fleet-pulse-book.cmd` from Downloads (no remote shell exists).
3. frankx.ai production: merge **#708**; allow GitHub Actions to create PRs (fixes intelligence-refresh + ACOS monitor); later merge **#709** after its review.
4. Enable GitHub Actions on claude-code-config (or keep local-only validation).
5. Money/credentials: Railway stack ($83/mo, failing), revoked OpenAI key, malformed Gemini key, Hermes fallback order, Hermes Nous Portal re-auth, plan right-sizing; Codex co-primary routing nod.
6. Settings/destructive: enable Dependabot alerts on Tier 1/2 repos; baseline protection ruleset (arcanea-platform first); delete old Hermes `.bak` (8.7 GB) and Claude `vm_bundles` (10 GB); approve deletion list for 257 stale agent branches.
7. Optional: look up Codex Cloud environment IDs once (`codex cloud`) to enable Codex Cloud lanes.
