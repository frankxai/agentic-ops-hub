# Slack Operating System Audit

Created: 2026-06-22  
Scope: FrankX / Starlight / Arcanea Slack cockpit, Codex automations, Hermes runtime, content production, social channels, and multi-agent operating model.

## Executive Read

The Slack foundation is good: the workspace already has the right bones for a serious agentic operating system.

What exists:

- core command rooms
- Hermes runtime room
- repo command room
- daily report room
- work queue and execution room
- start-here onboarding room
- social command and approval system
- platform-specific social rooms
- brand operating rooms
- content-to-film and research rooms
- design intelligence room

What is not yet elite:

- most rooms have anchor posts, but not enough live intake, proof, and closure traffic
- Slack channel names and the ecosystem registry had drift; registry has now been reconciled to actual Slack names and IDs
- Workflow Builder / Slack Lists are recommended, but not confirmed as active through the connector
- Hermes gateways and Hermes crons are intentionally stopped
- Codex has daily and weekly automations, but the daily loop is still a thread heartbeat rather than a detached workspace cron
- social production has channels, but not yet a fully instrumented content calendar, approval ledger, and post-performance loop

Bottom line: Slack is set up as a cockpit, but still needs the operating rhythm and structured workflow layer to become a high-performance command system.

## Current Slack Surface

### Portfolio Command

| Channel | Role |
| --- | --- |
| `#ops` | executive operating room, portfolio decisions, cross-business updates |
| `#daily-report` | morning plan and end-of-day proof report |
| `#work-queue` | intake before assignment |
| `#execution-room` | active assigned work only |
| `#start-here-agents` | onboarding front door for humans and agents |

### Agent Runtime And Repo Truth

| Channel | Role |
| --- | --- |
| `#hermes-agent` | Hermes runtime proof, profile/gateway/kanban/crons, activation status |
| `#repo-command` | repo-level truth, PRs, branch state, deploy readiness, build failures |
| `#mcp-integrations` | MCP, connectors, integrations, tool wiring |
| `#knowledge-systems` | memory, knowledge systems, second brain, docs |
| `#design-intelligence` | reusable visual QA, design-agent capability, image/video intelligence |

### Content And Social

| Channel | Role |
| --- | --- |
| `#research-intel` | research signal intake and source-backed insights |
| `#content-film-prep` | recording-ready briefs, scripts, shot lists, B-roll, claim checks |
| `#social-command` | weekly social planning, campaign priorities, source material |
| `#social-carousels` | LinkedIn and Instagram carousel production, deterministic decks, PDF/PNG exports, visual QA |
| `#social-approvals` | final approval queue before any social publish/schedule |
| `#social-x` | X/Twitter drafts and platform-specific variants |
| `#social-linkedin` | LinkedIn variants |
| `#social-instagram` | Instagram variants |
| `#social-youtube` | YouTube titles, descriptions, shorts/long-form packaging |
| `#social-tiktok` | TikTok hooks and short-form variants |
| `#social-threads` | Threads variants |
| `#social-bluesky` | Bluesky variants |
| `#social-farcaster` | Farcaster variants |
| `#social-syndication` | Medium, Dev.to, Mirror, Substack, blog syndication |

### Brand Operating Rooms

| Channel | Brand / Unit |
| --- | --- |
| `#brand-starlight` | Starlight substrate and fleet governance |
| `#brand-frankx` | FrankX demand, authority, audience, content |
| `#brand-creator-systems` | GenCreator / ACOS creator systems |
| `#brand-arcanea` | Arcanea product, creative platform, visual intelligence |
| `#brand-agentic-income` | income engine, affiliate, revenue content |
| `#brand-ai-coe` | AI-Architect / enterprise AI CoE |
| `#brand-reality-architect` | RealityArchitect method and vault boundary |
| `#brand-anime-legends` | Anime Legends IP/media |
| `#brand-research-intelligence` | broad research intelligence lane |
| `#brand-mind` | Mind Intelligence: psychology, neuroscience, mind palace, family/health intelligence |
| `#brand-tooling-oss` | developer tooling, OSS, skills, MCP, repo safety |

## Why These Names Are Mostly Right

The naming scheme follows the right Slack pattern: use clear prefixes so rooms sort by function and purpose.

- `#brand-*` means owned business unit or product surface.
- `#social-*` means platform-specific distribution or social operations.
- `#repo-*` means code truth and engineering state.
- `#content-*` means production asset preparation.
- `#daily-*`, `#work-*`, and `#execution-*` describe operating rhythm.

This is close to best practice because a new human or agent can infer where work belongs before reading any docs.

The one issue was alias drift. Some docs used shorter names like `#brand-income`, while Slack actually has `#brand-agentic-income`. That is now corrected in `C:\Users\frank\starlight\ecosystem.json`.

## Current Automations

### Codex

Active:

- `daily-hermes-report-prep`: thread heartbeat, daily, active. Produces portfolio report, brand signals, Hermes runtime signals, research intel, content-to-film prep, and execution queue.
- `starlight-weekly-blessing-ledger`: local cron, weekly Sunday 09:00, active. Produces private weekly estate ledger in `frankx-starlight-command`.

Limitations:

- Daily Hermes loop is a thread heartbeat, not a detached workspace cron.
- It prepares outputs but does not automatically post every report into Slack unless the running thread decides to notify.
- It should now read `ecosystem.json` `brandAgents`, `operatingSurface`, and channel IDs before routing.

### Hermes

Current:

- Profiles exist, including `mind`.
- Gateways are stopped.
- Hermes crons: none scheduled.
- Kanban: zero ready/running, blocked activation cards only.

This is correct for guarded autonomy.

### Slack Workflow Builder / Lists

Not verified through connector:

- Slack Workflow Builder form existence
- Slack Lists existence
- Slack channel canvases

Known limitation:

- A prior Canvas creation attempt returned `not_supported_free_team`, so anchor posts and repo docs are the current fallback.

## Best-Practice Target Model

High-performance teams do not make Slack a dumping ground. They make it a routing surface.

The operating loop should be:

```text
Signal -> Intake -> Triage -> Assignment -> Execution -> Proof -> Approval -> Distribution -> Learning
```

Slack owns:

- signal capture
- decisions
- approvals
- status
- proof links
- human steering

Slack should not own:

- source code
- long-term docs
- private vault content
- unstructured strategy sprawl
- final canonical repo state

GitHub owns code truth. Docs own durable memory. Hermes owns live runtime. Codex owns synthesis and automation prep. n8n handles deterministic workflow glue when manual loops are proven. Temporal handles durable multi-step workflows only after the manual path works.

## Content Production Pipeline

Use this as the canonical flow:

```text
Research signal
  -> #research-intel
  -> content angle
  -> #content-film-prep
  -> recording brief
  -> recording / asset capture
  -> platform variants
  -> #social-command
  -> #social-* platform rooms
  -> final candidate
  -> #social-approvals
  -> approved schedule/publish
  -> #social-syndication if reused
  -> performance and learning note
```

Every content item needs:

- brand
- audience
- source or origin
- hook
- primary format
- platform variants
- media/assets
- claim risk
- approval gate
- proof link
- performance follow-up

## Social Channel Rules

Use platform rooms for adaptation, not as disconnected content silos.

| Stage | Channel |
| --- | --- |
| weekly plan | `#social-command` |
| source material | `#research-intel`, `#brand-*`, `#content-film-prep` |
| platform adaptation | `#social-x`, `#social-linkedin`, `#social-youtube`, etc. |
| final approval | `#social-approvals` |
| carousel production | `#social-carousels` |
| reuse/syndication | `#social-syndication` |
| proof/performance | original platform thread plus `#daily-report` or brand room |

Do not publish or schedule from platform rooms directly. Platform rooms produce variants. `#social-approvals` gives permission.

## Workflows To Build Next

### 1. Universal Work Intake

Trigger: form or message shortcut  
Destination: `#work-queue`  
Fields:

- outcome
- brand/unit
- owner/agent suggestion
- repo/asset
- deadline
- approval gate
- proof required
- urgency
- blockers

Follow-up:

- Hermes kanban card or manual execution item
- active work moves to `#execution-room`

### 2. Social Approval Form

Trigger: form in `#social-approvals`  
Fields:

- platform
- profile/account
- brand
- source
- proposed publish window
- post text
- media link/path
- risk/claim note
- reuse plan

Required replies:

- `APPROVE`
- `APPROVE WITH EDITS`
- `REVISE`
- `HOLD`

### 3. Content-To-Film Builder

Trigger: research signal or daily report item  
Destination: `#content-film-prep`  
Fields:

- title
- brand
- audience
- hook
- three beats
- CTA
- assets needed
- B-roll notes
- claim check
- next recording action

### 4. Repo Risk Sweep

Trigger: daily or on-demand  
Destination: `#repo-command`  
Fields:

- repo
- branch
- dirty/ahead/behind
- failing command
- risk class
- owner
- next decision
- proof required

### 5. Daily Executive Digest

Trigger: every morning  
Destination: `#daily-report` plus summary in `#ops` if decisions are needed  
Sections:

- top 3 outcomes
- blockers
- approvals needed
- brand signals
- repo/infra risk
- content to film
- execution queue

### 6. Weekly Portfolio Review

Trigger: weekly  
Destination: `#ops` and durable doc/ledger  
Sections:

- shipped
- proof
- what moved business
- stalled loops
- channel noise
- open approvals
- next 3 priorities

## What To Improve In The Current Slack

1. Keep current channel names; do not rename now.
2. Stop adding new permanent rooms until each existing room has owner, purpose, workflow, and proof rule.
3. Add actual workflow forms/lists where Slack plan allows it; keep anchor-post fallback.
4. Put all channel IDs in `ecosystem.json` and make agents route from that, not memory.
5. Reduce `#ops` to decisions and portfolio proof; move execution chatter to `#execution-room`.
6. Use brand rooms for brand-specific decisions, not as dumping grounds.
7. Make `#daily-report` the daily synthesis artifact, not a second ops room.
8. Make `#social-command` the planning layer, platform rooms the adaptation layer, and `#social-approvals` the permission layer.
9. Create WIP limits: no more than 3 active execution items per agent/profile without explicit escalation.
10. Add weekly channel hygiene: quiet rooms with no activity, archive temp campaign rooms, refresh anchors.

## Recommended Sidebar Sections

For humans:

- Command: `#ops`, `#daily-report`, `#work-queue`, `#execution-room`
- Agents: `#hermes-agent`, `#start-here-agents`
- Code: `#repo-command`, `#mcp-integrations`
- Content: `#research-intel`, `#content-film-prep`, `#social-command`, `#social-approvals`
- Brands: all `#brand-*`
- Social Platforms: all `#social-*`
- Knowledge/Design: `#knowledge-systems`, `#design-intelligence`

For agents:

- only their brand room
- `#work-queue`
- `#execution-room`
- `#repo-command` if code-facing
- `#social-approvals` if public-facing
- `#hermes-agent` for runtime proof

## Immediate Action Plan

1. Use `ecosystem.json` channel IDs as canonical routing.
2. Update the daily Codex automation prompt to read `brandAgents`, `operatingSurface`, and channel IDs.
3. Create or verify Workflow Builder forms for work intake, social approval, film prep, repo risk, and daily digest.
4. Create Slack Lists if plan supports them: Work Queue, Social Approvals, Content Pipeline, Repo Risk, Decisions.
5. Post an updated `Proof` note in `#ops` and `#hermes-agent` with current Slack/runtime state.
6. Only then activate one safe Hermes gateway test for `starlight`.
