# Sovereign AI Control Plane — Orq-Class Operations Without Vendor Authority

**Date:** 2026-07-19  
**Status:** approved architecture brief / overnight execution baseline  
**Scope:** SIS, `starlight-memory`, ACOS, Hermes, Prompt Engine, Starlight Evals, Token Tracker/Planner, and production AI products  
**Decision posture:** local-first, provider-neutral, and evidence-first. Vendors may execute, accelerate, or visualize; Starlight remains authoritative.

---

## Executive recommendation

Do not adopt Orq.ai as the foundation of the estate.

Orq.ai is a capable managed LLMOps product: a multi-model gateway, agent runtime, tracing/observability, experiments/evaluations, managed RAG, and enterprise governance console. Its advantage is **integrated operational packaging**, not ownership of the primitives that differentiate Starlight.

The estate should close the real gap with a thin, composable control plane:

> **SIS owns canonical identity, memory, policy, provenance, and evaluation receipts. A provider-neutral gateway owns request policy and durable trace envelopes. Existing systems render the operational views and execute approved work.**

This is not a rewrite of Orq.ai. It is a small set of contracts and feedback loops that make the existing estate observable, testable, and commercially deployable without surrendering authority.

---

## What was validated

### External reference: Orq.ai (live official product pages)

Orq.ai currently presents a unified product surface for:

- multi-provider AI gateway: model routing, retries, fallbacks, cache, guardrails, budgets, OpenAI-compatible API, and provider abstraction;
- OpenTelemetry-compatible traces, span/trace search, cost and token analytics, privacy/redaction controls, custom metadata, and dashboards;
- online/offline evaluations, evaluator libraries, datasets, human review, feedback loops, and regression experiments;
- agent runtime: tools, MCP connectivity, memory, approvals, multi-step execution, deployments, and tenant identities;
- enterprise administration: RBAC, SSO/SCIM, audit logs, compliance packaging, data residency, and private/VPC/on-prem deployment.

Official references:

- https://orq.ai/platform/features
- https://orq.ai/platform/agent-runtime
- https://orq.ai/platform/evaluation
- https://orq.ai/platform/observability-monitoring
- https://orq.ai/pricing
- https://docs.orq.ai/docs/ai-gateway/get-started/introduction

### Existing estate evidence

| Existing component | Evidence | Strategic implication |
|---|---|---|
| Canonical local-first memory and policy routing | `Starlight-Intelligence-System`, `starlight-memory/src/types.ts`, `starlight-memory/src/router.ts` | Memory IDs, privacy, retention, provenance, and provider shadow references must remain SIS-owned. |
| Multi-harness agent estate | `Starlight-Intelligence-System/AGENTS.md`, `agentic-ops/fleet/` | We already have orchestration, roles, worktree leases, receipts, and machine specialization. Do not replace this with a vendor runtime. |
| Prompt versioning, red-team and eval discipline | `prompt-engine/README.md` | Git/native prompt assets plus promptfoo are the authoritative prompt surface; production telemetry must feed them rather than fork a vendor-only prompt library. |
| Whole-system evaluation | `Starlight-Intelligence-System/tools/proving-ground/`, `starlight-evals/` | The estate evaluates memory, retrieval, harness, datasets, substrate, and models—not only individual calls. Preserve this broader scorecard. |
| Cost/capacity routing | `starlight-token-tracker`, `fleet/TOKEN-PLANNER.md`, `fleet/model-routing.json` | Subscription-aware capacity allocation is a better fit than gateway-only per-token optimization. Gateway economics must augment, not overwrite, the planner. |
| Existing security model | `docs/PROTECTION-LAYERS.md`, `docs/MCP-STRATEGY.md` | Any new control-plane action must keep append-only audit evidence, IAM, circuit breakers, and human gates intact. |

---

## Product boundary

### We own

| Control-plane concern | System of record | Why |
|---|---|---|
| Identity, tenant policy, memory IDs, provenance, privacy class, retention | SIS / `starlight-memory` | It is differentiated, exportable, and must survive a vendor exit. |
| Agent identity, capability, worktree lease, approval ceiling, and action receipt | Agentic Ops + SIS | This governs what the fleet may do—not merely what a model generated. |
| Skills, commands, creator workflows, tool contracts | ACOS | This is product IP and needs portable distributions. |
| Prompt source, version, red-team result and benchmark fixture | Prompt Engine + Git | Reviewable, portable, reproducible, and compatible with CI. |
| Whole-system scorecards and promotion decision | Starlight Proving Ground | A trace dashboard alone cannot decide whether the system is healthy. |
| Subscription/capacity allocation | Token Tracker + Token Planner | The actual estate uses flat plans, local CLI capacity, and outcome receipts. |

### We adopt or allow as adapters

| Capability | Default stance | Rule |
|---|---|---|
| Model providers / hosted inference | adapters | Provider IDs are references; no provider becomes canonical. |
| OpenTelemetry collector / dashboard | adopt or self-host behind our envelope | Raw export is optional and policy-gated; local receipt remains durable. |
| Orq.ai | optional evaluation or enterprise delivery adapter | Never the memory, prompt, policy, or fleet source of truth. |
| Managed enterprise tools | customer-specific adapter | Require export, deletion, tenant isolation, and an explicit data-processing decision. |

---

## Reference architecture

```text
Clients, product apps, Hermes, coding agents, MCP tools
                         |
                         v
             Sovereign Gateway Policy Layer
  route / quota / retry eligibility / privacy / approval / correlation
                         |
          +--------------+--------------+
          |                             |
          v                             v
Provider adapters                 Local trace writer
OpenAI / Anthropic / xAI /         append-only JSONL + SQLite index
Gemini / local / Orq optional      (canonical trace receipt)
          |                             |
          +--------------+--------------+
                         |
                         v
                  SIS control plane
 identity + tenant policy + memory provenance + work receipts + evaluation links
                         |
      +------------------+------------------------+
      |                  |                        |
      v                  v                        v
Prompt Engine       Starlight Evals       Token Tracker / Planner
versions + cases    regression + drift    cost/capacity + outcome routing
```

### Non-negotiable invariants

1. **Every request receives a Starlight-owned `trace_id` before provider dispatch.**
2. **Every trace records the policy decision, prompt version reference, model/provider reference, privacy class, and outcome state.**
3. **Secret and regulated content stays local unless a tenant policy explicitly permits a compliant external route.**
4. **A vendor trace ID is a secondary reference, never the primary receipt.**
5. **Provider failure cannot block the canonical trace or memory receipt.**
6. **Production feedback creates a candidate evaluation datum, not an automatic truth or training record.**
7. **Promotion requires an independent evaluation receipt; a dashboard graph is not acceptance.**
8. **No new per-terminal heavy daemon.** Any collector, cache, or index runs as a bounded shared service or a lightweight local writer.

---

## The first vertical slice: trace → evaluation case

The first implementation is deliberately narrow. It closes the highest-value gap—unified observability connected to quality—without building an agent platform, RAG product, or SaaS dashboard.

### Input

A gateway/client wrapper receives a model call or tool step.

### Canonical receipt

It writes a policy-sanitized `SISAITraceEnvelope` locally:

```ts
interface SISAITraceEnvelope {
  trace_id: string;
  span_id: string;
  parent_span_id?: string;
  occurred_at: string;

  tenant_id: string;
  workspace_id?: string;
  agent_id?: string;
  run_id?: string;

  operation: "model" | "tool" | "retrieval" | "evaluation" | "approval";
  status: "started" | "succeeded" | "failed" | "blocked";
  privacy_class: "public" | "private-shareable" | "private" | "secret" | "regulated";

  policy: {
    route_id?: string;
    provider_allowed: boolean;
    external_export_allowed: boolean;
    retry_allowed: boolean;
    approval_required: boolean;
  };

  invocation?: {
    provider?: string;
    model?: string;
    prompt_ref?: { id: string; version: string; commit?: string };
    tool_ref?: { id: string; version?: string };
    input_digest?: string;
    output_digest?: string;
  };

  usage?: { input_tokens?: number; output_tokens?: number; cached_tokens?: number; cost_usd?: number | null };
  timing?: { started_at: string; finished_at?: string; latency_ms?: number };
  outcome?: { error_class?: string; feedback_ref?: string; evaluation_case_ref?: string };
  provider_shadow_refs: Record<string, { trace_id: string; synced_at?: string; sync_state: "pending" | "synced" | "failed" }>;
  provenance: Array<{ event_id: string; transform: "raw" | "redacted" | "hashed" | "exported" | "evaluated"; at: string }>;
}
```

### Feedback loop

1. A human correction, failed call, policy block, latency breach, or evaluator failure attaches to the trace.
2. A deterministic selector creates a **candidate** Prompt Engine or Starlight Evals case only after privacy and deduplication checks.
3. An evaluator independently scores the candidate against declared criteria.
4. Only a passing evaluation may promote it to a regression fixture, prompt experiment, or routing policy adjustment.

### Explicit non-goals for the first slice

- no visual dashboard;
- no hosted collector;
- no automatic prompt rewrite;
- no automatic model rerouting based solely on one failure;
- no managed RAG/vector store;
- no tenant admin UI;
- no external data export by default.

---

## Delivery roadmap

### P0 — canonical contracts and durable receipts (first 1–2 implementation waves)

| ID | Outcome | Owner repo | Done when |
|---|---|---|---|
| SCP-001 | `SISAITraceEnvelope` and policy result types | `starlight-memory` / SIS | Types compile; fixtures cover parent-child spans, cost unknown, privacy classes, and provider shadow references. |
| SCP-002 | Local append-only trace writer plus bounded SQLite index | SIS | A trace survives provider failure; trace lookup by `trace_id` works; no heavy per-agent process. |
| SCP-003 | Privacy/export gate | `starlight-memory` / SIS | `secret` is local-only; `regulated` defaults local-only; redacted private trace export has an explicit receipt. |
| SCP-004 | Trace-to-evaluation candidate selector | SIS + Starlight Evals | Failure/feedback generates an evaluable candidate with provenance; no automatic promotion. |
| SCP-005 | Prompt/test reference bridge | Prompt Engine | A trace can point to an immutable prompt version and an accepted case can link back to the trace receipt. |

### P1 — policy-aware gateway and operational views

| ID | Outcome | Owner repo | Done when |
|---|---|---|---|
| SCP-101 | Provider-neutral gateway adapter contract | SIS / product runtime | Direct providers and an optional Orq/OpenTelemetry adapter share the same trace and policy shape. |
| SCP-102 | Route policy: model capability, privacy, retry, budget, fallback | Agentic Ops + SIS | A decision is explainable and recorded before dispatch; planner capacity is an input, not overridden. |
| SCP-103 | Compact local control view | Agentic Ops / cockpit | Displays live trace health, policy blocks, cost/capacity, evaluation backlog, and receipt freshness—not raw private prompts. |
| SCP-104 | Evaluation promotion gate | Starlight Evals | Candidate → evaluated → accepted/rejected state is enforceable and appears in a dated scorecard. |

### P2 — enterprise product capability, only when revenue requires it

| ID | Outcome | Gate |
|---|---|---|
| SCP-201 | Tenant quotas and per-identity attribution | Real multi-tenant workload and acceptance criteria. |
| SCP-202 | SSO/SCIM/RBAC/audit export | Paying enterprise requirement; contract and data-processing review. |
| SCP-203 | Self-hosted/OpenTelemetry collector and dashboard | Evidence that local JSONL/SQLite views are insufficient. |
| SCP-204 | Optional Orq.ai adapter | Customer requires its procurement/compliance surface and provider export is proven. |

---

## Evaluation scorecard for any vendor or adapter

A provider becomes an approved adapter only when it is measured against the following table. “Has a feature” is not a passing result.

| Dimension | Required evidence | Blocker |
|---|---|---|
| Canonical authority | Starlight IDs and receipts remain authoritative | Vendor-only identity or trace history. |
| Privacy | Secret/regulated tests prove no unapproved export | Unverifiable payload retention or broad default export. |
| Exportability | Raw trace/eval metadata can be exported and replayed | Dashboard-only history. |
| Observability quality | Trace completeness, latency, errors, cost fields, span nesting | Missing correlation between agent/tool/model steps. |
| Evaluation value | Candidate/feedback to reproducible test case works | A proprietary score cannot be reproduced locally. |
| Operational cost | Cost per verified objective, not only per token | Fees that erase the product margin without reducing operator work. |
| Reliability | Provider outage does not block local receipt or core delivery | Gateway is a single point of failure. |
| Resource profile | No per-agent heavyweight daemon; bounded caches | RAM grows linearly with terminal agents. |
| Enterprise fit | Specific customer requirement and DPA/security validation | “Enterprise-ready” marketing alone. |

---

## Overnight execution rules

1. Work only in dedicated clean worktrees; never mutate the currently dirty SIS, Agentic Ops, production, or main worktrees.
2. Begin each code slice with a failing test and record the RED result.
3. One mutating owner per worktree. A different reviewer verifies the diff and test receipts.
4. Every generated artifact must state `created`, `tested`, `integrated`, `verified`, and `delivered` separately.
5. No deployment, provider credential change, production model routing change, secret export, or vendor subscription purchase without a human decision.
6. Disk is currently above the 50 GB floor but below the 80 GB target; avoid large installs, model downloads, or clone proliferation.

---

## Strategic decision

**Adopt the Orq-class operational patterns; do not adopt Orq authority.**

The estate already owns the differentiated layers: sovereign memory, fleet policy, skills, prompt discipline, and whole-system evaluation. The engineering agenda is to bind those capabilities with a trace/evaluation feedback loop and thin policy-aware gateway—not to replace them with a rented platform.
