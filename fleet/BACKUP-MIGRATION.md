# Backup & Migration Plan — Fleet

**Date:** 2026-07-16  
**Scope:** C940 + Yoga Book + future machines  
**Principles:** 3-2-1, private-first, GitHub for code SoT, never secret dumps in public/private-by-mistake

## 1. Current posture (C940, tool-verified 2026-07-16)

| Layer | Status | Notes |
| --- | --- | --- |
| GitHub private + public remotes | Active | `gh` auth frankxai; code SoT |
| OneDrive | Present | Windows native versioning; selective sync recommended |
| Local disk free | ~67 GB / 476 GB | Post Phase-0 reclaim; target ≥80–100 GB |
| restic | Install if missing | Encrypted snapshots before risky cleanup |
| rclone | **MISSING** | Install for encrypted offsite (B2/S3) |
| Docker | **MISSING** | Optional; not required for fleet sync |

## 2. What to back up (classes)

| Class | Examples | Method | Frequency |
| --- | --- | --- | --- |
| **Code (git)** | All remotes under frankxai | GitHub + local clones | Continuous (push) |
| **Control plane** | agentic-ops, claude-code-config, .agent-harness | Git private/public + OneDrive optional | Daily push |
| **Hermes state** | profiles, config.yaml, cron jobs (not secrets raw) | Export profile tar + document; secrets in Infisical | Weekly |
| **Secrets** | API keys, .env, wallets | Infisical + SECRETS-REGISTRY; **never git** | On rotate |
| **Business / BV** | Business/ | C940 only; encrypted restic + offline | Weekly |
| **Vaults / memory** | SIS local, starlight-private-memory | Git private where appropriate + encrypted snapshot | Daily/weekly |
| **Inbox / intake** | `_inbox`, FrankX `.intake` | OneDrive or restic | Daily |
| **Machine registry** | MACHINE-ESTATE, clone-manifest, inventory JSON | Git in agentic-ops | On change |

## 3. 3-2-1 target architecture

1. **Primary:** GitHub remotes (code) + live working trees  
2. **Secondary:** OneDrive selective (docs, non-huge) + restic local snapshots (external drive/NAS if available)  
3. **Offsite:** rclone crypt → Backblaze B2 or S3 (encrypted)  

### Install gaps (C940)
```bash
# optional but recommended
winget install Rclone.Rclone
# restic: winget search restic / scoop install restic
```

## 4. Migration plans

### A. Yoga Book first-time onboard
1. Install: git, gh, Node 24 LTS, pnpm, Python 3.11+, Claude Code, Codex, Hermes (lite OK).  
2. `gh auth login` → frankxai, scopes repo/workflow.  
3. Clone control plane only first:  
   `gh repo clone frankxai/agentic-ops-hub agentic-ops`  
   (local folder name: `agentic-ops`)  
4. `cd agentic-ops && python scripts/fleet_inventory.py --machine yoga-book`  
5. `python scripts/fleet_sync.py --machine yoga-book`  
6. Set hostname hint in clone-manifest if not matching.  
7. Ledger: "Yoga Book online — role frontend".  

### B. C940 → Book selective migration (no full disk clone)
- **Do migrate via git:** control plane + shared product repos (manifest).  
- **Do not mirror:** node_modules, .next, Business secrets, full SIS heavy caches, Hermes session DBs unless needed.  
- **Do migrate configs carefully:** export Hermes profile with `hermes profile export` if Book needs same skills; re-auth OAuth on Book.  

### C. Machine failure / rebuild
1. New Windows user / laptop.  
2. Restore secrets from Infisical / password manager.  
3. `gh auth login`.  
4. Clone agentic-ops → fleet_sync.  
5. Reinstall agent CLIs from CODING_AGENTS_REGISTRY.  
6. Reattach Railway/Cloudflare tokens from SECRETS-REGISTRY.  
7. Do **not** restore random node_modules from backup — reinstall.  

### D. Future machine N
Same as Book onboard with new `machines.<id>` entry and clone subset.

## 5. Backup check automation

`scripts/fleet_backup_check.py` reports:
- gh auth  
- OneDrive path presence  
- rclone / restic presence  
- control-plane repo dirty/ahead  
- Business origin status  
- free disk  

## 6. Pre-cleanup snapshot rule

Before any dual-control disk reclaim batch:
1. `fleet_inventory.py`  
2. restic snapshot of protect list paths OR ensure remotes pushed  
3. Quarantine log under `_quarantine/YYYY-MM-DD/`  
4. Blue/Red dual-control for high-risk deletes  

Protect forever: `.ssh`, secrets, Business, SIS vaults, Hermes profiles, production SoT until dual-approved thin.

## 7. Production data vs code

| Surface | Backup owner |
| --- | --- |
| Vercel prod site | Vercel + git prod repo |
| Railway services | Railway snapshots + Infisical secrets + git |
| Domain DNS | Cloudflare (document zone export periodically) |

## 8. Immediate actions (this sprint)

- [x] clone-manifest + inventory/sync scripts  
- [ ] Run inventory + sync on C940  
- [ ] Install rclone (operator) + configure crypt remote  
- [ ] Yoga Book onboard packet executed on Book  
- [ ] Business remote policy decision (private remote vs encrypted-only)  
- [ ] Weekly backup-check cron on C940  
