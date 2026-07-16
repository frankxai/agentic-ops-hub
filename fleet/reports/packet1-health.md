# Packet 1 — C940 Install & Repo Health

**Date:** 2026-07-16  
**Host:** DESKTOP-1B4ICID (c940)  
**Status:** YELLOW  
**Evidence:** `python scripts/fleet_inventory.py`, `fleet_sync.py`, `gh auth status`, live git

## Tools

| Tool | Status |
| --- | --- |
| git 2.55 | OK |
| gh 2.88 frankxai | OK |
| node 24.14 | OK |
| hermes 0.18.2 | OK |
| claude 2.1.178 | OK |
| codex / opencode / railway | Present in shell PATH (inventory script WinError false-negatives possible) |
| restic | OK |
| rclone | MISSING |
| docker | MISSING (optional) |

## Repos (manifest set)

| Repo | Branch | Dirty | Notes |
| --- | ---: | ---: | --- |
| agentic-ops | main | was 23 → fleet committed | control plane |
| claude-code-config | main | 5 | |
| FrankX | main | 111 | content SoT |
| frankx.ai-vercel-website | content-integrity-gate | **427** | PROD clone RED hygiene |
| frankx-prod-sync | main | 2 | behind origin |
| gencreator.ai | main | 1 | |
| Arcanea | integrate/... | 100 | |
| agentic-creator-os | feat/v12-open-core | 0 | GREEN |
| SIS | main | 22 | |
| Business | main | 23 | **no origin** |
| arcanea-platform | staging/... | 0 | |
| AnimeLegends.ai | rename/... | 0 | no upstream track |
| vibeclubs.ai | main | 0 | ff pulled |
| library-os | main | 1 | |
| starlight-memory | main | 9 | |
| agentic-life-os | main | 0 | |

**Summary:** 16/16 present · dirty majority · missing=0 · disk free ~67 GB

## Sync actions taken

- Safe fetch on all; ff-pull only on clean (ACOS, platform, vibeclubs, life-os)
- Dirty trees: fetch only — no reset

## Recommended next (no auto-execute)

1. Packet 6 dirty steward on prod website (427) + FrankX (111)  
2. Commit remaining agentic-ops docs (DEVICE-STRATEGY etc.) after rebase onto origin (behind 4)  
3. Business remote policy  
4. rclone install  
