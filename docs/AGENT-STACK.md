# Agent Stack — Founder, Queens, Workers

> How to configure agents for the three operating roles, and the **escalation contract** that keeps money safe: queens run streams, the founder owns capital, humans hold the final gate.

Last updated: 2026-06-14. Model: **hybrid queens-per-stream** (decided 2026-06-14).

---

## The three tiers

```
                       ┌─────────────────────────────┐
                       │      FOUNDER AGENT          │
                       │  starlight-orchestrator     │
                       │  + /starlight-board gate    │
                       │                             │
                       │  Sets thesis · approves     │
                       │  capital · owns irreversible│
                       └──────────────┬──────────────┘
                                      │ escalation contract
              ┌───────────────┬───────┴───────┬───────────────┐
              ▼               ▼               ▼               ▼
        ┌──────────┐   ┌───────────┐   ┌───────────┐   ┌────────────┐
        │ AFFILIATE│   │ PRODUCTS  │   │  CONTENT  │   │  PAYMENTS  │
        │  QUEEN   │   │  QUEEN    │   │  QUEEN    │   │   QUEEN    │
        └────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬──────┘
             │ mesh          │               │               │
        ┌────┴────┐     ┌────┴────┐     ┌────┴────┐     ┌────┴─────┐
        │ workers │     │ workers │     │ workers │     │ workers  │
        └─────────┘     └─────────┘     └─────────┘     └──────────┘
```

Topology: **queen-led per stream, mesh within a stream.** Each queen runs a hierarchical swarm of workers; workers collaborate peer-to-peer inside their stream; queens do not command across streams — they coordinate through the founder.

---

## Tier 1 — The Founder Agent

**Identity:** reuse `starlight-orchestrator` (SIS) as the seat; decisions pressure-tested by `/starlight-board`.

**Owns:**
- The income thesis (which streams, what gate ladder) — sourced from SIS **Wealth IS** (`/wealth-dpi`, `/wealth-thesis-review`, `/wealth-gate-progress`).
- All **capital allocation** and any **irreversible** action (new payment rail, contract, spend above cap, structural site change).
- Conflict resolution between queens.

**Never:** does the per-stream work. The founder sets direction and holds the gate; queens execute.

---

## Tier 2 — Stream Queens (4)

Each queen reuses the `queen-coordinator` + `hierarchical-coordinator` harness patterns, scoped to one income stream. Each runs a **self-improving loop** and **escalates** per the contract below.

| Queen | Income stream | Workers | Self-improving loop |
|---|---|---|---|
| **Affiliate Queen** | Recurring affiliate revenue (`agenticincome` + spoke) | catalog-auditor · link-binder · disclosure-checker · ranker | audit → join programs → bind links → measure → re-rank |
| **Products Queen** | Digital products, templates, courses | product-architect · packager · pricer · launch-coordinator | gap-scan → build → price → launch → retro |
| **Content Queen** | Traffic → trust → routing | researcher · writer · hook-engineer · distributor | top-queries → draft → gate → publish → learn |
| **Payments Queen** | Authorization + settlement | mandate-verifier · spend-cap-enforcer · settlement-auditor · fraud-sentinel | propose-charge → verify mandate → check cap → settle → audit |

**Queen discipline:** a queen may act autonomously **within its scope and below its caps**. It must escalate the moment an action crosses a stream boundary, exceeds a cap, or becomes irreversible.

---

## Tier 3 — Workers

Reuse `worker-specialist`. A worker does exactly one job, reports progress through shared memory (SIS vault), and **never moves money or publishes** without its queen's gate. Workers are stateless between tasks — all state lives in the vault.

---

## The escalation contract (load-bearing)

This is the safety spine of the hybrid model. **No autonomous money movement. Ever.**

| Action class | Who decides | Gate required |
|---|---|---|
| Worker task within stream (draft, audit, research) | Worker → Queen | Queen review |
| Bind an affiliate link, schedule a post, build a product page | Queen | brand/claims gate (`@integrity-guard`, `@claims-guard`) |
| **Verify** a payment is authorized (AP2 mandate + spend-cap) | Payments Queen | Payments MCP, **verify-only, fail-closed**. The Queen authorizes; it never holds standing rail credentials. |
| **Settle** a *pre-authorized, capped merchant* payment | Payments Queen, agent-signed via x402/ACP | mandate verified + under cap + audit entry; signed with a **single-use, scope-limited credential released per settlement** by the governance layer — never a standing key |
| Spend **above cap**, new rail, new vendor contract | Founder | `/starlight-board` pressure-test + **human approval** |
| Move funds outside a pre-authorized capped settlement (treasury, arbitrary transfer) | Founder | **human approval, always** + multi-sig / HSM on the signature (per FrankX hard-stops) |
| Other irreversible (delete, rename live URL, rotate key, send blast) | Founder | **human approval, always** |

**Reconciling "verify-only" with "settle":** the swarm never holds a standing rail credential (matches `MCP-STRATEGY.md` — income swarm = verify-only). A *capped, pre-authorized merchant* settlement may be agent-signed, but only with a single-use, scope-limited credential the governance layer releases for that one settlement after mandate + cap verification. Everything larger, novel, or treasury-level escalates to the Founder + human gate.

**The standing rule (inherited from `agentic-business-os`):** *agents draft, gate, and commit; humans deploy, post, and send.* Arbitrary or treasury-level money movement and irreversibility are never delegated to autonomy.

---

## How to configure each role

```
Founder    : starlight-orchestrator + /starlight-board + Wealth IS + full MCP stack
             (SIS Vault · Payments · claude-flow · Higgsfield · Slack approvals)
Queen      : queen-coordinator scoped to one stream + that stream's skills
             (Affiliate → agentic-income + affiliate-audit skills; Payments → mandate skill)
             + SIS Vault (rw) + Payments MCP (verify-only) + Slack (escalation channel)
Worker     : worker-specialist + one skill + SIS Vault (append-only) — no payment MCP
```

Runtime that wires this: `starlight-swarm` (L6). Governance substrate: SIS council + `/starlight-board` (L0). Safety enforcement: ACOS hooks + Payments MCP (L1/L5). Continuous attack/defense: `starlight-evals` (L7).
