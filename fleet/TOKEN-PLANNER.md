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

## 8. Plan-limit plane — subscription allowance (the second currency)

Everything above denominates in **USD at API rates**. That is correct when a run is metered by an API key: `--max-budget-usd` is a real wall. It is the **wrong denominator for work on a Claude Max subscription**, where you do not spend dollars — you spend a **weekly allowance metered in hours of model use**, reset on a fixed per-account schedule, with a 5-hour session window on top.

**These are two different currencies. Never conflate them.** A $40 envelope says nothing about how much of the week's allowance is left; a healthy allowance says nothing about API spend. USD envelopes (§3) govern API-metered work; this plane governs subscription-metered work.

| Plane | Currency | Governs | Hard wall |
|---|---|---|---|
| USD envelopes (§3) | dollars at API rates | API-key-metered runs | `--max-budget-usd`, `--max-turns` |
| Plan-limit plane (§8) | weekly model-time allowance | Claude Max subscription runs | Anthropic's weekly + 5h session caps |

### Mechanics (verified 2026-08-28)

- Every paid plan meters two ways: a **session limit resetting every 5 hours** and a **weekly limit resetting at a fixed per-account day/time**. Read the reset from Settings → Usage and write it into `plan_limits.json:weekly_reset` (shipped value is a placeholder).
- **Opus is tracked and reset separately.** Max plans carry an all-models weekly limit plus a Sonnet-specific one; the planner tracks three buckets: `all_models`, `sonnet`, `opus` (Fable-class models are *assumed* to meter in the premium bucket — unverified).
- Published Max 20x figures — **240–480 h Sonnet, 24–40 h Opus per week** — were for the Sonnet 4 / Opus 4 generation and are **ranges: calibration priors, never contract numbers**. Actual burn varies with codebase size, message length, and history.
- Weekly limits carry a **+50% boost through 2026-08-31**, modeled as a time-bounded multiplier (`plan_limits.json:boost`), not a permanent one.
- Burn per token differs per model. Normalized to Sonnet 5 = 1.0 (output-price ratios): Haiku 0.5 · Sonnet 1.0 · Opus 2.5 · **Fable 5.0 — Fable burns 2x Opus per token**. This is the single most important routing fact once the allowance thins.
- **No public API exposes subscription usage.** The estimator reads local Claude Code session JSONL (`~/.claude/projects/**/*.jsonl`, natively — or `ccusage daily --json` as alternative input); `/usage` inside a session is the authoritative live read. Past the included limit, usage credits extend at standard API rates, capped at $2,000 redemption/day.

### Down-tier policy (`PlanLimits.advise`)

| Remaining (binding bucket) | Posture | Effect |
|---|---|---|
| > 60% | normal | honor normal routing |
| 30–60% | watch | normal routing honored; prefer cheaper tiers where quality allows |
| 10–30% | conserve | non-critical classes capped at Sonnet/Haiku; expensive tiers reserved for classes that measurably need them (`deep-backend`) |
| ≤ 10% | floor | everything except `--critical` work goes to the cheapest passing tier |

### Commands

```bash
python fleet/usage_ingest.py                          # bucket fractions + per-model burn, this week
python fleet/usage_ingest.py --advise deep-backend    # + routing recommendation for a job class
python fleet/usage_ingest.py --ccusage usage.json     # ingest `ccusage daily --json` instead of raw JSONL
```

No session data on a fresh container/machine is expected, not a bug: the CLI says so and exits non-zero.

### Executable SoT (this plane)

| Artifact | Purpose |
|----------|---------|
| `fleet/plan_limits.json` | Plan tier, reset anchor, buckets, boost, per-model weights — every number tagged provenance + confidence |
| `PlanLimits` in `fleet/token_planner.py` | Weekly/session windows, consumed-vs-remaining per bucket, down-tier advice |
| `fleet/usage_ingest.py` | Local JSONL / ccusage ingestion into allowance-equivalent consumption |

---

*Living planner — update when pricing, agents, or night policy change.*
