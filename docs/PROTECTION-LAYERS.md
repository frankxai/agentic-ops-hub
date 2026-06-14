# Protection Layers — Humans, Agents, and Wealth

> Defense-in-depth for an ecosystem where agents touch money. Each layer assumes the one above it can fail. Money and irreversibility are never one mistake away.

Last updated: 2026-06-14.

---

## The principle

> **An autonomous agent should never be one bad token away from losing money, leaking a human's wealth, or taking an irreversible action.**

Every protection below exists so that a single compromised prompt, drifted instruction, or hallucinated tool call hits a wall — not a bank account.

---

## The seven layers

```
  ┌─────────────────────────────────────────────────────────────┐
  │ L7  HUMAN GATE        irreversible + money = human approval   │  ← last line
  ├─────────────────────────────────────────────────────────────┤
  │ L6  RED/BLUE          continuous adversarial testing          │
  ├─────────────────────────────────────────────────────────────┤
  │ L5  PAYMENT GOVERNANCE mandate · spend-cap · audit · consensus│
  ├─────────────────────────────────────────────────────────────┤
  │ L4  ESCALATION         queen→founder→human contract           │
  ├─────────────────────────────────────────────────────────────┤
  │ L3  AGENT IAM          per-tool, per-directory scoping         │
  ├─────────────────────────────────────────────────────────────┤
  │ L2  CIRCUIT BREAKER    failure tracking → warn/restrict/block │
  ├─────────────────────────────────────────────────────────────┤
  │ L1  AUDIT TRAIL        append-only log of every action        │  ← foundation
  └─────────────────────────────────────────────────────────────┘
```

### L1 — Audit trail (foundation)
Append-only JSONL of every significant action, across the whole stack.
- **Source:** ACOS audit-trail hook; payments echo to `record_audit_entry` (Payments MCP).
- **Invariant:** no money action exists without a prior audit entry. If the log write fails, the action fails.

### L2 — Circuit breaker
Tracks failures per file/agent. 3 → warn, 5 → restrict, 8 → block.
- **Source:** ACOS circuit breaker. Applied to income agents this wave.
- **Protects:** a looping or drifting agent from compounding damage.

### L3 — Agent IAM
Per-tool, per-directory scoping. The 6 ACOS IAM profiles, applied to the agent stack:
- Content workers can't run bash. Auditors are read-only. **Only the Payments Queen can call the Payments MCP, and only verify-only tools — never a "transfer" tool, because none exists.**
- Workers get **append-only** vault access; queens get read-write within their stream.

### L4 — Escalation contract
The queen→founder→human ladder from `AGENT-STACK.md`. Structural, not discretionary: crossing a cap, a stream boundary, or into irreversibility forces escalation.

### L5 — Payment governance
The control surface that makes money safe. Enforced by the Payments MCP (fail-closed):
- **Mandate verification (AP2):** every charge must carry a cryptographically signed mandate proving the human authorized *this* purchase for *this* amount. No mandate → reject.
- **Spend caps:** per-transaction, per-day, per-stream. Over cap → escalate, never auto-approve.
- **Audit entry:** every settlement writes to L1 first.
- **Multi-agent consensus (Byzantine):** high-value or cross-stream payments require agreement from independent verifier agents (`agentic-payments` pattern) — no single agent authorizes large money.

### L6 — Red/blue
Continuous adversarial testing (`starlight-evals` Income & Payments Safety lane). Red team forges mandates, removes disclosures, tampers links, attempts exfiltration; blue team must hold. See `RED-BLUE-CHARTER.md`.

### L7 — Human gate (last line)
The non-negotiable hard-stops (from FrankX doctrine): moving funds **outside a pre-authorized, capped merchant settlement** (treasury moves, arbitrary transfers), sending blasts, rotating keys, deleting/renaming live URLs, force-pushing production. **Always human** — and fund movement is additionally multi-sig / HSM-gated on the signature itself.

A *capped, mandate-verified merchant settlement* may be agent-signed per L5 (using a single-use, scope-limited credential released for that one settlement). Everything larger, novel, or treasury-level is human. Agents prepare; humans commit.

---

## Protecting the three subjects

### Protecting humans
- Their **wealth data** is Tier 1/2 confidential — stays in private vaults (`second-brain-os`, SIS), never in public repos, never in `.mcp.json`, never in a prompt sent to a third-party model.
- Their **money** can only move through L5 governance + L7 human gate.
- Their **identity/voice** is non-licensable (SIP sovereignty clause); clones are forbidden, patterns are forkable.

### Protecting agents
- From **drift:** SIS identity-drift detection + circuit breaker.
- From **injection:** red-team probes + input sanitization at every untrusted boundary (affiliate catalogs, web content, PR comments).
- From **scope creep:** Agent IAM + self-modify gate (config snapshot; auto-revert if intelligence score drops >5).

### Protecting wealth (the streams themselves)
- **Diversification:** four independent streams; one compromised stream is contained by IAM + the no-cross-stream-command rule.
- **Reversibility bias:** prefer actions that can be undone; irreversible ones go to L7.
- **Compounding integrity:** the affiliate brain's "honest pick wins" rule — never let a commission override the truth — is itself a protection: trust is the asset, and a single dishonest recommendation is an existential risk to the stream.

---

## Where each layer is implemented

| Layer | Implemented in |
|---|---|
| L1 Audit | `agentic-creator-os` hooks · `payment-intelligence-system/mcp` |
| L2 Circuit breaker | `agentic-creator-os` hooks (applied to income agents) |
| L3 Agent IAM | `agentic-creator-os` IAM profiles |
| L4 Escalation | `agentic-ops-hub/docs/AGENT-STACK.md` · `starlight-swarm` runtime |
| L5 Payment gov | `payment-intelligence-system` (vertical + MCP) |
| L6 Red/blue | `starlight-evals` Income & Payments Safety lane |
| L7 Human gate | doctrine (FrankX `CLAUDE.md` hard-stops) · enforced everywhere |
