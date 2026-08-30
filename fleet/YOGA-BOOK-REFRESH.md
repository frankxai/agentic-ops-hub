# Yoga Book — Refresh command (not cold first-boot)

**Context (2026-08-30):** Book was already online on the **git-bus**. Origin has Book-authored heartbeat:

```json
{"machine_id":"yoga-book","hostname":"Starlight","status":"live","free_gib":151.01,"at":"2026-08-16T10:45:05+00:00","notes":"… Dual ONLINE git-bus."}
```

C940 local tree had lost that file; restored from `origin/main` (Book-authored — **not forged**). Age ~14 days → needs a **refresh pulse**, not a full Packet-4 install from zero.

**Connection model:** git-bus is canonical. Hermes LAN peer is optional. Telegram bot = `@Hermesyogabookbot`.

---

## Approach

| Situation | Approach |
| --- | --- |
| Book machine on, Hermes/`agentic-ops` already present | **Refresh** (this doc) |
| Brand-new Book / wiped disk | Cold Packet 4: `fleet/YOGA-BOOK-FIRST-BOOT.md` + Telegram align |
| Only need UI work after HB fresh | Claim FE lane on `agent/book/<scope>` |

---

## Paste this to the Book agent (DM `@Hermesyogabookbot` or local Hermes on Book)

```text
You are the Yoga Book frontend fleet agent (hostname Starlight / machine_id yoga-book).
C940 (DESKTOP-1B4ICID) is the always-on backend control plane. You are frontend-innovation only.
Primary model: Grok 4.6 (hermes default). Codex only as fallback. Free tier (hy3) OK for non-critical review.

CONNECTION MODEL: the fleet bus is git-based under agentic-ops/fleet/bus/ (heartbeats, queues, activity).
You were already ONLINE on the git-bus (last HB 2026-08-16 dual ONLINE). This is a REFRESH, not a cold first boot.
Do NOT wait for a Hermes LAN peer. Do NOT forge c940 heartbeat.

EXECUTE NOW:

1) cd ~/agentic-ops   # or C:\Users\frank\agentic-ops — wherever agentic-ops-hub is cloned
   If missing: gh repo clone frankxai/agentic-ops-hub agentic-ops && cd agentic-ops

2) git fetch origin && git checkout main && git pull --ff-only origin main

3) gh auth status   # must be frankxai with repo+workflow

4) python scripts/fleet_inventory.py --machine yoga-book
   python scripts/fleet_sync.py --machine yoga-book

5) Refresh YOUR heartbeat only (never write c940.json):
   python scripts/fleet_bus.py identity
   python scripts/fleet_bus.py heartbeat --status live --notes "Book refresh 2026-08-30 · ACK C940 model-routing v4 grok-4.6 primary · ready for FE lanes"

6) Log activity:
   python scripts/fleet_activity.py log \
     --machine yoga-book --agent hermes-book \
     --did "HB refresh + fleet_sync after C940 handshake" \
     --evidence "fleet/bus/heartbeats/yoga-book.json" \
     --next "claim FE lane if open; mirror any DM proposals"

7) git add fleet/bus/heartbeats/yoga-book.json fleet/bus/identity/yoga-book.json fleet/activity fleet/last-inventory.json 2>/dev/null
   git status
   git commit -m "activity(book): HB refresh 2026-08-30 — dual ONLINE git-bus"
   git push origin HEAD:main
   # If main is protected: push agent/book/hb-refresh-20260830 and open PR — still fine; C940 pulls either way.

8) Telegram Swarm one-liner only:
   [book] ONLINE host=Starlight disk=…GB repos=… HB refreshed · FE ready

9) Read fleet/bus/queues/to-book.json and ops/OPS-LEDGER.md top. Claim frontend-only work on branches agent/book/<scope>.
   Do not touch Business. Do not force-push. Do not run C940 always-on cron fleet.

Report back: hostname, disk free, repos present, dirty counts, HB path + timestamp, next FE claim.
```

---

## Shorter one-liner (if Book agent already mid-session)

```text
Refresh Book git-bus now: cd agentic-ops && git pull && python scripts/fleet_inventory.py --machine yoga-book && python scripts/fleet_sync.py --machine yoga-book && python scripts/fleet_bus.py heartbeat --status live --notes "Book refresh 2026-08-30" && python scripts/fleet_activity.py log --machine yoga-book --agent hermes-book --did "HB refresh" --evidence "fleet/bus/heartbeats/yoga-book.json" --next "FE claim" && git add fleet/ && git commit -m "activity(book): HB refresh" && git push. Swarm: [book] ONLINE … Primary model Grok 4.6. Frontend lanes only. No c940 forge.
```

---

## Optional: Hermes LAN peer (only if you want gateway-to-gateway)

On **Book** after gateway is running:

```bash
hermes gateway status
# note the API base URL (e.g. http://<book-lan-ip>:8732) and API_SERVER_KEY from Book's hermes .env
```

On **C940** (only after Book shares URL+key):

```bash
hermes peer add yoga-book --url http://<book-lan-ip>:<port> --key <BOOK_API_SERVER_KEY> --note "frontend peer"
hermes peer list
```

This is **optional**. Git-bus already works without it.

---

## C940 side after Book pushes

```bash
cd C:/Users/frank/agentic-ops
git fetch origin
git show origin/main:fleet/bus/heartbeats/yoga-book.json   # or pull into local bus
python scripts/fleet_bus.py status
# expect book_online true + fresh HB age_minutes small
```

---

## What C940 already did
- Restored Book-authored HB + identity from origin/main into local bus (not forged).
- Refreshed `to-book.json` with handshake + FE tasks.
- Corrected model routing: **Grok 4.6 primary**; Codex fallback-only.
- R2 reviews on agentic-ops PRs #54/#53/#48.
