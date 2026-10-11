# An agent-operated software and creator company

TL;DR: Build a reusable company runtime that turns market evidence into products, distribution, customer activation and profitable delivery, with a shared business model, measurable agent work and installations customers can own.

Research date: 11 October 2026. Status: a proposed design, with current-source research and local estate inspection. No implementation, buyer acceptance or independent approval of this revision is claimed. This document expands the [record/workflow blueprint](OSS-BUSINESS-STACK-BLUEPRINT.md) after the founder rejected its breadth and intelligence as insufficient. Preserve that blueprint as one supporting layer and as a serious alternative to the larger investment.

Implementation planning now has a [foundation choice matrix](COMPANY-FOUNDATION-CHOICES.md) and [team briefs](COMPANY-BUILD-TEAM-PROMPTS.md), including DAM/CMS/storage/desktop details. Fresh source inspection found the accepted private VIS R2 exception and newer remote VIS main; existing local/README metadata ownership must be reconciled with the shared approval plane before migration or hosted dual writes.

## The company outcome

A founder should be able to choose a market problem, gather evidence, test a useful offer, build a product, distribute it, observe customer results and improve its economics without personally coordinating every step. The system must also handle interruption, conflicting evidence, failed releases and failed experiments. A billion-dollar ambition makes distribution, demand, retention and operating capacity consequential; installing tools supplies none of that evidence by itself.

The software has two customers: the founder making consequential choices and the agents carrying out bounded work. Give the founder a short decision and exception view. Give agents structured state, executable tools, fresh evidence, budgets and acceptance criteria. Both use the same domain rules and record owners.

Treat software, templates, publishing, media and world/experience products as separate studios over shared capabilities. A portfolio can generate many products while limiting simultaneous expensive experiments. Roles below describe capabilities; they do not imply twelve permanent processes or one running model per role.

## A complete capability map

| Capability | Jobs agents must actually perform | Foundation to reuse or evaluate | Owned product behavior |
|---|---|---|---|
| Market and buyer intelligence | Investigate customer problems, competing offers, reviews and direct feedback; retain contradictory evidence | Existing research/search tools; Firecrawl; selected Apify Actors; source APIs | Evidence records, freshness, deduplication, claim validation, interview synthesis and experiment proposals |
| Strategy and investment | Compare market hypotheses, constraints and distribution paths; allocate bounded R&D | Existing decision ledger, company profile and actual financial data | Assumption register, alternatives, experiment budgets, review dates and stop/continue decisions |
| Product discovery | Turn observed pain into a testable offer and acceptance criteria | Customer feedback, analytics, surveys and existing product sources | Problem-to-feature traceability, prototypes, usability evidence and experiment specifications |
| Software production | Implement, test, preview, review, release within authority and recover | GitHub, admitted coding harness, v0 for bounded UI, sandbox, browser tools, CI | Product templates with working domain modules, exact-revision acceptance and migration/rollback contracts |
| Creative production | Produce and revise writing, visual assets, video, music and educational products | Existing GenCreator and studio tools; accepted CMS/DAM sources | Brand/taste context, editable artifacts, rights, provenance, revisions, review and verified exports |
| Distribution and growth | Test positioning, social formats, search content, newsletters, partners and referrals | Existing Postiz, Resend, channel/search analytics and official APIs | Campaign briefs, approved variants, cohort tracking, attribution limits and budgeted experiments |
| Relationships and revenue | Capture inbound demand, prepare follow-ups, manage opportunities and partnerships | Existing CRM records; focused relational CRM or Twenty; Communications OS | Source-linked qualification, deduplication, contact permission and accountable follow-up |
| Customer lifecycle | Onboard, explain, diagnose activation failures and support self-service | Product analytics, knowledge base, mailbox/support adapters | Activation tasks, reproducible support cases, product feedback, churn evidence and retention experiments |
| Commerce and entitlements | Reconcile orders, licenses, access, usage and refunds | Existing payment/merchant, marketplace and accounting providers | Product/license mapping, scoped entitlements, reconciliation and operational projections |
| Finance and operations | Attribute costs, review cash exposure and contribution, detect margin changes | Actual provider receipts/invoices, accounting source, metering | Cost per accepted outcome, product economics and approved budget actions |
| Agent operations and learning | Assign bounded jobs, supply tools, measure quality, resume and improve | Existing Starlight tool/runtime plane; AI Gateway; evaluation/trace service | Work contracts, tool discovery, versioned task packs, evidence-linked evaluations and exception handling |
| Reliability and trust | Detect failures, inspect dependencies, restore data and verify access | CI, runtime telemetry, backups, secret store and current permissions | Recovery exercises, release gates, data lifecycle and production receipts |

The next stage of intelligence comes from joining these capabilities. For example, a support incident should be traceable to a customer task, a product revision, a proposed fix, an experiment and the cost of the repair. A scheduled social post should be traceable to a market hypothesis and a useful customer action.

## Shared business state and learning

Use provider-neutral identifiers to connect:

```text
source observation -> supported claim -> market/problem hypothesis
-> experiment -> product/revision -> campaign -> customer/cohort
-> activation/retention -> order/usage -> cost -> decision
```

Store ordinary relational business facts in PostgreSQL. Represent relationships with normal foreign keys and edge tables initially. Introduce a graph database only after measured traversal requirements justify another operated service. Embeddings help retrieve evidence; financial totals, access checks and customer status should come from their authoritative records.

Each important fact needs its source, observed time, source revision, confidence or uncertainty, permitted use and owner. Separate observed facts, model inferences, forecasts and approved decisions. Unknown revenue remains unknown. A repeated model summary is not an additional source.

Learning has an executable path: a production failure or founder rejection becomes a preserved example; a candidate prompt, tool or implementation runs against it and existing examples; a reviewer assesses the resulting artifact; an approved revision rolls out with monitoring. Preserve unsuccessful variants and customer-specific learning under the right permissions. Cross-company reusable patterns need explicit rights and de-identification.

This is a proposed product mechanism. The estate already has memory, registries and ledgers. Implement through their existing owners and domain records, with read projections for the dashboard. Do not create a second canonical company queue or store every source in a global agent memory.

## What an agent needs to do useful work

| Requirement | Concrete behavior |
|---|---|
| Objective | Receives a business job, target artifact and measurable acceptance criteria |
| Task context | Retrieves current company policy, product/brand facts, relevant evidence and the current task state |
| Skill | Uses a versioned procedure with examples, tool schemas and failure cases; improvements require evaluation |
| Tools | Discovers a small permitted subset; uses typed domain actions, APIs, CLI or MCP as appropriate |
| Execution | Uses a suitable admitted worker/sandbox, with durable continuation for long jobs |
| Memory | Retains decisions and useful observations externally; source freshness and permission remain visible |
| Authority | Operates under a server-enforced identity, scope, deadline and cash/tool grant |
| Coordination | Hands over an artifact ID, source revision and receipt; downstream jobs do not depend on chat recollection |
| Verification | Checks a useful result with tests, source reconciliation or a distinct reviewer, according to the job |
| Accountability | Reports outcome, failed/uncertain effects, provider usage and repair effort |

Use an event-driven runtime: a customer question, failed deployment, new order or approved experiment starts a bounded job. Idle workers need not consume model tokens. Durable jobs pause for external results or approval and resume from recorded state. Concurrent work follows actual capacity, dependencies and cost grants.

One durable owner controls a workflow. Existing estate decisions select Cloudflare Workflows for shared agent/entity work already on that platform and Vercel Workflows for application-local Next.js/Sandbox work. Preserve existing n8n integration ownership where applicable. Temporal is a serious alternative for workloads that demonstrate its need; introducing all of them for the same task would multiply state and recovery responsibilities. [Cloudflare Workflows](https://developers.cloudflare.com/workflows/), [Vercel Workflows](https://vercel.com/docs/workflows) and [Temporal](https://docs.temporal.io/evaluate) supply durable execution mechanisms; side effects still require application-level idempotency and reconciliation.

Cloudflare Agents is a candidate for addressable, persistent agent entities that need session identity, scheduling or real-time coordination. Its runtime supports durable identity and local SQL state. Ordinary business records retain their accepted relational owner. Evaluate its [runtime and Code Mode](https://developers.cloudflare.com/agents/) against the existing admitted harness before expanding the deployment footprint.

An illustrative engineering job contract:

```json
{
  "job": "repair-onboarding-export",
  "product_id": "example-product",
  "input_revision": "immutable-source-revision",
  "evidence_ids": ["reproduction", "customer-task", "baseline"],
  "output": "reviewable-patch-and-preview",
  "acceptance": ["retains-original", "exports-valid-file", "resumes-after-interruption"],
  "allowed_actions": ["read-issue", "edit-owned-worktree", "run-scoped-tests", "create-preview"],
  "cash_limit_usd": 12,
  "deadline_minutes": 30,
  "on_uncertain_external_effect": "reconcile-before-retry",
  "release_authority": "separate-existing-grant",
  "review": "distinct-reviewer-bound-to-final-revision"
}
```

Numbers here illustrate a contract, not a recommended universal limit or an executed job. The executing service must validate the actual grant; a model cannot authorize itself by editing this JSON.

## How the agents make better decisions

Decision work needs explicit uncertainty and a way to learn. For each proposal, ask which evidence would change the choice, how expensive the error would be, what reversible experiment could resolve the uncertainty and when the result must be reassessed. Compare observed customer behavior with the forecast. Calibrate forecasts across repeated experiments instead of treating a model's confidence statement as reliability evidence.

Choose execution effort by the job: deterministic code for reconciled calculations; a validated smaller model for routine classification; retrieval plus source checking for research; stronger reasoning for ambiguous design; a bounded builder and distinct verifier for consequential changes. Use self-contained handoffs between roles. Repeated delegation without new evidence consumes budget without resolving the decision.

Give the runtime a capability gap path. When a required tool is missing, inspect existing adapters first, then propose a narrow adapter or skill with a typed contract, retained examples, test and license/maintenance cost. Promotion follows review and evaluation. Agents can improve procedures and propose tools under authority; they cannot expand their own permissions, cash grants or deployment scope.

Use progressive autonomy by job family. Observations and proposals can run with read authority. Reversible internal writes can run within an approved bounded scope. Live publication, sensitive customer actions, billing and production changes follow their actual grants and review gates. Widen the scope only after retained job-specific success and recovery evidence. Keep an exception inbox that names the choice, consequence and relevant artifact; group related approvals while retaining each action's exact scope. Count founder interventions and their causes to identify the next automation investment.

## A modern tool stack, with adoption conditions

| Layer | Recommendation | Why and adoption condition |
|---|---|---|
| Experience | Existing Next.js/Vercel app; v0 for bounded screens | Reuse working products and accelerate design; test real workflows before promoting a template |
| New content/admin modules | Payload | Core provides schemas, access control, admin and APIs; existing Git/MDX and media authorities remain explicit |
| CRM | Focused PostgreSQL module or Twenty adapter | Build business-specific relationships; adopt mature CRM behavior when it earns its integration/operation cost |
| Data/auth | Existing approved Supabase/PostgreSQL identity and records | Transactions, migrations and access rules; preserve current account/linking semantics |
| Asset delivery | Accepted metadata, private master store and delivery provider | Rights, versions and approvals matter more than a grid of uploads |
| Product analytics | PostHog managed service first for evaluation | Connect activation, retention, errors, flags and experiments; require a real event taxonomy and customer permission |
| Agent evaluation | Existing compatible trace/eval service; evaluate Langfuse | Link prompts, traces, offline examples and production quality; avoid duplicating telemetry without a demonstrated gap |
| Model access | Existing AI Gateway lane | Compare workload quality, latency and actual costs; one provider ingress per execution lane |
| Durable entity/job runtime | Accepted Cloudflare/Vercel boundary | Resume jobs and preserve owner identity; retain portability in business logic and tool contracts |
| Engineering/browser execution | Admitted coding harness, suitable sandbox and Playwright | Test real user behavior and bounded code; prefer CLI/skills where the host supports them |
| Research/extraction | Existing search, Firecrawl and selected Apify jobs | Cache source evidence; public web extraction and licensed verified contact data are different purchases |
| Repeated crawling | Crawlee when operationally justified | Own extraction code when volume and maintenance evidence favor it |
| Integration automation | Existing n8n route | Useful fixed integrations; external workflow-building and commercial bundles require license-scope verification |
| Third-party OAuth connectors | Existing shared adapters first; Composio selectively | Buy missing OAuth/token-refresh/schema maintenance where it saves measurable work; verify per-user/project scopes |
| Social/email | Existing Postiz and Resend routes | Authorized delivery and reconciliation; source strategies live in company/product records |
| Usage metering | Plain durable usage ledger first; evaluate OpenMeter at complexity threshold | Product entitlements and billing need reconciled events; advanced usage catalogs may justify a dedicated system |
| Fine-grained authorization | Existing domain access rules first; OpenFGA when delegation becomes complex | Useful for company/brand/project/asset relationships; budget and execution limits still need separate enforcement |
| Secrets | Existing accepted secret store and delegated access | Avoid distributing long-lived privileged keys to every agent |
| Reliability | Existing CI, logs, monitoring and recovery tooling | Measure the customer workflow and restore actual state; vendor dashboards alone do not establish health |

[PostHog's MCP](https://posthog.com/docs/model-context-protocol) exposes analytics, feature flags, experiments and other product operations. That makes it useful to an agent testing a product hypothesis; collecting events without a decision and measurement plan adds storage and cost. No account connection or product measurement was tested in this slice.

[Langfuse's agentic evaluation interfaces](https://langfuse.com/docs/evaluation/agentic-access) support CLI/skills, MCP and APIs for evaluation work. Its [self-hosted architecture](https://langfuse.com/self-hosting) involves web/worker services, PostgreSQL, ClickHouse, Redis/Valkey and object storage. A managed option can cost less in total than operating that set for a small company. Existing telemetry compatibility and license additions require evaluation before adoption.

[Composio's session MCP interface](https://docs.composio.dev/docs/sessions-via-mcp) can expose selected tools and connected accounts. Its documentation says calls over hosted MCP bypass SDK-local tool-call modifiers. Enforce company authority and budgets at a point the actual execution path uses. Prefer a scoped project credential; treat exported connection headers as secrets. Composio is an optional connector purchase, not an additional authority over our domain records.

[OpenMeter](https://openmeter.io/docs) offers usage metering, plans, billing and entitlements. [OpenFGA's task authorization model](https://openfga.dev/docs/modeling/agents/task-based-authorization) can represent permissions delegated for a task. They address different needs. Neither supplies the product's full cost accounting, cash grant or business acceptance logic by installation alone.

## Agent interfaces without MCP setup for every tool

Build one domain-action implementation per owned module, with shared validation and permissions. Offer a generated typed SDK/OpenAPI adapter for services, a CLI for shell-capable agents, and a remote authenticated MCP adapter for compatible chat hosts. Provider webhooks and jobs call the same domain behavior. Avoid separate business logic in every transport.

Prefer actions such as `crm.propose_company`, `assets.request_revision`, `experiments.record_result` and `jobs.inspect_receipt` to an unrestricted database-writing tool. An action validates source revision, scope and idempotency; a receipt tells the caller whether the effect was confirmed, denied, running or uncertain. External effects stay uncertain until reconciled with their provider.

Discover and load only the tool family required for the job. Where execution is allowed, a sandbox can compose multiple typed operations and return a compact result, with scopes and budgets enforced on each actual call. [Cloudflare Code Mode](https://developers.cloudflare.com/agents/tools/codemode/) provides a current example of code-based tool composition. Its existence is not evidence of savings for this workload; measure an equivalent task against direct tool calls.

For coding/browser work, the [Playwright project](https://github.com/microsoft/playwright-mcp) recommends considering CLI plus skills for token efficiency, while retaining MCP for suitable persistent exploratory contexts. Keep MCP for hosts that need it. The goal is a useful agent surface across hosts, with setup generated and tested by the installer.

ChatGPT cloud needs an externally reachable authenticated endpoint and a compatible configured client/account. A local Codex MCP configuration does not configure ChatGPT. Host support for authorization, tool discovery, writes and background execution must be tested in each supported host. A successful connector read establishes only that observed capability.

## Complete loops the company should be able to run

### Demand to delivered value

1. Market work retains sourced observations and direct customer feedback, including reasons the offer might fail.
2. The founder approves a problem/offer experiment with a target customer task, a cash/time budget and a learning question.
3. Product and creative work produce a usable prototype or artifact and a truthful offer. A reviewer checks the artifact against the target task.
4. Approved distribution sends the offer through selected channels and records the campaign/variant identifiers.
5. Customer activation and order records show whether people reached the useful result, bought and continued using it. Interviews explain results that analytics cannot.
6. The next product revision addresses the observed constraint. The decision retains the hypothesis, evidence, cost and reason to continue, change or stop that experiment.

Track qualified demand, first useful result, repeat use, contribution and founder intervention time. Distinguish demand for a free artifact from willingness to pay for the actual product. Attribution remains uncertain when customers cross channels or devices. A small cohort often supports qualitative learning before a statistically meaningful A/B conclusion.

### Customer problem to verified product improvement

A customer cannot reopen and edit an exported artifact. The support agent gathers permitted reproduction evidence; the engineer reproduces the failure in an isolated lane; the product owner defines the expected behavior; a bounded worker produces a patch and preview. Tests cover original preservation and interrupted recovery. A distinct reviewer binds acceptance to the final revision. Release occurs under the existing grant. Runtime and product telemetry then check the repaired customer path and retention indicators.

Success is a usable recovered artifact and improved customer behavior. Opening a PR, publishing a package and reaching production are separate observations. A customer request can create evidence and a proposed task without giving an agent authority to merge, charge or publish.

### Delivery cost to better economics

Actual job/provider receipts reveal a product's expensive repeated extraction step. The agent proposes a cache/freshness policy and a cheaper extraction candidate. Both run on the same representative inputs, including previously failed cases. Compare accepted quality, repair effort, time and actual billed usage. An approved canary rolls out the winning change; reconciliation checks whether the invoice and customer outcomes improved.

The agent must account for retries, review, sandbox runtime, source acquisition and founder repair. Subscription use and API-equivalent token prices are different accounting measures. Customer-owned provider bills and our own delivery costs need separate ledgers.

### Social and media experiments

For Frank's creator and software portfolio, build campaigns around demonstrated useful work: a before/after customer task, an engineering result, a creative artifact or a source-backed lesson. Produce editable variants for selected channels from the same evidence and approved assets. Give each variant a specific audience, offer, destination and measurement window.

Use LinkedIn to test professional/buyer explanations where that audience is relevant; use video and visual channels for demonstrable creative work; let search content answer concrete questions; use the owned newsletter for permissioned repeat contact and feedback. These are channel hypotheses to measure, not universal posting-frequency or algorithm claims. Preserve brand-specific voice, rights and audience context.

A distribution job should return approved artifact references, provider receipt links, destination events and follow-up observations. Review qualified traffic, activation, purchases and useful replies alongside reach. Founder-premium content and live publishing retain their existing human gates. Scheduling metadata is insufficient proof of successful delivery.

## Package the system for other founders

The product hypothesis is a maintained deployment and operating system for a company's agent-enabled workflows. A customer should finish installation with a useful job running, an understandable bill and a tested export/recovery path. A folder of prompts or a dashboard alone would leave too much of that job to the customer.

Extend an existing product home. A company profile supplies business model, products, channels, existing tools, data sensitivity, budget, permitted autonomy and target customer outcomes. A transparent planner produces:

- A capability gap map and build/buy/adopt recommendation with serious alternatives.
- A provider/edition/license bill of materials and a parameterized cost model.
- An install plan using the company's existing accounts where suitable, with migrations, connector consent and record ownership mapping.
- Versioned skills, tool contracts, evaluation examples and runtime grants for selected jobs.
- A readable decision log and source records, alongside machine-readable deployment configuration.
- A doctor, first-job acceptance, supported host checks, backup/export/restore and update plan.

This planner is proposed engineering work. It should compile approved configuration into the existing runtime and installation mechanisms, rather than becoming another orchestrator. Make choices inspectable: the founder can see which feature requires which provider and choose a different adapter.

For customer-owned delivery, provider keys and business records stay in the customer's accounts. Release application, schema and harness updates as separate versioned components; the existing harness update contract does not establish safe application/database upgrades. Test upgrades on retained representative data, keep a rollback plan and disclose which versions are supported.

Provide a maintained catalog of useful modules and evaluated work recipes: research-to-offer, product repair, editable media production, activation support, relationship follow-up and cost investigation. Users activate what their company needs. Shared schemas, acceptance examples and adapters improve across the catalog. Customer data does not become shared training material by default.

Commercial possibilities include licenses for complete company installations, maintained module packs, studio/product templates and updates. An optional managed service would introduce custody, recurring operating cost and support responsibilities, requiring a separate business decision. Support/update/refund/distribution costs remain real even with BYOK.

### Serious competitive alternatives

| Route | What a buyer obtains | What must be shown before we claim an advantage |
|---|---|---|
| Managed SaaS suite and native AI | Maintained standard operations and integrations | Our relevant job succeeds more reliably or at lower total cost, including founder time |
| n8n plus OSS applications | Flexible self-built workflows and owned deployments | Our installation, updates, rights model and recovery reduce the buyer's integration burden |
| A template or agent prompt pack | Low purchase/setup scope | Our delivered application produces materially more useful accepted work |
| Our customer-owned installation | Connected domain modules, evaluated jobs, decision history and maintained delivery | A fresh user installs, completes a real task, resumes after failure and understands/export their records |

The differentiated asset would be the tested job catalog, shared business semantics, accumulated permitted evaluation cases and reliable installation/update experience. Buyer demand and defensibility remain hypotheses. Interview and observe intended customers before claiming market superiority or spending broadly on distribution.

## Cost design and scale

The previous $120/month scenario covered a small shared records application with assumed usage. It is not a full company-runtime budget. A company producing video, crawling sites, running sandboxes and serving customers has a workload-dependent bill. Free tiers cannot establish its operating economics.

Use:

```text
monthly cash = fixed platform subscriptions
             + completed and failed jobs' model/research/runtime costs
             + files, delivery, email, telemetry and connector usage
             + licenses and transaction-related provider costs

total operating cost = monthly cash
                     + installation/update/repair labor
                     + allocation of product engineering cost

cost per accepted result = attributed run costs and repair
                        / accepted useful results
```

Treat build cost and monthly operation as separate cash-flow items. For planning, a simple scenario of 1,000 jobs at an assumed $0.20 each implies $200 in job cash. At an assumed $3 each it implies $3,000. The assumptions must be replaced with measured representative runs; neither figure is a price quote or prediction. Apply the same sensitivity model to source acquisition, video minutes, storage, customer volume and failure rate.

Use stronger reasoning on consequential strategy or ambiguous repair when evaluation supports it. Use validated smaller models, batches and deterministic code for routine extraction/classification. Cache source evidence with an explicit freshness rule, avoid repeated full-document ingestion, load tools on demand, and cap retries. An extra model review must earn its cost through measured error prevention.

Managed PostgreSQL, delivery, email, analytics and evaluation often deserve a subscription because they save operated state, recovery work and founder attention. Choose self-hosting with a pinned license, upgrade plan, restore proof and a measured cash/maintenance comparison. Public crawling tools cannot supply every kind of verified proprietary enrichment. Clay or another data vendor can remain a bounded fallback where its paid data measurably improves useful results.

Keep existing HubSpot/Attio/Notion records when they do the job economically. A migration needs a useful-task comparison, record fidelity, export/recovery and an explicit owner. The decision to build our focused CRM has a product/reuse investment case as well as a subscription-saving case.

Stage additional capabilities by evidence:

| Stage | Activate | Evidence before expanding |
|---|---|---|
| Existing products and manual baseline | Current records, accepted tool plane, real customer task and cost capture | A usable baseline and its bottleneck |
| First closed loop | Shared domain actions, selected durable owner, role procedures and measured job | Useful accepted artifact, failure recovery and founder effort |
| Repeatable company operations | Product analytics, evaluation, distribution/lifecycle jobs and reconciliation | Several comparable successful runs, actual costs and bounded exceptions |
| Customer-owned product | Install/update/export, host adapters, license inventory and first-job acceptance | Fresh install and actual receiving-user acceptance |
| Larger scale | Additional workers, sophisticated usage/authorization, complex orchestration or warehouse as needed | Measured capacity/economic requirement and verified recovery |

These are capability gates, not fixed calendar promises. A mature company may need several stages at once; a solo founder without customers may get more value from an offer test than an advanced warehouse. Keep the overall design visible while admitting a bounded implementation slice.

## R&D and decisions that agents can maintain

Use the existing reviewed decision home. Give each experiment a hypothesis, owner, source/date, alternatives, input and artifact revisions, method, costs, uncertainty, observed result, decision and next review trigger. A decision has a status such as proposed, tested, accepted, superseded or rejected. An agent can propose a record; acceptance follows the company's actual authority.

Keep readable Markdown rationale and versioned structured configuration together. Generate dashboard projections from those records. Link large/retained artifacts and private receipts by ID instead of copying private conversations into reusable repositories. For a generic customer installation, a folder layout can be:

```text
company/profile.yaml
decisions/ADR-*.md
experiments/<id>/hypothesis.md
experiments/<id>/result.json
capabilities/<module>/contract.json
evals/<job>/cases.jsonl
releases/<version>/manifest.json
```

This is an illustrative customer artifact contract. In the existing estate, keep canonical decisions, task queues, evidence, memory and handovers in their already accepted homes. This research document creates no new authoritative registry.

Evaluate architectural choices on useful work, setup/update time, reliability, data ownership, portability, license scope and total cost. Evaluate agent changes on retained cases, exact-revision output quality, recovery, permissions and cost. Public superiority claims need buyer/competitor evidence beyond our internal tests.

## Acceptance and remaining gaps

Document-level acceptance: complete capability map; explicit shared state/learning and tool interfaces; matched alternatives; end-to-end jobs; current-source research; cost assumptions; customer-owned delivery and honest implementation status. Product acceptance additionally needs a fresh installation, useful artifact, receiving-user acceptance, measurable outcome, scoped authority, interruption/recovery, upgrade/export/restore and exact-revision independent review.

A production slice must test stale writes, duplicate events, revoked access, wrong company, source contradictions, unavailable providers, uncertain side effects, expired OAuth, exhausted budget, cancellation and restore. Idempotent internal state does not guarantee exactly-once external publishing or charging. Reconcile receipts before another attempt.

This design has not implemented those jobs or audited current production health. Provider prices/licenses must be bound to the actual pinned editions and distributions. No model benchmark, customer demand, savings, revenue or valuation was measured. Independent provider review of this revision remains pending; earlier review clients failed before substantive inference and were not retried without a changed access signal.

## Estate application, without new authorities

The company-specific recommendation remains private. Reuse the existing Business OS installation candidate and governed runtime factory; existing GenCreator/studio products for creation; shared tool plane, model ingress, memory and secret ownership; accepted media fabric; Communications OS for messages/booking; private Registry for accepted portfolio decisions. Existing source and recent ledger records establish work to reuse, not complete live integration.

The recommended next implementation target is one existing software/creator product's demand-to-first-useful-result loop, including one meaningful product improvement and one approved distribution experiment. Select its free lane and exact owners first. Compare a manual/incumbent route and our owned route using the same customer brief. Retain the full company design and add modules as their workflows earn adoption. The document slice can finish; the company product objective remains open.
