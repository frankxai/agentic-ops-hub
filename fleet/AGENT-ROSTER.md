# Agent Roster — Per-Domain Responsibilities, Tiers, Cadence, Verifier

**SoT:** `fleet/AGENT-ROSTER.md` + `fleet/model-routing.json` (machine-readable).
**Machine:** C940 control plane. Peer (Yoga Book) owns UI lanes (offline until Packet 4).
**Last verified:** 2026-08-29 (real `hermes`/`opencode`/`codex`/`gh` state).

## The 4 standing roles (per live domain)
| Role | Responsibility | Default tier | Verifier |
| --- | --- | --- | --- |
| **R1 Backend Lead** | Backend/product engineering, APIs, SIS/ACOS primitives, Railway | critical (codex gpt-5.6) or research | different-family review |
| **R2 Code Reviewer** | PR/branch review, security + contract gates, no auto-merge | free (hy3) for non-prod; critical (grok-4.6) for prod | tests + merge gate |
| **R3 Best-Practice Dev** | Lint/style/health-command adherence, taste.md, register boundaries | free (hy3) | CI/health cmd |
| **R4 Research & Developer** | Lit survey, architecture research, long-context mapping, R&D | research (codex+gemini+grok) | receipt + citation |

Every role respects: **register boundaries** (FrankX Professional / Arcanea Mythic / SIS-ACOS Neutral), **one agent per branch**, **dirty trees are leases** (fetch-only / classify), and **critical actions need human approval**.

## Live domains × roles
| Domain (repo) | R1 Backend Lead | R2 Code Reviewer | R3 Best-Practice | R4 Research & Dev |
| --- | --- | --- | --- | --- |
| **frankx.ai-vercel-website** (prod) | codex gpt-5.6 (critical) | grok-4.6 (critical, merge-gated) | hy3 (free, non-prod branches) | grok-4.6 live web |
| **FrankX** (content/dev) | codex (research) | hy3 (free) | hy3 (free) | grok-4.6 + gemini |
| **Arcanea** (mythic) | codex (critical) | hy3 (free) | hy3 (free) | grok-4.6 |
| **arcanea-platform** | codex gpt-5.6 | hy3 | hy3 | gemini long-context |
| **gencreator.ai** | codex (critical, R1 bridge) | hy3 (free) + grok-4.6 (prod gate) | hy3 | grok-4.6 |
| **AnimeLegends.ai** | codex | hy3 | hy3 | grok-4.6 |
| **VibeClubs.ai** | codex | hy3 | hy3 | grok-4.6 |
| **Starlight-Intelligence-System** (SIS) | codex (critical) | hy3 (free) | hy3 | gemini long-context |
| **agentic-creator-os** (ACOS) | codex | hy3 | hy3 | grok-4.6 |
| **agentic-ops** (control plane) | codex | hy3 | hy3 | grok-4.6 |
| **starlight-token-tracker** | codex | hy3 | hy3 | gemini |
| **Business** (private/sensitive) | human-only | human-only | human-only | human-only (no auto-agent) |
| **satellite brands** | codex | hy3 | hy3 | grok-4.6 GEO |

## Profiles (Hermes model-family isolation)
- `default` (grok-4.6) — critical orchestration/judgment.
- `free-tier` — `opencode/hy3-free` + `omniroute/auto/best-free`; non-critical reviewers/observers. **Created 2026-08-29.**
- `arcanea-agent` (grok-4.6) — Arcanea mythic lane.
- `gemini-35` — long-context survey (Gemini 3.5 OAuth).
- Optional `kimi-k3` reviewer after live probe (adversarial, different-family).

## Cadence pattern (pilot, then bulk)
- **Observers/evals (free):** every 6h, no-agent script → opencode best-free.
- **Reviewers (free):** every 6h on non-prod branches; prod review daily 02:00 critical.
- **Best-practice (free):** daily 02:30.
- **Research & dev (research tier):** daily 03:00 or on-demand.
- **Weekly:** free-model rotator (Sun 03:00); Railway Queen (Mon 09:30, read-only).

## Verification ladder (every role)
`CREATED → VERIFIED → DELIVERED`. Report/existence alone is not done. Independent verifier = different model family than implementer.

## Gated / not yet done
1. **Observability DOWN** — ClickHouse 88.8% P0; Langfuse/LiteLLM/evals-service FAILED ~23d. "Evaluate all" currently relies on lightweight evals watchdogs + SIS tracker; repair is a separate gated action (capacity + possible redeploy cost). See `OBSERVABILITY-PLAN.md`.
2. **Bulk rollout** — roster above defines all 13 domains × 4 roles. Pilot crons prove the pattern; bulk creation (≈ one cron per role/domain) is the next approved wave (disk 44 GiB < 50 floor — keep free-tier jobs as cheap no-agent opencode scripts).
3. **Yoga Book** — UI lanes (R1 CTA UI, frontend) await Packet 4 boot.
