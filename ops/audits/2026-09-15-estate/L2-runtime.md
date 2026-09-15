# L2: Runtime state of local agent stack (c940 / DESKTOP-1B4ICID)
Audited 2026-09-15 ~20:40 CEST. Read-only. RAM at audit: FreeMB=4273 / TotalMB=16143 (Win32_OperatingSystem).

## 1. CLIs
| CLI | Path | Installed | Latest (source) | Auth (source) |
|---|---|---|---|---|
| claude | ~/.local/bin/claude | 2.1.272 | 2.1.272 (`npm view @anthropic-ai/claude-code`), current | loggedIn=true, claude.ai, firstParty (`claude auth status`) |
| codex | AppData/Roaming/npm/codex | 0.153.4 | 0.154.0 (`npm view @openai/codex`), 1 minor behind | "Logged in using ChatGPT" (`codex login status`) |
| grok | ~/.grok/bin/grok | 1.0.30 stable | unknown (no read-only check) | `grok auth status` unsupported; ~/.grok/auth.json exists, so likely authed (unverified) |
| hermes | AppData/Local/hermes/bin/hermes | v0.21.3 (2026.9.14), git install | unknown (update check not run) | see section 2; xAI OAuth OK (refreshed 09-15 20:40), Codex OAuth OK (refreshed 09-07), **Nous Portal: "Invalid refresh token"**, Qwen/MiniMax not logged in |
| agy (Antigravity) | AppData/Local/agy/bin/agy | 1.2.3 | unknown | ~/.gemini/antigravity state present (unverified) |
| antigravity | not on PATH | n/a | n/a | n/a |
| gemini | AppData/Roaming/npm/gemini | 0.54.4 | 0.59.0 (`npm view @google/gemini-cli`), **5 minors behind** | ~/.gemini/oauth_creds.json (Aug 12) present |
| opencode | AppData/Roaming/npm/opencode | 1.14.48 | 1.18.31 (`npm view opencode-ai`), **4 minors behind** | `opencode auth list`: 0 stored credentials; env keys OpenRouter/OpenAI/Groq |
| cursor | AppData/Local/Programs/cursor | 3.7.27 | unknown | unknown |
| node | fnm multishell | v22.13.0 | unknown (not checked) | n/a |
| npm | fnm | 10.9.2 | 12.0.2 (`npm view npm`), major behind | n/a |
| pnpm | AppData/Roaming/npm/pnpm | 10.32.1 | 12.4.2 (`npm view pnpm`), major behind (breaking) | n/a |
| python | C:/Python313 | 3.13.7 | unknown | n/a (Hermes venv uses 3.11.11) |
| git | /mingw64/bin/git | 2.55.0.windows.4 | v2.55.0.windows.5 (`gh api repos/git-for-windows/git/releases/latest`) | n/a |
| gh | Program Files/GitHub CLI | 2.88.1 (2026-03-12) | v2.101.0 (`gh api repos/cli/cli/releases/latest`), **~6 months behind** | Logged in as `frankxai` (keyring), scopes gist, read:org, repo, workflow |
| tailscale | Program Files/Tailscale | 1.102.2 | unknown | `tailscale status` shows desktop-1b4icid, arcanea (linux), starlight (windows) |
| ccusage | fnm | 20.0.20 | 20.0.20, current | n/a |
| tokscale | fnm | 4.17.0 | 4.17.0, current | n/a |

## 2. Hermes runtime + cron health
- `hermes gateway status`: login item installed (Startup\Hermes_Gateway.vbs); gateway running PID 18684.
- `hermes status`: model grok-4.6 via xAI Grok OAuth; Telegram + Slack configured. Keys shown only as masked presence.
- `hermes profile list`: **13 profiles**; only `default` has a running gateway. The brief lists 8, so the doc is out of date (new ones: free-tier, starlight-creative, starlight-growth, starlight-product, starlight-research). **Warnings:** arcanea-publishing-test, free-tier, starlight-product and starlight-research share default's Slack+Telegram bot credential. This blocks `gateway migrate --multiplex`.
- `hermes cron list`: **14 active jobs** (brief says 10, also out of date). All last runs "ok" except:
  - **e37ad751663c fleet-swarm-pulse** (0 */6): last run 2026-09-15 18:00 "ran, but the result was not delivered: Chat not found" (target telegram:-1004300203404). gateway.log shows the same error every 6h since at least 09-14 06:00, so it is ongoing, not a one-off.
  - OK: c940-always-on-host-watchdog (20:07), c940-security-sentinel-watchdog (every 10m, 20:40), c940-disk-growth-guard (20:08), c940-safe-reclaim-worker (18:07), design-workflow-drift-watch (12:05), c940-storage-movement-graph-refresh (18:05), brand-media-control-plane-watch (12:05), github-tech-radar-daily (12:07), topology-health-pulse (18:16), llm-evals-integrity-watchdog (12:07), creative-enterprise-stage0-watchdog (20:09), grok-bot-health-pulse (18:45).
  - Daily jobs scheduled for 06:15, 06:30, 07:50 and 08:00 all last ran around 12:05. They ran late, after the machine woke (it was asleep or off at the scheduled time).
- Log tails (agent.log / errors.log / gateway.log, last 3-4k lines, grep only):
  - `AttributeError: module 'asyncio' has no attribute 'start_unix_server'` at gateway/shutdown_watchdog.py:572, plus "Loop tick socket unavailable, liveness probes ... will not escalate on a stale heartbeat". This heartbeat does not work on Windows and keeps recurring (12:05, 14:18).
  - `cua-driver daemon is STALE - process alive (pid: 17444) but \\.\pipe\cua-driver` (around 15:5x). cua-driver.exe PID 17444 is still alive (tasklist, 18.5 MB).
  - MCP starlight-memory/starlight-substrate failed (CancelledError) 15:38-15:54, then **recovered**: "registered 17 tool(s) from 2 server(s)" at 17:24 and 20:40.
  - Hermes logs dir 40 MB; agent.log rotation working (4 x 5 MB).

## 3. Windows scheduled tasks outside \Microsoft\ (`Get-ScheduledTask` + `Get-ScheduledTaskInfo`)
Enabled (Ready) agent-stack tasks, all last result 0x0: Hermes-Starlight-MCP-Supervisor (every 5m, last 20:38), Hermes-Unattended-Watchdog (every 5m, 20:39), FrankXMachineMonitor (every 2h), StarlightFleetPulse (every 30m, prio 4, runs fleet_pulse.py from a **worktree path** `starlight-token-tracker\.worktrees\pulse-runtime`), StarlightAPIKeyMonitor (04:00), StarlightSecretScan (04:45), StarlightSubstrateBackup (01:15), StarlightMachineSentinel (last 09-14 07:30, next 09-16), FrankXZiggoOptimizerElevated (04:30), cua-driver-serve (logon, 12:03), Codex-Claude-Desktop-Supervisor (logon, last 09-07).

Non-zero results:
- **Git for Windows Updater**: Ready, last 2026-09-15 01:14, **0xFFFFFFFF**. Git is also 1 patch behind.
- OneDrive Per-Machine Standalone Update Task: 0x8004EE04 (vendor task, low priority).
- LenovoUtility Startup: 0x1, last run 2019 (dead vendor task). NVIDIA App SelfUpdate: 0x41303 (never ran).
- Disabled tasks with old failure codes (no action unless re-enabled): Cockpit-Periodic-Snapshot 0xC000013A, Cockpit-Shutdown-Snapshot 0xC0000142, StarlightAgentWatchdog 0x2, StarlightCrossRepoIndexer 0x1, StarlightSBReflect 0x1, StarlightClaudeRemoteControl and StarlightPortfolioAudit 0x41306, Launch Adobe CCXProcess and Opera autoupdate 0x80070002.
- About 22 disabled legacy Starlight/Cockpit/FrankX tasks add clutter.

Priority: almost all tasks run at the default priority 7. Enabled heavier ones at priority 7: StarlightSecretScan and StarlightSubstrateBackup (nightly pwsh scan/backup), FrankXMachineMonitor (pwsh every 2h). The Hermes supervisor and watchdog start wscript+pythonw every 5 minutes (2 tasks x 288 runs a day). Each run is light, but the constant process starts add up on a machine short of RAM. StarlightFleetPulse at priority 4 (below normal) is set correctly.

## 4. MCP / local services (curl -m 3 + Get-NetTCPConnection)
| Port | Service | Result |
|---|---|---|
| 127.0.0.1:8767 | Starlight MCP | **UP**: listening PID 23796; `/` 404, `/mcp` 404, `/health` 401 (auth required) |
| 127.0.0.1:27123 | Obsidian Local REST | **DOWN**: curl exit 7 (connection refused), no listener. This Claude session also got obsidian MCP ConnectionRefused. |
| 127.0.0.1:3001 | SIS Operator | **DOWN**: curl exit 7, no listener |

## 5. Claude Code harness hooks
- `~/.claude/settings.json` has **2 hooks**: SessionStart `C:/Python313/python.exe -I -B hooks/session-boot.py` (timeout 2s, 95 lines) and Stop `... hooks/session-stop.py` (timeout 2s, 26 lines). Grepping both for urllib/requests/http/subprocess/os.walk/glob/socket found **no matches**, so both fit the doctrine.
- `~/.claude/settings.local.json` has 1 hook: PostToolUse on Edit|Write|MultiEdit runs `cmd.exe /c "if exist ...\skills\impeccable\scripts\hook.mjs (node ...hook.mjs) else exit 0"` with a 5s timeout. **Minor doctrine issue:** it is user-global but uses the 5s repo budget. STOP-HOOK-DOCTRINE says "Global hook: 2 seconds; Repo hook: 5 seconds". It also cold-starts node on every edit. hook.mjs contents not inspected.
- No hooks make network calls or scan repos.

## 6. Disk
- `df -h /c`: 476G total, 454G used, **22G free (96% used)**.
- Largest regenerable or reclaimable folders under C:\Users\frank (per-folder PowerShell sums, limited to named folders):

| Size | Path | Nature |
|---|---|---|
| 10.17 GB | AppData\Roaming\Claude\vm_bundles | Claude Desktop VM bundle (re-downloads when needed) |
| 8.70 GB | AppData\Local\hermes\state.db.pre-update-emergency-2026-09-09T{14-54-47,15-01-07,16-10-36}.bak (3 x 2.90 GB) | emergency backups from 6 days ago; live state.db is 3.00 GB |
| 4.58 GB | AppData\Local\pnpm (store) | regenerable (`pnpm store prune`) |
| 4.58 GB | AppData\Local\Temp | regenerable (includes live session temp, so only prune files older than 7 days) |
| 2.21 GB | .codex | session history/logs (partly regenerable) |
| 1.16 GB | AppData\Local\Microsoft\WinGet | installer cache |
| 0.95 GB | .grok | sessions/bundled |
| 0.41 GB | AppData\Local\npm-cache | regenerable |
| 0.37 GB | AppData\Local\Package Cache | installer cache (deleting can break repair/uninstall) |
| 0.30 GB | AppData\Local\uv | regenerable |

- Missing or negligible: pip cache, ms-playwright, Cursor caches, .cache (0.01 GB), top-level node_modules (largest is .opencode at 0.09 GB). node_modules deeper than one level was not measured.
- Hermes state.db is 3 GB on its own. It could be VACUUMed, but only with the gateway stopped.

## Ranked fixes
1. **Hermes emergency DB backups take 8.7 GB on a 96%-full disk.**
   Evidence: section 6. Action: check that state.db is healthy (`hermes status` works today), keep the newest .bak (16-10-36), delete or move the other two. Impact: +5.8 to 8.7 GB disk, 0 RAM, 2 min. Autonomy: **needs Frank (destructive)**.
2. **fleet-swarm-pulse fails to deliver to Telegram every 6h ("Chat not found").**
   Evidence: section 2 cron list; gateway.log 09-14 06:00 to 09-15 18:00. The same fleet_pulse.py also runs as Windows task StarlightFleetPulse (every 30m). Action: point the job at a valid chat (`hermes cron edit e37ad751663c --deliver <target>`). The bot was likely removed from the group, or the group id changed. Or turn off one of the two duplicate pulses. Impact: stops a repeating error and halves pulse runs; 5 min. Autonomy: needs Frank to choose the chat; the edit itself is agent-safe after that.
3. **Claude Desktop vm_bundles uses 10.17 GB.**
   Evidence: section 6. Action: if Cowork/VM features are unused, remove the bundle from Claude Desktop (it re-downloads when needed). Impact: +10 GB, 15 min. Autonomy: **needs Frank (destructive, feature choice)**.
4. **Cache prune: pnpm store 4.58 GB, Temp older than 7 days, WinGet 1.16 GB, npm-cache 0.41 GB, uv 0.30 GB.**
   Evidence: section 6. Action: run one at a time: `pnpm store prune`, `npm cache clean --force`, `uv cache prune`, delete Temp files older than 7 days (skip Temp\claude), clear the WinGet cache. Impact: about 4-7 GB disk; pnpm prune is disk-heavy (~100 MB RAM); 20 min. Autonomy: agent-safe (caches rebuild), but it deletes files, so run on Frank's go. The c940-safe-reclaim-worker cron could take this on.
5. **Outdated CLIs: gh 2.88.1 -> 2.101.0, gemini 0.54.4 -> 0.59.0, opencode 1.14.48 -> 1.18.31, codex 0.153.4 -> 0.154.0, git .windows.4 -> .5 (its updater task fails with 0xFFFFFFFF).**
   Evidence: sections 1 and 3. Action: `winget upgrade GitHub.cli Git.Git`, then `npm i -g @google/gemini-cli opencode-ai @openai/codex`, one at a time. Hold pnpm 10 -> 12 and npm 10 -> 12: both are breaking major versions, and the Arcanea monorepo pins pnpm 8.15. Impact: ~300 MB download, ~10 min, ~300 MB RAM per npm install. Autonomy: agent-safe (no credentials), but outside this read-only lane.
6. **Hermes gateway liveness watchdog does not work on Windows (`asyncio.start_unix_server`).**
   Evidence: gateway.log traceback at shutdown_watchdog.py:572. Action: add a `hasattr` guard or a TCP-loopback fallback (local patch or upstream issue). Until then, the Hermes-Unattended-Watchdog task handles restarts. Impact: hangs get detected again; 0 disk. Autonomy: agent-safe as a PR; any restart needs Frank.
7. **Stale cua-driver daemon (PID 17444 alive, pipe dead).**
   Evidence: agent.log "cua-driver daemon is STALE". Action: kill PID 17444, then `schtasks /Run /TN cua-driver-serve` (the fix the log itself suggests). Impact: ~18 MB RAM; brings back the computer-use tool; 1 min. Autonomy: low risk, but it is a kill/restart, so needs Frank's go.
8. **Nous Portal auth expired ("Invalid refresh token").**
   Evidence: `hermes status`. Action: run `hermes portal` to log in again, but only if a profile uses Nous. None of the profile models do. Otherwise ignore. Autonomy: **needs Frank (login)**.
9. **Four Hermes profiles share the default bot credentials.**
   Evidence: `hermes profile list` warnings. Action: remove the Telegram/Slack tokens from arcanea-publishing-test, free-tier, starlight-product and starlight-research, or give each its own bot. Impact: unblocks the multiplex gateway and prevents two gateways reading the same bot. Autonomy: **needs Frank (credentials)**.
10. **Services down: Obsidian REST on 27123, SIS Operator on 3001.**
    Evidence: section 4, curl exit 7, no listeners. Action: start Obsidian (Local REST API plugin) when the vault MCP is needed. Start SIS Operator only when needed; RAM is too tight to autostart it. Autonomy: agent-safe to start on demand. Not a fault if they are off on purpose.
11. **Brief is out of date: says 8 profiles and 10 cron jobs; the runtime has 13 and 14.**
    Evidence: section 2. Action: update the "Hermes Runtime" section of `C:\Users\frank\.agent-harness\global-agent-brief.md`. Impact: correct routing; 5 min. Autonomy: agent-safe (doc edit).
12. **Global PostToolUse hook uses a 5s timeout (limit is 2s); scheduled tasks cluttered.**
    Evidence: section 5 (settings.local.json) and section 3 (~22 disabled legacy tasks, dead LenovoUtility task, StarlightFleetPulse running from a worktree path). Action: move the impeccable hook to repo scope or cut its timeout to 2s. After Frank reviews, delete the disabled legacy tasks. Point StarlightFleetPulse at the main checkout. Autonomy: config change needs Frank's approval; deleting tasks needs Frank (destructive).

Reclaimable total from items 1, 3 and 4: about **20-26 GB**, which would bring C: from 96% to about 91% used.
