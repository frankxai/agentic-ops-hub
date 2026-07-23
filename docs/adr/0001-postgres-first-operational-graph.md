# ADR 0001: Postgres-first operational graph

**Status:** proposed
**Date:** 2026-07-23
**Decision owner:** Starlight Intelligence architecture

## Context

The ecosystem needs graph-like retrieval across sources, claims, evidence, entities, concepts, audience signals, products, content and outcomes. Existing assets include SIS’s JSONL/SQLite FTS5 memory substrate and the public Starlight Knowledge Tree’s typed graph schemas. There is no demonstrated production requirement for a separate graph database.

## Decision

The first operational intelligence service will use Supabase Postgres as the primary store:

- normalized relational records for governed business objects;
- `pgvector` for permitted semantic retrieval;
- `tsvector`/Postgres full-text search for lexical and exact-language retrieval;
- explicit typed edge/provenance tables for graph relationships;
- recursive CTEs and cached projections for bounded traversals.

SIS remains the sovereign memory/governance substrate. The public Knowledge Tree remains the public graph/canon lineage. Neither is replaced by this implementation decision.

## Consequences

### Positive

- one transactional system for RLS, consent, deletion, source records, jobs and graph edges;
- lower operational complexity and a straightforward Supabase baseline;
- relational reporting and audit work remain simple;
- embeddings and graph traversal are introduced without duplicating data stores.

### Negative

- complex many-hop graph analytics may need optimized projections;
- graph-engine migration remains a future project if measured requirements justify it.

## Dedicated graph-engine gate

A new graph engine requires benchmark fixtures and evidence of at least one of:

1. production p95 traversal failure after indexed SQL/cache optimization;
2. unacceptable relational edge scale or maintenance cost;
3. required graph-native algorithms unsuitable for batch projections;
4. independently scaled graph service requirements.

The proposal must include an operational cost comparison, import/replay plan, rollback plan and a superseding ADR.

## Validation

- migrations prove relational/edge/retrieval constraints;
- retrieval fixtures test lexical, vector and bounded traversal parity;
- query plans and p95 measurements are retained before considering a graph-engine change.
