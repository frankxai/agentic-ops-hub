# Harness verification, 23 October 2026

Actor: Codex. Scope: independent local checks and a portability bug fix. No model calls, paid infrastructure, deployment, merge, PR comment or formal sign-off.

## Exact revisions and results

| Target | Revision | Result |
|---|---|---|
| Routing PR 377 | `b432b7b9492651bf5f5fb1e6c49a1d7ba4a8482e` | `python -B -m unittest tests.test_routing_brain tests.test_opencode_launch tests.test_token_planner tests.test_cli_capacity`: 217 tests, 215 pass, 2 Windows-only skips on Linux |
| Lab PR 379 before fix | `9f5999f18b9e1ec6a181b70d8b2b3ce080ded11f` | With CI's jsonschema 4.26.0 installed: 99 tests, 88 pass, 2 errors, 9 skips |
| Lab with this fix | parent above plus the decorator move in this commit | Same suites: 99 tests, 97 pass, 2 external SIS-conformance skips; registry check passes: 9 experiments, 15 gates |

Environment: Linux, Python 3.12. The receipt suite requires `jsonschema==4.26.0`, as declared in CI; it was installed into an isolated review virtual environment. Initial missing-dependency failures were environment setup failures, not product defects.

## Fixed: conformance skip was attached to the wrong class

`SemanticInvariantTests` uses only the vendored schema and local bridge, but its entire nine-test class was skipped without Frank's Windows SIS checkout. `ConformanceTests` actually needs that checkout, yet ran unconditionally and failed on Linux. Move the existing class decorator to `ConformanceTests`. This enables all nine local semantic checks and skips only the two external integration checks when their prerequisite is absent. No production policy changes. External SIS validator conformance is still unverified here.

## Activation blocker: provider containment is not budget admission

At PR 377's exact revision, `fleet/opencode_launch.py:run` resolves a model, constructs a provider-restricted config and invokes its process runner. It does not call `reserve`, `preflight` or `record_receipt`. The token planner and capacity probe use that wrapper.

A no-network probe populated an isolated routing ledger with current-month spend equal to `token_pass.hard_cap_usd`, then called both entry points using a synthetic key and an injected fake process runner:

```json
{"ledger_at_monthly_cap":true,"router_preflight_admitted":false,"launcher_invoked_fake_process":true,"launcher_exit_code":0,"real_processes_or_api_calls":0}
```

This demonstrates a local admission gap. It does not establish that a real gateway key would permit over-budget requests; server-side limits were not inspected. Do not describe the wrapper as enforcing the routing ledger's monthly or per-task ceilings. A multi-call harness also needs a run-level allowance and actual usage reconciliation, rather than treating one estimate as a hard provider ceiling.

Next bounded repair: require a funded run admission before paid process launch, preserve unresolved holds on interruptions, ingest real usage before settlement, and test full-budget refusal, concurrent claims, timeout recovery and duplicate settlement. Keep activation held until the server-side key cap and registry preflight are verified. No live launch was attempted.

## Repository disposition

The main-branch focus window in `AGENTS.md` and `ops/plans/estate-convergence-2026-10-21.md` makes the hub drain-only and caps new PRs. This is an isolated correction branch stacked on PR 379; no new PR is opened. The existing PR owner can cherry-pick the test fix after review. This record is evidence of local checks, not a formal pr-gate sign-off or proof that a harness experiment ran.
