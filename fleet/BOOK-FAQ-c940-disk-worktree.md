# Book FAQ — c940.json, worktree, 80GB (2026-07-16)

## Do you need `c940.json`?

**File:** `fleet/bus/heartbeats/c940.json` (also mirrored under `bus/heartbeats/` sometimes)

| Who | Need? | How |
| --- | --- | --- |
| **C940 (Lenovo)** | Yes — write **self** heartbeat only | `python scripts/fleet_bus.py heartbeat` or fleet_pulse cron |
| **Yoga Book** | **Read-only optional** | `git pull` agentic-ops-hub — sees last committed heartbeat |
| **Book must NOT** | Forge / invent c940 heartbeats | Only C940 may write machine_id=c940 |

Book’s required file is **`yoga-book.json`** (written **on Book**, same folder pattern), not a copy of c940.json.

**Pull is enough.** You do **not** need to copy files off Lenovo by hand if agentic-ops is on GitHub (`frankxai/agentic-ops-hub`).

---

## Do you need the whole worktree?

| Goal | Need |
| --- | --- |
| Read dispatch / activity / heartbeats | **Only** `agentic-ops` clone (small) |
| Frontend on frankx / GenCreator / Arcanea | **yoga_book_core** clone set via `fleet_sync --machine yoga-book` — **not** every private repo |
| Business / wallets / full C940 estate | **No** — do not clone |

So: **not** the whole estate worktree. Control plane + core product repos only.

```bash
gh repo clone frankxai/agentic-ops-hub agentic-ops
cd agentic-ops
python scripts/fleet_inventory.py --machine yoga-book
python scripts/fleet_sync.py --machine yoga-book
```

---

## Do we *truly* need 80GB free?

| Level | Free space | Meaning |
| --- | --- | --- |
| **Floor** | ~50 GB | Avoid hard failure; OK short-term |
| **Target (fleet docs)** | **≥80 GB** | Comfortable builds, node_modules, images, dual clones |
| **Excellent** | ≥100 GB | Headroom for agents |

**C940 now:** ~**60 GB free** (≈88% used) — **above floor, below target**.  
Not an emergency stop, but **YELLOW**: large Next builds / dual agents / docker will hurt.

**Book:** only needs enough for its **core** clones — often **30–50 GB free** is workable if it doesn’t full-mirror the estate. Don’t force Book to free 80GB on C940’s behalf.

---

## How to free space on C940 (safe order)

Protect forever: `Business`, `.ssh`, Infisical, Hermes profiles secrets, restic repos you care about.

1. **Empty Recycle Bin** + Storage Sense  
2. **Temp:** `%TEMP%`, Windows Temp  
3. **Package caches:** `pnpm store prune`, `npm cache clean --force`, old `uv`/`pip` caches  
4. **Hermes caches:** image/audio cache under `%LOCALAPPDATA%\hermes` (sessions careful)  
5. **Browser caches**  
6. **Orphan `node_modules`** in abandoned folders (classify first)  
7. **Docker** images if present  
8. **Old worktrees / ship clones** no longer needed  

Never: mass `rm -rf` dirty git trees; never delete Business.

---

## What C940 already provides for Book

After `git pull` on agentic-ops-hub you get:

- `fleet/bus/heartbeats/c940.json`  
- `fleet/bus/queues/to-book.json`  
- `fleet/activity/*`  
- Packet 4 docs  
