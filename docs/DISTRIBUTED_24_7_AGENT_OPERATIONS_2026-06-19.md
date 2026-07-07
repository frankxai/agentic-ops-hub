# Distributed 24/7 Agent Operations

Created: 2026-06-19  
Mode: guarded 24/7, primary/satellite device split, approval-gated autonomy

## Operating Thesis

Frank's agent estate should run like a disciplined portfolio company, not a pile of open terminals.

Slack is the cockpit. Hermes is the runtime. GitHub is code truth. Codex is synthesis, planning, automation design, and implementation prep. Claude Code, Antigravity, Grok, and other harnesses are specialist workers invoked by a human, Hermes task, or Codex-approved workflow. They should not become uncontrolled daemons.

Default permissions:

- Agents may research, triage, draft, test, summarize, prepare branches, prepare PRs, and queue work.
- Agents may not publish, deploy to production, merge, spend money, send customer-facing messages, post externally, delete data, or change credentials without explicit approval.
- Any action that leaves the private operating system must pass through a Slack approval room or a repo/brand command room.

## Implementation State

The foundational Hermes runtime is already staged:

- Hermes profiles exist for `starlight`, `frankx`, `gencreator`, `arcanea`, `income`, `aicoe`, `reality`, `research`, `tooling`, `anime`, and `mind`.
- Hermes kanban is initialized with board `starlight-portfolio-os`.
- Current activation cards are blocked, not ready or running.
- All profile gateways and crons remain stopped until credentials, Slack routing, approval gates, and machine health are verified.
- `starlight` remains the first and only gateway candidate.
- Codex daily synthesis remains the active daily loop while Hermes gateway/crons are still gated.
- Canonical brand-agent ownership now lives in `C:\Users\frank\starlight\ecosystem.json`.

Current blocked activation cards:

| Card | Assignee | Why blocked |
| --- | --- | --- |
| Configure Starlight gateway credentials and Slack routing | `starlight` | Needs token, channel map, approval policy, and proof test |
| Generate `portfolio-repo-registry.json` from the 267-repo audit | `starlight` | Needs approved workflow and no accidental repo mutation |
| Create profile-specific gateway and cron activation plan | `starlight` | Needs per-profile Slack/gateway policy |
| Package Agentic Organization OS template v1 | `tooling` | Needs device runtime and guarded autonomy template |

## Local Device Snapshot

Yoga Book / primary machine scan was run on 2026-06-19.

Capability output:

- Hostname: `STARLIGHT`
- OS: Windows 11 Home, version `10.0.26200`
- Architecture: `AMD64`
- CPU: Intel Core Ultra 7 255H
- GPU: Intel Arc 140T GPU (16GB)
- RAM: 31.4 GB total, 7.2 GB free at scan time
- Disk: 482.0 GB free, 469.6 GB used, 49.3% used
- Agent processes seen: 10 Codex processes using about 1557 MB, 29 Node processes using about 6028 MB
- Capability file: `C:\Users\frank\starlight\machines\starlight.json`
- Local profile file: `C:\Users\frank\.starlight\umwelt\env.json`

Detected tools:

| Tool | Version |
| --- | --- |
| Git | `2.54.0.windows.1` |
| GitHub CLI | `2.92.0` |
| Node | `24.16.0` |
| Bun | `1.3.14` |
| UV | `0.11.21` |
| Python | `3.11.15` |
| restic | `0.19.0` |

Current local zone: GREEN for controlled command work, with a caution flag for existing Node/Codex process load. Keep the Yoga Book default at max 4 heavy sessions until repeated telemetry proves a higher ceiling.

Second Lenovo Yoga status: not yet confirmed by live telemetry in this implementation pass. It remains a planned satellite worker, not an activated runtime node.

## Device Split

### Yoga Book 9i: Primary Command And Creative Workstation

Purpose: command, review, creative, frontend/product, and executive judgment.

Owned workflows:

- `starlight` Hermes gateway first
- Slack command surface
- portfolio decisions and approvals
- frontend/product review
- content and film prep
- creative direction and visual QA
- Vercel preview verification
- Codex daily reports and implementation prep
- interactive Claude Code / Antigravity / Grok sessions for product and creative work

Default limits:

- Max 4 heavy sessions until telemetry proves more is safe.
- In GREEN: may spawn approved workers.
- In YELLOW: finish current work, avoid new heavy workers.
- In RED: stop starting new workers, run safe cleanup, report health.

### Second Lenovo Yoga: Satellite Backend And Batch Worker

Purpose: repo, backend, QA, research, and batch execution.

Owned workflows:

- `tooling`, `research`, `aicoe`, `income`, and selected `starlight` tasks
- repo sweeps
- test/build jobs
- backend maintenance
- GitHub branch hygiene
- source-backed research scans
- customer-support drafts
- batch automation

Default limits:

- Max 2-3 heavy sessions until telemetry proves more is safe.
- No public publishing authority by default.
- No production deploys by default.
- No customer-facing sends by default.

### Mobile And Secondary Devices

| Device | Role |
| --- | --- |
| OnePlus | mobile Slack cockpit, approvals, quick triage |
| Huawei / sandbox laptop | experimental or isolated tests only |
| Samsung / security vault | sensitive review and account recovery, not automation |
| Lenovo Yoga 2 / Linux satellite if available | lightweight batch jobs, renders, isolated compute |

## Sync And State Policy

Code moves through Git. Private operating memory moves through approved vault lanes. Runtime state does not sync across machines.

Allowed Syncthing lanes:

- vaults
- inbox
- scratch
- notes
- handoff documents

Forbidden Syncthing lanes:

- `.git`
- tokens
- `.env`
- SSH keys
- logs
- sessions
- Hermes runtime state
- Codex/Claude/Grok/Antigravity runtime state
- caches
- `node_modules`
- `.venv`
- `.next`
- `.turbo`
- lock files
- PID files
- ports
- MCP credentials

## Machine Health Zones

| Zone | Conditions | Agent behavior |
| --- | --- | --- |
| GREEN | disk, RAM, CPU, battery/power, and network healthy | can spawn approved workers within concurrency limit |
| YELLOW | resource pressure, uncertain sync state, low battery, or elevated process count | finish current work, queue new work, avoid new heavy sessions |
| RED | low disk, memory exhaustion, runaway workers, broken sync, credential risk, or unclear runtime state | no new workers, stop gateways if needed, run safe cleanup, report status |

Minimum scan for every device:

- hostname
- OS and architecture
- RAM and disk
- GPU if available
- installed tools: GitHub CLI, Git, Slack/Hermes readiness, Codex, Claude Code, Antigravity, Grok, Node, Python, Bun, UV, Vercel, Railway, Syncthing, restic
- active heavy processes
- current repo/sync lanes
- recommended max concurrency

## Slack Operating Surface

Keep the current command surface. Do not add more permanent channels until every existing room has an owner, purpose, approval gate, and onboarding anchor.

Core rooms:

- `#ops`
- `#hermes-agent`
- `#repo-command`
- `#daily-report`
- `#work-queue`
- `#execution-room`
- `#start-here-agents`
- `#social-approvals`

Brand rooms:

- `#brand-starlight`
- `#brand-frankx`
- `#brand-gencreator`
- `#brand-arcanea`
- `#brand-income`
- `#brand-aicoe`
- `#brand-reality`
- `#brand-anime`
- `#brand-mind`

Required top-level labels:

- `Decision`
- `Ask`
- `Update`
- `Blocker`
- `Proof`
- `Draft`
- `Approval`

Approval routing:

| Action | Required approval surface |
| --- | --- |
| Social post | `#social-approvals` plus relevant `#brand-*` room |
| Customer message | relevant brand room or customer-success room |
| Production deploy | `#repo-command` plus brand/business owner |
| Merge to main | `#repo-command` |
| Spend money | `#ops` or business owner room |
| Public claim | `#research` or `#brand-*` with source proof |
| Private-to-public asset | guardian review in brand room |

## Agent Responsibility Map

| Profile | Primary device | Responsibility |
| --- | --- | --- |
| `starlight` | Yoga Book first, satellite secondary later | orchestrator, repo registry, machine health, kanban routing, cross-brand governance |
| `frankx` | Yoga Book | authority, content, funnel, film prep, newsletter, FrankX site |
| `gencreator` | Yoga Book | ACOS, creator workflows, templates, client/community productization |
| `arcanea` | Yoga Book | frontend/product, visual intelligence, creative platform, IP/media |
| `tooling` | Second Yoga | GitHub hygiene, OSS, hooks, MCP, agent config, repo risk |
| `research` | Second Yoga | source-backed research, claim checks, market scans, content angles |
| `mind` | Second Yoga for research/batch, Yoga Book for sensitive review | psychology, neuroscience, research-intelligence systems, mind palace, family/health intelligence, and claim-risk governance |
| `aicoe` | Second Yoga | enterprise/Oracle offers, partner prep, academy assets |
| `income` | Second Yoga | affiliate/revenue content, offer pages, checkout blockers |
| `reality` | Yoga Book, with strict private/public boundary | method/vault content and paid/private boundary |
| `anime` | Yoga Book for creative, satellite for asset QA | Anime Legends IP, canon, assets, launch workflows |

## Worker Tiers

| Tier | Runtime | Examples | Default |
| --- | --- | --- | --- |
| 0 | Human approval | publish, merge, production deploy, customer send, spend | always required |
| 1 | Lightweight always-on | Codex daily synthesis, Slack digest, health heartbeat | allowed after setup |
| 2 | Queued workers | Hermes kanban task, repo sweep, research scan, support draft | approval-gated |
| 3 | Heavy interactive workers | Claude Code, Antigravity, Grok, long builds, visual QA | invoked, not daemonized |
| 4 | Durable workflows | n8n forms/reminders, Temporal multi-step flows | only after one manual loop works |

## Activation Sequence

1. Run `umwelt-scan` on Yoga Book and record the current machine snapshot.
2. Run the same scan on the second Lenovo Yoga and record hostname/specs.
3. Confirm both machines have the required tools and that Syncthing excludes forbidden lanes.
4. Confirm Hermes profile list and kanban stats: profiles present, gateways stopped, ready/running cards at zero.
5. Configure `starlight` Hermes gateway credentials on Yoga Book only.
6. Create Slack anchor posts for `#start-here-agents`, `#work-queue`, `#repo-command`, `#social-approvals`, and brand rooms.
7. Start `starlight` gateway only.
8. Run one safe kanban card: read-only repo/runtime health report.
9. Verify Slack notification, kanban event, no unexpected file mutation, and no public action.
10. Unblock `portfolio-repo-registry.json` generation through approved workflow.
11. Add second Yoga as satellite worker only after telemetry and sync lanes are green.
12. Activate additional profile gateways one at a time, starting with `tooling` or `research`.
13. Activate `mind` only after research proof, private/public boundaries, and health-sensitive output gates are tested.
14. Delay brand publishing profiles until social/customer approval tests pass.

## First Safe Runtime Test

Task:

```text
Ask: Produce a read-only portfolio runtime health report.
Profile: starlight
Allowed: read Hermes profile list, Hermes kanban stats, repo status summaries, local device scan output.
Forbidden: start gateways, create branches, edit files, deploy, publish, send external messages.
Proof: Slack post in #hermes-agent and doc/update link in #repo-command.
```

Acceptance:

- `hermes profile list` shows the eleven profiles.
- `hermes kanban stats` shows no ready or running cards before activation.
- One test card routes to `starlight`.
- The card returns proof.
- No public action occurs.
- No production deployment occurs.
- No unapproved file mutation occurs outside expected report output.

## Automations To Add Later

Add only as separate approved automations after the manual path works:

1. Daily Slack Executive Digest
2. Daily Repo Risk Sweep
3. Social Approval Monitor
4. Content-to-Film Builder
5. Revenue Blocker Monitor
6. Customer Support Triage
7. Weekly Portfolio Review
8. Onboarding Drift Check

Implementation split:

- Codex handles synthesis loops, planning, reporting, and implementation prep.
- Hermes handles live profile runtime, Slack gateway, kanban, cron, skills, and memory.
- n8n handles Slack forms, webhooks, routing, and approval reminders.
- Temporal handles durable multi-step workflows only after one manual workflow is proven.

## Client And Community Template Rule

This is not just Frank's ops layer. It should become a reusable architecture for:

- founders
- SMBs
- creators and influencers
- agencies
- universities and labs
- enterprise AI CoEs

Every template must include:

- device/runtime plan
- Slack channel map
- role/profile map
- approval gates
- autonomy policy
- sync/state policy
- first safe test
- 7-day launch plan
- proof standard
- rollback/stop procedure

## Stop Procedure

If the system behaves unexpectedly:

1. Stop any newly started Hermes gateway.
2. Do not start new workers.
3. Preserve logs and session state.
4. Post `Blocker` in `#hermes-agent`.
5. Move active kanban cards to blocked.
6. Record what happened in the relevant doc or handoff.
7. Resume only after the cause and approval gate are understood.
