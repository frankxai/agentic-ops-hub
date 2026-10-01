# GenInvestor cloud continuation — Codex

Continue with the strongest available frontier coding model. A different provider must review Codex-authored changes. No live-service release or new-code approval is implied.

# Cloud-agent delivery — 2026-10-01

This is a reviewed-and-expanded draft alpha, not a live-service release. Original Claude public heads were independently reviewed; new Codex-authored changes still require a different-provider review.

| Repository | Draft or handover | Feature commit |
|---|---|---|
| GenInvestor | [PR #2](https://github.com/frankxai/GenInvestor/pull/2) | [ebe4452](https://github.com/frankxai/GenInvestor/commit/ebe4452eeb556fa0a6dd048108299760cee77f1f) |
| geninvestor-skills | [PR #2](https://github.com/frankxai/geninvestor-skills/pull/2) | [6eb38e7](https://github.com/frankxai/geninvestor-skills/commit/6eb38e7716b6249b3b48fc359876fd44d209907c) |
| awesome-investor-agent-skills | [PR #9](https://github.com/frankxai/awesome-investor-agent-skills/pull/9) | [3c1e1c3](https://github.com/frankxai/awesome-investor-agent-skills/commit/3c1e1c3e1b0048e2138892eb937a40e83f8654e5) |
| starlight-investor-portal | [PR #41](https://github.com/frankxai/starlight-investor-portal/pull/41) | [ad24097](https://github.com/frankxai/starlight-investor-portal/commit/ad24097be6144940b9eac727deb4b84c967a1f78) |
| agentic-ops-hub | [handover branch](https://github.com/frankxai/agentic-ops-hub/tree/agent/codex/geninvestor-handover) | Docs-only continuation; no added PR because existing queue is above the stated budget |

The first four PRs are stacked onto their original agent branches. Read full ancestry before deciding any owner-authorized merge order. All new commits use the required noreply identity for author and committer; no main update, merge or force push occurred.

## Evidence and inventory

- [Detailed continuation prompt](https://github.com/frankxai/starlight-investor-portal/blob/agent/codex/evidence-foundations/docs/geninvestor/CONTINUATION.md).
- [All 408 accessible repositories and 485-open-PR snapshot](https://github.com/frankxai/starlight-investor-portal/blob/agent/codex/evidence-foundations/docs/geninvestor/REPOSITORY-INVENTORY.md); JSON beside it. Branch inventory covers the five active repositories, not all 408. Four newly created draft PRs postdate that snapshot; refresh it before estate-wide work.
- [Local verification receipts](https://github.com/frankxai/starlight-investor-portal/blob/agent/codex/evidence-foundations/docs/geninvestor/qa/VERIFICATION.md), screenshots, distribution dry-run output and SBOM.
- [LICENSE and integration receipts](https://github.com/frankxai/starlight-investor-portal/blob/agent/codex/evidence-foundations/docs/geninvestor/CLOUD-INTEGRATION-RECEIPTS.md); [read-only Hermes recipe](https://github.com/frankxai/starlight-investor-portal/blob/agent/codex/evidence-foundations/docs/geninvestor/HERMES-CONNECTOR.md).

## Remote verification

[GenInvestor packages CI](https://github.com/frankxai/GenInvestor/actions/runs/36803943062) passed all ten jobs at ebe4452: Node 22.18/24 on Linux/macOS/Windows, Python, policy parity, ownership and dashboard build. [Skills validation](https://github.com/frankxai/geninvestor-skills/actions/runs/36803898921) passed at 6eb38e7. [Catalogue validation](https://github.com/frankxai/awesome-investor-agent-skills/actions/runs/36803367698) passed at 3c1e1c3.

The catalogue [link check](https://github.com/frankxai/awesome-investor-agent-skills/actions/runs/36803367807) initially failed on two existing Shields badge endpoints: a stars timeout and last-commit HTTP 503. All other checks in that report succeeded. The focused failed-job retry passed on attempt two; checks remained enabled and HTTP 503 was not accepted.

The private [packages run](https://github.com/frankxai/starlight-investor-portal/actions/runs/36804244314) passed at ad24097, including the platform matrix, Python, policy parity, ownership and dashboard. This docs-only receipt follows the feature commit; use the commit links above for the exact checked source.

## Remaining gates

Real SEC contact and ownership fixtures; independently checked live price rights/corporate-action basis; genuine distinct-provider model trials and balanced masking evaluations; filled/corrupt/stale dashboard browser states; valid performance trace; standalone package resolution; official MCP SDK conformance; owner-selected skill installation; actual Hermes host test; different-provider code review. No advice, targets, position sizes or probabilities in any output. L2 simulation only. Frank retains merges, contact identity, Actions permissions, counsel/trademark, Vercel ownership and TradingView login.

A workspace-shell outage occurred after the validated source snapshot was captured. The final GitHub commits were assembled from that captured exporter output with true remote parents; no local reconstructed history was pushed.

---

# Frontier cloud-agent continuation

Use the strongest available frontier coding model in your cloud environment. For review of Codex-authored changes, use a different provider; a second OpenAI agent is not a cross-provider reviewer. Do not claim a model switch or review that did not happen.

Start from `frankxai/starlight-investor-portal`, branch `agent/codex/evidence-foundations`. Read `CLOUD-AGENT-BRIEF.md`, this document, `CLOUD-INTEGRATION-RECEIPTS.md`, `SPEC.md`, `strategy.md` and `branding.md`. Preserve concurrent agents' branches and the brief amendment. The user's explicit rules win: **no advice, probabilities, targets or position sizes in any output**. Do not enable the brief's optional probability or personal modes.

## Repositories and branches

| Repository | Continue/review branch | Starting head reviewed |
|---|---|---|
| frankxai/GenInvestor | agent/codex/evidence-foundations | f34ffd54cab7e389b28de449ca3b22128adee6e8, original PR #1 |
| frankxai/geninvestor-skills | agent/codex/review-fixes | 22c53d96b2019ca9a31db2590d6da834f345bc12, original PR #1 |
| frankxai/awesome-investor-agent-skills | agent/codex/review-fixes | 0ed10e2f85179295beab1b3198563932d45ae8d2, original PR #8 |
| frankxai/starlight-investor-portal | agent/codex/evidence-foundations | dccf345a4a8402a3af9516ba03e722171164737a plus preserved 4f8659d48dfaf860918ddde8c860ab934aad9d09 |
| frankxai/agentic-ops-hub | agent/codex/geninvestor-handover | 5aae603e987380546588bb4d732f74faa1b87b11 |

The original three public PRs have independent Codex review comments anchored to their original Claude heads. Fixes are on stacked draft branches. The new code has **not** received a different-provider review. Do not approve it because local tests passed.

`REPOSITORY-INVENTORY.md` lists all 408 accessible repos and the paginated 485-open-PR snapshot. JSON provides machine-readable records and all branches for the five repos above. Other repositories' branches were not enumerated. Re-fetch heads and PR states before editing; the snapshot ages. Ops hub had fourteen open PRs, so no additional PR was opened there. Locate the actual PR-budget file before expanding the estate review queue.

## What was implemented

Evidence source identities include rights and delay metadata; changed citations create a new claim; all stated numbers need supporting values; exponents, leading decimals and magnitude suffixes retain meaning; recompute failures block; inherited prototype fields cannot be cited. Screen counts and ranking scores have audited claim references. CLI/MCP probabilities and raw forecast text are withheld; stored artifacts are re-audited before serving.

The original Python sidecar preserves Form 4 tables/codes/footnotes and 13F holdings/options/classes/amendments, filing-date availability, raw XML and hashes. It refuses implicit 13F units. The optional edgartools retrieval dependency is pinned; **live ownership and real recorded fixtures are not verified**.

Recorded prices carry source/terms/rights, availability, currency and share basis. An owner-defined annual earnings-multiple filter works end to end. Compatibility is an owner assertion; split history and an independently checked automatic free-price connector remain needed.

OpenAI/Anthropic/Google native model transports require explicit model IDs, three distinct providers, audit-before-network, qualitative-only notes, existing claim IDs and a rejecting-verifier stop. Masked/unmasked replay records exist. **Mocked transports are not live trials or evidence of predictive performance.** Model notes stay in local replay records, separate from the displayed deterministic evidence.

The Next.js/shadcn dashboard has dark/light themes, keyboard navigation, a command palette, dense panels and click-through receipts. It blocks invalid contracts, tampered evidence and unsupported lines. It is localhost-only, with no authentication or hosted backend. Screenshots and browser receipts are under `qa/`; Lighthouse accessibility and best practices passed, performance was unavailable because filmstrip screenshots were not collected.

Daily preparation is owner-invoked, re-reads inputs, audits requested sources, optionally calls explicitly enabled models, and stops at human review. Staged artifacts are content-addressed; changed artifacts fail review. There is no activated schedule or outward publication. The owner alone runs the explicit local review command.

Skills validation rejects mixed prohibition/advice clauses; the calibration skill keeps sourced resolutions instead of asking models for numbers. The weekly catalogue workflow uses unique branches, draft PRs, a PR budget and visible failure on Actions permission problems. Metadata is escaped before Markdown rendering. Existing discovery reports remain dated snapshots, not verified absorption licences.

## Next work, in order

1. **Independent review first.** Review the four new draft diffs as a skeptical buyer. Exercise rights downgrades, every output surface, inherited fields, source-ID compatibility, unsupported semantic paraphrases, damaged SQLite and staged review identity. Reproduce findings with focused tests, fix them, and rerun the planted-error corpus. Never self-approve.
2. **Real SEC trials.** Use only the owner's real SEC identity if already configured. Record genuine Form 4 and 13F cover/information-table responses privately. Verify accession/document retrieval against pinned edgartools, both amendment kinds, missing values, multiple information tables, explicit reporting units and exact filing availability. No contact invention, proxy-evasion or uncontrolled retries.
3. **Prices.** Select a free connector only after checking its actual data terms, display/reuse rights and corporate-action basis. Add an immutable response fixture and historical availability test. Never mark vendor data public merely because its endpoint is reachable.
4. **Live models.** Select explicit current frontier model IDs supported by the owner's keys. Analyst, skeptic and verifier must use different providers. Run repeated, order-balanced masked/unmasked trials and planted unsupported claims under a written request/token budget. Keep credentials, headers and private payloads out of replay logs. Report failure cases and semantic re-identification limits; never convert comparisons into forecasts or probabilities.
5. **Dashboard quality.** Test candidate-filled and evidence-drawer states in-browser with clearly labelled fixtures, plus corrupted/restricted/stale/zero-result states, keyboard focus, light/mobile contrast and clean-clone builds. Replace generic annual freshness with source cadence. Obtain a valid performance trace before making speed claims. Keep every displayed figure linked to an audited claim.
6. **Distribution.** Fix independent npm package resolution of sibling contracts, include required licences and test tarballs in a clean temp install. Packages remain private: dry run is not publish. Validate against the official MCP SDK; add only evidence-bound read tools. Draft-branch discovery was verified with an explicit clone and CLI --list; tree URLs with slash-containing branches failed. Keep the documented clone path and verify a clean owner-selected installation next. Run the weekly digest without auto-merging it. Audit the SBOM before adding dependencies.
7. **Broader depth.** Evaluate Python-engine evidence ingestion, deflated Sharpe/decay and source-specific connector health behind existing interfaces. Use the pinned licence sweep to choose narrowly scoped reuse. OpenBB's checked current licence differs from its older AGPL history; do not copy older code. Hermes has a private read-only MCP recipe awaiting a real host test.

## Commands and release gates

```sh
npm test
npx --yes --package node@22.18.0 node --disable-warning=ExperimentalWarning --test 'packages/*/test/*.test.ts'
python3 -m unittest discover -s packages/edgar-sidecar/test -v
uv run --directory engine --extra dev ruff check src tests
uv run --directory engine --extra dev pytest -q
node --test tools/export-public.test.mjs
npm ci --ignore-scripts --prefix apps/dashboard
npm run typecheck --prefix apps/dashboard
NEXT_TELEMETRY_DISABLED=1 npm run build --prefix apps/dashboard
node tools/export-public.mjs /empty/product-export
node tools/export-public.mjs /empty/skills-export --profile skills --source-root /checkout/geninvestor-skills
node tools/export-public.mjs /empty/catalogue-export --profile catalogue --source-root /checkout/awesome-investor-agent-skills
```

Keep the core dependency-free and Node type-stripping compatible. Read LICENSE before absorbing code, preserve notices, never copy AGPL/source-available code. Publish product and companion changes only from the export profiles. Use the prescribed noreply identity for public author and committer. Verify it after committing. Draft PRs only; no merge, main push or force push. Recheck the CI matrix remotely; local Linux checks do not establish macOS/Windows CI status.

Frank owns merges, SEC contact identity, awesome-repo Actions permissions, counsel/trademark decisions, Vercel ownership and TradingView login. Do not change those, activate a hosted service or publish npm packages. Complete authorized reversible work without permission loops, and end with exact commits, draft links, validation and concrete remaining blockers.


This hub branch changes only this handover document. No shared configuration, agent rules, automation or hub CI was changed.
