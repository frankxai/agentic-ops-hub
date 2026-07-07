# Agentic Organization OS Template

This template turns the Starlight Portfolio OS into a reusable setup for founders, SMBs, creators, universities, and enterprises.

## Operating Loop

```text
Signal -> Decision -> Work -> Proof -> Distribution -> Learning
```

## Required Pieces

| Layer | Purpose |
| --- | --- |
| Slack cockpit | channels, intake, approvals, reports, proof |
| Agent runtime | Hermes profiles or equivalent agents |
| Source of truth | GitHub, docs, Linear, Notion, Drive, CRM |
| Automation | Codex, n8n, Temporal, Workflow Builder |
| Governance | approvals, data boundaries, audit trails |
| Learning loop | weekly review, scoreboards, memory updates |

## Minimal Channel Map

```text
#hq
#daily
#work-queue
#approvals
#content
#sales
#build
#support
#knowledge
```

## Expanded Channel Prefixes

```text
#hq-*       executive command
#ops-*      shared services
#brief-*    recurring reports
#brand-*    permanent brand/business units
#camp-*     temporary campaigns
#prod-*     product execution
#repo-*     load-bearing repos only
#client-*   client-specific delivery
#social-*   social execution and approvals
```

## Agent Profiles

Start with:

```text
orchestrator
ops
research
content
growth
build
guardian
knowledge
```

Scale into brand/client-specific profiles only when volume justifies it.

## Approval Gates

| Action | Approval |
| --- | --- |
| Publish externally | human approval |
| Spend money | business owner |
| Merge/deploy production | build owner + business owner |
| Send customer/partner message | account owner |
| Use private data in public asset | guardian |

## Daily Template

```md
**Daily Brief - YYYY-MM-DD**

**Top outcomes**
- ...

**Signals**
- ...

**Blockers**
- ...

**Approvals needed**
- ...

**Proof**
- ...
```

## Weekly Template

```md
**Weekly Review - YYYY-MM-DD**

**What shipped**
- ...

**What moved the business**
- ...

**What stalled**
- ...

**Decisions**
- ...

**Next week's top 3**
- ...
```

## First 7 Days

1. Map units, workflows, risks, and source-of-truth systems.
2. Create Slack cockpit and onboarding channel.
3. Create agent profiles or role prompts.
4. Create intake and approval forms.
5. Run one real workflow end-to-end.
6. Add proof and weekly review.
7. Package the system as the team's operating manual.

