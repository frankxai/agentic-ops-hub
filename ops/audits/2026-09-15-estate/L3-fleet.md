# L3 — Fleet, Cloud, Book, Coordination (read-only audit, 2026-09-15 ~19:00Z)

Scope: c940 (DESKTOP-1B4ICID) + yogabook (Starlight, 100.83.206.47). All data via `git fetch`/`git show`, `gh api`, `gh run`, `gh pr`. No writes to any repo. Working data in `estate-audit/L3-work/`. The scratchpad was wiped once mid-run by an outside process, and the data was rebuilt.

Note: local `C:/Users/frank/agentic-ops` has origin **frankxai/agentic-ops-hub**. A *separate* GitHub repo `frankxai/agentic-ops` also exists and holds a second bus. See section 1c.

---

## 1. Fleet bus truth

### 1a. agentic-ops-hub `origin/main` (`git show origin/main:fleet/bus/...`, head e5adc93 2026-08-24)
| Signal | Value | Age |
|---|---|---|
| heartbeats/c940.json `at` | 2026-08-25T01:27:57Z, status live | **21.7 days stale** |
| heartbeats/yoga-book.json `at` | 2026-08-16T10:45:05Z, tailscale `hold_needs_uac` | **30.4 days stale** |
| queues/to-book.json active | `BOOK-HEARTBEAT-20260825` P0, ttl 24h, status active | **TTL expired ~21 days ago** |
| to-book historical | FE1 `hold` (agent/book/r1-cta, no PR); BOOK-CLI-20260717 closed-unmerged (PR #326) | — |
| queues/to-c940.json | `active: []`; dispatch_gate `unattended_dispatch: blocked` (Book HB >24h), updated 2026-08-07 | stale gate |
| to-c940-night-2026-07-17.json | status `ready`, N1–N4 from 2026-07-17. The ledger shows the night mission ran, but the file was never closed | orphan |
| COMMAND-CENTER-DISPATCH.md | dated 2026-07-16; section A says "no Book heartbeat on bus" | outdated |

The last bus commits were 2026-08-23/24 (#49–#51). Nothing has been written to the bus for about 3 weeks, though c940 is clearly running (pulse is live, see section 2).

**PR frankxai/agentic-ops-hub#65** (`agent/c940/book-pulse-install`): OPEN, not draft, MERGEABLE, check `verify` SUCCESS, updated 2026-09-15T17:42Z. It changes only `fleet/bus/queues/to-book.json`, adding `BOOK-PULSE-INSTALL-20260915`. It is 3 ahead and 0 behind main.

**Fleet watch (off-machine dead-man switch)** `.github/workflows/fleet-watch.yml`: **40 of the last 40 scheduled runs failed** (2026-09-06 → 2026-09-15T18:30Z, 131 scheduled runs total). `gh run view --log` lists 4 signals: c940 HB stale, yoga-book HB stale, OPS-LEDGER last sweep 2026-08-10 >72h, and to-book TTL expired. Each run adds a comment to issue **#43**, which is OPEN with **130 comments**. That is alarm fatigue: the watch works, but nobody acts on its output.

### 1b. OPS-LEDGER (tail 80)
The last entry is "C940 preservation receipt 2026-09-09 v3": six preservation branches, restic snapshot b9ab528b…, "Yoga Book acceptance, off-device restore and rollback verification remain pending". The entry before that is 2026-08-10. The ledger has no Book entry since mid-July.

### 1c. Parallel buses (fragmentation, verified)
| Bus | Location | State |
|---|---|---|
| fleet/bus (canonical per FLEET-OPS) | agentic-ops-hub | stale as above |
| multi-machine/hermes-bus | **frankxai/agentic-ops** (separate repo), commit db6cef7 2026-09-01 | `observability-activate-c940` / `-yogabook` **pending since 2026-07-17**; `vacation-hardening-c940` **critical, pending since 2026-09-01**; machines.json maps bus_name↔tailnet_host↔hostname and records an unassigned `arcanea` linux node |
| swarm-bus | starlight-token-tracker `origin/main` | heartbeats/yogabook.json `ts` 2026-07-15; inbox to-c940 "Bootstrap ack" **pending**; inbox to-yogabook "Token tracker sync" **pending**; last commit 2026-07-17 |
| pulse/* branches | starlight-token-tracker | see section 2, the only live channel |

The db6cef7 commit message says it itself: "A pull-based queue with no puller is a queue that does not exist."

## 2. Pulse

`git fetch origin "+refs/heads/pulse/*:..."` and `git ls-remote origin 'refs/heads/pulse/*'` → **only `pulse/c940`** (292d81a, 2026-09-15 17:51Z). **`pulse/yogabook` does not exist.**

`python scripts/fleet_view.py --hours 24` (18:41Z):
- c940 **ok, 49m ago**. RAM 5.1/15.8 GB free, disk 23.7 GB free. Processes: antigravity x2, claude-code x2, claude-desktop x12, codex x2, grok x7, hermes x7. Today's tokens: grok 102.1M, claude 36.0M, hermes 0.8M.
- yogabook: **absent** (never pulsed).
- Quota: Claude Max 20x session 5% / weekly 69% / Fable 75%; Codex weekly 24%; Grok Build weekly 53%.
- Attribution: **Codex/Weekly +12 pts with 0.0M local tokens → UNATTRIBUTED**. Likely Codex usage on the Book or in the cloud. The Book is the obvious suspect because it doesn't pulse. (Unknown; can't be confirmed without a Book pulse.)
- The command exited with code 1 only because the chained `head PULSE.md` pointed at the repo root. `PULSE.md` exists only in the `.worktrees/pulse-runtime` worktree, which suggests the main checkout is behind the tracker's merged PR #3.

## 3. Book coding work

Method: the 25 most recently pushed non-archived repos (`gh repo list`), all branches (654), and branches matching book/yoga or agent lanes (434). Each was compared against its default branch (all repos use `main`), and open PRs were matched by head ref. A commit search (`gh search commits --owner frankxai yogabook|"yoga book"|"book queen"`) turned up only fleet/heartbeat commits, the latest Book-authored ones being agentic-ops-hub #46/#47 on 2026-08-15/16. None was coding work.

| Repo | Branch | Last commit | Ahead/Behind | Open PR | Class |
|---|---|---|---|---|---|
| frankx.ai-vercel-website | agent/book/r1-cta | 2026-07-16 | 1 / 260 | none | **stranded** (FE1 "hold") |
| frankx.ai-vercel-website | agent/book/first-100-hardening | 2026-07-17 | 1 / 251 | none (PR #326 closed unmerged) | **stranded** |
| agentic-ops-hub | agent/book/cli-max-wiring | 2026-07-17 | 4 / 31 | none | **stranded** |
| agentic-ops-hub | agent/book/online-5666907 | 2026-07-16 | 4 / 39 | none | **stranded** (likely superseded heartbeat work) |
| agentic-ops-hub | agent/book/p4-online | 2026-07-16 | 1 / 42 | none | **stranded** (likely superseded) |

**5 Book branches, all stranded, about 60 days old, 0 active, 0 merged-leftover.** Branches that mention "book" in the name but belong to other lanes (claude/codex book-content work, e.g. `codex/arcanea-cinematic-book` 28 ahead, 5d old, no PR) were excluded. Unknown: Book work that exists only locally or on branches not following `agent/book/*` can't be seen from c940.

## 4. Other agent-lane branches (same 25 repos)

419 agent-lane branches (`agent/{hermes,codex,claude,c940,gemini,antigravity,grok,book,research-fanout}/*`, `claude/*`, `codex/*`). 100 have a commit within 7 days; 119 have an open PR. **257 are stale >14 days with no open PR** (3 of them have 0 commits ahead). Two `agentic-ops` branches (`agent/claude/bridge-hardening`, `bridge-session-index`) share no common ancestor with main.

Stale branches by repo: frankx.ai-vercel-website 78/97 · FrankX 36/44 · arcanea-ai-app 35/73 · agentic-ops-hub 21/31 · starlight-agent-config 15/33 · starlight-swarm 14/16 · agentic-ops 12/23 · SIS 11/18 · starlight-agent-skills 9/10 · starlight-evals 8/10 · frankx-strategy 6/12 · arcanea-agent-skills 5/8 · others ≤3.
Stale branches by lane: claude/ 56 · codex/ 46 · agent/hermes 39 · agent/codex 39 · agent/claude 35 · agent/c940 21 · agent/gemini 8 · agent/antigravity 5 · agent/book 5 · agent/research-fanout 3.

Worst 15 (ahead>0, oldest):
1. FrankX agent/c940/ai-coe-hub-preserve-20260909: 1↑/360↓, 130d (preservation, intentional)
2. FrankX agent/c940/acos-l99-eis-preserve-20260909: 8↑/331↓, 122d (preservation)
3. FrankX agent/c940/library-os-ikigai-books-preserve-20260909: 3↑/323↓, 119d (preservation)
4. arcanea-ai-app claude/las-tierras-chapters-fix-gGgnZ: 2↑/189↓, 105d
5. arcanea-ai-app claude/chat-experience-enhancement-NJM8l: 2↑/189↓, 104d
6. arcanea-ai-app claude/ci-lighthouse-permissions: 1↑/189↓, 104d
7. arcanea-ai-app agent/claude/world-integration: 10↑/204↓, 95d
8. arcanea-ai-app agent/claude/genesis-providers: 3↑/204↓, 98d
9. arcanea-ai-app agent/claude/world-ingest: 3↑/204↓, 98d
10. arcanea-ai-app agent/claude/world-render-book: 3↑/204↓, 98d
11. arcanea-ai-app agent/claude/world-render-surface: 3↑/204↓, 98d
12. arcanea-ai-app agent/claude/world-foundation: 2↑/204↓, 98d
13. frankx.ai-vercel-website claude/multi-agent-newsletter-system-anKSZ: 4↑/536↓, 96d
14. frankx.ai-vercel-website claude/exec-hardening-ruxnO: 2↑/426↓, 97d
15. frankx.ai-vercel-website claude/newsletter-doi-revival-ruxnO: 2↑/426↓, 97d

(The `-XXXXX` suffixes are the pattern claude.ai cloud sessions use when naming branches, so many of these are orphaned cloud-routine outputs.)

## 5. Cloud agents (GitHub side)

claude.ai routines: known state is 20 routines, all disabled, last fired 2026-09-08 (not re-queried).

Workflows on the top 15 repos (133 total; latest run and schedule-run count via `actions/workflows/<id>/runs`):
- **Agent workflows:** Copilot PR reviewer (dynamic) on 8 repos, all green, last runs Jun–Aug. Copilot cloud agent: frankx.ai-vercel-website **failure** (2026-08-12); arcanea-ai-app, SIS, agentic-ops-hub, FrankX all success, all dormant since May–Jun. FrankX `Claude` (anthropic-code-agent) and `OpenAI Codex` (openai-code-agent) success, last runs 2026-06-11/12, dormant. ai-architect-academy `Claude AI Assistant` (claude.yml) success on PR 2026-09-15. arcanea-ai-app `Claude Sonnet Fix` disabled_manually, skipped.
- **Scheduled workflows and latest conclusion:**
  - agentic-ops-hub **Fleet watch**: active, **failure** (40/40), 2026-09-15
  - frankx.ai-vercel-website **intelligence-refresh**: active, **failure** (last schedule 2026-09-14, last dispatch 2026-09-15)
  - arcanea-ai-app CodeQL: active, success 2026-09-14
  - SIS Capability Foundry: active, schedule success 2026-09-14
  - FrankX Prompt Library Automation: active, **skipped** since 2026-06-11 (157 runs; the workflow is in effect dead)
  - Disabled manually after failing: arcanea-ai-app Sync arcanea-openclaw (failure 08-16), Ecosystem Weekly Refresh (failure 08-17), Claude config snapshot (success 08-20, disabled); FrankX Video Inbox Sync (1177 runs, failure 08-19)
- Other latest-run failures: arcanea-ai-app Aiyami Submission Swarm (PR, 09-12), Visual QA Gemini (disabled); gencreator.ai CI (PR, 09-15 18:44); ai-architect-academy Render Diagrams (08-21); Dependabot on frankx.ai-vercel-website (09-14) and FrankX (09-11); SIS Content drift check (06-11).
- Unknown: repos outside the top 15, and org-level Codex cloud / Jules tasks that don't show up as Actions.

---

## Ranked interconnection fixes

| # | Problem | Evidence | Proposed action | Autonomy |
|---|---|---|---|---|
| 1 | c940 is live but its bus heartbeat is 21d stale, so Fleet watch fails every run and the whole dispatch gate is closed | pulse/c940 49m fresh vs `fleet/bus/heartbeats/c940.json` at 2026-08-25; fleet-watch 40/40 failure | Have the existing StarlightFleetPulse task (or a c940 Hermes cron) also refresh `c940.json` via PR/auto-merge at most daily, or teach fleet-watch to accept `pulse/c940` freshness as the c940 liveness source | agent-safe (on c940) + Frank approval for auto-merge on the bus path |
| 2 | The Book is invisible: no pulse, bus HB 30d stale, and +12 pts of Codex quota is unattributed | `ls-remote` shows only pulse/c940; fleet_view UNATTRIBUTED Codex; yoga-book.json 2026-08-16 | Merge #65, then on the Book run `install-pulse.ps1` + `fleet_bus.py` self-heartbeat and fix the Tailscale UAC hold | needs Frank approval (merge #65) + **needs Frank physically at the Book** |
| 3 | Three competing buses, all with dead queues | fleet/bus (hub), hermes-bus (agentic-ops: 3 pending envelopes, 1 critical), swarm-bus (tracker: 2 pending since July) | Declare agentic-ops-hub `fleet/bus` + `pulse/*` canonical; freeze the other two with a README pointer; migrate the critical `vacation-hardening-c940` envelope into to-c940.json with a TTL | agent-safe (PR drafting) + Frank approval to merge/freeze |
| 4 | Alarm fatigue: issue #43 has 130 bot comments and nobody acts | `gh issue view 43` | Change fleet-watch to comment only when the signal set changes, and raise TTL-expired items as a one-line Telegram alert via Hermes | agent-safe PR + Frank approval |
| 5 | Queue hygiene: expired and orphaned items keep the watch red | to-book `BOOK-HEARTBEAT-20260825` TTL expired; to-c940-night-2026-07-17 still `ready`; dispatch_gate from 08-07; COMMAND-CENTER-DISPATCH 07-16 | Reconcile PR: move expired/finished items to historical with evidence and refresh dispatch_gate. #65 should also retire the expired item it sits next to | agent-safe PR + Frank approval |
| 6 | 5 stranded Book branches (~60d, no PR) | section 3 | Book triage: rebase-and-PR `r1-cta`/`first-100-hardening` if still wanted, otherwise tag `archive/` and delete; the hub `online`/`p4-online` ones are superseded | needs Frank approval (delete); the Book owner decides on the UI work |
| 7 | 257 stale agent branches with no PR, many orphaned cloud-session `claude/*-xxxxx` outputs | section 4 | Weekly report-only "branch janitor" (Actions or a c940 cron) posting a table; deletion only via an explicit Frank-approved list; keep `*-preserve-*` | agent-safe (report) / Frank approval (delete) |
| 8 | OPS-LEDGER cadence broken (last sweep 2026-08-10) | fleet-watch signal 3 | Re-enable the Hermes `daily-ops-sweep` append, or drop the declared daily cadence from the watch | agent-safe on c940 (verify cron) |
| 9 | Failing or dead cloud schedules | intelligence-refresh failure; Prompt Library Automation skipped for 3 months; 4 schedules disabled after failure; Copilot cloud agent failure on frankx.ai | Diagnose intelligence-refresh logs; disable or remove the dead Prompt Library schedule; decide keep/remove for the disabled ones | agent-safe diagnosis / Frank approval for changes |
| 10 | c940 disk is at 23.7 GB free, under the doctrine's "serial control mode below 50GiB" | fleet_view host line; c940.json notes | Keep serial mode; hand off to the disk lane | agent-safe |
