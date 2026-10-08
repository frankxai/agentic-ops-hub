# GenCreator Social: tooling, ownership and first installation

Date: 8 October 2026. Status: researched setup proposal and verified isolated skill intake. No new subscription, OAuth grant, scheduler change or publication. This public projection omits billing records, account identifiers, credentials and private project names.

## Decision

Use the existing GenCreator workflow with Canva for editable design, Descript or the existing local video module for editing, and Postiz as the designated publisher. Content OS coordinates the brand queue. Buy another tool only for a demonstrated gap. Package the reusable methods as **GenCreator Social inside frankxai/gencreator-skills**, with existing modules retained. Do not create another skills repository or coordinator.

The creator outcome is one permitted source turned into distinct, editable work for selected channels, with durable revisions, review, an approved delivery and measurable results. Installation alone does not establish that outcome. The serious alternative is the existing host model plus Canva/Descript and a managed scheduler, without additional orchestration. Compare both on the same source before claiming that our bundle is better.

## What was verified

- Canva answered a read-only brand-kit request in this session and returned six kits. Existing private mappings retain exact IDs. A kit's existence does not prove approved fonts, master templates or folder associations.
- Descript answered a read-only project-list request. Editing, export quota, paid tier and renewal were not tested or inferred from that response.
- Current `frankxai/gencreator-skills` main was inspected at `982aa4a400fdc7eace03b65d118ada6c8a2c0cfe`. It already contains `video-social-studio`, with seven portable skills, a local engine, commands, trigger fixtures and tests. This corrects the older local checkout inventory in the first audit.
- The local `agentic-creator-skills` checkout points at `frankxai/gencreator-skills`, but is ahead one and behind six relative to its remote-tracking main. It was not reset, pulled, switched or edited. The current remote marketplace name is `gencreator-skills`; older local naming remains stale.
- Existing operations [gencreator.ai #147](https://github.com/frankxai/gencreator.ai/issues/147) and tools/usage [#136](https://github.com/frankxai/gencreator.ai/issues/136) already own this product direction. Keep activation [#5](https://github.com/frankxai/gencreator.ai/issues/5) and the [Content OS pilot](https://github.com/frankxai/content-os/issues/5) open.
- Eleven skill directories were installed in an isolated local review destination: seven owned and four upstream. Their 34 files, 232,987 source bytes, match pinned Git blobs. Four license files were retained separately. No upstream executable files were selected. See [intake receipt](2026-10-08-social-skill-intake.json).

Private subscription registers were consulted. Several records are historical or have unresolved current charges, renewal dates and seats. No current total, savings estimate or paid entitlement is established by this document.

## Subscription choices

| Job | Selection | Purchase trigger |
| --- | --- | --- |
| Writing, research synthesis and review | Existing host subscriptions and native GenCreator skills | No additional writing seat for the pilot. Consumer subscriptions do not supply arbitrary API credits. |
| Editable carousels, covers and brand assets | Existing Canva connection and paid-plan record | First verify one approved master and export using current access. Do not buy Enterprise on the assumption that all MCP autofill needs it. |
| Talking-head video, transcript editing and clips | Existing Descript connection | Inspect actual export rights/limits, then run one approved editing task. Upgrade only if the useful pilot exceeds the existing entitlement. |
| Local video fallback | Existing `video-social-studio` | No new editing SaaS required to evaluate it. ffmpeg/transcription/model downloads are separate dependencies and admission decisions. |
| Publishing | Existing self-hosted Postiz first | Verify the deployed version, healthy exact destination connections, media handling and recovery. Switch the publishing owner to Postiz Cloud only if maintenance or app approvals prevent useful delivery. |
| Analytics | Native platform exports and available publisher data first | Evaluate Metricool for consolidated reporting when manual collection becomes the bottleneck. Advanced is needed for its API, not merely its MCP. |
| Short-form competitive research | Sandcastles if already entitled and useful | Verify account/plan/access before connecting. Start with a small research task and compare useful findings against permitted manual research. No price was verified. |
| Comment-to-DM conversion | Manychat later | A real offer, opted-in audience action and measured manual reply burden come first. Price and plan eligibility depend on region and account cohort. |
| Music and generated visuals | Existing permitted native tools and licensed catalog | Verify rights and real quota per tool. Keep the current Higgsfield ban. Do not buy another generation subscription for an untested workflow. |
| Assets and source storage | Existing private storage, brand mirrors and provenance | No replacement DAM purchase or additional public upload during this setup. |

Public quotes checked 8 October, separate from Frank's private charges:

- Postiz Cloud monthly list prices: Standard $29/5 channels; Team $39/10; Pro $49/30; Ultimate $99/100. Current docs say unlimited posts and MCP/CLI/API/webhooks on every plan. A channel is a connected account. These are conditional fallback options; existing self-hosting still has infrastructure and operational costs. Hosted agent features can arrive before self-hosted parity. [Pricing](https://postiz.com/pricing), [self-hosted versus cloud](https://postiz.com/).
- Descript advertises Hobbyist $24 per person/month monthly or $16/month billed annually; Creator $35 monthly or $24/month billed annually. Its current page also links API/MCP. This is a public quote, not evidence of the connected account's tier or connector credit allowance. [Pricing](https://www.descript.com/pricing).
- Metricool MCP is documented on every plan, including Free. Free has one brand, 30 days of analytics and no LinkedIn or X connection. API access requires Advanced or Custom; X and some advanced analytics involve separate add-ons. For the FrankX LinkedIn/X pilot, Free therefore does not solve the required coverage. [Plan and access matrix](https://help.metricool.com/plans-add-ons-and-api-access-explained-xux1u).
- Manychat's current page shows Free at 25 monthly active contacts, two eligible channels and up to four live triggers. Essential displays $14/month billed annually at $168, and Pro $29/month billed annually at $348, with different included contacts/channels and overages. These are annual commitments, not monthly checkout quotes. Existing accounts and regions may have a different model. [Pricing](https://manychat.com/pricing), [eligibility](https://help.manychat.com/hc/en-us/articles/25800347122716-Manychat-subscription-How-to-choose-the-right-one-for-you).

Canva changed recently: current official MCP docs list brand templates and autofill for Pro, Business and Enterprise. The older blanket Enterprise prerequisite must not be carried into an MCP recommendation. A custom REST integration's entitlement, scopes and approval remain a separate check. No autofill write was run here. [MCP dataset tool](https://www.canva.dev/docs/apps/mcp/tools/get-design-dataset/), [brand-template discovery](https://www.canva.dev/docs/apps/mcp/tools/search-brand-templates/).

## Brand sequence and Frank's job

These are proposed priorities, not account activations. Preserve existing channel, product and brand holds.

| Brand | First useful output and channels | Tools and boundary |
| --- | --- | --- |
| Frank personal / FrankX | One weekly source edition: useful LinkedIn post or carousel, distinct X treatment, newsletter material. Add a clip when real footage exists. | GenCreator, Canva, Descript if needed, Postiz after connection verification. Keep personal experience separate from product promises. FrankX's visual foundation reset still requires resolution before promoting new branded masters. |
| Arcanea | Canon-backed art/story edition for Instagram; test a Short or Pinterest treatment when approved material exists. | Canon/source review, existing media tools, Canva and Postiz. Preserve the TikTok/series hold until its acceptance passes. |
| GenCreator | Demonstrate one actual creator transformation or workflow with source/output evidence; prepare product education for LinkedIn/X/YouTube. | Reuse native Producer/Operations/Launch and existing product packages. Public product/release holds remain; a content draft does not enable checkout or autonomous publication. |
| Starlight | Technical explanation or verified case from an actual engineering outcome, initially LinkedIn/X. | Reuse the existing draft-only cell. Share evidence selectively, without exporting private operations. |
| Starline, Energetic Income, Akamoto and other held cells | Resolve identity, source authority, audience and an owner before adding cadence or paid tooling. | A Canva kit is insufficient readiness evidence. Starline is not Starlight; Energetic Income is not automatically Agentic Income. Akamoto must reconcile fiction canon and the older roster. |

For Frank, propose a small sustainable routine: capture one source note or recording each week, review the selected drafts and actual assets in one batch, approve exact channel destinations, then review results on Friday. An initial planning allowance of roughly 60 minutes per week is a hypothesis to measure, not a demonstrated saving. Reduce brand breadth if editing or approval exceeds that allowance.

## Connectors to use and why

| Connector | Purpose | Evidence / next bounded check |
| --- | --- | --- |
| Native file/source access and existing Drive/Notion routes | Retrieve a selected source and preserve its revision; provide a human review surface when useful | Confirm access for the actual item. Host access is not a GenCreator backend account connection. |
| Canva app/MCP | Read kits/templates; create editable designs and export reviewed assets | Kit read passed. Inspect the selected template's fields, then test a reviewed duplicate/export. No sharing changes. |
| Descript app/MCP | Read projects; support transcript/media editing and exports | Project read passed. Editing/export and spend limits remain unverified. |
| Postiz API or deployment-compatible MCP | Resolve channels, prepare approved delivery, reconcile provider IDs and URLs | Designated/deployed is historical evidence. No live account or publication check was performed here. The hosted MCP endpoint is not proof of compatibility with the Railway deployment. |
| Metricool MCP, optional | Analyst reads consolidated metrics | Documented, absent from this session's exposed connector inventory. Scope analytics separately and keep Postiz as publisher. |
| Sandcastles MCP, optional | Scout examines permitted examples/outliers and records source/date/sample | Official endpoint documented; connection and entitlement not verified here. Do not adopt its blanket Always allow recommendation. |
| Existing n8n plane | Bounded durable queue/receipts when the pilot needs automation | Preserve coordinator ownership. Known repurposer/atomizer defects from the first audit need repair and verification before execution. |
| Manychat, later | Permissioned comment-to-DM and reply workflow | No live funnel or current account connection verified. Account grants and message sends require separate authority. |

Postiz's hosted OAuth MCP is documented at `https://mcp.postiz.com/mcp-oauth-dynamic`; its API/CLI uses API-key authentication. Keep raw publishing credentials behind the existing delivery controls when exact revision approval is required. Installing a publisher skill does not add those controls. [Official connector distinction](https://postiz.com/mcp).

Sandcastles documents `https://mcp.sandcastles.ai/` and interactive account authorization. Verify available read actions and retention before sending sources. [Official setup](https://sandcastles.ai/mcp).

Use existing shared/remote transports on demand. No global local MCP registration, new background workers or service fanout is needed for this pilot. Current Canva/Descript host access also does not establish Claude Desktop or ChatGPT cloud configuration; those clients have separate settings.

## GitHub ownership and distribution

| Repository | Responsibility |
| --- | --- |
| `frankxai/gencreator-skills` | Public reusable skill/plugin catalog and the proposed GenCreator Social capability bundle. Preserve existing `content-engine`, `brand-architect`, `video-social-studio`, examples and license boundaries. |
| `frankxai/gencreator.ai` | Source-owned native product workflows, CreatorPack, operations engine, review/recovery and authenticated adapter implementation. Generate versioned distribution artifacts from the owning source, with a source revision/hash; do not maintain independent hand-edited copies. |
| `frankxai/creator-skills` | Existing focused media/creator skills. Reference or export selected capabilities into the distribution bundle with provenance; do not force a repository merger. |
| `frankxai/agentic-creator-os` | Existing ACOS host commands and routing. Route into the chosen skills and repair stale social guidance; avoid another competing copy. |
| `frankxai/content-os` | Brand queue, stage ownership and coordination. Keep private brand state separate from the portable catalog. |
| `frankxai/starlight-social` | Existing delivery/approval adapter boundary, where selected. Do not bypass it by handing a raw publisher token to a drafting role. |
| Brand repositories and private operations | Actual brand identity, source content, account maps, private results and approvals. No private records in the public skills catalog. |

GenCreator Social should be a curated bundle of existing skills plus the smallest missing strategy/research capability. First extend the current content calendar to handle source editions and brand capacity. Extend the current post kit to produce genuinely distinct channel treatments. Reuse the existing review and performance contracts. Add community/reply drafting only when there is a real inbox pilot. A new `gencreator-social` plugin name or bundle manifest is a proposal, not a published installation target today.

The installed native plugin exposes `gencreator-produce`, `gencreator-operations` and `gencreator-launch`. Product portable skills such as `gencreator-campaign`, `gencreator-review` and `gencreator-performance` are a different package inventory. Preserve those boundaries when designing distribution; the seven video/social skills are a third, existing module, not seven replacements for the native workflows.

Source review found improvements needed in our existing module before promotion. `social-post-kit` says captions do the alt-text job for TikTok/Shorts; captions communicate speech/audio, so visual descriptions need separate treatment. `content-calendar` treats reusing one file with changed captions as the default; evaluate when a channel needs a different opening, duration, cover or music rights. Its automatic lesson append should become a reviewable proposal, preserving the existing GenCreator rule against silently changing approved voice/strategy. Verify platform limits and accessibility in current primary documentation rather than inheriting the module's September reference as universal authority. These are source findings and proposed repairs, not implemented fixes or behavior-test results.

Give each public skill a portable `SKILL.md`, narrow trigger description, on-demand references, concrete input/output examples, original evaluation cases and clear connector fallbacks. Brand records are caller inputs. Ship no user paths, keys, analytics, invoices or internal approvals. Keep one source owner for each skill and a deterministic export when native packaging needs a copy.

## Absorb upstream work

| Source | Keep and adapt | Correct before promotion |
| --- | --- | --- |
| [Corey marketing skills](https://github.com/coreyhaines31/marketingskills) | Source/context intake, anti-AI prose, carousel/short-form/listening references | Replace generic high-frequency posting prescriptions with capacity and owned-data tests. Do not present repository algorithm interpretation as live ranking weights. |
| [Social Media Skills](https://github.com/social-media-skills/skills) | Channel selection, strategy structure and operating-model references | Remove vendor scheduling dependency, arbitrary universal cadence and unsupported experiment thresholds. Preserve Postiz ownership. |
| [BlackTwist](https://github.com/blacktwist/social-media-skills) | Pattern taxonomy and supplied-data analysis | Adapt to authorized exports. Replace claims about exactly why a post won with testable hypotheses. Retain missing/zero denominators and objective-specific metrics; engagement rate is not always the business objective. |
| [Aaron marketing skills](https://github.com/aaron-he-zhu/aaron-marketing-skills) | Dated platform norm cards and explore/craft/host/observe separation | Evaluate selected files next; do not import its full registry/runtime. Localize channels and verify current official sources. This source was researched but not installed in this intake. |
| [Postiz agent](https://github.com/gitroomhq/postiz-agent) | Official provider-specific usage reference | Keep as an adapter dependency. Its AGPL license needs separate review before redistributing code/text inside another licensed bundle. It was not installed here. |

Prefer selective, pinned reuse. MIT and Apache reuse must preserve required attribution/license notices, including applicable Apache notices and change notices. A rewrite closely based on source still needs provenance; use original official platform documentation and our measured outcomes for a foundation-based implementation. Unlicensed sources remain reference-only until permission exists. Do not describe an imported collection as newly invented work.

Keep upstream snapshots immutable for comparison. Record source repo, commit, file hashes, license, modifications and review date. Adapt in our source-owned module, then compare current GenCreator, the adapted candidate, and a plain host baseline using the same permitted source. Score usable output, unsupported claims, creator editing, continuity/export and recovery. Add invented-metric, cross-brand leakage, stale-rule, wrong-account, missing-source, duplicate-send and ambiguous-provider-response cases where relevant. Structural validation is not an editorial benchmark.

## Channel and algorithm coverage

Use separate dated references by platform and surface. Do not install one generic algorithm hack skill.

- LinkedIn: professional expertise and actual examples; distinguish personal profile from company page and document from text/video treatments.
- X, Threads and Bluesky: native conversations and distinct concise treatments; feed/reply/search behavior differs, and Bluesky custom feeds need separate handling.
- Instagram: treat Feed, Stories, Reels and discovery separately; maintain a source-derived carousel or original visual story and current technical limits.
- TikTok: a coherent opening, useful story/search intent and retention analysis; stage as a video pilot only when that brand is admitted.
- YouTube: distinguish long-form packaging and Shorts; use actual Studio metrics with definitions/window, never assume raw views mean the same across formats or dates.
- Pinterest: searchable, useful evergreen assets and link outcomes; verify the destination and rights.
- Facebook: distinguish Page, Group and Reels, respect group rules, and use original content.
- Reddit: community-specific contribution and disclosure; manually review participation rules before any proposed interaction.
- Newsletter/website: owned conversion and ongoing relationship, maintained through their existing native systems.

Each card needs surface, source URL, verification date, account/locale caveats, technical versus editorial distinction and a review-due date. Separate official facts from creator hypotheses. Observe comparable formats/windows within one channel and change one variable at a time. Small observational samples cannot establish causality or reveal the algorithm. See the [first audit's primary sources and limits](2026-10-08-social-media-skills-audit.md).

## Download, install and use

Completed with the installed Codex `skill-installer` helper, using explicit immutable revisions and a custom destination outside automatic skill discovery. No npm package lifecycle, media engine, model download, upstream script or publishing command was executed. Ordinary text/source installation was bounded; no bulk clone, agent or build was launched.

Local intake root:

```text
C:/Users/frank/.starlight/skill-audits/social-media-20261008/
  owned/gencreator-skills/       seven existing portable skills
  upstream/corey/social/
  upstream/social-media-skills/social-strategy/
  upstream/blacktwist/content-pattern-analyzer-sms/
  upstream/blacktwist/performance-analyzer-sms/
  intake-receipt.json
  operations-plan-proposal.input.json
  operations-plan-proposal.output.json
```

These are isolated candidate installs, not globally active skills. Use them now by explicitly reading the selected `SKILL.md` and referenced files in an owned, verified brand workspace. Begin with owned `content-calendar`, `social-post-kit` and `platform-specs`; video work also requires `video-engine` and the relevant editing skill/dependencies. Keep upstream skills read-only until their behavioral review and adaptations are accepted.

For later project-scoped discovery, start a native session in the verified repo or owned worktree, read instructions, route explicit `.agents/skills` files and check ownership. The official Skills CLI supports installing selected names from a local directory. Example to run from that admitted project, after reviewing the CLI version and destination:

```powershell
npx skills add "C:/Users/frank/.starlight/skill-audits/social-media-20261008/owned/gencreator-skills" --agent codex --skill video-engine video-edit captions shorts-from-long platform-specs social-post-kit content-calendar
```

This command is documented here, not executed. It selects the reviewed local source snapshot rather than a moving repo head. Pin the CLI version for a reproducible automated installer. Do not use `--all` or `--global` for the pilot. Project installation affects the chosen local harness, not other clients or cloud chats. Promoted skills become available to discovery on the next turn. [Official CLI options](https://github.com/vercel-labs/skills).

To reproduce a narrow upstream intake using the already installed helper:

```powershell
python C:/Users/frank/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo coreyhaines31/marketingskills --ref b9ba399dd88b082b926e261e8ccfb843d20aa066 --path skills/social --dest C:/Users/frank/.starlight/skill-audits/social-media-20261008/upstream/corey --method download
```

That exact destination already exists. The helper refuses overwrite; keep that refusal and choose a new revision-specific review path for an update. The helper fetches a repository archive into a temporary directory and copies only selected skill directories; this is not a sparse network fetch. We retained root licenses separately.

First use prompt:

> Use the existing GenCreator workflow and the staged content-calendar, social-post-kit and platform-specs skills. From this permitted source and the approved FrankX voice, prepare one LinkedIn treatment and a distinct X treatment, plus a weekly plan. Cite the source revision, preserve editable outputs, flag unsupported claims and missing assets, and propose one measurement experiment. Save drafts for review. Do not schedule or publish.

The local `gencreator-operations` engine also compiled a six-brand **proposal**, with one FrankX weekly edition and other brands paused pending their gates. Every social connection is explicitly unknown. Its $0 daily cap is a planning value, not an enforced runtime budget. The compiler ran without inference keys or network; it did not deploy roles or schedule jobs. Private billing stays in the existing business register.

## Acceptance and next gate

Done for this slice: current source/connector research, a concrete stack and brand sequence, a repository ownership decision, eleven pinned isolated installations with per-file verification/licenses, and a local operations proposal. No new subscription is needed to start the proposed pilot; paid capacity and a whole-stack budget remain unverified.

Next: verify one source-bound FrankX LinkedIn plus X edition through existing review/export, then confirm Postiz's actual destination and media readiness. Compare against the plain host baseline and obtain exact-revision independent review before promoting adapted skills or releasing a bundle. Repair the known Content OS automation gaps before enabling a durable queue.

Current machine admission reported 2,302 MB RAM free, 56 task runtimes, BOUNDED interactive/one parallel. Ordinary reading, text installation and a small compiler run were used; no heavy/reviewer workload was admitted. Disk was about 108 GiB free, above both hard floors. Native/project/global activation, connected backend accounts, live publication, media quality, current invoices and independent review remain open. No session-owned server, watcher or worker remains.
