# Knowledge Tree ↔ Operational Intelligence Ontology Mapping

**Status:** draft mapping for canonical review
**Date:** 2026-07-23
**Authority boundary:** this document proposes an adapter boundary. It does **not** amend the Knowledge Tree canon, approve SIS PR #44, or authorize private-data publication.

## Purpose

The Starlight Knowledge Tree is the public, governed canon of humanity’s knowledge and capability pathways. The proposed Starlight Signal Intelligence service is a private, consent-bound operational system for participant signals, research evidence, product decisions and reports.

They must interoperate without either becoming the other:

- the **Knowledge Tree** never receives participant data or private operational metadata;
- the **operational service** may reference public canon objects and may propose eligible public contributions;
- private derived intelligence is never promoted merely because it is useful;
- a public Knowledge Tree edge cannot be fabricated from an operational inference.

This mapping was checked against:

1. SIS PR #44, draft `verticals/knowledge-tree/ONTOLOGY.md`, `LAWS.md`, and `data/graph.schema.json`;
2. `frankxai/starlight-knowledge-tree` main ontology and graph-schema package;
3. SIS main `graph-entity`, `graph-edge`, `agent-run`, and evaluation-result schemas;
4. the operational ontology in [`STARLIGHT-INTELLIGENCE-ARCHITECTURE.md`](../../STARLIGHT-INTELLIGENCE-ARCHITECTURE.md).

## Canonical authority model

| Concern | Canonical authority | Permitted direction |
|---|---|---|
| Public knowledge/capability vocabulary, public canon nodes and relationships | SIS Knowledge Tree lineage; PR #44 remains board-gated and draft | Knowledge Tree → operational service reference/ingest |
| Private participant signals, consent, responses, transcripts, identity bindings, reports and outcomes | Starlight Signal Intelligence service | Never direct-publish to Knowledge Tree |
| Public-source research metadata and evidence artifacts | Source owner + public Knowledge Tree after review | Public source → operational service and/or Knowledge Tree |
| Cross-system mapping, promotion receipts, adapter versions | Signal service mapping registry, reviewed with Knowledge Tree owners | Explicit, provenance-carrying links only |
| Portfolio architecture and migration coordination | `agentic-ops` | Coordination only; no data authority |

## Non-negotiable boundary

SIS PR #44 LAW-11 is controlling: the public Tree contains humanity’s knowledge, **never a person’s data**, including purported anonymized derivatives of identifiable health, biometric, genetic, financial, or identity information.

Therefore no following object is a Knowledge Tree node, edge, reference, note, label, alias, summary, or training corpus input without a separate public-source and publication review:

- participant/person identifiers or pseudonymous session IDs;
- raw response text, transcript, audio, attachment metadata, consent records, or behavioral/commercial/outcome events;
- segment membership, private report, model prompt/output, or personal route recommendation;
- quoted audience language unless the original material is independently public and attributable-quotation consent plus legal/research review both pass;
- a private insight summarized as a general public fact.

Aggregate statistics are not automatically safe. A promotion review must prove that the aggregate is non-identifying, consent/permitted-purpose compatible, methodologically sound, and useful as a public canonical contribution.

## Vocabulary comparison

### Knowledge Tree draft core (SIS PR #44)

| Dimension | Value |
|---|---|
| Node kinds | `concept`, `skill`, `practice`, `artifact`, `evidence`, `contribution`, `quest` |
| Relation kinds | `unlocks`, `requires`, `part-of`, `contributes-to` |
| Identity grammar | `<domain-prefix>/<kind>/<slug>`; public IDs permanent after publication |
| Confidence | `established`, `supported`, `contested`, `speculative`, `unknown` |
| History | no deletion; deprecate and preserve ID/history |
| Admission | persistent provenance reference; independent verification; human merge gate |
| Privacy | public canon excludes personal data |

### Operational intelligence core

| Dimension | Value |
|---|---|
| Evidence objects | source, claim, evidence, contradiction, provenance edge, model run, prompt version |
| Signal objects | participant, journey, instrument, question, response, transcript, consent, report |
| Intelligence objects | entity, concept, theme, problem, desired outcome, exact phrase, segment, product/content hypothesis |
| Commercial/outcome objects | offer, experiment, conversion event, outcome |
| Signal classes | stated, inferred, behavioral, commercial, outcome; never collapsed |
| History | immutable raw evidence; append-only corrections/derivations; governed deletion/erasure lifecycle |
| Admission | consent, purpose, RLS, provenance, workflow receipt and applicable human review |
| Privacy | private tenant-bound service; no cross-brand link by default |

## Node/object mapping

**Mapping states:**

- **Direct candidate** — can be promoted to one Knowledge Tree kind after public verification.
- **Conditional projection** — may produce a public projection only after transformation and review; original remains operational.
- **Reference only** — stores a Knowledge Tree ID/reference but is not promoted.
- **No mapping** — intentionally private or outside the public-canon concern.

| Operational object | Mapping state | Knowledge Tree target | Rules |
|---|---|---|---|
| `concept` | Direct candidate | `concept` | Must be a general public concept, not a participant label or an unpublished model abstraction; needs public persistent refs and independent review. |
| `entity` | Conditional projection | usually `concept`; no generic `entity` kind | An entity is metadata in the operational service. Only a public, canonicalizable subject becomes a Tree concept; preserve external identifiers in source references, not as private entity IDs. |
| `source` | Reference only | `refs[]` on `evidence`/`concept`; sometimes `artifact` | A source is provenance input, not a Tree node kind. A public source may anchor a reviewed Tree evidence node. |
| `claim` | Conditional projection | `evidence` or metadata on `concept` | The Tree’s `evidence` is a verified result, not every operational claim. Atomic claims remain operational until independently verified and canon-worthy. |
| `evidence` | Direct candidate, conditional | `evidence` | Only public, reproducible/inspectable evidence with persistent reference and required verification may be promoted. Exact private evidence excerpts never promote. |
| `contradiction` | No direct mapping | none | PR #44’s closed relation set intentionally excludes `contradicts`; preserve conflict analysis in the operational service and use Tree confidence/review only after canon process resolves it. |
| `artifact` / `published_asset` | Conditional projection | `artifact` | A public inspected output can be a Tree artifact. Marketing pages or unpublished drafts are not automatically artifacts. |
| `contribution` | Direct candidate, conditional | `contribution` | Must be licensed/published/citable public value; operational contribution record is not sufficient. |
| `quest` / public research question | Direct candidate, conditional | `quest` | Must be well-posed, unsolved, and have `requires` relations; a business backlog item is not a quest. |
| `skill` / curriculum capability | Direct candidate, conditional | `skill` | Public demonstrable capability only. Individual assessment score or membership never maps. |
| `practice` | Direct candidate, conditional | `practice` | Public/general repeatable practice, not private user behavior. |
| `research_instrument`, `question`, `journey` | No mapping | none | Versioned operational collection/routing machinery. |
| `participant`, anonymous session, identity reference | No mapping | none | Explicitly prohibited by LAW-11. |
| `raw_response`, audio, transcript | No mapping | none | Explicitly prohibited by LAW-11 and consent/retention policy. |
| `exact_audience_phrase` | No mapping by default | none | May only be separately submitted as an attributable public artifact after explicit quotation/publication consent and review. |
| `theme`, `problem`, `desired_outcome`, `fear_consequence`, `existing_alternative`, `JTBD` | Conditional projection | generally `concept` | Generalized, source-backed public knowledge may become a concept. The operational cluster/labels and source responses remain private. |
| `segment` | No mapping | none | A private/reproducible operational grouping; never a public Tree identity category. |
| `product_hypothesis`, `mechanism`, `offer`, `experiment` | No mapping by default | none | Business decision objects. A public reproducible scientific result might produce `evidence` separately; it does not promote the commercial record. |
| `content_hypothesis` | No mapping | none | Planning object. |
| `conversion_event`, commercial event | No mapping | none | Private commercial fact. |
| `outcome` | Conditional projection | `evidence` only | A properly consented, non-identifying, independently verified aggregate outcome may become public evidence. Individual or claimed outcomes do not. |
| `model_run`, `prompt_version`, confidence calculation | Reference only | provenance note / external artifact | Never a Tree ontology kind. A public reproducibility artifact may be cited, but private inputs/outputs stay private. |
| `consent_scope`, deletion request | No mapping | none | Operational governance only. |
| `provenance_edge` | Reference only | Tree `refs[]` / review receipt | The operational edge is richer than the Tree’s four relations and is retained locally. |

## Relation mapping

### Direct mappings

| Operational relation | Knowledge Tree relation | Conditions |
|---|---|---|
| `requires` | `requires` | Direction must remain source prerequisite → target; public canonical objects only. |
| `unlocks` | `unlocks` | Use only when source makes target tractable, not merely correlated. |
| `part-of` | `part-of` | Structural composition, not a loose topical association. |
| `contributes-to` | `contributes-to` | A public source/artefact/evidence advances a public quest or larger program. |

### No direct relation mapping

| Operational relation | Why it remains operational | Safe public alternative |
|---|---|---|
| `supports`, `refutes` | The Tree draft has a closed four-relation vocabulary. Truth support/refutation is carried by `refs`, evidence nodes, confidence and human review, not a new public edge. | Propose reviewed evidence node and appropriate `contributes-to`/metadata only if it passes canon review. |
| `contradicts` | Deliberate exclusion from the PR #44 closed vocabulary; an unresolved conflict must not be flattened. | Keep contradiction record private/research-side; Tree confidence may be `contested` after review. |
| `derived_from`, `classified_from` | Record processing lineage and may expose personal/private inputs. | Tree `refs[]` for public sources only; retain exact lineage privately. |
| `about`, `mentions`, `belongs_to` | Operational retrieval/indexing semantics, not capability/canon relationships. | Use `domainId`, tags or a reviewed concept only. |
| `causes_or_contributes_to`, `addresses`, `desires`, `uses_alternative` | Audience/market/product semantics are not Knowledge Tree canonical relations. | Potential public concept/evidence promotion through separate review. |
| `belongs_to_segment` | Private/personal data. | None. |
| `tests`, `measures` | PR #44’s draft closed relation set lacks these even though the existing public repo’s older schema includes them. | Do not use until the canonical Tree owner explicitly retains/changes its relation vocabulary. |
| `published_from`, `converts_to`, `results_in` | Publication/commercial/outcome lineage is operational and potentially personal. | Cite independently public research/output as a reference when appropriate. |
| `supersedes` | PR #44 requires preserving history but its closed edge vocabulary lacks a successor relation. | Use deprecation metadata/curator record until board decides an explicit successor semantics. |
| `consented_for` | Consent is governed personal data. | None. |

## Identifier and lifecycle policy

| Subject | Operational service | Knowledge Tree |
|---|---|---|
| Internal ID | UUIDv7/opaque internal IDs; never infer meaning from ID | Permanent public `<domain-prefix>/<kind>/<slug>` IDs |
| Cross-system reference | `external_canon_ref` containing Tree ID, adapter version and verification timestamp | No private-service ID in Tree data |
| Version change | raw evidence immutable; derived records append a version/supersession edge | published IDs remain; canon review/deprecation preserves history |
| Delete | personal payload undergoes governed erasure/deletion lifecycle | no personal payload admitted; published public canon follows no-history-deletion law |
| Duplicate | local entity-resolution evidence and review | curator deduplication; aliases/public refs only |

## Confidence mapping

The systems have different confidence jobs. Do not map a numeric model score directly to a Tree confidence label.

| Operational confidence | Tree confidence | Mapping rule |
|---|---|---|
| model confidence / classifier probability | none | Never map automatically; it measures model output uncertainty, not public epistemic status. |
| evidence coverage/quality score | candidate input | Can inform a curator packet only; no automatic Tree label. |
| human-reviewed evidence assessment | `established`, `supported`, `contested`, `speculative`, `unknown` | Curator applies Tree definitions and retains public sources. |
| absence/insufficiency | `unknown` | Default; never imply absence of a private signal supports a public conclusion. |

## Promotion pipeline: private operational insight → public canon proposal

```text
private evidence/derived signal
        │  (never direct copy)
        ▼
eligible public-source research question
        │  public refs + purpose/legal/consent check
        ▼
independent evidence packet + redaction review
        │  adapter validates mapping and relation closure
        ▼
Knowledge Tree proposal (draft only)
        │  independent verifier
        ▼
human/curator merge gate
        │
        ▼
public Tree node/edge with permanent ID and refs
```

### Promotion requirements

A candidate proposal must contain all of:

- public source IDs/URLs appropriate to the Tree’s persistent-reference rule;
- no participant IDs, text, quotes, transcripts, consent details, internal model output or operational IDs;
- independent verifier identity/session and verification record;
- proposed kind from the closed seven-kind set;
- proposed relation only from the closed four-relation set;
- public confidence label with written rationale;
- legal/license review and, if applicable, attributable-quotation permission;
- a human curator/board disposition.

A failure is a **safe refusal**, not a request to loosen the Tree schema.

## Adapter contract v0

The future signal service may emit a `knowledge_tree.proposal_requested` record, but it is not a direct write.

```ts
type KnowledgeTreeProposal = {
  proposalId: string;
  mappingVersion: '0.1';
  sourceService: 'starlight-signal-intelligence';
  candidate: {
    kind: 'concept' | 'skill' | 'practice' | 'artifact' | 'evidence' | 'contribution' | 'quest';
    label: string;
    summary: string;
    domainId: string;
    confidence: 'established' | 'supported' | 'contested' | 'speculative' | 'unknown';
    publicRefs: Array<{ type: 'doi' | 'arxiv' | 'wikidata' | 'orcid' | 'isbn' | 'url'; id: string; note?: string }>;
  };
  proposedEdges: Array<{
    source: string;
    target: string;
    relation: 'unlocks' | 'requires' | 'part-of' | 'contributes-to';
    note?: string;
  }>;
  review: {
    privacyScreen: 'passed' | 'failed';
    legalLicenseScreen: 'passed' | 'failed';
    independentVerifierRef?: string;
    humanMergeRequired: true;
  };
};
```

The adapter must reject every proposal with `privacyScreen !== 'passed'`, `humanMergeRequired !== true`, a non-public reference, an unmapped kind/relation, or source material outside the documented permitted purpose.

## Compatibility fixtures required before implementation

| Fixture | Expected result |
|---|---|
| DOI-backed general scientific result | eligible `evidence` proposal after independent verification. |
| Public, reusable open-source research artifact | candidate `artifact` or `contribution`; requires license/citation review. |
| Anonymous participant transcript | rejected; no Tree payload emitted. |
| De-identified but small segment summary | rejected pending aggregation/privacy review; no automatic promotion. |
| Model-generated market theme with no public sources | rejected; remains private inference. |
| Publicly sourced contradiction cluster | stays operational until human review; cannot emit `contradicts` edge to Tree draft. |
| Personal assessment outcome | rejected; no Tree payload emitted. |
| Public quest with source-backed prerequisites | candidate `quest` plus `requires` edges; needs curator gate. |

## Decisions still requiring canonical owner approval

1. Does PR #44’s four-relation set remain closed when it merges, or should a separate successor/history relation be added to fulfill LAW-6 more explicitly?
2. How should a public contradiction disposition be represented when `contradicts` is intentionally excluded—confidence only, curator notes, evidence metadata, or a new major-version relation?
3. What is the canonical migration direction between the older `starlight-knowledge-tree` 11-kind/10-relation schema and PR #44’s 7-kind/4-relation schema?
4. Who is the named Knowledge Tree curator/board owner for operational-service proposal disposition?
5. Which public aggregate/outcome methodology and privacy threshold is acceptable for submission as public `evidence`?

Until these are answered, the operational service may **read/reference** the published Tree but must not emit write proposals or rely on a direct schema conversion.

## Verification performed

- Confirmed PR #44 is an open **draft** and declares board/explicit Frank acknowledgement as a prerequisite to merging.
- Confirmed PR #44’s draft Tree ontology uses seven node kinds and four relations.
- Confirmed its LAW-11 prohibits identifiable-person data and even anonymized derivatives in the public Tree.
- Confirmed existing `starlight-knowledge-tree` main has an older, wider 11-kind/10-relation schema, including relations that are not in PR #44’s proposed closed vocabulary.
- Confirmed SIS base `graph-edge` requires evidence reference, confidence, actor and timestamp—aligned with the operational provenance requirement, but not a substitute for consent/purpose enforcement.
