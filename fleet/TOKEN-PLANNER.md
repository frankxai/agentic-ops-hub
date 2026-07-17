# Starlight Token Planner

**Companion to Token Tracker.** Tracker answers *what did we spend?* Planner answers *who should spend next, on what, with which LLM, and why — under a budget.*

**Owners:** Starlight Queen (C940 backend) · Command Center (Book frontend)  
**SoT files:** this doc · `fleet/night/` missions · `.private/subscriptions.md` (budget) · tracker `reports/`

---

## 1. Why this exists

| Without planner | With planner |
|-----------------|--------------|
| Spawn Claude/Codex on vibes | Explicit lane + model + $ cap |
| Overnight burn with no ceiling | Budget envelopes + stop conditions |
| Same model for everything | Fit model to job class |
| Tracker shows $746 Claude spike after | Planner prevents or flags mid-run |

Tracker = **accounting**. Planner = **allocation + assignment**.

---

## 2. LLM / agent assignment matrix (default estate)

| Job class | Prefer | Why | Avoid |
|-----------|--------|-----|--------|
| **Orchestration / Queen judgment** | Hermes + **Grok 4.5** (xAI Heavy) | Cheap-ish, strong ops voice, always-on | Burning Opus for chat routing |
| **Hard multi-file backend / TDD** | **Claude Code** (Sonnet default; Opus only if stuck) | Best long autonomous coding loops | Opus for docs |
| **Mechanical refactor / batch fix** | **Codex** (`exec --full-auto`) | Fast, good at local edits under Max plan | Codex for architecture doctrine |
| **Huge context map / repo survey** | **Gemini** (long-context) | 1M window | Gemini for tight style gates |
| **Trivial / high-volume** | **OpenCode free models** | $0 metered | Free models for prod security |
| **Interactive UI polish** | Cursor / Book UI lane | Human-in-loop visual | Overnight unattended UI |
| **GitHub PR/issue ops** | `gh` + light model | Deterministic CLI | LLM inventing merge without gate |
| **Infra / Railway** | Queen + railway skills | Domain skill > raw LLM | Blind `railway up` overnight |

Aligned with `~/.starlight/routing.toml` and `CODING_AGENTS_REGISTRY.md`.

---

## 3. Budget envelopes (night / day)

Values are **planner targets**, not hard API walls (except Claude `--max-budget-usd` / max-turns).

| Envelope | Day | Night (unattended) | Notes |
|----------|-----|--------------------|--------|
| **Claude Code** | $25–40 | **$35–50** | Prefer Sonnet; Opus only on named hard ticket |
| **Codex** | $20–35 | **$25–40** | Max plan — still cap runs |
| **Hermes/Grok** | continuous | continuous | Prefer for orchestration + reports |
| **OpenCode free** | unlimited tokens | ok | No paid burn |
| **Fleet weekly pace** | ≤ ~€115/week (~€499/4.33) | same | Tracker budget health |

**Stop conditions (any agent):**
1. Budget flag hit (`error_budget` / cost cap)
2. Main-branch ship attempted without approval → abort
3. Disk free < 40GB → no large installs
4. Destructive path (`rm -rf`, force-push, wipe dirty) → abort

---

## 4. Overnight protocol (C940 backend)

1. **Plan file** in `agentic-ops/fleet/night/YYYY-MM-DD.md` with missions + budgets  
2. **Branch rule:** `night/<date>-<short>` or worktree — **never commit direct to main as ship**  
3. **Assign** each mission to Claude *or* Codex with why  
4. **Launch** print/exec modes with caps (`--max-budget-usd`, `--max-turns`, codex sandbox)  
5. **Write reports** to `fleet/reports/night/`  
6. **Morning:** Queen aggregates + `token-usage hermes` + tracker weekly light  
7. **Human ships** after review  

### Default night mission mix (healthy disk ~60GB+)

| Slot | Agent | Repo | Mission class | Budget |
|------|-------|------|---------------|--------|
| N1 | Claude | `agentic-ops` | Dirty steward + fleet hygiene + rclone install plan | $40 / 25 turns |
| N2 | Codex | `Starlight-Intelligence-System` | Verify/tests + fix small failures | $30 |
| N3 | Claude | `agentic-creator-os` | Health/tests/docs hardening | $25 / 20 turns |
| N4 | Codex | `starlight-token-tracker` | Planner hooks / anomaly script | $15 |

**Explicit non-goals overnight:**
- No `frankx.ai-vercel-website` ship (dirty ~427, no-ship gate)
- No Book frontend (Book lane)
- No force-push / no dirty wipe
- No domain DNS changes

---

## 5. How Queen uses this every run

```
if task is "chat/orchestrate/report" → Hermes/Grok
if task is "deep fix/TDD multi-file" → Claude Code + budget
if task is "batch refactor/local fix" → Codex + budget
if task is "map huge monorepo" → Gemini survey → handoff Claude/Codex
if task is "cheap volume" → OpenCode free
always → log estimate in night report; next day Token Tracker measures actual
```

---

## 6. Commands

```bash
# See plan
cat ~/agentic-ops/fleet/TOKEN-PLANNER.md
cat ~/agentic-ops/fleet/night/$(date +%Y-%m-%d).md

# After night
token-usage daily
token-usage hermes
token-usage codex
# Optional: aggregate fleet
aggregate-reports
```

---

## 7. Product boundary

| System | Role |
|--------|------|
| **Token Tracker** | Measure spend (ccusage/tokscale) |
| **Token Planner** | Assign models + budgets + night missions |
| **Starlight Queen** | Execute plan, stop on safety gates |
| **ops bus** | Cross-machine tasks (not cost) |

---

*Living planner — update when pricing, agents, or night policy change.*
