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
**Status:** OPEN — no Book heartbeat on bus  

**Do:**
1. Follow `fleet/YOGA-BOOK-FIRST-BOOT.md`  
2. Apply `fleet/YOGA-BOOK-TELEGRAM-ALIGN.md`  
3. `fleet_inventory` + `fleet_sync` for `yoga-book`  
4. Write heartbeat only if host is Book (never forge c940)  
5. Paste one Swarm line: `[book] ONLINE host=… repos=…`  
6. Claim frontend only: frankx.ai UI, GenCreator UI, Arcanea UI on `agent/book/<scope>`

**Blocked if:** Business clone, full C940 cron fleet, dual-write dirty C940 trees.

---

### B. c940 (now) — THIS MACHINE

| ID | Assignment | Priority | Status |
|----|------------|----------|--------|
| B1 | Commit `agentic-ops` fleet control plane (driver, bus, scripts, reports) | P0 ops | IN PROGRESS |
| B2 | R1 evidence refresh: frankx.ai ↔ gencreator.ai CTAs (measure, don’t ship) | P0 product | NEXT |
| B3 | Packet 6 light: classify top dirty trees (commit names only, no wipe) | P1 | NEXT |
| B4 | rclone install path documented / attempt if safe | P1 backup | AFTER B1 |
| B5 | Keep anti-thrash + pulse cron | ongoing | DONE |

**Do not:** ship frankx.ai main/prod; reset dirty; thrash Swarm.

---

### C. Shared after Book online

1. Book claims UI ticket from B2/B3 findings.  
2. C940 does content/backend R1; Book does nav/homepage CTA UI if needed.  
3. Handoff via branch + 5 lines OPS-LEDGER.

---

## Acceptance

- [ ] `fleet/bus/heartbeats/c940.json` LIVE  
- [ ] `fleet/bus/heartbeats/yoga-book.json` LIVE (Book)  
- [ ] agentic-ops fleet committed + pushed when clean enough  
- [ ] R1 evidence table updated in ledger  
- [ ] Dirty top-3 classified  
- [ ] Swarm used only for short status  

**Last update:** 2026-07-16 · C940  
