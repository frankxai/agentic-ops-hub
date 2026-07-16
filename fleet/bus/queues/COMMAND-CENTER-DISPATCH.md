# Command Center dispatch — 2026-07-16

**Issuer:** Frank / Starlight Command Center (via C940 control plane)  
**SoT:** `ops/OPS-LEDGER.md` + `fleet/TASK-PACKETS.md` + this file  
**Bus:** `fleet/bus/` (not the thrash channel)

## Protocol (both bots)

1. Work **lanes only** — C940 backend/ops; Book frontend.  
2. Interactive work in **DM with one bot**.  
3. Starlight Swarm channel = **status one-liners only** (`[c940]…` / `[book]…`).  
4. No dual-@ same task. No long tables in channel.  
5. Report done → OPS-LEDGER + optional Swarm one-liner.

---

## Active assignments

### A. yoga-book (Packet 4) — RUN ON BOOK

**Owner:** `@Hermesyogabookbot` / Book machine  
**Status:** **DONE / ONLINE** — `fleet/bus/heartbeats/yoga-book.json` LIVE (2026-07-16T16:45:59Z)

**Done:**
1. First-boot + Telegram align (Book control plane + Packet 4 claim report)  
2. Heartbeat `yoga-book.json` written **on Book only** (never forged c940)  
3. FAQ d12a38a applied: pull agentic-ops-hub only; ~60GB C940 = YELLOW not hard stop  
4. FE1 CLAIMED / implement HELD (disk TIGHT + dirty frankx `codex/blog` primary — no new worktree)

**Do next (optional):**
- `fleet_inventory` + `fleet_sync --machine yoga-book` when free headroom allows  
- FE1 branch `agent/book/r1-cta` when worktree gate clear  

**Blocked if:** Business clone, full C940 cron fleet, dual-write dirty C940 trees.

---

### B. c940 (now) — THIS MACHINE

| ID | Assignment | Priority | Status |
|----|------------|----------|--------|
| B1 | Commit `agentic-ops` fleet control plane (driver, bus, scripts, reports) | P0 ops | DONE d10d81c |
| B2 | R1 evidence refresh: frankx.ai ↔ gencreator.ai CTAs (measure, don’t ship) | P0 product | DONE YELLOW |
| B3 | Packet 6 light: classify top dirty trees (commit names only, no wipe) | P1 | DONE |
| B4 | rclone install path documented / attempt if safe | P1 backup | DONE install; crypt config MANUAL |
| B5 | Keep anti-thrash + pulse cron | ongoing | DONE |

**Do not:** ship frankx.ai main/prod; reset dirty; thrash Swarm.

---

### C. Shared after Book online

1. Book claims UI ticket from B2/B3 findings.  
2. C940 does content/backend R1; Book does nav/homepage CTA UI if needed.  
3. Handoff via branch + 5 lines OPS-LEDGER.

---

## Acceptance

- [x] `fleet/bus/heartbeats/c940.json` LIVE  
- [x] `fleet/bus/heartbeats/yoga-book.json` LIVE (Book)  
- [x] agentic-ops fleet committed + pushed when clean enough  
- [x] R1 evidence table updated in ledger  
- [x] Dirty top-3 classified  
- [ ] Swarm used only for short status  

**Last update:** 2026-07-16T16:45:59+00:00 · Book P4 ONLINE; FE1 claimed/held  

