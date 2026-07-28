# SMIS Knowledge Governance

**Status:** canonical operating rule
**Owner:** `agentic-ops/ops/media-intelligence`
**Scope:** how media intelligence becomes durable, discoverable knowledge without creating a second second-brain.

## The problem

A chat answer, a vendor demo, or a social Reel is not operational knowledge unless it is captured with source, scope, confidence, and a decision. Agents must not reconstruct the same research from chat history or promote one creator claim into policy.

## The simple model

```text
raw evidence → research ledger → operational decision → reusable projection
```

Each layer has one owner and a different privacy/reuse boundary.

| Layer | Canonical location | Purpose | Write rule |
| --- | --- | --- | --- |
| Raw private intake | `Starlight-Intelligence-System/memory/intake/` | Links, captions, exports, screenshots, and unprocessed notes | Immutable, provenance-labeled; never store secrets or unlicensed media blobs |
| Reviewed research and decisions | `agentic-ops/ops/media-intelligence/RESEARCH-LEDGER.md` | What was checked, what it means, and what is still unknown | Update per research decision with source URL, retrieval date, evidence class, and decision state |
| Operational rules and contracts | `agentic-ops/ops/media-intelligence/` | Policies, schemas, queue/receipt semantics, provider posture | Reviewed Git changes only; no raw credentials, transcripts, invoices, or customer analytics |
| Durable reusable learning | SIS vault projection | Sanitized lessons, patterns, and queryable context for agents | One-way projection; cite SMIS record IDs/paths and preserve privacy class |
| Brand authoring, assets, and publication outputs | FrankX / `gencreator.ai` / their production surfaces and platforms / approved object storage | Private editorial bodies and owned captures stay with the brand authoring repository; deployed/public artifacts and platform receipts stay with the production surface or platform | Preserve the authoring-to-production boundary; raw media remains with its approved storage owner |

## Required capture fields

Every research entry that informs a tool, workflow, or publishing decision records:

```yaml
id: stable local identifier
source_url: direct source or artifact path
retrieved_at: ISO-8601 UTC
source_kind: official_docs | official_vendor_page | creator_caption | first_party_observation | original_analysis
evidence_scope: what was actually observed
confidence: high | medium | low
rights_state: reference_only | cleared | unknown
decision: adopt | pilot | watch | reject | research_only
limitations: what the evidence does not establish
```

A creator caption is not a full video transcript. A marketing page is evidence of what the vendor says it offers, not proof of outcome, rights, price permanence, or unattended automation permission.

## Agent retrieval protocol

Before working on media intelligence, an agent reads:

1. `README.md` for Stage 0 boundaries and canonical links.
2. `RESEARCH-LEDGER.md` for current evidence and provider posture.
3. `KNOWLEDGE-GRAPH.md` for ownership and allowed projections.
4. The relevant brand repository instructions before drafting or handling assets.
5. SIS recall for prior distilled lessons when the task needs historical context.

After completing material research, the responsible agent updates the ledger and creates a sanitized SIS projection. Chat is a delivery surface, never the only record.

## Graph rule

The versioned `knowledge-graph.json` is an **operational projection**, not a second memory authority. It maps ownership and handoffs; it does not replace SIS provenance records, brand assets, or runtime state. New graph nodes require a real owner, stable ID, and explicit data boundary.

## Promotion rule

One finding remains a `research_note`. A pattern may become a reusable ACOS skill, SIS lesson, or product teaching material only after at least three independent uses or a documented owner decision with evidence.
