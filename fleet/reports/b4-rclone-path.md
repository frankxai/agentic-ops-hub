# B4 — rclone offsite layer (C940)

**Date:** 2026-07-16  
**Machine:** c940 / DESKTOP-1B4ICID  
**From:** Packet 2 + Command Center B4  

## Goal

Close backup RED gap: **rclone MISSING** (no offsite crypt).

## Install (operator / agent)

```powershell
winget install --id Rclone.Rclone -e --accept-package-agreements --accept-source-agreements
# new shell
rclone version
```

Or scoop/choco if preferred.

## After install (manual secrets — never commit)

```text
rclone config
# 1) remote: b2 or s3 (or other)
# 2) remote: crypt wrapping that remote
# Document remote names only in SECRETS-REGISTRY / Infisical — not git
```

## Verify loop

```bash
cd C:/Users/frank/agentic-ops
python scripts/fleet_backup_check.py
# expect rclone=True; overall may still YELLOW on disk/Business
```

## Disk note

Target free ≥80 GB. Protect-list first (Business, .ssh, hermes profiles, Infisical). No mass delete.

## Business origin

Separate decision: private remote vs encrypted-only. Not auto-created here.

## Status this session

See Swarm one-liner and `to-c940.json` results.B4 for install outcome.

## Status this session

**INSTALLED this session** via winget `Rclone.Rclone` **v1.74.4**.  
`fleet_backup_check.py` → **YELLOW** (rclone=True; disk free still under 80GB; Business no origin).

Crypt remote configuration remains **manual operator** (secrets).
