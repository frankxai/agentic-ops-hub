# Daily Objective-to-Quota Planner

This planner belongs to the **agentic-ops-hub swarm control plane**. It is not a standalone tracker feature.

Its optimization target is:

> Maximize verified, integrated outcomes per wall-clock hour from available subscription capacity, while preserving quota reserves, machine safety, maker/verifier separation, and human gates.

Token use is capacity. A token, prompt, process, report, or configured cron is never an outcome by itself.

## Architecture boundary

| Layer | Owner | Responsibility |
|---|---|---|
| Objectives and outcome policy | `objectives-registry.json` | Canonical outcomes, priority, owner, success metric |
| Swarm reasoning and allocation | `fleet/token_planner.py` | Route objective demand across CLI pools, machines, roles, windows, and reserves |
| Execution admission | `fleet/night_runner.py` | Branch, worktree, disk, RAM, live CLI, quota, and receipt gates |
| Fleet truth | `fleet/bus/` and `scripts/fleet_bus.py` | Machine identity, heartbeat, durable queue, acknowledgment |
| Token telemetry sensor | Tokscale / `starlight-token-tracker` | Read provider windows and usage; never choose objectives or dispatch work |
| Queen | Hermes on YogaBook | Select objectives, resolve conflicts, compile admitted lanes into campaign manifests, integrate receipts |

The tracker may improve telemetry adapters independently. Planning policy, historical estimates, daily allocation, and execution decisions stay here.

## Daily control loop

1. **Objective intake** — Queen selects at most three canonical objectives and supplies job class, urgency, artifact contract, admitted machines, and live CLI health.
2. **Capacity snapshot** — Tokscale or the tracker emits a sanitized quota map. Email, account identity, credentials, and raw auth data are discarded.
3. **Plan** — `daily-plan` reserves each provider floor, targets 85% of the usable capacity above it, and schedules maker/verifier lanes on admitted machines.
4. **Compile** — Queen converts the next admitted lane into a version-3 campaign mission with exact repo, worktree, branch, acceptance commands, receipt, and stop conditions.
5. **Execute** — `night_runner` performs live admission and launches one heavy coding CLI per machine.
6. **Learn** — a redacted observation records duration, quota delta when measurable, outcome status, and artifact score.
7. **Replan** — after every receipt, quota reset/change, CLI or machine state change, or 90 minutes while objective demand remains.

A plan does not blindly schedule past a depleted window. It records the provider reset as a replan point so the next live reading decides the post-reset allocation.

## CLI and quota pools

The planner inventories every current surface separately while preventing double counting:

- Codex CLI -> Codex Max pool
- Claude CLI -> Claude Max pool
- Gemini CLI -> Gemini Ultra pool
- Grok Build CLI -> xAI/Grok Heavy pool
- AGY -> unmeasured multi-model lane; one lane until live behavior is learned
- OpenCode -> provider-dependent lane; one lane until live auth is proven
- dcode -> inventoried metered API lane; non-admissible until a campaign carries the exact bounded
  approval contract **and** the installed launcher exposes an enforceable hard spend cap
- Hermes -> Queen/control plane, not an independent burn pool

`cli_capacity.py --live` performs bounded one-turn subscription checks. Declared login or an installed binary is not readiness. Use repeatable `--live-cli` flags to probe only candidate providers above reserve; this avoids burning depleted pools. dcode is intentionally not live-probed by the generic subscription command because it is metered. Reports are machine-scoped, and a failed machine resource gate blocks every execution lane from that report.

## Commands

```bash
# Produce redacted CLI readiness evidence.
python scripts/cli_capacity.py --machine yoga-book --live \
  --live-cli codex --live-cli claude \
  --output C:/Users/frank/.starlight/token-planner/cli-capacity-yoga-book.json

# Compile a deterministic daily plan from a request and sanitized quota snapshot.
python -m fleet.token_planner daily-plan fleet/daily-plans/example.request.json \
  --quota C:/Users/frank/.starlight/token-planner/quota.json \
  --cli-capacity C:/Users/frank/.starlight/token-planner/cli-capacity-yoga-book.json \
  --cli-capacity C:/Users/frank/.starlight/token-planner/cli-capacity-c940.json \
  --history C:/Users/frank/.starlight/token-planner/capacity-history.jsonl \
  --output C:/Users/frank/.starlight/token-planner/daily-plan.json

# Atomically record one receipt-bound observation. The verified receipt SHA-256 is the idempotency key.
# Replace the all-zero digest in the example with the actual receipt SHA-256 first.
python -m fleet.token_planner record-observation \
  fleet/daily-plans/example.observation.json \
  --manifest fleet/campaigns/<verified-campaign>.json \
  --history C:/Users/frank/.starlight/token-planner/capacity-history.jsonl
```

Private runtime observations and live quota snapshots remain under `C:/Users/frank/.starlight/token-planner/`; they are not committed to this public control-plane repository.

## Queen and scheduler contract

There must be **one scheduler owner**, not a new cron per provider. The existing Starlight Queen pulse is the owner. Its loop should:

1. read objective demand, fleet heartbeat, receipts, sanitized quota, and CLI capacity;
2. invoke `daily-plan`;
3. dispatch only the next admitted campaign lane per machine;
4. re-run after a receipt or material capacity event;
5. stay silent when no objective-backed lane is admissible.

Do not add another recurring planner job while that Queen pulse exists. If the pulse is replaced, remove or pause the old owner first.

## Learning model

Observations are grouped by CLI, job class, and role. Recording requires the source manifest plus a
repo-contained receipt whose digest, mission, agent, role, commit ancestry, artifacts, and exact
verification commands all validate. The receipt digest is rechecked before persistence. Forecasts use
verified artifact-producing samples only:

- median quota-window delta;
- median wall-clock duration;
- verified outcome rate;
- confidence: low below 3 samples, medium at 3-7, high at 8+.

The planner begins with conservative defaults and improves as real receipts accumulate. Self-declared,
failed, forged, legacy, report-only, or unbound observations are not admitted to learning history.

## Hard policies

- Preserve provider reserve floors.
- No synthetic work to consume quota.
- No metered fallback without an exact campaign approval object: approval ID, provider, configured
  quota pool, USD currency, positive finite cap bounded by the mission budget, and timezone-aware expiry.
- A metered receipt is not counted as complete or used for skip-verified unless the approval is still
  current and the configured launcher exposes an enforceable hard-spend-cap argument.
- A measured pool at `0%` is blocked even when its configured reserve floor is zero.
- Measured percentages must be finite and within `0..100`; malformed, NaN, infinite, boolean, or
  out-of-range telemetry is unavailable and fails closed in both admission and planning.
- Declared, mission, and every wave budget must be a numeric, finite, non-negative JSON amount;
  booleans, strings, `NaN`, and infinities fail validation before any budget comparison.
- No CLI admitted from login/version output alone.
- Every planned role is treated as a writer because makers, verifiers, and integrators emit artifacts,
  reports, or receipts. Lanes sharing the same normalized repo/worktree identity are serialized.
- Maker and verifier use different effective agents.
- Every campaign mission binds a canonical machine compatible with its CLI pool. The runner maps its
  local hostname to that canonical identity and queues—not launches—missions assigned to another node.
  Before process launch it also acquires OS-backed machine and normalized-worktree leases under the
  established machine-local `.starlight/swarm-leases` runtime; contention fails closed and locks release
  on completion, failure, or process exit. After acquiring both leases, the runner revalidates receipt
  status, dependencies, wave, machine, branch, cleanliness, resources, current quota/readiness, route,
  and launcher arguments so a stale prepared row cannot duplicate a completed or changed mission.
- Receipt-bound fallback is advisory until the replacement agent is committed to and revalidated in
  the manifest. The runner never launches an in-memory agent substitution.
- One heavy coding CLI per machine; at most two across YogaBook + C940.
- Completion requires accepted artifacts and machine-readable verification receipts. Version-2 and
  version-3 missions share the same strict agent, role, commit-ancestry, artifact-at-commit, and exact
  verification-ID-to-command receipt checks; legacy receipts remain unverified until upgraded.
- Manifest acceptance commands are parsed against fixed repo-scoped validation families. Shell
  separators, substitutions, redirections, newlines, path escapes, and command wrappers are rejected.
- Metered dcode remains disabled and receives no local shell allowance. The current CLI exposes a
  wall-clock timeout but no enforceable USD spend-cap flag, so approval alone never admits it. A future
  positive path requires both the validated approval object and a launcher-enforced hard spend cap.
