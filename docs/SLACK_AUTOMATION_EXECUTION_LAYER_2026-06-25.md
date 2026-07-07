# Slack Automation Execution Layer

Created: 2026-06-25

Purpose: make Slack the visible cockpit for portfolio execution while keeping
public actions approval-gated.

## Operating Verdict

The right move is not more Slack noise. The right move is a small number of
recurring loops that produce proof, decisions, and ready-to-approve work.

Slack owns visibility, routing, approvals, and proof. GitHub owns code truth.
Vercel and domain registries own site truth. Hermes owns runtime identity and
dispatch once activation gates are green. Codex owns recurring synthesis,
read-only scans, and preparation of human-approved next actions.

## Active Codex Automations

| Automation | Cadence | Primary Slack Route | Job |
| --- | --- | --- | --- |
| `daily-hermes-report-prep` | Daily heartbeat | Current Codex thread | Portfolio synthesis, brand signals, Hermes runtime, Slack workflow risks, research intel, content prep, execution queue |
| `starlight-daily-slack-executive-digest` | Daily 08:10 | `#daily-report` | Daily executive digest with outcomes, blockers, decisions, repo risks, domain/site watch, and execution queue |
| `starlight-daily-domain-and-deployment-digest` | Daily 08:35 | `#repo-command`, rollup to `#daily-report` | Domain, subdomain, site, GitHub, and Vercel/deployment health watch |
| `starlight-daily-repo-risk-sweep` | Daily 09:05 | `#repo-command`, P0/P1 rollup to `#daily-report` | Read-only repo risk sweep across flagship and now-priority repos |
| `starlight-daily-content-and-image-pipeline-prep` | Daily 10:30 | `#content-film-prep`, `#social-command`, drafts for `#social-approvals` | Recording briefs, platform variants, image/carousel prompts, and approval packets |
| `starlight-daily-carousel-factory` | Daily 11:15 | `#social-carousels`, approval candidates to `#social-approvals` | Premium LinkedIn/Instagram carousel packs with brief, learning input, design/taste docs, deterministic deck, post copy, approval packet, and QA evidence |
| `starlight-daily-slack-workflow-proof-monitor` | Daily 16:20 | `#daily-report` when meaningful | Detects stale anchors, missing proof, waiting approvals, and naming drift |
| `starlight-weekly-portfolio-ops-review` | Friday 15:00 | `#ops`, `#daily-report` | Weekly portfolio review: shipped, stalled, domain/repo movement, content, approvals, channel hygiene |
| `starlight-weekly-blessing-ledger` | Sunday 09:00 | Durable repo ledger | Private weekly estate ledger and visual constellation |

## Slack Routing Rules

| Work Type | Channel Of Record | Proof Required |
| --- | --- | --- |
| Daily executive state | `#daily-report` | Top three outcomes, blockers, decisions, next queue |
| Portfolio decisions | `#ops` | Decision label, owner, due date, proof link |
| Work intake | `#work-queue` | Brand/unit, outcome, owner, approval gate, proof required |
| Active execution | `#execution-room` | Assigned owner/agent, stop condition, proof reply |
| Runtime and Hermes | `#hermes-agent` | Profile/gateway/kanban/cron status and activation proof |
| Repo, PR, deploy risk | `#repo-command` | Repo, branch/PR, command run, risk class, next command |
| Content recording prep | `#content-film-prep` | Hook, three beats, CTA, B-roll/assets, claim risk |
| LinkedIn/Instagram carousels | `#social-carousels` | Brief, design/taste docs, deck, preview, post copy, QA score, approval route |
| Social planning | `#social-command` | Platform route, variants, asset status, approval plan |
| Social approval | `#social-approvals` | Final copy/media, platform, claim risk, AI disclosure, explicit approval |
| Platform adaptation | `#social-*` | Platform-specific variant and reuse notes |
| Brand decisions | `#brand-*` | Brand-specific decision, owner/profile, proof link |

## Hard Gates

Agents may research, inspect, summarize, draft, test, generate reports, prepare
branches, and prepare approval packets.

Agents must not publish, schedule social posts, merge, deploy production, spend,
change access, transfer domains, alter DNS, message customers or partners, or
start Hermes gateways without explicit approval.

## Domain And Website Daily Signal

Each daily domain/deployment digest should answer:

- Which domains and subdomains are known?
- Which repo owns each site?
- What changed since the previous scan?
- Did GitHub or Vercel show fresh activity?
- Which links should Frank open to inspect?
- Which domain or deployment risks need a decision?
- What is safe to do next?

Minimum output fields:

| Field | Meaning |
| --- | --- |
| Brand | FrankX, Arcanea, Starlight, GenCreator, AI CoE, Income, Reality, Anime, Mind, Tooling |
| Domain | Primary domain or subdomain |
| Repo | GitHub/local repo that owns the surface |
| Surface | Production, preview, docs, app, landing page, or registry |
| Last signal | Latest meaningful GitHub, local, Vercel, or registry signal |
| Risk | Green, Yellow, Red |
| Inspect link | Direct domain, preview, PR, deployment, or repo link |
| Approval gate | Where a human approves next action |

## Content And Image Production Loop

The daily content automation should create a small batch, not a flood:

1. 1 to 3 recording-ready briefs.
2. 2 to 5 image/carousel concepts.
3. Platform variants for LinkedIn, Instagram, YouTube, X/Threads, TikTok, and syndication only when useful.
4. Claim-risk labels and AI disclosure notes.
5. A final approval packet route.

Use generated images for covers, mood, scenes, architecture metaphors, and
premium visual concepts. Use deterministic SVG, HTML, Figma, Canva, or slides
for final text-heavy carousels where exact wording matters.

## Carousel Factory Learning Inputs

The daily carousel factory should not start from a blank prompt. Before creating
or revising a candidate, it should read:

1. Official AI lab/product sources when topical claims are involved.
2. `#social-approvals` decisions and Frank edit notes.
3. `#design-intelligence` QA findings and pack `evidence.json` scores.
4. Prior carousel/post performance when a human-published post has metrics.
5. Brand/lane foundations under `docs/social-media-team-os/`.
6. Brand packs from `starlight-design-intelligence`.

Output should include a learning note: what was learned, what was cut, what was
carried forward, and which approval gate remains.

## Channel Hygiene Standard

A channel is healthy only if it has:

- owner
- purpose
- agent/profile owner where relevant
- channel of record or support role
- approval gate
- proof format
- latest live proof within the expected cadence

If a channel repeatedly has no proof traffic, the weekly review should recommend
one of four actions: keep, merge, park, or archive.

## Next Manual Validation

Before adding n8n, Temporal, social publisher, or live Hermes gateways:

1. Confirm the first daily executive digest appears in `#daily-report`.
2. Confirm domain/deployment digest appears in `#repo-command`.
3. Confirm repo risk sweep does not mutate files.
4. Confirm content/image prep creates useful approval packets but does not publish.
5. Confirm proof monitor catches stale rooms without spamming.
6. Run one manual work item from `#work-queue` to `#execution-room` to `Proof`.
