# Strategy map: where each document lives and how the audit offer fits (draft, 2026-10-22)

Author: Claude Code. Status: draft for Frank and a different-harness review. This map points to documents; it does not restate or change them. Where documents disagree it says so (section 5). Nothing here is a decision.

## 1. The one line, and where it comes from

"Sovereign delegation, proven by receipts." Source: `lab/goals.json` (`north_star`), which cites the Starlight strategy of 2026-09-18 (Claude Docs artifact `BWdNqCEutFNvSS9HEUzhWH`; memory note `project_starlight_strategy_2026-09-18`). The audit offer, the routing brain, the verifier and the lab all serve it. Nothing in this map should contradict it.

## 2. Layers (what we build) and who owns each document

| Layer | What it is | State on 2026-10-22 | Owning document | Repo / PR |
|---|---|---|---|---|
| L0 commodities | OpenCode, OmO, gateway, models, Claude, Codex | Rented | `fleet/HARNESS-STACK.md` (exists only on the unmerged branch `agent/c940/massive-action-receipts-20260803`, see section 5 item 9) | n/a |
| L1 memory | SIS memory and MCP bridge | Live | SIS repo docs | Starlight-Intelligence-System |
| L2 routing brain (the moat per `HARNESS-STACK.md`) | Classes, ZDR chains, reserve/settle, strict OpenCode launcher | **Open draft**, 13 Codex rounds, none approved yet; round 14 queued | `fleet/ROUTING-BRAIN.md`, `ops/sessions/2026-10-21-routing-brain-hardening.md` | agentic-ops-hub PR 377 |
| Receipt standard | SIS run-receipt v1 (DSSE, in-toto, Ed25519) | Decided 2026-10-21 | `2026-10-21-receipt-schema-decision.md`; SIS `docs/receipts.md` | SIS |
| Verifier | `starlight verify-receipt` | **Open draft**, 5 Codex passes, last APPROVE WITH NOTES then a P3 fix | SIS `docs/receipts.md` "Verifying a receipt" | SIS PR 481 |
| Lab | Registry, validator, dashboard, receipt bridge, EXP-001 to 009 | **Open draft**; no experiment has run | `lab/README.md`, `2026-10-21-research-lab-and-cloud-workers.md`, `2026-10-21-harness-measurement-and-scale.md` | agentic-ops-hub PR 379 |
| L3 OmS | Config, governance and receipts pack on upstream tools; not a fork | Generator exists; profiles not split | `lab/goals.json` pillar `ecosystem`; `HARNESS-STACK.md` | agentic-ops |
| L4 template | `starlight-ai-harness` public template | Local repo only, **no remote**; the copy on disk was exported before PR 377 and carries the old classifier | `HARNESS-STACK.md` phase 3 | local |
| Product plan | Starlight Receipts PRD, ARD, funnel, tiers | Proposal | `2026-10-21-product-prd-ard-funnel.md` | PR 379 |
| **Audit offer (new)** | Paid or free read-only review of a prospect's agent setup | Draft, no demand evidence | `2026-10-22-audit-offer.md`, `2026-10-22-audit-runbook.md` | this branch |
| Paid layers beyond the audit | Hosted ledger, managed gateway, signing, dashboard | Only Open/Pro/Team/Workers tiers exist in the PRD (section 6.3). **Managed gateway, hosted signing and the audit are not in the PRD.** | none yet | n/a |

## 3. Streams (what Frank runs) and how each touches the audit

| Stream | Role relative to the audit | Boundary or rule that applies | Source |
|---|---|---|---|
| Agentic Income Trinity (agenticincome.ai, agenticpassiveincome.com, dpi) | Not the audit's audience. Trinity sells income education and packs, and its copy rules forbid income promises. At most a cross-link. | Zero income promises; dpi CANON inviolable; Polar is merchant of record | memory `project_agentic_income_trinity` |
| Affiliate Ops Agent | Best internal subject: an agent acting on external accounts, with human-only steps (consent, tax, credentials, 2FA). Its receipts could become a case study after the 30 to 60 day dogfood window that began 2026-09-28. | Relationship state and pricing are private; the case study needs Frank's consent | memory `project_affiliate_ops_agent` |
| GenCreator / ACOS | Later: packs for creators could ship with receipts. Not part of the audit. The premium strategy is private and was **not read** for this map. | Core stays free; premium strategy never goes in a public repo | memory `project_acos_v12` |
| Arcanea | Not involved. Its gateway keys appear in `lab/budget.json` (caps of $25), so they fall under any internal audit of the estate. | Arcanea Mythic register must not leak into this work | `REGISTER-BOUNDARIES.md` |
| FrankX | Candidate front door and professional register. Analytics was missing for months until a fix (frankx.ai#1068), so a funnel there needs instrumenting first. | FrankX Professional voice; no Arcanea terms | PRD section 6.2; `REGISTER-BOUNDARIES.md` |
| Investor OS | Not involved. Same principle (agents never execute trades), no data shared. No positions in any audit artefact. | Agents never execute trades or move money | memory `project_investor_os` |
| SIS / SIP | Owns the standard and verifier. The strategy's H1 goal (to 2026-10-31) is "first-ten external signers"; whether audits could produce any is a hypothesis, not a plan. | SIS/ACOS Neutral register | memory `project_starlight_strategy_2026-09-18` |

## 4. What depends on what merging

| Needs | Because | Until then |
|---|---|---|
| PR 377 merged | Audit claims "we fixed these classes" and cites its launcher and settle API | Say "in review" |
| SIS PR 481 merged | Check C10 uses `starlight verify-receipt` | Skip C10 or run from the PR branch |
| PR 379 merged | This branch is stacked on it (the plan documents it reads live there) | Merge order: 379 before this branch |
| Re-export of `starlight-ai-harness` from the merged router | The on-disk template has the old classifier | Do not publish the template (Frank's button) |
| Frank creates a ZDR-restricted gateway key | C7 recommends it; our own setup does not have one yet (`lab/gates.json` `dec-token-pass-key`) | Do not claim our own setup passes C7 |
| EXP-008 run | Any cost or quality claim about OmS | No such claim in the offer |

## 5. Contradictions and stale statements found (not smoothed over)

1. **Verifier scope.** The product plan requires a `verify` command that recomputes spend and "checks that maker differs from checker" (F3, F4). The verifier in SIS PR 481 explicitly does not check maker against checker, does not check real provider cost, and only checks that `totals.costEur` is not below the stage sum (`docs/receipts.md`). F4 is therefore unmet by 481; the plan or the verifier needs to change. Also the plan's first-run commands (`starlight init`, `run`, `verify`) are not what exists (`starlight verify-receipt`).
2. **BYO key versus a managed gateway.** ADR A9: "BYO key for any external user; we never hold their provider keys in R0". A managed gateway or hosted signing would hold keys. Not in the PRD; it needs its own decision and a data-handling answer.
3. **What "Pro: Token Pass profile" means.** Token Pass is one shared $80 monthly credit on the `starlight-intelligence` team (`lab/budget.json`). The plan does not say whether a paying user brings their own Token Pass or uses ours. Selling access to our pool would be reselling tokens, which A9 rejects.
4. **Stale PR status.** The product plan (section 2) says Codex rounds 1 and 2 on PR 377; `lab/gates.json` item `pr-377` says "round 1"; the measurement plan says 4 rounds and 65 to 71 tests and a classifier decision "in progress". Current state: 13 rounds, 161 routing tests at `c2dd301` as reported by the fix agent, Option A done. These documents are history, not current state.
5. **Neutral register and pricing.** `REGISTER-BOUNDARIES.md` forbids "product pricing" and brand CTAs in SIS/ACOS Neutral repos (`agentic-ops` is listed there), yet the product plan (section 6.3) carries tier price hypotheses in `agentic-ops`. Public copy needs a home in FrankX Professional register; the plan documents are internal drafts.
6. **Focus rule.** Until 2026-11-20 only a nine-repo spine gets features (PR 378). The plan says which repo hosts `fleet/` is UNVERIFIED. The audit is a service plus documents, not a feature, but the helper script `scripts/audit_inspect.py` is a feature in whichever repo holds it. Confirm the host repo before merging this branch.
7. **Dates.** First sale by 4 Nov and a customer-validated launch by 20 Nov (plan section 2) sit beside "no demand evidence" and an unpublished template. They can only both hold if the audit or an edition sells first. Flagged, not resolved.
8. **Two routers.** Queen's model routing (starlight-swarm#39) overlaps the Routing Brain. The plan recommends Routing Brain owns policy and Queen consumes it. Still Frank's decision.
9. **A source document that is not on main.** `fleet/HARNESS-STACK.md` defines the layer names (L0 to L4) and is cited by the measurement plan, `lab/harnesses.json`, EXP-008 and this map, but it is tracked only on `agent/c940/massive-action-receipts-20260803` (42 commits ahead of main, fast-forward blocked by a dirty ledger file, per the restart card). Until that branch is merged, the layer model is not on main.

## 6. Decisions left for Frank

| Decision | Owner document | State |
|---|---|---|
| Price, rail (Polar or invoice), and channel for the audit | audit offer | open |
| Open-core boundary, licence, trademark ("Starlight Receipts") | PRD section 7; `lab/gates.json` `dec-open-core` | open |
| Single router: Routing Brain or Queen | PRD section 3.2 | open |
| Managed gateway and hosted signing: do we hold keys; GDPR and key custody | none | open, new |
| ZDR strictness (strict or allow free) | `lab/gates.json` `dec-zdr-strictness` | open; code is strict by default |
| Create a ZDR-restricted gateway key and lower the lab key's cap | `dec-token-pass-key` | open |
| Railway cap ($20 proposed; $11 committed) | `dec-railway-budget` | open |
| Publish `starlight-ai-harness` | `HARNESS-STACK.md` | hold until re-exported from merged PR 377 |
| Who sees the internal worked example in the runbook | runbook section 7 | open |

## 7. Register boundaries for anything public

- Voice: FrankX Professional for frankx.ai copy (direct, technical, results-first); SIS/ACOS Neutral for protocol and repo docs. No Arcanea terms (Luminor, Gates, Realm, Seeker) in either.
- No income promises, no "passive income" framing, no unmeasured savings figures. Every number cites a file or says "unmeasured".
- Do not call receipts "tamper-proof" or the audit "compliance" (PRD section 11).

## Review notes

**Caveat on independence.** The two reviews below were written by the same agent that drafted the documents, in two separate passes with different questions (a marketing-honesty lens and a sourcing lens). They were not run by fresh subagents, because the drafting agent was a fork and may not spawn agents. Treat them as self-review. A different harness still has to sign this branch.

Marketing-honesty pass on the offer (would a stranger understand it; does it promise only what we can show; is demand evidence missing):
- Jargon: "gateway" and "ZDR" were undefined. Fixed: both now explained in plain words.
- "We run the same audit on our own setup first" overstated it: only C1 to C3 were run, by a script on one config. Fixed: the offer now says exactly that.
- "13 Codex review rounds" reads as tool trivia to a stranger. Fixed: "independent review rounds".
- Missing: who does the work, and why pay if the checklist could be free. Added a "Who does the work" section and a decision for Frank.
- Demand evidence: none exists. The offer says so; no change possible without conversations.

Sourcing pass on all three documents (is every claim sourced; contradictions with existing registries; is the map true):
- All cited files, gates and section numbers were checked against the branch. `fleet/HARNESS-STACK.md` is not on this branch: it is tracked only on `agent/c940/massive-action-receipts-20260803`. Added as contradiction 9 and the map's L0 row now says so.
- A reference to `lab/goals.json` as a user of the layer names was wrong (they appear in `lab/harnesses.json` and EXP-008). Fixed.
- The "$80 cap equal to the pool" observation is not in any repo file; the runbook says so.
- Figures: no price or saving appears. Counts used (13 and 5 review rounds, $25 and $80 caps, 9 experiments, 15 gates) each trace to a file or session note cited in the text. The 161 routing tests are the fix agent's report, not re-run here.
- Checks run on this branch: `python lab/build_lab.py --check` (ok, 9 experiments, 15 gates); `tests.test_lab_registry`, `tests.test_receipt_bridge` and `tests.test_audit_inspect` (77 tests, all pass).
