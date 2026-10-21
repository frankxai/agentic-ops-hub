# Receipt schema decision: SIS run-receipt v1 is the envelope

Decided by Frank on 2026-10-21 ("yes SIS run-receipt v1 as the envelope"). Author of this record: Claude Code. Code: `lab/receipt_bridge.py`, tests: `tests/test_receipt_bridge.py`, vendored schema: `lab/vendor/run-receipt.v1.schema.json` (SIS commit `f64efa8c`, sha256 `7bfe79ef…87ca`).

## What the decision changes

Before: three receipt formats (Routing Brain `routing.jsonl`, SIS run-receipt v1, Queen's signed per-dispatch receipt). After: **one signed unit of proof, SIS run-receipt v1** (DSSE v1 envelope around an in-toto Statement v1, Ed25519). Routing Brain's `routing.jsonl` stays as the raw, call-level source that receipts are built from; it stops being a competing format.

## A correction to my earlier recommendation

I proposed "SIS v1 as envelope plus our fields as an extension". Reading the schema shows **v1 has no extension point**: `additionalProperties: false` at the top level, on `run`, on every stage and on `totals`. Our fields cannot be added to v1 without changing the protocol, and the SIS docs say the schema is substrate tier and lands through the Board's process. So v1 is used as it is, and routing detail travels in the three places v1 allows (below). A v1.1 `extensions` block is a proposal for SIS, not something this repo does.

## Mapping

One receipt is one **run**: the routing calls made for one task attempt, then the checker.

| Routing Brain / lab field | v1 field | Notes |
|---|---|---|
| call `used`, `provider`, `latency_ms`, tokens | `stages[].model`, `provider`, `latencyMs`, `inputTokens`, `outputTokens` | One stage per call, in order |
| call `success` | `stages[].status` ok or failed | A failed fallback call stays visible |
| `cost_usd` | `stages[].costEur` and `note` | v1 prices in EUR only. The bridge converts with an explicit `fx_eur_per_usd` and keeps the USD figure and the rate in the note. No default rate: a missing rate is an error |
| `task_class`, `primary`, `fallback_used`, `zdr_override`, call id | `stages[].note` (`class=…;primary=…;fallback=…;zdr_override=…;usd=…;fx=…;call=…`) | Signed with the envelope; not machine-typed |
| checker run | extra stage `verify:<checker>` | status ok or failed |
| harness id | `run.host` | `opencode-bare`, `now`, `oms`, `claude-code`, … |
| task attempt, pack and task | `run.id`, `run.kind` (`lab.<pack>.<task>`), `run.correlationId` (`EXP-008:<task>` or `M-…`) | Mission id from PR 351 fits `correlationId` |
| routing policy choice | `decisions[gate=route]` decidedBy `policy` | |
| ZDR held or overridden | `decisions[gate=zdr]` approved or rejected | An override is a recorded rejection |
| who accepted the work | `decisions[gate=accept]` decidedBy `agent` or `human` | Human needs `approvalRef`; agents need nothing extra |
| produced artifact (diff, page, article) | `subject` name and sha256 | The signature binds this digest |
| raw routing records, checker output, routing schema | `evidence[]` with sha256 | Hash-bound references to files |
| pass, partial, fail | `verdict` | See next section |

## Acceptance is not the verdict

v1 refuses `PASS` when any stage failed. A task that passed its tests after a 403 fallback therefore has verdict `PARTIAL`. So the lab defines **accepted** separately: a different actor approved it (`decisions[gate=accept]`), the checker stage is ok, and the accepting actor is not the harness that made the work. `accepted()` and `separation_problems()` in the bridge implement that. Reports use accepted, not verdict. If this turns out to confuse readers, that is a case to raise with SIS for v1.1.

## What v1 verifies and what it does not

The SIS verifier checks: signature and key id, time ordering, totals not below stage sums (EUR, allowing rounding), human decisions carrying proof, `PASS` rules, evidence hashes present. It does **not** check: maker differs from checker, ZDR compliance, that the cost is the real provider charge, or that the checker output is genuine. Those are policy checks layered on top (`separation_problems()` today; the `receipt-verifier` gate adds the rest). A signature proves who attested, not that the contents are true (SIS receipts doc, "The rule").

## Verified now

- Receipts built by the bridge validate against the vendored v1 JSON schema (`jsonschema`, in CI).
- SIS's own `receiptProblems()` accepts a bridge receipt (runs locally when the SIS checkout exists, skipped in CI).
- A test fails if the vendored schema differs from the SIS copy.
- 16 bridge tests pass. Signing and verification with a real key are not exercised yet.

## Open items (gates in `lab/gates.json`)

1. `receipt-fields`: the routing record has no harness, experiment, task id or token counts, so the bridge cannot fill them from `routing.jsonl` yet. This lands after PR 377 merges (the PR 377 branch must not change under review).
2. `receipt-verifier`: a standalone `verify` command with planted-fault fixtures. No public verifier reads the run-receipt predicate today, and the SIS site's `/verify` page does not read run receipts.
3. Signing key custody for external users: R0 users run on their own machine with their own key (`sip-signing.key`, gitignored). Hosted signing is a later decision.
4. FX source and cadence: who sets `fx_eur_per_usd`, and where the rate is recorded for audit. Until decided, callers pass it explicitly.
5. Queen's per-dispatch receipt is the same predicate type, so it converges here; the Queen router decision is separate (`dec` item 2 in the product plan).
6. Proposal to SIS (not done): v1.1 with an optional `extensions` object and a `cost` block that carries currency, so routing fields stop living in a note.
