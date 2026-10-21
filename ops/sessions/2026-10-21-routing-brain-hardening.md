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

## Codex round 1 (reviewed SHA 69194f0): CHANGES REQUESTED, fixed in the next commit

Codex ran the 30 tests green, then broke the design with six findings. Each now has a failing-first test in `tests/test_routing_brain.py` (48 tests total).

| Finding | Fix |
|---|---|
| P1 singleton ZDR chain left `fallback_models` off, so `bulk-extraction` inherited `sisyphus-junior`'s free fallbacks (OmO checks truthiness, `[]` is truthy) | every category now emits `fallback_models`, empty when the ZDR-safe chain has one model; exact-slot-set test |
| P1 classifier tested vision/review before code, so `fix the screenshot upload bug` went to free non-ZDR vision | all ZDR classes are tested before vision and review; test asserts coding phrasings never land in a non-ZDR class |
| P1 preflight held nothing, two callers could pass the cap together | `reserve()` checks and writes a hold in one locked step (`reservations.jsonl`); `record_receipt(reservation_id=)` settles it; holds expire after 30 min; 6 concurrent processes against 1.0 USD headroom admit exactly 2 |
| P1 each worktree defaulted to its own `receipts/`, ignoring `schema.receipts.root` | `receipts_dir()` = `STARLIGHT_RECEIPTS_DIR`, else `schema.receipts.root`, else the checkout only when the root is not an absolute path on this OS |
| P2 missing `--est-cost` defaulted to 0 and admitted paid calls at the cap | paid models need an explicit estimate above zero; paid admission is refused once spend plus holds reach the cap; free models may omit it |
| P2 `"task_class":[]` crashed the weekly review | loader counts wrongly-typed `task_class`, `used`, `ts`, `success` as malformed; `analyze` guards too |

CLI: `--preflight` now reserves and prints `reservation_id`; pass it to `--record --reservation <id>`. `--no-reserve` checks without holding. Exit codes unchanged (0, 2, 3).

Test coverage gap Codex named (removing `oracle` still passed) is closed: the generated agent and category sets are compared for equality with the expected OmO slots.

Caveat: the schema root is `C:/Users/frank/agentic-ops/fleet/receipts`, so on this machine every worktree now writes the live ledger. Other machines (Railway worker) resolve to their own checkout and keep their own budget; a shared Token Pass cap across machines still needs a central ledger.

## Codex round 2 (reviewed SHA 95270ea): CHANGES REQUESTED, fixed in the next commit

Eight findings, each with a failing-first test (64 tests total, was 48).

| Finding | Fix |
|---|---|
| P1 OmO `applyDisabledProviders()` turns `[]` into undefined, so singleton ZDR categories inherit `sisyphus-junior`'s free fallbacks again | a ZDR category never emits an empty `fallback_models`; a singleton chain repeats its own primary. Test simulates the collapse |
| P1 a hold expiring at 1800 s released budget while the call could still run (spend reached $80.50) | expiry only relabels the hold `expired-unsettled`; it keeps counting against the cap until a late settle replaces it or `release_reservation()` / `--release <id>` reconciles it |
| P1 any receipt could settle any reservation | settle needs the same task class and model, and an open hold; otherwise `ValueError` and nothing is recorded |
| P1 coding verbs with screenshot/video/audit nouns still reached free vision/review | classifier is fail-closed: a mutation verb wins, and only an explicit read-only signal can reach scout/review/vision. No signal defaults to `code` (`source: default-zdr`) |
| P1 a Windows schema root on another OS silently gave each checkout its own budget | paid `preflight`/`reserve` are refused with a clear error unless `STARLIGHT_RECEIPTS_DIR` is set or the root is absolute on this OS; free calls still work |
| P2 sub-micro estimates were admitted but held as zero | paid estimates round up to a whole micro-dollar (minimum 1e-6); the cap check runs in integer micro-dollars |
| P2 lock timeout in `reserve()` crashed the CLI with exit 1 | `reserve()` raises `LedgerBusy` (a `BudgetError`); the CLI exits 2 with no traceback. `STARLIGHT_LOCK_TIMEOUT_S` shortens the wait for tests |
| P2 `cost_usd = 10**309` crashed the weekly review | overflow and values over $1,000,000 are counted as malformed; the spend scan and `record_receipt` also survive it |

Cost of the fail-closed classifier: ambiguous tasks ("hello there", "handle the upload") now use Token Pass credit instead of a free model. Known limit: the vision rule needs a read-only verb directly before the media noun, so "what is wrong with this screenshot" lands on `scout`, not `vision`.

## Codex round 3 (reviewed SHA e36f76c): CHANGES REQUESTED, fixed in the next commit

Seven findings, 71 tests total (was 64).

- Classifier: free classes need a read-only verb at the START of the request ("code a search function" no longer matches); more mutation verbs (correct, repair, resolve, adjust, rework, address).
- OmO: `sisyphus-junior`, `quick`, `unspecified-low`, `artistry` and `visual-engineering` execute edits, so they now sit on the `code` ZDR class. Only explore, librarian, multimodal-looker, momus and `code-review` stay free. A test removes each provider in turn and checks no ZDR category can resolve to a free model. If `vercel` is disabled the ZDR chains empty out and OmO has no model, which is an error rather than a leak.
- Settlement stores the cost rounded up to a micro-dollar, so tiny real costs cannot reopen budget.
- Costs above $1,000,000 are rejected as input (`1e308` exited 1 with a traceback) and ignored when read back from the ledger.
- Ledger readers catch `ValueError`, so a 5,000-digit integer cost is skipped instead of crashing.
- `is_paid` ignores a non-string `used`, so one malformed row no longer blocks paid admission.
