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
