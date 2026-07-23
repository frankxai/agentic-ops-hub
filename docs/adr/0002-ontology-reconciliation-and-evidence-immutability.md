# ADR 0002: Reconcile ontology; preserve immutable evidence

**Status:** proposed
**Date:** 2026-07-23
**Decision owner:** Starlight Intelligence architecture

## Context

The portfolio contains overlapping schema experiments:

- SIS PR #44 proposes a governed Knowledge Tree ontology and laws;
- `starlight-knowledge-tree` has graph node/edge schemas for public knowledge and capability progression;
- Research Intelligence Systems defines paper, claim and evidence-table schemas;
- Blue Life Commons proves source, review and sensitivity metadata;
- existing brand schemas hold members, profiles, events, conversations and leads.

Creating another unconstrained “universal” ontology would duplicate active work and make provenance unreliable.

## Decision

1. The operational intelligence ontology maps to, but does not redefine, the Knowledge Tree’s public/canonical terms.
2. Operational objects add governed participant, consent, instrument, evidence, outcome and commercial concepts that do not belong in the public Knowledge Tree.
3. Raw responses, source captures, transcript versions and observed events are immutable append-only records.
4. Corrections, retractions, model outputs, classifications, confidence and contradiction dispositions are new versioned records linked by provenance edges.
5. Inferred signal is always stored separately from stated, behavioral, commercial and outcome signal.

## Consequences

- a report can be reproduced against exact evidence/model/prompt versions;
- a participant correction does not erase the original capture or silently modify a model result;
- deletion workflows erase personal payloads according to policy while retaining only the minimum non-identifying compliance receipt;
- any new cross-system relation/kind requires mapping documentation, a migration, fixture and review.

## Validation

- schema tests reject derived records without input evidence references;
- tests prove a corrected transcript does not overwrite the original;
- consent withdrawal blocks future model jobs and retrieval;
- provenance traversal returns source/evidence/model/prompt lineage for every report assertion.
