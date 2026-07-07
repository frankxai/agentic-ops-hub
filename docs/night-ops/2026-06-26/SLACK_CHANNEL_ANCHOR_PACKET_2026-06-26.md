# Slack Channel Anchor Packet - 2026-06-26

Status: internal Slack operating refresh. No channels were created, renamed, or
deleted. No Slack admin settings were changed.

## SI Route

```json
{
  "intent": "ops + Slack channel anchors + agent onboarding",
  "repo": "agentic-ops-hub",
  "lanes": ["codex", "slack-readonly/write-proof", "starlight-si"],
  "readOnlyRuntime": true,
  "why": "The proof-loop now works; the next bottleneck is channel clarity, owner cadence, and onboarding for humans and agents.",
  "stopCondition": "Anchor packet saved, proof posted internally, no new permanent channels added."
}
```

## Observed Slack State

- `#start-here-agents` already has a solid onboarding anchor from
  2026-06-19.
- `#work-queue` has the first proof-loop test item.
- `#execution-room` contains proof that the loop moved from setup to artifacts
  to Slack proof.
- `#repo-command`, `#hermes-agent`, `#social-carousels`,
  `#social-approvals`, `#daily-report`, and `#brand-arcanea` now have fresh
  proof from the night pass.
- The channel surface is large enough. The next step is not more rooms; it is
  stronger anchors, closure, and weekly cadence.

## Channel Doctrine

Use Slack as the cockpit, not the database:

1. `#work-queue` captures asks before assignment.
2. `#execution-room` holds active assigned work.
3. `#repo-command` holds repo, branch, deploy, domain, and infra truth.
4. `#daily-report` holds executive signal and decisions.
5. `#social-carousels` is the workroom for carousel assets.
6. `#social-approvals` is the human gate, not a draft dump.
7. `#brand-*` rooms hold brand-specific decisions, weekly proof, and owner
   calls.
8. `#hermes-agent` holds runtime health and activation gates.

Labels:

- `Decision`
- `Ask`
- `Update`
- `Blocker`
- `Proof`
- `Draft`
- `Approval`

Rule: no proof means not done.

## Core Rooms

| Channel | ID | Job | Post When | Proof Required |
| --- | --- | --- | --- | --- |
| `#ops` | `C0B9M0AM2BZ` | business-level decisions and spend gates | cross-business decision, spend, access, owner conflict | decision owner and approved path |
| `#start-here-agents` | `C0BBP54EMA9` | human/agent onboarding | onboarding update or operating-system map change | source docs and current channel map |
| `#work-queue` | `C0BBRH91709` | intake before assignment | new ask with outcome, owner, deadline, proof | assigned channel or hold reason |
| `#execution-room` | `C0BB87M571V` | active work and proof | work begins, status changes, proof lands | artifact path, Slack link, PR, report, screenshot, or approval receipt |
| `#daily-report` | `C0BBHBAQZMH` | executive rollup | meaningful outcome, blocker, red/yellow decision | linked proof, owner, next decision |

## Runtime, Repo, And Knowledge Rooms

| Channel | ID | Job | Post When | Guardrail |
| --- | --- | --- | --- | --- |
| `#hermes-agent` | `C0BBMKHSVAS` | Hermes profile/gateway/cron/kanban health | runtime state changes, activation dry-runs, blockers | no gateway start without green gates |
| `#repo-command` | `C0BA49F2BRP` | repo, branch, PR, deploy, domain truth | sweeps, red repos, Vercel/domain signals, merge/deploy gates | no merge/deploy/domain edit by default |
| `#mcp-integrations` | `C0BA2FHNP2N` | MCP/plugin/tooling integrations | connector setup, token scopes, tool health | least privilege, no secrets posted |
| `#knowledge-systems` | `C0B9W4SNR0B` | memory, docs, registries, knowledge tree | taxonomy, registry, ontology, doc routing | no private data leak |
| `#design-intelligence` | `C0B9W4TE5K5` | visual QA and design standards | QA scores, visual gates, brand/taste decisions | inspect artifacts before claiming pass |

## Content And Social Rooms

| Channel | ID | Job | Post When | Approval Gate |
| --- | --- | --- | --- | --- |
| `#research-intel` | `C0BBMJYA17Y` | source-backed signals and claim checks | official-source update, claim risk, research pack | source list and claim-risk label |
| `#content-film-prep` | `C0BCJ0MNLKS` | recording briefs and B-roll prep | 1 to 3 recording-ready briefs | claim-check before recording |
| `#social-command` | `C0BB6K4U4MT` | social strategy and routing | campaign plan, platform decision, learning note | do not approve final posts here |
| `#social-carousels` | `C0BCPG55PJB` | carousel workroom | design pack, contact sheet, draft caption, QA | proof first, approval later |
| `#social-approvals` | `C0BB6K6TT1B` | final human approval | only ready candidates or queue hygiene | Frank/owner approval before public post |

Platform channels:

| Channel | ID | Use |
| --- | --- | --- |
| `#social-linkedin` | `C0BBBS3JH5X` | LinkedIn platform-specific variants and results |
| `#social-instagram` | `C0BBDL5KQ2G` | Instagram carousel/reel variants and results |
| `#social-youtube` | `C0BBBSBPKLZ` | YouTube titles, thumbnails, Shorts, long-form prep |
| `#social-x` | `C0BBDL3UCLU` | X thread variants and distribution ideas |
| `#social-tiktok` | `C0BBA1T0AE6` | TikTok hooks and short-video ideas |
| `#social-threads` | `C0BAUH4N61M` | Threads variants |
| `#social-bluesky` | `C0BC49Z2464` | Bluesky variants |
| `#social-farcaster` | `C0BBDL79TJ8` | Farcaster/community-native variants |
| `#social-syndication` | `C0BB3LHL8F5` | cross-platform repurposing and performance recap |

## Brand Rooms

| Brand | Channel | ID | Weekly Proof Pattern |
| --- | --- | --- | --- |
| Starlight | `#brand-starlight` | `C0BBUAMFCP3` | runtime health, repo registry, domain radar, activation gates |
| FrankX | `#brand-frankx` | `C0BBP3AJ39T` | authority content, funnel, film prep, site changes |
| GenCreator | `#brand-creator-systems` | `C0BBSFAJKDG` | ACOS templates, creator workflows, community/client packaging |
| Arcanea | `#brand-arcanea` | `C0BBUAKTGSD` | product/app proof, visual QA, canon/IP decisions |
| Agentic Income | `#brand-agentic-income` | `C0BBP3CF0CD` | offer page proof, checkout blocker, revenue content |
| AI CoE | `#brand-ai-coe` | `C0BCLPDGHAL` | enterprise offer, Oracle/partner prep, academy assets |
| Reality Architect | `#brand-reality-architect` | `C0BBQCXV7AA` | method content, public/private boundary, paid vault proof |
| Anime Legends | `#brand-anime-legends` | `C0BBUAQ1N57` | canon, asset provenance, launch workflow |
| Mind | `#brand-mind` | `C0BBN7ZS8TZ` | source-backed mind/research signals, private/public boundary |
| Tooling / OSS | `#brand-tooling-oss` | `C0BCLPGJ3RN` | releases, trust, hooks, skills, public package proof |

## Approval Gates

| Action | Approval Channel |
| --- | --- |
| publish public social | `#social-approvals` and relevant `#brand-*` |
| production deploy | `#repo-command` and brand/business owner |
| merge to main | `#repo-command` |
| customer or partner message | relevant `#brand-*` and account owner |
| spend money | `#ops` and business owner |
| public factual claim | source proof and relevant `#brand-*` |
| private-to-public asset | guardian review and relevant `#brand-*` |

## Post Templates

### Work Queue Ask

```md
**Ask: <outcome>**

Brand/unit:
Outcome:
Owner/agent:
Deadline:
Repo or asset path:
Approval gate:
Proof required:
Blocking decision:
```

### Execution Item

```md
**Execution item**
Outcome:
Owner/agent:
Deadline:
Channel of record:
Repo/asset:
Proof required:
Status: TODO / DOING / BLOCKED / DONE
```

### Proof

```md
**Proof: <thing completed>**

What changed:
Artifact:
Validation:
Slack route:
Safety proof:
Next decision:
```

### Social Approval Candidate

```md
**Approval: <asset/post name>**

Brand:
Platform:
Asset path:
Caption/post:
Sources:
Claim-risk:
Visual QA:
Decision needed: APPROVE / APPROVE WITH EDITS / REVISE / HOLD / REPLACE
```

### Brand Weekly Proof

```md
**Weekly Proof: <brand>**

Outcome this week:
Best artifact:
Risk/blocker:
Next decision:
Approval gate:
Proof link:
```

## Agent Onboarding Checklist

Every human or agent entering the system should:

1. Read `#start-here-agents`.
2. Identify the brand unit or shared service.
3. Read the relevant `#brand-*` room and support channel.
4. Read repo-local `AGENTS.md` before touching files.
5. Use `#work-queue` for unassigned asks.
6. Move active work to `#execution-room`.
7. Close with proof before calling work done.
8. Use approval gates for public, production, financial, access, or external
   actions.

## Current Automation Layer

| Automation | Status | Job |
| --- | --- | --- |
| `daily-hermes-report-prep` | active heartbeat | daily multi-brand action loop |
| `starlight-daily-domain-and-deployment-digest` | active cron | domain/deployment radar, updated to radar contract |
| `starlight-daily-repo-risk-sweep` | active cron | repo risk sweep |
| `starlight-daily-slack-executive-digest` | active cron | executive Slack digest |
| `starlight-daily-slack-workflow-proof-monitor` | active cron | stale proof/anchor monitor |
| `starlight-daily-content-and-image-pipeline-prep` | active cron | content/image prep |
| `starlight-daily-carousel-factory` | active cron | one high-quality carousel candidate or learning note |
| `frankx-ai-tool-update-radar` | active cron | AI tool/product update radar |
| `frankx-linkedin-top-voice-daily-packet` | active cron | LinkedIn daily packet |
| `frankx-weekly-linkedin-strategy-review` | active cron | weekly LinkedIn strategy review |

## Keep / Revise / Pause / Cut

Keep:

- `#work-queue -> #execution-room -> #daily-report`
- `#repo-command`
- `#hermes-agent`
- `#social-carousels`
- `#social-approvals` as the final gate

Revise:

- brand-room weekly proof cadence
- social approval queue hygiene
- domain/project ownership map in `ecosystem.json`

Pause:

- new permanent Slack channels
- additional Hermes gateways
- public social autopublishing

Cut:

- any channel whose only job is to receive duplicate reports
- social approval posts that are not ready for a decision
- agent status updates with no artifact, owner, or next decision

## Next Proof Test

Run one weekly brand proof cadence test:

- Pick `#brand-arcanea` because it has the clearest red decision.
- Post one `Weekly Proof: Arcanea` item with domain mapping, dirty-state split,
  and next owner decision.
- Route supporting repo details to `#repo-command`.
- Summarize only the decision in `#daily-report`.

This tests whether brand rooms can become useful decision rooms without becoming
parallel backlog dumps.

## Slack Proof

- `#start-here-agents` anchor refresh:
  https://frankxintelli-cu22555.slack.com/archives/C0BBP54EMA9/p1782440982026609
- `#work-queue` proof-loop closure:
  https://frankxintelli-cu22555.slack.com/archives/C0BBRH91709/p1782440995068479
- `#execution-room` automation/anchor proof:
  https://frankxintelli-cu22555.slack.com/archives/C0BB87M571V/p1782441005919419
