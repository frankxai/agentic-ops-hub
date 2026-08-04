# Starlight Media Intelligence Control Plane

Private cross-brand coordination layer for researched signals, content-package approvals, distribution intents, receipts, and tool experiments.

## What is implemented now

This directory contains a local-first, dependency-free **Stage 0** foundation:

- `smis` CLI and Python module for pre-registering experiments and creating provenance-linked draft packages.
- Tamper-evident JSONL receipts with hash links, immutable entity/event IDs, and sequence numbers.
  - Receipts retain entity metadata and payload hashes—not raw editorial content.
  - The verifier blocks stale-hash corruption before new local writes. A writer who controls the store can recompute an unkeyed chain, so filesystem ACLs plus periodic reviewed-Git anchors remain required; this is not an independently signed audit ledger.
- Policy preflight that blocks scheduling and publishing at Stage 0 even if every evidence gate is present. Stage 0 is hard-coded in this slice; there is no constructor, CLI, or metadata switch that can promote it.
- Typed JSON contracts for cost/accounting, approval gates, and tool research.

It has **no OAuth integration, browser automation, provider credential handling, scheduling call, publishing call, or paid-model invocation**. Those are later adapter work behind explicit authorization.

## Boundaries

- **SIS**: durable claims, provenance, and reusable lessons.
- **Brand repositories**: full drafts, calendars, assets, audience data, and brand-specific editorial execution.
- **ACOS**: proven generic workflows only after real use. SMIS references portable ACOS contracts; it does not duplicate ACOS identity, connector configuration, or creator runtime.
- **Token Tracker**: cost measurement only; no editorial body or task prompt is copied there.
- **This directory**: policy, typed queue state, outcomes, experiments, and adapter contracts. No secrets, raw OAuth tokens, invoices, or unrestricted customer analytics.

## First vertical slice

FrankX → GenCreator weekly signal-to-brief bridge:

1. Accept a source-backed AI/creator signal.
2. Record source, freshness, confidence, rights caution, and a content angle.
3. Produce an approval-ready FrankX draft with a GenCreator CTA.
4. Keep the private authoring record in FrankX; the deployed website or social platform owns its published artifact and external receipt.
5. Record only an opaque run ID, outcome class, and cost-class projection here.

## Stage 0 CLI

Run from the repository root with a store **outside Git**:

```bash
export PYTHONPATH=ops/media-intelligence
STORE="$HOME/.starlight/media-intelligence"

python3 -m smis.cli init --store "$STORE"
python3 -m smis.cli experiment \
  --store "$STORE" \
  --id smis-exp-001 \
  --hypothesis "A documented image recipe improves first-pass approval." \
  --brand frankx \
  --metric first_pass_acceptance_rate \
  --guardrail rights_clear \
  --decision-rule "Adopt only when the approved treatment beats the baseline."
python3 -m smis.cli package \
  --store "$STORE" \
  --id smis-cp-001 \
  --brand frankx \
  --thesis "Evidence-first creator tools beat novelty chasing." \
  --source-packet source-creator-radar-001
```

A preflight performs **no external platform side effect**; it only appends a sanitized local receipt. Stage 0 correctly refuses `schedule` and `publish`:

```bash
python3 -m smis.cli preflight \
  --store "$STORE" \
  --mode schedule \
  --evidence-file evidence.json
# {"decision": "blocked", "reason": "autonomy_stage_0_draft_only"}
```

## Operating rules

1. A `PublicationIntent` is immutable after approval. Amendments create a new intent.
2. All publishing writes require policy, account authorization, duplicate check, disclosure/rights status, budget/quota check, and an idempotency key.
3. Platform/scheduler post IDs are secondary references; SMIS IDs are canonical.
4. Scheduler products are adapters. They do not own policy, approvals, source claims, receipts, or credentials.
5. `unknown` is a valid state. Missing commercial/right/security evidence is never treated as permission.
6. Stage 0 is draft-only. No automatic publishing occurs until a verified promotion gate is satisfied.

## Canonical documents

- Strategy: `../../docs/strategic/STARLIGHT-MEDIA-INTELLIGENCE-SYSTEM-2026-07-27.md`
- Current execution program: `EXECUTION-PROGRAM.md`
- Research ledger: `RESEARCH-LEDGER.md`
- Knowledge governance: `KNOWLEDGE-GOVERNANCE.md`
- Ownership graph: `KNOWLEDGE-GRAPH.md` (machine-readable source: `knowledge-graph.json`)
- Manifest: `media-manifest.json`
- Metrics: `metrics-contract.json`
- Source policy: `source-policy.md`
- Tool catalog: `registry/tool-catalog.json`
- Local exploration/review projection: [`studio/CONTENT-STUDIO.md`](studio/CONTENT-STUDIO.md) — saved source cards and original draft packages; no publishing, scheduling, OAuth, or provider calls.
- Temporary swarm contracts: `SWARM-CONTRACTS.md`

## Data handling

Runtime database rows, object-store media, and encrypted connector credentials live outside this Git directory. Git holds sanitized policy, schemas, source links, decision records, and reproducible workflow contracts.
