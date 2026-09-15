# L4 — AI Capacity Economics (read-only audit, 2026-09-15 ~22:00 UTC)

Scope: route agent work across flat-rate OAuth subscriptions vs metered keys to maximize output per euro. No paid API calls, no config edits, no secrets printed.

## Evidence base

| ID | Source | What it shows |
|---|---|---|
| E1 | `npx ccusage@latest daily --since 20260816 --json --by-agent` (raw: `estate-audit/raw/ccusage.json`) | 29 active days, 2.67B tokens (2.51B cache-read), **$2,249 list-price value**, local C940 logs only |
| E2 | `npx tokscale@latest usage --json` (raw: `estate-audit/raw/tokscale.json`, emails stripped) | Live plan meters (below) |
| E3 | `agentic-ops/fleet/TOKEN-PLANNER.md`, `fleet/model-routing.json` v4 (2026-08-30), `fleet/free-model-active.json` | Planner doctrine: Grok 4.6 primary; Codex fallback; free tier for low stakes; €499/mo, ≤€115/wk |
| E4 | `~/.starlight/routing.toml` | STALE: `default = "claude"`, `substrate/voice = claude`; contradicts E3 |
| E5 | `%LOCALAPPDATA%\hermes\config.yaml` (model sections) + credential *names* in `.env`/`auth.json` | primary `xai-oauth grok-4.6`; fallbacks `anthropic claude-sonnet-4-6` → `xai-oauth grok-4.5` → `openai-codex gpt-5.6-sol` (chatgpt.com backend = subscription). auth.json holds `xai-oauth`, `openai-codex`, `openai-api`; **no Anthropic credential found** (ANTHROPIC_API_KEY unset in env/HKCU/hermes .env) |
| E6 | `SIS/private/api-monitor/usage-2026-09-15.json`, `ALERTS.md` | OpenRouter $7.70 lifetime of $100 limit, $0 this month; OpenAI API key 401 (revoked) daily; Gemini key malformed (73 chars, `sk-o` prefix) → 400; Groq healthy (free) |
| E7 | `fleet/OBSERVABILITY-PLAN.md` | Railway ~$83/mo run-rate; Langfuse/LiteLLM/evals deploys failing since ~2026-08-07; ClickHouse 88.8% full |

### Live meters (E2, 2026-09-15)

| Plan | Meter | Used | Resets |
|---|---|---|---|
| Claude Max 20x | Weekly | **69%** | Sun 2026-09-20 04:00 UTC |
| Claude Max 20x | Fable | **75%** | Sun 2026-09-20 03:59 UTC |
| Claude Max 20x | 5h session | 2% | 23:30 UTC today |
| Codex Pro | Weekly | **25%** (was ~14% earlier today) | Mon 2026-09-21 20:41 UTC |
| Codex Pro | GPT-5.3-Codex-Spark 5h / weekly | 0% / 0% | — |
| Grok Build | Weekly | **54%** | **Wed 2026-09-16 17:13 UTC (~19h)** |
| Copilot Pro | Premium | **0 / 7000 used** | 2026-10-01 |

### Assumed plan prices (USD, verify on invoices)

| Plan | Assumed | Source |
|---|---|---|
| Claude Max 20x | $200/mo | https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs , https://www.aipricing.guru/compare/chatgpt-pro-vs-claude-max-20x/ |
| ChatGPT/Codex Pro | $200/mo (a $100 Pro tier also exists — check invoice) | https://www.aipricing.guru/compare/chatgpt-pro-vs-claude-max-20x/ , https://www.aipricing.guru/compare/claude-max-5x-vs-chatgpt-pro-100/ |
| xAI (Grok Build + Hermes xai-oauth) | $300/mo SuperGrok Heavy (TOKEN-PLANNER says "xAI Heavy"; tiers $10/$30/$100/$300) | https://www.codeagentswarm.com/en/guides/grok-build-pricing , https://suprmind.ai/hub/grok/pricing/ |
| GitHub Copilot Pro | $10/mo ($15 AI credits since 2026-06-01 usage-based billing) | https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/ , https://automationatlas.io/answers/github-copilot-pricing-explained-2026/ |

Subscriptions ≈ **$710/mo** + Railway $83 ≈ **$793/mo (~€730)** — already **~46% over the €499 fleet target** before any metered spend.

---

## 1. Value extracted vs plan price (last 30 days, list-price equivalent)

ccusage prices every token at API list rates; since Hermes/Codex/Grok run over OAuth, this is *value extracted*, not money billed.

| Subscription | Paths counted (E1) | 30d tokens | List value | Plan | Value ÷ price | Headroom now | Reset |
|---|---|---|---|---|---|---|---|
| xAI Heavy | hermes grok-4.6 $1,085 + hermes grok-4.5 $16 + grok CLI grok-4.6-build $46 | 956M | **$1,147** | $300 | **3.8×** | 46% weekly, expires in ~19h | 09-16 17:13 |
| Codex Pro | codex CLI $927 (gpt-5.6-sol $788, gpt-6-astra $69, gpt-5.5 $67…) + hermes gpt-5.6-sol/terra $110 | 1,619M | **$1,037** | $200 | **5.2×** | 75% weekly, 6 days left | 09-21 20:41 |
| Claude Max 20x | claude-opus-5 $62.5 + sonnet-5 $2.2 (C940 only) | 51M | **$65 (local)** | $200 | 0.3× locally; true value unknown — 69% weekly used is mostly off-C940 (claude.ai / Cowork / cloud / other laptop) | 31% weekly, 25% Fable | 09-20 04:00 |
| Copilot Pro | none | 0 | **$0** | $10 | **0×** | 100% | 10-01 |
| Antigravity / Gemini Flash | not seen by ccusage/tokscale; ~66M tokens since Sun per session facts | ~66M/wk | unmeasured | unknown (likely free / Google plan) | — | — | — |

Daily peaks (E1, list $): 08-31 **$371** (codex $205 + hermes $165, 516M tok), 08-30 $287 (hermes), 09-10 $277 (hermes), 09-01 $257, 09-09 $182, 09-04 $179 (codex). Nine days <$6. Usage is bursty: swarm days, then idle — the weekly windows are not paced.

Hermes note: `hy3-free` only 15.9M tokens in 30d — the free tier the planner prescribes for low-stakes work is barely used; low-stakes Hermes cron work is going to grok-4.6 / gpt-5.6-sol instead.

## 2. Waste and overuse risk

**Waste (paid, expiring capacity):**
- **Grok Build weekly: 46% unused expiring 2026-09-16 17:13 UTC.** Largest immediate waste; use-it-or-lose-it.
- **Codex Pro: 75% weekly headroom** with 6 days left; Codex-Spark 5h/weekly pool 0% used (a separate fast pool not in any route).
- **Copilot Pro: 7000/7000 premium unused**, and no route in `model-routing.json` references Copilot (only `routing.toml` `github-agent`). $10/mo pure waste unless given PR-review work.
- Railway **$83/mo for services that have failed to deploy since ~08-07** — ~$110 paid for zero observability.
- Idle days: 9 of 29 days near $0 → subscription windows burned in bursts, leaving unused weeks.

**Overuse risk:**
- **Claude Max: 69% weekly / 75% Fable at day 2.75 of 7 (39% elapsed) → running at ~1.8× linear pace.** Remaining 31% must last 4.25 days (~7%/day). Fable will cap first (~25% left). Root cause is off-C940 usage the local trackers can't see.
- Codex: 25% at ~day 1 of its window (14% elapsed) → also ~1.8× pace today, and the jump from 14%→25% is not in C940 logs (codex cloud / other machine). Still safe if tomorrow is normal.

## 3. Metered (per-token) paths today

| Path | Billing | Current spend | Justified? | Action |
|---|---|---|---|---|
| Hermes fallback #1 `anthropic claude-sonnet-4-6` | Would be metered Anthropic API | $0 — **no Anthropic credential found**, zero hermes Claude usage in 30d | No: it is a dead or accidental-billing first fallback, ranked *above* the two subscription fallbacks | Demote to last or remove (Frank) |
| `openai-api` entry in Hermes auth.json + `OPENAI_API_KEY` env | Metered OpenAI | $0 — key returns 401 daily (E6) | No — dead | Remove stale reference / rotate only if needed (Frank) |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Metered/free Google | $0 — malformed (OpenRouter-style key in Gemini slot) → 400 | No — misconfig, blinds monitor | Fix variable (Frank, credential) |
| OpenRouter key | Prepaid, $100 limit | $7.70 lifetime, $0 month | Yes as capped overflow worker rail | Keep; it is the natural on-demand API envelope |
| Groq key | Free tier | $0 | Yes (free scratch) | Keep |
| Railway (Langfuse/LiteLLM/ClickHouse/evals) | Metered infra | **~$83/mo** | **No** while deploys fail | Pause or fix under one decision (Frank) |
| Copilot overage ($0.04/req after credits) | Metered past pool | $0 | n/a | Keep overage disabled |

**Current metered AI spend ≈ $0/mo; metered infra ≈ $83/mo.** All $2,249 of agent value rode subscriptions.

## 4. Routing policy

Reconciled with `model-routing.json` v4 (Grok primary, Codex fallback, free for low stakes). Change vs doctrine: Codex is promoted from "fallback-only" to **co-primary for implement/refactor** because it has 5.2× value/price and the most headroom; Claude is reserved for the scarce seat.

| Job class | First choice | Overflow | Never use |
|---|---|---|---|
| Orchestration / Queen judgment / reports | Hermes `xai-oauth grok-4.6` | `openai-codex gpt-5.6-sol` | Claude Opus/Fable; metered Anthropic |
| Implement / refactor / batch fix / tests | Codex Pro (`gpt-5.6-sol`; Codex-Spark for fast mechanical) | Grok Build / hermes grok-4.6 | Fable; free models on prod |
| Swarm fan-out / parallel lanes | Grok Build (native subagents) | Codex exec | Claude subagent fan-out while weekly >pace |
| Substrate architecture / security / long instruction (the scarce seat) | Claude Max (Sonnet default, Opus/Fable named-ticket only) | Codex gpt-6-astra/gpt-5.6-sol as different-family | Grok-only for security sign-off |
| Different-family review of PRs | **Copilot Pro** (premium pool) or Codex | Claude Sonnet | same family as implementer |
| Long-context repo survey | Antigravity/Gemini Flash | Grok 4.6 | Claude 1M context for mere mapping |
| Low-stakes volume (lint, docs, summaries, observers, cron) | opencode `hy3-free` / `omniroute/auto/best-free`, Groq | Hermes grok-4.6 | any paid model for no-agent observers |
| Deterministic repo ops | `gh` CLI | — | LLM |

**Five routing rules**
1. **Expiring-first:** before choosing a model, prefer the subscription whose window resets soonest with the most unused %: if a meter has ≥30% left within 24h of reset, route all eligible work there (today: Grok Build).
2. **Pace gate for Claude/Fable:** target weekly used ≤ 15% × days-elapsed (Sun 04:00 UTC start): Mon 15, Tue 30, Wed 45, Thu 60, Fri 75, Sat 90, Sun 100. Over target → Claude only for the scarce-seat class; Fable/Opus only on named tickets; fan-out moves to Grok/Codex. Fable ≥ 80% → Fable off until reset.
3. **Codex floor:** Codex weekly should be ≥ 10% × days-elapsed in its window; below floor, implement/refactor defaults to Codex even over Grok.
4. **Free before paid for low stakes:** anything in `tiers.free.use_for` must hit hy3-free/best-free first; paid models only on free failure, logged.
5. **On-demand API worker trigger (all must hold):** (a) every eligible subscription for the job class is ≥95% or rate-limited until after the deadline; (b) job is revenue- or prod-critical with a named ticket and a deadline before the reset; (c) month-to-date fleet spend + worker cap ≤ €499 envelope (currently exceeded by fixed costs → requires Frank's explicit OK); (d) worker runs through the capped OpenRouter key with `--max-budget-usd` ≤ $20/job and ≤ $50/week, one concurrent worker, receipt to `fleet/reports/agents/`. Never trigger for convenience, docs, research or cron.

## 5. Concrete config changes

| # | Change | File | Autonomy |
|---|---|---|---|
| C1 | Add `pacing` block (Claude 15%/day targets, Fable cap 80%, Codex floor 10%/day, expiring-first rule) and `on_demand_api_worker` block (trigger conditions, OpenRouter rail, $20/job, $50/wk, 1 concurrent) | `agentic-ops/fleet/model-routing.json` (v5) + §3/§5 of `fleet/TOKEN-PLANNER.md` | **agent-safe** (doc/routing, PR on branch) |
| C2 | Promote Codex to co-primary for `implement`/`refactor` routes; add `review` route → Copilot; add Codex-Spark for mechanical | `fleet/model-routing.json` routes + `docs/CODING_AGENTS_REGISTRY.md` roles | **agent-safe** but reverses 2026-08-30 user correction → needs Frank's nod |
| C3 | Reorder Hermes fallbacks to `xai-oauth grok-4.5` → `openai-codex gpt-5.6-sol` → (remove or last) `anthropic claude-sonnet-4-6`; point low-stakes Hermes crons at `hy3-free` | `%LOCALAPPDATA%\hermes\config.yaml` | **needs Frank** (live runtime config; touches paid-API path) |
| C4 | Sync stale `default = "claude"` → `hermes`/grok; `refactor = codex` stays; add `review = copilot` | `~/.starlight/routing.toml` | **agent-safe** (reversible), confirm consumer `orchestrator_router.py` |
| C5 | Feed tokscale meters into planner: `token_planner.py recommend` reads `tokscale usage --json` and applies rules 1–3; morning brief prints pace vs target | `fleet/token_planner.py`, `starlight-token-tracker/scripts/planner_snapshot.py` | **agent-safe** (read-only telemetry; run in command/cron, not a hook, per STOP-HOOK-DOCTRINE) |
| C6 | Railway: pause Langfuse/LiteLLM/evals/ClickHouse or fix in one gated session; stop paying $83/mo for failed deploys | Railway project | **needs Frank** (money) |
| C7 | Clean dead metered credentials: remove `openai-api` from Hermes auth, fix malformed `GEMINI_API_KEY`, decide on revoked `OPENAI_API_KEY` | env / `~/.secrets/.env.master` / hermes auth.json | **needs Frank** (credentials) |
| C8 | Plan right-sizing review: if Claude weekly stays mostly off-C940 and Copilot stays 0, consider dropping Copilot ($10) and verifying xAI tier (Heavy $300 vs Plus $100 at 3.8× value) | billing | **needs Frank** (plan change) |
| C9 | Add Claude off-machine visibility (claude.ai/Cowork/other laptop) to token tracker, since 69% weekly is unexplained locally | `starlight-token-tracker` | **agent-safe** design; data access may need Frank |

### Immediate (next 19h, agent-safe)
Queue bounded, already-approved Grok Build lanes (repo surveys, test-fix swarms on non-prod branches) before 2026-09-16 17:13 UTC; keep Claude to this audit's architect lane only.

### Caveats
- List-price "value" assumes the work would otherwise be bought at API rates; cache-read tokens (94% of volume) inflate it.
- Plan prices are public list prices, USD; invoices, VAT and EUR conversion not checked.
- Antigravity/Gemini and off-C940 Claude/Codex usage are not in E1.
