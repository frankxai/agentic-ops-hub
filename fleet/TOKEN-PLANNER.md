# Starlight Token Planner

**Companion to Token Tracker.** Tracker answers *what did we spend?* Planner answers *which estate objective should move next, which agent should own it, under which live subscription window, and what proof must exist before it counts.*

**Owners:** Starlight Queen (C940 backend) · Command Center (Book frontend)  
**SoT files:** this doc · `objectives-registry.json` · `fleet/campaigns/` · `fleet/model-routing.json` · tracker `reports/`

---

## 1. Why this exists

| Without planner | With planner |
|-----------------|--------------|
| Spawn Claude/Codex on vibes | Objective-linked maker/verifier contract |
| Overnight burn with no ceiling | Wave budgets + live quota floors + stop conditions |
| Same model for everything | Fit model to job class and healthy subscription window |
| Tracker shows $746 Claude spike after | Planner prevents or flags mid-run |

Tracker = **accounting**. Planner = **allocation + assignment**.

---

## 2. LLM / agent assignment matrix (default estate)

| Job class | Prefer | Why | Avoid |
|-----------|--------|-----|--------|
| **Orchestration / Queen judgment** | Hermes | Objective selection, admission, routing, receipts | Treating orchestration as implementation |
| **Hard multi-file backend / TDD** | **Claude Code** (Sonnet default; Opus only if stuck) | Best long autonomous coding loops | Opus for docs |
| **Mechanical refactor / batch fix** | **Codex** (`workspace-write`) | Fast, good at local edits under Pro plan | Unsafe full-access sandbox |
| **Huge context map / repo survey** | **AGY**, after smoke test | Secondary long-context lane | Repeating timeouts instead of falling back |
| **Trivial / high-volume** | **OpenCode free models** | $0 metered | Free models for prod security |
| **Current signal / CMO research** | **Grok**, only above its quota floor | Strong current-information and creative signal | Routine routing when weekly quota is depleted |
| **Interactive UI polish** | Cursor / Book UI lane | Human-in-loop visual | Overnight unattended UI |
| **GitHub PR/issue ops** | `gh` + light model | Deterministic CLI | LLM inventing merge without gate |
| **Infra / Railway** | Queen + railway skills | Domain skill > raw LLM | Blind `railway up` overnight |

Aligned with `~/.starlight/routing.toml` and `CODING_AGENTS_REGISTRY.md`.

---

## 3. Subscription and budget envelopes

Dollar values are **API-equivalent planner targets**, not the primary control for subscription products. Every campaign also captures live remaining-percentage quota through Tokscale.

| Envelope | Day | Night (unattended) | Notes |
|----------|-----|--------------------|--------|
| **Claude Code** | $25–40 | **$35–50** | Prefer Sonnet; Opus only on named hard ticket |
| **Codex** | $20–35 | **$25–40** | Max plan — still cap runs |
| **Grok** | 10% remaining floor | 10% remaining floor | Stop and fallback below floor |
| **OpenCode free** | unlimited tokens | ok | No paid burn |
| **Fleet weekly pace** | ≤ ~€115/week (~€499/4.33) | same | Tracker budget health |

**Stop conditions (any agent):**
1. Budget flag hit (`error_budget` / cost cap)
2. Main-branch ship attempted without approval → abort
3. Disk free < 50GB → stop the launcher; 50–79GB forbids new worktree/media fanout
4. Destructive path (`rm -rf`, force-push, wipe dirty) → abort
5. Memory pressure > 85% → stop before launch
6. No healthy quota-safe route that preserves maker/verifier separation → hold

---

## 4. Campaign protocol

1. Select at most three objectives from `objectives-registry.json`; ID, repo, owner, outcome, and success metric must match the canonical entry exactly. Campaigns accept only the full `github.com/frankxai/<repo>` origin identity; an attacker-owned same-name fork is rejected for both the control repo and mission repos.
2. Create a version-3 manifest in `fleet/campaigns/` with objective, role, quota pool, repo, branch, artifacts, verification IDs, exact acceptance commands, wave budget, stop conditions, report, and portable repo-relative receipt.
3. Capture live quota; recommend a healthy configured fallback when the declared campaign agent is depleted. Before execution, commit that fallback as the manifest agent and quota pool; the runner returns `requires-manifest-reroute` rather than accepting a self-attested fallback receipt.
4. Admit only one writer per repo and require a different verifier for consequential work. The committed manifest identity is the execution identity and is excluded from verifier routing.
5. Launch only the lowest dependency-ready wave. A verifier names every maker in `depends_on`, runs later, and cannot launch after a blocked or failed maker.
6. Count only VERIFIED receipts whose agent exactly matches the committed manifest, commit is reachable from the expected branch, every required artifact is tracked and unchanged from that exact commit, and verification IDs match the manifest's exact commands. HOLD/BLOCKED/FAILED receipts may record attempted fallback diagnostics but never advance an objective.
7. Human-gated merge, deploy, spend, production, external send, and destructive actions remain held.

### Six-hour wave shape

| Wave | Duration | Required exit |
|------|----------|---------------|
| Admission | 15m | Quota, machine, heartbeat, ownership, and objective checks pass |
| Maker 1 | 90m | First implementation artifact and local tests |
| Verifier 1 | 30m | Independent verdict and bounded fixes |
| Maker 2 | 90m | Second objective artifact or integration follow-up |
| Verifier 2 | 30m | Regression and proof gate |
| Product/executive | 60m | CPO/CMO/CDO/CRO artifact tied to product proof |
| Integrator | 45m | Receipts, draft PRs or HOLD issues, objective scoreboard, handoff |

**Explicit non-goals overnight:**
- No `frankx.ai-vercel-website` ship (dirty ~427, no-ship gate)
- No Book frontend (Book lane)
- No force-push / no dirty wipe
- No domain DNS changes

---

## 5. How Queen uses this every run

```
if task is "chat/orchestrate/report" → Hermes; use a healthy CLI for durable artifacts
if task is "deep fix/TDD multi-file" → Claude Code + budget
if task is "batch refactor/local fix" → Codex + budget
if task is "map huge monorepo" → AGY/Gemini after live smoke → handoff Claude/Codex
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

# Version-3 objective campaign
python -m fleet.token_planner validate fleet/campaigns/YYYY-MM-DD-name.json
python -m fleet.token_planner status fleet/campaigns/YYYY-MM-DD-name.json
python -m fleet.night_runner fleet/campaigns/YYYY-MM-DD-name.json

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
| `fleet/campaigns/*.json` | Objective-linked wave and receipt contract |
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
