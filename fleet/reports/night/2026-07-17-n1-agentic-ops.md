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

**Morning Windows rclone install path (operator):**
1. Open a new PowerShell window. If `winget` is unavailable, install or update **App Installer** from Microsoft Store first.
   ```powershell
   winget install Rclone.Rclone
   ```
2. Close and reopen PowerShell so the newly installed `rclone` is on `PATH`, then verify the binary:
  ```powershell
  rclone version
  Get-Command rclone
  ```
3. If `winget` is not available, use Chocolatey from an elevated PowerShell instead:
  ```powershell
  choco install rclone
  ```
4. Configure the approved remote and crypt layer only from the documented migration/operator instructions:
  ```powershell
  rclone config
  rclone listremotes
  ```
   Use `fleet/BACKUP-MIGRATION.md` and the `fleet/reports/b4-rclone*.md` notes; do not paste credentials into this report or the repository.
5. Confirm the crypt remote is readable with a small, non-destructive listing before starting any backup. Do **not** run a large restic job until the free-disk threshold below is met.

Do **not** run large restic until free disk ≥80GB target (currently ~61GB).

## Recommended morning PRs (if night workers finish)
1. `agentic-ops` night branch → PR: TOKEN-PLANNER + night reports only  
2. `starlight-token-tracker` night branch → PR: anomaly_check.py  
3. SIS/ACOS only if green tests  

## Morning PR checklist — agentic-ops
- [ ] Confirm the source branch is `night/2026-07-17-fleet-hygiene`; do not merge or push directly to `main`.
- [ ] Review `git status --short` and include only `fleet/TOKEN-PLANNER.md` and `fleet/reports/night/*` in the PR/commit.
- [ ] Confirm no unrelated dirty files, generated raw artifacts, credentials, or local state are staged.
- [ ] Read the final diff and ensure it contains the token-planner/night-report scope only.
- [ ] Run the relevant lightweight documentation or repository checks, and record any check that could not run.
- [ ] Push the night branch normally; never force-push.
- [ ] Open a PR to `main` with a concise summary, verification results, and the remaining backup constraints: rclone configuration and ≥80GB free disk.
- [ ] Before merge, confirm required CI/review checks are green and the PR has no out-of-scope files.

## Explicit non-touch
- vercel prod dirty  
- force-push  
- dirty wipe  
- Railway secret rotation  

## Next
- Re-auth Claude Max OAuth  
- Relaunch Codex with `--sandbox danger-full-access`  
- Yogabook still needs `sync-reports` for fleet completeness  
