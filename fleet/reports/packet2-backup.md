# Packet 2 — Backup & Migration Posture (C940)

**Date:** 2026-07-16  
**Host:** DESKTOP-1B4ICID (C940)  
**Script:** `python scripts/fleet_backup_check.py` → **RED**  
**Artifact:** `fleet/last-backup-check.json`  
**Constraints honored:** no secret upload; Infisical unchanged

---

## 1. Tool-verified posture

| Check | Result | Detail |
| --- | --- | --- |
| gh auth | **OK** | frankxai; scopes gist, read:org, repo, workflow |
| OneDrive | **OK** | `C:\Users\frank\OneDrive` present |
| restic | **OK** | 0.18.1 (WinGet Links) — encrypted local snapshots available |
| rclone | **MISSING** | No offsite crypt layer (B2/S3) |
| tar | **OK** | GNU tar 1.35 |
| Disk free | **YELLOW** | **66.9 GB** / 476 GB (target ≥80 GB) |
| Business | **GAP** | Exists + git repo; **no remote origin** (local-only risk) |
| agentic-ops dirty | **GAP** | dirty=23 — commit fleet control plane |
| Overall | **RED** | 4 gaps (see script output) |

### Script output (this run)

```
# Backup check — RED
free_gb=66.9 onedrive=True rclone=False restic=True
- GAP: rclone MISSING — no encrypted offsite layer
- GAP: disk free 66.9GB < 80GB target
- GAP: Business has no git origin — local-only risk
- GAP: agentic-ops dirty=23 — commit fleet control plane
```

---

## 2. 3-2-1 layer status

| Layer | Target | Status | Action |
| --- | --- | --- | --- |
| 1 Primary | GitHub remotes + live trees | **Partial** | gh OK; control plane dirty; Business has no remote |
| 2 Secondary | OneDrive + restic local snapshots | **Partial** | OneDrive OK; restic installed but no documented scheduled snapshot yet |
| 3 Offsite | rclone crypt → B2/S3 | **Missing** | Install rclone + configure crypt remote |

---

## 3. Protect-list verification (C940)

Protect forever: `.ssh`, secrets, Business, SIS vaults, Hermes profiles.

| Path | Present | Notes |
| --- | --- | --- |
| `~/.ssh` | **OK** | id_ed25519 + known_hosts |
| `~/.secrets` | **OK** | `.env.master` + load/redact scripts (not bare `~/secrets`) |
| `~/Business` | **OK** | git on `main`; **no origin** — ~25 MB tracked walk (excl. node_modules) |
| Hermes profiles | **OK** | `~/.hermes/profiles/*` (default, frankx-prod, sis-starlight, business-sensitive, …) |
| `~/AppData/Local/hermes` | **OK** | large (~1 GB) — sessions/cache; export profiles carefully, do not bulk-mirror DBs to Book |
| `~/starlight-private-memory` | **OK** | present |
| `~/arcanea-vault` | **OK** | has `.git` |
| `~/.infisical` | **OK** | present — **do not modify** without approval |
| `~/SIS` (home root) | **MISS** | no top-level `SIS/`; related: `sis-ship-wave2`, profile `sis-starlight`, Arcanea SIS paths |

**Local-only risk (highest):** `Business` — no `git remote`. Prefer decision: private GitHub remote **or** restic/rclone encrypted-only (no secret dumps to public remotes).

---

## 4. Install commands — **gaps only**

restic is already installed → **no restic install**. Docker optional → not required for fleet sync.

```powershell
# Offsite layer only (C940 operator)
winget install Rclone.Rclone
# After install, open new shell then:
rclone version
# Operator next (manual, not automated here):
#   rclone config   # create remote (e.g. B2 or S3)
#   rclone config   # create crypt remote over it
#   document remote name in SECRETS-REGISTRY / private notes — never commit crypt passwords
```

Optional later (not a gap today):

```powershell
# only if restic ever missing on another machine:
winget install restic.restic
```

---

## 5. C940 actionable checklist

- [x] Run `python scripts/fleet_backup_check.py` (RED; JSON written)
- [x] Confirm OneDrive path
- [x] Confirm restic present / rclone missing
- [x] Confirm Business origin gap
- [x] Verify protect-list paths (table above)
- [ ] **Operator:** `winget install Rclone.Rclone` + crypt remote config
- [ ] **Operator:** Business remote policy decision  
  - Option A: private remote under frankxai (no secrets in tree)  
  - Option B: encrypted restic + rclone only (no git origin)
- [ ] Commit agentic-ops fleet control plane (dirty=23) — Packet 6 / steward
- [ ] Disk reclaim toward ≥80 GB free (Phase dual-control; snapshot protect-list first)
- [ ] First restic snapshot of protect paths (before next high-risk cleanup)
- [ ] Schedule weekly: `python scripts/fleet_backup_check.py` (cron or Task Scheduler)

### Pre-cleanup snapshot rule (before reclaim)

1. `python scripts/fleet_inventory.py --machine c940`
2. restic snapshot of protect-list **or** ensure remotes pushed
3. Quarantine log under `_quarantine/YYYY-MM-DD/`
4. Blue/Red dual-control for high-risk deletes

Suggested restic includes (illustrative — operator sets repo path/password offline):

```text
C:\Users\frank\.ssh
C:\Users\frank\.secrets
C:\Users\frank\Business
C:\Users\frank\.hermes\profiles
C:\Users\frank\starlight-private-memory
C:\Users\frank\arcanea-vault
```

Do **not** put Infisical master secrets or raw API dumps into public git.

---

## 6. Yoga Book migration checklist (actionable)

**Role:** frontend-innovation · **Do not** clone Business · **Do not** always-on heavy crons.

### First-boot (on Book)

```bash
# 1) Core tools
winget install Git.Git GitHub.cli OpenJS.NodeJS.LTS Python.Python.3.12
# pnpm: corepack enable && corepack prepare pnpm@latest --activate
# Claude Code / Codex / Hermes lite per CODING_AGENTS_REGISTRY

# 2) Auth
gh auth login   # frankxai; scopes: repo, workflow, read:org

# 3) Control plane only first
gh repo clone frankxai/agentic-ops-hub agentic-ops
cd agentic-ops

# 4) Inventory + sync for this machine
python scripts/fleet_inventory.py --machine yoga-book
python scripts/fleet_sync.py --machine yoga-book

# 5) Hostname hint in clone-manifest if hostname ≠ yoga-book
# 6) Ledger: "Yoga Book online — role frontend"
```

### Migrate from C940 → Book (selective — **no full disk clone**)

| Migrate | How |
| --- | --- |
| Control plane + shared product repos | git via `fleet_sync` / manifest |
| Hermes skills/profile (if needed) | `hermes profile export` → import on Book; re-auth OAuth on Book |
| Secrets | Infisical / password manager only — **never** scp `.env.master` over chat |
| Machine registry | already in agentic-ops git |

| Do **not** mirror | Why |
| --- | --- |
| `node_modules`, `.next`, build caches | reinstall |
| `Business` tree / BV secrets | C940-only |
| Full SIS heavy caches | not Book role |
| Hermes session DBs bulk | large; re-auth + fresh sessions |
| Raw `.secrets` / wallets | Infisical SoT |

### Book verify gate

- [ ] `gh auth status` → frankxai  
- [ ] `agentic-ops` cloned + `fleet/last-inventory.json` written on Book  
- [ ] ≥ control plane + 3 product repos present  
- [ ] Branch prefix: `agent/book/<scope>`  
- [ ] Report inventory summary → OPS-LEDGER / Telegram Starlight Swarm  

### Copy-paste Book kickoff prompt

```
You are the Yoga Book frontend fleet agent for Frank's estate.
Control plane docs live in agentic-ops after clone: fleet/FLEET-OPS.md, fleet/TASK-PACKETS.md, docs/DEVICE-STRATEGY.md, ops/OPS-LEDGER.md.
Machine role: frontend-innovation. Branch prefix: agent/book/<scope>.
1) Verify gh auth frankxai. 2) Run fleet_inventory + fleet_sync for yoga-book.
3) Report installed tools and repo dirty counts.
4) Take frontend-only tasks: frankx.ai UI polish, GenCreator product UI, Arcanea platform UI.
5) Do not touch Business; do not force-push; update OPS-LEDGER after work.
Execute now.
```

---

## 7. Machine failure / rebuild (quick path)

1. New Windows user / laptop  
2. Restore secrets from Infisical / password manager  
3. `gh auth login`  
4. Clone agentic-ops → `fleet_sync`  
5. Reinstall agent CLIs from CODING_AGENTS_REGISTRY  
6. Reattach Railway/Cloudflare tokens from SECRETS-REGISTRY  
7. Reinstall deps — do **not** restore random `node_modules` from backup  

---

## 8. Immediate operator priority (ordered)

1. **Install rclone** (only install gap) — command in §4  
2. **Business origin policy** — private remote vs encrypted-only  
3. **Commit agentic-ops fleet/** (dirty control plane)  
4. **Disk reclaim** to ≥80 GB with protect-list snapshot first  
5. **Weekly** `fleet_backup_check.py` on C940  
6. **Human on Book** executes Packet 4 onboard  

---

## 9. References

- Plan: `fleet/BACKUP-MIGRATION.md`  
- Ops loop: `fleet/FLEET-OPS.md`  
- Packets: `fleet/TASK-PACKETS.md`  
- Last check JSON: `fleet/last-backup-check.json`  
- Script: `scripts/fleet_backup_check.py`  
