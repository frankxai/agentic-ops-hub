# Night Mission N1 Report — agentic-ops (Queen fallback)

**When:** 2026-07-17 ~04:40 CEST  
**Branch:** `night/2026-07-17-fleet-hygiene`  
**Agent:** Hermes/Grok Queen (Claude N1 failed: **401 OAuth expired**)

## Status
- **Token Planner created:** `fleet/TOKEN-PLANNER.md` + night plan + Hermes skill `starlight-token-planner`
- **Claude subagents:** blocked until `claude auth login` / valid API credentials
- **Codex subagents:** sandbox `CreateProcessAsUserW 1312` under Hermes — relaunch with `--sandbox danger-full-access`

## Dirty tree classification (backend-critical only)

| Repo | Branch | Signal | Night action |
|------|--------|--------|--------------|
| agentic-ops | night/…-fleet-hygiene | Many untracked docs + fleet planner | **Commit planner artifacts on night branch only** |
| SIS | night/…-sis-verify | Dirty + ahead/behind remote | Verify/tests only; no integrate war |
| ACOS | night/…-acos-health | feat/v12-open-core base | Health/tests only |
| token-tracker | night/…-tracker-planner | Clean-ish + planner hooks | anomaly script |
| frankx.ai-vercel-website | (main dirty ~427) | **NO-SHIP** | Do not touch overnight |

## Backup RED remediation (rclone)

From ledger: rclone missing · disk ~61GB free · Business NO_ORIGIN.

**Morning Windows install path (operator):**
```powershell
winget install Rclone.Rclone
# or: choco install rclone
rclone version
# Then configure crypt remote per fleet/BACKUP-MIGRATION.md / b4-rclone docs
```
Do **not** run large restic until free disk ≥80GB target (currently ~61GB).

## Recommended morning PRs (if night workers finish)
1. `agentic-ops` night branch → PR: TOKEN-PLANNER + night reports only  
2. `starlight-token-tracker` night branch → PR: anomaly_check.py  
3. SIS/ACOS only if green tests  

## Explicit non-touch
- vercel prod dirty  
- force-push  
- dirty wipe  
- Railway secret rotation  

## Next
- Re-auth Claude Max OAuth  
- Relaunch Codex with `--sandbox danger-full-access`  
- Yogabook still needs `sync-reports` for fleet completeness  
