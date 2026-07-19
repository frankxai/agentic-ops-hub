# Sovereign AI Control Plane — Orq.ai Product and Engineering Research Pass

**Date:** 2026-07-19
**Status:** bounded research result; roadmap corrections ready for a focused documentation commit in the dedicated control-plane branch
**Scope:** portable operating patterns only. No Orq account, API key, plan, production route, deployment, or external worktree was changed.

## Executive result

Orq.ai is useful evidence of the *operational package* customers may expect: OpenTelemetry-shaped traces, identity/project/thread correlation, structured review queues, versioned prompts/evaluators, dataset experiments, scoped budgets, and retry/fallback controls. It does **not** change the estate's authority decision.

The durable architecture remains:

> **SIS owns identities, policy, provenance, retention, evaluation receipts, and the primary trace. Providers and dashboards receive policy-approved projections only.**

This pass makes five bounded corrections. They tighten the existing trace-to-eval slice rather than creating a gateway service, a dashboard, an Orq dependency, or an enterprise product surface.

## Method and evidence classes

- **Verified external fact:** directly observed in current first-party Orq documentation or its public GitHub repository metadata on 2026-07-19.
- **Verified local implementation:** a source file exists in a local repository. It is not treated as live integration unless this pass executed its focused tests.
- **Inference/recommendation:** a Starlight design choice drawn from the evidence; it is labeled as such and does not assert an Orq feature is a contract.

The initial `agentic-ops` worktree was clean at `39c80ce624048e614662c754bd85c7818558cdb6`; its upstream branch was in sync before this documentation change. SIS and `starlight-memory` were inspected read-only and were already dirty, so no test or runtime claim is made for either source tree.

## What the external research actually validates

| Area | Verified current Orq material | Portable lesson | Boundary retained by Starlight |
|---|---|---|---|
| Trace topology | Orq documents OpenTelemetry instrumentation, nested multi-agent trace trees, human reviews on spans, and trace filtering by identity/thread.[^1] Its attribute reference specifies tenant/project/identity scope; prompt, dataset, workflow references; thread/session/agent execution; and evaluator version/stage.[^2] | A trace contract needs one correlation family for request, agent, tool, model, session, and thread—not only provider/model fields. | Starlight generates the identifiers and local receipt before dispatch; Orq IDs are optional shadow references. |
| OTLP/export boundary | Orq emits `orq.*` attributes on spans and documents them in trace exports/webhooks.[^2] Its open-source `@orq-ai/evaluatorq` README also supports a custom OTLP endpoint.[^3] | Use an OpenTelemetry/W3C-compatible projection so an exporter does not need an identifier translation layer. | No OTLP collector or vendor exporter becomes required for write/read correctness. |
| Review → dataset → evaluation | Orq's Annotation Queues define typed Human Reviews, bulk queues, API annotations, and write annotations back to source traces; it explicitly frames this as curation of production traces into evaluation datasets.[^4] | Feedback, correction, candidate fixture, evaluator result, and promotion must be distinct states with provenance. | A production annotation is not automatically a training record, regression fixture, or policy change. |
| Prompt/evaluator/experiment lifecycle | Orq prompts are versioned reusable model configurations.[^5] Evaluators have published versions, diffs, restore-as-draft behavior, and environment references; experiments run datasets through variants and record latency, cost, TTFT, evaluator, and human-review results.[^6] | Reference immutable prompt/evaluator versions and commits from the trace; run comparisons on owned datasets. | Prompt Engine + Git remain the prompt authority; Starlight Evals/SIS remain the promotion authority. |
| Gateway reliability and financial policy | Orq documents priority routing rules, scoped budgets, retries with error-code selection/backoff, and ordered fallbacks.[^7] Retry documentation notes that each retry consumes quota.[^8] | Record the pre-dispatch decision, every retry attempt, idempotency state, and terminal result under one trace. | Token Planner remains the fleet's subscription/capacity allocator; request-time routing must not recreate its planning logic. |
| Tenant isolation, privacy, and retention | Orq identity docs use an external ID for per-identity attribution.[^9] Its privacy docs say input-masked PII is still sent to the model while omitted from Orq logs; ZDR-compatible routing is a separate choice.[^10] It documents configured retention and automatic deletion of retained platform data.[^11] | Identity must be opaque/canonical locally; masking in a dashboard is not the same as preventing external provider transmission. Retention/export/delete need receipts. | `secret` stays local; `regulated` defaults local-only; any mirror is an explicit tenant-policy decision. |
| Public OSS surface | `orq-ai/orqkit` is publicly MIT-licensed and has a published `v1.3.2` release; its evaluatorq package contains tracing and result-sending adapters.[^12] The public `orq-python` and `orq-node` repository root listings exposed no root license file or GitHub license classification in this snapshot; their release pages show `v4.11.10`.[^13] | Use their public work as a pattern/reference, not a copied control-plane dependency. | No source is vendored, no SDK installed, and no platform account is required. |

## Current estate evidence and truthful boundary

| Estate component | Evidence inspected | Claim class | Strategic implication |
|---|---|---|---|
| `starlight-memory` policy router | `C:/Users/frank/starlight-memory/src/router.ts` always begins with `local_core`; it blocks `secret` and regulated records without a mirror allowance. | Implemented in current local source; **not live-proven in this pass** because the tree was already dirty/behind. | The trace/export gate must reuse `TenantMemoryPolicy` and route semantics rather than add a parallel privacy switchboard. |
| `starlight-memory` resource model | `src/resources.ts` distinguishes lightweight, shared daemon, remote API, and forbids per-agent instances for heavyweight providers. | Implemented in current local source; not runtime-tested here. | A trace writer/index must be a shared bounded service or local library, never another terminal daemon. |
| SIS source schemas | `Starlight-Intelligence-System/src/memory-provider/types.ts` already has privacy, retention, provenance, shadow-reference, session, and tenant primitives; `packages/core/schemas/eval-result.schema.json` is a minimal eval receipt. | Implemented in current local source; source worktree was already dirty and no tests were run. | Extend by reference and versioned adapters, not by copying raw memory or creating competing primary IDs. |
| Starlight Evals | `starlight-evals/README.md` says the repository is a mirror; canonical Proving Ground is in SIS and evaluates memory, retrieval, harness, substrate, datasets, and system lanes. Its stated next run was 2026-07-10. | Static/stale reference surface; **not current evaluation evidence** on 2026-07-19. | SCP-004 belongs in SIS `tools/proving-ground`, with the mirror updated only after a real accepted receipt exists. |
| Prompt Engine | `prompt-engine/schema/pattern.schema.json` requires semver, provenance, eval metadata, and red-team metadata; README states promptfoo runs in CI. | Implemented source contract; no suite run in this pass. | SCP-005 should link prompt/evaluator references to traces rather than create a managed prompt duplicate. |
| ACOS evaluation audit | `agentic-creator-os/mcp-servers/evaluator/src/logging/audit.ts` writes JSONL session/evaluation records but permits unconstrained `result` and metadata fields. | Implemented source; no runtime test. | Do not make that raw audit JSON the trace schema. The new receipt must be privacy-sanitized and typed at the boundary. |
| Token Tracker/Planner | `starlight-token-tracker/README.md` delegates executable planning SoT to `agentic-ops/fleet/`; `fleet/model-routing.json` separates outcome planning from tracking. | Implemented documented contract; no live capacity probe in this pass. | Gateway cost figures can enrich a receipt, but must not replace subscription-aware fleet allocation. |

## Architecture lessons adopted

```text
client / agent / tool
        |
        v
SIS policy decision + Starlight correlation
(trace_id, span_id, event_id, project/thread/session, privacy)
        |
        +--> append-only local receipt (required)
        |         |
        |         +--> typed review candidate -> independent eval -> promotion receipt
        |
        +--> provider dispatch (policy-gated; retry/fallback bounded)
                  |
                  +--> optional OTLP / Orq projection (secondary, redacted, replayable)
```

1. **Correlation is a control-plane primitive.** Use a Starlight-owned, OpenTelemetry/W3C-compatible `trace_id`/`span_id`/`parent_span_id` with a distinct `event_id`. Add `project_id`, `thread_id`, and `session_id`; do not attach raw emails/display names to the receipt.
2. **A trace is not a dataset.** A typed review first produces an auditable candidate. Independent evaluation, privacy review, and an explicit promotion receipt are required before a regression fixture or routing change.
3. **Version references beat copies.** Trace only the prompt/evaluator identifiers, version, and commit; resolve the source artifact from Prompt Engine/Git and SIS at evaluation time.
4. **Reliability is action-aware.** Retry only classified transient model requests inside a retry budget. Never automatically retry or fall back an irreversible tool/action or a completed terminal receipt.
5. **Retention must cover the derived paths.** Expiry, deletion, policy-approved export, and mirror failure need local lifecycle receipts. A masked vendor trace is not proof that a provider never received the payload.

## Prioritized roadmap decisions — five material changes only

| Priority | Decision | Owner repo | Dependency | Acceptance test | Privacy / lock-in risk | Why this beats adopting Orq wholesale |
|---|---|---|---|---|---|---|
| P0 | **Correct SCP-001:** make `ControlPlaneTraceEnvelope` versioned and OpenTelemetry/W3C-compatible; add `event_id`, project/thread/session correlation, and terminal-write idempotency. | `starlight-memory` | Existing `routeMemoryRecord()` and `estimateProviderResourcePlan()` in a clean dedicated worktree. | Fixtures prove 32-hex trace IDs, 16-hex spans, parent-child agent/tool/model links, duplicate-terminal-write rejection, and no raw content/PII. | Identity labels or raw tool inputs could leak through correlation metadata. | Establishes a portable receipt that supports Orq, OTLP, direct providers, and local-only operation without a gateway dependency. |
| P0 | **Correct SCP-004:** add typed review annotations and candidate states before fixture promotion. | `Starlight-Intelligence-System/tools/proving-ground` | SCP-002, SCP-003, and immutable prompt/evaluator references. | Schema validates categorical/range/correction annotations; candidate records trace/prompt/evaluator/privacy provenance; independent evaluation records accepted/rejected/withdrawn. | Corrections can contain customer data; review identity and correction text need their own retention/export policy. | Retains the whole-system Proving Ground and prevents a hosted review queue from becoming a hidden training/evaluation authority. |
| P0 | **Materialize SCP-005 in the backlog:** bridge trace receipts to Prompt Engine semver/source commit and evaluator version. | `prompt-engine` | SCP-001, Prompt Engine pattern schema, SIS eval-result schema. | A promotion receipt resolves all references at the recorded commit and fails closed for a missing version; raw prompt/test content is absent from the trace. | Copying prompt text or fixtures into telemetry exposes product IP and private test data. | Preserves Git review, provenance, red-team gates, and portability while still enabling experiment comparison. |
| P0 | **Add SCP-007:** make retention, deletion, and approved export/mirror lifecycle events replayable. | `Starlight-Intelligence-System` | SCP-002, SCP-003, existing `SISMemoryRecord.retention_policy` and shadow refs. | Tests cover local-only secret, regulated default denial, expiry tombstone, approved redacted export, idempotent deletion, and a failed mirror that remains visible. | An audit tombstone must not become an undeletable copy of secret/personal content. | Keeps legal/privacy control and recovery evidence in the canonical substrate rather than relying on a vendor retention setting. |
| P1 | **Correct SCP-101:** define retry/fallback as pre-recorded, error-classified, budgeted, idempotency-aware behavior. | SIS / product runtime | SCP-001–003, SCP-007, Token Planner route inputs. | Two adapters share one trace; only configured transient errors retry; every attempt is recorded; non-idempotent tool/approval calls never retry automatically. | Retrying can duplicate spend, outputs, or external actions; a vendor fallback can silently cross data-residency boundaries. | Captures Orq's reliability pattern but lets SIS policy and the fleet planner decide whether an alternate provider is permitted. |

## Roadmap changes made

The strategic blueprint and machine-readable backlog now contain only the five decisions above:

- `SCP-001` correlation/idempotency acceptance criteria;
- `SCP-004` typed review lifecycle;
- `SCP-005` as a real backlog work item, not only blueprint prose;
- new `SCP-007` retention/deletion/export receipts;
- `SCP-101` retry/fallback safeguards.

No provider adapter was added, no SaaS purchase is recommended, and the P2 enterprise surface remains demand-gated.

## Research uncertainty and non-claims

- This is a documentation/source review, not a contract, security, DPA, SLA, pricing, or performance audit of Orq.ai. Claims such as ZDR, VPC deployment, retention, and compliance must be revalidated against the exact customer agreement and selected provider route before a customer-facing promise.
- GitHub stars, public releases, a visible license, and zero listed repository advisories are process/history signals—not a security endorsement. `orq-python` and `orq-node` had no root license file in the public GitHub contents response at the time checked; no copying or adoption is proposed.
- No remote SIS, Prompt Engine, Evals, Token Tracker, or ACOS branch was fetched, modified, tested, staged, or claimed as integrated. The dirty SIS and `starlight-memory` worktrees remain independently owned work.
- No Orq API key was created or used. `@orq-ai/evaluatorq` was inspected remotely as an MIT reference only; its documented automatic platform result sending when `ORQ_API_KEY` is present reinforces the need for an explicit export gate.[^3]

## Sources

[^1]: Orq.ai, [LLM traces for debugging](https://docs.orq.ai/docs/ai-studio/observability/traces.md), accessed 2026-07-19.
[^2]: Orq.ai, [Orq span attributes reference](https://docs.orq.ai/docs/ai-studio/observability/span-attributes.md), accessed 2026-07-19.
[^3]: Orq.ai, [`@orq-ai/evaluatorq` README](https://github.com/orq-ai/orqkit/blob/main/packages/evaluatorq/README.md), accessed 2026-07-19.
[^4]: Orq.ai, [Annotation Queues](https://docs.orq.ai/docs/ai-studio/observability/annotation-queues.md), accessed 2026-07-19.
[^5]: Orq.ai, [Prompts](https://docs.orq.ai/docs/ai-studio/prompts/prompts.md), accessed 2026-07-19.
[^6]: Orq.ai, [Create Evaluators](https://docs.orq.ai/docs/ai-studio/optimize/evaluators.md) and [Build Experiments](https://docs.orq.ai/docs/ai-studio/optimize/experiments.md), accessed 2026-07-19.
[^7]: Orq.ai, [Routing Rules](https://docs.orq.ai/docs/ai-gateway/configuration/routing-rules.md) and [Budgets](https://docs.orq.ai/docs/ai-gateway/budgets.md), accessed 2026-07-19.
[^8]: Orq.ai, [Retries and fallbacks in the AI Gateway](https://docs.orq.ai/docs/ai-gateway/features/retries.md), accessed 2026-07-19.
[^9]: Orq.ai, [Identities](https://docs.orq.ai/docs/ai-gateway/identities.md), accessed 2026-07-19.
[^10]: Orq.ai, [Sovereign AI](https://docs.orq.ai/docs/enterprise/sovereign-ai.md), accessed 2026-07-19.
[^11]: Orq.ai, [Data compliance and privacy](https://docs.orq.ai/docs/ai-studio/organization/data-compliance.md), accessed 2026-07-19.
[^12]: GitHub API metadata for [orq-ai/orqkit](https://github.com/orq-ai/orqkit) (MIT; `v1.3.2` release), queried 2026-07-19.
[^13]: GitHub API metadata and root contents for [orq-ai/orq-python](https://github.com/orq-ai/orq-python) and [orq-ai/orq-node](https://github.com/orq-ai/orq-node), queried 2026-07-19.
