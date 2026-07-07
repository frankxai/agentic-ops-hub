# Hermes Pack Factory - 2026-06-23

Status: tracked Agentic Ops architecture note. Local evidence and full catalog live under `hermes-cockpit/.starlight/strategy/`.

## Thesis

The business opportunity is not another generic agent template library. The defensible product is a repeatable **agent operating pack**: a manifest-driven bundle of Hermes profiles, OpenClaw channel templates, Codex skills, n8n automations, Postiz publishing flows, Railway/Vercel runtime maps, evals, observability, approval gates, and proof receipts.

The product promise should be practical:

- install a small agent team for one business workflow;
- connect it to the tools the buyer already uses;
- keep risky actions human-approved;
- prove time saved, revenue influenced, quality improved, or risk reduced.

## Default Architecture

```text
Human / business request
  -> pack intake
  -> Hermes persistent profile
  -> short-lived worker agents
  -> MCP tools and app APIs
  -> n8n or Temporal workflow
  -> human approval gate
  -> Postiz, CRM, GitHub, Vercel, or client system
  -> proof receipt
  -> Langfuse, evals, cost ledger, and weekly learning loop
```

Rules:

- Git-backed manifests are canonical.
- Hermes owns persistent agent identity, memory, skills, and MCP access.
- OpenClaw is an optional channel gateway and SOUL template surface.
- n8n handles glue, approvals, retries, ETL, and workflow fan-out.
- Temporal is for long-running durable orchestration only when needed.
- Postiz is the social publishing and human review hub.
- Railway is the stateful runtime for workers, queues, data stores, observability, evals, and model gateways.
- Vercel is the public app, preview, and web delivery plane.
- Langfuse plus Starlight evals prove model behavior before a pack is sold as reliable.

## Pack Contract

Every pack should ship the same contract:

```text
pack-name/
  README.md
  pack.yaml
  AGENTS.md
  pricing.md
  onboarding.md
  support.md
  hermes/profiles/*.yaml
  openclaw/agents/*/SOUL.md
  codex/skills/*/SKILL.md
  workflows/n8n/*.json
  integrations/mcp/*.json
  integrations/infisical.required-keys.md
  integrations/postiz.channels.md
  integrations/vercel.project-map.md
  integrations/railway.service-map.md
  evals/graders/*.yaml
  observability/langfuse-tags.md
  runbooks/daily.md
  runbooks/weekly.md
  runbooks/approval-gates.md
  proof/receipt-schema.json
```

Required manifest fields:

- `id`, `name`, `buyer`, `useCase`, `businessPromise`.
- `profiles`, `channels`, `automations`, `tools`, `secrets`.
- `evals`, `observability`, `humanApproval`, `proofMetrics`.
- `pricing`, `rollback`.

Secrets are always key names only. Never store secret values in pack docs.

## First Pack Ladder

1. `content-social-genius`
   - First build because the current Railway estate already has Postiz, n8n, Temporal, Langfuse, LiteLLM candidate, and publishing workflow context.
   - Promise: turn ideas and launches into approved, scheduled, platform-specific content with learning reports.
   - Proof: drafts per hour, approval-to-publish time, posts scheduled, engagement by hook/platform/topic, cost per asset, manual hours saved.

2. `sales-genius`
   - Second build because ROI is direct.
   - Promise: turn ICP, offers, and proof into account research, outreach drafts, meeting prep, proposals, and pipeline insights.
   - Proof: accounts researched, meetings booked, response rate, proposal cycle time, revenue influenced, manual hours saved.

3. `marketing-growth`
   - Campaigns, landing-page experiments, message tests, lead magnets, analytics review.

4. `customer-success`
   - Onboarding, support KB, health scoring, QBR packets, churn-risk triage.

5. `founder-command`
   - Daily and weekly command loop across priorities, repos, infra, money, content, sales, and decisions.

6. `ai-coe`
   - Use-case intake, risk review, eval planning, pilot scorecards, executive reporting.

## Revenue Ladder

Treat these as hypotheses:

- Free blueprint: authority and lead magnet.
- Starter pack: `$97-$297`.
- Pro pack: `$497-$997`.
- Cohort or workshop: `$2,997-$5,997`.
- Done-with-you install: `$7,997-$15,000+`.
- Enterprise or agency install: `$25,000+`.
- Recurring support: `$197-$497/mo`.
- Managed operations retainer: `$2,500-$10,000/mo`.

The highest-value offer is the installed operating system plus measured proof, not the template alone.

## Install Discipline

Use now:

- Railway CLI/MCP and Starlight Railway Estate Operator.
- Starlight Work Ledger.
- GitHub plugin for repo, issue, PR, CI, and release work.
- Vercel plugin for Vercel projects, previews, logs, observability, AI Gateway, and web delivery.

Defer until proof:

- Slack, Notion, Google Drive/Sheets, Gmail, Calendar.
- Checkly, Postman, Kong, Datadog, New Relic.
- Any new paid SaaS, public domain, always-on Railway service, or model gateway.

Every new recurring dependency needs owner, job, existing alternative, cost class, stop condition, success metric, rollback, and review date.

## Railway Dependency

Before scaling live packs, resolve or explicitly defer the Railway top-state gates:

- Failed lowercase Redis in `perceptive-curiosity`.
- Crashed public setup-guide in `perceptive-curiosity`.
- Duplicate Infisical choice.
- Temporal UI exposure.
- LiteLLM canonical-gateway decision.
- Compute and Railway Agent usage alerts.

Evidence:

- `hermes-cockpit/.starlight/railway/railway-top-state-operating-plan-2026-06-23.md`
- `hermes-cockpit/.starlight/strategy/hermes-pack-factory-blueprint-2026-06-23.md`
- `hermes-cockpit/.starlight/strategy/hermes-pack-catalog-2026-06-23.json`

## Next Build

Build `content-social-genius` v0.1:

1. Create the pack folder from the contract.
2. Define Hermes profiles and OpenClaw SOUL templates.
3. Draft n8n intake, approval, Postiz scheduling, and report workflows.
4. Define Langfuse tags and eval rubric.
5. Run one internal pilot for FrankX, Arcanea, or Starlight.
6. Publish a proof receipt with cost, time saved, quality, and output metrics.
