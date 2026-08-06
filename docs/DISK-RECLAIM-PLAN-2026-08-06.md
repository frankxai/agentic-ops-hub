# C940 Disk Reclaim Plan — 2026-08-06

**Status:** EXECUTED (safe tier) + OWNER-APPROVED pending (large tier)  
**Machine:** DESKTOP-1B4ICID (c940)  
**Measured free at plan:** ~26.2 GB  
**Floors:** hard block new heavy work &lt;35 GB · ops RED &lt;50 GB · target ≥80 GB  

## Tier A — executed automatically (rebuildable only)

| Action | Result |
| --- | --- |
| `c940_safe_reclaim.py` (npm/playwright/browser caches when idle) | ~KB–MB only; most caches already empty |
| Hermes cache files &gt;3d under `terminal/`, `images/`, research caches | ~84 files · ~0.01 GB |
| User TEMP files &gt;2d | ~1363 files · ~0.07 GB |
| Recycle Bin clear | done |

**Post Tier A free:** ~26.3 GB (still under 35 GB hard floor).

## Tier B — owner-approved before delete (high yield, not auto)

Do **not** run without explicit Frank OK. Prefer inspect size first.

| Candidate | Why / risk | Suggested command (after OK) |
| --- | --- | --- |
| Old git worktrees under `C:/Users/frank/.worktrees/*` not on active leases | Multi-GB clones | `git worktree list` then `git worktree remove` only for **linked** idle clean trees |
| `C:/Users/frank/**/node_modules` in abandoned projects | Rebuildable via pnpm/npm | Per-repo `rm -rf node_modules` only if repo idle |
| Windows hibernation / pagefile | System | `powercfg /hibernate off` only if accepted (reboot impact) |
| Docker data / WSL vhdx | If installed | `docker system prune` / compact VHDX — verify docker present first |
| OneDrive “files on demand” offline copies | Cloud recoverable | Storage Sense / OneDrive settings — not agent-deleted bulk |
| `C:/Users/frank/AppData/Local/Google/Chrome/.../Cache` | Only if Chrome fully quit | Already in safe_reclaim when chrome count=0 |
| Old `.next` / `dist` / `coverage` build artifacts | Rebuildable | Find + delete per idle repo |
| Duplicate brand-assets / large media under `brand-assets/` | May be source assets | Inventory before delete; prefer archive to external |

### Recommended owner sequence (when present)

1. Quit Chrome/Edge/Claude Desktop fully → re-run `python %LOCALAPPDATA%/hermes/scripts/c940_safe_reclaim.py`
2. `git -C C:/Users/frank/agentic-ops worktree list` → remove retired linked worktrees only
3. Scan largest home folders (Storage Sense or TreeSize) → delete **rebuildable** `node_modules` in dormant repos
4. Optional: hibernate off + reboot if &gt;10 GB pagefile win is needed
5. Re-measure: `python -c "import shutil; print(shutil.disk_usage('C:/').free/1024**3)"`

## Tier C — never auto

- `.git` histories, vaults, Hermes `auth.json`/`.env`, Business/, wallet data  
- Unclassified dirty trees  
- Production deploy artifacts without inventory  

## Policy

- Disk free &lt;35 GB → block new heavy clones, full monorepo installs, image batch pipelines  
- Content/image Hermes crons stay **HOLD** until free ≥50 GB  
- This plan does not authorize Tier B without a follow-up message listing exact paths  
