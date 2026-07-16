# Fleet Shared Activity — Best Practices

**SoT for multi-agent visibility** (both machines, all bots).  
**Enhance-never-erase.** Append-only logs. Queue over interrupt.

## Why this exists

Private DMs are **not** visible across machines. Channel thrash is not a log.  
Agents must write **shared files** so Command Center (you) and peer bots can see:

- who did what  
- when  
- what they proposed next  
- what is **queued** vs **running**

## Layers (one SoT per concern)

| Layer | Path | Use |
| --- | --- | --- |
| **Activity log** | `fleet/activity/ACTIVITY-LOG.md` | Append-only timestamped events |
| **Day calendar** | `fleet/activity/calendar/YYYY-MM-DD.md` | Human glance of the day |
| **Proposals stream** | `fleet/activity/proposals.jsonl` | Machine-readable DM mirrors |
| **Book DM mirror playbook** | `fleet/activity/BOOK-DM-MIRROR.md` | Mandatory Book private-DM → log |
| **Machine queues** | `fleet/bus/queues/to-*.json` | Durable assign/claim |
| **Hermes Kanban** | `hermes kanban` (board `fleet`) | Atomic claim / status / schedule |
| **OPS-LEDGER** | `ops/OPS-LEDGER.md` | Cross-repo executive status |
| **Swarm channel** | Telegram `-1004300203404` | Short assign/done only |

## Queue, don’t interrupt (advanced collab)

1. New ask → **append log** + **queue file / kanban create** — do **not** steal a running agent turn.  
2. Running work stays running until done / blocked / human `/stop`.  
3. Peer “need X” → log + queue; peer picks up when free.  
4. Channel: one-line tickets; never long multi-agent debates.  
5. `busy_input_mode: queue` on both gateways.

## Mandatory log entry format

```markdown
### YYYY-MM-DDTHH:MM:SSZ · machine · agent · event
- **Did:** …
- **Evidence:** path / SHA / URL
- **Proposed next:** …
- **Queue impact:** none | queued TASK-ID | blocked on …
```

## After every meaningful turn

```bash
# from agentic-ops — general event
python scripts/fleet_activity.py log \
  --machine c940 \
  --agent hermes-lenovo \
  --did "..." \
  --evidence "..." \
  --next "..."

# Book (or any agent): private-DM proposal mirror (REQUIRED for cross-machine)
python scripts/fleet_activity.py propose \
  --machine yoga-book \
  --agent hermes-book \
  --title "one-line proposal" \
  --body "short detail" \
  --next "what peer should do" \
  --source private-dm \
  --queue-to c940

# then commit + push so peer can pull
```

Or hand-edit `ACTIVITY-LOG.md` + today’s `calendar/YYYY-MM-DD.md`.  
Full Book protocol: **`BOOK-DM-MIRROR.md`**.

## Reading peers (Book / other)

1. `git pull` agentic-ops (or hub)  
2. Read tail of `ACTIVITY-LOG.md`  
3. `python scripts/fleet_activity.py proposals -n 10`  
4. Read `fleet/bus/queues/to-c940.json` / `to-book.json`  
5. `hermes kanban list` on shared board if used  

**Private Telegram DM with one bot never reaches the other machine.**  
Peer must **mirror** proposals into this log (or queues).

## Calendar view

Each day file is a checklist + timeline. Not Google Calendar (optional later via google-workspace skill). Markdown first = git-visible, multi-machine, no OAuth friction.

## Kanban mapping

| Status | Meaning |
| --- | --- |
| triage/todo | Queued — not started |
| ready | Unblocked, claimable |
| running | One owner, do not interrupt |
| blocked | Waiting human / peer |
| done | Evidence in log |

## Anti-patterns

- Only talking in Swarm channel  
- Forging peer heartbeats  
- Starting three “urgent” threads mid-task  
- Erasing log history  
- Treating empty Kanban as “no work” without reading ACTIVITY-LOG  
