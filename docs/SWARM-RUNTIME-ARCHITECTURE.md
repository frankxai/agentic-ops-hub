# Starlight swarm runtime architecture — where agents run, who they are, how they talk

**Date:** 2026-10-13 · **Status:** proposed operating doctrine, composes accepted decisions · **Owner:** CTO General, Queen admission, Frank gates

This document answers one question: for a given workload, where does the agent run (local machine, cloud, a vendor subscription, a managed agent product, or a workflow tool), what identity does it carry, and how does it talk to the other layers and brands. It composes, and does not reopen, the accepted decisions below.

## Accepted inputs (binding)

| Decision | Source | What it fixes |
|---|---|---|
| Durable execution boundary (2026-10-04) | `starlight-swarm/docs/TEAM-RUNTIME-ADR-2026-08-06.md`, private registry `architecture_durable_execution_boundary` | Cloudflare Workflows (+ Agents, Durable Objects) own agent-centric durable state; Vercel Workflows own jobs of one Vercel app. One workflow, one durable orchestrator. Temporal, trigger.dev and n8n are not backbones. Railway hosts replaceable workers only. Queen owns policy and admission. SIS/Postgres is canonical memory and the approval/revocation authority. |
| Subscription lanes (2026-07-17) | `fleet/CLI-MAX-SWARM.md` | Codex Max = implementation; Claude Max = deep backend/TDD/architecture; Gemini Ultra = long-context mapping and review; xAI Heavy via Hermes = Queen orchestration and research. One heavy coding CLI per machine, two across the fleet. |
| Fleet topology | `fleet/REPO-LANES.md`, `fleet/STARLIGHT-SWARM-DRIVER.md` | C940 = always-on control plane (backend, ops, memory, crons, Hermes gateway on Telegram + Slack, file bus). Yoga Book = frontend/innovation companion. |
| Agent tiers and escalation | `docs/AGENT-STACK.md`, `docs/PROTECTION-LAYERS.md` | Founder agent → stream Queens → workers. Queens never command across streams. Money, irreversible actions and capital are human. Seven protection layers L1–L7. |
| MCP own-vs-adopt | `docs/MCP-STRATEGY.md` | Build a server only when it encodes proprietary substrate, is a control surface, and stays small. Otherwise adopt behind the `~~placeholder` connector pattern. |
| Identity and attestation | SIP v1.1.1, `protocol/sign.mjs` (proposed), PIS `verify_mandate` | "Built on SIP" block on artifacts that compose SIP; Ed25519 signed receipts proposed (board REVISE 2026-09-19); AP2-style signed mandates for money authority. |
| Capacity admission | `pp preflight`, `fleet/token_planner.py` | 8,192 MiB local floor; HOLD / bounded / allow per workload. |

## The placement rule

Four questions decide where a workload runs. Answer them in order; the first match wins.

1. **Does it need a human in the loop or local secrets, or does it write a working tree?** → Local, one of the two machines, under the subscription lane for that work type. This is interactive engineering, content authoring, anything that touches a checkout or a private vault.
2. **Does it need durable identity or state that must survive a machine being off?** → Cloudflare Workflows with an Agent/Durable Object per entity (a Queen per stream, a steward per registry row, a mission per Estate pilot). This is the only place a long-running agent *lives*.
3. **Is it a job owned by one Vercel app (a cron, a webhook fan-out, a content pipeline for that site)?** → Vercel Workflows in that app, with Vercel Sandbox for untrusted steps. Never a second orchestrator.
4. **Is it glue between two SaaS tools with no agent judgment?** → A workflow tool (Make, n8n) as an *edge integration*, triggered by and reporting to a durable owner above. Never mission authority, never money, never memory.

Vendor-managed agents (Claude managed agents, Codex Cloud tasks, Jules, Antigravity, Vercel Eve) are **replaceable execution** under rule 1 or 2: they do a bounded task, return a diff or artifact with a receipt, and are admitted by Queen like any worker. They never hold durable identity, memory, or a grant. The 11–12 October Cloud-routing session already runs this way for FrankX (Codex Cloud builds, one local lead integrates).

## Placement by workload

| Workload | Where it runs | Identity it carries | Durable owner | Memory | Human gate |
|---|---|---|---|---|---|
| Interactive engineering (PRs, refactors, TDD) | Local CLI on C940/Book under the matching subscription lane | Harness identity + Git author; receipt = PR with zero-exit evidence | none (Git is the record) | SIS vault on Stop hook | PR review, protected branches |
| Cloud build / review delegation when RAM is HOLD | Codex Cloud, Jules, Claude cloud sessions | Task id + exact base commit; returns diff | the local lead who integrates | none | same as above |
| Stream Queen (affiliate, products, content, payments) | Cloudflare Agent (Durable Object) per stream, policy from Queen class in `starlight-swarm` | SIP agent card + Ed25519 key, scoped grant from Founder | Cloudflare Workflows | SIS/Postgres canonical; DO state is disposable | escalation contract L4; caps L5; L7 human gate |
| Registry steward per S3–S5 entity | Cloudflare Agent, one per registry row, wakes on schedule and on webhooks | agent card bound to the row id | Cloudflare Workflows | writes only its row + receipts | COO signs demotions |
| Estate Factory pilot for a client (Trinity) | Client-namespaced Cloudflare Workflow + Durable Objects in the Starlight account, or the client's own account when the SOW says so | per-client key pair; SIP attestation on every artifact; AP2 mandate for any spend | Cloudflare Workflows | client SIS fork vault | SOW milestones 40/40/20; Frank signs |
| Site crons, newsletter sends, content fan-out | Vercel Workflows inside frankx.ai / gencreator.ai / arcanea.ai | app service identity | Vercel Workflows | app DB | newsletter sends and social posts stay human per FrankX doctrine |
| Untrusted generated code or third-party scripts | Vercel Sandbox or Cloudflare Worker with no secrets | ephemeral | caller | none | none; output is data |
| SaaS glue (CRM ↔ Polar ↔ Slack ↔ Notion) | Make scenarios (connector already present) or n8n | service connection | the Vercel or Cloudflare owner that triggered it | none | none; glue never decides |
| Always-on chat surfaces (Telegram, Slack) | Hermes gateway on C940 now; Cloudflare Agent with WebSocket hibernation when the machine must be allowed to sleep | gateway identity + per-user allowlist | Cloudflare (when migrated) | SIS | channel allowlist, mention-required |
| Payments authority | `payment-intelligence-system` MCP, verify-only, fail closed, hosted beside the durable owner | mandate signer keys | none (stateless verify + ledger) | audit ledger | always; no settlement tool exists |
| Evals and red/blue | GitHub Actions + local harness (`starlight-evals`) | CI identity | none | scorecards in repo | CAIO signs |

## Identity: who an agent is

- **Agent card.** Every durable agent has a registry row and a SIP agent card: id, brand, stream, owner General, capabilities, allowed MCP tools, spend caps, escalation path. The card is the thing another agent reads before talking to it.
- **Keys.** One Ed25519 key pair per durable agent, held by the durable owner (Cloudflare secret) and never by a local CLI. Local CLIs sign with the human's Git identity. Receipts and SIP attestation blocks are signed with the agent key; the proposed `protocol/sign.mjs` graph extension is the format. Human-verifiable claims need the signed receipt, not the block alone.
- **Grants.** Authority is a signed, scoped, expiring grant from the Founder agent (or Frank) to a Queen, and from a Queen to a worker: streams, tools, caps, TTL. Money authority is an AP2 mandate verified by PIS. Revocation lives in SIS/Postgres, which the durable engine must consult; the engine never becomes the authority.
- **Tenancy.** Brand is a namespace on the card and on every memory write. Arcanea, FrankX, GenCreator, Agentic Income and Blue Life never share a Durable Object, a vault namespace, or a key. Cross-brand work goes through A2A, not shared state.

## A2A: how agents talk

Three transports, each with one job.

| Transport | Used for | Rule |
|---|---|---|
| **MCP** | Agent → tool. SIS vaults, PIS, Arcanea 57-tool server, site offer tools, adopted vendor servers | Tools are capabilities, never peers. An MCP call carries the caller's grant id. |
| **A2A (agent-to-agent protocol over HTTPS)** | Agent → agent across streams, brands, machines, clients. Task request, status, artifact, cancel | Discovery by agent card from the registry. Every task carries the SIP attestation and a signed receipt on completion. Queens talk to Queens; workers never cross streams. |
| **File bus + ledger** | Human-readable coordination on the fleet (`fleet/bus/`, `ops/OPS-LEDGER.md`, session files) | The durable-output law: a run leaves a PR, a committed file or a Slack DM. Chat is never the record. |

Telegram and Slack are human channels, not A2A. The anti-thrash rules in the swarm driver stay.

## Connection to layers and brands

```
L7 assurance   starlight-evals · red/blue · estate-guard        → GitHub Actions + local harness
L6 runtime     Queens, stewards, pilots                          → Cloudflare Workflows + Agents/DOs
L5 payments    PIS verify-only MCP · AP2 · x402 · ACP            → hosted beside the durable owner; fail closed
L4 income      income hub, spoke, DPI, offers                    → Vercel apps + Vercel Workflows + one Polar store
L3 products    frankx.ai · arcanea.ai · gencreator.ai · BLC      → Vercel git-deploy; app-owned jobs only
L2 config      agentic-ops (private registry) → agentic-ops-hub  → Git; projection read by every layer
L1 capability  ACOS · skills library · ai-architect · SIS skills → installed per harness; marketplaces
L0 substrate   SIP · SIS vaults · starlight-memory · Postgres    → canonical memory and authority; Supabase/Postgres hosted
```

A brand is a vertical slice through these layers with its own namespace at L0, its own Queen at L6, its own apps at L3, and shared L1/L2/L5/L7. The Estate Factory sells exactly this slice to a client, forked at L0 and L6, consuming the shared layers by version.

## What we do not build

- A second orchestrator, cockpit, bus or scheduler. `CONTROL_PLANE.md` already demoted eight cockpits; `starlight-command-center` is the one operator UI.
- An all-in-one agent platform. Ruflo, Letta, Omnigent and similar stay upstream adapters measured in the lab, per the 2026-08-12 board.
- A hosted memory service. `starlight-memory` runs on the user's keys; SIS/Postgres is the estate's own authority.
- Mission authority in Make or n8n. Glue only.
- A token or on-chain settlement as a backbone. x402/USDC and Story Protocol stay optional behind signed receipts.

## Migration from today

1. **Now (local-first, two machines).** Hermes gateway, file bus, subscription lanes, Cloud delegation when RAM is HOLD. Nothing changes except that every durable thing gets a registry row.
2. **First durable pilot (by 2026-11-27).** One Queen (products stream) and one registry steward as Cloudflare Agents, admitted by the Queen class in `starlight-swarm`, with signed receipts into SIS. This is also the Trinity Estate pilot's runtime proof. The ADR's "fresh transport, health, access, budget, cancellation and named pilot evidence" is the acceptance list.
3. **Then.** Move the always-on chat gateway to a hibernating Cloudflare Agent so C940 may sleep; move site crons into Vercel Workflows per app; retire the Railway/Temporal reference artifacts after a reviewed versioned migration.

Nothing in this document starts a workflow, a worker, a schedule or spend.
