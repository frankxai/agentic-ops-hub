# Hermes Daily Action System

Created: 2026-06-19  
Timezone: Europe/Amsterdam  
Purpose: turn the multi-brand FrankX / Arcanea / Starlight estate into a daily execution machine coordinated through Hermes, Slack, Codex, Claude Code, Railway, n8n, Temporal, Postiz, and the repo command center.

Companion operating map: `agentic-ops-hub/docs/MULTI_BRAND_AGENT_OPERATING_SYSTEM_2026-06-19.md`

## Operating Thesis

Hermes should be the dispatcher, not just another worker. It should answer:

1. What matters today?
2. Who or which agent owns it?
3. What research is needed?
4. What content should be filmed?
5. What code/work needs to move?
6. What is blocked?
7. What evidence proves progress happened?

Slack is the human control surface. Repos are the source of truth. Codex creates scheduled briefs and work packages. Claude Code handles in-session implementation with hooks and quality gates. Hermes routes, remembers, and keeps the loop alive across local and Railway profiles.

The daily loop must run by Brand Operating Unit, not as one blended brand. Hermes should ask which unit owns each signal, which shared service supports it, which Slack room receives it, and what proof closes it.

## Slack Command Surface

| Channel | Role |
| --- | --- |
| `#hermes-agent` | Hermes dispatcher, routing decisions, profile health, agent handoffs. |
| `#daily-report` | Daily brief, end-of-day report, blockers, decisions needed. |
| `#research-intel` | Daily research, market/news scans, source-backed insights. |
| `#content-film-prep` | Scripts, talking points, filming briefs, shot lists, B-roll prompts. |
| `#work-queue` | Intake queue for humans and agents before assignment. |
| `#execution-room` | Active execution updates with owner, deadline, and proof. |
| `#ops` | Cross-business decisions and high-level blockers. |
| `#repo-command` | Repo status, branches, PRs, builds, deployment state. |
| `#content-comms` | Content calendar, launch comms, narrative packaging. |
| `#social-command` | Social campaign planning and platform matrix. |
| `#social-approvals` | Required human approval before social publishing or scheduling. |
| `#brand-frankx` | FrankX Demand command room. |
| `#brand-arcanea` | Arcanea Product and IP command room. |
| `#brand-starlight` | Starlight Substrate command room. |
| `#brand-ai-coe` | AI-Architect / AI CoE command room. |
| `#brand-agentic-income` | Agentic Income Network command room. |
| `#brand-reality-architect` | Reality Architect command room. |
| `#brand-creator-systems` | Creator Systems / ACOS command room. |
| `#brand-research-intelligence` | Research and Mind Intelligence command room. |
| `#brand-tooling-oss` | Tooling / open-source distribution command room. |
| `#brand-anime-legends` | Anime Legends / media IP command room. |

## Brand Operating Units To Run

| Brand unit | Primary outcome | Primary channels | Repo constellation |
| --- | --- | --- | --- |
| FrankX Demand | attention, trust, conversion | `#brand-frankx`, `#frankx-growth`, `#content-film-prep` | `FrankX`, `frankx.ai-vercel-website`, `author-os`, content worktrees |
| Arcanea Product and IP | creator platform, world engine, productized IP | `#brand-arcanea`, `#arcanea`, `#design-intelligence` | `arcanea-*`, `gencreator.ai`, `visual-intelligence`, `kura` |
| Starlight Substrate | agent runtime, memory, governance, evals | `#brand-starlight`, `#starlight-systems`, `#agent-teams` | `Starlight-Intelligence-System`, `starlight-*`, `second-brain-os` |
| AI-Architect / AI CoE | enterprise offers, Oracle/OCI authority, education | `#brand-ai-coe`, `#ai-coe`, `#revenue-ops` | `ai-coe`, `oci-ai-architect`, `claude-code-oracle-skills`, `ai-architect-academy` |
| Agentic Income Network | offers, affiliate, passive income | `#brand-agentic-income`, `#agentic-income`, `#revenue-ops` | `agenticincome`, `agenticpassiveincome`, `disruptivepassiveincome`, `affiliate-agent-skills` |
| Reality Architect | creator method, public method, paid Vault | `#brand-reality-architect`, `#reality-architect`, `#content-film-prep` | `realityarchitect`, `realityarchitect-vault` |
| Creator Systems / ACOS | reusable creator workflows and agent products | `#brand-creator-systems`, `#creator-systems`, `#prompt-systems` | `agentic-creator-os`, `agentic-creator-skills`, `workflow-tier-plugin` |
| Research and Mind Intelligence | research products, psychology/neuroscience/mind OS | `#brand-research-intelligence`, `#research-intel`, `#knowledge-systems` | `research-intelligence-*`, `mind-intelligence-*`, `agentic-mind-os`, `starlight-mind-os-pro` |
| Tooling / OSS Distribution | developer trust, skills, hooks, MCP, awesome lists | `#brand-tooling-oss`, `#repo-command`, `#mcp-integrations` | `claude-*`, `mcp-doctor`, `agentic-ops-hub`, `awesome-*` |
| Anime Legends / Media IP | media IP, interactive anime experience, social loops | `#brand-anime-legends`, `#anime-legends`, `#design-intelligence` | `AnimeLegends`, `Anime-Legends`, `AnimeLegends-Skills` |
| Incubator Lanes | music, health, investor, dream/life, chat/exporter experiments | brand channel only after promotion; otherwise `#work-queue` and `#repo-command` | ambiguous active repos from the 267-repo audit |
| Social Distribution | platform execution and approvals | `#social-command`, platform channels, `#social-approvals` | `starlight-social`, `agentic-creator-os` workflows |
| Ops / Infra | fleet, Railway, MCP, CI, safety | `#ops`, `#repo-command`, `#mcp-integrations` | `agentic-ops-hub`, `mcp-doctor`, `hermes-cockpit`, `claude-code-hooks` |

## Existing Automation Assets

| Asset | Current state | Use |
| --- | --- | --- |
| Claude Code hooks | Present via `claude-code-hooks` | Session lifecycle gates, audit trail, MCP health, compact handling, quality checks. |
| ACOS agents and workflows | Present via `agentic-creator-os` | Social generation, research, publishing, GitHub, monitoring, automation, GSD. |
| Hermes registry | Present via `hermes-cockpit/registry.json` | Local/cloud agent profiles and purposes. |
| Railway | Active estate includes Postiz, Temporal, n8n, LiteLLM, Langfuse, Infisical, Redis/Postgres services | Durable orchestration, social publishing, observability, model gateway, secrets. |
| n8n | Active Railway project | Good for webhook/time-based business workflows once credentials are settled. |
| Temporal | Active Railway project | Good for reliable long-running workflows and retries. |
| Postiz | Active Railway service | Social publishing backend candidate. |
| Codex automations | Thread heartbeat active: `daily-hermes-report-prep` / "Daily Hermes Action Loop" | Daily report, research intel, content-to-film prep, and execution queue prep in this Codex thread. |

## Hermes Agent Team

| Hermes profile | Role | Channel | Default action |
| --- | --- | --- | --- |
| `chief-of-staff` | Daily dispatcher and priority resolver | `#hermes-agent`, `#daily-report` | Turns signals into a work queue and owner map. |
| `research` | Research and source-backed synthesis | `#research-intel` | Produces daily intelligence briefs and content angles. |
| `film-producer` | Content-to-film package builder | `#content-film-prep` | Converts research/offers into scripts, shot lists, and filming prep. |
| `execution-dispatch` | Work assignment and follow-through | `#work-queue`, `#execution-room` | Assigns humans/agents and demands proof of completion. |
| `repo-guardian` | Repo/build/PR review | `#repo-command` | Checks branches, PRs, verification, and stale work. |
| `social-publisher` | Social staging and publication handoff | `#social-command`, `#social-approvals` | Stages content; publishes only after approval. |
| `railway-ops` | Railway/n8n/Temporal/LiteLLM health | `#mcp-integrations`, `#ops` | Watches services, cost, failures, and auth posture. |

## Daily Operating Cadence

### 08:15 Daily Report

Inputs:
- `agentic-ops-hub/docs/ECOSYSTEM_COMMAND_CENTER_2026-06-18.md`
- `agentic-ops-hub/ops/OPS-LEDGER.md`
- `hermes-cockpit/registry.json`
- latest Railway estate snapshot
- git status across active repos
- Slack channel activity from `#ops`, `#repo-command`, `#work-queue`, `#social-approvals`

Output: post to `#daily-report`, escalate decisions to `#ops`.

Template:

```md
**Daily Report - YYYY-MM-DD**

**Top 3 outcomes**
- ...

**Brand unit signals**
- FrankX:
- Arcanea:
- Starlight:
- AI CoE:
- Agentic Income:
- Reality Architect:
- Creator Systems:
- Research Intelligence:
- Tooling / OSS:
- Anime Legends:
- Incubator signals:

**Blockers**
- ...

**Work queue**
- Owner / agent / deadline / proof:

**Content to film**
- Topic:
- Why now:
- Script status:
- Recording ask:

**Repo / infra risks**
- ...

**Decisions needed from Frank**
- ...
```

### 09:00 Research Intel

Inputs:
- AI/agent market news
- creator economy and social/platform trends
- FrankX / Arcanea / Starlight strategic focus
- active content gaps
- audience/revenue opportunities

Output: post to `#research-intel`; route filmable items to `#content-film-prep`.

Rule: every research item needs a source, a take, and an action.

### 11:30 Content-To-Film Prep

Inputs:
- `#research-intel`
- FrankX posts, drafts, newsletters, offers
- current business priorities
- social calendar

Output: post recording-ready briefs to `#content-film-prep`.

Template:

```md
**Film prep**
Title:
Business:
Target platform:
Hook:
3 beats:
CTA:
Assets needed:
B-roll / visual notes:
Risk / claim check:
Next action:
```

### 14:00 Execution Dispatch

Inputs:
- `#work-queue`
- `#daily-report`
- repo status
- research and film prep queues

Output: assign work in `#execution-room` with owner, deadline, and proof requirement.

### 17:30 End-Of-Day Proof

Inputs:
- `#execution-room`
- git commits/PRs
- social drafts/approvals
- created assets

Output: post shipped / blocked / next to `#daily-report`; unresolved blockers go to `#ops`.

## Work Queue Rule

Every work item must have:

- brand unit
- owner: human or agent
- channel: where work happens
- repo or asset path
- deadline
- proof: PR, commit, Slack link, file path, published URL, screenshot, or approval receipt

No proof means not done.

## Content-To-Film Pipeline

1. Research signal lands in `#research-intel`.
2. Hermes picks angle and routes to `#content-film-prep`.
3. Film producer drafts hook, three beats, CTA, and claim check.
4. Frank approves or edits the filming brief.
5. Human films.
6. Editor/agent creates clips, titles, descriptions, and social variants.
7. Final social candidates go to `#social-approvals`.
8. Approved posts publish through Postiz / Starlight Social / manual upload.
9. Performance results return to `#social-command` and next research loop.

## Automation Recommendations

Use three automation engines:

| Engine | Best for | Do not use for |
| --- | --- | --- |
| Codex automations | daily briefs, repo sweeps, research packs, draft/stage work packages | direct publishing, secret changes, production deploys without approval |
| n8n | webhooks, recurring reminders, connecting SaaS tools, content calendar plumbing | reasoning-heavy synthesis |
| Temporal | reliable multi-step workflows with retries and state | quick ad-hoc drafts |
| Hermes | dispatcher, memory, long-running agent identity, Telegram/remote command gateway | replacing source-of-truth repos |
| Claude Code hooks | in-session quality and safety gates | scheduled business reporting |

Recommended Codex automations:

| Name | Cadence | Output |
| --- | --- | --- |
| Daily Report Prep | weekdays morning | Slack-ready `#daily-report` brief |
| Research Intel Pack | weekdays morning | 5-10 sourced opportunities in `#research-intel` format |
| Film Prep Builder | weekdays late morning | 1-3 recording-ready briefs |
| Execution Sweep | weekdays afternoon | owners/proof/blockers for `#execution-room` |
| EOD Proof Report | weekdays evening | shipped/blocked/next |
| Weekly Portfolio Review | weekly | repo/domain/agent team decisions |
| Social Approval Queue Review | weekdays | stale approvals and ready-to-publish candidates |

Current Codex automation state:
- A thread heartbeat named "Daily Hermes Action Loop" is active.
- It prepares the daily report, research intel, content-to-film prep, and execution queue.
- Detached workspace cron setup was attempted but rejected by the app schema in this environment, so the daily loop is currently thread-attached rather than a standalone workspace cron.

## Immediate Build-Out

1. Keep `#hermes-agent` as the dispatcher channel.
2. Add the planned Hermes profiles to `hermes-cockpit/registry.json`.
3. Use Codex for daily report prep and research pack generation once automation creation is confirmed.
4. Use Hermes Telegram for remote triggers and urgent check-ins.
5. Use n8n for calendar/reminder/webhook glue after the Slack channels settle.
6. Use Temporal only for real multi-step durable workflows, not simple reminders.
7. Add a publish guard to `starlight-social`: real publishing requires approval id from `#social-approvals`.

## First Daily Report Prompt

```md
Read the ecosystem command center, Hermes registry, Railway estate snapshot, ops ledger, and current git status across active repos. Produce today's Daily Report for Frank: top 3 outcomes, blockers, work queue, content-to-film candidates, repo/infra risks, and decisions needed. Format for #daily-report. Do not publish externally.
```
