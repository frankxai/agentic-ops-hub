# Starlight interfaces for founders and agents

Proposal dated 7 October 2026. Frank selected the first outcome: coordinate products, knowledge, and agent work in Starlight. This is an architecture and delivery proposal. It does not authorize a deployment, scheduler, provider purchase, platform migration, or broader agent fanout.

## 1. Decision and valuable outcome

Evolve the accepted Canvas creation experience, private Observatory observations, and existing Home/Command portfolio views into one coherent working experience. Share identity, navigation conventions, commands, evidence, and interaction components across their current owners. Preserve the applications and their accepted workflows. The first build improves one creation task inside Canvas and uses scoped contextual links to the other applications. Wider shared views follow measured benefit. This does not require merging repositories or creating another shell.

The founder should be able to choose a product outcome, collect the right sources, work on the actual deliverable, assign bounded work to an available agent, inspect the result, and resume it after interruption. The usable output is an editable, exportable creation artifact with source evidence and a recoverable work record. Examples include a website section with a working preview, a campaign with cited claims and publishable assets, or an implementation with a reviewed diff.

The interface earns its place if it reduces repeated briefing, app switching, repair work, and owner review time compared with the founder's native apps plus a Markdown/Obsidian record. A billion-dollar company is an ambition; this architecture can improve operating capacity, but customer demand, distribution, retention, and economics still need their own evidence.

## 2. Reuse and authority

| Responsibility | Existing owner | Interface integration |
| --- | --- | --- |
| Mixed-source capture, selected context, artifact inspection and creation | `starlight-agent-canvas` | Extend the accepted Capture → Map → Inspect → Ask → Handoff journey. Keep source readiness and portable export. |
| Private native session and usage observations | `starlight-observatory` | Read scoped observations; display missing coverage, observation age, and billing uncertainty. |
| Portfolio Home, product missions and oversight planning | `starlight-command-center` | Reuse Home/Command views and issue contracts; coordinate the console reuse decision in #62. |
| Canonical work identity, admission, continuity and protocol | `Starlight-Intelligence-System` | Consume the canonical work/continuity contract; send commands only through its admitted owner interface. |
| Durable memory and work-graph projection | `starlight-memory` and the existing Markdown vaults | Read rebuildable projections. Preserve original goal, work, session, repository and memory identities. |
| Team compilation and execution admission | `starlight-swarm` and the existing worker plane | Reuse current contracts; prove dispatch, cancellation and receipts before adding controls. |
| Brand, tokens, interaction standards and craft evidence | `starlight-design-intelligence` | Use the appropriate brand pack and surface mode in each product. |
| Capability/configuration discovery | `starlight-agent-config` and current pack registries | Load task-relevant interfaces on demand; preserve shared tool pooling. |
| Cross-repo handover | `agentic-ops-hub` | Keep this proposal and the estate record; product issues retain implementation acceptance. |

Current evidence changes the sequence. Canvas continuity PR31 and SIS continuity PR273 are merged according to live GitHub reads. A merged source change does not prove that the installed runtime, two harnesses, or all machines use it. Observatory #9 still tracks wider coverage and actual installation/acceptance. Command #62 explicitly requests reuse and a read-only first cut, with a separate build gate. Keep these distinctions in the product.

Local source inspected: Canvas `1729a5721a12a84d81faae4ef972c3fa3e8a859f`, Command Center `26a349c6e4100e7277254b20fbe70f172a8c3af8`, memory `38941aaca7ebe0a8ee63215ec13159b91feeb791`. These are inspection baselines, not deployment claims. GitHub main heads observed separately: Canvas `b13d84add4cc998e97c2a1c3799b873dce2d59ff`, SIS `7b33f3a228bf407e447e9b061a5d133622e39f81`, private Observatory `87f1bf087b6430bc1093a9d24a72fd6af4d72ddd`. Re-query and inspect the chosen revision before implementation; the full remote trees were not audited here.

### Read-model contract to ratify with the existing owners

This proposed join contract is the exit artifact of the bounded read-model design. It is not a new canonical schema. SIS owns its ratification and exact-version mapping before any control implementation.

| Join or field | Authority and resolution rule |
| --- | --- |
| Work | Use the existing `workId` with its principal/project scope. `correlationId` groups traces; it must not collapse distinct work items. Canonical admission/completion comes from SIS work events and proof gates. |
| Product/project | Preserve the canonical product/project reference and `projectId`; use reviewed source mappings where namespaces differ. Titles never establish identity. |
| Session/run | Preserve native session/run ID, harness/provider namespace, account/principal scope and machine reference. Join to work only through an explicit, source-backed association. Unassociated sessions remain visible as unresolved. |
| Repository/checkout | Use the canonical origin/repository mapping; keep checkout identity, branch and observed revision separate. Revalidate routing and ownership before a write. A similarly named folder is not an alias. |
| Artifact/review | Resolve through the artifact owner's stable reference plus revision/hash. A source link alone is reference-only. Bind a review to the exact hash and its acceptance criteria. |
| Runtime liveness/usage | Native collectors own their observations; show `observedAt`, coverage and provenance. A SIS declared work state cannot turn stale runtime observations into fresh liveness. Invoice and per-goal allocation remain separate facts. |
| Freshness/conflict | Use each owner's documented freshness limit; absent limits produce freshness unknown. Preserve source time and compilation time separately. Surface disagreements and owner repair links rather than blending status or inventing a relationship. |

The exact owner contract must pin schema versions, accepted input sizes and privacy limits, source field paths, unknown/null semantics, freshness limits, and fixtures for missing, duplicate and contradictory identities. The UI remains read-only until that mapping is accepted. This is engineering design within the existing slice, not a replacement ledger.

## 3. The human experience

The long-term experience has five understandable places: Today, Products, Create, Knowledge, and Runs. Map these concepts onto current routes. First prove the existing Canvas Create journey and link to Home/Observatory; new shared views are conditional on that benchmark.

**Today** answers what needs a decision, what can land today, and what is blocked. Group repeated signals by existing work identity. Rank them using visible deadline, dependency, and impact reasons. Let the founder pin priorities and mute noise. A refreshed observation must not silently change a declared goal or imply an old task is complete.

**Products** links each accepted product to its audience, buyer evidence, current deliverable, release constraints and next decision. Outcomes can remain qualitative until measurement exists. A source-reported stage, passing build, released artifact, and accepted customer outcome have different labels.

**Create** gives most screen space to the artifact: document, code/preview, storyboard, content package, or domain-specific work object. On desktop, use a narrow project navigator, a large work area, and an optional context/evidence inspector. Conversation sits beside the work when helpful. Selection scopes the agent's context, with a visible packet preview. Every generated result can be edited, compared, exported, and traced to its inputs.

**Knowledge** supports cited answers, relevant source passages, related decisions, and a bounded relationship view. Start a graph at the selected goal or artifact with a small visible neighborhood. Offer the same facts through a semantic list/tree. On a phone, prefer the list, focus card, and source inspector. Canvas remains useful for spatial work; global graph browsing must prove a benefit over search and lists.

**Runs** shows goal, artifact, owner, machine, harness, repository/branch, admission, current action, remaining budget, observation age, and recovery action. A founder can inspect the exact scope sent to an agent. Controls appear only when a tested adapter and current authority support them. Unknown cost or missing cloud transcript coverage stays explicit.

On a phone, prioritize decisions, review, concise source inspection and recovery. On tablet and desktop, support sustained editing and comparison. Preserve deep links, browser navigation, keyboard selection, and the selected artifact across refreshes and navigation. Streaming progress should not move controls, steal focus, or scroll someone away from an edit.

## 4. Shared design and frontend engineering

Canvas already uses Next.js, React, Tailwind, React Flow, the Vercel AI SDK and Playwright. Preserve its accepted stack and lockfile; assess security and compatibility on the implementation revision before changing versions. Share stable packages or source-pinned components across repositories. A forced estate-wide monorepo or runtime microfrontend migration adds coordination cost before proving a better workflow.

Build a small reusable set of interaction components: artifact inspector, source/citation link, editable brief, revision comparison, context selection, decision card, connection repair, run timeline, budget display, and recovery panel. Bind them to existing typed contracts. Domain views supply their own content and actions. Use existing accessible primitives before adopting another component library.

Public marketing and discovery pages should use server rendering/static delivery where appropriate, with small client islands for useful interaction. Creation tools load editors, graphs and media previews only when needed. Poll or stream observations while visible; coalesce updates, preserve cursor/focus, bound history, and stop background rendering when hidden. Measure bundle cost and interaction latency on real tasks before adding optimization libraries.

Starlight Operator mode calls for stable navigation, readable density and restrained signal color. FrankX retains its founder/product voice; Arcanea retains its canon and creative identity. Share operational meanings and accessible interaction behavior while keeping brand-specific typography, palettes, imagery and narrative. Reuse host tokens and the existing liquid kit only where it helps comprehension and remains within rendering budgets.

Target WCAG 2.2 AA; 44px primary touch targets are the stricter project standard. Acceptance includes keyboard operation and restored focus, readable contrast, semantic screen-reader alternatives, touch actions without hover dependencies, reduced motion, and repeated/interrupted transitions. Announce meaningful progress through a polite live region, with aggregation rather than every streamed token. Use an accessible alert for blocking errors/holds; focus an error summary after a user-initiated failed action and restore focus after a dismissed dialog. Asynchronous observations must not steal focus from editing. Graph/list parity tests must resolve the same item IDs, facts, source links and inspector selection. Frequent keyboard actions respond immediately. Occasional transitions should be short, interruptible and purposeful. No essential action requires drag, a gesture, a timer, or waiting for an animation.

## 5. Generative UI and current protocols

Keep the navigation and important editing surfaces stable. Allow an agent to propose task-specific cards, comparison tables, source selections and bounded forms using a versioned catalog of approved components. Validate both the structure and the action payload before rendering; enforce authorization again where the action executes. Render unsupported or invalid output as a usable text/list result with a recovery option.

Agents can supply domain data, component choices, and suggested actions. The application owns layout constraints, accessibility, URLs, permissions and execution. A schema-valid card can still carry an unsafe link, a misleading claim, or unauthorized scope, so catalog validation is only one check. The deterministic UI must remain usable if the model is slow or unavailable.

| Interface | Proposed use | Boundary |
| --- | --- | --- |
| MCP | Task-scoped tools, sources and data through the existing shared plane | Tool discovery does not grant action authority. |
| Codex app-server | Persistent native Codex threads, streamed items, interruption and runtime approval requests | Preserve native request/session IDs and approval semantics; do not infer cloud ChatGPT access. |
| Claude Agent SDK | Supported programmatic Claude runs, sessions and permission handling | Keep account mode and licensing distinct from API or managed hosting. |
| ACP | Optional editor/agent integration for runtimes that demonstrably support it | Negotiate capabilities and pin adapter versions; it is not universal app control. |
| AG-UI | Optional normalization of streamed interaction events across supported backends | Project events to the UI; canonical work authority remains SIS. |
| A2UI | Isolated pilot of generated component descriptions against the shared catalog | Official site lists v0.9.1 as current and v1.0 as candidate on the research date. Keep behind an adapter. |
| A2A | Optional delegation across independently operated agent services | Use where the external boundary requires it; local task allocation need not adopt another protocol. |

The first execution pilot uses existing MCP tools and native Codex app-server/Claude Agent SDK paths where their tested lifecycle semantics are needed. Use the existing AI SDK rendering path for model-backed creation inside Canvas. ACP, AG-UI, A2UI and A2A require a written pilot admission: the integration effort or user task they improve, the fixed baseline, pinned versions, acceptance threshold and removable adapter. They are not prerequisites for the first build. The product should continue working if an experimental pilot is removed.

Official sources: [Codex app-server](https://learn.chatgpt.com/docs/app-server), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), [ACP](https://agentclientprotocol.com/get-started/introduction), [AG-UI](https://docs.ag-ui.com/introduction), [A2UI](https://a2ui.org/), [AI SDK generative UI](https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces), [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [A2A specification](https://a2a-protocol.org/latest/specification/). Research was read on 7 October 2026; documentation support does not establish local account entitlement or installed compatibility.

## 6. Ontology, graph and memory

Extend the existing operational work graph and memory projection. Use a small shared vocabulary with domain extensions. Core references cover product/project, goal, work/task, artifact, source/claim, decision, memory, session/run, capability and evidence receipt. Accepted graph relations already include `motivates`, `targets`, `implements`, `depends_on`, `has_evidence`, `records` and `supersedes`. Reuse them where their endpoint types fit. New concepts and relations need the owning schema's review, not a second identity registry.

The useful query is specific: which current decision and verified sources shaped this artifact, which work item can change it, and what blocks delivery? Preserve source references, observed time, revision/hash, privacy classification and declared versus verified state. Record the review's artifact hash, reviewer, acceptance criterion and limitations. Changes to the artifact invalidate that review where relevant. Proposed relationships remain proposals until source evidence supports them.

Keep these memory classes distinct:

| Memory | Contents and promotion |
| --- | --- |
| Working context | Selected sources, current brief and budget for one bounded run; expire or checkpoint with the task. |
| Episodic | Run observations, failures, outcomes and receipts; useful for recovery and evaluation. |
| Semantic | Cited facts and concepts with validity and contradiction handling. |
| Procedural | Reviewed skills, workflows and repair practices tied to versions and outcomes. |
| Preference | Explicit taste and interaction feedback with scope and source; never promote a guessed preference as Frank's instruction. |

Canonical durable memory remains the existing Markdown/source records. Local lexical/vector indexes and graph views are rebuildable. Use the present local core and search paths first. PostgreSQL plus pgvector is a candidate projection backend for a user-operated multi-device deployment once scale and retrieval measurements justify it. A dedicated graph database is deferred until representative traversal workloads show it improves on the current typed projections. [pgvector documentation](https://github.com/pgvector/pgvector).

Retrieval should filter by principal, product, privacy, source rights and permitted corpus before ranking. Combine lexical results, semantic candidates when available, and a small neighborhood of declared graph relations. Rerank the resulting bounded set, return cited passages, and show conflicts or missing evidence. Scoping must happen before external model calls. Retrieved text remains data and cannot create tool permissions or overwrite policy.

Context packets contain the declared goal, acceptance, selected sources, accepted decisions, exact artifact/work references and missing evidence. Token ceilings and source selection should be visible. Evaluate answer usefulness, citation correctness, stale-source handling, retrieval latency and wrong-scope exclusion on fixed tasks. Embedding/search scores are not confidence probabilities.

Promotion follows the existing SIS operational-work-graph rule: a stable claim, evidence reference, privacy/retention classification, contradiction/staleness evaluation, human or policy-authorized promotion, and a reversible projection. Proposed claims/edges stay in the existing memory-candidate or product curation path; they never become accepted facts merely because an agent emitted them. The owning SIS/memory schema must define the exact candidate location, promoter authority and contradiction/supersession representation before the pipeline writes durable knowledge. Preserve competing source claims until an authorized decision resolves them.

Respect the existing graph layers: workflow legality, memory/truth, on-demand code impact for the active product, and the World steering model. Procedural capability records remain within their existing owner. No per-agent or per-domain second brain, estate-wide code index, or new scheduler is implied by this proposal.

## 7. State, orchestration and recovery

Separate UI state, creation documents, observed runtime state and canonical work state. UI state covers selection, focus, drafts and panels. Creation state covers the editable artifact and versions. Observations are explicitly timestamped views. SIS retains canonical work identity and admission. A browser component or generated card cannot directly declare a mission admitted or complete.

Use an explicit transition model for dispatch/recovery controls, implemented in the existing style or a proven state-machine library if needed. XState is a candidate for complex local interaction logic; the documentation currently exposes v6 alpha, so do not introduce an alpha dependency merely to be current. Model-based transition tests can validate the contract without adopting a new framework. [Stately actor documentation](https://stately.ai/docs/actors).

The logical run sequence is proposed → admitted → running → awaiting review → verified outcome, with distinct paused, cancelled, failed and unknown-effect branches. These UI concepts map onto existing SIS events and native observations rather than introducing a competing enum authority:

| UI concept | Source evidence | Projection rule |
| --- | --- | --- |
| Proposed | Existing intake/goal/task declaration, such as `intent.captured` | Work has been described; no execution authority is implied. |
| Admitted | Current SIS `work.admitted` plus required proof gates and applicable leases | Admit only the approved scope; expired or missing evidence removes readiness for a new effect. |
| Running | Native adapter's fresh run observation, correlated with canonical work; `run.started` where supported | Show source and time. A historical start event does not establish present liveness. |
| Awaiting review | `artifact.produced` and unsatisfied applicable verification gates | Display the exact artifact and missing review; do not infer acceptance. |
| Verified outcome | Required `verification.passed`/other admitted gates and canonical `work.completed` | Completion describes its verified scope; it does not imply revenue or unrelated production delivery. |
| Blocked, paused, cancelled, failed or unknown effect | Current owner-native states/receipts; `work.blocked` where applicable | Preserve the owner-native value and reason. Unsupported mappings remain unknown, with no dispatch/release permission. |

Before Increment C, the SIS owner must accept the version-pinned table of exact field paths, enum/event values, projection logic and transition fixtures. This conceptual table is not proof that the installed runtime emits every event. Streaming events and native completion remain observations to reconcile with artifact verification and actual acceptance.

Admission reserves task, worker/provider/account and budget atomically through the existing owner. Dispatch receives stable idempotency identity, exact repository/worktree, permitted outputs, context scope, deadline, cancellation policy and acceptance. A late result from an expired lease cannot silently gain release authority. Recheck authority and current artifact/source revisions at the effect boundary. Existing authorization carries forward within its scope; routine reversible steps should proceed without repeated confirmation. Human decisions bind to the exact proposed effect and revision and become invalid when that proposal changes.

Checkpoint before provider work and before side effects. Reconnect to the supported native session when possible. If session resumption is unsupported, continue from a portable checkpoint in a new, explicitly linked run. Switching providers transfers an approved context/artifact packet; hidden reasoning and native session identity do not migrate automatically.

Retries are bounded and classify the failure. If an external side effect may already have happened, query/reconcile its receipt before retrying. Idempotency requires provider cooperation or an adapter ledger; no distributed framework guarantees exactly-once external effects. Keep an unknown-effect hold when reconciliation is impossible. Proposed pilot limit: at most three reconciliation reads within two minutes, then hold. C admission records the actual release owner, permitted notification route, escalation policy, and backup if one exists. Notify the owner on hold; after fifteen unacknowledged minutes notify the recorded backup, or retain a visibly unacknowledged owner hold when there is no backup. Retain a daily reminder until acknowledgement through an existing authorized notification loop; no new scheduler is authorized here. The existing release authority resolves the hold using destination evidence. Acknowledgement, silence and elapsed time never clear it. With no backup, consequential unattended external actions remain sink-only; the solo founder can still create drafts and run already-authorized reversible work. If owner/notification support is absent, external-effect admission fails. Cancellation records a request and acknowledgement separately; it cannot undo an already completed external action.

An effect is a state change, including a billed call or file write. Distinguish already-authorized reversible changes inside allocated artifact/worktree paths from external consequential changes such as publishing, spending outside the admitted budget, credential changes or destructive operations. C can perform the former under existing scoped authorization; its fault suite uses an effect sink for the latter until their separate authority and recovery prerequisites pass. Writing outside admitted paths is denied. This classification supports a solo founder without manufacturing a second human operator.

Temporal remains the existing architecture's candidate for genuinely long, multi-machine missions. Its durable workflows can recover execution and waits, while non-deterministic model/tool work belongs in activities. Adopt it through the current runtime owner after operational proof, not as a new service in every installation. Small local workflows may retain the existing checkpointed runtime. [Temporal durable AI](https://docs.temporal.io/ai).

## 8. Several AI apps and useful swarms

Build a capability registry view over current adapters. For each adapter, record discovery, tested revision, account/auth mode, read/stream/start/resume/cancel/approval support, usage provenance, and evidence freshness. Represent states such as detected, configured, tested, unavailable, and unknown distinctly. An installed executable, model catalog entry or active subscription is not proof that a particular request is permitted or will succeed.

Increment A has no broker or dispatch surface. C's proposed topology is browser → Canvas server `/api/runtime/*` → existing owner adapter over a private process/internal RPC channel. The browser and Canvas API use exactly the same scheme, host and port: pilot origin `http://127.0.0.1:3000`, or one alternate port explicitly recorded at admission if 3000 is occupied. No separately exposed browser-facing gateway port and no hosted-page-to-localhost execution are included. Local operator pairing/authentication happens through the supported owner flow. Keep provider credentials in the supported OS/provider store, outside browser storage and rendered state. The authenticated application session needs CSRF/replay protection, exact origin/host checks, narrow tool scope and a visible disconnect. Any later remote surface needs a separately verified authenticated gateway and scoped data transfer.

Before C, the gateway maker and an independent security reviewer must assess a small concrete threat model and test plan: DNS rebinding and unexpected Host/Origin refusal; CSRF/replayed command rejection; pairing credential theft/revocation; confused-deputy scope escalation; compromised source/generated-card payloads; and wrong-principal responses. Use the exact reviewed production build, bind to loopback, and verify the admitted host/port at startup; refuse a collision or mismatch instead of choosing a silent fallback. Record the free port before launch and reuse the current server lifecycle/TTL owner. Require supported owner authentication and revalidate effect scope at execution. Use fixed commands/argv and bounded output paths through repository gates. Remote pairing, LAN access and browser private-network behavior stay deferred until independently reviewed. These controls are a design requirement, not evidence of an installed gateway.

C admission must also record disable/rollback behavior: turn off the pilot runtime route and deny new `/api/runtime/*` commands; revoke only pilot-scoped grants; checkpoint and drain/cancel only its owned runs under their cancellation policy; stop its owned server/workers. Keep artifacts, native histories, accepted Canvas editing and the shared tool plane available. Verify disabled-route denial and restart from the checkpoint. Shared configuration and other tasks remain untouched.

Do not scrape every app or silently consolidate transcripts. Read supported metadata and selected sources; preserve unavailable ChatGPT/cloud histories as coverage gaps. Each native app remains usable independently. Context handoff and returned artifacts are portable, even when lifecycle APIs differ.

A capable lead should handle coherent tasks. Add independent workers only for genuinely separable outputs with exclusive files and current machine/account admission. Add independent provider review for consequential deliverables. Swarms require fewer collisions, better accepted output, or reduced elapsed work to justify their orchestration overhead. Measure those gains against the same task with one capable agent.

Maintain four bounded loops through the existing loop owners: (1) fresh observations to useful operator exceptions; (2) scoped source intake to cited knowledge candidates; (3) admitted creation work to inspected artifacts and delivery receipts; (4) explicit rejection/failure evidence to evaluated improvement proposals. Each loop needs trigger, owner, read/write scope, deduplication, freshness, budget, deadline, stop condition, receipt and recovery. Scheduled activation remains a separate authorized action. New configurations remain candidates until exact installed behavior is observed.

## 9. Vertical products, web design and content

A vertical contributes its vocabulary, evidence sources, finished artifacts, permissions and acceptance rubric. The shared experience provides capture, scope, editing, inspection, run/recovery and export. Version domain extensions through their existing product owners. Avoid a universal form that flattens every product into the same task list.

For website creation, carry the accepted brief, audience, design tokens, content hierarchy, source assets and CTA behavior into a real editable page. Review at an existing preview with desktop/phone, loading/error, keyboard and motion checks. Preserve visual generation sidecars, both required ledgers, rights and source hashes. A screenshot or generated JSX alone does not finish the customer workflow.

For content, keep source-linked claims, an editable manuscript/package, brand voice, revision comparison, exports, asset provenance and destination-specific previews. A publication requires its actual destination receipt and applicable human approval. Learning records accepted and rejected work without silently rewriting brand rules.

For sustained rich-text editing, Tiptap with Yjs is a candidate once the current editor/export path proves insufficient. Yjs helps merge document edits; it does not resolve disagreements about claims, decisions, permissions, canon or release approval. Those need explicit review. Preserve checkpoints and portable Markdown/JSON. Evaluate open-source features separately from paid Tiptap services and extensions. [Tiptap collaboration extension](https://tiptap.dev/docs/editor/extensions/functionality/collaboration), [Yjs](https://yjs.dev/).

The scalable commercial shape follows the current installable/BYOK doctrine: portable workflow and domain packs that run in the buyer's environment, with useful defaults, self-service repair, upgrades and rollback. Optional user-owned cloud infrastructure is a deployment choice. Any future managed multi-tenant offering needs a separate accepted product decision and cost model.

## 10. First complete build and experience blueprint

Begin with one source-backed GenCreator campaign as the first build example, then use three distinct campaign tasks for the exploratory B pilot, aligned with Command #48's eventual three-accepted-campaign gate. Pilot acceptance is not a claim that those campaigns already exist or satisfy the commercial gate. B delivers the real editable campaign/page artifact, scoped context packet and edit/export recovery. C completes bounded agent dispatch, returned revision, independent review and session recovery, then uses three fresh matched tasks with counterbalanced order rather than replaying practiced tasks. Together B/C prove the first complete journey; B alone cannot establish multi-app coordination savings. Publication remains a separately authorized effect.

| Stage | Human | AI/agents | Systems |
| --- | --- | --- | --- |
| Choose outcome (B) | Select existing product, result and acceptance; supply any missing constraints | Propose a bounded next action using the product's actual sources | Existing product record and objective/work projection |
| Assemble context (B) | Select source nodes; inspect omissions and private scope | Extract cited material and flag reference-only sources | Canvas ingest/artifact/chunk records and memory read interface |
| Create and edit (B) | Edit the deliverable and accept/reject proposed changes | Produce a usable draft or patch through existing admitted creation actions | Canvas artifact/version/export path; product-owned checkout or preview |
| Prepare execution (C) | Review exact scope and any genuinely required decision | Compile task and capability needs | SIS work/admission owner; current worker/provider/budget ledger |
| Execute (C) | None for the admitted bounded step; inspect or request cancellation when needed | Work within exclusive outputs and budget; checkpoint | Native runtime adapter and existing tool plane |
| Verify (B artifact; C run) | Judge the artifact against the outcome; retain rejected versions when useful | Independently review the exact artifact/revision | Existing eval/review receipts; source and preview evidence |
| Deliver (C, if authorized) | Approve publication/release where the product's policy requires it | Execute only the reviewed effect under current authority | Product release owner and actual provider/destination receipt |
| Learn (D, after schema acceptance) | Correct facts/preferences or reject the result | Propose memory and eval updates with provenance; B performs no new durable-memory writes | Existing memory candidates and evaluation owner |
| Failure: source unavailable (B) | Choose replacement, attach text, or continue with stated limits | Preserve prior context; identify the missing source | Canvas source readiness and intake receipt |
| Failure: provider or budget unavailable (C) | Choose a tested permitted route or defer the work | Keep artifact/checkpoint; do not silently switch account mode or scope | Capability/admission owner and portable handoff |
| Failure: interrupted session (C) | Inspect checkpoint and choose resume/cancel | Reconcile native state and receipts before continuing | SIS continuity and native adapter |
| Failure: stale edit (B) or approval (C) | Resolve revision conflict and review the changed proposal | Preserve both drafts; invalidate stale release authority | Artifact revisions and effect-boundary checks |
| Failure: ambiguous publication (C, if authorized) | Review the reconciliation result if unresolved | Query destination before retry; retain unknown-effect hold | Delivery receipt and adapter reconciliation |

Blueprint method applied from AI Architect: [experience-blueprint](https://github.com/frankxai/ai-architect). Generated by AI Architect · https://www.frankx.ai/ai-architect

## 11. Delivery sequence and acceptance

A is a small documentation/identity reconciliation step. B is the first product-code slice and stays inside the accepted Canvas. Its source inputs do not require a new integrated suite, gateway or all-machine collector. Keep contextual links as the integration boundary until B demonstrates value.

| Increment | Concrete result | Gate before proceeding |
| --- | --- | --- |
| A: reconcile the read model | Exact-revision identity/source contract and existing contextual links; no new shared view or broker | Preserve owners; obtain SIS-owner acceptance of join/conflict/freshness rules and missing-identity fixtures. Name an independent artifact scorer and verifier and pre-register the exploratory B/C pilots. Respect #62's separate build gate. |
| B: finish the creation artifact | One source-backed editable campaign/page package with comparison, selected context export, save/reload and repair | Actual output accepted; cited source/scope tests; no lost edits under failed save/import, stale tabs or source drift; exact-revision keyboard/focus/touch/reduced-motion/interruption/graph-list checks. Exploratory paired artifact score is equal/better and median active creation/edit/repair time does not increase. No new durable-memory writes. |
| C: prove one runtime loop | Sink-only fault suite first, then scoped Codex execution with text-only Claude review, returned artifact/receipt, restart and cancellation tests | Current admission; recorded owner/backup availability and effect class; independently reviewed same-origin threat model; accepted state mapping; fourteen fault traces per execution adapter; disable/restart proof; actual two-harness continuity acceptance where claimed; exact-revision control accessibility. Exploratory coordination gate: median active coordination/review time at least 30% lower with equal/better accepted artifacts and no recovery/privacy regression. |
| D: integrate further only if earned | Add the most useful shared view or second vertical with its own artifacts/rubric; optional catalog UI pilot under written admission | B/C beat their fixed baseline; trace source/owner/blocker/next decision in under thirty seconds; graph/list parity; repeat-use and buyer evidence; owning memory schema before promotion; no paid launch without its current release gate. |

These are dependency-ordered increments, not a committed timeline. Fresh admission and free owner lanes determine execution. Existing continuity, graph, campaign and console issues remain open until their complete acceptance is met.

Pre-register separate exploratory pilots: B measures creation/context/edit quality and active edit/repair time; C measures full coordination/review and runtime recovery against the native-app/Markdown baseline. Use identical source snapshots, acceptance and cost ceilings. Proposed operator/acceptance judge is Frank; A must appoint and record an independent artifact scorer and verifier before collecting pilot results. Neither role was appointed in this proposal. Give the scorer presentation-normalized artifact copies without workflow-revealing metadata, with a separate sealed provenance audit for the verifier; record any failed blinding. Counterbalance order and label the three paired tasks exploratory. Use interaction/dispatch timestamps for active work time and preserve Frank's acceptance judgment separately. Record accepted artifact quality, elapsed time, edits/repairs, app/context switches, token use, actual or unknown cash cost, and recovery after the same relevant injected interruption. The proposed default C threshold is 30% lower median active coordination/review time with equal/better accepted artifacts and no recovery/privacy regression. A freezes that threshold and its measurement rules before the pilot; any later change requires a new pilot rather than moving the goalposts. Three pairs can justify a next pilot; they cannot establish general savings or commercial proof.

Stop criteria: if B fails its creation/quality/edit-recovery thresholds, retain useful artifacts and contextual links, stop C/D expansion, and repair or reject the product hypothesis. If C fails its coordination/quality/runtime-recovery thresholds, preserve useful B improvements and links and stop new shared views or wider runtime integration. Do not add more departments or protocols to explain away failure. Expand measurements with real repeat users before claiming savings publicly.

The Increment C fault-injection suite uses owned test workers and a deterministic effect sink, plus a separately admitted safe real-adapter check. Codex is the first execution adapter and owes fourteen fault runs. Claude is a text-only review adapter with no filesystem/tool permissions; it needs privacy, permission-denial, schema, deadline/cancellation and usage tests, and owes the execution suite only if future scope makes it an execution adapter. For every implemented execution adapter, run each case below twice from clean checkpoints. Planned suite: seven cases × two repeats = fourteen runs per execution adapter.

| Injected fault | Required pass observation |
| --- | --- |
| Lost response after external effect | Reconcile receipt; effect sink records one effect; no blind replay. |
| Replayed/out-of-order/duplicate events | Stable identity and revisions; no duplicate dispatch, artifact overwrite or effect. |
| Owned worker interrupted at checkpoint boundary | Resume from the verified checkpoint or expose a hold; preserve accepted edits. |
| Provider unavailable or budget exhausted | Stop new calls at the ceiling; preserve context/artifact and expose an available permitted recovery. |
| Expired lease or stale artifact approval | Deny the new effect and require current authority; retain the proposed artifact. |
| Cancellation races with completion | Record request/acknowledgement and any completed effect accurately; no resumed action after acknowledged cancellation. |
| Receipt cannot be reconciled | Fake-clock trace reaches hold at the two-minute/three-read limit, notifies the owner, exercises fifteen-minute backup or no-backup hold and daily reminder behavior, and denies automatic release; acknowledgement alone never releases. |

Pass requires all fourteen traces per adapter, zero duplicate effects in this test matrix, no lost accepted edits, and the expected denial/hold states. Record the adapter/runtime, source and installed revisions, fixture version, effect receipts, reviewer and remaining gaps. This bounded suite does not prove universal exactly-once behavior or production safety.

Each increment records its source and installed/deployed revision separately. B covers edit recovery, wrong-scope source/refusal tests and creation accessibility; C covers replay/effect recovery and runtime-control accessibility; D covers the thirty-second shared-view task and graph/list parity. React Flow's built-in accessibility helps but does not replace the list alternative or actual testing. [React Flow accessibility](https://reactflow.dev/learn/advanced-use/accessibility).

Command #48 already requires three accepted campaigns and a paid design-partner commitment before expansion. Carry that gate forward. Preserve list views or native tools wherever the new surface fails the comparison.

## 12. Alternatives and remaining evidence

| Alternative | Strength | Decision |
| --- | --- | --- |
| Native Codex/Claude apps + Markdown/Obsidian + existing issue/preview tools | Strong editing and agent features, little new infrastructure; founder performs coordination | Mandatory benchmark and recovery fallback. Starlight must demonstrate a coordination/quality advantage. |
| Extend only Command Center into every creation and knowledge workflow | Existing portfolio views and oversight work | Retain its job; prefer the accepted Canvas creation implementation for source/artifact work. Complete the #62 candidate comparison before consolidating its console role. |
| Hosted generic agent workspace | Centralized onboarding and service operations | Does not fit the current local/BYOK doctrine without a new product decision. |
| New fully generated interface, new graph store and a swarm framework for every app | High flexibility and large experiment space | Defer broad adoption until one real task beats the stable experience and current authority boundaries. |

Unverified: live continuity adoption across two harnesses/devices; full runtime adapter coverage and entitlements; installed artifact revisions; remote gateway and scoped sync; commercial demand/pricing; baseline savings; proposed new library suitability; visual and interaction acceptance of future screens. The applicable independent provider review must identify the exact proposal hash and its limits. No screenshots, generated imagery or UI code were produced in this slice.

Skills selected and read: Emil design engineering, experience blueprint, official OpenAI documentation, humanizer. Applied: stable high-frequency interactions, accessible recovery/inspection requirements, the human/agent/system failure blueprint, current native lifecycle source selection, and edited prose. Verified here: source/issue observations and repository routing for the document lane. Reduced motion, focus, touch and interrupted transitions are specified acceptance criteria; they have not been behaviorally tested on a changed interface because no interface was changed. Automatic design-scan notices do not constitute UI verification.

Issue homes: [Command #62](https://github.com/frankxai/starlight-command-center/issues/62), [Command #48](https://github.com/frankxai/starlight-command-center/issues/48), [Command #45](https://github.com/frankxai/starlight-command-center/issues/45), [Command #40](https://github.com/frankxai/starlight-command-center/issues/40), [memory #20](https://github.com/frankxai/starlight-memory/issues/20), [Canvas #33](https://github.com/frankxai/starlight-agent-canvas/issues/33), [Canvas #27](https://github.com/frankxai/starlight-agent-canvas/issues/27). No new competing objective or backlog was created.

## 13. Visual direction after Frank's 7 October review

Frank rejected the plumbing-led presentation: no images, inadequate design choices and approach, and insufficient comparison with competitor interfaces. That rejection changes quality evidence. Canvas45's source CI still verifies its stated behaviors; it does not establish an accepted product experience. Preserve its useful provider/recovery work while changing the design sequence.

The recommended experience is a decision-focused founder home connected to an artifact-focused studio, with contextual knowledge inspection and explicit agent work. The first screen helps the founder decide what deserves attention and continue meaningful work. The studio gives the actual page, document or code change most of the working area. A relation view supports answering a specific question about sources or dependencies. Product/knowledge/agent integration should be judged through this journey before broader dashboard expansion.

### Competitive references and what to adopt

These are publisher references inspected on7October, not authenticated customer app sessions or a comprehensive competitive audit.

| Reference | Observed pattern | Starlight design choice |
| --- | --- | --- |
| [Linear initiatives](https://linear.app/docs/sub-initiatives) and [agents](https://linear.app/agents) | Nested work, compact ownership/status columns; agent contributions retain a human assignee | Clear work hierarchy, quiet operational density, visible accountable owner and inspectable agent contributions |
| [Notion custom agents](https://www.notion.com/help/custom-agents) and [connected AI workspace](https://www.notion.com/product/ai) | Familiar navigation, searchable agent records, connected context and model controls | Let the founder find durable objects and inspect agent configuration without learning a separate orchestration vocabulary |
| [Figma Make](https://www.figma.com/make/) | Code-backed, visually editable artifacts; design context, version history and annotations | Keep the deliverable dominant, select an element and propose a scoped change, preserve prior versions for comparison |

Actual unmodified Linear and Notion reference PNGs were downloaded from their publishers and visually inspected. Private files `linear-initiatives-reference-20261007.png` and `notion-agents-reference-20261007.png` under `.starlight/tmp/` have source URL/time/hash reference companions. The Figma page was inspected as documentation; its image fetch failed. No authenticated Figma editing session, quota, editable design file or live competitor interaction audit is claimed.

### Considered layout alternatives

| Approach | Useful for | Tradeoff | Decision |
| --- | --- | --- | --- |
| Decision-focused home | Running several products and deciding what to review next | Needs trustworthy prioritization and careful density | Default entry in existing Home/Command ownership |
| Artifact-focused studio | Creating websites/content or reviewing a concrete implementation | Less suitable for the whole portfolio at once | Primary working surface inside accepted Canvas creation ownership |
| Graph-first workspace | Investigating dependencies, conflicting evidence and context | Large graphs can require substantial interpretation before action | Contextual knowledge mode, with search/list parity and a focused subgraph |
| Chat-first workspace | Rapid questions and initial exploration | Long transcripts can obscure versions, state and the deliverable | Retain chat as contextual input and a supported native-app fallback |

The original concept board shows the first two views and a mobile decision view. It uses current Canvas/Starlight tokens, sentence case, quiet chrome and a contrasting artifact artboard. Other products keep their accepted brand and task experience; shared identity, components and interaction conventions do not require identical visual skins.

The board is a generated raster design concept with illustrative work states, not an implemented app, real agent telemetry or customer-approved design. First output was inspected and one factual-cleanup edit removed invented identity text/source count and adjusted the sample CTA. No second aesthetic-polish loop occurred. Final image is `C:/Users/frank/.codex/generated_images/01a113ec-1c95-70a0-84eb-ae2b8aae03a3/exec-4cde4d62-89eb-476b-8a0c-00cdc5fca916.png`, SHA256 `c64a9d87dd96699db604733ce8b7174a80268b3e4dc1063c3082cc7541291152`, with its adjacent `.vis.provenance.json`. Exact prompts, input-image hash, provider and session are recorded, and both central ledgers were appended/read back. Built-in image_gen did not report model/seed identities; they remain explicitly unknown. The external VIS schema could not be retrieved; schema validation and memory-vault synchronization are pending. The image is preview-only and is not an app asset or public release.

### Architecture dictated by the interaction

The shared conceptual objects are Product, Work, ArtifactVersion, SourceObservation, Decision, AgentRun and Memory. Map them to the existing owners' canonical identities and contracts before implementation. An artifact version carries its content/hash, supporting sources, work association and review state. A decision references the exact reviewed version. Agent runs propose new versions and report observations; they do not silently replace accepted work. Retain original goals, native IDs, provider namespaces and source freshness. A title never establishes identity.

The UI should make this chain navigable: product outcome → work → artifact version → source observations → proposed changes → reviewed decision → accepted handoff → resumable work. Knowledge relations and retrieval are projections of authoritative records; a useful graph is rebuildable, scoped and inspectable. Memory needs origin, scope, timestamp, supersession and deletion semantics, with conflicting observations kept visible. Retrieved summaries are not source authority. Permission/filtering belongs before retrieval as well as rendering.

Use a stable, accessible application shell and tested artifact viewers. Let models generate bounded content and propose permitted changes within those viewers. New UI composition should be limited to reviewed components and typed actions. Arbitrary model-generated executable UI, credentials or unreviewed actions must not enter the stable founder shell. Contextual suggestions can change; navigation, recovery, accepted versions and ownership remain predictable.

The agent work view needs plain states for queued/running/needs review/cancellation requested/cancellation acknowledged/recovery hold, mapped to actual canonical events. A stop button is not proof that execution stopped. Each supported adapter needs run identity, heartbeat/freshness, scoped permissions, budget, checkpoints, artifact references and effect receipts. Codex/Claude/OpenRouter retain their own account/entitlement boundaries. Shared context packets and explicit handoffs are the first integration; unseen chats or unsupported native controls are not implied.

Loops follow the same work: observe → propose → execute within admitted scope → verify → review or reconcile → retain the artifact and next useful context. Put limits on concurrent work, time, spend and founder interruptions. Reconcile effects before retrying a lost response. Escalate when evidence conflicts or stops being fresh. Reuse the current owner/runtime contracts and existing durable recovery before selecting another workflow framework. Event journals support recovery; adding a queue does not establish it.

### First useful build and design workflow

1. Design the same real task in the selected approaches: take retained product sources, create a website direction, compare its complete page, edit the artifact, save/reload, make a human choice and recover the selected export. Use the native app plus Markdown workflow as the baseline. For content, use the same object/version/source model with an editorial viewer; for knowledge, inspect the supporting claims and conflicts.
2. Translate the selected visual direction into editable components/states in the existing design and code system. Reuse current Next/React, tokens, canonical store, bounded provider adapter and provenance controls. Use current Figma design context/Code Connect where access is confirmed. Browser previews are the behavioral artifact; generated images remain proposals. Do not replace accepted Canvas first-screen source intake with the concept's portfolio home.
3. Build the complete Canvas studio journey first, then contextual links into existing Home/Command and Observatory. Maintain one selected work/artifact identity across app boundaries and explicit scope on each link. Wider shared pages follow measured benefit; no new shell, graph store, task queue or rebranding is implied.
4. Inspect real375/768/1440 views and reduced motion, keyboard/focus, touch targets, interrupted transitions, loading/empty/conflict/offline states and return after reload. Frequent keyboard actions should respond immediately. Content transitions should not move the artifact unexpectedly; focus and draft recovery must survive dismissal/interruption. Independent exact-source/image review and founder feedback follow actual previews.
5. Compare completed output, editing/repair effort, time to find the next decision, repeated briefing, app switches, recovery and actual reported cost on the same task. Qwen3.8 Flash is a cheap structured-generation candidate, not evidence of quality; Gemini and the native drafting alternative remain comparisons. Repeat with real users before commercial or scale claims. A billion-dollar outcome depends on market demand, distribution and economics as well as operating capacity.

Selected/read/applied: installed Emil design engineering for layout/interaction requirements, native imagegen for the board and one correction, humanizer for prose, shared memory and accepted token reads. Verified: visual inspection of the actual board and two publisher screenshots; image/sidecar hashes and both ledger identities. Not verified: interactive prototype, focus/touch/reduced-motion/interruption behavior of these new screens, current independent visual review, founder approval, live provider generation and cross-app native execution. Preserve the original proposal/review scope and all open runtime/customer gates.
