TL;DR: The portable CLI is verified in production and the draft-CI cost fix is merged; the next product gate is a real authenticated creator journey, with G2-G6 still open.

## Current execution update, 11 October 2026

Frank resumed implementation after the historical planning snapshot below.
The [current execution prompt](gencreator-starlight-execution-prompt-2026-10-11.md)
and [capabilities record](gencreator-capabilities-2026-10-11.md) govern the next
step. Earlier pause, budget-block and unexecuted-client statements below describe
the planning snapshot; they do not pause his resumed instruction.

G1's CLI release PR201 merged as `47a798a`; candidate and receiving-main full CI,
source-bound production/domain checks, exact published0.5.3 archive and the
downloaded Windows13-step/three-live-call consumer proof all pass. Public smoke
passes22 checks. PR201 used a validated independent exact-source substitute
after manual native requests hit a quota limit, preserving all21 earlier
findings and every actual configured gate. The historical requirement for that
specific native service is superseded by the current repository review contract
and documented execution evidence; it was not a branch-protection requirement.

CI cost PR202 merged as `f12797b` after refresh/source review against `47a798a`.
Its draft ran only the slim aggregate and rejected the four skipped dependencies;
marking ready ran all five successful jobs.34 local cases, exact independent
source review and automatic native code/security reviews passed at `3078739`.
The receiving-main run is [38095053367](https://github.com/frankxai/gencreator.ai/actions/runs/38095053367);
its successful result remains a release requirement and the final observation
belongs in the current session handover. No measured overall savings are claimed.

Supabase sessions plus explicit Starlight linking is settled. Managed namespace,
server/OAuth credentials, backup/recovery, retention/delete, real two-account
acceptance and creator judgment remain unfinished. Fresh swarm admission still
prohibits new parallel agents despite recovered RAM; use the one local lead and
existing remote review/check services. Keep the phased writers, client adoption
and commercial goals below, with existing owners and clean sequential merges.

## Historical planning snapshot

TL;DR: Use one Codex coordinator, two implementation lanes at a time and an independent reviewer; finish the pending release, prove one authenticated creator journey, then extend its tested contracts into clients, apps and the commercial offer.

Frank requested this planning package on 11 October 2026. Native goal `01a123db-5493-7220-8d0d-f80760cad443` remains paused. This document defines proposed execution; it starts no workers and authorizes no billing, migration, merge or deployment. The full CLI, SDK, ADK, desktop, mobile, platform, API, router, memory, cloud, adoption and subscription programme remains open.

The first customer outcome follows GenCreator's accepted ADR-007 and ADR-010: an expert brings owned sources and a guided conversation, gets source-linked work in their own voice, edits it, approves exact revisions, exports it and recovers after interruption. The 30-minute first useful artifact is the accepted product target, with actual time still to be measured. Preserve the accepted Studio, director recovery and host-revision implementations.

**Current evidence and constraints**

GitHub observations were refreshed late on 10 October UTC, which is 11 October in Amsterdam. Re-query before execution; these heads are snapshots.

| Repository | Remote main observed | Candidate or ownership constraint |
| --- | --- | --- |
| `frankxai/gencreator.ai` | `e54006250334734d31d09efbb8ffdd66fad60e1c` | [PR201](https://github.com/frankxai/gencreator.ai/pull/201), `a7cc25f62867bd45e94f6033c0021db19ba41d94`, open and blocked. Canonical checkout belongs to another lane and contains untracked work. |
| `frankxai/starlightintelligence.ai` | `1f1ff7eb595189082b7ae429c30579652d36a65a` | [PR110](https://github.com/frankxai/starlightintelligence.ai/pull/110), `a55c5cb0b53acba390e224e4a27f9039c9991e14`, belongs to the Starlight delivery task. It proposes Supabase auth; its live activation remains pending. |
| `frankxai/Starlight-Intelligence-System` | `6bbf3a17c6b1aaa089045fffa441df5158a407b3` | Reuse published SDK8.5.1 after fresh registry/source verification. Canonical checkout is Antigravity's `agent/antigravity/npm-ecosystem-alignment`, with dirty foreign work. Its local package says8.3.0 and is not the published baseline. |
| `frankxai/starlight-creator-mcp` | `ffdbdc68d95ef318c69c729347f0ad7a94917545` | [PR6](https://github.com/frankxai/starlight-creator-mcp/pull/6), `ebf0f6337d1485519c6c416775e546cc7e9b035b`, has a separate publisher. Canonical `agent/claude/publish-readiness` is dirty; root agent guide was absent there. |
| `frankxai/starlight-memory` | `c532743d1a6c101e8a4167e09e49e2714f05f080` | Memory owner and scoped instructions must be inspected before admitting a write. No write lane assigned by this plan. |
| `frankxai/agentic-ops-hub` | `0dff5f2318bb4c921a019a0f1540bdd58bcd68a0` | This package uses the existing coordinator-owned worktree and draft [PR245](https://github.com/frankxai/agentic-ops-hub/pull/245). Primary checkout is Hermes's branch. |

PR201 has 116 passing local focused tests and two exact-source Poolside static reviews. Current full CI, current native review and extracted-client execution still need completion. The successful thirteen-step client proof belongs to earlier `79966f9`; current `a7cc25f` attempted zero steps under RAM hold. Published plugin0.5.1 and candidate0.5.3 remain distinct. The last source-bound production observation was READY at GenCreator main `e540062`; this planning turn refreshed remote main, not the deployment or customer journey.

Fresh `pp preflight --workload swarm` returned HOLD: 4,220 MiB free against a 10,240 MiB swarm requirement, eleven task runtimes against eight, and `pause-new-swarms`. Use one local coordinator for small reads and planning. Admit local writers only after a fresh preflight permits them; respect the 4 GiB floor and storage admission. A cloud checkout is an option only after actual account access, quota, data handling and cost admission are verified. A GitHub branch is not a running cloud worker.

GenCreator's Actions budget blocks release CI. The spending-cap question remains unanswered. Restore the existing budget or obtain a concrete spending authorization; do not repeatedly dispatch blocked jobs, change billing or bypass checks. GenCreator currently requires strict `CI Status` on main, but admin enforcement is disabled. The coordinator must use ordinary protected merges without admin bypass; stronger repository enforcement is a separately reviewable change. Hub requires `verify` and enforces admins; its latest existing-head CI passed, independently of the product budget.

Frank's identity decision is settled: keep GenCreator Supabase sessions and explicitly prove Starlight account links. Preserve PR196. Starlight PR110 is a separate candidate, so its proposed auth must not be described as deployed. Do not infer a link, membership, entitlement or source rights from matching emails. Prepared additive SQL, production migration approval, schema exposure, SMTP/credentials and real-account acceptance remain separate conditions.

**Goals and completion evidence**

| Goal | Bounded result | Done when | Dependency or stop condition |
| --- | --- | --- | --- |
| G0: establish release inputs | One refreshed source/owner/gate matrix; admitted execution lanes | Exact main and PR heads, instruction hashes, lease owners, branch protections, deployment source, package provenance and machine/cost admission recorded | Keep implementation paused until Frank resumes it. No occupied checkout takeover or invented cloud capacity. |
| G1: finish the existing release | PR201's CLI and plugin reach accepted main and production | Full candidate CI and required current reviews pass; current extracted candidate proves the real source/edit/recovery workflow before merge; receiving-main CI, production source/domain binding, live archive bytes and published consumer proof pass afterward | Actions budget, RAM admission or a real defect holds this release. Earlier-head evidence cannot clear it. |
| G2: activate a scoped managed alpha | Real Supabase sessions, explicit Starlight link and durable creator work | Two distinct actual accounts prove login, membership, link/cancel/retry/revoke, cross-tenant denial, idempotent save/readback and interruption recovery. Export, disconnect and a reviewed retention/delete path work with sealed audit constraints | Prepare a concrete migration/configuration packet first; apply only with the recorded production migration authorization. Keep managed routes unavailable until configured. Coordinate Starlight PR110's owner. |
| G3: prove valuable creator work | One source-to-constellation journey through the accepted Studio/Eve paths | A consented expert receives a usable newsletter or long-form draft, social sequence and script/brief with traceable claims, voice, rights, revision review and export. They edit and accept at least one artifact. Provider outage, duplicate retry and interrupted recovery preserve authored work | Compare the same brief with the creator's native assistant plus Markdown/manual process. Record time, repair effort, owner judgment and observed usage; no superiority claim without results. |
| G4: connect developer and agent clients | Existing CLI/plugin, published SDK, ADK recipes and creator-MCP consume the same accepted contract | Independent cold installs, real authenticated scoped calls where applicable, actual native assistant use, version negotiation, cancellation and restart pass. One receiver imports/edits/exports the same artifact without losing provenance or approval state | Package publishing/OIDC bootstrap has its own owner and approval. Keep the public stateless transform distinct from authenticated persistence and human approval. |
| G5: prove desktop/mobile and memory continuity | Desktop and phone can resume the same scoped creator work; native-app deliverables stay tracked | Actual desktop and phone login/edit/reopen/export pass; selected native desktop/mobile implementations are installed and exercise the same contract. Tenant-scoped memory recall, deletion/expiry and conflict recovery pass | Responsive web is a first test surface, not evidence of a native app. Choose packaging from installed implementations and user needs before creating another shell. |
| G6: validate adoption and the paid offer | An evidence-backed onboarding, community and subscription offer | Consented alpha users complete the workflow; demand/support/retention and actual unit costs are recorded. Entitlement reconciliation, cancellation/refunds, webhook retries and limits pass before checkout. A reviewed offer names contracting entity, license and provider account mode | Accepted Pro/Team prices and margin/onboarding figures remain hypotheses or targets. Personal AI subscriptions do not establish managed API/resale rights. Public payments, publication and paid provider effects retain their approval gates. |

G1 is the next release task. G2 and G3 form the first managed product milestone. G4 follows stable API contracts, while G5 and G6 stay explicit parts of the programme. A blocked gate may permit independent reversible preparation; it does not justify marking a dependent goal complete. The programme closes only after all goals have their own evidence or Frank explicitly changes its scope.

**Team and waves**

Keep one lead. Use the current Codex lead for coordination, architecture, source ownership and integration. Reuse the repository's backend, frontend and QA/release agent briefs. A role name does not establish an installed model or account entitlement; verify each harness before admitting it. Independent review uses a different provider from the maker when available under the actual privacy/cost contract. This planning package receives one bounded Poolside static review, not a spawned local swarm.

| Lane | Responsibility and ownership | Output |
| --- | --- | --- |
| Coordinator/integrator | Own the programme queue, shared interface decisions, receiving-main checks and normal merge order. Write only its admitted files; never share a writer's index. | One current dependency/gate record, reviewed receiving PRs and source-bound release receipts. |
| A: identity/data | `gencreator-backend-engineer` brief. Own admitted GenCreator auth, membership/linking, persistence/API and SQL files. Coordinate with the existing Starlight identity owner. | Small auth/data PR, reviewed migration packet, actual tenant/identity/retry/recovery proof. |
| B: creator experience | `gencreator-frontend-engineer` brief with creator/editorial judgment. Own admitted Studio components/styles and UI tests; preserve accepted workflows. | One polished source-to-artifact journey, desktop/phone and keyboard evidence, export/recovery proof and creator feedback. |
| C: client/router/memory | Existing SIS/creator-MCP/package owners. Consume the ratified contract; own separate admitted package or adapter files. Consult the memory owner for its boundary. | Source-pinned cold-install and real client acceptance, scoped recall/cancellation/recovery evidence. |
| Independent reviewer | Read-only security, engineering and reliability checks of exact revisions. Add focused craft/demand review at the product/commercial gates. Cannot merge or repair a writer's tree. | Reachable findings, inspected paths, review revision, limits and a decision for the relevant gate. |

Once admitted, the active ceiling is four slots: lead, up to two writers and one reviewer. In the first wave, A and B work in separate checkouts after their interface boundaries are agreed. In the client wave, C replaces a finished writer; this is not a fifth concurrent agent. Craft and commercial specialists use a freed review slot for a bounded task. Builds and browser tests are separately admitted and scheduled so idle roles do not become competing heavy processes.

The lead freezes the smallest shared interface packet before concurrent edits: identity/workspace context, artifact/revision IDs, source/right/approval bindings, operation receipt, idempotency and error/recovery behavior. Existing schemas remain authoritative. Each task lists exact files and tests. Shared `lib/creator-studio/project.ts`, generated bundles, lockfiles and migrations have one owner each; any boundary change is sequentially reassigned before edits. New agents are told they are not alone and must preserve other owners' work.

**Checkouts, branches and integration**

Local canonical repos remain under `C:/Users/frank/starlight/repos/`. Assigned worktrees remain under `C:/Users/frank/starlight/worktrees/`. Each cloud writer needs its own isolated checkout of the same verified GitHub origin and immutable base, with no production credentials. GitHub hosts the branch and PR; a worktree belongs to the worker's machine or environment.

| Work | Checkout | Branch and target | State |
| --- | --- | --- | --- |
| Finish current GenCreator release | `gencreator-agent-release-20261010` | `agent/codex/revision-cli-20261010` → `gencreator.ai/main`, PR201 | Existing coordinator-owned lane; retain its fourteen-file scope. |
| Save this plan/handover | `hub-gencreator-agent-release-20261010` | `agent/codex/revision-cli-20261010` → `agentic-ops-hub/main`, draft PR245 | Existing owned lane; planning documents only. Product goal stays paused. |
| Starlight auth | `starlight-platform-delivery-20261010` | `agent/codex/starlight-supabase-auth-20261010` → `starlightintelligence.ai/main`, PR110 | Existing foreign task; coordinate through its owner and issues82/95. |
| GenCreator identity/data | `gencreator-managed-alpha-20261011` | `agent/codex/managed-alpha-20261011` → `gencreator.ai/main` | Proposed, not created. Base from fresh accepted remote main when admitted. |
| GenCreator creator experience | `gencreator-creator-journey-20261011` | `agent/codex/creator-journey-20261011` → `gencreator.ai/main` | Proposed, not created; separate index and explicit files from A. |
| Client integration | `sis-gencreator-adoption-20261011` | `agent/codex/gencreator-adoption-20261011` → `Starlight-Intelligence-System/main` | Proposed, not created; agree with existing SIS owner first. |
| Creator-MCP release | Publisher's existing isolated checkout, verified at admission | `agent/codex/creator-npm-release-20261010` → `starlight-creator-mcp/main`, PR6 | Existing separate owner; do not use dirty primary checkout or republish an existing version. |

Use `codex --cd <verified-repo-or-owned-worktree>` for new repository sessions. Existing sessions explicitly read the destination root/deeper instructions and record hashes; a shell directory change does not reload native instructions. Run routing guard and explicit-file check, then inspect ownership separately before each write/stage transition. Fresh storage admission precedes worktree creation or dependency installation. Missing required guidance blocks dependent writes; recover it through the indexed owner before assigning that lane.

All receiving branches are the repositories' actual `main`, freshly verified. Avoid a long-lived cross-product integration branch. Feature branches may start from the same accepted main, but each is updated and reviewed against the latest receiving base before normal merge. A coordinator integrates one PR at a time; it does not consolidate foreign dirty checkouts. [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) require configured status checks, and strict checks bind the receiving base.

1. Refresh the candidate head, receiving base, owner, required checks and preview source. Inspect actual logs and any skipped required jobs.
2. Run meaningful behavior/security/recovery checks and exact-revision independent review. Resolve findings in the owner's tree; new code revisions need changed-scope verification and appropriate review.
3. On an admitted machine, run the current extracted consumer before PR201 merge. After budget restoration, obtain full candidate CI and the current required native review. Use normal protected merge only when every release gate passes.
4. Confirm the resulting main revision and expected source files. Run receiving-main CI; on failure stop subsequent integrations and prepare a reviewed revert or repair in an isolated lane.
5. Verify the accepted deployment's source SHA, environment and READY state, both stable domains, critical routes and downloadable artifact bytes. Prefer existing Vercel previews and Git integration. A preview promotion rebuild uses production environment variables, so preview tests alone do not validate production configuration. [Vercel promotion behavior](https://vercel.com/docs/deployments/promote-preview-to-production).
6. Prove the real published client and configured user journey. Record source, environment, account scope, artifacts, actual results, remaining gaps and a known-good rollback. Stop only session-owned workers/watchers. Keep additive database compatibility; an application rollback does not undo a migration.

Before any live managed migration, prepare exact SQL and its hash, target project/schema, preserved namespaces/grants, backup/restore evidence, exposure/configuration changes, staged auth proof and rollback limits. Obtain the existing explicit migration/deployment approval against that packet. The Supabase identity choice alone is not that approval. Retention must address the current sealed evidence/delete constraints before a customer deletion promise.

**Existing branches and platform choices**

Keep [PR141](https://github.com/frankxai/gencreator.ai/pull/141) as a recovery/Honor-edition donor for G3; its base is another feature branch. [PR137](https://github.com/frankxai/gencreator.ai/pull/137) supplies agency production ideas, [PR148](https://github.com/frankxai/gencreator.ai/pull/148) operations/subscription planning and draft [PR162](https://github.com/frankxai/gencreator.ai/pull/162) connector work. Inventory their unique useful changes against accepted main, consult their owners and port only necessary deltas with provenance into a fresh receiving PR. CLEAN status alone does not establish acceptance. [PR116](https://github.com/frankxai/gencreator.ai/pull/116) touches money/security and migration002; keep its separate approval and review gates. Do not mass-merge, delete or archive these branches to obtain a tidy list.

Keep Next.js/Vercel and the accepted Supabase data plane for the alpha. Reuse the existing SIS runtime, SDK, router and memory contracts. Eve is an existing pilot whose connected-provider creation and recovery need proof. Cloudflare is conditional: add a bounded service only when a measured task needs it and the current owner, authentication, cost and operational tradeoff are reviewed. Avoid a second identity store, another canonical work ledger or a new protocol broker without an evidenced need.

This sequencing fits the current constraints because the accepted implementation already covers much of the portable workflow, the live gaps concern identity/durable recovery and creator usefulness, and several package/platform owners are active. A contract shared by one proven journey reduces repeated implementation across APIs, clients and apps. Separate checkouts limit file conflicts; sequential receiving merges expose failures before another product depends on them. The serious alternative is simultaneous work across every surface; under the observed RAM, CI and authority constraints it increases blocked work and integration risk before establishing customer value.

Every worker receives a packet containing: source issue/task, intended user outcome, verified origin/base, named owner, separate checkout/branch, exact writable files, inputs and privacy, bounded artifact, authority/spend limit, acceptance tests, independent review, stop condition and handoff. Its report includes output paths/head, executed checks with environment, failures and recovery, provider-reported cost or unknown, untested claims, remaining gaps and one next action. Record one handover and issue update per finished or genuinely blocked slice; avoid repeated prose-only revisions while a gate is unchanged.

The ready-to-run [execution prompt](gencreator-starlight-execution-prompt-2026-10-11.md) is for an explicit implementation resume. Planning used the installed `starlight-swarm-orchestration` skill. The activation hint mentioned `starlight-swarm-ops`, but no callable installed operations skill was found in the inspected locations; no dependency on it is assumed. The estate registry source was missing both from the inspected config checkout and its cached main tree. Verified Git origins/heads and existing owner records support this plan; registry repair and complete estate coverage remain open. This package is a proposed execution contract, not runtime enforcement.
