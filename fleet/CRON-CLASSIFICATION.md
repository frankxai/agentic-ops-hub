# Cron Classification — C940 Fleet (2026-08-29)

**SoT:** `fleet/cron-classification.json` (machine-readable) + this file.
**Live source:** `hermes cron list` on `DESKTOP-1B4ICID`.
**Purpose:** close FLEET-OPS Foundation #2 ("classify every job before it exists") — the prior estate was 17 active crons with **no class recorded**. Now every job is classed; gaps listed below.

## Class distribution (active = 17, paused = 0)
| Class | Count | Rule |
| --- | ---: | --- |
| `watchdog` | 12 | script-only, `no-agent`, silent when healthy, never mutates LLM state |
| `specialist` | 4 | one domain, one outcome (SIS memory, Railway audit) |
| `queen` | 1 | the single permitted cross-domain LLM lane — read-only by default |
| `oneshot` / `retired` | 0 | none left dangling |

## One-mutating-Queen rule (Foundation #1)
- The only scheduled mutating LLM lane is `sis-memory-maintenance` (SIS dreaming, bounded + receipted) and the read-only `railway-queen-weekly-review`.
- `c940-safe-reclaim-worker` mutates disk but is **script-gated** (idle cache leaves only, exact owner checks) — not an LLM queen.
- Dormant Queens paused 2026-08-14 (Queen-autonomy, Merge-Queen, 7h-Spring-Orchestrator, tier1-self-heal) remain paused. Do not re-enable a second always-on mutator in the same window.

## Jobs (compact)
| Cron | Class | Domain | Cadence | Delivers |
| --- | --- | --- | --- | --- |
| sis-memory-maintenance | specialist (LLM) | SIS memory | Mo–Fr 11:00 | local |
| railway-queen-weekly-review | queen (read-only) | Railway | Mon 09:30 | local |
| railway-monthly-rotation-audit | specialist | Railway security | 1st 10:00 | local |
| fleet-swarm-pulse | watchdog | fleet bus + heartbeat | every 6h | Telegram swarm |
| c940-always-on-host-watchdog | watchdog | host health | every 120m | Telegram DM |
| c940-security-sentinel-watchdog | watchdog | security | every 720m | Telegram DM |
| c940-disk-growth-guard | watchdog | capacity floor | every 60m | origin |
| c940-safe-reclaim-worker | watchdog (mutates disk, gated) | reclaim | every 360m | origin |
| design-workflow-drift-watch | watchdog | design system | daily 08:00 | origin |
| c940-storage-movement-graph-refresh | watchdog | storage intel | every 360m | local |
| brand-media-control-plane-watch | watchdog | brand media | daily 07:50 | origin |
| github-tech-radar-daily | watchdog | tech radar | daily 06:15 | local |
| topology-health-pulse | watchdog | topology | every 6h | local |
| llm-evals-integrity-watchdog | watchdog | LLM evals | daily 06:30 | origin |
| llm-evals-weekly-d0-regression | watchdog | LLM evals | Sun 07:15 | origin |
| creative-enterprise-stage0-watchdog | watchdog | creative | every 120m | origin |
| grok-bot-health-pulse | watchdog | grok bot | every 6h | local |

## Open gaps (see JSON `gaps`)
1. **P1 — Yoga Book peer OFFLINE.** No `yoga-book.json` heartbeat. Packet 4 first-boot never ran. Run `fleet/YOGA-BOOK-FIRST-BOOT.md` **on the Yoga Book** to stand up the second machine.
2. **P0-ops — disk 44 GiB < 50 floor < 80 target.** Capacity watchdogs hold; keep heavy work gated.
3. **P2 — evals weekly dirty.** `llm-evals-weekly-d0-regression` exits 1 (canonical repo not clean); clean worktree before live eval.
4. **P2 — GitHub harness inventory stale.** `GITHUB-HARNESS-INVENTORY.md` is 2026-07-21; 214 operational repos still unregistered. Refresh with `awesome-repo-control-plane` generator.

## Heartbeat now REAL+LIVE
`fleet-swarm-pulse` was upgraded 2026-08-29 to write genuine metrics into `fleet/bus/heartbeats/c940.json` (disk_free_gb, uptime_hours, book_state) instead of a static `live` flag. Peer machines and observers now see actual liveness. C940 still never forges a peer heartbeat (Foundation #11).
