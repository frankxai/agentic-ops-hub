# Estate Agentic Quality & Evolution Strategy

**Status:** ACTIVE control-plane doctrine
**Owner machine:** C940 (DESKTOP-1B4ICID)
**Canonical repo:** `frankxai/agentic-ops-hub`
**Register:** Neutral (ops/fleet)
**Created:** 2026-08-18
**Authority class:** strategy + operating contract (not a merge/deploy authorization)

---

## 1. Purpose

Turn Frank’s multi-agent estate from activity-rich automation into a **verified delivery system**:

```text
detect → root-cause → bounded repair → declared gates
→ independent exact-head review → receipt → VERIFIED / DELIVERED
```

Done means **verified and delivered**, never:

- cron `ok`
- heartbeat / report / markdown theater
- draft PR
- one green check while required contexts are missing
- “implemented” without evidence or an explicit blocker

---

## 2. Current baseline (live-measured 2026-08-18)

### Control plane

| Surface | State |
|---|---|
| Hermes Agent | v0.18.2; gateway running |
| Scheduler | ~28 active jobs (LLM + script workers) |
| Native hooks | `pre_tool_call` Git safety gate + `pre_verify` E2E closure guard |
| MCP | Starlight Memory + Starlight Substrate |
| Skills | 150+ local skills |
| Profiles | 11+ operational/creative profiles |
| Coding CLIs | Claude Code, Codex, OpenCode, Gemini CLI, Agent Browser |
| Deploy/infra CLIs | Vercel, Railway, rclone, restic, Git LFS |
| Mobile | Expo / EAS present |

### Hard constraints

| Constraint | Rule |
|---|---|
| Disk free **&lt; 35 GB** | Hard floor. No reclaim roulette; containment only |
| Disk free **35–&lt;50 GB** | Control / triage / exact repair packets only. No new worktrees, installs, builds, broad scans, dirty-lane edits |
| Disk free **≥ 50 GB** | Clean owned worktrees + focused installs/checks allowed |
| Dirty / leased path | Fenced. Never second-writer |
| Public / money / secrets / DNS / destructive | Human or operation-specific acceptance chain |

### Known gaps (priority-ordered)

1. **Capacity near floor** — blocks Playwright Chromium, Docker, heavy local gates
2. **Dirty occupied trees** — prod site, FrankX, Arcanea, agentic-ops often NO-SHIP in-place
3. **Required CI not bound** on many active repos (workflows exist but are advisory)
4. **Production PR queue** — many open PRs; none merge-ready without Command Center exact-head + full required contexts
5. **User account (not Org)** — no org-wide rulesets; protections must be per-repo
6. **Design-skill drift across Hermes profiles** — estate-owned skills not forced-overwrite without reconciliation
7. **Web search backend** not fully configured for Hermes managed research in some environments
8. **Docker missing** — optional until a concrete container need + capacity headroom exist

---

## 3. Operating model

### 3.1 Autonomy contract

Lead end-to-end on routine execution. Escalate only:

- money / payments / billing changes
- law / compliance
- public production exposure / brand canon
- credentials / permission expansion
- destructive data action
- true strategic trade-offs the operator must own

### 3.2 Outcome ladder

```text
CREATED → CANDIDATE → VERIFIED → DELIVERED
```

| Label | Meaning |
|---|---|
| CREATED | Artifact exists (branch, draft, report) |
| CANDIDATE | Worker claims readiness |
| VERIFIED | Independent evaluator ≠ worker; exact-head gates green |
| DELIVERED | Merged/deployed/live-probed or durable adopted control-plane change |

### 3.3 Classification vocabulary (PR / change)

```text
NOW | REPAIR | HOLD | CLOSE-REVIEW | NOT PROVEN
```

A green bot status alone is insufficient. Drafts stay drafts unless promotion evidence is real.

### 3.4 Capacity modes

Every reasoning loop must encode:

1. Live free-space measurement
2. Worktree / lease / dirty ownership check
3. If constrained: read-only evidence + repair packet only
4. Mutations only on clean owned lanes when capacity permits

---

## 4. Control loops (non-overlapping)

| Loop | Cadence | Responsibility | Not responsible for |
|---|---|---|---|
| **Disk / host watchdogs** | minutes–hours | Changed-only capacity/security/topology alerts; safe reclaim of approved leaves | Product merges |
| **PR review swarm** | every 4h | Exact-head PR/draft triage, REPAIR packets, hold/close-review | Direct production merge |
| **Tier-1 self-heal E2E** | daily | Classified detect→repair→verify→receipt | Unclassified / public force-ship |
| **Merge Queen** | 2× daily | Integration of already-verified candidates | Inventing readiness |
| **Queen autonomy / Spring** | multi-hour | Portfolio prioritization, one material outcome per tick | Duplicate full-context scans |
| **Native hooks** | every session | Block dangerous Git shortcuts; require closure evidence | CI replacement |
| **Design drift watch** | daily | Detect profile skill drift | Blind overwrite without ownership decision |

Strengthen existing loops before inventing new frameworks.

---

## 5. GitHub governance rollout

Because `frankxai` is a **user account**, protections are per-repository.

### Tiers

| Tier | Examples | Minimum gate |
|---|---|---|
| **A — production / control** | frankx.ai-vercel-website, gencreator.ai, arcanea-ai-app, agentic-ops-hub, starlight-agent-config, ACOS, SIS-related deployables | PR required; 1 approval; dismiss stale; linear history; enforce admins; required CI job names after validation; no force-push |
| **B — public libraries / content** | design packs, content kits | validation + approval for non-trivial PRs |
| **C — experimental / dormant** | labs, drafts | block force-push/deletion; avoid stranding checks |

### Rollout sequence

1. Enforce admin + stale-review on repos that already have PR protection
2. Validate exact Actions **job names** from green runs
3. Bind only those names as required checks
4. Do **not** invent required contexts
5. Queue governance (owners, age, draft hygiene) before adding more gates that strand stacks

### Already verified improvements

- `frankxai/FrankX` main: admin enforced, 1 approval, stale dismissal, linear history
- `frankxai/arcanea` main: same

### Explicit non-goals until capacity recovers

- Playwright Chromium install
- Docker Desktop
- Bulk org migration
- Mass PR merges
- Dirty-tree auto-cleanup

---

## 6. Local quality stack (install only after ≥50 GB free)

### Phase 1 — high leverage

```bash
# Hermes browser E2E / visual proof
cd "$LOCALAPPDATA/hermes/hermes-agent"
npx playwright install chromium

# Compact Python quality tools
uv tool install ruff
uv tool install pre-commit
uv tool install pytest
```

### Phase 2 — when a concrete project needs it

- Docker / Compose
- CodeQL / Semgrep on Tier-A only
- Renovate with tight limits (no PR floods)

### Phase 3 — observability / evals

- Keep local-first receipts
- Expand LLM-eval integrity + golden tasks (Promptfoo-class)
- Optional Langfuse/Phoenix only with explicit retention/privacy policy

**Do not add** another orchestration framework (LangGraph/Crew/AutoGen) as a second home. Hermes profiles + cron + Git receipts + SIS are the substrate.

---

## 7. Elite-team workflow assets (what world-class teams keep)

| Layer | Pattern | Estate mapping |
|---|---|---|
| Source authority | Protected main, CODEOWNERS, PR templates | Per-repo protection tiers |
| Isolation | One issue → one worktree/branch/container | `agent/<machine>/<scope>` + leases |
| CI gates | lint/type/unit/integration/security/build/preview | Bind existing workflows after job-name validation |
| Independent review | Fresh-head human/bot-of-record ≠ author | Command Center exact-head + PR swarm |
| Artifact truth | version, provenance, release notes | Release receipts; no green-theater |
| E2E / visual | Playwright, a11y, mobile viewports | Install Chromium post-capacity |
| Evaluation | Golden tasks, regression, adversarial | llm-evals watchdogs + expand |
| Knowledge | Versioned runbooks + decision records | SIS + OPS-LEDGER + fleet reports |
| Security | least privilege, secrets manager, SCA | Infisical doctrine + secret-guard + sentinel |
| Human authority | Escalation matrix | Autonomy contract above |

### Reference open systems (study; do not cargo-cult install)

- Hermes Agent (Nous)
- Claude Code plugin ecosystem
- LangGraph (durable graphs — only if Hermes loops prove insufficient)
- MCP Python/TS SDKs
- Langfuse / Phoenix (eval/trace)
- pinact (pin GitHub Actions SHAs)

---

## 8. Night evolution protocol (authorized autonomous window)

When the operator authorizes overnight progress:

1. **Remeasure** disk, RAM, gateway, cron health
2. **Fence** dirty/leased trees
3. **Land durable doctrine** (this file + receipts) via clean worktree PR
4. **Apply reversible governance** (admin enforcement, stale reviews) on classified Tier-A repos
5. **Triage open PRs** with exact-head evidence; post only if materially new
6. **Pause colliding crons** whose workdir is an occupied production checkout
7. **One material verified outcome per tick**; silence on no-ops
8. **No** public force-ship, secret print, DNS, billing, Book heartbeat forge

### Acceptance for a night tick

A tick is successful only if it produces at least one of:

- merged/control-plane PR with evidence
- verified protection change
- exact repair packet with SHA/check evidence
- capacity recovery receipt
- explicit HOLD with blocker that unblocks next human decision

---

## 9. Immediate execution backlog

### P0 — tonight / next constrained window

1. Publish this strategy to `agentic-ops-hub`
2. Baseline-protect unprotected control-plane repos (`agentic-ops-hub`, `starlight-agent-config`, strengthen ACOS)
3. Keep PR swarm + self-heal active; silence no-ops
4. Reclaim only approved idle cache leaves; target ≥50 GB free
5. Hold production PR train at #456 authorization design until owner decision

### P1 — after ≥50 GB free

1. Install Playwright Chromium; smoke browser tool
2. Shared Python quality tools
3. Bind required CI job names on FrankX / ACOS / gencreator / ops-hub
4. Clean worktree repair lanes for REPAIR-class PRs only

### P2 — structural evolution

1. Reusable GitHub workflow catalog (Tier A/B/C)
2. Profile design-skill drift reconciliation with force-owned only after ownership map
3. Golden-task eval suite per critical skill/agent
4. Optional org migration decision (human) for estate-wide rulesets

---

## 10. Safety non-negotiables

- Enhance-never-erase: never mass-wipe dirty trees
- No force-push to default branches
- No direct production merge without exact-head required contexts + independent review
- No secrets in commits, receipts, or chat
- No second writer in occupied worktrees
- Cron success ≠ delivery
- Register boundaries: Neutral ops; Professional FrankX; Mythic Arcanea

---

## 11. Verification of this document’s adoption

This strategy is **adopted** only when:

1. File exists on a pushed branch/PR in `frankxai/agentic-ops-hub`
2. OPS-LEDGER / session receipt references it
3. At least one governance or automation change is executed under its rules with live evidence

Until merged to `main`, treat as **CANDIDATE doctrine on a receipt branch**.

---

## 12. Related SoTs

- `ops/OPS-LEDGER.md` — cross-repo status
- `docs/ESTATE-OPS-GOVERNANCE.md` — ops governance
- `docs/SELF-HEALING-SELF-PATCHING-UPDATING-SYSTEMS.md` (when present on branch) / self-healing skill
- `fleet/FLEET-OPS.md` — fleet operations
- `C:/Users/frank/.agent-harness/AMBITION-AND-EXCELLENCE.md` — excellence floor
- Hermes hooks: `%LOCALAPPDATA%/hermes/hooks/git_safety_gate.py`, `e2e_preverify_guard.py`
- Jobs: `tier1-self-heal-e2e`, `pr-review-swarm`, Merge Queen, disk/security watchdogs

---

**End of strategy.**
