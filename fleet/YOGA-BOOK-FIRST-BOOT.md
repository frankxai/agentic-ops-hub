# Yoga Book — First Boot (Packet 4)

Run this **on the Yoga Book** (frontend machine). C940 is already the control plane.

## 1. Install (if missing)

- Git for Windows
- GitHub CLI (`gh`)
- Node 24 LTS + pnpm
- Python 3.11+
- Claude Code, Codex (optional Hermes lite)

## 2. Auth

```bash
gh auth login
# account: frankxai · scopes: repo, workflow, read:org
gh auth status
```

## 3. Control plane + sync

```bash
cd ~
gh repo clone frankxai/agentic-ops-hub agentic-ops
cd agentic-ops
python scripts/fleet_inventory.py --machine yoga-book
python scripts/fleet_sync.py --machine yoga-book
python scripts/fleet_backup_check.py
```

## 4. Role rules

| Do | Don't |
| --- | --- |
| Frontend UI on FrankX / prod / GenCreator / Arcanea | Clone Business |
| Branches `agent/book/<scope>` | Always-on heavy Hermes crons |
| Worktrees for parallel UI | Two agents same dirty main tree |
| Update OPS-LEDGER after sessions | Force-push main/prod |

## 5. Report back

Paste inventory summary into Telegram **Starlight Swarm** or append OPS-LEDGER:

```
Yoga Book online
hostname: ...
disk free: ...
repos present: ...
dirty: ...
```

Also write self heartbeat + first activity entry:

```bash
python scripts/fleet_bus.py identity
python scripts/fleet_bus.py heartbeat --status live --notes "Packet 4 first boot"
python scripts/fleet_activity.py log \
  --machine yoga-book --agent hermes-book \
  --did "Packet 4 first boot complete" \
  --evidence "fleet/last-inventory.json" \
  --next "claim FE1 if open"
git add fleet/ && git commit -m "activity(book): online" && git push
```

## 6. Private DM proposals → shared log (always)

Any plan agreed with Frank in **private DM** is invisible to C940. Mirror with:

```bash
python scripts/fleet_activity.py propose \
  --machine yoga-book --agent hermes-book \
  --title "…" --source private-dm --queue-to c940
```

See `fleet/activity/BOOK-DM-MIRROR.md` + `fleet/YOGA-BOOK-TELEGRAM-ALIGN.md`.

## 7. First frontend claims (after sync)

1. frankx.ai UI polish (coord with C940 content)  
2. GenCreator product UI (R1 bridge complement)  
3. Arcanea platform UI  

Full prompts: `fleet/TASK-PACKETS.md` Packet 4.
