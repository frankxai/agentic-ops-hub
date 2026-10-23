# Execution coordination candidate

Native Cloudflare Durable Object adapter for the existing Starlight execution and kernel contracts. It stores task identity, allowance reservations, claims and completion metadata; it does not run an LLM, clone repositories or create PRs itself.

## Local verification

Use Node 24, then `npm ci --ignore-scripts`, `npm test`, `npm run build`. Tests execute the actual Worker and SQLite Durable Object under pinned Miniflare/workerd. An official MCP SDK client also connects over Streamable HTTP, discovers the five tools, submits a task and queries it. Restart coverage disposes workerd and starts a fresh instance against the persisted database. This is infrastructure verification, not a live Cloudflare deployment or model evaluation.

`npm run dev` starts Wrangler locally. Supply distinct random 32–256 character `EXECUTION_CLIENT_TOKEN` and `EXECUTION_WORKER_TOKEN` secrets in ignored `.dev.vars`; no usable credentials ship here. Keep credentials out of command arguments, commits and logs. Operator configuration also requires a fixed `TENANT_ID`, exact `ALLOWED_REPOSITORIES_JSON`, `ALLOWED_TASK_KINDS_JSON`, and positive integer `BUDGET_MICROUSD`. One microUSD is one millionth of a USD. The development deployment has a one-microUSD model-admission cap and an authenticated workers.dev route. It cannot accept authenticated work without secrets.

## HTTP contract

Client routes require `Authorization: Bearer <client token>`:

| Route | Method | Input |
|---|---|---|
| `/tasks` | POST | `{idempotency_key,repository,revision,task_kind,prompt?,allowance_microusd,deadline_seconds}` |
| `/runs/:id` | GET | — |
| `/runs/:id/cancel` | POST | — |
| `/runs/:id/artifacts` | GET | — |
| `/runs/:id/eval` | GET | — |
| `/mcp` | POST | JSON-RPC initialize, ping, tools/list, tools/call |

MCP tools: `submit_task`, `get_run`, `cancel_run`, `get_artifacts`, `get_eval_report`. Run tools take `{run_id}`. The transport is stateless Streamable HTTP JSON responses (protocol `2025-03-26`), with notifications acknowledged by 202. GET streaming is not provided. This package does not install or authorize a ChatGPT connection; client setup must supply appropriate authentication.

Worker routes require the separate worker token:

| Route | Method | Input |
|---|---|---|
| `/internal/claim` | POST | `{worker_id}` |
| `/internal/runs/:id` | GET | — |
| `/internal/complete` | POST | `{run_id,lease_token,result}` |
| `/internal/reconcile` | POST | `{run_id,lease_token,actual_cost_microusd}` |

A claim returns `{run:null}` when nothing is queued, otherwise `{run}` including its one-shot lease token. Client/read responses omit that token. `result` has exactly `status` (`succeeded` or `failed`), `actual_cost_microusd` (integer or null), `artifacts` (`[{name,sha256,ref}]`), `verification` (`{passed,actor,maker,evidence_sha256}` or null for failure), and `receipt_sha256` (64-hex or null for failure). Success needs passing distinct maker/checker labels, nonempty artifact metadata, evidence and receipt digests. Labels are simple identifiers; artifact refs are relative paths without traversal.

## State and trust

- A single fixed-tenant Durable Object owns the ledger, so concurrent tasks reserve shared headroom atomically. Repeating the same idempotency key and canonical request returns its original run; a changed request conflicts.
- Claim transitions `queued → running`; claims are never automatically reissued. A worker crash must be reconciled before another paid attempt. Deadline expiry is evaluated on subsequent API calls, not by an always-on loop.
- Cancelling queued work releases its allowance. Cancelling claimed or uncertain work retains the allowance. Cancellation cannot later be changed into success by completion or reconciliation.
- Known completion replaces the hold with actual usage. Unknown usage stays null and keeps its hold; `/internal/reconcile` settles known actual usage later exactly once. Overruns are recorded, not discarded; exhausted aggregate headroom refuses subsequent tasks.
- This ledger is a total development allowance, not a monthly reset, payment processor, provider-enforced spending limit or guarantee against malicious workers. Provider limits must be independently configured before paid activation. The existing routing ledger is a different admission boundary; do not sum their reservations as independent spend.
- Worker proof is explicitly `worker-self-asserted`. A receipt digest binds a claimed artifact identity; this Worker does not validate kernel signatures, verify artifact bytes, prove the checker identity or attest actual provider usage. Those duties belong to the execution and verification adapter. The worker token is a trusted service credential.
- Reconciliation has no release-without-evidence endpoint. An abandoned live claim conservatively keeps its hold. No merge, deployment or publication action exists on the client surface.
- Maximum 1,000 retained runs per development tenant bounds state scanning. There is no automatic retention deletion; reaching capacity requires an operator-reviewed archival/migration decision.
- Browser origins are denied unless explicitly listed in `ALLOWED_ORIGINS_JSON`; bodies are limited to 64 KiB of actual bytes. Tasks cannot supply commands, tokens, policy changes or arbitrary repository URLs. A prompt is data for a registered task preset, never a grant of tools or permissions.

## Deployment boundary and rollback

Development deployment on 23 October 2026: `https://starlight-execution-dev.frankxai.workers.dev`. Separate SQLite namespace, client/worker secret bindings, one-microUSD model-admission cap, 10 ms CPU limit, no inference binding, no cron and no hosted executor. Health and authenticated MCP/REST were exercised over real HTTPS. Do not upload it over production `starlight-cloud-worker`: that worker has an existing containment restriction and different bindings. No production resource or budget was changed. Infrastructure usage cost was not measured.

Rollback a development release by restoring its preceding Worker version while keeping the same Durable Object class/tenant identity and schema. Do not delete its namespace or change `TENANT_ID` to bypass unresolved reservations. Snapshot and reconcile claims before schema changes; no destructive migration is included.

Retrieved Cloudflare references: [SQLite storage](https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/), [Durable Object rules](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/). The implementation uses synchronous SQL and `transactionSync`; the `new_sqlite_classes` configuration remains supported by the pinned Wrangler release.
