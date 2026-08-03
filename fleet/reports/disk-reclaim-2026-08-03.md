# Disk reclaim receipt — 2026-08-03

**When:** 2026-08-03T16:53:50+02:00
**Host:** DESKTOP-1B4ICID (c940)

## Actions (rebuildable only)
- npm cache clean --force
- pnpm store prune (unused packages)
- Temp files older than 7 days removed (~0.37 GB)
- Rotated hermes agent/errors logs removed (~19 MB)

## Result
- Free space now: **51.02 GB**
- Status: **YELLOW** (floor 50 / target 80)
- No repos, worktrees, or active agent state deleted
- pnpm store still ~8.6 GB (active packages retained)

## Next reclaim candidates (owner review)
- Review pnpm store / unused global packages
- Packet 6 worktree retirement only with upstream-backed linked worktrees
- Larger media/caches require dual-control plan
