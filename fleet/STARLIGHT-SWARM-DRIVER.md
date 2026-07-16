# Starlight Swarm — Driver (how we run multi-machine agents)

**Owner (always-on):** C940 · host `DESKTOP-1B4ICID` · bot `@lenovostarlightbot`  
**Companion:** Yoga Book · bot `@Hermesyogabookbot` (thin Hermes)  
**Last aligned:** 2026-07-16  

This is the **operating model** for continuous multi-agent / multi-machine work without Telegram thrash.

---

## 1. What is set up NOW (C940)

| Layer | Status | Notes |
| --- | --- | --- |
| Hermes gateway | ✅ running | Telegram + Slack connected |
| Home (interactive) | ✅ DM Frank `8582160385` | Topics per task — **keep this** |
| Shared bus (one-way) | ✅ channel `-1004300203404` **Starlight Swarm** | Status / digests only |
| Channel allowlist | ✅ `TELEGRAM_GROUP_ALLOWED_CHATS` | Required for channel-scoped auth |
| Anti-thrash patch | ✅ adapter echo filter + channel require-mention | Prevents self-interrupt storms |
| `busy_input_mode` | ✅ `queue` | No hard interrupt on new inbound |
| Fleet control plane | ✅ `agentic-ops/fleet/` | inventory / sync / backup scripts |
| Fleet file bus | ✅ `fleet/bus/{heartbeats,identity,inbox,queues}` | Lightweight agent↔agent files |
| Always-on crons | ✅ (must be **model-pinned**) | ops, GEO, SIS, Railway, fleet inventory |
| Yogabook first boot | 📄 `fleet/YOGA-BOOK-FIRST-BOOT.md` | Run **on Book** |

**Not home:** Starlight Swarm channel. Do **not** `/sethome` there.

---

## 2. Roles (lead vs execute)

| Who | Leads | Executes |
| --- | --- | --- |
| **You (Frank)** | Priorities, ship gates, hard-stops | Approvals, secrets, Book first-boot |
| **C940 / Lenovo bot** | Fleet control plane, backend, content/GEO, crons, Railway | Heavy Hermes profiles + Claude/Codex |
| **Yoga Book bot** | Frontend / product UI / innovation | Thin Hermes + Codex/Antigravity |
| **Git + OPS-LEDGER** | Cross-machine truth | Branches `agent/<machine>/<scope>` |

**Rule:** One machine = one role = one primary Telegram **DM** session for interactive work.  
**Channel** = bulletin board, not a shared brain.

---

## 3. How to drive work (daily)

### A. Interactive (best quality)

1. Open **DM with the right bot** (Lenovo for backend, Yogabook for UI).  
2. One topic per task (auto-renamed).  
3. Give a clear goal + repo path + “done when…”.  
4. Do **not** paste the same goal to both bots unless lanes are split.

### B. Cross-machine handoff

1. C940 finishes backend → `git push` branch `agent/c940/<scope>`.  
2. 5 lines in `agentic-ops/ops/OPS-LEDGER.md`.  
3. Optional one-line status to Swarm:  
   `hermes send --to telegram:-1004300203404 "[c940] handoff: …"`  
4. Book claims frontend on `agent/book/<scope>` only.

### C. Always-on (no chat thrash)

C940 crons own recurring loops. Prefer **local** or **Swarm one-way** delivery — not dual interactive sessions in the channel.

---

## 4. Telegram rules (stop interrupting each other)

| Rule | Why |
| --- | --- |
| Channel = **@mention required** | No free-process every post |
| Status posts ignored as echoes | Stops self-interrupt loops |
| `busy_input_mode=queue` | New mail waits; doesn’t steal turn |
| **Exclusive bot mentions** | `@otherbot` is ignored by this bot |
| One bot per instruction | No dual-@ same task |
| After “Stop / END thrash / (no-op)” | **Zero tools, empty turn** until real task |
| Ignore ⚡ / ⏳ / 📋 system banners | Not user tasks |

**Talk to Lenovo in Swarm only as:**

```text
@lenovostarlightbot <one clear task>
```

Deep work → **DM**.

---

## 5. Alignment checklist (both machines best state)

### C940 (this machine — control plane)

- [x] Hostname `DESKTOP-1B4ICID` = `c940`
- [x] Gateway running; home = DM
- [x] Swarm allowlisted; anti-thrash config
- [ ] All crons **pinned** to `xai-oauth` / `grok-4.5` (fix after pin)
- [ ] `python scripts/fleet_inventory.py --machine c940` daily (cron)
- [ ] Heartbeat file written under `fleet/bus/heartbeats/c940.json`
- [ ] No second full always-on Hermes profile fighting default gateway

### Yoga Book (companion)

- [ ] Run Packet 4: `fleet/YOGA-BOOK-FIRST-BOOT.md`
- [ ] Hostname recorded in `clone-manifest.json` hints
- [ ] Same Telegram discipline: **require_mention**, **busy_input_mode=queue**, group allowlist for Swarm
- [ ] **Do not** install full C940 cron fleet
- [ ] Bot only responds to `@Hermesyogabookbot`
- [ ] Clone set `yoga_book_core` only — no Business
- [ ] Paste “Book online” inventory summary to Swarm **once** after boot

### Shared excellence bar

| Metric | Target |
| --- | --- |
| Free disk C: | ≥80 GB (excellent ≥100) |
| Dirty prod trees | Classify; no mass wipe |
| Register boundaries | FrankX / Arcanea / SIS-ACOS never leak |
| Two writers same tree | **Never** |
| Bus heartbeats | Only **self** machine writes its own |

---

## 6. Commands (C940)

```bash
# Identity
hostname
# → DESKTOP-1B4ICID

# Fleet health
cd C:/Users/frank/agentic-ops
python scripts/fleet_inventory.py --machine c940
python scripts/fleet_sync.py --machine c940 --dry-run
python scripts/fleet_backup_check.py

# One-way status to Swarm (no agent loop)
hermes send --to telegram:-1004300203404 "[c940] …"

# Interactive work
# → Telegram DM @lenovostarlightbot (topics)
```

### Book (on Book only)

```bash
cd ~/agentic-ops   # after clone agentic-ops-hub
python scripts/fleet_inventory.py --machine yoga-book
python scripts/fleet_sync.py --machine yoga-book
```

---

## 7. What C940 leads and executes by default

| Domain | Action |
| --- | --- |
| Backend / infra | SIS, ACOS, Railway, agentic-ops |
| Content / GEO | frankx.ai strategy, images, audits |
| Fleet | inventory, sync policy, backup posture |
| Swarm hygiene | channel config, anti-thrash, status posts |
| Book | **does not** run Book UI — waits for Book claims |

Book leads UI/UX on FrankX/prod/GenCreator/Arcanea surfaces after Packet 4.

---

## 8. Escalation / thrash recovery

1. In Swarm or DM: `/stop` once.  
2. Do not re-@ both bots.  
3. Continue in **DM topic** with a single bot.  
4. If dual gateways monologue: hard-stop phrase → agents go silent.  
5. Structural fix: forum group with **topics per machine** (future), not more channel chat.

---

## 9. Future upgrade (recommended)

Replace channel-as-bus with **private forum supergroup**:

| Topic | Owner |
| --- | --- |
| `c940` | Lenovo home-adjacent work |
| `yogabook` | Book |
| `ops` | digests / heartbeats |
| `incidents` | alerts only |

Until then: **DM = work · Swarm channel = bulletin**.

---

## 10. File SoTs

| Path | Role |
| --- | --- |
| `fleet/STARLIGHT-SWARM-DRIVER.md` | This driver |
| `fleet/FLEET-OPS.md` | Daily/weekly loops |
| `fleet/clone-manifest.json` | Machines + clone sets |
| `fleet/YOGA-BOOK-FIRST-BOOT.md` | Book onboard |
| `fleet/activity/` | Shared ACTIVITY-LOG + calendar + proposals |
| `fleet/activity/BOOK-DM-MIRROR.md` | Book private-DM → log (mandatory) |
| `scripts/fleet_activity.py` | `log` / `propose` / `proposals` / `tail` / `today` |
| `ops/OPS-LEDGER.md` | Cross-repo status |
| `~/.hermes` (per machine) | Gateway + Telegram config |
| skill `agentic-fleet-strategy` | Agent playbook |

### Private DM mirror (both bots)

Private Telegram DMs never cross machines. After a proposal in DM:

```bash
python scripts/fleet_activity.py propose --agent hermes-book --title "…" --source private-dm
# commit + push agentic-ops so the peer can pull
```
