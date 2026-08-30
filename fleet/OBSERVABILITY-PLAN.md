# Observability Plan — ClickHouse / Langfuse / LiteLLM / n8n

**Status (2026-08-29, live):** Railway `5.26.1` CLI present. ClickHouse **88.8% (P0, 4.41/5 GB)**. **Langfuse + LiteLLM + evals-service Railway deploys FAILED ~23 days** (ledger 2026-08-07/08). n8n **NOT installed** on C940. SIS Operator live at `127.0.0.1:3001/operator`. Local HTML "n8n-like" cockpit exists (`agentic-ops/docs/estate-workflow-graph.html`).

## Principle
Observe + evaluate ALL agents, but **start free/local, repair paid only when a gated decision approves spend + capacity**. The machine is at 44 GiB (under 50 floor), so we do not stand up heavy new services yet.

## What we HAVE (use first — zero new infra)
| Signal | Source | Already wired? |
| --- | --- | --- |
| Per-agent outcomes | `fleet/reports/agents/*`, cron receipts | partial |
| Token usage | `starlight-token-tracker` (`anomaly_check.py`, `planner_snapshot.py`) | yes |
| Free-tier evals | `llm_evals_*` watchdogs (no-agent) | yes |
| Live liveness | `fleet/bus/heartbeats/c940.json` (real metrics since 2026-08-29) | yes (upgraded) |
| Self-eval of free agents | opencode `best-free` observer crons | pilot (this change) |
| Visual cockpit | `estate-workflow-graph.html` | yes |

## Repair backlog (gated — needs your approval + capacity)
1. **ClickHouse P0** — 88.8% full. Either raise volume (Railway paid) or purge old fleet/evals rows. Blocks observability ingestion if it hits 100%.
2. **Langfuse redeploy** — failed 23d. Re-run `railway up` / redeploy from `agentic-ops` infra manifest; verify ingest endpoint. Cost: Railway usage (already ~$83/mo run-rate).
3. **LiteLLM** — same: redeploy + healthcheck. Needed if we route model calls through a gateway for cost attribution.
4. **evals-service** — redeploy; wire to ClickHouse + Langfuse so "evaluate all" lands in one pane.
5. **n8n** — **recommend DO NOT install.** You already have `estate-workflow-graph.html` (n8n-like, local-first, no node process). Adding n8n = another always-on service + RAM on a 44 GiB machine. If you later want workflow orchestration, run n8n in a Railway project (off this box), not C940.

## Target architecture (when repaired)
```
agents (cron/profile) --receipt--> fleet/reports/agents/*  --ingest-->  ClickHouse (railway)
                                                        \--eval--> Langfuse (railway) <-- LiteLLM (gateway)
SIS Operator (3001) + estate-workflow-graph.html = local single pane (no n8n)
token-tracker + cron receipts = cost/usage truth
```

## Decision needed
Approve Railway redeploy of Langfuse/LiteLLM/evals-service (spend + possible volume bump for ClickHouse)? Until then, observability = local watchdogs + SIS + token-tracker + free-tier self-eval.
