# Estate consolidation, org migration, and marketplace platform plan

Measured 2026-10-16 across the 56 checkouts under `/home/user` plus GitHub counts. Decisions first. No invented numbers.

## Context

The estate is capability-saturated and decision-starved. The GitHub footprint was 367 repos at the August audit; 56 are checked out here; about 150 more are referenced but not present. There are 7,861 agent, command, and skill files, 372 instruction files totalling 22,219 lines, 10 competing marketplace manifests, 3 competing strategy front doors, and 435 open issues plus 394 open PRs (260 of the PRs sit in five repos). No product takes money today: six repos carry payment routes and every one refuses to sell until a key is set and a product is flipped to for-sale.

The governance to fix this already exists and is split across three authorities that disagree in places:

- Lifecycle registry S0 to S7 with owner Generals and signatures: `agentic-ops-hub/registry/README.md`
- Canonical authority map and branch convergence contract: `Starlight-Intelligence-System/docs/architecture/STARLIGHT_PORTFOLIO_TOPOLOGY.md`
- Production spine, revenue streams R1 to R10, 90-day plan, entity posture: `Starlight-Intelligence-System/docs/strategic/2026-10-08-agentic-estate-production-architecture.md`
- Licensing at the economic boundary: `arcanea/LICENSING.md`
- Instruction layering and PR governance: `agentic-ops-hub/docs/layering.md`, `docs/ESTATE-OPS-GOVERNANCE.md`
- Marketplace code: `Starlight-Intelligence-System/src/marketplace/{catalog,pack-manager}.ts`, `packs/registry.json`; distribution surface `claude-skills-library` (8 packs, 114 skills, 0 evals)

This plan reuses all of it. It adds one sequencing rule, one distribution mechanism, one target repo list, one marketplace MVP, and a phase schedule with receipts.

Decisions already taken by Frank in this session: protocol org plus brand orgs; first checkout is frankx.ai Blueprint $67 on Polar; GitHub Projects is the issue plane; additional existing orgs to be listed by Frank (slot in section 1).

## 0. Spine decisions

1. **Consolidate first, migrate second, archive in place.** Orgs are created now as empty name reservations. A repo transfers only after its cluster is consolidated and its registry row is S2 or higher. S6 and S7 repos stay in `frankxai` and are archived there. Every transfer breaks Vercel git linkage, npm provenance, App installs, and org secrets. Paying that about 24 times for clean living repos is cheap; paying it 367 times, mostly for dead repos, is the one mistake this plan refuses.
2. **npm packages plus one generator** replace vendored copies. Submodules and copies are rejected: 16 of 19 estate-guard copies are already behind canonical and the web-excellence workflow has 6 versions.
3. **Revenue loop in week 1**, independent of everything else. frankx.ai Blueprint $67 through the existing Polar route. Homepage untouched.
4. **GitHub Projects**, one org-level project per org, fields mirroring the registry. Linear rejected: second plane, sync agent, bill.
5. **One public marketplace repo**: `claude-skills-library`, marketplace name `starlight`. The other ten manifests become redirects.
6. **Resolve `frankxai/agentic-ops` first.** 341 references across 11 repos name it the private fleet registry; `agentic-ops-hub/docs/CONTROL_PLANE.md` says it is only the ASPH protocol spec. It is not checked out. Attach it in the first session and settle which it is before any registry row is treated as authoritative.

## 1. Org migration

### Target topology

| Org | Proposed legal owner | Holds | Default visibility |
|---|---|---|---|
| `starlight-intelligence` (create; matches the Vercel team name) | Starlight Holding BV | Substrate L0 to L2 (SIS monorepo, starlight-evals, starlight-memory, starlight-private-memory), ops (agentic-ops private, agentic-ops-hub public), distribution (claude-skills-library), holding-owned products (gencreator.ai, agenticincome, agentic-business-os, mind-intelligence-system, marine-mcp, ocean-intelligence-system, vibeclubs), starlight-agent-lab | public unless the row says private |
| `Arcanea-Labs` (exists; purge stale duplicates; rename to `arcanea` only if the handle is free) | Arcanea BV | arcanea-ai-app monorepo, arcanea-canon (private), arcanea-academy | mixed |
| `oci-ai-architects` (exists) | community, Frank maintains | one merged `oci-ai-architect` | public, Apache-2.0 |
| `frankxai` (personal) | Frank Riemer | frankx.ai-vercel-website (protected homepage), frankx-mind (private), awesome-agent-skills, realityarchitect, ai-architect-academy, and the archive graveyard with redirect READMEs | personal brand and archives only |
| Other existing orgs (Frank to list) | per org | dispose each as: merge into one of the four above, or archive with recovery tag | |

Rule: the personal namespace never holds substrate or anything a BV should own. Transfer preserves stars, watchers, issues, and 301 redirects, so stars are not a reason to keep a repo personal.

### What breaks on transfer and the fix

| Breaks | Fix on the per-repo transfer checklist |
|---|---|
| Vercel git integration detaches | Install the Vercel GitHub App on the new org before transfer; re-link the same hour; verify a READY production deploy from the new remote before closing the item |
| npm provenance and trusted publishing are per owner | Claim npm scopes first; update `repository.url`; re-bind trusted publisher; publish a patch release to prove it |
| GitHub App and OAuth installs (Claude, Dependabot, Vercel, merge steward) | Install at org level once; re-authorize per repo |
| Org-level Actions secrets and variables do not travel | Re-set `ESTATE_AUTONOMY` and keys per `agentic-ops-hub/docs/ESTATE-OPS-ACTIVATION.md` |
| Org rulesets do not travel | Define one org ruleset per org before the first transfer: no force-push on main, signed recovery tags |
| marketplace.json `source` refs and instruction links | Git redirects keep them working; the generator rewrites them on next sync; estate-guard flags surviving `frankxai/<transferred>` strings as medium |

Sequencing rule, stated once: **tag, consolidate, row at S2 or higher, transfer, verify deploy, then archive the sources where they stand.** Nothing is transferred in order to be archived.

Read: `Starlight-Intelligence-System/docs/architecture/STARLIGHT_PORTFOLIO_TOPOLOGY.md` (disposition table, branch convergence contract), `agentic-ops-hub/docs/ESTATE-OPS-ACTIVATION.md`.

## 2. Repo topology

### Cluster decisions

- **FrankX retires as a code repo.** About 73 percent byte-identical to the website; only the website deploys. Unique strategy docs move to the front door by owner-selected PR, not bulk. Recovery tag, redirect README, 7-day window, archive. Frank signs (paid history).
- **arcanea merges into arcanea-ai-app.** The live app owns the design system; the 40 colliding package versions resolve in its favor. Canon leaves code: one private `arcanea-canon` holds the single `CANON_LOCKED.md`; the other copies become pointer files.
- **Income merges into agenticincome.** agenticpassiveincome catalog and MCP fold in, domain redirects; agentic-income-template becomes `templates/`; agentic-income-skills becomes a marketplace pack. frankx.ai keeps its own Polar route for the first sale, then the two stores reconcile under one offer registry (the registry row for frankx.ai already says "one offer registry").
- **Mind cluster (9) becomes 2:** `mind-intelligence-system` (public product plus skills pack) and `frankx-mind` (private).
- **Marine cluster (4) becomes 2:** `marine-mcp` (Apache-2.0, free corpus, absorbs marine-agent-skills and blue-life-commons data) and `ocean-intelligence-system` (private metered gateway, stream R6, mock figures removed).
- **claude-flow/SPARC agent set deleted from all four repos.** Upstream MIT material (ruflo in `upstreams.json`), not estate IP, and the largest single contributor to the 7,861-file count. Estate agents are the 151 in the SIS registry.
- **awesome-* lists become one `awesome-agent-skills`**, CC BY 4.0, sections per domain.
- **oci repos become one `oci-ai-architect`**, Apache-2.0, skills published as a pack.
- **SIS becomes the substrate monorepo** (pnpm plus turbo), absorbing starlight-swarm, starlight-cosmos-engine, agentic-intelligence-system, starlight-agent-skills, payment-intelligence-system. starlight-evals stays separate on purpose: the judge does not live in the repo it judges. starlight-memory stays separate: public contract with external consumers.
- **GenCreator becomes one monorepo** (apps/web, apps/community, apps/studio). agentic-creator-os goes S6: registry stale since July, agent set is a claude-flow copy; extract its packs, archive next quarter.
- **Academies merge** into one `ai-architect-academy` (S2, gate 100 signups). ai-music-academy and music-intelligence-systems go S6 unless a row claims them.
- **Orphans and the empty repo** go S7 in wave 1 with recovery tags.

### Target living repos (24)

| Repo | Org | Layer | License | Shape |
|---|---|---|---|---|
| Starlight-Intelligence-System | starlight-intelligence | L0 to L2 | FSL-1.1-ALv2; protocol packages Apache-2.0 | monorepo |
| starlight-evals | starlight-intelligence | L7 | Apache-2.0 | poly |
| starlight-memory | starlight-intelligence | L1 | Apache-2.0 | poly |
| starlight-private-memory | starlight-intelligence | L1 | UNLICENSED | private |
| agentic-ops | starlight-intelligence | L6 | UNLICENSED | private source of truth |
| agentic-ops-hub | starlight-intelligence | L6 | CC BY 4.0 docs, Apache-2.0 scripts | public projection |
| claude-skills-library | starlight-intelligence | L5 | Apache-2.0 manifests; per-item content | the marketplace |
| starlight-agent-lab | starlight-intelligence | L1 | Apache-2.0 | quarantine |
| gencreator.ai | starlight-intelligence | L3 | FSL-1.1-ALv2 | monorepo |
| agenticincome | starlight-intelligence | L4 | FSL-1.1-ALv2 | monorepo, income store |
| agentic-business-os | starlight-intelligence | L3 | Apache-2.0 skeleton; packs FSL | template |
| mind-intelligence-system | starlight-intelligence | L3 | FSL-1.1-ALv2 | poly |
| marine-mcp | starlight-intelligence | L1 | Apache-2.0 | poly |
| ocean-intelligence-system | starlight-intelligence | L2 | UNLICENSED | private |
| vibeclubs | starlight-intelligence | L3 | FSL-1.1-ALv2 | poly; fix the ERROR deploy or S6 in 7 days |
| arcanea-ai-app | Arcanea-Labs | L3 | FSL-1.1-ALv2 | monorepo |
| arcanea-canon | Arcanea-Labs | canon | All rights reserved | private |
| arcanea-academy | Arcanea-Labs | L3 | FSL-1.1-ALv2 | poly, 90-day TTL |
| oci-ai-architect | oci-ai-architects | L5 | Apache-2.0 | poly |
| frankx.ai-vercel-website | frankxai | L3 | FSL-1.1-ALv2 code; content all rights reserved | poly, protected homepage |
| frankx-mind | frankxai | L1 | UNLICENSED | private |
| awesome-agent-skills | frankxai | L5 | CC BY 4.0 | poly |
| realityarchitect | frankxai | L3 | FSL-1.1-ALv2 | poly; S6 after the $39 sale |
| ai-architect-academy | frankxai | L3 | FSL-1.1-ALv2 | poly |

Everything else in the 367 is S6 (maintenance lane) or S7 (recovery tag, redirect README, archive). Merges move history with `git subtree` or `git filter-repo` on retained paths only. No `cp -r` between repos.

Read: `agentic-ops-hub/registry/vercel-projects-2026-10-13.md`, `agentic-ops-hub/ECOSYSTEM.md` (re-date it).

## 3. Pack and instruction distribution

**Mechanism: npm packages under one scope, consumed by one generator, pinned by one lockfile.**

- Packages: `@starlight-intelligence/estate-guard`, `/web-excellence`, `/routine-contract`, `/instructions` (shared AGENTS.md and CLAUDE.md sections as named blocks), `/harness-adapters`. Source stays in `claude-skills-library/packs/*`; CI publishes with provenance.
- Generator: `estate sync`, extending `Starlight-Intelligence-System/src/marketplace/pack-manager.ts`, same shape as `agentic-ops-hub/scripts/sync-agent-rules.mjs --check`. Renders workflows, the marked block in `AGENTS.md`, `CLAUDE.md` as a shim (`@AGENTS.md` plus deltas), and adapters for Cursor, Gemini, Grok, Codex, OpenCode, and Void (Cursor-compatible rules). Generated files carry the tamper-evident header from `layering.md`.
- Lockfile: `estate.lock.json` per repo. CI job `estate sync --check` fails on drift. estate-guard counts vendored copies; target zero across living repos.
- Claude Code marketplace, Codex, Cursor, and the rest are channels; `marketplace.json` points at the same package versions.
- claude-flow is not distributed by the estate at all.

**Divergence rule:** a repo may override a block only in `estate.overrides.yaml` with `reason`, `owner`, `expires` (max 90 days). Overrides render with a visible banner; expired overrides are a high finding. Production websites may pin a package minor behind for 30 days; substrate repos may not.

Read: `agentic-ops-hub/docs/layering.md`, `Starlight-Intelligence-System/src/marketplace/pack-manager.ts`, `claude-skills-library/packs/estate-guard/`.

## 4. Where plans live

| Kind of truth | One authority | Frozen with redirect README |
|---|---|---|
| Lifecycle rows | `frankxai/agentic-ops` registry; projection `agentic-ops-hub/registry/` | per-repo status tables, `products.graph`, `REPO-LANES` |
| Session ledger and handover | `agentic-ops-hub/ops/OPS-LEDGER.md`, `ops/sessions/YYYY-MM-DD.md`, `ops/NEXT-PROMPTS.md` | FrankX `docs/ops`, SIS `docs/ops/HANDOVER*`, arcanea-ai-app `docs/ops` |
| Strategy front door | `Starlight-Intelligence-System/docs/strategic/` | FrankX `docs/strategy` (archives with the repo); website `docs/strategy` keeps only pages the site renders |
| ADRs | `docs/adr/NNNN-title.md` per living repo; estate-wide in SIS `docs/adr/`; template ships in the instructions package | ad hoc decision docs |
| Agent registry | `Starlight-Intelligence-System/agents/AGENT_REGISTRY.md` (151) | ACOS registry |
| Skill catalog | `claude-skills-library/catalog/skills.json`; pack registry `SIS/packs/registry.json`; both generated | every other `marketplace.json` |
| Handover format | the daily `ops/sessions` file: Done, Receipts, Open, Next prompt | all HANDOVER streams |

**Issue plane: GitHub Projects**, one org-level project per org with fields state, owner General, gate, mirroring the registry.

**Bulk triage rules** for the 435 open issues and 394 open PRs, scripted, dry-run first, counts logged to the ledger:

1. Repos going S7: close all open items `not_planned` with a comment linking the recovery tag.
2. S6 repos: close anything with no activity for 90 days; keep security findings.
3. Living repos: dependabot and estate-guard items keep labels; everything else gets `triage` and a 14-day window; the owner General moves it into the project or it closes.
4. The five repos holding 260 open PRs (agentic-ops-hub 73, arcanea-ai-app 57, gencreator.ai 56, frankx.ai-vercel-website 43, SIS 31) run the branch convergence contract: adopt, supersede, archive, investigate, bottom-up for stacks.
5. Issues from merged clusters: transfer only items the owner General labels `keep` inside the window.

Read: `agentic-ops-hub/registry/README.md`, `agentic-ops-hub/ops/README.md`.

## 5. Platform and marketplace

**MVP that takes a first third-party listing inside 60 days:** a listing is a PR to `claude-skills-library` adding `listings/<publisher>/<item>/manifest.json` plus either the pack directory or a pinned git ref. CI runs schema, estate-guard scan, and a starlight-evals lane. Merge means listed. No portal UI in the MVP; the site reads the generated catalog.

- **Manifest:** reuse `MarketplacePackItem` from `src/marketplace/catalog.ts`. Add `publisher` (GitHub org, SIP node id, Polar org id), `license` (SPDX), `revenueShare`, `evalReport` hash, `scanReport` hash; `permissions` stays mandatory; attestation must still carry "Built on SIP". Extend `MarketplaceHarnessTarget` with codex, gemini, opencode, void; keep universal.
- **Conformance gate:** new starlight-evals lane `marketplace-listing`: manifest valid, SKILL.md frontmatter present, no secrets, declared permissions match observed tool calls in a sandbox run, at least three eval cases with a threshold per item kind. The first 20 estate skills pass the same gate before any third party does. That is the dogfood receipt.
- **Attestation and receipts:** `/sip-attest` on listing; the receipt is the signed tuple (manifestSha, scorecard hash, scan hash, publisher key) stored beside the manifest and in `packs/registry.json`. Polar order webhooks write a receipt row to the ledger. Money plane stays verify-only.
- **Tiers and share:** keep free, subscription, enterprise. Proposal: estate items 100 percent, third party 80/20, alliance nodes 85/15. Frank decides the split.
- **Merchant of record:** Polar, estate account, for every MVP listing; publisher payouts monthly from the ledger. Polar does not split a single order natively, so this is a known manual step until a publisher brings their own Polar org and pays a listing fee instead. Written into publisher terms from day one.
- **Harness targets:** one manifest; `starlight pack build --target <harness>` renders Claude Code plugin, Codex, Cursor rules, Gemini, Grok, OpenCode, Void.
- **Channels:** `marketplace.json` in claude-skills-library, the npm scope, zip kits on R2 behind Polar signed URLs, starlightintelligence.org/marketplace reading the catalog projection.
- **Trust:** estate-guard scan on every submission (secrets, prompt-injection patterns, undeclared network or filesystem use, license header), SHA pinning, publisher identity bound to a GitHub org and a SIP node declaration, optional signature.
- **Stays proprietary:** the 52-plugin private suite, Generals' prompts, routing tables, the agentic-ops registry, alliance register, canon, customer data, private estate-guard rules.

Read: `Starlight-Intelligence-System/src/marketplace/catalog.ts`, `docs/strategic/plugin-product-system-doctrine-2026-06-19.md`, `starlight-evals/SPEC.md`, `claude-skills-library/.claude-plugin/marketplace.json`.

## 6. IP, brands, income protection

1. **License sweep, in order:** (a) the 11 repos with no LICENSE: FSL unless protocol, same day; (b) the 3 CC0 repos: tag the boundary, relicense forward, state in the README that prior CC0 releases stay CC0; (c) about 30 MIT repos: keep MIT where external contributors or forks exist (awesome lists, oci), relicense sole-authored repos at a tagged boundary; (d) copyright line "Frank Riemer" plus NOTICE in every living repo, shipped by the instructions package.
2. **DCO now, CLA before the first external PR on an FSL repo.** DCO sign-off on Apache repos today. CLA Assistant on FSL repos; until it exists, a CI label blocks external PRs to commercial layers, which makes the current written policy mechanical.
3. **Trademarks:** word marks for FrankX, Arcanea, Starlight Intelligence, GenCreator at EUIPO in classes 9, 41, 42; Arcanea adds 16. Which marks first and the budget are Frank's call.
4. **npm scopes:** claim `@starlight-intelligence`, `@arcanea`, `@gencreator`, `@frankx` this week; trusted publishing only from the target orgs.
5. **Domain registry:** `domains.json` in agentic-ops (registrar, expiry, DNS authority, brand, entity); projection to the hub.
6. **Private boundary:** the economic-boundary rule in `arcanea/LICENSING.md`, enforced by estate-guard: anything on the proprietary list in a public repo is a high finding.

Read: `arcanea/LICENSING.md`, the production architecture doc section 8.2.

## 7. Contribution ladder

| Rung | Gets | Gate |
|---|---|---|
| User | free packs, the AGENTS.md pattern, catalog, community channel | install |
| Replicator | registered downstream of agentic-business-os, support channel, listing eligibility | row in `downstreams.json`, estate-guard green |
| Vertical owner | a vertical namespace in the marketplace, 80/20 share | one listed item passing evals, CLA signed, one paying user |
| Partner | co-delivery on R1 and R2 commissions, referral share, DELIVERY.md tier access | one co-delivered SOW |
| Alliance node | declared domain and decision rights per ALLIANCE.md, 85/15 share, attestation | node declaration, attestation record, Frank signature |

Each rung is a publisher class in the manifest; review depth and payout terms follow the rung. Trinity is the first alliance node and the first third-party listing.

Read: `Starlight-Intelligence-System/ALLIANCE.md`, `DELIVERY.md`.

## 8. Execution

| Phase | Weeks | Owner General | Work | Receipt | Kill or escalate |
|---|---|---|---|---|---|
| P0 Revenue and freeze | 1 to 2 | CFO | Attach `frankxai/agentic-ops` and settle what it is. Polar env set on frankx.ai; Blueprint $67 flipped to for-sale in the existing route; product page passes integrity guard; homepage untouched. Tag `consolidation-2026-10-start` on all 56 checkouts | first external payment webhook row in the ops ledger | no checkout by day 14: escalate to Frank; no sale by day 30: freeze new SKUs, plan continues |
| P1 Governance surfaces | 2 to 4 | COO | front door, ledger redirects, ADR convention, registry rows for all 24 living repos, license sweep (a) and (b), npm scopes claimed, orgs created empty, org rulesets, GitHub Projects per org | every living repo has a row; estate-guard reports zero living repos without LICENSE | a row contested more than 7 days goes to the weekly pulse |
| P2 Packs | 3 to 6 | CTO | publish the five packages; `estate sync` generator; roll out to living repos; delete vendored copies and the claude-flow set | `estate sync --check` green in all 24; vendored-copy count 0 | a repo that cannot sync in 2 weeks gets an override with expiry, not an exception |
| P3 Consolidation waves | 5 to 9 | CTO plus CPO | A: FrankX retire, arcanea merge, canon to one repo. B: income, mind, marine. C: oci, awesome, academies, orphans. Bulk triage rules 1 to 5 run per wave | per repo: recovery tag, PR with retained paths, redirect README, 7-day window logged, archived | any merge that needs a force-push stops and goes to Frank |
| P4 Org migration | 8 to 12 | CTO, Frank signs | transfer living repos per completed wave; Vercel re-link; App installs; secrets; provenance patch release | READY production deploy from the new remote per deployed project; old URLs 301 | a transfer with a broken deploy for more than 24 hours transfers back |
| P5 Marketplace MVP | 6 to 12 | CPO plus CAIO | evals lane; first 20 estate skills through it; submission pipeline; publisher terms; first third-party listing (Trinity) | listing merged with receipt tuple and a Polar product by week 9 | no third-party listing by week 12: marketplace goes S3 hold, not killed |
| P6 IP and community | 12 to 16 | CEO | trademark filings, CLA Assistant, ladder published, archive wave 2 (the 11 Vercel S7 candidates), ECOSYSTEM.md re-dated | filing numbers and archive tags in the ledger | none; this phase has a date, not a kill |

Constraints honored throughout: no bulk copies between repos, recovery tag before archive, no force-push on main, Frank signature on every irreversible step, frankx.ai homepage untouched, counts quoted only as measured.

## Decisions only Frank can make

1. **Entity and namespace mapping:** `starlight-intelligence` to Starlight Holding BV, `Arcanea-Labs` to Arcanea BV, frankx.ai stays personal; plus the written copyright assignment schedule, without which org naming is cosmetic. Also the list of other existing orgs and their disposition.
2. **Money:** the first prices as they stand in the registry (Blueprint $67, Worldbuilder EUR99, Founding Council EUR99) and the marketplace split (80/20, alliance 85/15).
3. **Relicensing and marks:** the MIT and CC0 boundary tags for sole-authored repos, and which trademarks file first with what budget.

## Verification

- P0: a Polar order webhook row appears in `agentic-ops-hub/ops/OPS-LEDGER.md` naming the order id; frankx.ai homepage contract test unchanged.
- P1: `node .claude/ci/estate-guard-scan.mjs --root .` on each living repo reports no missing LICENSE; `registry/` has 24 rows with owner and gate.
- P2: `estate sync --check` exits 0 in all 24 repos; `md5sum` across estate-guard copies returns one hash or zero copies.
- P3: each archived repo has a signed recovery tag, a redirect README, and a ledger line with the 7-day window dates; `git log` on merge PRs shows subtree or filter-repo history, not a single bulk commit.
- P4: Vercel `list_deployments` shows READY production for each transferred project from the new remote; old GitHub URLs return 301.
- P5: `catalog/skills.json` shows 20 estate items with eval report hashes; the Trinity listing PR is merged with the receipt tuple and a Polar product id.
- P6: EUIPO filing numbers and CLA Assistant status recorded in the ledger.

## Critical files

- `/home/user/agentic-ops-hub/registry/README.md`
- `/home/user/agentic-ops-hub/registry/vercel-projects-2026-10-13.md`
- `/home/user/Starlight-Intelligence-System/docs/architecture/STARLIGHT_PORTFOLIO_TOPOLOGY.md`
- `/home/user/Starlight-Intelligence-System/docs/strategic/2026-10-08-agentic-estate-production-architecture.md`
- `/home/user/Starlight-Intelligence-System/src/marketplace/catalog.ts`
- `/home/user/agentic-ops-hub/docs/layering.md`
- `/home/user/arcanea/LICENSING.md`
- `/home/user/frankx.ai-vercel-website/app/api/checkout/polar/` (P0 route)
