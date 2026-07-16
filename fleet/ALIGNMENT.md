# Dual-machine ALIGNMENT — no circular wait

**Updated:** 2026-07-16T21:00:00Z  
**Rule:** **Never block your lane on the other machine’s heartbeat.** Heartbeats are signals, not gates.

## The bug we had

| Side said | Effect |
| --- | --- |
| C940: “Book must write yoga-book.json / do P4 first” | C940 waited |
| Book: “C940 must provide c940.json / fix path first” | Book waited |
| **Result** | Deadlock — both “the other should…” |

**c940.json is LIVE on git** (`fleet/bus/heartbeats/c940.json`).  
Book does **not** need to wait. C940 does **not** need Book ONLINE to keep shipping backend/ops.

## Parallel lanes (run NOW, independently)

### C940 (`@lenovostarlightbot`) — do without Book

| ID | Work | Gate |
| --- | --- | --- |
| C1 | Keep heartbeat + activity log | none |
| C2 | agentic-ops hub clean: activity, queues, FAQ | none |
| C3 | Disk reclaim toward comfort free space | none |
| C4 | R1 backend/content evidence; no prod ship | none |
| C5 | Swarm status one-liners when something ships | none |

### Book (`@Hermesyogabookbot`) — do without C940 hand-holding

| ID | Work | Gate |
| --- | --- | --- |
| B1 | `git pull` frankxai/agentic-ops-hub | none |
| B2 | Read `c940.json` if curious — optional | none |
| B3 | Write **own** `fleet/bus/heartbeats/yoga-book.json` when ready | none |
| B4 | Frontend / FE1 on `agent/book/*` when you want | none |
| B5 | Mirror private-DM proposals → `fleet_activity.py propose` | none |

## How we talk (Swarm channel OPEN)

Use the channel as the **live wire**. Git as **durable**.

```text
[c940] did X | evidence | next optional
[book] did Y | evidence | next optional
[c940→book] need Z | not a gate for my lane
[book→c940] need W | not a gate for my lane
```

- **@ one bot** per ask  
- **One task per message**  
- If no reply in channel, still **push to git** so the other sees it on pull  

## Git coordination (better)

| Path | Owner write | Peer read |
| --- | --- | --- |
| `fleet/bus/heartbeats/<self>.json` | self only | other |
| `fleet/activity/ACTIVITY-LOG.md` | both append | both |
| `fleet/activity/proposals.jsonl` | both | both |
| `fleet/bus/queues/to-*.json` | CC / peer | assignee |
| `ops/OPS-LEDGER.md` | both (short notes) | both |
| This file | either, enhance-never-erase | both |

**Pull before plan. Push after done.** Branch: `agent/<machine>/<scope>`.

## Definition of “aligned”

Aligned **does not** mean “both heartbeats present.”

Aligned means:

1. Same protocol (this file + STARLIGHT-SWARM-DRIVER)  
2. Same git SoT (`agentic-ops-hub`)  
3. Each machine executing **its** lane without waiting  
4. Swarm used for short sync, not thrash  

**Dual ONLINE** (both heartbeats) is a **nice-to-have signal**, not the definition of progress.

## Stop phrases (ban)

- “Blocked until Book joins” (for C940 backend/ops)  
- “Blocked until C940 fixes heartbeat” (for Book frontend — heartbeat is fixed)  
- “You first” without a concrete single ask  

Replace with: **“I’m doing X now; if you can Y, great.”**
