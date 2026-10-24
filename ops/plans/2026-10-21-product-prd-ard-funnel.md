# Starlight Receipts: product plan (PRD, ARD, UX, funnel, ranking, metrics)

Author: Claude Code, 2026-10-21. Status: **proposal for Frank**. Nothing here spends money, sets a price, picks a licence or publishes. Those stay Frank's.

Sources: the estate scout of hub PRs 343-378 and `OPS-LEDGER.md` (21 Oct), the Routing Brain work (PR 377), the lab (PR 379). Claims the scout could not verify are marked **UNVERIFIED**. Numbers in the metrics sections are targets to test, not baselines; no baseline exists yet.

## 1. The product in one paragraph

**Starlight Receipts** lets a person or small team run several coding agents (Claude Code, opencode, Codex, OmO and others) under one budget and **prove what each task cost and who checked it**. A router picks the model per task class under a cost ceiling and a data-handling rule (ZDR). Every call writes a signed receipt. A verifier anyone can run recomputes spend, checks that maker and checker differ, and flags receipts that do not add up. The moat is the **receipt format plus our own measured data on which model wins which task class at what cost**. Models and harnesses are rented; the ledger and the measurements are ours.

This is the north star already in the estate: "Sovereign delegation, proven by receipts" (`lab/goals.json`, Starlight strategy 2026-09-18) and the PR 356 category line: "a runtime that routes work to the best provider under a budget and leaves a receipt".

## 2. Where we are (facts, with sources)

| Area | State | Source |
|---|---|---|
| Routing Brain v5 | Built, local Python on one Windows box, 7 task classes, ZDR flags, receipts. Live proof: Token Pass call resolved to `token-pass`, 403 fallback walk worked, 5 receipts (synthetic/test). | OPS-LEDGER 21 Oct |
| Hardening | PR 377 (draft). Codex rounds 1 and 2 both CHANGES REQUESTED; round-2 fixes in progress. Not merged. | PR 377 |
| Research lab | PR 379 (draft): registry, validator, 12 tests, dashboard. **No experiment has run.** | PR 379 |
| Receipts elsewhere | SIS run-receipt v1; Queen's signed `starlight.run-receipt.v1` per dispatch (starlight-swarm#39, unmerged); work-registry mission id `M-YYYYMMDD-xxxxxx`. | PR 351, 373 |
| Second router | Queen's model routing (starlight-swarm#39) and PR 356's "routing policy" promise overlap Routing Brain. | PR 356, 373 |
| Money path | 0 of 62 Vercel projects take money. Polar is the rail; Polar's merchant and per-offer approval is a launch gate. | PR 378 |
| Packaging | `@starlight-intelligence/*` npm packs planned (PR 356). Publication **UNVERIFIED**. Licence and open-core ruling **UNVERIFIED** (queued for Frank). | PR 356 |
| Capacity | 3.4 GiB RAM free, below the 4 GiB floor; sentinel YELLOW; mutation runs held. GitHub Actions budget $0. | restart CURRENT.md |
| Focus | Until 20 Nov only a nine-repo spine gets features (PR 378 guardrail). Frank's dated goals: first sale by 4 Nov, first customer-validated launch by 20 Nov. | PR 378, 356 |

## 3. Decisions this plan needs from Frank (summary)

1. **One receipt schema. DECIDED 2026-10-21: SIS run-receipt v1 is the envelope.** Correction: v1 forbids extra properties, so there is no extension block; routing detail travels in stage notes and hash-bound evidence. See `ops/plans/2026-10-21-receipt-schema-decision.md`. `routing.jsonl` stays as the raw call-level source, not a competing format.
2. **One router.** Recommendation: Routing Brain owns policy data and classification (it has the budget and ZDR code); Queen consumes it as its model-selection step. Reason: Queen#39 has no independent checker yet and Routing Brain has the tests.
3. **Open-core boundary.** Recommendation below (section 7). Needs Frank's licence and trademark ruling.
4. **ZDR default.** Recommendation: fail-closed (unrecognised task means ZDR class). The PR 377 fork is implementing this on the draft branch; it is reversible.
5. **Which spine repo hosts the product.** The nine-repo spine rule blocks features elsewhere until 20 Nov. UNVERIFIED which repo hosts `fleet/`; if it is not in the spine, only fixes and the named gate may land there.
6. Prices, Polar approval, Railway cap, Token Pass key (already open in `lab/gates.json`).

## 4. PRD

### 4.1 Problem

People who run more than one coding agent cannot answer three questions: what did that task cost, which model should have done it, and did a different party check it. Spend leaks (a plaintext gateway key was found on our own machine), free models are used on data that must not leave, and "the agent said it passed" is the only evidence.

### 4.2 Users and jobs

| Persona | Job | Why they pay |
|---|---|---|
| **P1 Solo agent power user** (the founder, and people like Frank) | Run 2-5 harnesses without a surprise bill or a leak | Stops waste, gives proof of cost per task |
| **P2 Small team / agency lead** | Give agents budgets per project and show a client what was done | Receipts double as an audit trail they can hand over |
| **P3 Platform or security owner** | Enforce ZDR and approved models across a team | Policy as data plus a verifier |

First target is P1 (we are P1; dogfood is free and fast). P2 is the first paying segment. P3 is later and needs tenant isolation we do not have.

### 4.3 Scope by release

**R0 "Local proof" (target: before 20 Nov):** routing and receipts on one machine, open spec, verifier, weekly digest, free and Token Pass profiles of oh-my-starlight, public benchmark page generated from real receipts.
**R1 "Team ledger":** hosted ledger and dashboard, BYO key, shared budgets, Slack/GitHub digest.
**R2 "Workers":** managed cloud workers (activated first), draft PR output.
**R3 "Marketplace":** third-party packs with manifest, eval hash, revenue share (reuses claude-skills-library catalog).

### 4.4 Requirements (R0)

| ID | Requirement | Acceptance test |
|---|---|---|
| F1 | Classify a task into a class; unknown means ZDR | Corpus of 100 labelled prompts: no ZDR task reaches a non-ZDR model |
| F2 | Reserve budget before a call, settle after; holds bound to class and model | Concurrency test: spend plus holds never exceeds cap |
| F3 | Write one receipt per call in the single schema | Schema validation in CI; verifier recomputes totals |
| F4 | `verify` command: recompute spend, check maker differs from checker, flag gaps | Fixture set with 10 planted faults, all flagged |
| F5 | Weekly digest from receipts (cost per accepted task per class) | Digest generated from real receipts only; empty state otherwise |
| F6 | Free and Token Pass profiles for OmO/opencode | Generated config passes a no-leak check (no key in file, only `{env:...}`) |
| F7 | Lab dashboard reads receipts | Already built (PR 379) |

Non-goals for R0: hosted anything, multi-tenant, auto-merge, money movement (payments doctrine: no autonomous money movement, PR 375).

### 4.5 Risks

- Benchmarks are contaminated or not ours: the lab replays our own closed PRs instead.
- Token Pass terms can change; the router must keep a free-only profile working.
- OmO licence (SUL-1.0) forbids a commercial fork: we ship config and governance, not a fork.
- A receipt is only as trustworthy as who signs it. The first version proves consistency and separation of duties, not that the model never lied. Say so in the spec.

## 5. ARD (architecture)

```
task --> classifier --> policy (routing.schema.json, ZDR, ceilings)
                          |
                    reserve(budget) --> harness/gateway call --> settle
                          |                                        |
                          +------------- receipt writer <----------+
                                              |
                          ledger (jsonl local, signed) --> verifier --> digest, dashboard, lab
```

Key decisions (ADRs, each with the alternative rejected):

| ADR | Decision | Rejected alternative and why |
|---|---|---|
| A1 | Policy is data (`routing.schema.json`), code only enforces it | Hard-coded chains: unreviewable, drifts (the OmO generator already drifted) |
| A2 | Fail closed on ZDR and on an unusable ledger root | Fail open: one checkout gets its own budget (Codex finding 5) |
| A3 | Reserve then settle, holds bound to (class, model), expiry never frees budget silently | Plain timeout release: both calls settle, spend exceeds cap (Codex finding 2) |
| A4 | One receipt envelope (SIS run-receipt v1), routing detail in stage notes and hash-bound evidence | Three formats: no single verifier. A custom extension: v1 forbids extra properties |
| A5 | Maker and checker are different actors, enforced by the verifier | Self-attestation: the author never checks their own box |
| A6 | Harness-neutral: opencode headless first, others as challengers measured in EXP-002 | Betting on one harness: the market moves weekly |
| A7 | oh-my-starlight is a config and governance pack on upstream tools, not a fork | Fork OmO: licence bars commercial use, permanent merge debt |
| A8 | Git is the record, a generated page is the dashboard, Artifact is a snapshot | Notion as a second copy: drifts |
| A9 | BYO key for any external user; we never hold their provider keys in R0 | Resell tokens: pricing and compliance exposure |

Security boundaries: keys only as `{env:...}`; receipts never contain prompts or outputs by default (hashes only); the ledger path is validated; external users run the router on their machine in R0, so there is no tenant isolation problem yet. R1 hosted ledger stores receipts only, never prompts.

Capacity: the laptop is YELLOW. R0 needs no extra RAM beyond a Python process. Anything heavier (benchmark replays, workers) runs in CI or on Railway under a cap, not on this machine.

## 6. UX and funnel

### 6.1 First-run experience (target under 10 minutes to first receipt)

1. Install one pinned package (no `curl | sh`).
2. `starlight init` writes a profile (free or Token Pass), checks that no key is in a config file, and sets a monthly cap.
3. `starlight run "<task>"` routes, calls, and prints the receipt line: class, model, cost, ZDR status.
4. `starlight verify` after a task shows pass/fail with reasons.
5. Monday digest: "cost per accepted task, per class" and the one change worth making.

Design rules: the receipt line is the product moment, so it is short and readable; errors say what to do (for example "key found in opencode.json, move it to env, command below"); empty state says "no real receipts yet" and never shows fake numbers.

### 6.2 Funnel (AARRR) with the metric and target to test

| Stage | Event | Metric | R0 target (hypothesis) |
|---|---|---|---|
| Awareness | Reads the benchmark or spec page | Unique visitors | UNVERIFIED baseline; frankx.ai had zero analytics for months until a fix (frankx.ai#1068), so instrument first |
| Acquisition | Clicks install | Visitor to install page rate | 5% |
| Activation | First receipt written | Install to first receipt within 10 min | 60% |
| Aha | First `verify` passes or catches a fault | Activated users who run verify | 40% |
| Retention | Receipts in week 2 and 4 | Weekly active receipts per user | 50% still active at week 4 |
| Revenue | Starts a paid plan or buys an edition | Activated to paid (R1) | 3-5% |
| Referral | Shares a digest or badge | Shares per active user | 0.2 |

Distribution that exists: frankx.ai (founder proof and front door), Starlight Intelligence site, npm under `@starlight-intelligence/*`, GitHub, claude-skills-library marketplace. Money: Polar (merchant approval is a launch gate), founders' Stripe links for factory pages. No checkout before Polar approves.

### 6.3 Packaging (proposal; prices are Frank's)

| Tier | Contents | Price | Basis |
|---|---|---|---|
| Open | Router, schema, verifier, free profile, spec | Free | Open-core; builds trust and the standard |
| Pro (individual) | Token Pass profile, digest, benchmark data feed, lab dashboard template | Test at about $9-19 a month or a one-off edition | Estate editions are listed at roughly $39-$99 in earlier notes (Blueprint $67, Realityarchitect $39, Founding Council EUR99); UNVERIFIED, no live offer or repo evidence was checked for these figures, so confirm each against the live offer before quoting; a one-off edition is the cheapest first test |
| Team (R1) | Hosted ledger, shared budgets, digest to Slack/GitHub, audit export | Test at about $49-99 a seat-group a month | Hypothesis only; validate with 3 design partners before pricing |
| Workers (R2) | Managed activated workers | Usage-based plus margin | Needs EXP-004 cost data first |

These are hypotheses to test with real buyers. Do not publish before Polar approval and Frank's ruling.

## 7. Open-core boundary (recommendation)

Open: the receipt schema, verifier, classifier corpus, free profile, generator. Reason: a standard that cannot be inspected is not trusted, and the moat is data and the hosted ledger, not the parser.
Closed (or source-available): aggregated benchmark data across users, hosted ledger, managed workers, curated packs.
Trademark "Starlight Receipts" order: Frank's decision. Keep OmO-derived content out of the open repo unless its licence allows it.

## 8. Ranking of what to build (my scoring, 1-5, higher is better; judgement not measurement)

Score = moat x time-to-first-user x low-cost x unblocked, then ranked.

| Rank | Initiative | Moat | Speed | Cost | Unblocked | Notes |
|---|---|---|---|---|---|---|
| 1 | Merge PR 377 (hardening) | 4 | 5 | 5 | 4 | Everything else depends on its receipt API |
| 2 | One receipt schema plus verifier (F3, F4) | 5 | 4 | 5 | 3 | Needs decision 1; this is the moat |
| 3 | Suite `starlight-core-v0` plus EXP-001 and EXP-006 | 5 | 3 | 4 | 3 | Produces the first real, ours-not-theirs numbers; free runs cost $0 |
| 4 | Public benchmark page from real receipts | 4 | 4 | 5 | 2 | Awareness engine; blocked by 3 |
| 5 | oh-my-starlight packs (free, Token Pass) | 3 | 4 | 5 | 4 | Distribution wedge, low risk |
| 6 | Weekly digest | 3 | 5 | 5 | 3 | Retention hook |
| 7 | Key rotation and `{env:}` migration | 2 | 5 | 5 | 1 | Frank must create the key; also removes our own leak |
| 8 | Polar offer plus first edition | 3 | 3 | 4 | 2 | Gated on Polar approval |
| 9 | Hosted ledger (R1) | 4 | 2 | 2 | 1 | Only after 5 and 6 show retention |
| 10 | Cloud workers (R2) | 3 | 2 | 2 | 1 | Reuse the railway-ci-runners findings in the ledger; do not re-measure |
| 11 | Marketplace (R3) | 4 | 1 | 2 | 1 | Needs a third-party publisher first |

Overlaps to resolve instead of building again: receipts (3 formats), routers (2), Railway worker measurements (EXP-004 vs ledger `railway-ci-runners`), harness packs (PR 356 npm packs, claude-skills-library packs, `gen_omo_config.py`).

## 9. Roadmap with dates

| When | Goal | Exit evidence |
|---|---|---|
| By 25 Oct | PR 377 round 3 clean and signed by a different harness; Frank decisions 1, 2, 4 | Signed SHA; schema ruling written |
| By 1 Nov | Receipt envelope merged; verifier with 10 planted-fault fixtures; key rotated | CI green; old key removed (id in session notes) |
| By 4 Nov | Suite v0 (12 closed PRs with tests); EXP-006 and EXP-001 free arm run | `lab/results/EXP-00x.md` from receipts |
| By 10 Nov | Benchmark page and digest from real receipts; oh-my-starlight free profile | Page generated in CI; no synthetic numbers |
| By 20 Nov | 3 design partners using R0; one paid test (edition) if Polar has approved | Interview notes; Polar approval status |
| After 20 Nov | Decide R1 on retention data | Week-2 active receipts per user |

CI note: the Actions budget is $0 so private CI fails before any step. Until Frank sets a November budget, run tests locally and have the checker harness run them; do not claim CI green.

## 10. Success metrics

**North star:** accepted tasks per week that have a verified receipt (maker is not checker, cost recomputed).

Leading indicators: receipts with a passing verifier; share of tasks routed to the cheapest sufficient model; time to first receipt; ZDR violations (must be 0).
Guardrails (stop if breached): any key found in a file; spend above cap; a ZDR task on a non-ZDR model; any receipt that fails recomputation without being flagged.
Lab metrics: cost per accepted task per class (EXP-001, EXP-005, EXP-006); acceptance rate versus the baseline model.
Business: first sale by 4 Nov (Frank's goal), design partners by 20 Nov, paid conversion from activated users.

## 11. Other things to consider

- **Legal and trust:** receipts can contain sensitive data, so hashes only by default; GDPR if hosted (EU user, EU region); do not call receipts "tamper-proof" unless they are signed with keys we do not hold for the user.
- **Naming collisions:** `starlight queen` built-in name collides (SIS #462, agentic-ops #289).
- **Provider terms:** Token Pass and gateway terms change; keep a free-only path.
- **Community and standard:** publish the spec early; invite review from other harness authors; this is how a receipt format becomes a standard rather than our file.
- **Support burden:** a solo founder cannot support teams; start with design partners and an issue template.
- **Machine load:** keep heavy runs off the laptop (YELLOW zone).
- **Focus rule:** until 20 Nov, features only in the nine-repo spine.
- **Evidence discipline:** no claim without a source; prior evidence is listed with caveats and never counted as a result (lab README).
