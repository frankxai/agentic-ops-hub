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

### Subscription pacing and on-demand API workers

**Measured 2026-09-15:** Claude Max 20x weekly 69% used and Fable 75%, with 4 days left (about 1.8x linear pace); Codex Pro weekly 25%; Grok Build weekly 54%, expiring within a day; Copilot premium 0 of 7000 used. Fixed plan costs already exceed the EUR 499/month fleet envelope.

Policy is recorded in `fleet/model-routing.json` (version 5); existing routes and planner recommendation logic are unchanged.

1. **Expiring first:** If a subscription meter has >=30% remaining and resets within 24 hours, route all eligible work classes there first. Eligibility includes the restrictions below.
2. **Claude pacing:** Weekly target used is <=15% x days elapsed since Sunday 04:00 UTC, capped at 100% (Mon 15, Tue 30, Wed 45, Thu 60, Fri 75, Sat 90, Sun 100). Over target, Claude is only for architecture/security/long-instruction work; Fable/Opus require named tickets, and fan-out moves to Grok/Codex. At Fable >=80% used, disable Fable until reset.
3. **Codex floor:** Weekly usage should be >=10% x days elapsed in its own window. Below that floor, implement/refactor defaults to Codex, subject to expiring-first priority.
4. **On-demand API worker:** All gates must hold: every eligible subscription for the job class is >=95% used or rate-limited until after the deadline; the job is revenue- or production-critical, has a named ticket, and a deadline before reset; month-to-date spend plus the worker cap fits EUR 499. Fixed costs currently exceed that envelope, so explicit approval by Frank is required for the budget exception; all other gates and caps still apply. Run through the capped OpenRouter key only: max USD 20/job, USD 50/week, one concurrent worker, and a receipt in `fleet/reports/agents/`. Never for convenience, docs, research, or cron.

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
# Recommend the right agent/model and explain why
token-plan recommend deep-backend --complexity 8 --unattended

# Validate / inspect today's manifest
night-queen plan
night-queen commands
night-queen status
night-queen debrief

# Safety-gated launch (explicit only; dry run is default)
night-queen dry-run
night-queen launch

# After night
token-usage daily
token-usage hermes
token-usage codex
python ~/starlight-token-tracker/scripts/planner_snapshot.py
python ~/starlight-token-tracker/scripts/anomaly_check.py
```

### Executable SoT

| Artifact | Purpose |
|----------|---------|
| `fleet/model-routing.json` | Job class → agent/model/budget/why |
| `fleet/token_planner.py` | Recommend, validate, commands, status, debrief |
| `fleet/night_runner.py` | Branch/auth/disk preflight + durable run state |
| `fleet/night/YYYY-MM-DD.json` | Machine-readable mission contract |
| `~/bin/token-plan` | Planner CLI |
| `~/bin/night-queen` | Night UX wrapper |

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
