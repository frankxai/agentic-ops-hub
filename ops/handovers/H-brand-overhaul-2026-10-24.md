---
id: H-brand-overhaul-2026-10-24
what: Brand overhaul: land the four reviewed PRs, QA GenCreator #281, then roll out the brand lint and slop purge
where: prompt below; tracking issue Starlight-Intelligence/starlight-design-intelligence#61
owner: claude
status: open
note: 2 merged (vault #5, agenticincome #81); 5 open in Grok review or draft; Frank decisions listed in the prompt
updated: 2026-10-24
---

## Prompt

Author of the slice: Claude Code (Opus 5.5), 2026-10-23/24. Tracking issue: https://github.com/Starlight-Intelligence/starlight-design-intelligence/issues/61. Session: `ops/sessions/2026-10-24.md`. Board (private): https://claude.ai/artifact/62eD9YfXPUwregaBwgyQsH.

State on 2026-10-24 (re-check with `gh pr view` before acting):

- Merged: Starlight-Intelligence-Systems/starlight-memory-vault#5 (vault sync origin allowlist; Grok sign-off at head `2b839a1`, merge `634f0a4`); frankxai/agenticincome#81 (main build repaired; Grok at head `d2263bd`, merge `a56c3e6`).
- Open: agenticincome#87 offer honesty (Grok re-review after update-branch, head `77f508c`); frankx.ai-vercel-website#1099 purple purge (Grok passed `f274d207`, earlier block being retracted); claude-skills-library#84 brand lint rules (Grok review); starlight-design-intelligence#60 brand foundations (unsigned, Grok review).
- Draft: gencreator.ai#281 Territory B shell (needs 375/768/1440 screenshots; conflicts with Grok's #214); agenticincome#83 removes implementation sprints from the homepage.

Do next, in order, within `AGENTS.md` guardrail 7:

1. Merge #87, #1099, #84 and #60 through `node tools/pr-gate.mjs` only on GATE CLEAR at the signed head. Never self-merge.
2. Screenshot QA for gencreator.ai#281 at 375, 768 and 1440 when free RAM is at least 8 GB (swarm HOLD below that).
3. Brand lint rollout per repo; start with the FrankX upstream NOT_UI exclusion.
4. AgenticIncome and FrankX visual purge PRs: gradient text, grid backgrounds, and in FrankX 31 files with 102 hardcoded purple gradients.
5. Embeddings fallback in starlight-memory.
6. Logo loop test on GenCreator C02.

Waiting on Frank:

- Vault sync resume: the starlight-memory-vault checkout is on `agent/codex/gaming-brand-feedback-20261005` (Codex PR #3, idle draft since 10-05). Glance at the 52 deletions under `starlight-repos/` before the first push, then: `cd C:\Users\frank\starlight\repos\starlight-memory-vault; git switch main; git pull --rebase --autostash; pwsh -NoProfile -File .\sync.ps1`.
- Ladder conflict: TRUTH.md §2 [RULED 2026-10-22] parks everything outside the Kernel ladder, but the 2026-10-23/24 asks covered GenCreator and AgenticIncome. Recommendation: ladder first; parked brands get honesty and slop fixes only.
- gencreator.ai #281 versus #214. Recommendation: #281.
- GenCreator buyer definition: [OPEN].
- Spend: Mobbin (about $10/mo) and OpenArt credits for logo concepts.
- Figma is unauthenticated.

Research findings (2026-10-23): design stack 5/10 (routing ledger 508 rows, 3 verified); memory stack 5/10; Supermemory as a product-backend pilot only; Mobbin only through a clean-room loop (ToS §3/§10.1); Recraft not needed yet (OpenArt Ideogram 4.5 or GPT Image 2.5 plus Codex for concepts, Claude-written SVG with Potrace/vtracer/svgo, then a human redraw); Canva and Figma optional. Brand scores from markup only: Starlight Intelligence 8, AnimeLegends 8, GenCreator 7, Starlight Technology 7, Arcanea 6, RealityArchitect 6, FrankX 5, AgenticIncome 5.

Doctrine drift to fix or route: AGENTS.md §11.3 claims vh-not-dvh and hover-ungated lint rules that do not exist, and understates linter coverage (only AnimeLegends and starlightintelligence.ai lack it); the agentic-ops registry has no entry for claude-skills-library `packs/web-excellence`; AgenticIncome has 7 Dependabot alerts (5 high).
