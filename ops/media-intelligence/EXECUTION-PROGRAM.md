# SMIS Execution Program

**Purpose:** a current-state program, not an aspirational roadmap.
**Default posture:** move one independently useful seam at a time; use an isolated branch, tests or contract validation, independent review, and a clean merge.

## Verified foundation

| Capability | State | Evidence |
| --- | --- | --- |
| Canonical strategy | Complete | `docs/strategic/STARLIGHT-MEDIA-INTELLIGENCE-SYSTEM-2026-07-27.md` |
| Stage 0 local control plane | Merged | PR #29 merged into `night/2026-07-17-fleet-hygiene` at `4f0a6d8772991fb346526a72e74e6172ef8dad4b` |
| Stage 0 safety | Verified | Hard-coded draft-only runtime; no network, OAuth, browser automation, scheduling, publishing, provider calls, or credential handling |
| Local runtime checks | Verified before merge | 17 focused tests, compilation, receipt-chain and same-ID concurrency tests |
| Daily research pulse | Active | `starlight-media-daily-draft-pulse`, daily 08:30 CEST, draft-only |
| Draft contract enhancement | In review hold | `agent/hermes/smis-draft-contracts`; 25 tests had passed locally, but the independent review request hit provider usage-limit HTTP 429 and must be retried before commit/merge |

## Current program order

```text
1. Finish contract review/merge
2. Build Hook Ledger intake and original-brief contract
3. Run one-month Sandcastles Pro pilot only if its measured inputs fit the contract
4. Build owned Moment Intelligence fixture from one authorized timestamped recording
5. Project durable lessons to SIS and proven generic workflow to ACOS
6. Ship a small GenCreator teaching surface only after repeated operator use
```

## Work packets

### P1 — Draft contracts (active)

**Goal:** validate source packets and draft content packages before any record/approval flow claims readiness.

- Versioned Source Packet and Content Package contracts.
- Fail-closed checks for provenance, rights state, claim mapping, accessibility, source linkage, and schema version.
- Local `validate-draft` command with no receipt, publication intent, network, or provider side effect.
- Exit: repeat independent review after reviewer capacity returns; then commit, PR, CI, and merge.

### P2 — Hook Intelligence Ledger

**Goal:** turn selected external references into original, rights-aware Hook Briefs.

- Input: manual/exported reference with URL, capture time, source/rights state, outlier context, and evidence scope.
- Output: mechanism classification, originality boundary, approved claim constraints, and original brand-specific hook variants.
- Excludes: bulk scraping, copied scripts, copied visuals/audio, scheduling, and publishing.
- Exit: three real research references produce reviewable briefs; at least one is selected for a Frank-owned recording.

### P3 — Owned Moment Intelligence

**Goal:** select valuable moments from a Frank-owned or explicitly authorized timestamped long-form transcript.

- Input: owned media reference + timestamped transcript.
- Output: candidate moments with evidence timestamps, context-completeness explanation, hook options, and human-ranked edit brief.
- Excludes: external creator corpus ingestion, automatic editing, and publication.
- Exit: one source transcript yields a human-reviewed set of candidate clips and one real capture/edit decision.

### P4 — Learning projections

**Goal:** make verified lessons reusable without leaking private operations.

- SMIS → SIS: one-way sanitized learning records with source/event references and privacy class.
- SMIS → ACOS: generic skill/template only after the workflow works at least three times.
- SMIS → Token Tracker: opaque package/run reference plus cost class and utilization fields only.
- Exit: projection fixtures prove that source bodies, raw assets, secrets, and editorial text are absent.

### P5 — Public teaching surface

**Goal:** show the proven method, not sell autonomous posting.

- Owner: `gencreator.ai`.
- Surface: research → brief → package → review → learn method, with sample/public-safe templates.
- Gate: at least three real internal packages, outcome notes, and a reviewed public claim set.

## Permanent stop rules

- No external social writes, OAuth, account changes, paid spend, browser-based publishing, or scheduler connection before an explicit Stage 0 exit decision.
- No copied creator wording, visual identity, audio, or unsupported performance claims.
- No second memory system: SIS remains memory/provenance authority; SMIS remains the media operational control plane.
- No dashboard until weekly operators use the ledger and can name a concrete decision it makes easier.
