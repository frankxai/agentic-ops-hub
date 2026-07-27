# Starlight Media Intelligence — Temporary Swarm Contracts

**Register:** neutral operations.
**Control-plane owner:** `agentic-ops/ops/media-intelligence/`.
**Rule:** a swarm is a bounded project team, not a permanent set of expensive daemons.

## Daily quality loop

```text
Signal → source packet → editorial thesis → content package → quality/rights gate
       → human approval → adapter preflight → (later: controlled publish) → receipt → learning
```

At Stage 0 the loop ends at **draft** or **dry-run preflight**. No role can schedule, publish, authenticate, spend credits, or grant itself a higher autonomy stage.

## Temporary roles

| Role | Mission | May do | Must not do | Completion / handoff |
|---|---|---|---|---|
| **Starlight Queen** | Own the bounded objective, quality bar, and stop conditions. | Assemble task envelopes; reconcile evidence; select temporary lanes; request human decisions. | Become a second source of truth, bypass a gate, or run permanent background agents. | Close package with decision, evidence IDs, risks, and next owner. |
| **Signal Scout** | Find high-signal opportunities and primary evidence. | Research, capture source packet, label freshness/confidence/reuse caution. | Treat a link as reuse permission; turn unverified claims into editorial facts. | Source packet with claim classes and citation links. |
| **Brand Editor** | Convert an approved thesis into channel-native narrative candidates. | Build a content package and derivative map; apply FrankX/GenCreator register rules. | Publish, overrule rights/facts review, or duplicate a brand identity store. | Draft package plus reviewer questions and source references. |
| **Quality Sentinel** | Independently test facts, rights, register, accessibility, policy readiness, and taste. | Return `READY_FOR_HUMAN`, `REVISE`, or `BLOCKED` with evidence. | Review its own authored package, publish, schedule, or waive any gate. | Review receipt tied to the exact package revision. |
| **Visual / Production Director** | Define recording, b-roll, screenshots, edit, image, and accessibility requirements. | Prepare asset brief, shot list, caption/alt-text requirements, reproducible creative recipe. | Represent AI output as owned/cleared without evidence; spend subscription credits without an approved experiment. | Asset manifest and reviewable production recipe. |
| **Distribution Steward** | Check platform capability, policy, quota, duplicate risk, and idempotency. | Execute a dry-run preflight and record a receipt. | Use browser automation to bypass API/terms; schedule/publish at Stage 0. | `eligible_draft_only` or a specific block reason with remediation owner. |
| **Learning Auditor** | Turn approved/published outcomes into reusable evidence. | Reconcile outcome, human minutes, cost class, failure tags, and decision. | Convert estimates into invoices or retain unscoped analytics in Git. | Experiment decision: adopt, pilot, watch, or reject. |

## Required task envelope

Every lane receives a typed envelope before work begins:

```yaml
id: smis-task-...
objective: one measurable, bounded outcome
brand_id: frankx | gencreator | other registered brand
register: professional | neutral | mythic (only if explicitly applicable)
inputs: [source_packet_ids, package_ids, approved asset IDs]
allowed_tools: [read-only research, local draft generation]
repo_owner: agentic-ops | FrankX | gencreator.ai | ACOS | SIS
write_scope: exact paths or none
acceptance_checks: [evidence, rights, quality, accessibility, policy]
human_gate: none | editorial_approval | connector_authorization | publication_approval
stop_conditions: [rights_unclear, unsupported API, secret exposure, duplicate-risk, budget unknown]
handoff: next owner and required receipt IDs
```

## Promotion gates

| Stage | Authority | Evidence required |
|---|---|---|
| 0 — Draft only | Local SMIS | Source/rights/voice/accessibility/policy checklist; no external action. Synthetic adapter design/research remains non-credentialed. |
| 1 — Assisted manual publishing | Human operator performs every real account action | Prior synthetic validation, scoped secret-storage review, preflight + reconciliation receipt design, rollback/revoke proof, explicit owner decision. |
| 2 — Human-approved real-brand schedule | Explicit publication approval | At least 10 accepted packages, clean incident record, accountable owner, platform/account readiness. |
| 3 — Narrow auto-publish | Founder-approved policy | Reversible evergreen format, fixed content class, budget/quota ceiling, kill switch, audit cadence. |

## Stop and dissolve

The Queen closes a swarm immediately when its acceptance criteria are met, a stop condition fires, or the work begins to overlap an active owner. The closing receipt names the next owner, retained artifacts, unresolved risk, and whether a reusable ACOS skill should be proposed.
