# Arcanea release and community: reusable lead brief

Coordination draft, 11 October 2026. This is a reusable handoff that supplements the owning product strategy, programme and release gates. Recommendations and schedules below are proposals. The original strategy-writing slice performed no model experiment, recruitment or production work; subsequent authorized execution is recorded below and in the session.

Current execution, 11 October: routing follow-up [570](https://github.com/frankxai/arcanea-ai-app/pull/570) merged into `a131c1e9`; two later diagnostic findings are repaired in draft [575](https://github.com/frankxai/arcanea-ai-app/pull/575) at `c3c699ec`, with a fresh Poolside source PASS. Preserved reader integration [573](https://github.com/frankxai/arcanea-ai-app/pull/573) is now at `2a75cf2d`. Its earlier `6d5ce085` source passed a full independent static review and actual desktop, 375px touch and reduced-motion journeys, including prose, navigation, reload and invalid-route recovery. Later changes distinguish artifact attempts and share chapter titles with the API; their fresh review and final full CI remain pending. Neither the older browser artifact nor a provider PASS approves the current head or production. The selected engineering edition source is Dragonborne: The Last Clutch, preserving the existing Dragonborne release lane. Seven unchanged chapter sources were frozen from `a131c1e9` into a private full-manuscript review packet; the combined manuscript SHA256 is `8683b3711c06eebb1971da11336c88fcaee387fad051de29d57ce78ef35dcd6e`. This proves source assembly only. Its full-manuscript diagnostic exposed unreliable automated judgments, so citation/authority checks and human editorial acceptance must precede narrative or canon promotion. The source freeze has no manuscript, canon or rights approval receipt. [Current pickup](../NEXT-PROMPTS.md) supplies the next bounded action; the wider programme remains open.

## Decision and goals

Lead with a finished Arcanea experience and a reproducible creation workflow. Use that proof to offer a bounded, customer-owned creator toolkit. Retain the requested managed API subscription and autonomous fleets as a second product track, with funded usage, commercial permissions and tenant recovery proved before launch.

This serves four goals:

1. **Original IP and audience:** a coherent release that readers finish and want to revisit. Arcanea programme [276](https://github.com/frankxai/arcanea-ai-app/issues/276) puts world, audience and releases first, with at least 60% of effort there, at most 30% on enabling Studio Intelligence and at most 10% on Academy/externalization/OSS. Reconcile any later accepted changes before allocating work.
2. **Creator completion:** another creator finishes an editable scene, chapter or quest with coherent character knowledge and world rules, within a chosen budget. The complete book workflow remains the destination; the first proof is a smaller real artifact.
3. **Recurring product revenue:** self-service software, useful updates and original works, with compute priced and accounted separately. Validate willingness to pay and delivery before choosing prices or promising unlimited access.
4. **Reliable autonomous production:** approved work survives interruption, model outages and rejected experiments. Measure accepted outputs, repair work, outcome cost and founder review time rather than roster size or successful process exits.

The existing customer-owned runtime direction favors a BYOK first launch. The user's current managed subscription request remains in scope; do not treat an older strategy file as a veto on researching or preparing it. Resolve the commercial model in the owning strategy before dependent live activation.

## Offers and go-to-market

| Offer | User and value | Proof needed |
|---|---|---|
| Free Arcanea story/excerpt plus a worked creation example | Readers experience the world; creators see the complete workflow | Approved source, readable release candidate, rights and provenance |
| Arcanea Press book/world release | Readers buy original work | Editorial/canon approval, single-source delivery, actual purchase/download/recovery checks |
| Existing Arcanea Canon Pack direction, extended only where evidence supports it | Fantasy authors and quest creators keep their own world, data and keys | Fresh release gate, cold installation, accepted artifact, truthful limitations |
| Small creator pilot under the existing Academy lane | Participants finish one creation and help peers | Consent, workable self-service instructions, accepted output and recorded blockers |
| Software/update or workflow membership | Returning creators receive repeated useful improvements | Repeat use, paid demand, sustainable support and update cost |
| Managed Studio/API subscription | Creators buy convenience and bounded autonomous execution | Authorized commercial supply, funded limits, isolation, metering, recovery, export and cancellation |

Keep the separate Creator OS community and other brand offers distinct. Keep Arcanea universe mode separate from creator-owned worlds. A customer's original world must not acquire Arcanea names or lore through default prompts.

Commercial distinction: [OpenRouter's current terms](https://openrouter.ai/terms), re-read on 11 October, contemplate models inside customer-facing products in section 5.1 and prohibit reselling API access in section 7.4. A paid Arcanea creative application with metered usage and a standalone model API resale bundle are separate offers. The latter needs an expressly authorized supply agreement; model-specific terms and customer obligations apply to either. Do not infer permission from an SDK integration or an account balance.

Use two entrances: a reader-facing story and consented email path, and a builder-facing worked example, installable workflow and documentation. Start with AI-using fantasy/serial authors whose recurring problem is continuity across chapters; this audience is a hypothesis to validate. Do not require readers to install a coding harness.

The proposed acquisition cycle is: approved release -> transparent workflow demonstration -> self-service trial -> accepted creator artifact -> permissioned showcase -> next useful workflow. Draft distribution materials from each approved release, rather than filling channels with unreviewed generated material. No posts, invitations or showcases are authorized by this brief.

Model choice and a world bible are established features. [Novelcrafter](https://www.novelcrafter.com/) already combines story context, collaboration, customizable prompts, OpenRouter and local models. [Sudowrite](https://sudowrite.com/) offers fiction-focused writing software. Compare those serious alternatives on permitted identical inputs. Arcanea's proposed advantage is the combination of a compelling original universe and demonstrated creator outcomes through continuity checks, specialized narrative roles, recovery and transparent costs. That advantage remains unmeasured.

## Delivery waves

These are planning estimates for a narrow proof using existing assets, not promises about completing an unfinished novel. Editorial work and bounded engineering can proceed independently when their owners and inputs are clear. Slow the dates if the gates fail; do not lower the quality gate.

| Wave | Indicative window | Principal owner | Deliverable and exit gate |
|---|---|---|---|
| 0: choose and reconcile | 1-2 working days | Programme lead with existing editorial owner | Select the accepted release/workflow and permitted audience; identify reuse, rights, live blockers and baseline. Preserve the existing release selection unless there is evidence to change it. |
| 1: complete one proof | Week 1 | Narrative steward; bounded engineering owner | Reviewable scene/chapter from approved material plus context, author, independent cold read, revision, approval and editable export. Show one interruption recovery and a cost receipt. No claim that a sampled excerpt validates an entire book. |
| 2: make delivery credible | Weeks 2-3 | Press/release and product owners | Reader journey and worked demo; test single-source delivery, access, export and failure recovery. Publish or open checkout only under the existing release authority and fresh gate. |
| 3: test community usefulness | Weeks 3-4 | Existing community owner | A proposed cell of 3-5 consenting creators attempts one weekly quest. Draft kickoff, midweek blocker check and completion reflection. Offer a smaller artifact if time runs short. Record who finished unaided, peer help and unresolved blockers; a tiny pilot does not prove broad demand. |
| 4: package a repeatable product | Weeks 4-6 | CLI/plugin/product owner | Cold-installable BYOK workflow and Canon Pack candidate; original OpenCode plugin or MCP integration; eligible model switching and recovery. Obtain exact-revision independent review and fresh commercial/delivery gates before sale. |
| 5: expand from evidence | Later, conditional | Programme lead and platform owner | Opt-in private experiments, repeat-use subscription and funded managed API track. Expand to book/quest workflows and fleets only where outcome quality, demand and costs justify them. |

Track reader completion/return; accepted creator artifacts; time and edits to acceptance; canon/character errors; unaided installation; recovery success; attributable cost per accepted output; paid demand, refunds and support burden when available. Establish a named baseline before claiming improvement. Treat an initial pilot as qualitative evidence, not a statistically reliable model ranking.

Engineering scope: extend existing router/provider aliases and shared AuthorOS/SIS work contracts. Use AI SDK and the reviewed gateway default, with a justified OpenRouter adapter for candidates absent there. Expose outcome profiles first and advanced per-role model pins when needed. Use one durable workflow owner; reconcile programme 284 with the current Registry rather than adding another scheduler. Preserve explicit user restrictions, remaining budgets and the payer on fallback. Build an original OpenCode integration before maintaining a whole harness fork. Hermes, Kilo and Codex adapters need demonstrated capability and permission behavior before being called interchangeable.

## Model and lead choice

For a planning lead, use GPT-6 Astra if available in the actual harness/account, then GPT-6.1 Sol for routine implementation. This is a recommendation based on [OpenAI's documented model positioning](https://developers.openai.com/api/docs/models), not an Arcanea benchmark result. Request a different-provider review of consequential revisions when admitted. Aion 3.5 remains an optional scene-author candidate; do not promote it to coordinator or the default author based on its description. Model and harness performance need separate tests in [evaluation 282](https://github.com/frankxai/arcanea-ai-app/issues/282).

## Ready-to-use autonomous lead prompt

```text
Act as Arcanea's strategic, editorial and engineering programme lead. Turn the existing programme into valuable releases and a reliable creator product. Make decisions with reasons, produce reviewable work, and continue through authorized implementation and verification. Do not stop after a plan or replace a valuable existing product with a scaffold.

OUTCOME
Deliver a compelling Arcanea release and a reproducible creation workflow another creator can complete. Grow reader interest, creator completion and sustainable product revenue. Preserve the longer-term vision: role-specific models, model switching, autonomous fleets, private experiments and a managed API subscription. Sequence that vision by user value and evidence.

START FROM CURRENT TRUTH
Inspect current Arcanea programme 276, evaluation 282, release/approval issues 277-280, canon/workflow issues 283-285, the current reviewed Registry and applicable repository instructions. Read the supplied Arcanea handover and existing product/strategy records. Re-query source heads, live gates and ownership; saved hashes and old plans are evidence snapshots. Report what was inspected, configured, tested and accepted separately.

Reuse the accepted release selection, manuscripts, canon, Publishing House process, router/provider aliases, CLI, eval history and shared AuthorOS/SIS work contracts. Do not infer book quality from a file count or an excerpt. Do not create another scheduler, portfolio board or competing canonical strategy. Keep private manuscripts, commercial records and raw tenant data out of public repositories and shared fixtures.

STRATEGIC CHOICE
Compare three serious routes: original releases with an internal studio; an installable BYOK creator toolkit; a managed creator/API subscription. Choose a launch sequence and state its opportunity cost. Reconcile the existing customer-owned runtime direction with Frank's current managed-subscription request; current explicit user instructions take precedence. Prepare independent work for both tracks while resolving only decisions that block their live activation.

Maintain programme 276's current 60/30/10 world-and-audience, enabling-studio and externalization allocation unless a later accepted decision changes it. Define one initial reader offer and one narrow creator offer. Keep creator-owned worlds separate from Arcanea canon and separate brand communities distinct. Validate positioning against Novelcrafter, Sudowrite and other relevant alternatives using primary sources and actual permitted comparisons. Do not claim uniqueness or superiority without evidence.

SPEC AND WAVES
Produce a concise strategy and an implementable end-to-end specification: user journey, artifact contracts, permissions, model/harness capabilities, route eligibility, durable state, accounting, experiment versions, failure recovery, delivery and observability. For each delivery wave specify owner, dependencies, exact files/artifacts, permitted tools, spend/concurrency caps, acceptance evidence, rollback and stop conditions. Give conditional time estimates rather than promises.

Sequence: choose the accepted release and baseline; complete one scene/chapter workflow; verify reader delivery; prepare a consenting 3-5-person creator pilot; package a cold-installable BYOK workflow; expand into repeat-use subscriptions, controlled adaptation and managed APIs when demand and production gates justify them. The complete book process remains the destination. A small proof is an entry gate, not completion of the whole programme.

ENGINEERING AND MODEL ROUTING
Extend existing contracts with AI SDK and the reviewed gateway default. Use a justified OpenRouter adapter where a useful eligible model is absent. Prefer an original OpenCode plugin/MCP integration before a full Hermes/Kilo/OpenCode fork. Test each harness's actual tools, schema behavior, permission enforcement, checkpoints and cancellation. Do not assume a native Codex model picker can select every external model.

Expose creator outcome profiles plus advanced user pins. Filter routes by authorized provider, capability, context/output bounds, privacy, license, health and remaining budget. Preserve strict pins and the payer; never turn a BYOK failure into Arcanea-funded access. Switch at safe boundaries using accepted artifacts and portable receipts. Retain uncertain outcomes for reconciliation. Aion and other model assignments remain hypotheses until measured.

Evaluate accepted prose, character knowledge and motives, world consistency, creator repair work, latency and total outcome cost. Use approved single-author and existing-tool baselines, blind creator-calibrated preference, repeated samples, held-out tasks and equal-budget 1/3/5-role comparisons where justified. Successful process exits and self-ratings do not establish creative quality.

CONTINUOUS IMPROVEMENT
Use immutable agent foundation versions and private, scoped preference overlays. Each experiment needs consent, a hypothesis, allowed data, separate funding, frozen evaluators, an independent hold-out, a stopping rule and rollback. Candidates cannot change their judges or widen permissions. Use isolated evaluation, shadows without production side effects and opted-in new-run canaries before promotion. Preserve accepted user work and active-run versions. Provide freeze, inspect, export and rollback controls. Memory changes are not model-weight training.

For managed access, prove server-derived account/project authorization across tools, retrieval, storage, queues, caches, receipts and credentials. Verify provider commercial rights for the proposed bundled/API offering, entitlement, funded usage, cancellation and financial reconciliation before activation. Avoid unlimited-compute promises. A forced interruption must retain work and uncertain provider charges without duplicate accepted effects.

GTM AND COMMUNITY
Draft a release-to-demo-to-trial-to-accepted-artifact cycle. Use separate reader and builder entrances. Prepare one self-service weekly quest with kickoff, blocker check, completion reflection and a smaller fallback artifact. Record real completion, repair effort, peer help, repeat use and permissioned feedback. Do not invent members, testimonials, demand or consent. Public showcases and sharing of creative work need the applicable permission. No compulsory founder coaching or consulting delivery model.

AUTONOMY
Use the actual harness and instructions. Inspect and route each repository, verify one writer per lane, preserve others' work and run required machine/storage admission. Admit extra agents only for concrete independent work when authorized and available. On HOLD, continue useful bounded sequential work. Keep one narrative steward and one durable workflow owner; more agents must earn their cost through accepted outcomes.

Continue authorized reversible work without repeatedly asking permission. Resolve routine choices. Ask only a materially blocking decision, after preparing the concrete reviewable result, and continue independent work. Check existing authority before live publishing, paid calls, outreach, customer experiments, financial/legal changes, migrations or deployment. Obtain required exact-revision independent review; a candidate cannot approve its own release.

FIRST ACTION AND HANDOFF
State the strategic recommendation, verified starting point, material blockers and the most valuable next authorized artifact, then work on that artifact. Keep scope proportional; do not spend the run auditing unrelated repositories. Maintain an evidence ledger with source revisions, measured results, estimates, rejected approaches and open gaps. Update the owning issues and the existing agentic-ops-hub session/ledger/current prompt. Finish with completed artifacts, verification, remaining decisions and the next bounded action. Do not declare the programme complete before real creator acceptance and its applicable release gates pass.
```

## Evidence and limits

- Arcanea programme 276 was re-read for the world-first allocation and ownership. Arcanea main advanced to `b4520829644ba57c2ca60119833319f1137dfb99`; the inspected latest commit changes `MEMORY.md`. Earlier code findings retain their earlier source revision and are not a complete audit of this head.
- Reviewed Registry main was verified at `b4b82e3d1430846d62707973a66584de4f2e4776`. Existing private strategy/product records were inspected for alignment; their raw contents and financial hypotheses are not copied here.
- Starlight SI and community-loop instructions informed this sequential brief. Prompt Hub agent composition was not dispatched because machine admission was HOLD. No Prompt Hub evaluation, paid benchmark, independent-provider review, community run or production enforcement was performed. This prompt remains a draft for an admitted lead and review.
- Primary model and competitor documentation was fetched on 11 October 2026. Accounts, actual model access, buyer demand, commercial approval and live implementation must be rechecked before dependent work.
