---
name: arcanea-product-development
description: "Use when designing or shipping an Arcanea product, feature, academy experience, story-world surface, or campaign that must protect canon while delivering a premium creator experience."
version: 1.0.0
argument-hint: "[product brief or opportunity]"
allowed-tools: "Read, Write, Edit, Search, Web, Browser"
---

# Arcanea Product Development Extension

Use this as a brand extension to `agentic-product-development`. It does not replace the base lifecycle; it adds the evidence, review roles, and release gates required when a product carries lore, identity, or emotional worldbuilding.

## Success condition

Ship a useful, coherent product slice whose canon-bearing claims are traceable, whose creator-owned material is clearly separated from official canon, and whose visual and narrative choices reinforce the intended emotional experience.

## Required inputs

1. A product brief: audience, customer job, scope, and desired decision or behavior.
2. A canon source list with stable links or excerpts. If none exists, mark every lore claim `unverified`.
3. A brand and visual direction packet: approved motifs, prohibited motifs, asset provenance, and accessibility needs.
4. An evidence ledger distinguishing facts, inferences, assumptions, and open questions.

Do not infer locked canon from names, fan material, or model memory. Do not represent creator-owned additions as official canon.

## Brand-specific operating loop

### 1. Classify the work before ideation

Assign one scope label:

- `canon-bearing`: changes or asserts official lore, named characters, historical events, rules, or symbols.
- `canon-adjacent`: uses the world as a framing device but makes no new official claims.
- `creator-owned`: a participant's original world, character, or learning artifact.

For `canon-bearing` work, attach a claim-to-source table before design begins. For `canon-adjacent` and `creator-owned` work, state the boundary visibly in the product packet.

### 2. Reframe around transformation, not lore volume

Define the audience's emotional job in one sentence: what should they understand, feel, make, or become able to do? Generate three thin-slice options and select the smallest one that delivers that change without expanding canon unnecessarily.

### 3. Run the Arcanea review cell

| Review role | Tests | Required evidence |
|---|---|---|
| Arcanea Product Queen | audience value, scope, and product coherence | reframed opportunity, alternatives, success measure |
| Canon Guardian | claim provenance and boundary labels | claim-to-source table; unresolved-claim list |
| World Experience Designer | emotional arc, interaction, and narrative pacing | journey map and key moments |
| Visual Quality Critic | composition, legibility, asset provenance, and brand fit | visual direction, source links, QA captures |
| Companion Tester | first-use comprehension and human-plus-AI handoff | task script, observed friction, revisions |

A role may recommend; a designated human owner approves canon changes, public claims, and irreversible release actions.

### 4. Build with separation of concerns

Keep these artifacts distinct:

- `canon-claims.md`: only sourced lore claims and their citations.
- `creator-material.md`: original contributions and consent/status.
- `experience-spec.md`: UX, learning, or story experience decisions.
- `evidence-ledger.md`: facts, assumptions, tests, and results.

This separation lets the product evolve without silently converting an experiment into canon.

### 5. Gate release

Release only when all applicable gates pass:

- **Canon gate:** each public lore claim has a source or is removed/rephrased as unverified.
- **Narrative gate:** the opening, choice points, and ending deliver the stated emotional job.
- **Visual gate:** images have provenance, pass legibility/accessibility checks, and contain no unexplained visual claims.
- **Companion gate:** a new user can complete the intended first action; the AI handoff does not obscure user agency.
- **Claims gate:** product and marketing language do not imply official status, outcomes, or guarantees that have not been approved.

## Product packet additions

Add these fields to the base product packet:

```yaml
brand: Arcanea
scope_label: canon-bearing | canon-adjacent | creator-owned
emotional_job: ""
canon_sources: []
unsupported_claims: []
creator_material_boundary: ""
visual_provenance: []
canon_approval: pending | approved | not-required
```

## Portability adapter

The workflow requires a review queue, an evidence store, and a decision log; it does not require a particular runtime. A Starlight deployment can map those interfaces to a Queen-led swarm and SIS-backed records. Other deployments may map them to issue trackers, pull requests, and an append-only project ledger.

## Handoff

Hand the completed packet to the base skill's design, QA, and release phases. Preserve the claim-to-source table and gate results in the release evidence packet.
