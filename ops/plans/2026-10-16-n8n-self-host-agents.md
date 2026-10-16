# n8n stays self-hosted, and agents sit beside the queue

Decision, 16 October 2026. The running Railway project `n8n w/workers` stays the automation spine. n8n Cloud is not the next move. The new Agents tab is real on the version now running, and it does not belong on the worker.

Prices below are from the n8n pricing page read on 16 October 2026. Behaviour below is from the current n8n docs for Agents, Assistant, and queue mode, plus the live Railway services checked the same day.

## What is already running

Project `9c413057-9f42-400c-bfc3-d31dde5be598`, region `europe-west4-drams3a`.

| Service | Image and start | Proof |
|---|---|---|
| Primary `9ff2af9d-0f60-4d11-b913-1d788dc9d0a9` | `n8nio/n8n:2.43.7`, `n8n start` | Deploy `2d076fc3-64bd-4496-9a5d-e0f6ebc508cc`. Log `Version: 2.43.7`. |
| Worker `ead9c22b-e7d4-4c86-bfb1-f2006c48f986` | `n8nio/n8n:2.43.7`, `n8n worker`, one replica | Deploy `57e96f3b-2baf-4f22-ac98-4af6a2e6d25a`. Log `Version: 2.43.7`. |
| Postgres | `ghcr.io/railwayapp-templates/postgres-ssl:16` | Left as it was. |
| Redis | `railwayapp/redis` | Left as it was. |

`https://primary-production-ff336.up.railway.app/healthz` and `/healthz/readiness` both returned `{"status":"ok"}` after the worker caught up. Primary and Worker had been `n8nio/n8n:2.36.8` since 28 August 2026. Official stable that day was 2.43.7. Beta was 2.44.3. 3.0 was still the next breaking release, so the pin stopped there.

`EXECUTIONS_MODE=queue`. `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true`. The public API key stored as `N8N_API_KEY` on Primary returned 401, so the live workflow list was not refreshed. The inventory used here is the 2 September 2026 snapshot in `starlight/logs/systems-map/n8n-snapshot.json`: 27 active, 19 inactive.

A scale command during the upgrade briefly aimed the worker at `us-west2`. It was returned to Europe before the image change. One mixed-version warning appeared at 14:06 UTC and did not return after the worker logged 2.43.7 at 14:08 UTC.

The pin is recorded on `agent/grok/n8n-2437-pin` in `frankxai/agentic-ops`, file `railway/platform-manifest.json`. That file is not on `main`. It lives on `agent/hermes/railway-platform-hardening`.

## Why Cloud loses

| Plan | Price, billed annually | Executions | Where it runs | What matters here |
|---|---|---|---|---|
| Community | Software is free | No vendor cap | This Railway project | Already paid for as Primary, Worker, Postgres, Redis |
| Starter | €20/month | 2,500 | n8n Cloud | 5 concurrent runs, 5-minute limit, 1 shared project |
| Pro | €50/month | 10,000 | n8n Cloud | Up to 50 concurrent runs, 40-minute limit, no queue mode |
| Business | €667/month | 40,000 | Self-hosted only | Queue mode, Git, environments. Still our server |
| Enterprise | Sales | Custom | Cloud or self-hosted | Not the current shape |

Cloud Starter and Pro would be a new bill on top of Railway. They would also drop the worker, change every webhook on `primary-production-ff336.up.railway.app`, and put a hard stop on runs. One workflow every five minutes is about 8,600 executions a month by n8n's own example, which already passes Starter. The 2 September snapshot does not prove the crons fire that often. The cap is still the wrong shape for a queue that already offloads work.

Business is the plan that has queue mode, and it is self-hosted. Paying €667 to keep the architecture we already have is the expensive way to stand still.

Cloud does include a managed sandbox. That sandbox is what self-hosted Assistant and the agent knowledge base need. We do not need it for the workflows below. Assistant credits are a Cloud meter. Self-hosted Assistant is bring-your-own-key, and it still wants a sandbox. Skip Assistant until someone is building agents all day in the UI.

## What 2.43.7 actually adds

Use the feature where it is allowed to run.

| Feature | Since | On this spine |
|---|---|---|
| AI Agent node, tools, MCP Client, MCP Server Trigger | Already in 2.36 | Yes. This is the production path |
| Anthropic prompt caching on the chat model node | 2.37, node 1.6, off unless enabled | Yes, opt in on long system prompts |
| Message an Agent node | 2.37 | Same instance only. Useless on the spine until an agent exists there |
| Agents tab, draft and publish, schedules, sub-agents, tool approval | 2.32.3, builder called out in 2.40 | Present in the UI. Do not publish one here |
| Channels: Slack, Telegram, Linear | With the Agents tab | Needs a public `N8N_WEBHOOK_URL` and regular mode |
| Knowledge base | Self-hosted preview | Needs a Daytona sandbox. Cloud includes one |
| n8n Assistant | Preview | Needs `instance-ai` plus a sandbox. Build by hand for now |
| Browser Use for all users | 2.43 | Available if a workflow needs a browser |
| Durable scheduler for Schedule Trigger | Off by default until 2.45 | Leave it off on 2.43.7 |
| Save blocked when a node is deprecated | 2.42 and 2.43 | Open Settings, then Migration Report, before editing an old workflow |
| Queue mode for first-class Agents | Not supported | The docs say to run agents in regular mode. Channels can fail in queue mode |

The AI Agent node and the Agents tab are different products. The node is a step inside a workflow, and the worker can run it. The tab is a separate artifact with its own draft, publish history, channels, and schedules. n8n's current warning is specific: queue mode is not supported for those agents yet.

## The shape

Two planes. Only the first one exists.

```text
Harnesses (Claude, Grok, Queen)
        |  MCP, after the API key works
        v
Spine, queue mode, n8n 2.43.7
  Primary: UI, webhooks, schedules
  Worker: executions, including AI Agent nodes
  Redis queue, Postgres 16
        |
        |  header-auth webhooks, only if the seat exists
        v
Seat, regular mode, not deployed
  one n8n, no worker, own Postgres, own encryption key
  two published agents
  Daytona only if a knowledge file is required
```

The spine keeps side effects. Slack, email, Stripe, and Postiz credentials stay there. A model may draft. A workflow with a human approval node is what sends.

The seat is how first-class Agents get a legal process. It is not created in this change. [agentic-ops#83](https://github.com/frankxai/agentic-ops/issues/83) is an open cut of identified Railway spend. A second always-on n8n plus a second Postgres fights that cut. Build the seat only when a channel or a knowledge base is the requirement, and queue-mode agents are still unsupported.

Do not flip the spine to regular mode to unlock the tab. The worker and `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS` exist so runs leave the UI process. Taking that away to host a preview feature is the wrong trade.

Do not point both processes at the spine database. Two mains on one n8n database fight over migrations, execution rows, and the encryption key. The seat, when it exists, gets its own Postgres and its own `N8N_ENCRYPTION_KEY`. Same image pin. Same region. No Redis. Start command `n8n start`. `EXECUTIONS_MODE` left at the regular default.

## Phase 1, on the spine, no new service

Replace the pile of model schedules with two workflows. The 2 September snapshot shows these active briefs overlapping: Daily AI Standup `dHobUIjq3gcJAVJ0`, AI Strategic Daily Brief `JbIxQmQJCbVOpqCr`, Morning Intelligence Brief `Mo48CtRHOuwB09Rr`, Competitor Intelligence Monitor `vMifyQ7E6OszLR5V`, Weekly Intelligence Swarm `r7Coxxj0EnQeUq7M`, Mega Orchestrator `YYDAv4mZtRdDTtBq`, Dev Briefing `1fkzT8C5Y6MkY5Sb`, YouTube Content Strategist `mtiZHiwpQiRoyz3o`, RSS Content Monitor `KreaIR8oZDVDajvx`, Website Analytics Reporter `USEEbA336lTJrfqX`, SEO Rank Tracker `4io2hOw3sn7QDsDT`, Product Idea Validator `CITXGg3H7pdI5K69`, Product Launch Pipeline `k9TSM94HkxiLJTUw`, Content Repurposer `bJJxH5o7TSY4eJ3W`, Content Atomizer `X5qZYPNayRMspuYX`, Blog Post Generator `vZasSAblJ8k3kgxi`, AI Newsletter Engine `i9xMdF9LTNw643Ys`, Email Nurture Sequencer `kXk1j4t9nE58WQzP`.

1. Fix the API key in the n8n UI. Replace `N8N_API_KEY` on Primary through Railway or Infisical. Do not paste the key into chat. Reconnect the n8n MCP afterwards. The handshake failed on 16 October, and the stored key returned 401.
2. Add `FrankX — Signal pack`. Deterministic nodes only: site, SEO, RSS, and whatever those monitors already fetch. No model. One execution, on a weekday morning schedule.
3. Add `FrankX — Morning desk`. An AI Agent node whose tools are Execute Workflow on the signal pack, plus any single lookup that is still missing. One model call writes the brief. A human approval node gates the send. The send node is the only one with the Slack or email credential. Opt in Anthropic prompt caching if the system prompt is large.
4. Add an MCP Server Trigger on the morning desk, with header auth, so a harness can ask for today's brief without a second product.
5. Run the desk on weekdays for five successes. Then deactivate the overlapping schedules listed above. Do not delete them in the same week.
6. Leave these inactive until someone confirms a live caller: Stripe Purchase Fulfillment `vtjac4qhXmaDU5hQ`, Weekly Newsletter `iiofpKztxKvA13wZ`, Blog Publish to social `RpIpv0LIuFJI3p8H`, AI Architect Newsletter Engine `Efidv5OaPe5uerLP`, X and LinkedIn publisher `ftOUGv4YNPzDk49R`, YouTube cross-publish `w7mi39wXYDv0DzEV`. Social posting stays on Postiz.
7. Keep the global error handler `jgE6zf8y9uSxy9o8` and the system health monitor `XJUVV35i23r0SQR7` as workflows with no model.
8. Before the first save of an old workflow, open Settings, then Migration Report. 2.43 refuses a save that still contains a deprecated node. The "any workflow can call this" caller policy is marked for removal in 3.0.

LiteLLM on `perceptive-curiosity` is the preferred model route when its catalog has a model admitted. The August 2026 wiring map still had that catalog empty. Until a completion works through LiteLLM, the morning desk uses one provider credential created in the n8n UI. Do not put the key in a Set node or a workflow field.

## Phase 2, the seat, only when the tab is the point

Create it when Frank wants a Slack, Telegram, or Linear channel, or a knowledge file the agent can search, and n8n's queue-mode warning is still in the docs.

Service name `n8n-agents`, same Railway project, image `n8nio/n8n:2.43.7`, region `europe-west4-drams3a`, one replica. Own Postgres. No worker and no shared Redis. Public hostname only because channels need `N8N_WEBHOOK_URL`.

Two agents, built by hand in the Agent Builder. No Assistant sandbox.

* **Morning researcher.** Tools: one header-auth call to a new spine webhook `POST /webhook/agent-signals`, which returns the signal pack. Web search stays off until a Brave or SearXNG credential exists. Instructions tell it to draft and not to send.
* **Desk.** Sub-agent: the researcher. Tools: `POST /webhook/agent-deliver` and `POST /webhook/agent-postiz-draft` on the spine. Both tools require approval in the agent. The spine workflows behind those paths are the only senders, and Postiz still stops at a draft.

The seat calls the spine. The spine does not host the agent. Message an Agent cannot cross instances, so a schedule on the seat is the trigger, not a node on the worker.

Daytona is a later switch on the seat only: `N8N_AGENTS_AI_SANDBOX_ENABLED=true` and `N8N_INSTANCE_AI_SANDBOX_PROVIDER=daytona`, plus the Daytona key. Without it, the rest of the agent still runs. The knowledge base does not.

Leave instance context (`114_instance_activity_context`) off. It is still preview.

## What this refuses

* An n8n Cloud workspace for this estate.
* A Business license at €667 to keep a queue we already run.
* Publishing an agent on Primary while `EXECUTIONS_MODE=queue`.
* Sharing `N8N_ENCRYPTION_KEY` or the spine Postgres with a second main.
* A Daytona account, an Assistant key, or a second Railway service in phase 1.
* One agent per old workflow. Two workflows replace the list above. Two agents replace them later, and only on the seat.
* Turning 3.0 on. Read the migration report first. npm installs are removed in that release, which does not affect this Docker pin, but removed nodes will.

## Acceptance

Phase 1 is done when the morning desk has five weekday runs, the overlapping schedules are inactive, the MCP trigger answers a harness with header auth, and the error handler still fires on a forced failure. Phase 2 is done when a published agent on the seat drafts a brief, waits for approval, and the spine delivery workflow is the thing that sends. Health of Primary stays on `/healthz` and `/healthz/readiness`. Worker image stays identical to Primary.
