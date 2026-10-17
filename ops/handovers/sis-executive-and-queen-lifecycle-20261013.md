---
id: sis-executive-and-queen-lifecycle-20261013
what: Starlight: Independent review and sequential merge of PR #406 and PR #407
where: prompt below
owner: unknown
status: open-unverified
note: not reconciled since the split
updated: 2026-10-13
---

## Prompt

Moved verbatim from `ops/NEXT-PROMPTS.md` lines 211-215 on 2026-10-17 (marker `sis-executive-and-queen-lifecycle-20261013`).


Continue from Starlight PR #406 (Queen Terminal Agent Lifecycle, issue #398) and PR #407 (Hardened Executive Tier cards, 151 agents, issue #408). Both draft PRs are cleanly branched from origin/main with 100% green test passes across substrate (142/142), operational (73/73), Track D evals (34/34), and lifecycle unit tests (11/11). Run independent review via allowlisted GitHub Apps per `tools/merge-review/merge_review_gate.py` (`STARLIGHT-INDEPENDENT-REVIEW-V1`). Once signed receipts pass, promote PRs from draft and execute sequential fast-forward merge into main. Verify post-merge receiving main CI and rebuild dist/ artifacts.
