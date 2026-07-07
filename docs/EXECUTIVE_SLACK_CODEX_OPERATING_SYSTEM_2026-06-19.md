# Executive Slack and Codex Operating System

Created: 2026-06-19  
Purpose: define the best-practice operating layer for Slack, humans, agents, Codex automations, brand pods, approvals, and onboarding across the multi-brand repo estate.

## Verdict

The current `#brand-*` setup is a good first scaffold, but it is not yet how the best operators would run it.

The best version is not "more channels." It is a named operating system:

**Starlight Portfolio OS**

Operating loop:

```text
Signal -> Decision -> Work -> Proof -> Distribution -> Learning
```

Slack is the cockpit. GitHub is the code truth. Linear or repo-native sprint files are the execution backlog. Notion/Docs/Drive are the narrative archive. Codex is the recurring analyst and execution-prep layer. Hermes is the dispatcher. n8n and Temporal are the deterministic automation layer. Postiz or the social publisher handles approved social scheduling.

Runtime companion: `agentic-ops-hub/docs/HERMES_PORTFOLIO_RUNTIME_AND_CLIENT_TEMPLATE_2026-06-19.md`

## What Elite Marketing CEOs Would Change

They would optimize for:

1. Fewer places to decide.
2. Clearer places to execute.
3. Faster approval loops.
4. A visible daily scoreboard.
5. A single funnel from ideas to shipped proof.
6. Onboarding that works for humans and agents without a private briefing.
7. A bias toward campaign rooms and operating templates, not permanent channel sprawl.

They would not let every brand become a mini-company with separate chaos. They would run a portfolio system with pods:

- Portfolio Command
- Brand Pods
- Shared Services
- Temporary Campaign Rooms
- Approval Queues
- Knowledge Canvases
- Codex Automation Reports

## Should There Be Separate Slack Organizations?

Not yet.

Use one Slack workspace with strict naming and channel sections until one of these becomes true:

- outside clients, partners, contractors, or community members need persistent access
- a brand needs privacy boundaries that normal private channels cannot handle cleanly
- external collaboration becomes high-volume enough to justify Enterprise Grid-style separation
- a brand has its own full-time team, budget, and operational calendar

Recommended now:

| Layer | Use | Example |
| --- | --- | --- |
| One workspace | internal portfolio command | FrankX / Arcanea / Starlight operations |
| Public `#brand-*` rooms | brand command, priorities, proof | `#brand-frankx` |
| Private rooms | sensitive strategy, legal/IP, finance, private vault | `#private-portfolio-strategy` |
| Temporary rooms | launches, campaigns, incidents, sprint pushes | `#camp-frankx-coe-launch` |
| External rooms | partners/contractors only when needed | `#ext-partner-oracle-coe` |

## Recommended Naming System

Keep the existing `#brand-*` rooms, but add stricter prefixes.

### Executive layer

| Prefix | Purpose | Examples |
| --- | --- | --- |
| `#hq-*` | executive command and allocation | `#hq-portfolio`, `#hq-decisions`, `#hq-weekly-review` |
| `#ops-*` | shared operating services | `#ops-repo`, `#ops-infra`, `#ops-automation`, `#ops-knowledge` |
| `#brief-*` | recurring reports and briefings | `#brief-daily`, `#brief-weekly`, `#brief-research` |

Recommended mapping from current rooms:

- Keep `#ops`, but treat it as `#hq-portfolio`.
- Keep `#daily-report`, but treat it as `#brief-daily`.
- Keep `#repo-command`, but future naming should be `#ops-repo`.
- Keep `#mcp-integrations`, but future naming should be `#ops-infra`.
- Keep `#hermes-agent`, but future naming should be `#ops-hermes`.

### Brand layer

| Prefix | Purpose | Examples |
| --- | --- | --- |
| `#brand-*` | permanent brand command room | `#brand-arcanea` |
| `#camp-*` | temporary campaign or launch | `#camp-frankx-coe-launch` |
| `#prod-*` | product build room when a product needs heavy execution | `#prod-arcanea-app` |
| `#repo-*` | only for load-bearing repos | `#repo-frankx-site` |

### Social layer

Keep platform rooms, but make `#social-command` the single planner and `#social-approvals` the hard gate.

Recommended substructure:

- `#social-command`: strategy, calendar, performance, channel mix
- `#social-approvals`: final approvals only
- `#social-x`, `#social-linkedin`, `#social-youtube`, etc.: platform packaging and variants
- `#social-syndication`: final cross-posting plans and published links

## Channel Canvas Standard

Every persistent channel needs a channel canvas. The canvas is the onboarding and operating manual.

Required channel canvas sections:

```md
# Channel Operating Manual

Purpose:
Owner:
Human approver:
Agent owner:
Primary repos/assets:
Current priority:
Decision rules:
Approval gates:
Daily update format:
Proof format:
Useful links:
Current sprint:
Do not post here:
```

This is the critical onboarding primitive. A new human or agent should be able to join any `#brand-*` room, read the canvas, and know what to do.

## Slack Lists To Add

Use Slack Lists only for lightweight queues that live inside Slack. Do not replace GitHub, Linear, or repo sprint files.

Recommended Slack Lists:

| List | Home channel | Purpose |
| --- | --- | --- |
| Portfolio Decisions | `#ops` | decisions needed from Frank, status, due date, decision owner |
| Social Approval Queue | `#social-approvals` | post candidates, platform, brand, risk, approval status |
| Content-to-Film Queue | `#content-film-prep` | recording topics, hook, CTA, assets, claim check |
| Repo Risk Queue | `#repo-command` | branches, PRs, deploy risks, owner, next command |
| Partner / Revenue Follow-ups | `#revenue-ops` | partner/account, offer, next touch, owner |
| Brand Weekly Scoreboard | each `#brand-*` | shipped, blocked, KPI, next bet |

## Slack Workflow Builder Forms

Forms should collect structured work instead of letting requests arrive as loose chat.

Recommended forms:

1. New Work Intake
   - posts to `#work-queue`
   - fields: brand, desired outcome, repo/asset, urgency, approval needed, proof required

2. Social Post Approval
   - posts to `#social-approvals`
   - fields: brand, platform, post copy, asset link, claim-risk, requested publish window

3. Content-to-Film Request
   - posts to `#content-film-prep`
   - fields: brand, topic, audience, hook, offer/CTA, sources, urgency

4. Repo Risk Escalation
   - posts to `#repo-command`
   - fields: repo, branch/PR, risk, command run, owner, requested decision

5. Brand Weekly Score
   - posts to the source `#brand-*` channel and `#ops`
   - fields: shipped, blocked, revenue movement, audience movement, next bet

## Best Slack Behavior Rules

1. Decisions go in `#ops` or the relevant `#brand-*` command room.
2. Work assignments go in `#execution-room` or a campaign room.
3. Drafts go in the relevant workroom, not the executive room.
4. Final social candidates go only to `#social-approvals`.
5. Proof links return to the room that assigned the work.
6. Threads are for discussion; top-level posts are for decisions, assignments, reports, and artifacts.
7. Every work post starts with one label: `Decision`, `Ask`, `Update`, `Blocker`, `Proof`, `Draft`, or `Approval`.
8. Every recurring report uses the same template.
9. Channels without a canvas, owner, and purpose should not exist long-term.
10. Temporary campaign channels are archived after the postmortem.

## Onboarding System For Humans And Agents

Create one onboarding channel:

- `#start-here-agents`

Channel canvas:

```md
# Start Here: Human and Agent Onboarding

1. Read `agentic-ops-hub/docs/MULTI_BRAND_AGENT_OPERATING_SYSTEM_2026-06-19.md`.
2. Read this channel canvas.
3. Identify your Brand Operating Unit or Shared Service.
4. Join the relevant `#brand-*` and support channels.
5. Read the channel canvas before posting.
6. Use the standard update format.
7. Do not publish, merge, deploy, spend, or message externally without the approval gate.
8. Proof closes work.
```

Standard agent kickoff prompt:

```md
You are joining the Starlight Portfolio OS. Read the multi-brand operating system, Hermes daily action system, target channel canvas, and target repo instructions. Classify work by Brand Operating Unit or Shared Service. Use Slack for routing and proof, GitHub for code truth, and the approval gate before public actions.
```

## Tooling Verdict

Current stack is strong, but each tool needs a narrower job.

| Tool | Keep? | Job |
| --- | --- | --- |
| Slack | Yes | human cockpit, approvals, intake, daily reports, decision visibility |
| GitHub | Yes | code truth, PRs, issues/releases where repo-native |
| Linear | Yes, for high-priority execution | cross-brand milestones, deadlines, human-owned work |
| Notion / Docs / Drive | Yes | strategy archive, briefs, investor/partner docs, durable narrative |
| Codex | Yes | recurring synthesis, repo sweeps, report prep, implementation with verification |
| Claude Code | Yes | deep local coding sessions, hooks, repo-level execution |
| Hermes | Yes | dispatcher identity, routing, memory-aware handoffs, Telegram/remote triggers |
| n8n | Yes | SaaS/webhook glue, intake forms, reminders, notifications |
| Temporal | Yes, selectively | durable multi-step workflows with retries and state |
| Postiz / social publisher | Yes | scheduling approved social content |
| Slack Lists | Yes, lightweight only | decisions, approvals, content queue, repo risk queue |

Avoid:

- replacing GitHub/Linear with Slack chat
- letting agents publish directly from Slack without approvals
- creating brand workspaces too early
- making every repo a channel
- storing private strategy in public Slack rooms

## Codex Automations To Add

Keep the current `Daily Hermes Multi-Brand Action Loop`. Add these in order.

### P0: Daily Slack Executive Digest

Cadence: weekdays morning  
Output: Slack-ready digest for `#daily-report`  
Reads: `#ops`, `#repo-command`, `#work-queue`, `#execution-room`, `#social-approvals`, all `#brand-*` rooms  
Purpose: tell Frank what changed, what needs attention, and where decisions are blocked.

### P0: Daily Social Approval Monitor

Cadence: weekdays midday and late afternoon  
Output: stale approvals, ready-to-post items, blocked assets, claim risks  
Reads: `#social-approvals`, `#social-command`, platform rooms  
Purpose: keep social moving without bypassing approval.

### P0: Daily Repo Risk Sweep

Cadence: weekdays morning  
Output: active PRs, stale agent branches, production risks, failing checks, unowned repos  
Reads: GitHub audit files, local repo statuses, `#repo-command`  
Purpose: keep the 267-repo estate from drifting.

### P1: Weekly Portfolio Review

Cadence: Friday or Sunday  
Output: executive review for `#ops`  
Reads: daily reports, repo risk sweep, social performance, revenue blockers, brand scoreboards  
Purpose: decide what to double down on, park, archive, or promote.

### P1: Brand Scoreboard Builder

Cadence: weekly per brand  
Output: one scoreboard per `#brand-*` room  
Fields: shipped, blocked, KPI movement, content created, repo movement, revenue movement, next bet.

### P1: Content-to-Film Prep Builder

Cadence: weekdays late morning  
Output: 1-3 recording-ready briefs  
Reads: research intel, brand priorities, offer calendar, content gaps  
Purpose: turn research and strategy into filming action.

### P1: Revenue Blocker Monitor

Cadence: weekdays or 3x weekly  
Output: checkout, offer, domain, CRM, partner follow-up, payment blockers  
Reads: `#revenue-ops`, business docs, Linear/sprint files where available  
Purpose: keep money-path blockers visible.

### P2: Onboarding Drift Check

Cadence: weekly  
Output: channels missing canvas/owner/purpose, stale docs, broken source links  
Purpose: keep humans and agents able to self-onboard.

### P2: Incubator Promotion Review

Cadence: weekly  
Output: music, health, investor, dream/life/library, chat/exporter lane recommendations  
Purpose: decide promote, merge, park, or archive.

## Recommended Next Build Order

1. Add channel canvases to all `#brand-*` command rooms.
2. Add `#start-here-agents`.
3. Create Slack Lists for decisions, approvals, film prep, and repo risks.
4. Create Workflow Builder forms for intake, social approval, film prep, and repo risk.
5. Promote Codex automations in this order: executive digest, social approval monitor, repo risk sweep, weekly portfolio review.
6. Generate `portfolio-repo-registry.json`.
7. Use weekly review to reduce channels, not increase them.
