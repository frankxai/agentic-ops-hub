# 2026-10-21 Research lab registry and dashboard

Branch `agent/claude/research-lab`, based on `hub/main` (1b2c09e). Author: Claude Code. A different harness must sign the SHA before merge.

## Made

- `lab/`: goals, gates, budget, seven S1 experiments (EXP-001 to EXP-007), `build_lab.py` (validator and dashboard generator), README.
- `tests/test_lab_registry.py` (12 tests) and a CI step that validates the registry and builds the page.
- `ops/plans/2026-10-21-research-lab-and-cloud-workers.md`: decisions on OmO (no fork), Flash, Railway harness, worker topology, dashboard home.

## Verified

- `python -B -m unittest tests.test_lab_registry`: 12 passed.
- `python lab/build_lab.py --check`: ok. Dashboard rendered and viewed at desktop width, dark theme.

## Not done

- No experiment has run. All are blocked or proposed.
- No runner, no suite, no worker container. They are follow-up PRs and need PR 377 merged first.
- Light theme and phone width were not reviewed by eye.

## Needs Frank

See `lab/gates.json`: create a Token Pass key named lab-worker in the dashboard, ZDR strictness, Railway cap approval, what "software factory" means, delete the $1-budget keys.

## Codex pass 2 (2026-10-22, on b30511f): CHANGES REQUESTED, 10 P2 and 1 P3, all addressed in the next commit

- `lab/receipt_bridge.py`: `accepted()` and `build_receipt()` now also run `semantic_problems()`, a Python mirror of the SIS `receiptProblems()` checks that JSON Schema cannot express: RFC 3339 dates with a zone, time order, finite non-negative numbers, and totals not below the stage sums (cost with the SIS rounding allowance, latency, tokens). A cost that overflows when converted (1e308 at fx 2) is refused at build time.
- `lab/build_lab.py`: routing rows count only with real booleans and an explicit finite non-negative `cost_usd`; checker types are classified (`blind-judge` and `human-review` are judged, unknown types are an error and count as judged); required dashboard fields are validated for harnesses, packs, gates, pillars and projects; a measured claim needs a non-empty source that is an existing repo file; every experiment declares a tier and T1 or above never runs on the laptop; owner and verifier are compared after trim and casefold; arm harnesses must be registered or carry `harness_pending`; `design.runs_per_cell` below the sample floor requires `decision_effect: none`.
- Data: tiers added to EXP-002 (T2), 003 (T3), 004 (T0), 005 (T0), 007 (T1); arms that said `opencode` now say `opencode-bare`; open choices (`any`, `best of EXP-002`, `eve`, `worker from EXP-004`) are `harness_pending`; EXP-001 and EXP-006 are labelled one-run-per-cell directional pilots that change no routing, and their kill and pass rules say so.
- `ops/plans/2026-10-21-harness-measurement-and-scale.md`: the "4 toy tasks, 16 rows" figures are marked unverified (the files are not in this branch), and the tier table lists the new tiers.
- Tests: `tests.test_lab_registry` 57, `tests.test_receipt_bridge` 42 (99 in total). 24 of the new tests fail against the previous code. Codex has not re-reviewed this change.
