# Cron Classification — C940 Fleet (2026-08-29)

**Repository source of truth:** `fleet/cron-classification.json` only.
**Live source:** `hermes cron list on DESKTOP-1B4ICID`.
**Projection:** this file is generated from the JSON `jobs` array; edit the JSON, then run `python scripts/render_cron_classification.py`.

## Class distribution (active = 17, paused = 0)

| Class | Count | Rule |
| --- | ---: | --- |
| `watchdog` | 14 | script-only, no-agent; silent when healthy; never mutates LLM state |
| `specialist` | 2 | one domain, one outcome, pinned model (or script) |
| `queen` | 1 | cross-domain judgment lane; write permissions are declared independently and default to false |
| `oneshot` / `retired` | 0 | none left active or dangling |

## Write dimensions

| Dimension | Writers | Meaning |
| --- | ---: | --- |
| `llm_state` | 1 | writes or consolidates LLM-managed memory/state |
| `heartbeat_control_plane` | 1 | writes fleet heartbeat, queue, or control-plane state |
| `filesystem` | 3 | creates, updates, or removes filesystem content beyond transient process logs |

## Scheduled-write policy

- LLM-state writer limit: **1**.
- LLM-state writers: `sis-memory-maintenance`.
- Read-only queen lanes: `railway-queen-weekly-review`.
- Heartbeat/control-plane writers: `fleet-swarm-pulse`.
- Filesystem writers: `sis-memory-maintenance`, `fleet-swarm-pulse`, `c940-safe-reclaim-worker`.

## Jobs

| Cron | Class | Write dimensions | Domain | Cadence | Delivers |
| --- | --- | --- | --- | --- | --- |
| `sis-memory-maintenance` | `specialist` | `llm_state`, `filesystem` | memory/SIS | 0 11 * * 1-5 | local |
| `railway-queen-weekly-review` | `queen` | none | Railway estate | 30 9 * * 1 | local |
| `railway-monthly-rotation-audit` | `specialist` | none | Railway security/audit | 0 10 1 * * | local |
| `fleet-swarm-pulse` | `watchdog` | `heartbeat_control_plane`, `filesystem` | fleet bus | 0 */6 * * * | telegram:-1004300203404 |
| `c940-always-on-host-watchdog` | `watchdog` | none | host health | every 120m | telegram:8582160385 |
| `c940-security-sentinel-watchdog` | `watchdog` | none | security | every 720m | telegram:8582160385 |
| `c940-disk-growth-guard` | `watchdog` | none | capacity | every 60m | origin |
| `c940-safe-reclaim-worker` | `watchdog` | `filesystem` | capacity/reclaim | every 360m | origin |
| `design-workflow-drift-watch` | `watchdog` | none | design system | 0 8 * * * | origin |
| `c940-storage-movement-graph-refresh` | `watchdog` | none | storage intelligence | every 360m | local |
| `brand-media-control-plane-watch` | `watchdog` | none | brand media | 50 7 * * * | origin |
| `github-tech-radar-daily` | `watchdog` | none | tech radar | 15 6 * * * | local |
| `topology-health-pulse` | `watchdog` | none | topology | 15 */6 * * * | local |
| `llm-evals-integrity-watchdog` | `watchdog` | none | LLM evals | 30 6 * * * | origin |
| `llm-evals-weekly-d0-regression` | `watchdog` | none | LLM evals | 15 7 * * 0 | origin |
| `creative-enterprise-stage0-watchdog` | `watchdog` | none | creative enterprise | every 120m | origin |
| `grok-bot-health-pulse` | `watchdog` | none | grok bot | 45 */6 * * * | local |

## Open gaps

1. **P1 — book-peer-offline.** Yoga Book heartbeat is stale; no fresh self-heartbeat has been observed since 2026-08-16T10:45:05+00:00. Packet 4 first-boot remains incomplete, so dispatch stays blocked. Fix = run fleet/YOGA-BOOK-FIRST-BOOT.md ON the Yoga Book machine.
2. **P0-ops — disk-below-floor.** 44GiB free < 50GiB ops floor < 80GiB target. Capacity watchdogs active but heavy work must stay gated.
3. **P2 — evals-weekly-dirty.** llm-evals-weekly-d0-regression exits 1 because canonical repo is dirty; needs a clean worktree before live eval.
4. **P2 — github-harness-inventory-stale.** GITHUB-HARNESS-INVENTORY.md (2026-07-21) shows 214 unregistered operational repos; refresh via awesome-repo-control-plane generator.

## Heartbeat writes are explicit

`fleet-swarm-pulse` declares both `heartbeat_control_plane` and `filesystem` writes: Writes c940 heartbeat + one-line Swarm bulletin; UPGRaded 2026-08-29 to carry real disk/uptime metrics. Each machine still writes only its own heartbeat.
