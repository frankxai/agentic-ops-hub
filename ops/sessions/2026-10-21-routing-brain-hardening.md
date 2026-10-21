# 2026-10-21 Routing brain hardening (brief for the opencode session)

Branch `agent/claude/routing-brain-hardening`, two commits on `hub/main` (1b2c09e):

1. `feat(fleet): routing brain baseline ...` is your seven files, verbatim, so the second commit reads as a diff.
2. `fix(fleet): harden routing brain ...` is the hardening.

Author was Claude Code. Verifier must be a different actor: run `python -m unittest tests.test_routing_brain` and read the diff. The 30 new tests fail on the baseline (10 failures, 17 errors) and pass on the fix.

## Why

An independent read-only pass over the baseline found these, each now fixed and tested:

| Defect | Fix |
|---|---|
| Receipts lost under concurrent writers on Windows (`fcntl` absent, silent unlocked append; 11-12% lost at 8 writers) | sidecar lock via `msvcrt`/`fcntl`, one binary `os.write`, LF endings |
| `--cost nan` passes the ceiling and writes `NaN` | finite/non-negative checks, `allow_nan=False` |
| Ceiling only checked after the spend, over-ceiling calls got no receipt | `--preflight --est-cost` before the call; after the call over-ceiling is recorded with `over_ceiling` (exit 3) |
| Token Pass hard cap never read | `preflight` refuses a paid model that would pass `token_pass.hard_cap_usd` for the UTC month |
| `zdr_required` never enforced, free non-ZDR fallbacks accepted | ZDR classes walk only Token Pass models; `--allow-non-zdr` is explicit and stamped `zdr_override` |
| Classifier lifted free tasks into paid classes on single words; unmatched text defaulted to paid `code` | paid classes need explicit signals; default is free `scout` |
| Weekly review crashed on torn/incomplete lines, unknown classes, NaN; local-time stamps; proposals with no sample floor or target checks | tolerant loader with skip counts, UTC, 5-sample floor per model, target must be in the ZDR-safe chain, synthetic receipts ignored |
| OmO falls back to its own paid built-in chains (`deep-high` -> `openai/gpt-6-astra`, `sisyphus-junior` -> `openai/gpt-5.6-sol`) when a slot has no list | generator emits an explicit list for every agent and category incl. `sisyphus-junior`, `deep-high`, `deep-low`, `artistry` |
| `hephaestus` on GLM throws `HephaestusRequiresGptError` | `allow_non_gpt_model: true` |
| Generator hardcoded models, no `--out`/`--dry-run`, overwrote `~/.omo/omo.jsonc` with no backup | models come from the schema chains; `--out`, `--dry-run`, timestamped backup, atomic write |

Schema change: `code` gains `vercel/deepseek/deepseek-v4.1-flash` as a ZDR-safe fallback, so a code task still has somewhere to go when GLM errors.

## Behaviour change to be aware of

ZDR classes no longer fall back to free models by default. If Token Pass is down, `code` tasks fail over to DS flash, then stop. Pass `--allow-non-zdr` to route.py / route_task.py when losing ZDR is acceptable for a task. The OmO agents that use ZDR classes (sisyphus, hephaestus, atlas, oracle, prometheus, metis) get no free fallback for the same reason.

## Applying it

1. Land this branch (draft PR, different harness signs the SHA).
2. `python fleet/gen_omo_config.py --dry-run` and diff against `~/.omo/omo.jsonc`, then run it without the flag (it backs the old file up).
3. Mark the five test receipts in the live ledger (`fleet/receipts/routing.jsonl` lines 1-5, gitignored) as synthetic, or move them aside. Add `"synthetic": true` to those lines.
4. Already done outside this branch: `"enabled_providers": ["opencode", "vercel"]` in `~/.config/opencode/opencode.json` (backup beside it). That is what closes the env-key path to openai/google/groq/openrouter.

## Not done

- `night_cap_usd` and `soft_alert_usd` enforcement beyond the `preflight` soft-alert flag.
- The registry preflight in `core/policies/portfolio-platform-architecture.v1.md` (registry SHA, governing decision) was not run: `architecture_decisions.yaml` is absent locally. This touches gateway/provider routing, so it needs doing before merge.
- `beam-free` is missing from the Oct 16 model catalog but answers headless; confirm.
- Per-agent model overrides on opencode v2.1.2 were not confirmed to apply; OmO v1 agents do not register on v2.
- `fleet/model-routing.json` is modified in the main checkout by an unrelated change and is not part of this branch.
