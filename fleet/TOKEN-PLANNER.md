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

## 8. Local activity index — subscription-metered work (the second currency)

Everything above denominates in **USD at API rates**. That is correct when a run is metered by an API key: `--max-budget-usd` is a real wall. It is the **wrong denominator for work on a Claude Max subscription**, where you do not spend dollars — Anthropic meters a weekly allowance in **hours of model use**, reset on a fixed per-account schedule, with a 5-hour session window on top.

**These are two different currencies. Never conflate them.** USD envelopes (§3) govern API-metered work; this plane governs subscription-metered work.

### What this measures, and what it does not

This plane emits a **local activity index**: locally-observed session tokens, weighted per model and token kind, divided by an *estimated* capacity.

**It is not a measurement of your plan state, and nothing here may be called "remaining allowance."** Getting from local token counts to a percentage of the real plan requires an inference stack, and every layer is an assumption:

| Layer | Status |
|---|---|
| API output-price ratios → allowance burn | assumption; prices are verified, the mapping is not |
| Published hour ranges (240–480 Sonnet, 24–40 Opus) | measured on the **Sonnet 4 / Opus 4** generation; a range, not a contract |
| Per-account weekly reset anchor | **required input** — no defensible default exists |
| Fable-class → Opus bucket | assumed, unverified; check `/usage` |
| `sonnet_tokens_per_hour` calibration constant | the weakest link; unverified until derived from observations |

None of those establish how Claude Max actually meters usage. Reporting a figure like "98.6% remaining" from that chain is false precision, and acting on it can down-tier the wrong work.

### Consequences, enforced in code

- **Index rises with use.** `activity_index` of 1.0 means local activity reached the midpoint capacity *estimate*. It is not a percentage of anything real.
- **Every index carries an interval.** `activity_index_interval` comes from the width of the published hour range — a wide band, honestly reported. Each bucket also carries `is_measurement: false`.
- **The reset anchor is required input.** `weekly_window()` raises rather than guessing. Read the real value from Settings → Usage, set `weekly_reset`, and mark `confidence: "verified"`.
- **Dated facts expire.** `valid_until` on `weights`, `token_kind_multipliers`, `boost` and each bucket. Any expired fact forces the uncalibrated state — stale facts are loud, not silent.
- **Uncalibrated is advisory-only and never auto-routes.** `advise()` returns `advisory_only: true` and `auto_route: false` unless calibrated. Calibrated requires **both** a verified anchor **and** at least `minimum_observations` human `/usage` readings spanning at least one reset boundary, recorded in `calibration.observations`.

### Calibrating it

Record what `/usage` actually showed, by hand, into `calibration.observations` (schema in `plan_limits.json`). Three readings spanning a reset boundary is the floor. Until then the state is uncalibrated by definition, and that is the correct state — not a bug to work around.

### Relationship to model routing

`model-routing.json` remains the **single source of truth for model routing**. It routes across vendors and denominates in USD. This file adds no routes and overrides none; its `advice` block is a Claude-lane suggestion keyed by the same job classes, advisory until calibrated.

### Commands

```bash
python3 -m fleet.usage_ingest                          # local activity report
python3 -m fleet.usage_ingest --advise deep-backend    # + advisory suggestion
python3 -m fleet.usage_ingest --ccusage out.json       # ccusage daily --json as input
```

Exits 2 with a plain message when no session data exists — expected on a fresh container, not a bug.

| Artifact | Role |
|---|---|
| `fleet/plan_limits.json` | facts, expiries, weights, buckets, calibration observations |
| `fleet/token_planner.py` → `PlanLimits` | windows, weighting, index + interval, calibration status, advice |
| `fleet/usage_ingest.py` | reads `~/.claude/projects/**/*.jsonl` or ccusage; read-only, no network, no ClickHouse |
