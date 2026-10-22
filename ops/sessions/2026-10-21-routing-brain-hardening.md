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

## Codex round 4 (reviewed SHA 6159c4b): CHANGES REQUESTED, fixed in the next commit

Five findings, 83 tests total (was 71). Frank chose Option A for the classifier.

- P1 classifier: a read-only lead verb let a later, unlisted mutation through ("Review auth.py, then code a new login function", "Read settings.json and save it to backup.json"). Free classes now need a short single-clause request: at most 30 words, a read-only opening verb, no clause connector (and, then, also, next, before, ; , : & + newline, backtick, `->`, a second sentence) and no mutation or action word anywhere (save, store, run, execute, send, post, upload, copy, export, publish, release, sync, pull, `code a ...`, plus the earlier mutation verbs). Everything else is ZDR. A 100-prompt corpus (50 must be ZDR, 50 may be free) asserts zero leaks and no over-blocking of the plain read-only set.
- P1 ledger: an unterminated tail line swallowed the next paid receipt while the hold closed. Every append now starts a new line when the file does not end in a newline. A reservation only closes after the receipt is read back as the last line of the ledger; otherwise `OSError` and the hold stays open. The reserve event is verified the same way.
- P2 settle retry: a receipt now carries its `reservation_id`. If a retry finds a receipt for that id (the settle event failed after the receipt was written), it finishes the settlement and returns that receipt; no second receipt is written.
- P2 weekly review and `record_receipt`: `latency_ms` is bounded (0 to 86,400,000); out-of-range is malformed, so two `10**308` latencies no longer sum to infinity.
- P2 weekly review: negative cost or latency is malformed, so it can no longer drive a proposal.

Cost of Option A: a read-only request with a comma, "and", or more than 30 words now uses Token Pass credit. "review the code" stays free; "review the diff and commit it" does not.

## Codex round 5 (reviewed SHA 741e130): CHANGES REQUESTED, mechanical findings fixed, finding 1 left open

Seven findings; 91 tests total (was 83). No further Codex round was run on the fixes.

Fixed (findings 2 to 7, all mechanical):
- 2: a settle retry that finds the receipt already written now fsyncs the ledger (and the holds file) before it closes the hold.
- 3: `_append_unlocked` loops until every byte is written; a short `os.write` no longer loses a receipt.
- 4: `shared_root_usable()` is true only for an absolute `STARLIGHT_RECEIPTS_DIR`; a relative override refuses paid admission (free calls still work).
- 5: the existing-receipt lookup runs before the open-hold check, so a retry after a settlement that errored after writing returns the receipt. A retry with another class or model is still refused. A repeat settle with the same id now returns the first receipt instead of raising (the old test was updated).
- 6: a reservation estimate over $1,000,000 is malformed and skipped, so it cannot overflow the micro-dollar math.
- 7: both ledger readers decode bytes with `errors="replace"`, so a torn UTF-8 tail is one malformed line, not a crash.

Finding 1 (P1, classifier) is NOT resolved: "Read settings.json or erase backups" and "List files | xargs unlink" reached free classes. Only structural connectors were added (`or`, `|`, `<`, `>`, `$`). Verbs such as `erase` and `unlink` are still not listed, and any verb list will keep losing. It needs a policy decision: a closed set of request templates for free routing, or a ZDR-only gateway key so a classifier miss cannot leak.

## Codex round 6: finding 1 resolved structurally (closed grammar for free routing)

Frank approved continuing; the coordinator asked for a structural fix. The mutation-verb blacklist (`MUTATION`, `ACTION_WORDS`, `CLAUSE_BREAK`, `READ_ONLY`) is gone from `fleet/route_classifier.py`. A request may use a free class only if ALL hold:

- (a) it opens with a word from `READ_ONLY_VERBS` (read, list, show, summarise/summarize, explain, find, search, describe, map, count, print, plus review, audit, lint, analyze, inspect, locate and where/what/how/why, which the review and vision classes need). `check` is excluded on purpose;
- (b) at most 15 words;
- (c) every other word is in the closed vocabulary (function words and plain nouns, no verbs) or is an identifier/path (`settings.json`, `src/app.py`, `wipe_disk`, `v2`: alphanumerics joined by `. / _ -`, no separator at either end) or is quoted;
- (d) only letters, digits, spaces and `. / _ - ' "` are used. One trailing `?` or `.` is ignored (a small widening of the coordinator's list: it cannot hide anything).

Any unknown word means ZDR. `erase`, `unlink`, `truncate`, `wipe`, `drop`, `purge`, `overwrite`, `nuke` and `shred` need no entry anywhere, because they are not in the vocabulary. The strong rules (ultrabrain, hard-reasoning, bulk) still run first and are all ZDR classes.

A mutation test caught one mistake of mine: `private` was in the vocabulary as an adjective, so "Find the private key" went free. It is removed, and a test pins that the vocabulary holds no mutating, connector or sensitive word.

Tests: 101 (was 91). The corpus is now `tests/routing_corpus.py`: 100 must-be-ZDR prompts (zero leaks) and 100 natural read-only prompts.

Free hit rate, honestly: **41 of 100** natural read-only prompts still route free. On the 50 prompts the old blacklist classifier let through, the new grammar lets 17 through (34%). Natural questions often contain a word the vocabulary lacks ("does", "uses", "happens", "retry", "fails"), so they now pay Token Pass credit. This is the accepted cost; the vocabulary can grow by reviewed pull request. `Explain the retry logic` is ZDR (retry is unknown) and `Explain the error log` is free, pinned by a test. A floor test keeps the hit rate at or above 35 of 100.

Known limit: an identifier or quoted span is treated as data, so `Read 'erase everything'` and `Show ./rm` stay free. The text is only sent to a model that was already allowed to read.

## Codex round 6 verdict (reviewed SHA 0e64f42, whole branch vs hub/main): CHANGES REQUESTED

Verdict: `scratchpad/codex-verdict-6.txt`. No further Codex round was run. Three findings:

- Fixed, mechanical (finding 3, P2): a settle retry trusted any prior receipt for the reservation id. A corrupted timestamp or an incomplete record closed the hold, reopened budget, or crashed the CLI with `KeyError: 'over_ceiling'`. `_countable_receipt()` now requires every field present and typed, a parseable timestamp, and a finite in-range cost and latency. Otherwise `record_receipt` raises `ValueError`, the hold stays open, and `--release` reconciles it. 104 tests (was 101).
- OPEN (finding 1, P1, not mechanical): quoted text and identifiers are treated as data, so `Read .env`, `Print api_key`, `Show passwords.txt` and `Print 'the api token is sk-live-123456789'` route free. The grammar says nothing about what the data IS. Closing it needs a policy: drop identifiers and quotes from free routing (many paths then pay), or add a sensitive-name list (a blacklist again), or use a ZDR-only gateway key.
- OPEN (finding 2, P1, not mechanical): the vocabulary lets nouns act as verbs and lets hyphens hide connectors: `Review auth.py code a new function`, `How to code a new function`, `Read file 'and' 'erase' it`, `Show the file then-delete-it` all route free. Needs a decision: remove `code` and similar verb-nouns from the vocabulary, forbid hyphenated or quoted tokens that contain a connector, or enforce a fixed sentence template.

Two review rounds in a row (5 and 6) found classifier leaks that a word list cannot close. The reliable control is outside the classifier: a gateway key that can only reach ZDR providers for ZDR work, so a classifier miss cannot leak.

## Option A hardening

Frank approved option A on 2026-10-22: mechanical tightening of the classifier, then stop the Codex loop. No further Codex round was run on this change.

What changed in `fleet/route_classifier.py`:
- Verb-like nouns left the vocabulary: code, test(s), import(s), comment(s), route(s), flag(s), order, print, map, count, type(s), key(s). `build`, `run`, `set`, `patch`, `change`, `update`, `fix` were never in it. `log`, `name`, `branch` stay (reading them as verbs is rare and the words are common in real questions).
- Quotes are not an allowed character any more. Quoted text is never routed free.
- Joined words (`a-b`, `a_b`) need every part in the vocabulary, so `then-delete-it` and `wipe_disk` go to ZDR. A lone word counts as data only inside a path or file name, and a dotted name needs a known extension.
- Sensitive guard: the whole request is lower-cased and checked for env, key, token, secret, password, passwd, credential, cred, pem, ssh, auth, cert, private, wallet, seed, mnemonic, bearer, jwt, rsa, gpg as substrings. It over-matches on purpose (`author`, `keyboard` go to ZDR).
- All eight round-6 leak examples plus 30 variants are in `MUST_BE_ZDR`; none reaches a free class.

Cost: free routing of the 100 natural read-only prompts fell from 41 to 35. The floor test stays at 35 and was not loosened.

Plainly: the classifier is a cost heuristic, not the security boundary. Four review rounds found leaks a word list cannot close, and this change does not claim otherwise. The real control is a gateway key that can only reach ZDR providers, so that a classifier miss fails instead of leaking. Frank creates that key in the dashboard. Until then, treat free routing as best effort for requests that carry nothing sensitive.

## Codex round 8 fixes

Codex round 8 (on `749bff5`) found two design issues and two mechanical ones. Fixed in this commit:
- P1, free routing was opt-in only in the generator. Now it is opt-in at every entry point: `route()` and the admission, receipt and `pick_next` calls take `allow_free` (default off), and `route_task.py` and `route_executor.py` take `--allow-free`. Without it scout, review and vision are served by the cheapest ZDR gateway model.
- P1, the generator's paid replacements were off-chain for the executor and had a zero ceiling. `route_executor.effective_route()` now derives the chain and ceiling in one place, and `gen_omo_config.py` calls it. Each free class has an explicit `zdr_cost_ceiling_usd` in the schema; a missing or non-positive value is an error, not zero. A test checks that every model in the generated config (both modes) passes `preflight` and `record_receipt` for its class.
- P2, concurrent generator runs shared one `.tmp` name. The temp file is now created with `tempfile.mkstemp` in the target directory, one per invocation, and the replace retries on a Windows `PermissionError`.
- P3, `_countable_receipt` accepted a timestamp that overflows UTC conversion (`0001-01-01T00:00:00+01:00`). It now uses `_as_utc`, the path `month_paid_spend` takes, and treats `OverflowError` as uncountable.

Cost of the safe default: scout, review and vision calls spend Token Pass credit unless the caller passes `--allow-free`. Plainly: the gateway key guarantees only the calls that go through the gateway.


## Codex round 12 fixes

Codex round 12 (on `4938ab1`) found one design issue and two mechanical ones.

- **P1, `-m` pins only the primary model.** Fixed with `fleet/opencode_launch.py` (see "Launches under a generated config" in `fleet/ROUTING-BRAIN.md`). The empirical check, run read-only on opencode 2.1.2 with no model call, using `opencode models` as the observable. A temporary HOME and config directory held a hostile global `opencode.json` (`enabled_providers: ["opencode","vercel"]`, `small_model: "opencode/beam-free"`), and all temporary material was deleted afterwards:
  - `opencode debug config`, `opencode models` and `opencode debug agents` without `--standalone` talk to the managed background service (port 45278, started with the user's own config). With a launch directory set in the client environment, `opencode models` still listed 11 `opencode` models and 49 `vercel` models: the environment is ignored.
  - With `opencode models --standalone` and a hostile global config: 11 `opencode` models.
  - Adding `OPENCODE_CONFIG=<file with disabled_providers:["opencode"]>` did NOT remove them, and neither did `OPENCODE_CONFIG_CONTENT`. A project-level `opencode.json` did not either. `OPENCODE_CONFIG_DIR=<dir>` did.
  - A launch directory with `model`, `small_model`, `enabled_providers: ["vercel"]`, `disabled_providers: ["opencode","omniroute"]` and no provider block listed zero models even with the real credentials present. The directory replaces the global config, so it must carry the gateway `provider` block. With that block copied in: 316 `vercel` models, no `opencode`.
  - The same directory plus a hostile `OPENCODE_CONFIG` file (re-enabling `opencode`, `small_model: opencode/beam-free`), and again plus a hostile project-level `opencode.json` in the working directory: still 316 `vercel` models, no `opencode`.
  - Not verified: the effective `small_model` value, which cannot be read without a model call.
- **P2, variant.** Codex asked for `--variant`. The installed `opencode run --help` documents `-m provider/model#variant` and lists no `--variant` flag, so the variant stays inside `-m`; a test asserts this.
- **P2, settlement after a model is retired.** `record_receipt()` now checks a reservation settlement against the hold's own class and model, not the current chain. A retired model between `reserve()` and settle records its real cost (pool `token-pass`, counted in monthly spend). New admissions are still checked against the current chain, an unknown or mismatched reservation is still refused and leaves the hold open, and a class removed from the schema still settles.

Plainly: the guarantee covers launches made through `opencode_launch.py`, and it depends on `--standalone` plus `OPENCODE_CONFIG_DIR` behaving as observed on this version. A different OpenCode version needs the same check.

## Round 13 (Codex on 51536b1: CHANGES REQUESTED, 2 P1, 2 P2, 1 P3)

- **P1, Windows shim injection.** `shutil.which("opencode")` returns `opencode.CMD`; cmd.exe parses its arguments even with `shell=False`, so task text such as `x" & echo MARKER & rem "` ran a command. `resolve_opencode()` now returns the native exe (found next to the shim) and refuses a shim-only install; the task is passed after `--`. Test: a real child process echoes its argv, and the metacharacter task arrives as one literal argument.
- **P1, copied provider block.** The global `provider.vercel` could carry `baseURL`, `api`, `npm` or model overrides that survive `enabled_providers`. The launch config now holds a fixed gateway block (`{env:AI_GATEWAY_API_KEY}` only); `gateway_key()` takes just `options.apiKey` from the global file and passes it in the child's environment. Tests: a hostile global block contributes nothing but the key, and the key never reaches the generated file.
- **P2, CLI settle.** `route_task.py --record --reservation` now takes the class from the hold and skips the current-chain check, so a retired model or a removed class still records its spend. Test covers both cases.
- **P2, lifecycle.** `supervised_run()` ends the whole tree on exit, timeout, Ctrl-C or error (Windows kill-on-close Job object, `taskkill /T` fallback; POSIX new session and `killpg`). Test: a timed-out child and its grandchild both stop. No literal credential is on disk any more, so a skipped cleanup leaves only an inert config. Residual limits are in `fleet/ROUTING-BRAIN.md`: POSIX SIGKILL of the wrapper leaves the child.
- **P3, CI.** `tests.test_opencode_launch` added to the unit-test step.

Verified locally: opencode_launch 26/26, routing_brain 161/161, the eight neighbouring suites 183/183. Full Windows ACL behaviour of the temp directory is still unverified.

