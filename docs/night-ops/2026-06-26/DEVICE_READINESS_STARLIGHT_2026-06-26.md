# Device Readiness Scan - STARLIGHT - 2026-06-26

Status: read-only local scan. No process cleanup, service installation,
gateway start, sync change, repo cleanup, or system configuration change was
performed.

## Verdict

Health zone: `YELLOW` for 24/7 worker expansion.

Meaning:

- Safe for command, creative review, Slack cockpit, Codex planning, light repo
  tasks, and one or two focused heavy sessions.
- Do not promote this host to broad always-on multi-agent execution until
  current process load is reduced or observed under telemetry for a full work
  cycle.
- Hermes gateway remains stopped and should stay stopped until credential,
  Slack routing, approval gates, and process health are green.

## Machine

| Field | Value |
| --- | --- |
| Hostname | `STARLIGHT` |
| OS | Microsoft Windows 11 Home |
| Version | 10.0.26200 |
| Build | 26200 |
| Last boot | 2026-06-25 13:27:51 local |
| CPU | Intel Core Ultra 7 255H |
| Cores / logical processors | 16 / 16 |
| GPU | Intel Arc 140T GPU |
| GPU driver | 32.0.101.8132 |
| RAM | 31.43 GB total, 9.5 GB free at scan time |
| Disk | C: 951.6 GB total, 473.6 GB free, 49.8 percent free |

## Tool Readiness

| Tool | Status | Notes |
| --- | --- | --- |
| Hermes | Found | `C:\Users\frank\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe` |
| Codex | Found | npm shim available |
| Claude | Found | local binary available |
| Grok | Found | local binary available |
| Git | Found | Git for Windows available |
| GitHub CLI | Found | `gh` available |
| Node | Found | available |
| Python | Found | Hermes venv Python is default in this shell |
| UV | Found | available |
| Bun | Found | available |
| Vercel CLI | Found | available |
| Railway CLI | Found | available |
| Restic | Found | available |
| Antigravity CLI | Not found as `antigravity` | wrappers are loaded in shell aliases, but direct command was not found |
| Syncthing | Not found as `syncthing` | confirm GUI/service or install path before satellite sync assumptions |
| `umwelt-scan` | Not found | use this report as a temporary read-only substitute |

## Runtime State

- Hermes profiles exist for the major portfolio lanes.
- All Hermes profile gateways are stopped.
- Hermes gateway status: not running.
- Hermes cron has an active `daily-swarm-evolution` job, but Hermes warns that
  jobs will not fire automatically while gateway is stopped.
- Hermes kanban remains 7 ready, 4 blocked, 0 running.

## Process Load Snapshot

Grouped processes at scan time:

| Process group | Count | Working set |
| --- | ---: | ---: |
| `chrome` | 24 | 2956.2 MB |
| `codex` | 10 | 2479.0 MB |
| `node` | 44 | 1521.9 MB |
| `msedgewebview2` | 23 | 533.4 MB |
| `python` | 28 | 502.9 MB |
| `Hermes` | 6 | 500.3 MB |
| `grok` | 6 | 185.9 MB |
| `node_repl` | 13 | 111.1 MB |

Interpretation: this is a busy operator workstation, not a clean always-on
worker baseline.

## Recommended Concurrency

Current safe posture:

- 0 autonomous always-on heavy workers.
- 1 to 2 new heavy coding/design sessions at a time.
- Keep Chrome/Codex/Grok/Hermes process load visible before starting more.
- Use this host as primary command and creative workstation.

Only promote toward 3 to 4 heavy sessions after:

1. Process baseline is cleaner.
2. Hermes gateway dry-run passes.
3. Slack routing and approval gates are proven.
4. Second Lenovo satellite telemetry is confirmed.
5. Syncthing exclusions are verified for `.git`, tokens, logs, sessions, caches,
   and runtime state.

## Next Safe Actions

1. Run the same readiness scan on the second Lenovo Yoga.
2. Confirm whether Syncthing is installed/running through GUI/service/path.
3. Prepare, but do not start, Hermes gateway credential/routing dry-run.
4. Prepare repo risk sweep with no cleanup or mutation.
5. Keep all profile gateways stopped until approval gates are green.

## Slack Route

Posted summary to live `#hermes-agent` channel `C0BBMKHSVAS` and refer broader
execution proof to `#execution-room`.

Channel ID check: live Slack search resolved `#hermes-agent` to `C0BBMKHSVAS`,
and canonical `C:\Users\frank\starlight\ecosystem.json` already contains that
same ID. A stale/noncanonical working-context ID was rejected by Slack as
`channel_not_found`; do not use that stale ID in future automation.
