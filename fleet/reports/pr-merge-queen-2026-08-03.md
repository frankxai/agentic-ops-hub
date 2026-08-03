# PR Merge Queen Matrix — 2026-08-03

**Rule:** NOW/NEXT/HOLD/CLOSE-REVIEW · no bulk merge · independent acceptance required

## frankx.ai-vercel-website
- Open listed: 32 · non-draft: 2

| PR | Class | Why |
|---|---|---|
| [#408](https://github.com/frankxai/frankx.ai-vercel-website/pull/408) feat: launch the Human Proof Studio | **HOLD** | mergeable=CONFLICTING; review=REVIEW_REQUIRED; files=57 |
| [#400](https://github.com/frankxai/frankx.ai-vercel-website/pull/400) Restore the source-led MVU Tallinn field atlas | **HOLD** | mergeable=CONFLICTING; review=REVIEW_REQUIRED; files=46 |

### Drafts
- 30 drafts remain unpromoted (HOLD by default).

## FrankX (authoring)
- Open listed: 32 · non-draft: 8

| PR | Class | Why |
|---|---|---|
| [#107](https://github.com/frankxai/FrankX/pull/107) Unbreak CI, resolve the puppeteer peer conflict, drop the un | **NEXT** | mergeable=MERGEABLE; review=REVIEW_REQUIRED; files=8 |
| [#101](https://github.com/frankxai/FrankX/pull/101) rescue(meta-os): recover 6 unpushed Meta ecosystem OS commit | **HOLD** | mergeable=MERGEABLE; review=REVIEW_REQUIRED; files=16 |
| [#99](https://github.com/frankxai/FrankX/pull/99) feat(crm): activate MVU network intelligence | **NEXT** | mergeable=MERGEABLE; review=REVIEW_REQUIRED; files=18 |
| [#90](https://github.com/frankxai/FrankX/pull/90) Consolidated Main Sweep: Merged 6 Parallel Agent Branches | **HOLD** | mergeable=MERGEABLE; review=REVIEW_REQUIRED; files=2417 |
| [#83](https://github.com/frankxai/FrankX/pull/83) Rebuild model-arena as a multi-provider frontier arena + add | **NEXT** | mergeable=MERGEABLE; review=REVIEW_REQUIRED; files=17 |
| [#57](https://github.com/frankxai/FrankX/pull/57) [WIP] Identify best affiliate programs for AI resources | **HOLD** | mergeable=CONFLICTING; review=CHANGES_REQUESTED; files=9 |
| [#56](https://github.com/frankxai/FrankX/pull/56) feat(resources): add Affiliate Tools and GitHub Repos sectio | **HOLD** | mergeable=CONFLICTING; review=REVIEW_REQUIRED; files=3 |
| [#54](https://github.com/frankxai/FrankX/pull/54) docs(metrics): add Metrics Truth Rule + living ledger seed | **HOLD** | mergeable=CONFLICTING; review=REVIEW_REQUIRED; files=45 |

## Merge-eligible now?
- **Production:** none — both non-drafts are CONFLICTING + REVIEW_REQUIRED.
- **FrankX:** none without fresh human/independent approval; #107 is MERGEABLE but review-required and deletes a large lockfile surface (needs careful acceptance).
- #90 (2417 files) = HOLD mega-diff.

## Immediate production path
1. Clean worktree from origin/main for any prod fix (R1 CTA).
2. Rebase or recreate #408/#400 only if still desired after main diff.
3. Do not merge from dirty local content-integrity-gate checkout.
