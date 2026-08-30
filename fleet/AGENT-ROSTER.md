# Agent Roster — Per-Domain Responsibilities, Tiers, Cadence, Verifier

**SoT:** `fleet/AGENT-ROSTER.md` + `fleet/model-routing.json` (machine-readable).
**Machine:** C940 control plane. Peer (Yoga Book) owns UI lanes via **git-bus** (not Hermes LAN peer).
**Last verified:** 2026-08-30 — **Grok 4.6 PRIMARY** (user correction). Codex gpt-5.6 = fallback only.

## Primary model doctrine
| Tier | Model | When |
| --- | --- | --- |
| **PRIMARY (default)** | `hermes/grok-4.6` (xai-oauth) | Orchestrate, implement, critical, Queen, research live-web |
| **FREE (non-critical)** | `opencode/hy3-free` + `omniroute/auto/best-free` | Non-prod review, best-practice, observers, docs drafts |
| **FALLBACK only** | `openai-codex/gpt-5.6-sol` (or terra) | When Grok blocked/unavailable OR different-family review after Grok implement |
| **LONG-CONTEXT only** | `gemini-3.5-flash` | Huge corpus map, not default implement |

**Never prefer Codex terra over Grok 4.6.** Prior v3 wrongly elevated terra from stale token-planner notes — corrected 2026-08-30.

## The 4 standing roles (per live domain)
| Role | Responsibility | Default tier | Verifier |
| --- | --- | --- | --- |
| **R1 Backend Lead** | Backend/product engineering, APIs, SIS/ACOS, Railway | **critical = grok-4.6** | different-family review (codex/claude) |
| **R2 Code Reviewer** | PR/branch review, security + contract gates, no auto-merge | free (hy3) non-prod; **grok-4.6** prod | tests + merge gate |
| **R3 Best-Practice Dev** | Lint/style/health-command, taste.md, register boundaries | free (hy3) | CI/health cmd |
| **R4 Research & Developer** | Lit survey, architecture research, long-context, R&D | **grok-4.6** (+ gemini long-ctx) | receipt + citation |

Every role respects: **register boundaries**, **one agent per branch**, **dirty trees are leases**, **critical actions need human approval**.

## Live domains × roles
| Domain (repo) | R1 Backend Lead | R2 Code Reviewer | R3 Best-Practice | R4 Research & Dev |
| --- | --- | --- | --- | --- |
| **frankx.ai-vercel-website** (prod) | **grok-4.6** (critical) | grok-4.6 (merge-gated) | hy3 (non-prod) | grok-4.6 live web |
| **FrankX** (content/dev) | **grok-4.6** | hy3 (free) | hy3 | grok-4.6 + gemini |
| **Arcanea** (mythic) | **grok-4.6** | hy3 | hy3 | grok-4.6 |
| **arcanea-platform** | **grok-4.6** | hy3 | hy3 | gemini long-context |
| **gencreator.ai** | **grok-4.6** (R1 bridge) | hy3 + grok-4.6 (prod gate) | hy3 | grok-4.6 |
| **AnimeLegends.ai** | **grok-4.6** | hy3 | hy3 | grok-4.6 |
| **VibeClubs.ai** | **grok-4.6** | hy3 | hy3 | grok-4.6 |
| **Starlight-Intelligence-System** (SIS) | **grok-4.6** | hy3 | hy3 | gemini long-context |
| **agentic-creator-os** (ACOS) | **grok-4.6** | hy3 | hy3 | grok-4.6 |
| **agentic-ops** (control plane) | **grok-4.6** | hy3 | hy3 | grok-4.6 |
| **starlight-token-tracker** | **grok-4.6** | hy3 | hy3 | gemini |
| **Business** (private/sensitive) | human-only | human-only | human-only | human-only |
| **satellite brands** | **grok-4.6** | hy3 | hy3 | grok-4.6 GEO |

## Profiles (Hermes model-family isolation)
- `default` (**grok-4.6**) — primary for all critical/implement/orchestrate.
- `free-tier` — `opencode/hy3-free` + rotating best-free; non-critical reviewers/observers.
- `arcanea-agent` (grok-4.6) — Arcanea mythic lane.
- `gemini-35` — long-context survey only.
- Optional `kimi-k3` / codex reviewer **after** Grok implement (different-family only).

## Yoga Book connection model (corrected 2026-08-30)
Book was **already online via the git-bus** (origin heartbeat 2026-08-16: hostname Starlight, free 151 GiB, dual ONLINE). It is **not** a Hermes LAN peer (`hermes peer list` empty is expected until optional gateway peer is added).

| Channel | Status | Purpose |
| --- | --- | --- |
| **git-bus** (`fleet/bus/heartbeats/`, queues, activity) | **canonical** | heartbeats, task queues, activity proposals |
| Telegram Swarm `@Hermesyogabookbot` | status one-liners + DM work | human + Book agent |
| Hermes `peer add` (LAN gateway) | optional | only if Book gateway URL+key shared |

Local C940 tree had dropped the Book heartbeat; restored from `origin/main` (Book-authored, not forged). Age ~14d → Book needs a **refresh pulse**, not cold Packet-4 install.

## Cadence pattern
- Observers/evals (free): every 6h
- Reviewers (free non-prod): every 6h; prod review = grok-4.6
- Best-practice (free): daily 02:30
- Research (grok-4.6): on-demand / daily
- Weekly: free-model rotator Sun 03:00; Railway Queen Mon 09:30

## Verification ladder
`CREATED → VERIFIED → DELIVERED`. Independent verifier = different family than implementer when needed.

## Gated / not yet done
1. Observability DOWN — ClickHouse 88.8% P0; Langfuse/LiteLLM/evals FAILED ~23d.
2. Bulk free-tier cron rollout across 13 domains.
3. Book HB refresh (give Book the refresh command below; last HB 2026-08-16).
