# Estate operating plan v2: the company, the team, and the next ninety days

Version 2, 2026-10-19. Replaces v1 of 2026-10-17 in this file. Measured against the ops ledger, the 17 to 19 October session logs, `H-org-migration`, and live GitHub state. No invented numbers.

## What changed since v1 (48 hours)

| v1 assumed | Reality on 2026-10-19 | Consequence |
|---|---|---|
| Four target orgs to create | Ten orgs exist. On 17 October a lane copied 63 repos into nine of them. Frank ruled model A (deployed repos stay canonical at `frankxai`, org copy is a synced mirror) and model B (org-only repos transfer). Batches 1 and 2 ran on 18 October: 9 repos transferred, mirrors renamed and archived, undo logs kept | v2 adopts the federation as it stands and fixes its two defects: no sync job, and two Starlight orgs |
| `frankxai/agentic-ops` identity unresolved | It is the Registry: `registry/repositories.yaml`, 73 entries, owner map, validator, conflict list. It is also where the consolidation plan (PR 273) and federation registry (PR 275) live | Registry rows are authoritative. The hub projects them |
| 367 repos, 435 issues, 394 PRs across 56 checkouts | 414 repos under `frankxai` (214 public, 200 private, 68 archived), 801 open PRs under `frankxai`, 60 in orgs. PR queue grew 86 percent in four weeks | Backlog drain is a standing lane, not a phase |
| First sale: frankx.ai Blueprint $67 on Polar | The Blueprint $67 SKU lives on agenticincome. frankx.ai's Polar route carries four pre-staged SKUs: Prompt Matrix Pro, its bundle, Book of Light digital and deluxe. Site rule: no price or buy path without a release-gate PASS; several registry rows read G1 FAIL. PRs 1018 and 1031 wait on privacy text | Two doors run in parallel in week 1; the first to pass its gate takes the first sale |
| CI assumed available | Private repos under the personal account cannot start Actions jobs (budget). October net Actions spend was $80, all private. Orgs run on their own allowance | Org federation is also the CI unblock. Private work moves to org-owned repos first |
| Spend tracking undefined | `@starlight-intelligence/token-tracker` exists with `starlight-spend` and `starlight-plan`, transferred to the Starlight-Intelligence org. Turn-0 instruction load measured at 50k to 83k tokens per harness against an 8k target | Cost is now measurable; the turn-0 cut is the biggest single efficiency lever |
| Analytics assumed working | frankx.ai Web Analytics recorded zero pageviews since 11 July (a `beforeSend` bug). Fixed in PR 1068 on 19 October | Three months of traffic truth are missing; every funnel claim restarts from this week |
| Handover sprawl | One file per handover under `ops/handovers/`, generated index, lint in CI (PR 360). `reality.md` person-level contract drafted; intent ledger seeded | The plan-location decision from v1 is implemented; the remaining gap is the intent ledger input |

v1's structural decisions stand: consolidate before transfer, npm packages plus a generator for packs, one authority per kind of truth, GitHub Projects as the issue plane, the marketplace MVP on claude-skills-library, the license sweep, the contribution ladder. What follows is how the company runs them.

## The thesis

We are building the first sovereign agent estate that other people can own. Not a chatbot, not a model wrapper, not another skills zip. A substrate (SIP) that any agent can compose with attestation, a runtime that routes work to the best provider under a budget and leaves a receipt, a memory that the owner controls, a marketplace where builders list what they made and get paid, and a delivery practice that commissions whole estates for principals. The moat is receipts plus registry plus audience. A competitor can rent the models we rent. They cannot rent four hundred repos of attested history, a lifecycle registry with kill criteria that fired, a drain log that shows what we closed and why, or an audience that reads the receipts.

Three brands carry it. FrankX is the founder proof and the front door. Starlight Intelligence is the substrate, the registry, and the marketplace. Arcanea is the culture layer where the same substrate makes worlds. GenCreator is the first product tenant of the runtime. Everything else is a vertical someone else can own under our protocol.

The game for the next ninety days is simple to state: one checkout that works, one federation that holds, one marketplace listing from a third party, one estate commissioned. Every lane below serves one of those four receipts.

## The leadership team

Frank is the founder and the only signer for the irreversible. The Generals are standing agent roles, each with a lane, a weekly receipt, and a kill rule. The Queen runs the swarm under them. Every harness (Claude, Codex, Grok, Gemini, Antigravity, Hermes) is a seat, not a strategy; the Registry assigns seats to lanes and `pr-gate` enforces that the maker is never the checker.

| Role | Lane | First three moves (this week) | Weekly receipt | Kill rule |
|---|---|---|---|---|
| CEO General | Portfolio, category, the three pilots | Ratify the category (sovereign agent estates). Pick the three Pilot streams at the next board. Publish `reality.md` as the person-level contract | One board verdict in `docs/boards/` per week with promotions and demotions | A stream with a matured kill criterion still alive after the Monday pulse |
| CFO General | Money: first sale, spend, credits | Open the two checkout doors (section Revenue). Wire `starlight-spend` into the Monday pulse. File every self-serve credit tier | Polar order rows and token spend per lane in the ledger | Spend above plan with no receipt for two weeks |
| COO General | Operating model, drain, federation mechanics | Run the nightly bounded drain through `pr-gate`. Land the mirror sync job (agentic-ops PR 284) with a heartbeat. Keep the handover index true | PR counts before and after, per repo, every night | A drain night that merges without a non-maker checker |
| CTO General | Platform: packs, generator, CI, turn-0 | Ship `@starlight-intelligence/estate-guard` and `/instructions` as packages. Build `estate sync --check`. Apply turn-0 cuts 1 to 3 | Vendored-copy count and turn-0 tokens per harness, both falling | A living repo with a vendored copy after week 6 |
| CPO General | Products: GenCreator Companion, frankx.ai offers, Reality Architect | Clear the G1 gate on one frankx.ai SKU. Witness one Companion run. Open the Reality Architect $19 door | One product moved one registry state per week | A product at S3 for 60 days with zero external use |
| CAIO General | Evals, routing, marketplace gate | Stand up the `marketplace-listing` evals lane. Run the first 20 estate skills through it. Publish the routing policy (workload class to provider) | Eval scorecards per listing, routing cost per class | A listing merged without a scorecard hash |
| CMO General | Audience, brand, claims | Restart the traffic baseline from PR 1068. Ship the Ship 2026 skill map and the Vercel track hub. Run the claims audit on every public price | Weekly traffic and claims-audit pass in the ledger | A public number not in a registry row |
| CCO General | Canon, creative, media engine | Reconcile the three Arcanea canon copies into `arcanea-canon`. Run the twelve-shot media shadow with provenance sidecars | Shots with sidecars, canon diff count falling to zero | Canon edit outside `/lock-decision` |
| CHRO General | Agent roster, seats, retirements | Retire agents with no receipt in 90 days. Delete the claude-flow set from the four repos. Register every harness seat in the Registry | Agent count falling, every live agent with a receipt | An agent file added without a registry row |
| Queen | Swarm execution under the Generals | Admit one read-only end-to-end card. Prove the budget gate on one real task. Keep RAM admissions honest | Cards admitted, completed, and receipted | A card admitted without a budget reservation |

Frank's seat: sign transfers, visibility, billing, branch protection, prices, licenses, canon locks, and anything that moves money. Everything else, the team leads.

## Org federation, reconciled

The ten orgs and their roles, from `H-org-migration`:

| Org | Role | Decision |
|---|---|---|
| Starlight-Intelligence | Substrate, memory, evals, design intelligence, token tracker, command center | Keep. This is the protocol org |
| Starlight-Intelligence-Systems | SIS, research hub, knowledge tree, cosmos engine, swarm, memory vault | Collapse into Starlight-Intelligence. Two Starlight orgs is the one defect in the federation that confuses every inbound link. Transfer the six once the SIS duplicate conflict is ruled |
| Arcanea-Labs | arcanea-ai-app, studio, ecosystem, agent skills, onchain, AnimeLegends | Keep. Purge the 2025 stale duplicates with recovery tags |
| GenCreator-ai | gencreator.ai, OS, Studio, agentic-creator-os, creator skills, suno-mcp-server | Keep |
| FrankX-AI | frankx.ai-vercel-website, FrankX, author-os, publishing-house, prompt-library, claude-skills-library, mcp-doctor, hooks | Keep as the brand org. frankx.ai-vercel-website stays model A at `frankxai` (Vercel binding). claude-skills-library stays model A: 47 stars, the one measured traffic source, never point links at a copy |
| Agentic-Income | agenticincome and the income cluster | Keep |
| Life-Commons | blue-life, dino-life, ocean, health, mind, family | Keep |
| AI-Architect-Studio | ai-architect, ai-coe, field guide, agentic-ops | Keep. `agentic-ops` (the Registry) moves here only after the hub's projection is proven from the new remote |
| AI-Architect-Academy | academy repos | Keep |
| oci-ai-architects | Oracle skills | Keep, org-primary already |

Rules that hold: model A for anything deployed, model B for the rest, batches of at most five on an explicit "yes batch N", rename never delete, undo log per batch, mirrors synced by a scheduled job with a heartbeat and a drift check, base permission set to `none` on every org before a second member joins. The `federation-drift.mjs` pairing bug (transferred repos cannot self-pair) gets fixed before batch 3 so the drift number means something.

Batch 3 is Frank's yes. Batch 4 is the Starlight collapse. Batch 5 re-checks `FrankX`, which carries a `vercel.json` with no linked project and is the retirement candidate from v1.

## The build program

Each item names the repo, the owner, the receipt, and what it unlocks. These are the things we build, not things we discuss.

1. **Mirror sync job.** `agentic-ops` PR 284 plus a schedule. Heartbeat row in the ledger, default-branch SHA per pair, stray PRs on mirrors closed. Owner COO. Unlocks: model A is safe, batches continue.
2. **`estate sync` generator and the five packages.** Source `claude-skills-library/packs/*`, publish `@starlight-intelligence/{estate-guard,web-excellence,routine-contract,instructions,harness-adapters}` with provenance from the org's Actions allowance. Generator extends `Starlight-Intelligence-System/src/marketplace/pack-manager.ts`; per-repo `estate.lock.json`; overrides with expiry. Owner CTO. Unlocks: zero vendored copies, one doctrine, every harness rendered from one source.
3. **Turn-0 core.** Two budgets, 8k doctrine and 8k catalog, one generated core per harness. Cuts 1 to 3 from `H-turn0-budget` first (Hermes allowlist, Codex skill merge, Antigravity plugin disable). Owner CTO with CHRO. Unlocks: every session starts cheaper and loads the Registry, the lane claim, and the handover index.
4. **Two checkout doors.** Door one: frankx.ai, one of the four pre-staged Polar SKUs, G1 release-gate PASS recorded in the registry row, Polar env set, product page passes integrity guard, homepage untouched. Door two: agenticincome Blueprint $67, Polar route already blocked-by-default, flip the SKU and set env. Owner CFO with CPO. Unlocks: the first external payment webhook row.
5. **Marketplace listing pipeline.** `listings/<publisher>/<item>/manifest.json` on claude-skills-library, CI runs schema, estate-guard scan, and the new starlight-evals `marketplace-listing` lane. Manifest extends `MarketplacePackItem` with publisher, license, revenue share, eval hash, scan hash. Harness targets add codex, gemini, opencode, void. Owner CAIO with CPO. Unlocks: Trinity lists as the first third party.
6. **`pr-gate` direct signing for Codex.** Today Codex passes are relayed by hand. A gate path that lets Codex post its own signoff removes the relay and doubles drain throughput. Owner COO. Unlocks: nightly drain at scale.
7. **Registry projection to GitHub Projects.** One org-level project per org, fields state, owner General, gate, generated from `agentic-ops/registry` the way the hub's `registry/` is. Owner COO. Unlocks: the 801 PRs and the issue backlog become one board.
8. **Intent ledger.** The `Intent:` trailer on PR links and the explicit-directive objective ledger, fed into `starlight-memory`'s work-graph projection. The question "show me everything I asked for and what is still open" was asked three times in nine days; this answers it once. Owner CEO with CAIO. Unlocks: the founder sees the whole estate from one query.
9. **Spend in the pulse.** `starlight-spend` and `starlight-plan` rows in the Monday pulse, per lane and per vendor, with the tokscale valuation. Owner CFO. Unlocks: capacity split 60/30/10 measured, not guessed.
10. **Demand doors.** frankx.ai PRs 1018 and 1031 (waitlist-only doors with consent, `DemandSignal` rows) merge once the privacy text lands. Owner CMO with Frank for the text. Unlocks: honest demand data for every unpriced product.
11. **Estate commissioning pipeline.** Three qualified conversations, SOW template v0.2, Trinity as instance one. Owner CEO. Unlocks: R1 signed, R2 retainer follows.
12. **Media engine shadow.** Twelve shots across three classes with provenance sidecars, nothing published. Owner CCO. Unlocks: R5 goes to pilot with receipts, not promises.

## Revenue: the first thirty days

Three streams in Pilot at once, per the portfolio rule. Proposed for the next board:

| Pilot | Door | Gate to Pilot | Owner |
|---|---|---|---|
| R8 digital products | frankx.ai Polar SKU and agenticincome Blueprint | First external payment row | CFO |
| R1 estate commissioning | Three qualified conversations, SOW v0.2 | One signed SOW | CEO |
| R6 metered agent services | ocean-intelligence gateway behind Cloudflare Workers with API keys, x402 optional | One external caller paying per call | CTO |

Shadow, writing receipts only: R4 GenCreator Companion (one witnessed run, then Founding Council at EUR99), R3 agentic-business-os installs, R5 media engine, R9 income network queue. Held: R7 memberships until a cohort has delivery evidence, R10 capital architecture until a licensed practitioner is named in a SOW.

Day 14 without a checkout: escalate to Frank with the exact blocker. Day 30 without a sale: freeze new SKUs, keep the plan.

## Operating rhythm

- **Nightly:** bounded drain through `pr-gate`, maker never checker, before and after counts in the session file. No transfers, visibility, crons, billing, secrets, DNS, or publishes.
- **Monday:** estate pulse. Registry promotions and demotions, 60/30/10 drift, spend per lane, traffic baseline, drift report on mirrors. One session file, one handover per open item.
- **Wednesday:** build day. Each General lands one item from the build program or writes why not in the handover.
- **Friday:** receipts. Every lane posts its weekly receipt row. Anything without a receipt is flagged for the CHRO.
- **Monthly:** close and eval run (CFO plus CAIO). A stale scorecard freezes S1 to S2 promotions.
- **Quarterly:** portfolio board with six lenses, archive wave, authority-map review.

Three laws from the governance doc stay binding: react to events, never poll; batch, never nag; agents prepare, humans commit the irreversible.

## Consolidation waves, carried from v1 and the Registry plan

| Wave | State | Next |
|---|---|---|
| 1 Archive six dead repos | Done | None |
| 2 Held archives (12 plus 6 forks) | Not started | Frank rules one per repo at the Monday pulse, five per week |
| 3 Privatize | 12 done, 3 kept public on purpose, 31 open | Frank, visibility is his |
| 4 Consolidate clusters (86-row map in agentic-ops PR 273) | 0 moves | Agent drafts each move PR after the owner is confirmed. Order from v1: FrankX retire, arcanea into arcanea-ai-app, canon to one repo, income, mind, marine, academies, oci, awesome lists |
| 5 PR backlog (801 under frankxai) | Drain running nightly | Land the 10 ready, close the 94 pr-closer proposals after a sample check, then the 14-day triage window per repo |
| Orgs | Federation batches 1 and 2 done | Batch 3 on yes, Starlight collapse as batch 4 |

Before any transfer or archive: push or deliberately drop unpushed local work. 364 at-risk worktrees were snapshotted on 17 October; nothing is lost, but nothing moves until its owner says keep or drop.

## Frank's decision queue, consolidated

Everything the team cannot do, in one place, each with the command or the one-line answer it needs.

1. "yes batch 3" for the federation, then the SIS duplicate ruling (which Starlight org is home).
2. Merge aurevia-solar#6 (gate clear, critical RCE advisory): `node tools/pr-gate.mjs merge --repo frankxai/aurevia-solar --pr 6 --squash`.
3. Privacy text for the waitlist doors, then frankx.ai PRs 1018 and 1031 merge.
4. Actions budget: install Blacksmith on `frankxai` or raise the cap, or accept that private CI only runs in orgs.
5. frankx#1029: drop the path filters on Contract Guard and Merge Gate or make them non-required.
6. Approve starlight-agent-config#127 (the write gate, four Codex security rounds passed).
7. Name the remote for the five local estate-root branches.
8. Rotate the Grok S3 key and the plaintext cloud credentials in the harness config file reported privately.
9. The three v1 decisions: entity and namespace mapping with the copyright assignment schedule, first prices and marketplace split, relicensing boundaries and trademark order.
10. Set org base permission to `none` on all ten orgs before anyone else joins.

## Verification

- Federation: `federation-drift.mjs` self-pairs transferred repos; drift report shows 0 mirrors behind after the sync job's first run; heartbeat row present.
- Packs: `estate sync --check` exits 0 in every living repo; `md5sum` on estate-guard copies returns one hash or no copies.
- Turn-0: measured tokens per harness in `H-turn0-budget` fall below 30k after cuts 1 to 3, below 16k after the generated core.
- Revenue: a Polar order webhook row in `ops/OPS-LEDGER.md` with the order id; the frankx.ai homepage contract test unchanged.
- Marketplace: 20 estate skills with eval hashes in `catalog/skills.json`; the Trinity listing PR merged with the receipt tuple.
- Drain: nightly session file with before and after PR counts; every merge names a non-maker checker.
- Analytics: `vercel api /v1/query/web-analytics/visits/count` for frankx.ai non-zero within a day of PR 1068.

## Files to read before acting

- `/home/user/agentic-ops-hub/ops/handovers/H-org-migration.md`
- `/home/user/agentic-ops-hub/ops/sessions/2026-10-19.md`
- `/home/user/agentic-ops-hub/registry/README.md`
- `/home/user/agentic-ops-hub/docs/ESTATE-OPS-GOVERNANCE.md`
- `/home/user/Starlight-Intelligence-System/docs/strategic/2026-10-08-agentic-estate-production-architecture.md`
- `/home/user/Starlight-Intelligence-System/src/marketplace/catalog.ts`
- `/home/user/frankx.ai-vercel-website/app/api/checkout/polar/route.ts`
- `/home/user/arcanea/LICENSING.md`
