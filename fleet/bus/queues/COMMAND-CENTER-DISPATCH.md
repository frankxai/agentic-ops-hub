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
- [ ] `fleet/bus/heartbeats/yoga-book.json` LIVE (Book)  
- [x] agentic-ops fleet committed + pushed when clean enough  
- [x] R1 evidence table updated in ledger  
- [x] Dirty top-3 classified  
- [ ] Swarm used only for short status  

**Last reconciled:** 2026-08-28T11:32:57+00:00 · this document distinguishes historical entries from
current work; it is not a machine-liveness source.

## Current control-plane reconciliation (2026-08-28)

- The 2026-07 B1–B5 rows above are historical. They are not an authorization to restart C940 work.
- `fleet/bus/heartbeats/c940.json` and `fleet/bus/heartbeats/yoga-book.json` are observed historical
  files. Only their physical machine may refresh them; a stale heartbeat proves neither current work
  nor current availability.
- The prior private-bus Observatory envelope
  `da6438f6-12f2-4fc5-953d-3b7cd741bbc3` remains pending without a `resultRef`. It is superseded by
  priority-1 envelope `1c8e7f46-872a-4369-a665-6341ef10afcb`; C940 must provide the next receipt.
- The 2026-08-19 seven-hour packet is historical. It is not a current queue item or a basis for a
  second concurrent campaign.

### Dispatch rules for new work

1. Verify the local machine identity and four Git facts before a lane write.
2. Inspect active queues/contracts first. Preserve stale envelopes; send at most one explicit
   priority-1 supersession rather than duplicate tasks.
3. Create a fresh contract with `task-lease --file`; only its issuer may write the lease and only its
   owner may claim or complete it. Expired or unclaimed contracts cannot receive a receipt.
4. Keep peer identities/heartbeats out of other machines' commits. Use a returned `resultRef`, not a
   chat update, as cross-machine completion evidence.
5. Merges, deploys, credentials, spending, external sends, force pushes, and branch deletion remain
   human-gated.
