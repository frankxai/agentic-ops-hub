## Packet 1 — C940 Install & Repo Health Auditor

**Machine:** c940 (`DESKTOP-1B4ICID`)  
**Agent:** Hermes subagent (terminal/file)  
**When:** 2026-07-16 (local ~05:39–05:49)  
**Status:** **YELLOW**  
**Evidence:**
- `python scripts/fleet_inventory.py --machine c940 --json` → `fleet/last-inventory.json` (2026-07-16T03:49:09Z)
- `python scripts/fleet_sync.py --machine c940` → `fleet/last-sync.json` (2026-07-16T03:48:12Z) — **ok=16 fail=0**
- Manual `git fetch --prune origin` on all Tier-1/2 repos (no reset/merge/pull on dirty trees)
- Bash tool probe + `gh auth status`

---

### Host / disk

| Field | Value |
| --- | --- |
| Hostname | DESKTOP-1B4ICID |
| OS | Windows 11 (10.0.26200) / MSYS |
| Home | `C:\Users\frank` |
| Disk C: | 476G total · ~410G used · **~65–67G free** · **86% full** |
| Control plane | `C:\Users\frank\agentic-ops` |

Disk free is adequate for ops but tight for large clones/backups — prefer pruning + OneDrive/restic before heavy media.

---

### Tools status

Bash probe (authoritative for PATH). Inventory Python probe has false negatives on several Windows shims (`npm`/`pnpm`/`codex`/`opencode`/`railway` → `WinError 2` via subprocess).

| Tool | Status | Version / notes |
| --- | --- | --- |
| git | **OK** | 2.55.0.windows.2 |
| gh | **OK** | 2.88.1 · logged in as **frankxai** (keyring) · scopes: gist, read:org, repo, workflow |
| node | **OK** | v24.14.0 |
| npm | **OK** (bash) / ERR in inventory | 11.6.1 · `C:\Program Files\nodejs\npm` |
| pnpm | **OK** (bash) / ERR in inventory | 10.32.1 · AppData Roaming npm |
| python | **OK** | 3.13.7 |
| uv | **OK** | 0.11.28 |
| hermes | **OK** | v0.18.2 (2026.7.7.2) · local +1 carried commit |
| claude | **OK** | 2.1.178 (Claude Code) |
| codex | **OK** (bash) / ERR in inventory | codex-cli 0.139.0 |
| opencode | **OK** (bash) / ERR in inventory | 1.14.48 |
| railway | **OK** (bash) / ERR in inventory | 5.26.1 |
| restic | **OK** | 0.18.1 (windows/amd64) |
| docker | **MISSING** | optional |
| rclone | **MISSING** | optional / backup path |
| cloudflared | **MISSING** | optional |

**Flag — missing tools:** `docker`, `rclone`, `cloudflared` (optional per packet; rclone relevant for Packet 2 backup posture).  
**Flag — inventory bug:** `fleet_inventory.py` tool detection fails on npm-global CLIs under Windows; treat bash/`command -v` as SoT until fixed.

---

### Repo inventory summary

| Metric | Count |
| --- | --- |
| Manifest repos on c940 | 16 |
| Missing clones | **0** |
| Dirty trees | **11** |
| Clean trees | **5** |
| Dirty > 50 | **3** (frankx.ai-vercel-website, FrankX, Arcanea) |
| Missing remote (origin) | **1** (Business) |

---

### Key repos — branch / dirty / origin / ahead-behind (post-fetch)

Ahead/behind = local…upstream after safe `git fetch --prune`. Sync actions from `last-sync.json`.

| Repo | Branch | Dirty | Origin | Ahead | Behind | Sync action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agentic-ops | main | **24** | github.com/frankxai/agentic-ops-hub | 0 | 4 | fetch_only_dirty | Control plane; fleet/ untracked |
| claude-code-config | main | 5 | frankxai/claude-code-config | 0 | 8 | fetch_only_dirty | |
| **FrankX** | main | **111** | frankxai/FrankX | **39** | **131** | fetch_only_dirty | HOT · diverged + dirty |
| **frankx.ai-vercel-website** ⚠ PROD | agent/claude/content-integrity-gate | **427** | frankxai/frankx.ai-vercel-website | 0 | 0 | fetch_only_dirty | HOT PROD · ~417 under `public/` |
| frankx-prod-sync ⚠ PROD | main | 2 | frankxai/frankx.ai-vercel-website | 0 | **156** | fetch_only_dirty | PROD mirror stale |
| gencreator.ai ⚠ PROD | main | 1 | frankxai/gencreator.ai | 0 | **45** | fetch_only_dirty | behind after fetch |
| **Arcanea** | integrate/agent-native-main-2026-06-12 | **100** | frankxai/arcanea-ai-app | 8 | **36** | fetch_only_dirty | HOT · upstream is origin/main |
| agentic-creator-os | feat/v12-open-core | 0 | frankxai/agentic-creator-os | 0 | 0 | fetch_and_ff_pull | clean |
| Starlight-Intelligence-System | main | **22** | frankxai/Starlight-Intelligence-System | 8 | 29 | fetch_only_dirty | |
| Business | main | 23 | **NO origin** | n/a | n/a | fetch_only_dirty | local-only sensitive |
| arcanea-platform | staging/madrid-2026-05-25 | 0 | frankxai/arcanea-platform | 0 | 0 | fetch_and_ff_pull | clean; main advanced on remote |
| AnimeLegends.ai | rename/akashic-frame-drops-way-origins | 0 | frankxai/AnimeLegends | n/a | n/a | fetch_ok_pull_skipped | no upstream set |
| vibeclubs.ai | main | 0→ff | frankxai/vibeclubs | 0 | was 2 | **fetch_and_ff_pull** | fast-forwarded OK |
| library-os | main | 1 | frankxai/library-os | 0 | 2 | fetch_only_dirty | |
| starlight-memory | main | 9 | frankxai/starlight-memory | 0 | 3 | fetch_only_dirty | |
| agentic-life-os | main | 0 | frankxai/agentic-life-os | 0 | 0 | fetch_and_ff_pull | clean |

---

### Production risks (dirty / stale prod trees)

| Risk | Severity | Detail |
| --- | --- | --- |
| frankx.ai-vercel-website dirty **427** on `agent/claude/content-integrity-gate` | **RED** | Almost all churn in `public/reading/**` HTML + indexes (`data/route-index.json`, `vault-manifest`, `youtube-index`). Do **not** ship without content-integrity gate / Packet 3 + Packet 6 classification. |
| frankx-prod-sync **156 behind** main | **YELLOW→RED** | Prod mirror lagging remote main by 156 commits; 2 local dirty files block ff-pull. |
| gencreator.ai **45 behind** + 1 dirty | **YELLOW** | Bridge target for P0 R1; cannot ff while dirty. |
| FrankX **111 dirty**, **39 ahead / 131 behind** main | **YELLOW** | Diverged content/geo tree; not pure prod but feeds frankx.ai pipeline. |
| Business **no origin** | **YELLOW** | 23 untracked docs/xlsx; protect-list only local (Packet 2). |

No force push, no hard reset, no dirty wipe performed.

---

### Dirty > 50 breakdown (for Packet 6)

**frankx.ai-vercel-website (~427)**
- ~417 `public/` (mostly `public/reading/...` generated HTML)
- 3 `data/` index files
- 1 `content/`

**FrankX (~111)**
- docs 23 · scripts 19 · .claude 16 · public 12 · app 9 · components 7 · content 5 · tests/data/lib…

**Arcanea (~100)**
- apps 41 · planning-with-files 13 · packages 10 · profiles 8 · scripts 5 · wiki/docs/book…

**SIS (~22)** — memory-provider, site/motion, antigravity docs, untracked pricing/stills  
**agentic-ops (~24)** — fleet control-plane docs + scripts untracked; `ops/OPS-LEDGER.md` modified

---

### Recommended commits (names only — do not auto-commit)

1. **agentic-ops: fleet control plane** — `fleet/`, `scripts/fleet_*.py`, device/strategy docs, registries  
2. **agentic-ops: ops ledger + sessions** — `ops/OPS-LEDGER.md`, `ops/sessions/2026-07-*`  
3. **frankx.ai: content-integrity-gate batch** — classify `public/reading` generated HTML vs intentional content (likely multi-commit or discard-safe generated)  
4. **frankx.ai: data indexes** — `data/route-index.json`, `vault-manifest.json`, `youtube-index.ts`  
5. **FrankX: docs + scripts agent work** — docs/, scripts/, .claude/  
6. **FrankX: app/components product surface**  
7. **Arcanea: apps monorepo WIP** on integrate branch  
8. **Arcanea: planning-with-files + profiles**  
9. **SIS: memory-provider hardening** (+ test file)  
10. **SIS: site motion / pricing untracked**  
11. **Business: local protect-list docs** (no remote — backup only)  
12. **frankx-prod-sync: resolve 2 dirty then ff**  
13. **gencreator.ai: resolve 1 dirty then ff**  
14. **claude-code-config: local 5 dirty + pull 8 behind**  
15. **starlight-memory / library-os: small dirty then catch-up**

---

### Findings

1. **All 16 c940 clones present** — no missing remotes except Business (by design / sensitive).  
2. **Safe sync completed** — 16/16 ok; dirty trees fetch-only; clean trees ff-only where possible (`vibeclubs.ai` advanced; ACOS/platform/life-os already current).  
3. **Hot dirty confirmed:** vercel-website **427**, FrankX **111**, Arcanea **100**, SIS **22**, agentic-ops **24**, Business **23**.  
4. **Prod hygiene blockers:** content-integrity-gate dirty sprawl; prod-sync 156 behind; gencreator 45 behind.  
5. **Tools mostly healthy** for Tier-1 work; missing docker/rclone/cloudflared; restic present.  
6. **Inventory tool-probe bug** under-reports npm-global CLIs — fix later in `scripts/fleet_inventory.py` (shell=True / `where` / `cmd /c`).  
7. **Disk 86%** — watch before large media/backup jobs.  
8. **AnimeLegends** branch has no upstream tracking (fetch OK, pull skipped).  
9. First `fleet_sync` invocation timed out at 300s mid-run; a full run later wrote complete `last-sync.json` (ok=16). Manual fetches cover all Tier-1/2 regardless.

---

### Actions taken

1. Ran `fleet_inventory.py --machine c940 --json` (wrote `fleet/last-inventory.json`).  
2. Ran `fleet_sync.py --machine c940` (no force) → complete report `fleet/last-sync.json` ok=16 fail=0.  
3. Probed tools via bash + `gh auth status`.  
4. Manual safe `git fetch --prune origin` on 15 remoted repos; **no reset/merge/dirty wipe**.  
5. Sampled dirty trees for commit-name recommendations.  
6. Wrote this report to `fleet/reports/packet1-health.md`.

---

### Blocked on

- Human/Packet 6 classification before any mass clean of frankx.ai `public/reading` or FrankX/Arcanea WIP.  
- Explicit approval before prod push/main merge on frankx.ai / gencreator.  
- Operator install if rclone/docker/cloudflared needed (not blocking Tier-1 audit).  
- Business remote decision (private origin vs backup-only).

---

### Next

1. **Packet 6** — commit agentic-ops fleet control plane first; then classify frankx.ai dirty.  
2. **Packet 3** — prod targets with gate; do not ship content-integrity-gate dirty tree as-is.  
3. **Packet 2** — rclone/restic backup path; Business protect-list.  
4. Optional: fix inventory tool detection for Windows npm globals.  
5. Optional: set upstream on AnimeLegends branch or checkout main if intentional.

---

### Verify checklist

| Check | Result |
| --- | --- |
| `fleet/last-inventory.json` exists | YES |
| `fleet/last-sync.json` exists | YES (ok=16 fail=0) |
| Summary matches reality | YES — 16 repos, 0 missing, 11 dirty, 3 dirty>50 |
| No hard reset / force push / dirty delete | HONORED |
| Report path | `C:/Users/frank/agentic-ops/fleet/reports/packet1-health.md` |
