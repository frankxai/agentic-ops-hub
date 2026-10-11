# Company swarm build programme

TL;DR: Build the complete company workflow through existing product owners, shared domain operations and measured integration waves, with explicit economics, recovery and release evidence.

Prepared 11 October 2026. Proposed execution programme. No workers, infrastructure or recurring jobs were started by this packet. Earlier briefs were rejected for insufficient depth; their revision remains in Git. This programme contains a full engineering scope, while deployment, independent acceptance and product implementation remain separate work.

Read [economics](COMPANY-BUILD-BUY-ECONOMICS.md), [coordinator prompt](COMPANY-SWARM-COORDINATOR.md), [lane prompts](COMPANY-SWARM-LANE-PROMPTS.md), [foundation choices](COMPANY-FOUNDATION-CHOICES.md) and [architecture](AGENT-OPERATED-COMPANY-ARCHITECTURE.md). The machine-readable [programme](company-swarm/programme.json), [schema](company-swarm/programme.schema.json) and [evaluation cases](company-swarm/evaluations.json) are planning artifacts. No JSON field grants runtime authority.

## The complete useful outcome

DAM work is optional and is not a prerequisite for the first revenue product. Use existing folders, desktop tools and already-approved assets when they satisfy the selected job. Admit an asset-library improvement only for an observed browsing, retrieval or delivery problem. The commercial DAM estimates describe a broader product, not the minimum internal R2 gallery. Execute the relevant parts of the waves; do not start every module.

A founder can choose an offer from evidence, create an editable artifact using approved sources/assets, review it, place it in a CMS, prepare distribution, receive a permitted customer event, deliver the correct version, record costs and feedback, and resume after interruption. Another founder can install the selected components in their own accounts, update without losing edits, revoke a connector and export/restore the data.

The creator still controls rights and external publication. The same operation can be reached from an appropriate web app, CLI, supported host or MCP client without bypassing permissions. A connected tool is not proof that these journeys work.

Business functions covered: strategy/customer research; relationships and acquisition; asset ingest/curation; content/creative production; editorial/CMS; distribution; commerce/entitlements; delivery/support; finance/cost observation; intelligence/memory; platform/reliability; security; installation/update/export; R&D and evaluations. Do not invent a separate new platform for each function.

## Reuse and ownership

The private agentic-ops Registry is the portfolio authority. This hub is a sanitized proposal/projection. Refresh Registry and product main sources before writing; observed source pins are evidence snapshots. Resolve a missing owner before building.

Existing implementation candidates include GenCreator's CreatorPack/Mission and distribution adapters; VIS asset/version/provenance/rights/placement operations; Business OS pack and foundry product structure; SIS runtime/journal/memory and published SDK; existing commerce and release owners. Inspect current source, not only README claims.

The accepted hosting boundary is Vercel for Next.js web delivery, Cloudflare for justified persistent entities and cross-entity workflows, and a single durable owner per job. App-local workflows can use the accepted Vercel workflow boundary. Railway is a conditional worker/service host for a workload that earns it. Do not install Temporal, Redis, a new queue, gateway or vector store from an old skill default.

Private VIS R2 is an accepted storage exception. Public web asset delivery has its separate owner/default. Reconcile older SQLite catalog prose with accepted Postgres metadata/approval ownership before cloud synchronization. Do not dual-write competing rights authorities.

## Shared operation contract

Implement one domain operation, with adapters around it. The server owns authorization; host/plugin descriptions and tool annotations cannot grant it.

Every request carries an authenticated subject, workspace/brand, operation, resource ID, expected revision, requested side effect, idempotency key, deadline/cancellation context and admitted budget reference. A server derives allowed operations from trusted membership and permissions. Client-supplied approval, entitlement or “safe” flags remain untrusted.

An operation returns changed resource/revision, durable job ID if asynchronous, explicit observed state, export/recovery reference where relevant, usage/cash meter and a typed error or pending/unknown effect. HTTP success without an observed provider effect cannot mean published/delivered.

Use transactions or an outbox where local state and external delivery cross a failure boundary. Keep correlation IDs through adapters. Retain unknown side effects and reconcile them using provider lookup/receipts before retrying. Never promise exactly-once behavior across an uncooperative external service.

An asset placement references stable asset ID, version, rendition and current rights/approval decision, not just an expiring URL. A content edition references sources and exact assets; a customer delivery references accepted artifact/version and verified entitlement. Approved revision A cannot silently authorize revision B.

## Waves and dependency graph

| Wave | Required work | Useful evidence before progressing |
| --- | --- | --- |
| W0 | Refresh ownership, economic assumptions, customer job, baseline and admission | Current source/owner map; matched build/buy decision; actual authorized budget |
| W1 | Shared operations, record ownership, private storage/recovery and telemetry | One real permitted record operation; denial/retry; recoverable private asset retrieval |
| W2 | Existing DAM/CMS/creator workflow and host adapters | Editable source-backed artifact with approved asset placement; same revision visible in permitted surfaces |
| W3 | Distribution intent, checkout/entitlement/delivery and customer support | Reviewed payload, actual authorized receiving event, correct delivery/refund/export recovery |
| W4 | Customer-owned install/update, selected CRM/research adapters | Cold installation, preserved edits, revoke/export/restore and measured support burden |
| W5 | Controlled improvement and broader commercial scope | Independent exact-revision verdict, buyer task comparison, outcome/cost improvement with no critical regression |

Economics can defer an entire module even if the architecture supports it. W3 may reuse a proven existing checkout without waiting for W4 CRM. Instrument the chosen useful slice early; avoid months of platform work before a sellable artifact.

Suggested first vertical slice: reuse VIS and GenCreator to select approved assets, create/edit a source-backed campaign, export it, recover it, and deliver the accepted version through an existing permitted product flow. In parallel planning, retain the customer-owned Business OS pack product hypothesis. The receiving owner must accept the result before calling the connection complete.

## Assignment and integration discipline

A lane is a capability responsibility, not a permanently running agent. The sixteen lane prompts cover the programme; normally one coordinator, one or two builders and a distinct verifier operate in staged waves. Local runtime slots and fresh machine admission can reduce that to serial work. The coordinator never creates overlapping writer scopes.

Before execution, compile each selected lane into an assignment containing verified repo/origin/base/branch, exclusive exact output paths, current guides, input IDs/revisions, allowed tools/actions, actual time/cash/context limits, acceptance and stop condition. Unresolved fields make the lane unadmitted. Hashing a proposal does not authenticate an admission receipt.

Each builder submits an inspectable artifact and handoff: source/implementation revision; instructions read; behavior observed; commands/evidence; failures; cash/provider attempts; migration/rollback; open gaps; next bounded action. The integration owner alone merges sequentially. A reviewer stays read-only unless separately assigned a write lane.

Freeze operation semantics first, then implement separate adapters. Validate on both sides of every seam: VIS to CMS; CMS to campaign; campaign to destination; payment to entitlement; entitlement to delivery; package to customer accounts. Test partial failure and mismatched revisions at each seam. Do not solve integration by copying private databases between products.

## Improvement loop

Capture task outcome and failure evidence with minimal permitted data. A failed task proposes a specific candidate change to a prompt, skill, adapter, model route or deterministic operation. Bind the proposal to its source case and baseline. Sensitive sources stay private; test fixtures use approved/sanitized examples.

Run the candidate on development cases, then untouched holdout cases and the named serious alternative. Compare accepted output quality, unsupported claims, repair minutes, actual cash, latency, recovery and permissions. Include rejected founder examples. A lower token bill cannot offset broken authorization, lost work or poorer accepted output.

Permit at most two revision rounds for one hypothesis before reassessing it. Keep new model/skill evaluation traffic within its own actual budget. Use a reversible staged rollout with a named owner, observed window and rollback criteria. Automatic improvement may propose a PR; it cannot self-award new permissions, publish premium work or replace a human-approved policy.

Retain failed attempts and previous accepted versions. Memory stores source-backed decisions and compact lessons; it does not treat repeated generated claims as facts. Update the existing decision log and product issue. No extra perpetual observer, self-modifying production agent or competing objective queue is implied.

## Observable acceptance

Use [evaluation cases](company-swarm/evaluations.json) as a specification to implement, not a claim that tests have run. Track proposed, implemented, executed, independently reviewed and customer accepted separately.

Representative journeys:
- A permitted creator ingests a supported file, gets a stable identity, reviews rights, creates an editable edition, places a selected version, exports and restores it.
- A host reads permitted records, makes an authorized draft change, sees a conflict for stale revision, loses access after revoke and cannot access another tenant.
- A destination times out after possibly accepting an edition. The job remains unknown, reconciles by provider receipt and avoids blind duplicate posting.
- A customer install uses their own accounts/keys, upgrades while preserving content and demonstrates migration rollback and restore in a clean environment.
- A budget/cancellation signal stops new provider calls, retains partial useful work and reports actual billed attempts.

Prototype and synthetic results cannot establish live customer success. Consequential releases need independent provider review of the final revision, applicable design/editorial/rights checks and current deployment evidence. If reviewer access fails, retain pending status and a source-bound packet.

## Remaining gaps and stop conditions

This proposal has not proved live cross-device private retrieval/restore, synchronized host/cloud state, actual bill savings, licenses for every redistributed dependency, installation in a customer account or buyer preference. Current VIS catalog authority needs reconciliation; occupied branches remain protected.

Stop dependent execution on missing owner/guide/grant, admission hold, crossed spending cap, unexplained side effects, critical permission/recovery failure or unresolved independent release findings. Continue authorized documentation, research or another independent admitted slice. Report the exact blocker and preserve work; do not archive the objective or call the fleet complete.
