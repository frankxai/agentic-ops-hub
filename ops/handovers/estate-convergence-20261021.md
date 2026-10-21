---
id: estate-convergence-20261021
what: Drain in the plan's order once Frank sets the Actions budget (cost cuts and draft-CI, security, then spine PRs from starlightintelligence.ai#180 and starlightintelligence.ai#175); until then, prepare those two
where: prompt below
owner: claude
status: open
note: decisions ruled 21 Oct (delegated); wave 1 closed; starlightintelligence.ai#180 needs a non-Claude pr-gate check at its head
evidence: https://github.com/frankxai/starlightintelligence.ai/pull/180
updated: 2026-10-21
---

## Prompt

Read `ops/plans/estate-convergence-2026-10-21.md` and `ops/sessions/2026-10-21.md` first. The five decisions were ruled on 21
October; the last table of the plan says what is done and what waits on Frank's own accounts.

1. Merges follow the plan's drain order only. Before any budget or runner returns: Frank lowers `ESTATE_AUTONOMY`
   everywhere estate-pr-guardian is installed, then you disable every auto-merge it already armed and record the list in
   this ledger. Once Frank sets the Actions budget: cost cuts and the draft-CI rule, then
   security PRs (the plan names the private document that lists them), then spine PRs, then Dependabot minor/patch in the
   spine repositories not on hold, then the approved close sweep. Record every close and merge in this ledger the same day.
2. Until then, prepare the first spine PRs so they are ready at step 3, without merging them:
   - starlightintelligence.ai#180 (head `27f6fb1` or later) needs a non-Claude pr-gate check on the exact head and a Vercel
     READY preview for that head; CI runs once runners exist. It merges only through pr-gate, by a non-Claude harness or
     Frank.
   - The rail is Polar, so starlightintelligence.ai#175 needs offers that may grant `starlight.factory`, refund revoking
     the entitlement, a dispute rule, one sandbox purchase-to-run receipt and Polar's approval of the offering before
     `STARLIGHT_COMMERCE_ENABLED` is set anywhere. Codex cannot edit that branch until Frank creates a Codex cloud environment for starlightintelligence.ai.
3. Do not open PRs outside the spine table until 20 November. The only writes outside it are the drain owner's, as the
   focus rule in `AGENTS.md` lists them; anything else needs Frank to revise that ruling first.
