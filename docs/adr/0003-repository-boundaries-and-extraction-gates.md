# ADR 0003: Repository boundaries and extraction gates

**Status:** proposed
**Date:** 2026-07-23
**Decision owner:** Starlight Intelligence architecture

## Context

The requested target names—`starlight-signal-intelligence`, `starlight-research-graph`, `starlight-intelligence-agents`, `starlight-intelligence-studio`, and `starlight-intelligence-contracts`—describe useful bounded contexts. Existing portfolio assets already own portions of those responsibilities: SIS, Knowledge Tree, ACOS, agentic-ops, Library OS and brand applications.

Creating every named repository now would recreate the portfolio-sprawl problem the platform is meant to solve.

## Decision

- `agentic-ops` owns portfolio architecture, ADRs, roadmap/coordination and cross-repo receipts.
- SIS owns memory, provenance doctrine, agent governance and public substrate semantics.
- Knowledge Tree lineage owns public knowledge/capability graph canon.
- A new `starlight-signal-intelligence` repository is justified once the Highest Self Signal vertical contract is accepted. It owns operational signals, consent, private evidence, retrieval, workflows and the initial admin surface.
- Contracts, agents and studio begin as internal versioned packages/modules in the signal-service repository.

## Extraction gates

| Candidate repository | Extract only when |
|---|---|
| `starlight-intelligence-contracts` | Two independently deployed consumers require stable semver contracts/SDKs and compatibility tests. |
| `starlight-intelligence-agents` | Workflows have independent release/version cadence, at least two services consume them, and eval fixtures can run standalone. |
| `starlight-intelligence-studio` | Admin UI needs a different deployment, security/access model, or team cadence from the service. |
| `starlight-research-graph` | Public graph/canon ownership cannot remain in Knowledge Tree/SIS without operational coupling; requires explicit ontology governance decision. |

## Consequences

- first implementation is cohesive and deployable without fake package boundaries;
- future splits follow measured operational needs rather than naming preference;
- brand applications retain their own codebases and registers, but do not copy intelligence logic.

## Validation

Before any extraction, record consuming modules, release cadence, API compatibility suite, migration plan, maintainer, permissions, and rollback path in a new ADR.
