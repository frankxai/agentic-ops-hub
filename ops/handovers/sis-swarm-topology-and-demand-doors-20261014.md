---
id: sis-swarm-topology-and-demand-doors-20261014
what: Starlight: Independent review, merge of PR #406 / #407, and Demand Reporting Run
where: prompt below
owner: unknown
status: open-unverified
note: held to 20 Nov by the focus window (AGENTS.md guardrail 7): steps outside the spine, or features in a hold repository, wait; not reconciled since the split
updated: 2026-10-21
---

## Prompt

Moved verbatim from `ops/NEXT-PROMPTS.md` lines 205-209 on 2026-10-17 (marker `sis-swarm-topology-and-demand-doors-20261014`).


Continue from Starlight PR #406 (Queen Terminal Agent Lifecycle, issue #398) and PR #407 (Hardened Executive Tier cards, 151 agents, and Swarm & Cloud Topology Blueprint, issue #408). Demand doors #2 (KV alias), #5 (sender auth), and #6 (Akamoto surface) are resolved, reducing queue blockers to 21. Run independent review via allowlisted GitHub Apps per `tools/merge-review/merge_review_gate.py` (`STARLIGHT-INDEPENDENT-REVIEW-V1`). Once signed receipts pass, promote PRs from draft and execute sequential fast-forward merge into main. Supply local Upstash credentials in `.env.local` to run `node packages/demand-capture/report.mjs` for live estate demand reporting.
