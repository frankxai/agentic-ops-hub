# Railway capacity sample — read-only
# Project: perceptive-curiosity (3e19771a-09dd-4fa5-a2e5-80444d0b7627)
# Sampled: 2026-08-07T15:41:17Z by C940 Hermes estate action
# Issue: https://github.com/frankxai/agentic-ops-hub/issues/35

## Volume — clickhouse-volume
| Field | 2026-08-06 15:22 CEST | 2026-08-07 15:41 UTC |
| --- | ---: | ---: |
| currentSizeMB | 4418.88768 | 4440.670208 |
| sizeMB | 5000 | 5000 |
| used % | 88.38% | **88.81%** |
| free MB | 581.11 | **559.33** |
| state | READY | READY |
| Δ size | — | **+21.78 MB ~24h** |

Classification: **capacity incident, still serving**. Growth continues (~22 MB/day). At this rate free headroom exhausts in roughly **~25 days** if linear (559/22).

## Service plane (same sample)
| Service | latestDeployment | active instance | notes |
| --- | --- | --- | --- |
| clickhouse | SUCCESS | RUNNING | health `/ping`, restart ALWAYS |
| langfuse-web | FAILED | RUNNING | serving-with-failed-latest-rollout |
| langfuse-worker | FAILED | RUNNING | serving-with-failed-latest-rollout |
| litellm | FAILED | RUNNING | serving-with-failed-latest-rollout |
| evals-service | FAILED | RUNNING | serving-with-failed-latest-rollout |
| Redis (official) | SUCCESS | RUNNING | |
| redis (legacy name) | FAILED | none | orphan candidate — do not restart blindly |
| Postgres / postgres / minio / Infisical | SUCCESS | RUNNING | |
| evals-runner | SUCCESS | EXITED | cron `0 */6 * * *`, restart NEVER — expected |

## Mutation gate (unchanged)
Do **not** without explicit infrastructure approval:
- resize/delete volume
- purge ClickHouse partitions / Langfuse data
- redeploy/restart Langfuse/LiteLLM/evals to “fix” capacity
- dump secrets or event payloads

## Recommended reversible options (prepare only)
1. **Retention-driven cleanup** — identify dominant Langfuse CH tables/TTL; backup proof; delete expired partitions only.
2. **Approved capacity resize** — increase volume with billing impact recorded; keep `/ping` green.
3. **Ingestion freeze** — keep raw prompts disabled; do not increase trace volume while headroom < 15%.

## Acceptance for close
- headroom restored above agreed threshold (suggest ≥20% free / ≤4000 MB used)
- clickhouse `/ping` green
- Langfuse read/write smoke (if still required) or explicit decommission decision
- OPS ledger + this receipt updated
