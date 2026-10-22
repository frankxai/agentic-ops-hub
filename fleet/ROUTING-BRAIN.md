# Starlight Routing Brain (v5)

Self-improving, cost-aware model router for the Starlight sovereign agent estate.

## Files

| File | Purpose |
|---|---|
| `routing.schema.json` | Single source of truth: task classes → model chains, Token Pass pricing, cost ceilings, ZDR flags |
| `gen_omo_config.py` | Generates `~/.omo/omo.jsonc` from the schema (run after editing schema) |
| `route_classifier.py` | Classifies a task prompt into a routing class (regex fast-path + heuristic); its model fields come from `effective_route()` (`--allow-free` to opt in to free models) |
| `route_executor.py` | Decision layer: model + fallback chain; atomic+locked receipt append |
| `route_task.py` | One-shot CLI: classify + route (+ optional receipt recording) |
| `weekly_routing_review.py` | Parses receipts, proposes routing diffs (human approval, never auto-commit). Reviews one mode (strict by default, `--allow-free` for the opt-in mode); receipts record `allow_free`, and receipts from the other mode are filtered out and counted as `other_mode` |

## Usage

```bash
# Classify + route a task
python route_task.py "refactor the auth module and add tests"

# Record a receipt after the call completes
python route_task.py "refactor the auth module" --record success \
  --used vercel/zai/glm-5.3 --cost 0.0002 --latency 1500 --provider token-pass

# Regenerate OmO config after editing routing.schema.json
python gen_omo_config.py

# Weekly review (run via cron, Sundays 04:00)
python weekly_routing_review.py
```

## Task classes

| Class | Primary | Cost ceiling | ZDR | Use for |
|---|---|---|---|---|
| scout | mimo-v2.6-flash-free (default: cheapest ZDR model, $0.02) | $0 with `--allow-free` | no | exploration, search, mapping |
| review | deepseek-v4.1-flash-free (default: cheapest ZDR model, $0.05) | $0 with `--allow-free` | no | code review, lint, style |
| bulk | vercel/deepseek/deepseek-v4.1-flash | $0.05 | yes | high-volume extraction |
| code | vercel/zai/glm-5.3 (medium) | $0.50 | yes | everyday coding, edits |
| hard-reasoning | vercel/moonshotai/kimi-k3 (high) | $2.00 | yes | complex reasoning, deep codegen |
| vision | nemotron-3.5-super-vl-free (default: cheapest ZDR model, text-only, $0.02) | $0 with `--allow-free` | no | multimodal analysis |
| ultrabrain | vercel/moonshotai/kimi-k3 (max) | $5.00 | yes | hardest tasks |

## Guardrails

- Free routing is opt-in. By default scout, review and vision are served by the cheapest ZDR gateway model, with the explicit ceiling in the schema's `zdr_cost_ceiling_usd` for that class (scout $0.02, review $0.05, vision $0.02), so a paid call needs an estimate and is counted in the ledger. `--allow-free` (CLI) or `allow_free=True` (library: `route`, `preflight`, `reserve`, `record_receipt`, `pick_next`) keeps the free `opencode/*` models. `route_executor.effective_route()` is the one function that decides this; `route_task`, the admission checks, `record_receipt` and `gen_omo_config.py` all call it, so a model the generator writes into the OmO config is always one the executor admits.
- `--preflight --est-cost` checks the per-class ceiling and the monthly Token Pass hard cap BEFORE a call.
- Spend that already happened is always recorded: over-ceiling costs get `over_ceiling: true` (exit 3), NaN/inf/negative are rejected.
- ZDR classes (bulk, code, hard-reasoning, ultrabrain) only walk Token Pass models. Free fallbacks are excluded unless `--allow-non-zdr`, which is stamped `zdr_override` on the receipt.
- Used model must be in the (ZDR-safe) chain; off-chain models are rejected.
- Unmatched, ambiguous or unknown-word task text classifies to a paid ZDR class (`code`). Only a short request that opens with a read-only verb and uses a closed vocabulary reaches the free `scout` class; anything quoted or naming something sensitive (`.env`, key, token, secret, password and similar) goes to ZDR.
- The classifier is a cost heuristic, not a security control. The control is a Vercel gateway key that can only reach ZDR providers: when a call goes through that key, a classifier miss fails instead of leaking. The guarantee covers only calls that go through the gateway. Free `opencode/*` models run on OpenCode's own endpoint and never pass through it, which is why they are an explicit opt-in at every entry point (`--allow-free`, `--allow-free-agents`) and are for repos with nothing confidential. Without the opt-in a read-only request such as `Read notes.txt` is routed to a gateway model.
- Receipts are append-only JSONL under `receipts/routing.jsonl`, written under a cross-process lock (Windows and POSIX), LF endings. Set `STARLIGHT_RECEIPTS_DIR` to redirect (tests, dry runs); `--synthetic` marks test receipts so the weekly review ignores them.
- Each receipt carries a `pool` (`token-pass`, `free` or `other`), stamped by `record_receipt()`. Monthly Token Pass spend counts a receipt by its own pool, so removing a model from `token_pass.models` cannot erase what it already cost. Fail closed: a call that cost money is `token-pass` even for a model outside the catalog; only a zero-cost call on a free-marked model is `free`; a `pool` that is present but not one of the three known values counts as Token Pass. A legacy receipt with no `pool` counts when it cost money and its model is not explicitly free (listed under `free_tier.models` or named `*-free`).
- `effective_route()` takes `primary` from the filtered chain, never from the raw schema entry, and refuses a class whose ZDR-safe chain is empty.
- The weekly review skips malformed lines, needs 5 samples per compared model, and only proposes models already in the class's ZDR-safe chain.
- `gen_omo_config.py` gives every agent and category (including OmO built-ins `sisyphus-junior`, `deep-high`, `deep-low`, `artistry`) an explicit list so OmO never falls back to its own paid chains; `--dry-run`, `--out`, a unique backup (microsecond timestamp plus random suffix, created exclusively so an existing backup is never replaced) and a temp file owned by the invocation (so two concurrent runs never install each other's output) protect the live file. By default no slot uses an `opencode/*` free model, because those calls go to OpenCode's own endpoint, outside the gateway key. Scout, review and vision slots then run on the cheapest ZDR model in `token_pass.models` (currently `vercel/deepseek/deepseek-v4.1-flash`, about $0.75 per 1M tokens in plus out), which spends Token Pass credit, and vision falls back to a text-only model until a ZDR vision model is listed in the schema. `--allow-free-agents` restores the free models; the output header then says they sit outside the ZDR guarantee, so use it only in repos with nothing confidential. Pair it with `"enabled_providers": ["opencode", "vercel"]` in opencode.json.
- Not implemented yet: `night_cap_usd` and `soft_alert_usd` enforcement beyond the `preflight` soft-alert flag.
- Proposals require human approval; never auto-commit.

## Token Pass credit

Team: starlight-intelligence. Two keys (StarVibe c940, Starlight Yogabook), shared $80/month credit.
Soft alert at $60. Hard cap $80. No rollover, no overage (requests fail with 403).

## Doctrine

- Use commodities (OpenCode, OmO, Vercel, OpenRouter), build the moat (this).
- Done = verified. Every phase ships a runnable proof.
- Money/merges/deployments stay on the human's button.

## What the guarantee covers (and what it does not)

The classifier is a cost heuristic. The control is the gateway key: calls that go through the Vercel gateway with a ZDR-restricted key cannot reach a non-ZDR provider, whatever the classifier decided.

- **Launches under a generated config.** Unattended OpenCode runs started by `fleet/token_planner.py` (missions with `agent: "opencode"` need a `route_class`) and the live probe in `scripts/cli_capacity.py` run through `fleet/opencode_launch.py`. It resolves the model from `route_executor.effective_route()`, writes a private per-launch config directory (`opencode.json` created exclusively, removed after the run) and runs `opencode run --standalone -m <provider/model#variant>` with `OPENCODE_CONFIG_DIR` pointing at it. The config pins `model` and `small_model` to that gateway model, sets `enabled_providers` to the gateway only and `disabled_providers` to `opencode` and `omniroute`. An unknown or missing class, or missing gateway credentials, refuses to launch. With `AI_GATEWAY_API_KEY` set the file holds only an `{env:AI_GATEWAY_API_KEY}` reference; otherwise the `provider.vercel` block is copied from the user's global `opencode.json` into the temporary file for the duration of the run. `--allow-free` on either tool also enables `opencode/*`, outside the gateway key.
- **Why `--standalone` and a config directory.** Checked on opencode 2.1.2: without `--standalone` the run goes to a long-lived managed service that already holds the user's own config, and the client's environment never reaches it. With `--standalone`, `OPENCODE_CONFIG_DIR` outranks the global `opencode.json`, an `OPENCODE_CONFIG` file, `OPENCODE_CONFIG_CONTENT` and a project-level `opencode.json`; `opencode models --standalone` then lists gateway models only under each of those hostile settings. The directory replaces the global config, so global plugins (OmO) and MCP servers are not loaded in these runs. What is not verified: the effective `small_model` value could not be read back without a model call. It rests on the provider restriction and the precedence above. The variant stays inside `-m` (`provider/model#variant`) because the installed `opencode run --help` documents that format and has no `--variant` flag.
- **Not covered.** A person typing `opencode` (or any other agent CLI) directly uses their own config and model choice. That use is outside the guarantee, as is any call that does not go through the gateway.
- **Receipts.** Only `route_executor.record_receipt()` writes a routing receipt (`route_task.py --record` and library callers). The generated OmO config, the classifier and OpenCode itself record nothing.
- **Weekly review.** `weekly_routing_review.py` writes `routing-proposals/YYYY-MM-DD-strict-zdr.json` or `...-allow-free.json`, so the two modes never overwrite each other. A receipt whose `allow_free` is not a real boolean is counted as malformed and appears in neither review.
