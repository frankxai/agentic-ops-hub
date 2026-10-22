# Strategy map: where each document lives and how the audit offer fits (draft, 2026-10-22)

Author: Claude Code. Status: draft for Frank and a different-harness review. This repository is public, so this map names no key, cap or account detail. This map points to documents; it does not restate or change them. Where documents disagree it says so (section 5). Nothing here is a decision.

## 1. The one line, and where it comes from

"Sovereign delegation, proven by receipts." Source: `lab/goals.json` (`north_star`), which cites the Starlight strategy of 2026-09-18 (Claude Docs artifact `BWdNqCEutFNvSS9HEUzhWH`; memory note `project_starlight_strategy_2026-09-18`). The audit offer, the routing brain, the verifier and the lab all serve it. Nothing in this map should contradict it.

## 2. Layers (what we build) and who owns each document

| Layer | What it is | State on 2026-10-22 | Owning document | Repo / PR |
|---|---|---|---|---|
| L0 commodities | OpenCode, OmO, gateway, models, Claude, Codex | Rented | `fleet/HARNESS-STACK.md` (**unpushed**: exists only on the local branch `agent/c940/massive-action-receipts-20260803`, which is not on `hub`; see section 5 item 9) | n/a |
| L1 memory | SIS memory and MCP bridge | Live | SIS repo docs | Starlight-Intelligence-System |
| L2 routing brain (the moat per `HARNESS-STACK.md`) | Classes, ZDR chains, reserve/settle, strict OpenCode launcher | **Open draft**, 14 Codex rounds, none approved; round 14 returned CHANGES REQUESTED (4 P2) on `c2dd301` | `fleet/ROUTING-BRAIN.md`, `ops/sessions/2026-10-21-routing-brain-hardening.md` | agentic-ops-hub PR 377 |
| Receipt standard | SIS run-receipt v1 (DSSE, in-toto, Ed25519) | Decided 2026-10-21 | `2026-10-21-receipt-schema-decision.md`; SIS `docs/receipts.md` | SIS |
| Verifier | `starlight verify-receipt` | **Open draft**, 5 Codex passes, last APPROVE WITH NOTES then a P3 fix | SIS `docs/receipts.md` "Verifying a receipt" | SIS PR 481 |
| Lab | Registry, validator, dashboard, receipt bridge, EXP-001 to 009 | **Open draft**; no experiment has run (8 experiments `blocked`, EXP-007 `proposed`, no `lab/results`). Its second Codex pass returned CHANGES REQUESTED with 11 findings (10 P2, 1 P3), now being fixed | `lab/README.md`, `2026-10-21-research-lab-and-cloud-workers.md`, `2026-10-21-harness-measurement-and-scale.md` | agentic-ops-hub PR 379 |
| L3 OmS | Config, governance and receipts pack on upstream tools; not a fork | Generator exists; profiles not split. The `oms/` package (manifest, `verify.py`, exporter) is also on the unpushed branch only | `lab/goals.json` pillar `ecosystem`; `HARNESS-STACK.md` | agentic-ops |
| L4 template | `starlight-ai-harness` public template | Local repo only (6 commits), **no remote**; the copy on disk was exported before PR 377 and carries the old classifier. The measurement plan's "Nothing / F (not built)" is stale | `HARNESS-STACK.md` phase 3 | local |
| Product plan | Starlight Receipts PRD, ARD, funnel, tiers | Proposal | `2026-10-21-product-prd-ard-funnel.md` | PR 379 |
| **Audit offer (new)** | Paid or free read-only review of a prospect's agent setup | Draft, no demand evidence | `2026-10-22-audit-offer.md`, `2026-10-22-audit-runbook.md` | this branch |
| Paid layers beyond the audit | Hosted ledger, managed gateway, signing, dashboard | Only Open/Pro/Team/Workers tiers exist in the PRD (section 6.3). **Managed gateway, hosted signing and the audit are not in the PRD.** | none yet | n/a |

## 3. Streams (what Frank runs) and how each touches the audit

| Stream | Role relative to the audit | Boundary or rule that applies | Source |
|---|---|---|---|
| Agentic Income Trinity (agenticincome.ai, agenticpassiveincome.com, dpi) | Not the audit's audience. Trinity sells income education and packs, and its copy rules forbid income promises. At most a cross-link. | Zero income promises; dpi CANON inviolable; Polar is merchant of record | memory `project_agentic_income_trinity` |
| Affiliate Ops Agent | Best internal subject: an agent acting on external accounts, with human-only steps (consent, tax, credentials, 2FA). Its receipts could become a case study after a 30 to 60 day dogfood period (the memory note says "productize after 30–60 days of receipts"; no start date is evidenced). | Relationship state and pricing are private; the case study needs Frank's consent | memory `project_affiliate_ops_agent` |
| GenCreator / ACOS | Later: packs for creators could ship with receipts. Not part of the audit. The premium strategy is private and was **not read** for this map. | Core stays free; premium strategy never goes in a public repo | memory `project_acos_v12` |
| Arcanea | Not involved. Its gateway keys appear in `lab/budget.json`, so they fall under any audit of the estate. | Arcanea Mythic register must not leak into this work | `REGISTER-BOUNDARIES.md` |
| FrankX | Candidate front door and professional register. Analytics was missing for months until a fix (frankx.ai-vercel-website#1068), so a funnel there needs instrumenting first. | FrankX Professional voice; no Arcanea terms | PRD section 6.2; `REGISTER-BOUNDARIES.md` |
| Investor OS | Not involved. Same principle (agents never execute trades), no data shared. No positions in any audit artefact. | Agents never execute trades or move money | memory `project_investor_os` |
| SIS / SIP | Owns the standard and verifier. The strategy's H1 goal (to 2026-10-31) is truth repair, then merge SIS #141 and sip-verify, then "first-ten external signers"; whether audits could produce any is a hypothesis, not a plan. | SIS/ACOS Neutral register | memory `project_starlight_strategy_2026-09-18` |

## 4. What depends on what merging

| Needs | Because | Until then |
|---|---|---|
| PR 377 merged | Audit claims "we fixed these classes" and cites its launcher and settle API | Say "in review" |
| SIS PR 481 merged | Check C10 uses `starlight verify-receipt` | Skip C10 or run from the PR branch |
| PR 379 merged | This branch is stacked on it (the plan documents it reads live there). PR 379's own second Codex review is CHANGES REQUESTED (11 findings) and open | Merge order: 379 before this branch |
| Re-export of `starlight-ai-harness` from the merged router | The on-disk template has the old classifier | Do not publish the template (Frank's button) |
| Frank creates a ZDR-restricted gateway key | C7 recommends it. The ZDR-only key is the control described in `fleet/ROUTING-BRAIN.md` ("What the guarantee covers", about line 75) and the PR 377 session note; the open decision `dec-token-pass-key` covers creating a dashboard key | Do not claim our own setup passes C7 |
| EXP-008 run | Any cost or quality claim about OmS | No such claim in the offer |

## 5. Contradictions and stale statements found (not smoothed over)

1. **Verifier scope.** The product plan requires a `verify` command that recomputes spend and "checks that maker differs from checker" (F4, product plan section 6.1; also ADR A5 and gate `receipt-verifier`, which require maker differs from checker). The verifier in SIS PR 481 explicitly does not check maker against checker, does not check real provider cost, and only checks that `totals.costEur` is not below the stage sum (`docs/receipts.md`). F4 is therefore unmet by 481; the plan or the verifier needs to change. Also the plan's first-run commands (`starlight init`, `run`, `verify`) are not what exists (`starlight verify-receipt`).
2. **BYO key versus a managed gateway.** ADR A9: "BYO key for any external user; we never hold their provider keys in R0". A managed gateway or hosted signing would hold keys. Not in the PRD; it needs its own decision and a data-handling answer.
3. **What "Pro: Token Pass profile" means.** Token Pass is one shared $80 monthly credit on the `starlight-intelligence` team (`lab/budget.json`). The plan does not say whether a paying user brings their own Token Pass or uses ours. Selling access to our pool would be reselling tokens, which A9 rejects.
4. **Stale PR status.** The product plan (section 2) says Codex rounds 1 and 2 on PR 377; `lab/gates.json` item `pr-377` says "round 1"; the measurement plan says 4 rounds and 65 to 71 tests and a classifier decision "in progress". Current state: 14 rounds (round 14 CHANGES REQUESTED), 161 routing tests at `c2dd301` as reported by the fix agent, Option A done. PR 377's own description is stale too. These documents are history, not current state.
5. **Neutral register, pricing, and visibility.** `REGISTER-BOUNDARIES.md` forbids "product pricing" and brand CTAs in SIS/ACOS Neutral repos (`agentic-ops` is listed there), yet the product plan (section 6.3) carries tier price hypotheses. Those plans live in `agentic-ops-hub`, which is a **public** repository (`agentic-ops` is the private one), so the plan documents, PR 379 and PR 381 are publicly readable. Public copy needs a home in FrankX Professional register.
6. **Focus rule (measured clash).** `hub/main:ops/plans/estate-convergence-2026-10-21.md` lists `agentic-ops-hub` as "This record; drain only", capped at 3 open agent PRs. It has 88 open PRs (checked 2026-10-22), 77 of them on `agent/*` branches per the review. It puts Starlight-Intelligence-System on Hold ("no new features"). PRs 377, 379, 381 and SIS PR 481 therefore all clash with PR 378's guardrail until the rule is lifted or the drain owner rules otherwise. The helper script `scripts/audit_inspect.py` is a feature in whichever repo holds it.
7. **Dates attached to the wrong product.** In the estate-convergence plan, "first sales by 4 November" is the frankx.ai Blueprint at $67 via agenticincome, and the 20 November launch is the starlightintelligence.ai launch factory. Neither depends on the receipts product or the audit. The error is the product plan (section 2 and its roadmap) attaching those dates to receipts. The fix belongs in the PRD.
8. **Two routers.** Queen's model routing (starlight-swarm#39) overlaps the Routing Brain. The plan recommends Routing Brain owns policy and Queen consumes it. Still Frank's decision.
9. **A source document that is not on main, or even on the remote.** `fleet/HARNESS-STACK.md` defines the layer names (L0 to L4) and is cited by the measurement plan, `lab/harnesses.json`, EXP-008 and this map, but it is tracked only on the local branch `agent/c940/massive-action-receipts-20260803`. That branch is not pushed to `hub`: the remote copy lacks the file and the local branch is ahead of it. The restart card said 42 commits ahead of main; a review measured 45. Until it is pushed and merged, the layer model is not on main.
10. **Rotation is open, and old key material persists (needs Frank).** Gate `dec-token-pass-key` in `lab/gates.json` is still `open` and says the exposed key is to be rotated; no commit records a rotation. A review also found two plaintext backups of the owner's OpenCode config holding a key different from the live one. Do not state that any exposed key was rotated or removed until the gate is closed with a date, and decide what happens to the backups. No values are recorded here.
11. **Our own setup would fail our own checks.** Generic classes found on our own machine (a missing `small_model`, a free provider enabled beside the gateway, a provider with an `npm` override, a stale temporary config file) match checks C3, C2 and C13. Details are kept privately because this repository is public.

## 6. Decisions left for Frank

| Decision | Owner document | State |
|---|---|---|
| Price, rail (Polar or invoice), and channel for the audit | audit offer | open |
| Open-core boundary, licence, trademark ("Starlight Receipts") | PRD section 7; `lab/gates.json` `dec-open-core` | open |
| Single router: Routing Brain or Queen | PRD section 3, item 2 (starlight-swarm#39 is open; PR 378 freezes starlight-swarm through 20 Nov, which defers this) | open |
| Managed gateway and hosted signing: do we hold keys; GDPR and key custody | none | open, new |
| ZDR strictness (strict or allow free) | `lab/gates.json` `dec-zdr-strictness` | open; code is strict by default |
| Create a ZDR-restricted gateway key; lower caps on shared keys | `dec-token-pass-key` (creating the dashboard key and rotating the exposed one); the ZDR-only and cap choices are in the PR 377 session note | open |
| Railway cap ($20 proposed; $11 committed) | `dec-railway-budget` | open |
| Publish `starlight-ai-harness` | `HARNESS-STACK.md` | hold until re-exported from merged PR 377 |
| Public history: this PR's first two commits (c8e0db4, 8e30845) contained our own worked example and remain in public history. Rewrite history or change repo visibility? | this PR | open, Frank's call |
| Share the private worked example with anyone | private copy only | open |

## 7. Register boundaries for anything public

- Voice: FrankX Professional for frankx.ai copy (direct, technical, results-first); SIS/ACOS Neutral for protocol and repo docs. No Arcanea terms (Luminor, Gates, Realm, Seeker) in either.
- No income promises, no "passive income" framing, no unmeasured savings figures. Every number cites a file or says "unmeasured".
- Do not call receipts "tamper-proof" unless they are signed with keys we do not hold for the user (PRD section 11). The PRD does not ban the word "compliance"; avoiding it for the audit is this map's own rule.

## Review notes

**Independence.** Round 1 was the drafting agent's own two passes. Round 2 (2026-10-22) was two fresh read-only Claude subagents dispatched by the parent session: a marketing-honesty review and a sourcing/truth review. Both are Claude models reviewing Claude drafts, so neither counts as a cross-family check. A different harness (Codex) still has to sign the exact head SHA.

What the second round found and what changed in this revision:
- Coverage was overstated (Claude Code, OmO, Codex). The inspector now reads JSONC and reports `*_BASE_URL` overrides; TOML and YAML are reported as unreadable. The offer and runbook state OpenCode-only coverage.
- The three questions implied the audit answers them. Rewritten: it shows whether the setup could answer them.
- The runbook claimed an exposed key was rotated; the gate registry says it is still open. The claim is removed (item 10).
- "Fixes" and an hourly walkthrough broke the read-only rule and read as consulting. Removed; a self-audit kit is the product-shaped option.
- The provenance claim ("independent review") was overstated: most findings came from Codex; C1 and C7 came from our registry. Corrected.
- Walkthrough time was unmeasured and C10 applies to nobody outside the estate. Marked unmeasured; C10 moved to an appendix.
- The map said round 14 was queued, but it had returned CHANGES REQUESTED. Updated; the C8 and C13 fixes are marked incomplete.
- Contradiction 6 (focus rule) was understated and 7 (dates) attached them to the wrong product. Both restated with measured values.
- A citation for the ZDR-only key pointed to a gate that does not describe it; fixed. An earlier note said a cap equal to the shared pool was in no repo file; that was wrong (`lab/budget.json` records per-key caps and the shared monthly pool, and they match). This public map no longer quotes the figures.
- **Public exposure.** The runbook's worked example and key history were in a public repo. They are removed from the files; earlier commits remain in public history (Frank's call).
- Added: rotation and plaintext backups (item 10), the template's 6 commits (L4 row), generic findings on our own setup (item 11). Fixed the PRD section reference (section 3, item 2) and the section 11 attribution.

Checks run on this revision: `python lab/build_lab.py --check` and `tests.test_audit_inspect` (results in the PR). The 161 routing tests are the fix agent's report, not re-run here. SIS memory "live" was not verified. The private ACOS premium strategy was not read.
