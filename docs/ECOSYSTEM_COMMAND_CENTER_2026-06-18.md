# Ecosystem Command Center - 2026-06-18

This is the operating map for FrankX, Arcanea, Starlight, and the repo/agent estate. It upgrades the previous ops ledger from a 44-repo local view into a 267-repo GitHub-aware command center.

## Read This First

Canonical command surfaces:

- Human operations ledger: `agentic-ops-hub/ops/OPS-LEDGER.md`
- Current sprint object: `agentic-ops-hub/ops/ecosystem-sprint-2026-06-18.json`
- Live GitHub audit evidence: `C:\Users\frank\starlight\repos\GITHUB_267_REPO_AUDIT_2026-06-18.md`
- Local repo stabilization evidence: `C:\Users\frank\starlight\repos\REPO_STABILIZATION_REPORT_2026-06-18.md`
- Structured cockpit projection: `C:\Users\frank\starlight\command-center\state.json`
- Source ecosystem graph: `C:\Users\frank\starlight\ecosystem.json`

Every agent should read this file before making cross-repo decisions. New repos should be registered against this map before they are treated as part of the production estate.

## North Star

One operator, three power brands, one substrate:

- FrankX is the authority and demand engine: content, readers, trust, books, offers, and conversion.
- Arcanea is the creative platform and IP/product layer: creator tools, world engine, media, community, and premium experiences.
- Starlight is the substrate and moat: agents, governance, registries, evals, orchestration, memory, and quality gates.

The current highest-leverage move is not "more repositories." It is connecting the estate so the work compounds: FrankX attention feeds GenCreator/CoE offers, Arcanea converts creator energy into products, and Starlight makes every future build faster, safer, and more reusable.

## Current Estate Snapshot

Evidence date: 2026-06-18.

| Area | Count / Status | Interpretation |
| --- | ---: | --- |
| Live GitHub repositories | 267 | This is the real estate size, not the stale local subset. |
| Active GitHub repositories | 225 | Enough surface area that governance must be registry-driven. |
| Archived GitHub repositories | 42 | Keep archived repos out of sprint planning unless resurrected. |
| Local checkouts | 62 | Local work is clean after stabilization. |
| Local dirty repos | 0 | Good baseline; preserve it with PR-first work. |
| Repos active in last 7 days | 96 | Strong momentum, but branch/default hygiene now matters. |
| Repos with agent-style branches | 56 | Need a standard promotion path and branch review cadence. |
| Risk-flagged repos | 83 | Most are sync/noise flags; a few require human decision. |

## Current Focus

### P0 - Protect production trust

Production credibility first. Merge or finish review of `frankx.ai-vercel-website` PR #186, repair broken hooks, and keep local repo state clean. The site is the highest-public-surface asset, and it had a tracked local database plus a syntax regression on `main`; that class of issue must not become normal.

### P1 - Repair the FrankX to GenCreator revenue bridge

The estate has content momentum, but the flywheel is still weak if readers do not flow into a paid or owned product surface. Treat ARC-204 as the main commercial sprint: add contextual GenCreator / Personal CoE CTAs to post-2026-06-06 FrankX content, add footer/nav paths, and verify no broken links.

### P2 - Turn the repo fleet into a governed portfolio

The old registry covers 28 repos; GitHub has 267. Promote the live audit into the new registry baseline, classify every active repo by constellation, owner, public/private status, lifecycle, default branch, and health command. Every new repo needs an entry before more agents build on it.

### P3 - Land agent stack and world-engine work cleanly

Arcanea orchestrator, Arcanea ecosystem, SDS, SIS profiles, and agent runtime work should now move through PRs with explicit verification records. The work is good; the next win is making it reviewable, repeatable, and visible to future agents.

### P4 - Productize what already exists

The next sprint should favor packaging and conversion over raw creation: Founding 50, Personal CoE Starter PDF, GenCreator bridge, Arcanea creator/product cockpit, and downloadable starter packs.

## Sprint Plan: 2026-06-18 to 2026-06-25

| Milestone | Owner Surface | Goal | Done When |
| --- | --- | --- | --- |
| M0 Production Safety | GitHub / FrankX site | Merge or resolve PR #186, repair hooks, validate production site. | `type-check`, `lint`, secrets scan, and PR review are green. |
| M1 Revenue Bridge | Linear ARC-204 / FrankX | Convert FrankX traffic into GenCreator / CoE paths. | Every post-06-06 article has one contextual bridge and the site has persistent navigation. |
| M2 Fleet Registry | agentic-ops-hub / SIS | Replace stale 28-repo governance with 267-repo registry. | Active repos have constellation, lifecycle, default branch, owner, and health command. |
| M3 Branch Promotion | GitHub | Review high-risk branch/default exceptions. | Decisions recorded for `arcanea-flow`, `arcanea-agent-skills`, `damfrost1`, `damfrost2`, and active agent branches. |
| M4 Agent Operating System | Arcanea / Starlight | Land agent runtime, run records, SDS, and agent profile quality gates. | PRs merged or parked with explicit validation and next action. |
| M5 Revenue Packaging | Linear / Notion | Package offers already implied by the work. | Founding 50 DM, Personal CoE Starter PDF, and download-page packs have owners and ship criteria. |

## Repo Constellations

Use these constellations for registry classification and agent routing.

| Constellation | Strategic Job | Example Repos | Current Action |
| --- | --- | --- | --- |
| FrankX Demand | Authority, content, audience, offer conversion | `frankx.ai-vercel-website`, `FrankX` | Fix production PR, then bridge to GenCreator / CoE. |
| Arcanea Product | Creative platform, worlds, creator workflows, media | `arcanea-ai-app`, `arcanea-ecosystem`, `arcanea-orchestrator`, `arcanea-claw` | Promote world-engine and agent runtime through review. |
| Starlight Substrate | Governance, agents, memory, evals, orchestration | `Starlight-Intelligence-System`, `claude-code-config`, `starlight-swarm` | Align profiles, health gates, and repo registry. |
| Revenue Experiments | Affiliate, passive income, pricing, offers | `agenticincome`, `agenticpassiveincome`, `affiliate-agent-skills` | Keep only experiments tied to a conversion path. |
| Enterprise / CoE | Oracle, AI CoE, partner/business packages | `ai-coe`, `enterprise-ai-coe` surfaces | Package into Personal/Enterprise CoE offers. |
| Support Tooling | Hooks, docs, MCPs, skills, automation | `mcp-doctor`, `claude-code-hooks`, `agentic-ops-hub` | Keep boring, reliable, and documented. |

## Immediate Risk Decisions

1. `frankx.ai-vercel-website`: PR #186 fixes tracked `.acos/agentdb.db` and a downloads-page syntax regression. Merge after review and ensure hooks are repaired so future pushes do not require `--no-verify`.
2. `arcanea-flow`: latest default-branch commit rewrote README with 16 additions and 5997 deletions. Compare against parent and decide whether to restore doctrine into `docs/` or accept the concise README.
3. `arcanea-agent-skills`: active private repo default branch appears to be `codex/world-engine-docs`. Decide whether that is intentional; if not, restore a durable default branch.
4. `damfrost1` and `damfrost2`: active private repos have no default branch. Initialize, classify, or archive.
5. `Starlight-Intelligence-System`: local `main` is one commit ahead. Do not layer more hidden main pushes; promote through a branch or explicitly push once reviewed.
6. `litellm-agent-platform`: local `main` is ahead of external upstream only due to local ignore changes. Keep those on `codex/starlight-local-ignores`; do not push to upstream.

## Agent Operating Protocol

Before any agent edits a repo:

1. Read this command center, `ops/OPS-LEDGER.md`, `ops/ecosystem-sprint-2026-06-18.json`, and the target repo's `AGENTS.md` / `CLAUDE.md`.
2. Check `git status --short --branch` and never assume a repo is clean.
3. Do not push production `main` directly unless Frank explicitly requests it for that repo in that turn.
4. Use a named branch for meaningful work: `codex/<scope>` for Codex, existing repo branch conventions when already established.
5. Record verification commands in the PR or final report. For docs-only changes, at minimum verify links/paths and repo cleanliness.
6. Every new repo must get a registry entry with purpose, constellation, lifecycle, default branch, owner, public/private status, and health command.
7. Every cross-repo decision must update this command center or the sprint JSON so future agents do not rediscover context from scratch.

## GitHub / Linear / Notion Alignment

GitHub is the source of code truth. Linear is the action and milestone surface. Notion is the executive narrative and planning archive.

Minimum sync rule:

- GitHub PRs carry implementation evidence and validation.
- Linear issues carry owner, due date, priority, and user-visible outcome.
- Notion captures strategy, architecture, and weekly executive state.
- `agentic-ops-hub` remains the repo-native command center that agents can read without connector access.

## Weekly Review Agenda

Run this review every Sunday or before any large agent wave:

1. Pull latest GitHub inventory and regenerate repo audit.
2. Compare local registry coverage against live GitHub.
3. Review PRs and branches older than 7 days.
4. Confirm P0 production surfaces are green.
5. Update sprint JSON with completed milestones and next owners.
6. Mirror only active, owner-needed work into Linear.
7. Archive stale/duplicate repos or label them as dormant so they do not consume planning attention.

## Current Bet

For the next week, the winning move is: stabilize the public site, connect FrankX traffic to GenCreator/CoE, make the 267-repo registry real, and land the agent stack through reviewable PRs. That gives the portfolio a spine: revenue, trust, and a system future agents can actually follow.
