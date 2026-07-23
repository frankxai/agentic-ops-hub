# Starlight Intelligence Ecosystem Architecture

**Status:** proposed implementation architecture
**Date:** 2026-07-23
**Owner:** Frank / Starlight Intelligence
**Portfolio control plane:** `agentic-ops`
**Scope:** shared audience, research, market, product, content, and personalized-path intelligence across distinct branded surfaces.
**Decision posture:** evidence-led; no production deployment, destructive migration, data export, or public publication is authorized by this document.

> **Purpose.** This is the root-level map for the intelligence ecosystem. It records canonical ownership, boundaries, and the first build sequence so that branded products can compound on one shared substrate without becoming one application or one undifferentiated database.

## Executive decision

Build a bounded operational intelligence service, provisionally named **Starlight Signal Intelligence**, around a Postgres-first evidence model. It will receive governed participant signals, retain immutable raw evidence, create reproducible derived intelligence, and expose scoped APIs to brand applications.

Do **not**:

- create a graph database in phase 1;
- merge surveys, Ask funnels, assessments, routers, and longitudinal pulses into one instrument type;
- make SIS the storage system for participant data;
- make a brand product database the cross-brand source of truth;
- create independent per-brand signal engines;
- extract separate contracts, agents, or studio repositories before a real second deployable consumer proves their boundary.

The correct first production proof is **FrankX — Highest Self Signal**. It is a privacy-bounded, anonymous-first, voice-or-text reflection flow—not a diagnosis—and exercises the entire chain from capture through an internal evidence view.

## What was inspected

| Asset | Evidence observed | Architectural implication |
|---|---|---|
| `Starlight-Intelligence-System` (SIS) | `src/retrieval.ts`, `src/temporal.ts`, `src/contradiction.ts`, `src/dreaming.ts`, MCP tools, JSONL→SQLite FTS5 source-of-truth model, privacy sanitization guidance, retrieval evaluation commands. GitHub production deployment recorded on 2026-07-20. | Canonical sovereign memory, provenance posture, agent governance, and cross-agent retrieval patterns. It is **not** the participant-data service. |
| SIS PR #44, “Knowledge Tree” | Active draft adds `verticals/knowledge-tree/`, governed laws, ontology, graph JSON/schema/validator, research loop, and research corps. Its CI completed successfully on its branch. | It is an active canonical-ontology candidate. New intelligence ontology must map to it and must not replace its public/civilizational taxonomy. |
| `starlight-knowledge-tree` | `packages/graph-schema`, graph utilities, public graph nodes/edges, evidence/progression types. | Reusable public-graph semantics and validator ideas; insufficient as a private operational graph by itself. |
| `research-intelligence-os` and `research-intelligence-systems` | Reusable research contracts, claim/evidence/paper schemas, packs, and evaluation-oriented documentation. | Reuse semantic vocabulary and fixtures selectively; no demonstrated production graph service or operational participant store. |
| `gencreator.ai` | Supabase schema for members, purchases, leads, events; RLS; PostHog client; research and Ask routes. Open PR #4 supplies a tested privacy-bounded quiz/ladder experiment with versioned experiment ID and preview evidence. | Closest user-facing routing/experiment reference. Reuse patterns, not tables, as a cross-brand system. |
| `frankx.ai-vercel-website` | Existing `/assess`, `/assessment`, `/ai-assessment` routes and lead/analytics APIs. The local production checkout is heavily dirty and has active deployments. | FrankX is the first branded surface, but implementation must use a clean branch/worktree and normal production release gates. |
| `Arcanea` | Supabase profile, conversation, message, relationship, creation, and media schemas. Storage permits private audio. Local branch is heavily dirty. | Reuse future auth/media/RLS patterns; Creator Soulprint is config over the shared engine, not an Arcanea-specific intelligence fork. |
| `Blue Life Commons` + `ocean-intelligence-system` | Commons owns source/ethics/review metadata; Ocean system owns connectors, agents, dashboards and explicitly cannot override the commons. | The desired pattern: canonical evidence authority below operational agents and branded surfaces. |
| `agentic-ops` | Control-plane docs, portfolio SoT, registry, ledger, machine/agent doctrine. | Owns this cross-repository architecture map, ADR index, migration coordination, and implementation receipts—not participant data or domain logic. |

## Current-state ownership map

```text
                         agentic-ops
      portfolio registry · ADRs · execution ledger · release gates
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
            SIS         ACOS / AIS         Brand applications
 memory/governance      skills/workflows     FrankX · GenCreator · Arcanea
  provenance posture     capability layer     income · academies · Blue Life
             │                 │                  │
             └──── existing public/experimental graph/research repos ────┘
               Knowledge Tree · Research Intelligence OS · Library OS
```

### Current problems to correct

1. There are multiple useful graph, research, and intelligence experiments but no shared operational participant/evidence authority.
2. Existing schemas are domain-specific (`members`, `profiles`, book records, public artifacts) and cannot safely become a global person/signal model by extension.
3. The public Knowledge Tree and private operational evidence graph solve different jobs; conflating them would either leak governed data or constrain research to public-learning semantics.
4. Production and major local worktrees are dirty; no new platform code should land in those paths by convenience.

## Target-state architecture

```text
                          ┌──────────────────────────┐
                          │        agentic-ops        │
                          │ architecture · ADR · plan │
                          └─────────────┬────────────┘
                                        │
       ┌────────────────────────────────┼────────────────────────────────┐
       │                                │                                │
┌──────▼────────┐              ┌────────▼─────────┐             ┌────────▼─────────┐
│ SIS / KT       │              │ Signal Intelligence│             │ ACOS / AIS       │
│ canonical      │              │ operational service│             │ runnable skills  │
│ memory/ontology│              │ Postgres + vectors │             │ + eval adapters  │
└──────┬────────┘              └───────┬───────────┘             └──────────────────┘
       │                                 │
 public research/canon           scoped APIs + async jobs
       │                                 │
       ├───────────────┬─────────────────┼────────────────────┬───────────────┐
       │               │                 │                    │               │
    FrankX          Starlight          Arcanea            GenCreator     Satellites
 Highest Self     Agentic Leverage   Creator Soulprint   Bottleneck Scan  Income/Academies/
 Signal           Scan                                  + routing         Blue Life
```

### Operational service components

| Component | Responsibility | Boundary |
|---|---|---|
| Journey API | Serves versioned instruments, records session lifecycle, consent and raw answers. | Does not calculate unreviewed personality claims. |
| Evidence store | Immutable raw response, transcript, source, attachment metadata, checksum, retention policy. | No silent mutation; delete workflow is auditable. |
| Intelligence projection | Derived claims, themes, segments, opportunities, summaries, confidence, provenance edges. | Every derivation references input evidence and model/prompt version. |
| Retrieval API | Filtered lexical, vector, and graph-neighborhood retrieval. | Enforces tenant, brand, purpose, consent, and audience policy first. |
| Workflow runner | Explicit idempotent research/extraction/report workflows with retries and human review gates. | No opaque autonomous loop or unobserved write. |
| Internal studio | Review queues, evidence traces, filters, theme/market views, and report inspection. | Private/admin-only; no fabricated charts. |
| Brand SDK/config | Typed client contracts and per-brand journey definitions. | Presentation/scoring configuration, not a copy of the engine. |

## Bounded contexts and repository decisions

| Context | Canonical owner now | Target repository decision | Why |
|---|---|---|---|
| Portfolio ownership, ADRs, migration coordination | `agentic-ops` | Reuse | It is already the cross-repo control plane and document SoT. |
| Memory, durable agent recall, public provenance doctrine | SIS | Reuse | SIS is the established substrate; participant operations do not belong there. |
| Public knowledge taxonomy and public contribution graph | Knowledge Tree lineage / SIS PR #44 | Reconcile, do not duplicate | Existing typed graph and active governance proposal are the correct upstream concern. |
| Operational signals, consent, private evidence, jobs, retrieval | none | Create `starlight-signal-intelligence` when vertical-slice contract is accepted | This is a genuine deployable bounded context with data lifecycle and security needs separate from brands. |
| Workflow catalog, prompts, eval fixtures | initially inside signal service | Extract `starlight-intelligence-agents` only after independent version/release cadence is proven | Avoid a repository before there are reusable consumers. |
| Internal studio | initially inside signal service under `/admin` | Extract `starlight-intelligence-studio` only when its deployment/access cadence differs | Same API/security boundary in phase 1. |
| Shared contracts/SDK | service workspace package, versioned | Extract `starlight-intelligence-contracts` only after two independently deployable consumers need it | A package/repo boundary must follow stable consumption. |
| Brand presentation | FrankX, GenCreator, Arcanea, satellite apps | Reuse per brand | Brand voice, UX and release cycles remain independent. |
| Book-level publication intelligence | `library-os` | Reuse as an ingest/publishing adapter later | Its book schema is not a general evidence graph. |

### Explicit deferrals

- Neo4j, Memgraph, or a managed graph engine.
- A separate contracts repository.
- A separate agents repository.
- A stand-alone studio repository.
- Cross-brand account linking by default.
- Behavioral analytics capture of raw text/audio/transcripts.
- Automated publishing or automated intervention recommendations.
- Psychometric/clinical/medical inference or “scores” presented as diagnosis.

## Canonical ontology v0

### Stable identity and boundary objects

| Object | Role | Core invariants |
|---|---|---|
| `tenant` | Data-isolation root; first implementation may map one-to-one with operating organization. | Every private object belongs to exactly one tenant. |
| `brand` | Branded public/private surface. | Has register, data-purpose policy and journey configurations. |
| `participant` | A person or anonymous participant. | Anonymous-first; only an immutable external reference or explicit merge joins identity. |
| `journey` | A versioned, brand-specific experience. | Declares allowed instrument kinds, report policy and consent requirements. |
| `consent_scope` | Purpose and duration of permission. | Separate grants for research, AI analysis, raw-audio retention, marketing, attributable quotation, aggregate publication. |
| `data_subject_request` | Access, correction, deletion, export, or consent withdrawal request. | State-machine tracked; deletion preserves minimal non-identifying audit receipt. |

### Instrument and evidence objects

| Object | Role | Immutable/versioned rule |
|---|---|---|
| `research_instrument` | Survey, Ask funnel, assessment, product router, or longitudinal pulse definition. | Kind is fixed; versions are immutable after publication. |
| `question` | Versioned prompt and answer contract. | Any semantic/scoring change creates a new version. |
| `response_session` | Participant’s run through an instrument. | Binds journey, anonymous participant, policy and instrument version. |
| `raw_response` | Original answer payload and normalized shape. | Append-only; corrections link to superseded response. |
| `media_asset` | Audio or uploaded evidence metadata. | Object retention separately governed from transcript retention. |
| `transcript` | Server transcription and participant-confirmed text. | Original, corrected, and confirmed variants are distinct; derivation prefers confirmed. |
| `source` | External document, book, paper, article, field note, interview, response collection, or dataset. | URL/identifier + acquisition/provenance metadata retained. |
| `claim` | Atomic, falsifiable assertion. | Text and interpretation are distinct; status and confidence are versioned. |
| `evidence` | Exact excerpt, response span, source passage, or observed event supporting/refuting a claim. | Stores locator, extraction method, hash, and source revision. |
| `contradiction` | Explicit conflicting claim pair/cluster and review disposition. | Never deletes either claim; resolution is a new record. |
| `provenance_edge` | Typed directed relation between objects. | Every derived/compiled relationship has generator and input refs. |

### Intelligence and commercial objects

| Object | Role | Rule |
|---|---|---|
| `entity`, `concept`, `theme` | Named or clustered research objects. | Map to Knowledge Tree semantics where applicable; retain local IDs. |
| `problem`, `desired_outcome`, `fear_consequence`, `existing_alternative`, `exact_phrase`, `job_to_be_done` | Audience/market language and structure. | `exact_phrase` is a governed evidence excerpt, not a free paraphrase. |
| `segment` | Reproducible grouping of declared/observed data. | Segmentation rule/model version and membership confidence are recorded. |
| `product_hypothesis`, `mechanism`, `offer`, `experiment` | Decision objects connecting evidence to action. | Evidence-backed and confidence-scored; no inferred revenue treated as fact. |
| `content_hypothesis`, `published_asset` | Content opportunity and release trace. | Published claims retain citations/provenance links. |
| `conversion_event`, `outcome` | Commercial and achieved results. | Distinct from stated/inferred signals; must have source system/event receipt. |
| `report` | Private reflective or operator report. | Includes model/prompt, evidence citations, uncertainty, policy disclaimer, and lifecycle. |
| `model_run`, `prompt_version` | Reproducibility/operations. | Input hash, output hash, model/provider, cost/latency, idempotency key, reviewer state. |
| `confidence_score` | Calibrated confidence component(s). | Store method, version, inputs, and limitations—not an unexplained scalar. |

### Signal classes are never collapsed

| Class | Meaning | Examples | Storage policy |
|---|---|---|---|
| `stated` | What someone explicitly said. | “I cannot choose a focus.” | Raw evidence + exact citation. |
| `inferred` | Model/human interpretation. | “May be experiencing prioritization friction.” | Versioned derived record with uncertainty. |
| `behavioral` | What someone did. | Completed journey, opened report, selected a path. | Purpose-limited event; no raw free text in analytics. |
| `commercial` | Transaction/entitlement facts. | Purchased a product, began checkout. | Receipt/source-system reference; access controlled. |
| `outcome` | What changed after intervention. | Self-reported repeat pulse, completed artifact. | Linked to baseline and measurement method; no causal overclaim. |

### Minimum relation vocabulary

`supports`, `refutes`, `contradicts`, `quotes`, `derived_from`, `classified_from`, `about`, `belongs_to`, `mentions`, `causes_or_contributes_to`, `addresses`, `desires`, `uses_alternative`, `belongs_to_segment`, `tests`, `measures`, `recommends`, `published_from`, `converts_to`, `results_in`, `supersedes`, `consented_for`.

The operational vocabulary remains extensible but a new relation requires an ADR, migration, validation fixture, and a documented mapping—or non-mapping—to the Knowledge Tree ontology.

## Event contract v0

All writes enter through an envelope. Event payloads are typed by event name and version.

```ts
type IntelligenceEvent<T> = {
  eventId: string;                 // UUIDv7
  eventName: string;               // e.g. response.submitted
  eventVersion: 1;
  occurredAt: string;              // RFC 3339 UTC
  tenantId: string;
  brandId?: string;
  journeyId?: string;
  participantRef?: string;         // internal opaque ID only
  correlationId: string;
  causationId?: string;
  idempotencyKey: string;
  actor: { kind: 'participant' | 'system' | 'operator' | 'agent'; id?: string };
  consentSnapshotRef?: string;
  dataClass: 'public' | 'internal' | 'personal' | 'sensitive';
  payload: T;
};
```

Initial event families:

- `journey.started`, `journey.completed`, `journey.abandoned`
- `consent.requested`, `consent.granted`, `consent.withdrawn`
- `response.saved`, `response.corrected`, `response.confirmed`
- `media.received`, `media.transcribed`, `media.deleted`
- `signal.extracted`, `claim.proposed`, `claim.reviewed`, `contradiction.detected`
- `segment.proposed`, `segment.reviewed`
- `report.generated`, `report.reviewed`, `report.viewed`
- `experiment.started`, `experiment.decision_recorded`
- `content.hypothesis_created`, `asset.published`
- `conversion.recorded`, `outcome.measured`
- `deletion.requested`, `deletion.completed`

## Data and security model

### Access control

- Enable RLS on every tenant-bearing table.
- Use application roles: `participant`, `brand_operator`, `research_reviewer`, `tenant_admin`, `system_worker`.
- Put every service-role operation behind server-only routes/workers and audit it.
- Require consent and purpose checks *in addition to* RLS before retrieval, model processing, export, or publication.
- Store vendor identifiers only as secondary references; the canonical ID stays local.

### Voice and transcript policy

1. Record/upload audio only after clear capture consent.
2. Transcribe in a server-side workflow.
3. Store transcript state as `raw`, `corrected`, or `confirmed`.
4. Delete original audio as soon as transcription succeeds unless the separate audio-retention scope is active.
5. Run signal extraction only from `confirmed` text where possible; label exceptions.
6. Never export raw audio/transcripts to PostHog or client analytics.

### AI processing policy

- Prompt and model versions are immutable records.
- Every generated report links to explicit supporting evidence and an uncertainty statement.
- High-risk/sensitive categories require a human-review state before operator use or publication.
- External model adapters receive the minimum permitted/redacted payload; secret and regulated classes are blocked by default.
- Retain cost/latency/error telemetry without retaining sensitive prompt text in observability tooling.

## Retrieval and graph decision

### Phase 1 implementation

Use Supabase Postgres with:

- normalized tables for entities, claims, evidence, sources and relationships;
- `pgvector` embeddings for allowed source/evidence content;
- lexical search (`tsvector`) for precise phrase/source retrieval;
- a typed `provenance_edge` table with source/target indexes;
- recursive CTEs for bounded traversals;
- materialized/cached projections for common studio graphs.

### Gate for a dedicated graph engine

Evaluate a graph database only after a production evidence log demonstrates at least one of:

1. repeated multi-hop traversals that cannot meet a defined p95 target after indexed CTEs/caching;
2. graph size/edge volume that makes Postgres maintenance/cost unacceptable;
3. graph-native algorithms required in operator workflows and not viable as batch projections;
4. multiple teams need graph-specific availability/scaling independent of the relational service.

Any proposal must include replayable benchmark fixtures, operational cost comparison, migration/rollback plan, and an ADR.

## Explicit agent workflow contract

Every workflow is a typed, observable job rather than an autonomous loop.

```ts
type AgentRun<I, O> = {
  runId: string;
  workflow: string;
  workflowVersion: string;
  input: I;
  inputEvidenceRefs: string[];
  output?: O;
  outputEvidenceRefs: string[];
  model: { provider: string; name: string; version?: string };
  promptVersion: string;
  idempotencyKey: string;
  status: 'queued' | 'running' | 'retryable_error' | 'needs_review' | 'completed' | 'failed';
  confidence?: { value: number; method: string; version: string; limitations: string[] };
  reviewPolicy: { threshold: number; required: boolean; reason?: string };
  telemetry: { startedAt: string; completedAt?: string; latencyMs?: number; costUsd?: number };
};
```

Required phase-1 workflow catalog:

| Workflow | Output | Human-review trigger |
|---|---|---|
| Source ingestion | normalized source + extraction receipt | source/authenticity ambiguity |
| Entity/concept extraction | proposed entities/concepts + evidence spans | low confidence or new canonical object |
| Claim/evidence | atomic claims with supporting/refuting evidence | contested/high-impact claim |
| Contradiction detection | candidate conflict cluster | any public/decision-bearing claim |
| Audience-language clustering | cluster proposal + exact phrases | low sample, sensitive or unstable cluster |
| Problem/outcome analysis | problem, desired outcome, alternatives, JTBD | inference above threshold or sensitive content |
| Segment discovery | reproducible rule/model + membership refs | marketing/route action |
| Market opportunity | scored opportunity with evidence | pricing/positioning/publish use |
| Product hypothesis | testable hypothesis, mechanism, experiment | roadmap/offer decision |
| Content opportunity | audience demand + sourced claim plan | publication |
| Personalized report | private reflective report | sensitive/high-impact route |
| Trend/pulse | shift estimate with sample/filters | small/biased population |
| Data quality/provenance audit | failed invariants and remediation queue | any publication or executive decision |
| Executive briefing | change-only evidence-backed summary | all recommendations need human owner |

## Visual analytics contract

All charts must declare: filter set, time window, sample size, denominator, data freshness, evidence/provenance scope, and confidence/limitation text.

| Visual | Minimum requirement | Do not show when |
|---|---|---|
| Problem × urgency | observed/stated evidence counts and explicit definitions | sparse sample or inferred-only data without warning |
| Demand × willingness-to-pay | declared or commercial signal provenance distinguished | WTP is inferred without a labelled method |
| Segment similarity | model/version and dimensionality/feature policy | sensitive features or unstable clusters |
| Theme co-occurrence network | edge definition, filters, counts | graph is a fabricated/demo network |
| Desired-outcome hierarchy | source-backed parent/child relations | only a model-generated taxonomy exists |
| Audience-language clusters | exact anonymized phrases and review state | attributable quotes lack consent |
| Competitor positioning | cited observations and timestamp | positions are speculative/unverified |
| Evidence-confidence distribution | method/component breakdown | confidence is an unexplained score |
| Product-opportunity frontier | pain/urgency/WTP/fit/confidence inputs | an axis has no measured/declared basis |
| Content-demand map | demand, evidence, asset linkage | published content has no traceable source |
| Longitudinal shifts | cohort/base period and interval/sample | changed instrument/segment invalidates comparison |
| Marginal plots | model form, controls, feature distribution and uncertainty | causal or significance claims cannot be supported |

## First vertical slice: Highest Self Signal

### Product contract

- **Brand:** FrankX, Professional register.
- **Purpose:** help a participant reflect on declared friction, desired change, assets and next actions; generate a private, non-diagnostic report.
- **Instrument class:** assessment plus router; it is not a research survey or a general Ask funnel.
- **Identity:** anonymous session by default; optional contact capture after report, with distinct marketing consent.
- **Input:** text or voice “ramble”; participant sees and may correct the transcript.
- **Output:** private reflective report, clearly distinguishing stated evidence from interpretations; route recommendation; optional consented aggregate insights for operators.

### Minimum delivery sequence

1. Versioned journey and question configuration.
2. Separate consent component and policy snapshot.
3. Text capture and server-side voice upload/transcription.
4. Transcript correction/confirmation state.
5. Immutable response/evidence write path and retention worker.
6. Model adapter plus extraction job, with prompt/model/cost/latency receipt.
7. Evidence-linked report renderer and participant correction/feedback event.
8. Operator review queue with provenance trace.
9. Internal theme/problem/opportunity view with real filters and sample limits.
10. Test fixtures, RLS/consent tests, deletion workflow test, and preview deployment verification.

### Acceptance criteria

- An anonymous participant can complete text-only capture without account creation.
- Voice asset is deleted after successful transcription when audio retention is not consented.
- A participant can correct text before extraction; default extraction uses confirmed text.
- Every report sentence that contains an interpretation has a visible uncertainty/evidence reference internally.
- A worker retry cannot duplicate a response, report, event, or derived claim.
- Withdrawal/deletion revokes future processing and completes the defined retention workflow.
- PostHog receives only allowed interaction metadata, never raw content or transcript.
- Studio contains no fake charts: every card has query filters/sample/provenance state.

## Migration strategy

1. **Inventory and classify, not import.** Existing `members`, `profiles`, leads, quiz/assessment payloads, content and research documents remain in their current owners.
2. **Create a source registry.** Each connector declares owner, legal basis, fields, consent availability, retention, import mode and delete capability.
3. **Shadow ingest only.** First connectors copy/redact eligible fixtures or newly collected opted-in data; no retrospective bulk transfer.
4. **Map, do not flatten.** Existing IDs become `external_identity_ref` records; local canonical IDs remain operational-service IDs.
5. **Dual-read at the edge only.** Brand applications continue to use their native identity/entitlement data until a specific migration passes reconciliation tests.
6. **Promote only measured reuse.** Extract contracts/agents/studio repositories only after two live consumers show stable shared interfaces.
7. **Deprecate with a 90-day path.** Mark duplicate experiments as `candidate_for_deprecation`, describe replacement/owner, migrate reads, then archive; never delete history.

## Risks and constraints

| Risk | Constraint / mitigation |
|---|---|
| Competing ontologies | SIS Knowledge Tree PR #44 is active; map first, require canonical review for shared kinds/relations. |
| Dirty production worktrees | Use isolated worktrees; never merge/push production from the current dirty checkout. |
| Consent ambiguity | Separate purpose scopes and snapshot them per event; default to least processing. |
| Sensitive inference | No diagnosis; policy routing, human review, evidence trace and participant correction. |
| Analytics leakage | Strict allowlist; no raw text/audio/transcript payloads in PostHog or traces. |
| Premature repo extraction | Workspace packages first; extraction gates are explicit above. |
| Dashboard theater | All views expose sample, filters, evidence and limitations; hide or label insufficient data. |
| Vendor lock-in | Provider adapters below local canonical IDs/data; external IDs are shadow references only. |
| Data deletion vs provenance | Delete/cryptographically erase personal payload; retain minimal non-identifying audit event and aggregate only if permitted. |
| Cross-brand voice leakage | Brand owns presentation; neutral substrate owns data and contracts; cross-brand use follows the existing council/register gate. |

## Prioritized implementation plan

### Phase 0 — reconcile and freeze boundaries

1. Review SIS PR #44 and Knowledge Tree mapping; make no divergent public ontology decision.
2. Create the signal-service repository only after this architecture and the first slice contract are accepted as an implementation baseline.
3. Establish source registry and data classification matrix.
4. Write ADRs and implementation issues with acceptance criteria.

### Phase 1 — foundation in the signal service

1. Supabase migrations: tenant/brand/journey/instrument/consent/session/evidence/provenance/model-run tables.
2. RLS and consent/purpose enforcement library.
3. Event envelope + outbox/idempotency implementation.
4. Storage/transcription policy and retention/deletion workers.
5. Retrieval: lexical + pgvector + explicit edge traversal.
6. Typed model adapter and workflow-run receipt store.
7. Eval fixtures, redaction tests, observability and cost/latency telemetry.

### Phase 2 — Highest Self Signal vertical slice

1. FrankX journey UI in a clean branch.
2. Service integration, transcript confirmation, extraction, report and operator review.
3. Preview-only test deployment and complete security/privacy/UX test matrix.
4. No production rollout until data-processing, legal copy, retention path, analytics allowlist and release review pass.

### Phase 3 — configurable journey engine

Add Starlight Agentic Leverage Scan, Arcanea Creator Soulprint, GenCreator Creator Bottleneck Scan, and Agentic Income Income Architecture Scan as configuration/presentation packages—not cloned systems.

### Phase 4 — compounding intelligence

Add research ingestion, market evidence, content lineage, opportunity ranking, longitudinal pulses and executive briefings once the first journey has real governed data and review feedback.

## Decision record index

- [ADR 0001 — Postgres-first operational graph](docs/adr/0001-postgres-first-operational-graph.md)
- [ADR 0002 — Canonical ontology reconciliation and evidence immutability](docs/adr/0002-ontology-reconciliation-and-evidence-immutability.md)
- [ADR 0003 — Repository boundaries and extraction gates](docs/adr/0003-repository-boundaries-and-extraction-gates.md)

## Verification status

This document is grounded in local repository instructions/state plus GitHub APIs, PR metadata, deployments and workflow evidence observed on 2026-07-23. It is an architecture and implementation baseline only. It does not claim that a shared operational signal service, journey engine, or production data migration already exists.
