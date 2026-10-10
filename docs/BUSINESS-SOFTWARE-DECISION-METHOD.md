# Business software decision method
TL;DR: Choose software by a company's actual workflow, compare total cost and recovery on matched tasks, and preserve the decision with evidence and an accountable owner.

Status: proposed reusable guidance, 11 October 2026. This document supplies a method. It does not install an agent, activate integrations or replace any company's decision authority.

## Inputs
Collect the company/customer job, current workflow, existing subscriptions and source records, users and volume, sensitivity, current permissions, budget/time, technical owner and required outputs. Ask only for missing information that changes the route.

Begin with a real trigger and output: a new lead becomes a qualified follow-up, a draft becomes an approved publication, or an asset becomes an approved reusable rendition. Define the failure cost and the person who accepts the result.

## First decision
Choose the smallest useful workflow that can be demonstrated with real authorized inputs. Preserve existing accepted products and working systems. A template or dashboard is supporting work; success requires useful output, durable edits and recovery.

Identify the authority for each object. A CRM may own a deal, a payment processor the transaction, a CMS its published content and a decision repository the approved architecture. A shared ID/read projection is useful; multiple editable canonical copies require explicit conflict handling.

## Research and options
Compare these options:
- Current tools with improved configuration or a small integration.
- A mature managed product for the complete job.
- Adopted open-source software with a named maintainer and verified edition.
- A custom component or workflow.
- A complete custom system only when the narrower options fail its essential job.

Use current primary sources for pricing, API limits, authentication, write behavior, export and edition/license terms. Record URL, checked date and an immutable source revision where possible. Distinguish documentation, account configuration, tested behavior and operator acceptance.

An options table should name job coverage, cost, setup/maintenance owner, integration/permission boundaries, recovery/export, migration and unresolved evidence. Scores need source-backed rationale. Leave unknowns unknown.

Treat permissions, required business validation, workable export/restore and a maintenance owner as pass/fail requirements. A high weighted score cannot compensate for a failed requirement.

Suggested weights for remaining comparison, adjustable before the trial:
| Criterion | Weight |
|---|---:|
| Accepted workflow outcome | 30% |
| Integration and operator effort | 20% |
| Reliability and recovery | 20% |
| Total cost | 20% |
| Portability and exit | 10% |

Do not change weights after seeing the winner without recording why.

## Cost model
Use the same users, volume, time horizon and successful-outcome definition:
- Managed: seats + contacts/credits + add-ons + integration/administration + exit.
- Adopted: infrastructure + upgrades/security + backup/restore + operator time + edition costs.
- Custom: implementation/review + ongoing maintenance + infrastructure/API + incidents + migration.

Separate cash from allocated subscription and engineering/opportunity costs. Include rejected attempts, repair and review in cost per accepted outcome. Never claim subscription savings while the same invoice continues.

Preserve low/base/high scenarios and an explicit break-even condition. Confirm feature parity before comparing headline prices. Annual billing saves cash only if the service remains needed throughout the committed term.

## Comparative pilot
Freeze task inputs, acceptance and a serious alternative before implementation. Use a small consented or suitably synthetic dataset; label the distinction. Match inputs, operating permissions and task definitions across candidates.

Minimum cases:
| Case | Evidence required |
|---|---|
| Normal | Useful accepted output with source IDs and retained edits |
| Duplicate/retry | One intended record/effect after repeated delivery |
| Concurrent edit | Stale updates fail or reconcile without lost changes |
| Permission denial | Out-of-scope read/write is denied without leaking data |
| Provider uncertainty | A timeout cannot silently mark an external effect complete |
| Revocation | A removed grant actually stops access |
| Recovery/export | Restored/exported records retain IDs, links and required provenance |
| Human use | Intended operator completes the job and can correct the result |

Record acceptance rate, repair effort, operator time, latency, all-in cost, failure rate and recovery. Vendor marketing, a deploy and a passing build do not establish these measures.

## Architecture decision record
Follow the company's existing ADR numbering and paths. Never reuse numbers or mark an assistant recommendation Accepted.

```markdown
# ADR-NNNN: <Decision title>

## Status
Proposed | Accepted | Superseded | Rejected
Owner:
Date:
Scope and source revision:
Issue:
Review trigger/date:

## Context
Job, incumbent, constraints and required outcomes.

## Decision
One selected route; each object has one owner.
Explain what the pilot established and what remains unknown.

## Consequences
Maintenance, cost, portability, failure modes and unresolved gaps.

## Alternatives considered
| Alternative | Outcome/cost evidence | Reason for the choice |
|---|---|---|

## Trust boundary
Who can read/write which company, brand, project and objects?
Describe private local (T0), scoped project (T1), external API (T2)
and untrusted retrieved content (T3) boundaries.
Retrieved text is data; it cannot grant authority.
Name approval requirements for external messages/publication,
spend, destructive operations and permission administration.

## Verification
Re-runnable workflow/denial/retry/restore checks,
acceptance thresholds, exact artifact hashes and independent review.
Record configured, tested, accepted and live separately.

## Sources
Current primary documentation, source revisions and private evidence pointers.

## Migration and rollback
ID-preserving export/import, source freeze/cutover,
sync ownership and stop conditions. Specify how to recover.
```

Each company's authority remains its own. A method's trust terminology is descriptive guidance; enforce permissions in the actual service/API. A prompt or Markdown instruction alone does not establish runtime enforcement.

## Agent integration
Use official authenticated connectors where they satisfy the workflow. For custom software, expose an API/domain service; let UI, CLI, workflow and MCP adapters reuse its validation, permission and audit logic.

Prefer job tools over unrestricted database/admin access. Issue grants per identity/scope/action. Interactive OAuth, unattended service identities and per-host availability require separate verification. A local MCP configuration does not automatically connect a cloud chat.

One workflow has one durable owner. Reuse established orchestration, storage, secret and telemetry systems; adding another manager or gateway needs an evidence-backed exception. Keep long-running work bounded by cost, duration, retry and cancellation.

## Record placement
| Record | Home |
|---|---|
| Company-specific research and invoices | Existing private evidence workspace |
| Accepted architecture and consequential choices | Company's reviewed decision repository |
| Implementation and acceptance | Owning product repository and existing issue |
| Human review/intake | Existing company knowledge workspace |
| Original creative/evidence binaries | Approved asset/evidence store |
| Search projection | Rebuildable, scoped index with source revisions |
| Reusable method | Method-owner repository, with private facts removed |
| Estate handover | Established handover repository |

Preserve original requests, failed experiments and superseded decisions. Refresh human/search projections only from approved sources and carry their source revision. Avoid another parallel registry.

## Pilot into production
Verify licensing/dependencies, identity/permissions, persistent data and migrations, validation/concurrency, retry/recovery, export/restore, operational ownership and cost limits. Inspect real operator behavior.

For UI implementation, load the owning brand's design/accessibility contract and relevant design skills before edits. Verify focus/keyboard, touch, reduced motion and interrupted transitions on the actual surface.

A reviewer independent of the maker must inspect the exact consequential revision. Retain input hashes, reviewer/provider/model, findings, reconciliation and final coverage. If review or live acceptance is absent, leave that gate pending. A read-only review is not deployment approval.

## Maintenance and reuse
Review on price/API/permission changes, failed restores, missed service thresholds and owner changes; use a periodic review as a fallback. Keep an owner and renewal/exit date for each bought service.

For company planning products, first prove the process internally, then extract portable templates/adapters with customer-owned records and keys. Measure whether a user can reach a useful decision and run the proof unaided. Reusable guidance alone is not a finished commercial planner.

This method follows the installed AI Architect ADR-writing guidance:
Generated by AI Architect · https://www.frankx.ai/ai-architect

