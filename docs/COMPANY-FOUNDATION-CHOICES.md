# Company foundations, cloud choices and the asset/content pipeline

TL;DR: Own the business contracts, asset/content lifecycle, agent work recipes and installation experience; use Vercel for web products, Cloudflare for suitable durable entities and private preview storage, Railway for container workloads, and managed services where they earn their operating cost.

Research: 11 October 2026. Status: proposed investment/build plan informed by primary documentation and existing source/architecture inspection. Accepted company architecture remains with its existing reviewed owner. No platform purchase, infrastructure mutation, product implementation or independent approval is claimed. Read the broader [company architecture](AGENT-OPERATED-COMPANY-ARCHITECTURE.md) and the [executable team briefs](COMPANY-BUILD-TEAM-PROMPTS.md) together.

## Fundamentals to invest in

| Investment | What we own | Why it compounds across products |
|---|---|---|
| Business contracts and identifiers | Company, brand, product, asset, content, customer, experiment, order and job semantics | Products and agents can exchange useful state without each inventing another database or integration |
| Domain actions and tool contracts | Validated business operations exposed through API, SDK, CLI and MCP | The same permissions, revisions and receipts apply to humans, agents and workflow adapters |
| Asset and content lifecycle | Provenance, rights, immutable revisions, renditions, editorial review, placements and takedown | Creative work becomes reusable, traceable and editable across studios and channels |
| Durable work and recovery | Task definitions, one execution owner, idempotency, cancellation, budgets and reconciliation | Agents can finish useful work through interruption and provider failure |
| Identity and delegated access | Company/brand/project membership and narrowly scoped action grants | New apps reuse the same authority instead of distributing privileged keys |
| Product production and installation | Templates with working behavior, evaluated recipes, deployment plans, updates and recovery | Internal engineering can become a maintained customer-owned product |
| Evaluation and economics | Retained cases, exact-revision quality, actual bills and founder effort | Tool/model changes are selected on useful results and total cost |
| Experience and distribution | Shared design system, editable artifacts, channel adapters and customer activation evidence | More products can reach their audiences without repeating every launch operation |

Start with a modular implementation inside existing product boundaries. Extract a shared package when at least two actual consumers need it and an owner can maintain it. Shared infrastructure should have deliberate failure boundaries: one product's bad job must not consume another brand's budget or corrupt its records.

## Choices across the stack

“Follow” means reuse an existing accepted boundary. “Propose” means the recommendation still needs implementation evidence. Optional adoption requires the named trigger; this table does not approve a new subscription or migration.

| ID | Layer | Choice | Why / alternative / revisit trigger |
|---|---|---|---|
| F01 | Web experience | Follow: existing Next.js/Vercel products | Reuse previews, release pipelines and UI integration. Cloudflare-only or Railway-only hosting needs measured capability/cost/operating advantage |
| F02 | UI acceleration | Propose: v0 for bounded screens and prototypes | Use generated code after review in the owning repo. Do not infer working data, authorization or a production workflow from a template |
| F03 | Business data | Follow: approved Supabase/PostgreSQL authority | Transactions, migrations, identity and relational truth; avoid adding a database per dashboard |
| F04 | Local asset state | Preserve VIS local library; propose an explicit cloud synchronization contract | Local discovery/curation can work offline. Shared rights/approval ownership must be reconciled with the accepted metadata plane before any migration or dual write |
| F05 | Public web media | Follow: Vercel Blob/product delivery and Vercel Image | Serve approved immutable renditions with the page. Cloudinary/Images/Stream are measured transformation/video exceptions |
| F06 | Private library masters/previews | Follow: existing accepted VIS private R2 exception | Cross-machine large masters and small previews have a distinct storage job. Verify routing, access and restoration before claiming a usable cloud library |
| F07 | Evidence and recovery | Follow: Drive for approved evidence/master handoffs and existing backup owner | Record which copy owns which purpose. Synchronization is not proof of backup/restoration |
| F08 | New CMS/admin workloads | Propose: Payload in an existing product | Reuse drafts, versions, admin and APIs. Preserve current Git/MDX sources until a deliberate migration; Sanity/Contentful or existing editor may win when managed editorial operations justify them |
| F09 | DAM application | Extend VIS; preserve Eagle as optional local browse/rate tool | Own provenance, rights, proposals, placements and agent workflows. Current VIS decisions supersede earlier Immich/PhotoPrism deployment proposals |
| F10 | Desktop surface | Existing local operator/PWA first; Tauri when native tasks justify it | Watch-folder intake, OS integration and offline work may earn a native shell. Retain the accepted implementation and compare a concrete task before changing framework |
| F11 | Durable agent/entity state | Follow: Cloudflare Agents/SQLite-backed Durable Objects for suitable entities | Use where persistent identity, coordination or real-time sessions are needed; ordinary business records stay relational |
| F12 | Job orchestration | Follow: Cloudflare or Vercel Workflows by owner; reuse n8n integrations | One durable owner per workflow. Temporal/other engines require a demonstrated workload exception |
| F13 | Containers and heavy jobs | Reuse Railway for appropriate Node/Python, integration and media workers | Suitable for existing n8n/Postiz and container workloads. Keep jobs/attempts/budgets in their owner; do not add another orchestrator because a worker lives here |
| F14 | Model ingress | Follow: existing AI Gateway execution lane | Compare models by task quality/latency/cost. Direct provider runtime is a bounded exception; avoid layering several routing gateways |
| F15 | Agent engineering tools | Reuse admitted harnesses, sandbox, GitHub and browser/CLI tools | Buy runtime capabilities through supported interfaces; keep task packs, artifacts and acceptance portable |
| F16 | Secrets and delegated connectors | Follow: Infisical/service ownership; evaluate Vercel Connect first for suitable Vercel workloads | Existing accepted Connect candidate supports scoped access. Composio is a selective alternative for missing providers/hosts; provider/subject compatibility and cost must be tested |
| F17 | Tool transport | Follow: shared tool plane plus task-scoped API/CLI/MCP adapters | One domain behavior per action. Remote OAuth MCP supports compatible chat hosts; local CLI/skills can be better for file/code jobs |
| F18 | Research and data | Existing search plus Firecrawl/selected Apify; Crawlee conditionally | Cache permitted evidence. Buy verified licensed data only when its useful-result advantage earns the cost |
| F19 | CRM and communications | Focused existing records or Twenty; reuse Communications OS | Use a standard CRM when its mature operations win; own the cross-product evidence/follow-up behavior |
| F20 | Social/email | Existing Postiz/Resend routes and official APIs | Own campaign logic and approved variants; rent delivery. Keep human live-publication and consent boundaries |
| F21 | Product/agent telemetry | Existing compatible telemetry; evaluate PostHog and Langfuse for gaps | Analytics measures customer outcomes; traces/evals measure agent work. Avoid duplicate instrumentation and unneeded operated state |
| F22 | Commerce and accounting | Existing payment/marketplace/accounting sources | Own product mappings, entitlements and reconciliation. OpenMeter becomes an option when usage catalogs justify it |
| F23 | Access complexity | Existing membership/domain rules; OpenFGA conditionally | Adopt when resource relationships/task delegation outgrow simple rules; it does not replace execution budgets |
| F24 | Provisioning | Versioned provider-native configuration and deterministic adapters; OpenTofu conditionally | Start with working platform APIs/CLI. Add IaC when resource coverage, drift, repeated installs and provider maintenance justify it |
| F25 | CI and release | Existing GitHub checks, previews and deployment owners | Maintain portable tests, exact-revision review, migration/rollback and customer-path verification |
| F26 | Decisions and R&D | Existing reviewed Git decision owner, readable projections and private evidence | Retain rationale, alternatives, method, source revisions, actual costs and revisit triggers; no new portfolio authority |

For a fresh customer, equivalent providers can implement these contracts. Our own estate follows its accepted choices and documented exceptions. Avoid presenting a universal stack as the correct answer for every industry and company stage.

## Business modules on these foundations

These are capabilities in the existing Business OS and product studios. A capability can be an agent recipe and a projection of existing records; each row does not need a new application, subscription or database.

| Company work | Build and retain | Adopt where it wins |
|---|---|---|
| Company discovery and IT decisions | Company profile, constraints, evidence-backed option comparison, decision/revisit history and installation plan | Primary research, actual invoices, provider tools and existing decision owner |
| Market/customer intelligence | Source-linked opportunities, consent-aware relationship evidence, experiment briefs and actual customer feedback | Search, permitted crawl/extraction, licensed data and a standard CRM when needed |
| Production | Evaluated recipes for the existing Publishing, Template, Software, Media and World/Experience studios; editable source and accepted artifacts | Domain editors, model/media providers, licensed templates and permitted OSS components |
| Asset/content operations | VIS lifecycle, provenance, rights, exact revisions, editorial states and placements | Storage, delivery, Payload editor/admin and optional Eagle browsing |
| Distribution | Audience/offer evidence, channel-specific variants, approval, attribution and learning | Postiz, Resend, official channel APIs and existing Communications OS |
| Customer activation and service | First useful result, entitlements, delivery state, feedback and support escalation linked to the actual product | Payment/delivery/helpdesk/community providers and existing receiving product |
| Economics and portfolio | Job cost, actual orders, repair effort, margin scenarios and evidence-based continuation/retirement decisions | Payment/accounting truth and selected telemetry/metering adapters |
| Engineering and reliability | Task packs, contract tests, migrations, installation/update/export/restore and release evidence | GitHub, platform runtimes, admitted coding tools and existing operational owners |

A sellable first package should complete one customer task, such as producing and distributing an approved offer with reusable assets and an editable page. Customer-owned deployment and updates can be part of the product. Offer the broader fleet as maintained modules with explicit dependencies, permissions and a successful first-use recipe. Benchmark installation and accepted-result effort against a serious incumbent. Demand, useful outcomes and maintenance economics remain to be demonstrated.

## Cost and reuse decisions

Use total cost per accepted result: infrastructure and provider usage, paid data/delivery, retries, storage/transfer, human repair, administration and amortized engineering. Compare both cash and founder hours. A lower subscription bill can still increase total cost.

For each module, require a named customer/operator task and source owner, a same-task alternative, a measured reason to build, and export/update/recovery obligations. Start a fresh installation with only its required services. An existing estate using three providers does not require every customer's first module to activate all three.

Reuse evaluated artifacts and permitted evidence before making another model/crawl call. Persist waiting jobs and wake them on real events; avoid model polling. Load the small tool family the task requires. Prefer bounded workers that release compute between jobs when the measured workload permits it. Allocate cash per company/brand/job and reconcile unknown remote effects before retries. These are implementation targets; no current bill reduction was measured here.

Keep core product code and third-party components distinguishable in the dependency/license inventory. A self-hostable application can still impose distribution or external-user restrictions. The current [n8n license guidance](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case) distinguishes an internal/backend use case from an external customer's access to n8n workflows, including through MCP; evaluate commercial rights before distributing that capability. Do the same pinned-version review for any adopted CRM, social or media component.

## Cloud responsibilities

Vercel carries the founder/customer web experience, application endpoints, previews, appropriate application-local jobs, model integration and web delivery. Cloudflare carries suitable persistent agent entities, their shared durable jobs and the accepted private preview/master workload. Railway carries selected container applications and workers. Supabase/PostgreSQL carries transactional records under an explicit owner.

Put the expensive data path near its processing/storage owner where practical. A worker reading a large master from another cloud can incur transfer, request and runtime costs even when the object store itself advertises free egress. Measure the complete route and choose regions with actual latency and residency requirements; this proposal makes no residency guarantee.

Railway has its own [private S3-compatible buckets](https://docs.railway.com/storage-buckets). Its [billing documentation](https://docs.railway.com/storage-buckets/billing) distinguishes bucket charges and service egress during uploads. That is an option for a Railway-local workload, not a reason to create another master archive. Railway volumes are attached persistent filesystems with [backup/restore mechanisms](https://docs.railway.com/volumes/backups); they have a different role from an asset object store.

[R2 pricing](https://developers.cloudflare.com/r2/pricing/) includes storage and operations; direct R2 egress is free. Transformation, worker, retrieval class and cross-cloud paths still need workload accounting. [Private Vercel Blob](https://vercel.com/docs/vercel-blob/private-storage) needs authorized access rather than exposing the object as an ordinary public URL.

## Our DAM, storage and visual apps

The reusable architecture has distinct records: asset identity, content hash/version, original locations, private master, rendition, approval and placement. A website uses an approved rendition reference; it should not query a private library and dynamically invent publication permission on every request.

Recommended pipeline:

```text
Local/cloud intake -> hash and provenance -> existing asset record
-> small private renditions -> search/curation -> human rights/approval
-> exact approved export -> web/social/content placement -> delivery receipt
```

Keep large originals private. Small thumbnails/previews make a laptop/phone/cloud UI useful without synchronizing every master to every device. Download the original when editing/export requires it. Retain local originals until the actual backup/restore acceptance permits removal.

For an existing local VIS workflow, keep its library and command interface. For a shared cloud workflow, define which records the existing local store can propose, which cloud owner accepts them, and how acknowledgments/revisions return. Never let an offline “approved” flag silently overwrite shared rights or publish state. Local curation edits can queue with a source revision; conflicts remain reviewable. This synchronization is proposed engineering work, not existing proof.

### Source inspection and gaps

The inspected local VIS implementation branch is older than current remote main. Current remote main was pinned at `812c538cdc2f773cd0735ffb49edbeac0b0116e9`. Its root instructions describe an existing library record, loopback review screen, MCP gates and private preview Worker. Source includes a four-operation storage adapter: put/get master, put rendition and obtain an expiring rendition URL. Original downloads verify SHA-256 before committing the destination.

The same source has older README/radar language about local SQLite truth and older delivery candidates. The reviewed portfolio media decision names Supabase/Postgres metadata/approval. These statements require an explicit boundary reconciliation before team members create a hosted catalog or migrate records. Preserve working local behavior, stable IDs and provenance. No live storage, screen, two-machine retrieval or restore was tested here.

The existing VIS human-gate issue records a configured private Worker with public routes disabled in an earlier receipt. That is configuration evidence, not a currently verified cross-machine retrieval path. A route/access change, R2 write, rights change, publication or deletion of the only copy keeps its existing owner/gate. Do not solve private access by enabling a public bucket.

### Human, agent and system responsibilities

| Stage | Human | Agents | Systems |
|---|---|---|---|
| Intake | Select permitted roots/sources | Inspect and propose bounded import | Existing VIS intake/local library; approved object adapter |
| Identification | Review exceptions | Hash, retain provenance, find exact duplicates | VIS IDs/version records and sidecars |
| Preview | Browse and compare | Generate authorized small renditions and label dimensions | Existing rendition worker/storage and local/cloud view |
| Curation | Rank, keep/reject, set rights through the existing process | Suggest tags, similarities and collections | VIS proposal/review record; optional Eagle browse projection |
| Export selection | Approve exact version and intended use | Prepare derivative/placement plan | Asset/content references and approved manifest |
| Delivery | Authorize the release action | Execute only the admitted export/upload job | Vercel delivery/product repo or authorized social provider |
| Receipt | Review exceptions | Reconcile exact served bytes/revision and placement | Deployment/provider receipts and placement records |
| Failure: interrupted upload | Decide only if recovery cannot proceed within grant | Resume/reconcile; preserve original; report unknown effect | Attempt receipt, object verification and job owner |
| Failure: changed/revoked approval | Review the affected placements | Stop stale delivery and prepare takedown/repair | Current approval revision, placements and release owner |
| Failure: private preview unavailable | Inspect access/routing decision | Use retained local preview; report failing path | Local cache, Worker access and existing operator |
| Recovery | Approve destructive steps separately | Restore to a safe destination and verify bytes/metadata | Existing backup owner, original hash and restore receipt |

## CMS and DAM together

CMS owns editorial content and its revisions. DAM owns asset identity/provenance and the accepted asset lifecycle. Link content to `(asset_id, version_id, rendition_id)` and record placements. Editing an image creates a new version; existing published references stay bound until an approved content revision changes them.

For a new workload, [Payload drafts](https://payloadcms.com/docs/versions/drafts), [versions](https://payloadcms.com/docs/versions/overview) and [preview](https://payloadcms.com/docs/live-preview/overview) supply useful foundations. We build the product-specific schema, brand permissions, asset picker, exact publication approval and receipt. Draft and published queries must explicitly select the intended revision. Keep preview access private; revoke approval when a revision changes.

[Payload storage adapters](https://payloadcms.com/docs/upload/storage-adapters) include Blob/S3 integrations and direct client uploads. Its native R2 adapter is for Workers bucket bindings; Node/Vercel uses the S3-compatible adapter. Large intake should bypass application request-body limits through authorized direct uploads, then verify content before accepting the record. This does not authorize Payload to become a second archive/rights owner.

The [Local API](https://payloadcms.com/docs/local-api/overview) exposes powerful in-process operations. User/agent requests must retain collection access checks and the actual authenticated principal; do not let a convenient internal API bypass become an agent's unrestricted write path. Recheck defaults against the pinned version.

CMS flow: brief -> editable draft -> choose approved asset -> private preview -> human review of exact content/assets -> admitted publication -> served-revision receipt. Failures include stale edits, unavailable assets, source conflicts, changed approval and failed deployment. The editor keeps its draft while publishing reports a pending/failed/uncertain result honestly.

## Desktop versus cloud

| Surface | Best job | Engineering choice |
|---|---|---|
| Existing local VIS operator/PWA | File intake, local browsing, review and privacy | Refine the accepted screen and existing commands first |
| Authenticated cloud web view | Cross-device preview, team review, content selection and job status | Extend an existing owned web surface with the same records/actions; avoid exposing a loopback server |
| Native desktop companion | Watch folders, offline batch work, OS dialogs and bounded local processing | Evaluate Tauri when those tasks earn packaging, signing and updating |
| Phone/browser intake | Submit a permitted file/link and review previews | Start with responsive web/PWA and existing provider adapters |

[Tauri supports web frontends with native backends](https://tauri.app/start/). Its [Next.js integration](https://tauri.app/start/frontend/nextjs/) requires a static frontend; ordinary server routes/actions are not bundled by a static export. Share React components/domain types where useful and keep the server API remote, or explicitly own a sidecar runtime. Do not promise one unchanged Next.js/Payload app can serve every desktop/server role.

Treat local paths as device-specific locations, not cloud identifiers. Encrypt/protect permitted local state and minimize caches according to the data lifecycle. Test offline queue reconciliation, wrong account, logout, expiry and update recovery before making a customer-facing desktop claim.

## Seamless provisioning and engineering

```text
Company profile -> capability/owner plan -> template and dependency resolution
-> infrastructure diff -> admitted provisioning -> credentials/consent
-> migration/configuration -> preview -> first useful task -> release/observe
```

Own the transparent planner and acceptance contracts. Use provider APIs/CLI/MCP to perform the actual work. [Railway's MCP](https://docs.railway.com/ai/mcp-server) and [Vercel's MCP](https://vercel.com/docs/agent-resources/vercel-mcp) provide supported platform interfaces. Cloudflare supplies [MCP OAuth support](https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/). These interfaces do not grant administrator permission or prove an end-to-end setup.

Track separate states: selected, installed, provisioned, configured, authenticated, tested and accepted. Rerunning a plan should discover existing resources and reconcile receipts instead of creating duplicates. Keep account/project/environment explicit, secret values out of logs, and the resource/cost diff reviewable. An installer can guide necessary provider consent; it cannot manufacture it.

[OpenTofu](https://opentofu.org/docs/intro/) supplies versioned write/plan/apply infrastructure workflows. Use it where actual provider coverage and state ownership are maintained; provider-native project files/adapters can be simpler for the first supported installation. Neither route replaces application/schema migrations and useful-task verification.

[Vercel Connect](https://vercel.com/kb/guide/vercel-connect) provides team connectors, project links and short-lived scoped tokens, including application/user subject distinctions. Verify the target provider, host, token subject, trigger and revocation behavior. Non-Vercel authentication differs from deployment OIDC. The record remains an accepted candidate until the actual workload passes those checks.

## Frontier tools and partners

Use frontier products through their supported SDKs, APIs, CLI, MCP, exports and licensed templates. Buy proprietary services when their functionality wins; absorb permitted OSS components with pinned licenses. Our portable artifact/tool contracts should make models and execution workers replaceable. Access to one model API does not include the vendor's entire browser, coding, connector or managed-agent product.

Keep one runtime/harness owner per job. Claude Agent SDK, Google ADK and other supported agent runtimes are candidates behind that boundary, not additional control planes to install together. [Claude's platform overview](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) distinguishes its API/SDK from higher-level agent products; [Google ADK's MCP tools](https://google.github.io/adk-docs/tools-custom/mcp-tools/) provide another integration route. Customer commercial access must use the permitted authentication/billing route.

Prioritize technical relationships:

| Relationship | Concrete investment | Evidence before commercial partner claims |
|---|---|---|
| Vercel | Working web/install templates, AI integration, delivery and connector examples | Customer outcomes and program acceptance; [technology partnerships](https://vercel.com/partners) are a route to investigate |
| Cloudflare | Durable entities, authenticated tools and measured private-library access | Reusable examples and actual workload economics; [startup benefits](https://www.cloudflare.com/startups/) depend on eligibility/coverage |
| Railway | Maintained container templates, updates and worker runbooks | Fresh install/recovery and current program terms; evaluate [template kickbacks](https://docs.railway.com/templates/kickbacks) separately |
| Supabase/PostgreSQL and Payload | Portable schemas, migrations, identity integration and editorial examples | Useful integration proof and clean licensing/ownership |
| Model/media providers | Job-specific quality/cost benchmarks and portable artifacts | Actual results, rights and authorized commercial usage; no fixed allegiance |
| Delivery/data partners | Reliable social/email/research adapters | Useful measured workflows, supported permissions and maintenance economics |

These are priorities and possible program routes. No current formal partnership, credit entitlement or commercial arrangement was verified here. Temporary credits should not determine the long-run architecture.

## Build sequence and acceptance

1. Reconcile current sources and record owners; preserve existing VIS/GenCreator/Business OS work and unresolved human gates.
2. Refine the existing VIS review journey and prove permitted private preview/recovery across devices.
3. Deliver one CMS/DAM journey with exact editable content, asset references, private preview and approved publication receipt.
4. Expose that proven behavior through the existing tool plane and supported API/CLI/MCP adapters.
5. Automate a repeatable customer-owned installation, application/schema update, export and restore.
6. Extend CRM, distribution, customer lifecycle and economics through those contracts; add specialized services when evidence justifies them.

Honor current WIP and machine/cost admission. The team briefs describe responsibilities and handoffs; they do not start simultaneous workers or authorize production, spend, rights, posting or destructive changes.

Acceptance: one real brief produces a useful editable artifact; an authorized release uses exact approved bytes/revisions; two permitted clients see consistent records; interruption resumes without duplicate effects; revoked access and stale approval are denied; the installed customer can export/restore/update; actual cash and repair effort compare with a serious alternative. Source inspection and documentation do not establish these outcomes.

Independent exact-revision review, runtime benchmarks, current invoices, actual two-device acceptance and live storage/host checks remain pending. The next build is assigned through existing product issues and write lanes. This document slice may complete; implementation remains open.
