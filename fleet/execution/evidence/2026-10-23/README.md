# Execution milestone evidence — 23 October 2026

Development endpoint: https://starlight-execution-dev.frankxai.workers.dev/health

| Boundary | Observed result |
|---|---|
| Local coordination and MCP | 24 actual workerd tests, including official MCP SDK and restart persistence |
| Worker, artifacts and publication | 15 tests pass |
| Paid launch admission | 229 tests, 227 pass, 2 Windows skips at e156d5c |
| Existing kernel suite | 145 tests; 144 pass and one timing-dependent 1ms lease failure; isolated rerun passes |
| Local estate repair | Authenticated submission, duplicate, workerd restart, isolated source clone, 97 protected checks + 2 external skips, signed receipt |
| Real Cloudflare estate repair | Official MCP SDK over HTTPS, anonymous request rejected 401, same worker/kernel path, four hashed artifacts, settled zero model usage |
| Real Cloudflare fault probes | 12/12 pass: role separation, command authority, idempotency, concurrent/exhausted admission, cancellation and unknown-usage reconciliation |
| Model quality evaluation | 0/12 tasks run; no frontier model calls |
| Draft publication | [PR 384](https://github.com/frankxai/agentic-ops-hub/pull/384), authorized connector consumed verified packet; exact Git tree equality checked |

The source for the deployed coordinator was committed locally as `83cd847d9f8cf581cb3776c620200d0d10f13f74`. Cloudflare returned deployment ID `7cf5f2cb2da54ddaac0f66163e87a8fe`, migration tag `execution-v1`, compatibility date `2026-10-23`, and a 10ms CPU limit. The isolated development Worker has a one-microUSD model-admission cap, no inference binding and no cron. No production Worker was modified. Infrastructure charges were not measured; zero inference is not zero infrastructure cost. Billing-read scope is unavailable to the connected OAuth account; no billing setting or budget was changed.

Reviewable source: [execution service PR386](https://github.com/frankxai/agentic-ops-hub/pull/386). Separate [paid admission PR385](https://github.com/frankxai/agentic-ops-hub/pull/385) stacks on routing PR377. Neither is merged. `cloud-faults.json` records the 12 explicit development-only probes. Their known-zero inference reconciliation is justified because the fault script never invokes any executor or provider; that rule must not be copied to interrupted real executions.

`cloud-live.json` is the real HTTPS result and public run view. `kernel-receipt.json` and `public-key.pem` permit standalone kernel signature verification. `verification.json` explicitly identifies deterministic fixture verification and zero model calls. `candidate.patch` is the actual lab repair. Private bearer credentials and the worker journal are excluded.

```sh
node /absolute/starlight-kernel/bin/starlight.mjs verify \
  --receipt fleet/execution/evidence/2026-10-23/kernel-receipt.json \
  --pubkey fleet/execution/evidence/2026-10-23/public-key.pem --json
```

A signature proves this key attested to the bound artifact, not an independently authenticated model checker. The coordinator's worker proof remains `worker-self-asserted`. The actual draft PR is the local demo's repair; the live HTTPS repeat produces the same Git tree and was not published as a duplicate PR.

No merges, production rollout, purchases, budget increase, live model activation or ChatGPT account connection occurred. The fixture worker is local and invoked once; no 24/7 executor is running. The endpoint's auth is configured, but a future ChatGPT connection needs its own approved credential provisioning; do not embed bearer secrets in plugin source.
