# G-Stack Portable Skill Projection

## Decision

Treat G-Stack as a source of tested specialist behaviors, not as a directory to mirror or a runtime dependency. Project the behaviors into small, vendor-neutral `SKILL.md` modules that share evidence and handoff contracts. A deployment that has G-Stack can use its native commands as an implementation; a deployment without it must retain the same decision quality through ordinary tools.

This keeps `agentic-ops-hub` in its L2 configuration role while letting Starlight Queen coordinate work at L6 and SIS retain durable decision evidence at L0.

## Non-goals

- Do not copy local G-Stack files into this public repository.
- Do not make a portable skill depend on a private path, a particular CLI, or a named model.
- Do not turn every G-Stack command into a shallow one-command skill.
- Do not grant a specialist authority to publish, spend, mutate production, or ratify brand canon.

## Portable skill contract

Every projected skill should have the standard frontmatter used by `skills/AGENTS.md` and these body sections:

1. **Decision to make** — the bounded question the specialist resolves.
2. **Required inputs** — facts, constraints, and existing evidence; state what blocks a decision.
3. **Method** — a short, reproducible sequence rather than an opaque persona prompt.
4. **Output schema** — a decision record with recommendation, alternatives, risks, and evidence links.
5. **Gate and escalation** — what the skill may recommend versus what requires an owner approval.
6. **Handoff** — the next specialist and the exact artifacts it receives.
7. **Runtime adapter** — optional mapping to local tools without altering the method.

The portable unit is therefore the **decision-and-evidence contract**, not a command alias.

## Proposed first projection set

The paths below are proposals; they are not created by this change. They are grouped by the existing portable-skill categories and ordered by their contribution to the PD-OS loop.

| Priority | Proposed file | G-Stack behavior absorbed | Decision record produced | PD-OS phase |
|---|---|---|---|---|
| P0 | `skills/orchestration/product-discovery-reframe/SKILL.md` | `office-hours` | customer job, reframed problem, three alternatives, thin slice | Discover |
| P0 | `skills/frameworks/product-spec-evidence/SKILL.md` | `spec` | product packet: facts, assumptions, unknowns, acceptance evidence | Define |
| P0 | `skills/orchestration/multi-discipline-plan-review/SKILL.md` | `plan-ceo-review`, `plan-eng-review`, `plan-design-review`, `plan-devex-review` | converged plan, dissent log, gate decision | Plan |
| P0 | `skills/tools/browser-evidence-qa/SKILL.md` | `browse`, `qa`, `qa-only` | reproducible test script, captures, defects, release recommendation | Test |
| P0 | `skills/frameworks/release-confidence/SKILL.md` | `review`, `ship`, `land-and-deploy`, `canary` | release checklist, verification evidence, rollback owner | Ship |
| P1 | `skills/orchestration/design-taste-review/SKILL.md` | `design-review`, `design-consultation`, `design-html` | taste rubric, visual defects, approved direction | Design |
| P1 | `skills/orchestration/security-risk-review/SKILL.md` | `cso`, `careful`, `guard` | threat/risk register, safe remediation order, escalation | Plan / Build |
| P1 | `skills/context/work-context-continuity/SKILL.md` | `context-save`, `context-restore`, `freeze`, `unfreeze` | compact handoff, working boundary, restore checklist | All phases |
| P1 | `skills/context/learning-retro/SKILL.md` | `retro`, `learn`, `autoplan` | observed outcome, decision update, next experiment | Learn |

## Example: portable multi-review skill

```markdown
---
name: multi-discipline-plan-review
description: "Use when a product or engineering plan needs independent product, engineering, design, and developer-experience review before implementation."
version: 1.0.0
argument-hint: "[plan or product packet]"
allowed-tools: "Read, Search, Write"
---

# Multi-Discipline Plan Review

## Decision to make
Can this thin slice proceed to build without creating a customer, technical, design, or delivery failure that should be resolved now?

## Required inputs
- Product packet with facts, assumptions, unknowns, and success criteria.
- Proposed scope, interfaces, and test strategy.
- Brand constraints and non-negotiable safety boundaries.

## Method
1. Review independently from product, engineering, design, and developer-experience perspectives.
2. Record only material objections: evidence, failure mode, severity, and smallest repair.
3. Reconcile disagreements; preserve unresolved dissent instead of averaging it away.
4. Choose `proceed`, `proceed-with-conditions`, or `reframe`.

## Output schema
- Decision and rationale
- Review findings by discipline
- Required changes and owner
- Deferred risks and expiry/review date
- Evidence links

## Gate and handoff
This skill recommends; the product owner accepts scope and the release owner accepts delivery risk. Hand the decision record and accepted conditions to build and QA.
```

## Runtime adapter policy

Use adapters outside the skill body or in an explicitly optional final section:

| Portable behavior | G-Stack-capable adapter | Generic fallback |
|---|---|---|
| discovery reframe | native `office-hours` workflow | structured interview and product-packet template |
| independent review | native plan-review specialists | separate review prompts or assigned reviewers using the same output schema |
| browser QA | native browse/QA workflow | browser test script, screenshots, and defect ledger |
| release confidence | native review/ship/canary workflow | CI, manual checklist, deployment evidence, and named rollback owner |
| retro | native retro/learn workflow | experiment ledger and versioned decision record |

An adapter must not change the required evidence or bypass a human gate. It should declare `available`, `unavailable`, or `fallback` in its receipt so the Queen can route safely.

## Queen and SIS absorption model

1. **Queen dispatches by decision, not by tool name.** The Product Queen creates a run ID and delegates independent work cells. Each cell receives the same packet version and a bounded question.
2. **Specialists write append-only receipts.** At minimum: `run_id`, `brand`, `skill`, `packet_version`, `recommendation`, `evidence_refs`, `risks`, `handoff`, `adapter_status`, and `timestamp`.
3. **SIS retains durable knowledge.** Promote only accepted decisions, validated evidence, released artifact provenance, and completed experiment outcomes. Keep raw drafts and transient tool chatter outside durable memory.
4. **The Queen resolves conflicts explicitly.** Material disagreement produces a dissent record and either a thin-slice repair or founder/human escalation; it is never silently merged.
5. **Brand packs extend the common loop.** The Arcanea and GenCreator skills in `skills/orchestration/` supply brand-specific inputs and gates while retaining the same receipt shape, so their work remains comparable across brands.

## Adoption sequence

1. Add the five P0 skills with one fixture product packet and expected decision records.
2. Add a lightweight validator that checks portable frontmatter, required sections, and banned machine-specific paths.
3. Add a `templates/decision-receipt.yaml` contract and a `templates/product-packet.yaml` contract.
4. Add dispatch metadata in the Queen runtime that maps a decision type to `native-gstack`, `portable`, or `fallback` execution.
5. Run one Arcanea and one GenCreator thin-slice pilot. Measure whether each gate returns evidence, whether the handoffs are lossless, and whether any specialist module is too broad.
6. Promote P1 only after the pilots show concrete missing decisions; avoid projection for command parity alone.

## Acceptance criteria for this projection

- A skill can run on a machine without G-Stack and still produce the documented decision record.
- A G-Stack-enabled run produces the same required evidence plus adapter status.
- Every cross-specialist handoff identifies the packet version and the next accountable role.
- Queen routing can surface unresolved dissent and required human approvals.
- SIS receives only durable, attributable records rather than undifferentiated session transcripts.
