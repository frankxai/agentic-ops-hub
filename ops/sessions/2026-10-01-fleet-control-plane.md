# 2026-10-01: fleet control plane handover (Claude, YogaBook)

Session `763985e0` ran from 09-14 to 10-01. Re-measure anything older than a few days before you act on it.

## Intent

Frank wants one control plane for every agent (Claude, Codex, Hermes, Grok, Antigravity) across the YogaBook, C940 and cloud. Agents do the work themselves. Anything that lands is verified by a different harness. Production stays green. Every prompt and image prompt goes into the second brain. Branches get landed or closed with evidence, not left stranded. A manual step handed to Frank is a defect unless it is a real human gate.

## What is live

| Thing | Where | State |
|---|---|---|
| Shared completion verifier and chained dispatch | [agentic-ops](https://github.com/frankxai/agentic-ops) `main` squash `f278176` ([PR 69](https://github.com/frankxai/agentic-ops/pull/69)) | Live on the queue through release `~/.starlight/queen-verify/f5e8ffa…` (`current.txt`) |
| Patched dispatcher | `starlight/tools/Invoke-StarlightQueenLoop.ps1`; source `agentic-ops/lifecycle/wire/` | Live. Task `StarlightQueenLoop` runs every 5 min. Backup `.before-queen-verify` |
| Verified-work archive | agentic-ops branch `queen/receipts` | 5 records |
| Chains | `starlight/queen/chains/*.plan.json` | `first-light-0926` (2 tasks, in #69); `sweep2-academy-0926` produced [ai-architect-academy#37](https://github.com/frankxai/ai-architect-academy/pull/37), merged |
| Watchdogs | tool plane and gbrain HTTP probes | Live; the fleet board shows both as `ok` |
| Fleet board | `node agentic-ops/lifecycle/fleet-view.js` → `~/.starlight/fleet/fleet.html` | Sessions, collisions, machines, goals, chains, watchdogs |
| akamoto.io | Vercel project `akamoto` | Back online |

## Landed this slice

- agentic-ops [#69](https://github.com/frankxai/agentic-ops/pull/69) (verifier, chains, wiring), [#79](https://github.com/frankxai/agentic-ops/pull/79)
- [ai-architect-academy#37](https://github.com/frankxai/ai-architect-academy/pull/37): diagram workflow, built by the queue
- [starlight-you#9](https://github.com/frankxai/starlight-you/pull/9): dead links
- [go-agenticincome#23](https://github.com/frankxai/go-agenticincome/pull/23): drift CI
- [frankx.ai-vercel-website#763](https://github.com/frankxai/frankx.ai-vercel-website/pull/763): licence evidence pinned to an immutable commit. Grok and Codex both signed off on `665b178`.

## Still open from this slice

- **[agentic-ops-hub#72](https://github.com/frankxai/agentic-ops-hub/pull/72)** (integer bus priorities). Codex failed the first head: the branch was stale and would have reactivated `BOOK-HEARTBEAT-20260825`. Fix: merged `origin/main` in as `6413f30` (no force push). The diff is now only the 4 priority lines. CI `verify` passes. The 2 `test_topology_health` failures also happen on `main`. Next: a Codex re-review on `6413f30`, then `pr-gate.mjs signoff` and `merge`.
- **[agentic-ops#81](https://github.com/frankxai/agentic-ops/pull/81)** (Claude review scope). Codex FAIL findings are posted on the PR. Fix them or close the PR.
- **[arcanea-ai-app#466](https://github.com/frankxai/arcanea-ai-app/pull/466)** (waitlist and real 404s). Draft with conflicts. Rebase it onto `main` after #458's migration. Signups return an honest 503 until Upstash is set up.
- **`agent/claude/queen-chain`** has one commit not on main, the `sweep2-academy-0926` plan. Grok has since taken over that worktree as `agent/grok/resume-identity` and carries the same commit. Leave it with Grok.
- **Estate root** branch `agent/claude/watchdog-http-probe`: `tools/Deploy-Watchdogs.ps1` is uncommitted. This repo cannot be pushed until Frank rules on it.

## Estate review load (measured 2026-10-01)

About 100 open PRs across about 60 `frankxai` repos. Most are 09-29/09-30 audit drafts from several harnesses. Heaviest: agentic-ops (9 drafts, 121–131), claude-code-config (7), gencreator.ai (8), frankx.ai-vercel-website (3: #829, #831, #837), Starlight-Intelligence-System (4). Get the full list with:

```
gh search prs --author @me --state open --owner frankxai --limit 200 --json repository,number,isDraft,title,url
```

## Human gates (Frank only)

1. Can the estate repo `starlight` be pushed? That unblocks 5 branches and the watchdog deploy script.
2. Arcanea signups: Upstash for Redis plus `WAITLIST_TOKEN_SECRET` on Vercel `arcanea-ai-app`.
3. `arcanea-orchestrator`: unarchive it or drop the fix.
4. Say "close stale" for the 6 stale agentic-ops PRs.
5. Revoke the gbrain token that was pasted into chat: `gbrain auth revoke "ledger-ingest"`.
6. gbrain MCP: config says `localhost:7318`, the server answers on `127.0.0.1:7318`. Pick one.
7. Hermes split brain (old gateway pair) and about 32 GB of `state.db` backups. Agents never kill Hermes processes.

## The bar for the next agent

- Plan and verify; the queue executes. First commit a planner-owned `*.acceptance.js` and pin it with `git diff --quiet <sha> HEAD -- <file> && node --test <file>`. Prove it fails today and passes against a throwaway reference fix. Then drop the chain plan in `starlight/queen/chains/`.
- Never trust a report, including your own. Re-derive from primary evidence before building.
- Test the production path. For every default, test the case where no config file exists.
- Maker ≠ checker. Codex review loops until it passes, and `starlight/tools/pr-gate.mjs` binds the sign-off to the head SHA. Never self-merge, never force-push.
- Run `pp preflight` before heavy work. The queue holds below 4 GB free RAM. C: is in CRITICAL storage mode, so no new worktrees for bulk installs.

Full file list and history: `~/.starlight/fleet/handovers/fleet-control-plane-handover-2026-09-26.md` (local to the YogaBook).
