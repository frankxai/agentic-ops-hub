# Rolling company software plan

TL;DR: Maintain one capability map that points to existing product issues, use the existing Projects for visual planning, and turn research into bounded, measured adoption decisions.

Prepared 11 October 2026. This is a reusable operating proposal and read-only reporting tool. The private Registry, owning issues and accepted product sources retain authority. No new recurring job, agent assignment, infrastructure, purchase or release is installed by this document. The internal financial baseline stays in the private dossier.

Read [the capability map](company-swarm/capability-map.json), [economics](COMPANY-BUILD-BUY-ECONOMICS.md), [the engineering programme](COMPANY-SWARM-BUILD-PROGRAMME.md), [coordinator](COMPANY-SWARM-COORDINATOR.md) and [lane prompts](COMPANY-SWARM-LANE-PROMPTS.md). The map is a dated projection; its IDs identify rows in this proposal, not new Registry entities.

## The problem and ownership

The company needs working customer and creator journeys across many tools. A long tool list does not tell a worker what to build next, which record it may change, or whether last week's evidence still applies. Keep the useful business outcome attached to one accountable product issue. Attach modules, experiments and design work to that outcome.

Use the existing homes:

| Record | Existing home | Maintenance rule |
| --- | --- | --- |
| Company/product/repository identity and accepted architecture | Private agentic-ops Registry | Reviewed PR; record merged SHA in consumers |
| Cross-repo outcome or unresolved architecture decision | Existing agentic-ops issue | Link owning implementation issues; retain rejected decisions |
| Customer-facing Foundry/Business OS packaging | agentic-business-os issue 4 | Reconcile current naming/placement before implementation; preserve SIS as substrate |
| Product implementation, defect and acceptance | Receiving product's issue and PR | One implementation record; cross-repo references do not create second owners |
| Visual portfolio plan | Project 8 | Outcome and decision index over issues |
| Revenue campaign | Project 10 | Selected demand, activation, delivery and commercial work |
| Machine/model/connector operations | Project 9 | Link starlight-estate issues and runtime receipts |
| Research methods | research-intelligence-os | Reusable method/contracts; issue 3 is a lineage dependency, not all technology R&D |
| Raw experiments, finance, personal/customer evidence | Existing private dossiers/vaults | Preserve source, rights, costs, failures and access scope |
| Shared design protocol and brand packs | starlight-design-intelligence | Pin pack revision in the receiving product; issue 48 owns the current v0 import pilot |
| Reusable handover and sanitized plan | agentic-ops-hub | Session, ledger and current prompt; no private customer or financial dataset |

Observed Projects on 11 October: 8, 9 and 10 are private and active. Issue 10 and Foundry issue 4 had no Project items on initial inspection. Board fields are projections; an issue assignee or named persona does not prove a running worker. Existing schedules and workflow automation must be checked through current receipts before relying on them.

## The business layers

Each row has a job, implementation candidate, evidence qualifier, existing issue anchor and next gate in the JSON map. Several rows intentionally share an issue because they serve one outcome. Issue counts are not a measure of capability completeness.

| Layer | Current approach | Trigger for more engineering |
| --- | --- | --- |
| Portfolio, offers and customer evidence | Existing Registry, Foundry and product manifests | Conflicting ownership or a validated product needs a new contract |
| Research and technology adoption | Private dossiers plus reusable research methods | A named customer/operator task justifies a comparison |
| Intelligence, memory and agent runtime | Existing SIS/SDK, journal and scoped memory | A real journey needs better retrieval, state, recovery or host support |
| Identity, secrets and permissions | Existing authentication and secure credential owners | Actual customer/workspace isolation and revoke tests |
| Workflows and integrations | Existing durable owner per job; narrow adapters | Repeated handoff or retry failures in a useful workflow |
| Hosting and provisioning | Accepted Vercel/Cloudflare boundaries; Railway conditional | A measured workload cannot fit the current deployment |
| Storage, backup and restore | Existing asset/data owners and private R2 exception | Restore, device retrieval or workload evidence identifies a gap |
| DAM and visual curation | Existing files/tools/VIS; optional | Observed browsing/reuse/approval pain; never an automatic revenue prerequisite |
| Creator production | Existing GenCreator edition/artifact workflow | Real creator save, edit, reopen, export and acceptance gaps |
| CMS and publishing | Existing repo/content workflow | Editors need structured draft/version/approval behavior beyond it |
| CRM and sales research | Existing simple records/free tools first | Follow-ups or data quality fail at actual volume; compare adoption with custom work |
| Communications and scheduling | Existing Communications OS issue 61 | One scoped inbox or buyer/support case can be proved end to end |
| Social and distribution | Source-backed derivatives and approved exports | One selected channel merits API integration and measurable attribution |
| Commerce and delivery | Existing checkout/entitlement/product owners | A permitted order/refund/export journey must close a verified gap |
| Support and community | Existing case/community/product owners | Repeated customer questions or access failures warrant automation |
| Finance and unit economics | Provider/payment/accounting truth plus usage receipts | Reconciled cost per accepted outcome; tax/accounting requirements stay with qualified systems |
| Analytics and evaluations | Existing product/runtime telemetry | A decision needs cohort, quality, repair or margin evidence |
| Engineering and release | Existing issues/PRs/review gates | Current-source checks, update/rollback and live acceptance |
| Design and experience quality | Existing brand packs and design issue 48 | Same-task native/v0 comparison and exact-revision interaction checks |
| Customer installation, modules and updates | Existing Foundry/Business OS and SIS contracts | Outside founder can install, achieve value, update, revoke and restore |

Public websites, creator assets and business records keep their respective owners. An internal dashboard reads approved projections of those records. A desktop app is justified by offline/local-file work; a browser/PWA suits shared records. A native shell does not establish offline correctness, authority or cloud synchronization.

## Issue structure and alignment

Use an outcome issue, linked capability work in the receiving repository, and bounded implementation issues when admission actually requires them. Use GitHub sub-issues where the relationship is real; use dependency links for shared rails rather than putting one task under unrelated parents. GitHub supports cross-repository issue hierarchies and parent-based Project views: [official sub-issue guidance](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues).

Do not create twenty new epics from the twenty map rows. Search existing open and closed work, source branches and owner handovers first. A missing module can remain an explicitly unrouted proposal until its job and owner are resolved. Architecture issue 10 tracks shared choices; Foundry issue 4 tracks the customer product. Neither issue claims all dependent products have shipped.

Every admitted implementation issue needs:

1. Named user and job; internal operator or external customer.
2. Current behavior and exact desired result, including recovery.
3. Existing source, ownership and serious same-task alternative.
4. Exact repo, branch, permitted files, acknowledged maker and distinct checker.
5. Build/adopt/buy/defer decision with uncertainty, provider cash and founder hours.
6. Dependencies, rights/security boundary, benchmark and acceptance evidence.
7. Admitted time, API cash, tokens/retries and maintenance budget; stop rule.
8. Next action, next decision date and direct evidence link.

The GitHub issue remains the task. Project fields mirror it. Backlog and Ready do not imply assignment. A stale execution receipt triggers investigation and a dated handover; it does not authorize deleting work, locks, branches or automatic redispatch. Issue 175's proposed three-day board rule is an existing implementation task, not proof of a running sweep. Closing an issue or merging a PR alone cannot prove live acceptance. GitHub's [built-in automation documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations) explains why inferred Done workflows require particular care.

## Rolling review

Use the current portfolio cadence, with these additions submitted to its owning issues rather than another scheduler:

| When | Check | Output |
| --- | --- | --- |
| Before work | Refresh Registry/source/issue state, owner and budget; inspect open handover | One acknowledged issue-bound work packet |
| End of a useful slice | Record artifact/revision, actual cost/time, failure/recovery and remaining gate | Issue receipt and hub handover |
| Monday | Reconcile active outcomes, buyer evidence, dependency gaps and capacity | Few admitted outcomes on existing boards; conditional experiments |
| Thursday | Review source drift, duplicate work, support defects and changed economics | Dated Continue/Hold/Validate/Park proposal; owner acceptance where required |
| Friday research window | Review relevant upstream releases and one matched experiment | Source-bound adoption dossier, including a rejected/deferred result when warranted |
| Sunday | Close the decision window with shipped/slipped/blocked evidence | Project status update and explicit next week |
| Monthly | Reconcile invoices, API usage, useful output, repair and support hours | Build/buy continuation decisions; no assumed savings |
| Quarterly or major license/security change | Recheck dependencies, exit/restore, brand packs and product terms | Versioned update/retirement proposal and migration evidence |

An event can trigger an earlier review: upstream license/API change, severe vulnerability, failed restore, founder rejection, rising support load or a new buyer task. Until the maintenance integration has a tested owner, run the report when taking up the work. This document adds no cron.

## Research and OSS adoption

Use a candidate lifecycle: discovered, screened, experiment admitted, measured, adoption proposed, accepted through the owning review, maintained, or rejected/deferred with reason. Preserve earlier decisions; an accepted experiment does not ratify portfolio architecture.

A dossier contains: question/job, baseline, upstream URL and immutable version, package/file license map, maintenance/security condition, data and API terms, integration mode, ownership, deployment/backup burden, measured useful output, repair/recovery, time, tokens, cash, commercial compatibility, decision, reviewer, next recheck and exit path. A source snapshot or stars count is discovery evidence, not product acceptance.

Prefer these integration modes in order when the task supports them: existing operation/API, configured upstream service, supported plugin, isolated vendored component, maintained fork, then new implementation. Choose a fork only with a named upstream-update owner and conflict budget. Copying code preserves its license and attribution obligations; agents cannot erase them by rewriting names.

Start with a small shortlist:

| Candidate | Experiment and comparison | Current disposition |
| --- | --- | --- |
| Payload | Structured editorial draft/version/export against the existing Git/content workflow | Candidate when CMS pain exists; root [MIT license](https://github.com/payloadcms/payload/blob/main/LICENSE.md), dependencies still reviewed |
| Twenty | Import actual permitted contacts, track one follow-up, export/restore; compare simple existing CRM | Conditional adoption candidate; [license](https://github.com/twentyhq/twenty/blob/main/LICENSE) includes different component terms and an Application Exception; no wholesale proprietary absorption assumption |
| Postiz | Draft/approve/export one campaign and reconcile selected channel outcomes against manual/native posting | Conditional scheduler candidate; [AGPL source](https://github.com/gitroomhq/postiz-app/blob/main/LICENSE); provider access and product redistribution reviewed separately |
| n8n | One internal reversible adapter flow versus existing durable workflow | Existing tool candidate, no new workflow owner; [official use-case guidance](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case) before customer distribution or MCP exposure |
| Firecrawl | Accepted source extraction on a bounded research task against current/API/manual retrieval | Metered API versus self-host cost experiment; [AGPL source](https://github.com/firecrawl/firecrawl/blob/main/LICENSE) and hosted terms reviewed separately |
| Langfuse | Attribute actual selected-job traces and recovery/repair against existing telemetry | Candidate only for a demonstrated observation gap; inspect exact package/enterprise terms in [source license](https://github.com/langfuse/langfuse/blob/main/LICENSE) |
| v0 and existing UI components | Same real creator journey, native baseline, approved brand-pack import | Existing design issue 48 owns pilot; generated UI remains a source candidate with integration work |

These are investigation candidates, not an instruction to install all of them. No matched result or license counsel acceptance is claimed here. A self-hosted database, browser worker or container still has costs for backup, security, upgrades, delivery and operator time.

Compare twelve-month incremental costs: setup cash + API/infra + migration + expected maintenance/support + founder hours valued separately. Count all failed/review attempts and refunds where relevant. Show subscription-covered coding usage separately from additional billed API use. Do not count the same token cost twice. Keep unknown cash, exchange rates and elapsed effort unknown. Use the existing economics model; calibrate estimates through the next useful slice.

## Agent use

An agent receives the selected issue, current authority/source revisions, smallest required capability family, permitted data scope, exact write lane, budget and acceptance. It reads records through the existing tool plane or supported connector, proposes changes, performs already-authorized operations, and writes receipts. APIs, CLI and MCP adapt the same domain operation; server authorization remains authoritative.

| Responsibility | Reads | Produces or changes |
| --- | --- | --- |
| Portfolio coordinator | Issues, capability gaps, source pins, bills/outcomes in permitted private scope | Alignment and admission proposals, linked next actions |
| Technology researcher | Official docs, pinned OSS sources, prior experiments | Comparable dossier; no install or canonical promotion from discovery alone |
| Product designer | User job, existing surface, brand pack, licensed references | Candidate in the existing product, interaction evidence and same-task comparison |
| Engineer/integrator | Accepted packet, code and domain contracts | Scoped implementation, failure/recovery evidence, update/export recipe |
| Independent checker | Frozen candidate and evidence, own permitted tooling | Findings and exact-revision acceptance or remaining gaps |
| Operating agent | Current records, explicit action grants and workflow state | Permitted record changes and verified receipts; retains unknown effects |

These are responsibilities, not six permanently running agents. Use one capable lead and admit independent work when needed and supported by current machine/provider budgets. Saved prompts do not grant access, spawn workers, or make ChatGPT cloud inherit local configuration. Supported hosts must separately prove discovery, authentication, allowed operation, denial, revoke and recovery. Never expose an entire company database to every agent.

For design work, pin the shared design protocol and the receiving brand pack. v0/template/Figma output is reviewed against the real existing user task. Check desktop/mobile, keyboard, touch, reduced motion, interruption and the actual editable artifact. Store approved visuals with exact provenance, rights and placements. The current design pilot issue records account access limits; refresh them before claiming v0/Figma are usable.

## Customer-owned and open-core offering

Package the useful internal operation as a versioned module after it has proved value. Keep common schemas, adapters, portable export, test contracts and installation/update tooling reusable. Candidate commercial value is maintained industry/workflow packs, carefully licensed extensions, updates and support with a defined boundary. Pricing, hosting offers and license grants remain separate reviewed product decisions.

The company product must also work for another founder: own data/keys/accounts, minimal required services, clear first-use recipe, useful artifact, repairable failure, revocable connectors, pinned dependencies, edits preserved during updates, complete export and demonstrated restore. Free portability and paid convenience can coexist. Do not remove export/security to manufacture lock-in. Measure cold install, first useful result, upgrade repair, monthly cash and support burden against the same incumbent task.

Keep the company's original code, permissive dependencies, copyleft services, source-available tools, paid data and trademarks distinct. Proposed original-core license: MIT or Apache-2.0 only for code with established rights. Commercial modules need clear boundaries and compatible dependency terms. Connecting to upstream through a permitted API does not grant redistribution or data resale rights. Foundry issue 4 retains its current product gates; this larger roadmap does not declare those gates passed or silently authorize another launch.

## Stages and next action

| Business evidence | Investment | Advance when |
| --- | --- | --- |
| Pre-revenue | Existing creator/delivery flow, simple CRM, current asset tools; small cost/recovery instrumentation | One useful offer/artifact and real demand/activation evidence |
| First customers | Fix onboarding/support failures; package install/export/update for one selected module | Outside users achieve the promised result with acceptable repair/support |
| Repeatable demand | Adopt or extend CMS/CRM/distribution only for measured recurring pain | Same-task improvement covers build and maintenance cost |
| Several maintained modules | Shared compatibility tests, module releases, upgrade/restore and partner terms | Repeated independent customer installation and sustainable maintenance |
| Scale | Improve proven workloads; selective dedicated services/forks or paid SaaS | Positive unit economics, reliability and replacement/exit evidence |

Review windows are weeks and months; release dates depend on evidence. A calendar anniversary is not a reason to build a full CRM or DAM.

Next bounded action: the existing creator/delivery owner selects one real artifact and acceptance gap under issue 5; Foundry issue 4 receives the customer-install/export dependency. Refresh both owners and source first. Keep the broader capability plan open. Add only the required module issue, with a measured build/adopt comparison and exact-revision review. DAM is optional throughout.

## Read-only alignment tool

`scripts/company_alignment.py` validates the projection, reads current selected issue metadata and source heads with authenticated `gh`, and writes a private observation. It does not update issues, boards, Registry, files in product repos or runtime queues. It does not inspect deployments, all comments, all repository code, worker liveness, invoices or actual acceptance artifacts.

```powershell
python scripts/company_alignment.py --catalog docs/company-swarm/capability-map.json --live --private-report <existing-private-dossier>/alignment-YYYY-MM-DD.json
```

For a reproducible check, pass `--snapshot <private-snapshot.json>` instead of `--live`. The snapshot has `observed_at`, `issues` keyed by issue URL, and `source_heads` keyed by full repository name. An issue observation has `state` and `updated_at`; a source observation has `sha`. Retain unavailable reads as unknown. Snapshots older than seven days require refresh; future timestamps also require investigation. The tool refuses a report destination inside a Git checkout and prints counts only.

Findings include unresolved placement, untracked capability, changed source, absent evidence/read, and an issue closure awaiting human acceptance reconciliation. Changed sources require inspecting the relevant diff; they do not automatically invalidate all previous evidence. An unchanged SHA proves only source identity. Report findings feed the owning issue's review, not automatic status changes. Internal records and release automation remain separately pending.
