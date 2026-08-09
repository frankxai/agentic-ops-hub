# C940 Queen 10-hour autonomy mission — 2026-08-09

**Window:** 2026-08-09T04:31+02:00 → 2026-08-09T14:31+02:00 (local host)  
**Host:** DESKTOP-1B4ICID = c940  
**Operator intent:** Continue massive-action estate work for ~10 hours without interactive babysitting.  
**Register:** Neutral  
**Mode:** Queen coordinator + finite continuation ticks. One non-overlapping verified outcome per tick.

## Capacity at start
- Disk free: **55.07 GiB** (≥50 floor PASS; target ≥80 still open)
- RAM available: ~3.2 GiB (tight — avoid parallel heavy CLIs)
- Night Runner allowed only with durable `queue_item_id` + linked worktree + budget
- No force-push, dirty wipe, DNS, Railway resize without explicit gate, Book heartbeat forge

## Intent sources
1. Direct operator: "work the next 10 hours on this" after massive-action summary
2. Prior session receipts: `ops/sessions/2026-08-07-starlight-queen-massive-action.md`
3. Open P0 issues: agentic-ops-hub #35 ClickHouse, #36 stale queues, #37 fail-closed CI, #38 domains
4. Product: R1 GenCreator bridge YELLOW; GenCreator Vercel blocked PRs; dirty trees Packet 6

## Priority order (do in order; skip if blocked)
| ID | Goal | Owner | Done-when | Status |
|---|---|---|---|---|
| M0 | Mission map + capacity freeze + continuation cron | c940 | this file + cron next_run advanced | IN_PROGRESS |
| M1 | Reconcile/repair fleet queues (#36) on clean branch from origin/main | c940 | PR open or merged; July actives → historical | PENDING |
| M2 | Remote PR merge wave: only MERGEABLE + green checks + independent intake | c940 | ≥1 verified merge or explicit no-candidate | PENDING |
| M3 | Stale merged-branch GC across Tier-1 | c940 | count deleted + skipped | PENDING |
| M4 | Packet 6 dirty-tree classification (no wipe) for top clones | c940 | report under fleet/reports/ | PENDING |
| M5 | R1 #419 live recheck; rebase plan or HOLD with exact head | c940 | comment + decision | PENDING |
| M6 | GenCreator #34/#35 Vercel block recheck | c940 | HOLD or path | PENDING |
| M7 | Railway ClickHouse/services read-only evidence refresh (#35) | c940 | issue comment + report line | PENDING |
| M8 | frankx.ai live routes: founder-signal + homepage + gencreator | c940 | HTTP table | PENDING |
| M9 | Push/commit Queen receipts if clean path exists; else leave local | c940 | PR or HOLD | PENDING |
| M10 | Morning/end debrief receipt | c940 | final status fingerprint | PENDING |

## Explicit holds
- Dirty multi-hundred-file prod checkout: no ship from orphan branch
- GenCreator Vercel author/team block: no force merge
- CONFLICTING PRs: HOLD even if checks green
- pnpm store mass delete: not authorized
- danger-full-access Codex: never

## Tick contract (continuation cron)
Each tick MUST:
1. Re-read this mission + measure disk/RAM
2. Compare fingerprint (main SHAs of prod/ops/FrankX/gencreator, open P0 issue states, disk free GiB band)
3. If unchanged vs last receipt → pick orthogonal safe action or stay silent
4. Deliver only material outcomes
5. Append tick receipt to `ops/sessions/2026-08-09-queen-10h-ticks.md`
6. Never recursively schedule more crons

## Fingerprint keys
- disk_free_giB band: RED<35 / YELLOW 35-50 / GREEN 50-80 / TARGET>=80
- origin/main tips: agentic-ops-hub, frankx.ai-vercel-website, FrankX, gencreator.ai
- open issue states #35 #36 #37
- founder-signal HTTP
- last_tick_id

## Safety
- Linked worktree for any mutating git work; refuse primary dirty checkout writers if contested
- One mutating mission at a time
- Admin merge only after green checks + exact-head recheck + intake comment
