# Starlight Routing Brain (v5)

Self-improving, cost-aware model router for the Starlight sovereign agent estate.

## Files

| File | Purpose |
|---|---|
| `routing.schema.json` | Single source of truth: task classes → model chains, Token Pass pricing, cost ceilings, ZDR flags |
| `gen_omo_config.py` | Generates `~/.omo/omo.jsonc` from the schema (run after editing schema) |
| `route_classifier.py` | Classifies a task prompt into a routing class (regex fast-path + heuristic) |
| `route_executor.py` | Decision layer: model + fallback chain; atomic+locked receipt append |
| `route_task.py` | One-shot CLI: classify + route (+ optional receipt recording) |
| `weekly_routing_review.py` | Parses receipts, proposes routing diffs (human approval, never auto-commit) |

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
| scout | mimo-v2.6-flash-free | $0 | no | exploration, search, mapping |
| review | deepseek-v4.1-flash-free | $0 | no | code review, lint, style |
| bulk | vercel/deepseek/deepseek-v4.1-flash | $0.05 | yes | high-volume extraction |
| code | vercel/zai/glm-5.3 (medium) | $0.50 | yes | everyday coding, edits |
| hard-reasoning | vercel/moonshotai/kimi-k3 (high) | $2.00 | yes | complex reasoning, deep codegen |
| vision | nemotron-3.5-super-vl-free | $0 | no | multimodal analysis |
| ultrabrain | vercel/moonshotai/kimi-k3 (max) | $5.00 | yes | hardest tasks |

## Guardrails

- Free tier first; Token Pass only for bulk/code/hard-reasoning/ultrabrain.
- `--preflight --est-cost` checks the per-class ceiling and the monthly Token Pass hard cap BEFORE a call.
- Spend that already happened is always recorded: over-ceiling costs get `over_ceiling: true` (exit 3), NaN/inf/negative are rejected.
- ZDR classes (bulk, code, hard-reasoning, ultrabrain) only walk Token Pass models. Free fallbacks are excluded unless `--allow-non-zdr`, which is stamped `zdr_override` on the receipt.
- Used model must be in the (ZDR-safe) chain; off-chain models are rejected.
- Unmatched or ambiguous task text classifies to the free `scout` class; paid classes need explicit signals.
- Receipts are append-only JSONL under `receipts/routing.jsonl`, written under a cross-process lock (Windows and POSIX), LF endings. Set `STARLIGHT_RECEIPTS_DIR` to redirect (tests, dry runs); `--synthetic` marks test receipts so the weekly review ignores them.
- The weekly review skips malformed lines, needs 5 samples per compared model, and only proposes models already in the class's ZDR-safe chain.
- `gen_omo_config.py` gives every agent and category (including OmO built-ins `sisyphus-junior`, `deep-high`, `deep-low`, `artistry`) an explicit list so OmO never falls back to its own paid chains; `--dry-run`, `--out`, and a timestamped backup protect the live file. Pair it with `"enabled_providers": ["opencode", "vercel"]` in opencode.json.
- Not implemented yet: `night_cap_usd` and `soft_alert_usd` enforcement beyond the `preflight` soft-alert flag.
- Proposals require human approval; never auto-commit.

## Token Pass credit

Team: starlight-intelligence. Two keys (StarVibe c940, Starlight Yogabook), shared $80/month credit.
Soft alert at $60. Hard cap $80. No rollover, no overage (requests fail with 403).

## Doctrine

- Use commodities (OpenCode, OmO, Vercel, OpenRouter), build the moat (this).
- Done = verified. Every phase ships a runnable proof.
- Money/merges/deployments stay on the human's button.
