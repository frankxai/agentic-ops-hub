---
name: gencreator-product-development
description: "Use when designing or shipping a GenCreator creator workflow, template, cohort experience, marketplace surface, or creator-facing SaaS feature that must prove useful creator leverage."
version: 1.0.0
argument-hint: "[creator segment and product opportunity]"
allowed-tools: "Read, Write, Edit, Search, Web, Browser"
---

# GenCreator Product Development Extension

Use this as a brand extension to `agentic-product-development`. The base lifecycle remains authoritative; this extension centers creator agency, a demonstrable workflow outcome, and marketplace or cohort trust.

## Success condition

A specific creator can reach a valuable first result quickly, understand what the system did versus what they control, and decide whether the workflow is worth returning to or paying for based on evidence rather than inflated promises.

## Required inputs

1. A defined creator segment and context: current workflow, constraints, tools, skill level, and intended outcome.
2. A before-and-after task: what artifact, decision, or published action changes.
3. A source-of-truth statement for templates, prompts, examples, and rights to reuse them.
4. A measurement plan for activation, quality, repeat use, and support burden.
5. A claims register for any income, growth, time-saved, or outcome statement.

Do not use generic "creator" language as a persona. Name the job, starting materials, and finish line. Do not frame generated output as a substitute for creator judgment.

## Brand-specific operating loop

### 1. Define the creator's leverage moment

State the smallest observable improvement:

> When a `[specific creator]` brings `[starting material]`, they can produce or decide `[concrete result]` within `[bounded effort]` while retaining `[human decision]`.

Test the statement with one representative workflow before expanding features or catalog breadth.

### 2. Produce a workflow contract

For every feature, template, or cohort module, write:

| Field | Meaning |
|---|---|
| Starting state | Inputs, permissions, and prerequisite knowledge |
| Creator action | The meaningful choice that remains with the person |
| Agent action | Bounded transformation, research, drafting, or QA work |
| Output | Concrete artifact or decision the creator owns |
| Quality check | How the creator verifies usefulness and accuracy |
| Recovery path | What to do when inputs, output, or tools fail |

A workflow without a clear creator action is automation theater, not creator leverage.

### 3. Run the GenCreator review cell

| Review role | Tests | Required evidence |
|---|---|---|
| GenCreator Product Queen | customer value, scope, and business model coherence | opportunity reframe, thin slice, success metric |
| Creator Workflow Designer | time-to-first-result and control clarity | workflow contract, journey map, task recording |
| Template and Marketplace Steward | reusability, provenance, packaging, and discoverability | template spec, versioning, rights/attribution record |
| Claims and Trust Reviewer | accuracy of outcome, income, and time claims | claims register with evidence or qualifying language |
| Companion Tester | onboarding, error recovery, and human-plus-AI collaboration | scripted test, friction log, changed design |

A role may recommend; a designated human owner approves public financial claims, marketplace policy, pricing changes, and public releases.

### 4. Measure the right evidence

Prioritize outcome evidence over activity counts:

- **Activation:** a creator reaches the defined first result.
- **Quality:** the creator accepts, meaningfully edits, or uses the output.
- **Repeat value:** the creator returns for the same or adjacent job.
- **Trust:** the creator can explain source material, ownership, and limitations.
- **Support burden:** observed confusion, failed handoffs, and manual rescue time.

Instrument only events needed to answer the active hypothesis. Capture consent and minimize personal data.

### 5. Gate release

Release only when all applicable gates pass:

- **Leverage gate:** a representative creator reaches the first result through the documented workflow.
- **Agency gate:** human choices, ownership, and editability are explicit at each consequential step.
- **Template gate:** the artifact has an owner, version, provenance, and a usable example.
- **Trust gate:** claims are sourced, qualified, or removed; no guaranteed earnings or unsupported transformation language.
- **Companion gate:** a newcomer can recover from one common failure without hidden operator intervention.

## Product packet additions

Add these fields to the base product packet:

```yaml
brand: GenCreator
creator_segment: ""
leverage_moment: ""
starting_material: ""
creator_decision: ""
first_result_definition: ""
template_provenance: []
claims_register: []
activation_metric: ""
trust_risks: []
```

## Portability adapter

The workflow needs an experiment ledger, review queue, analytics sink, and decision log; it does not require a particular agent runtime. A Starlight deployment can map those interfaces to a Queen-led swarm and SIS-backed records. Other deployments may use a project tracker, product analytics, and a versioned repository.

## Handoff

Hand the completed packet to the base skill's build, companion-test, and release phases. Preserve the workflow contract, claims register, and gate evidence with the release record.
