# Estate lifecycle registry (public projection)

One row per entity: repo, product, substrate, vertical, experiment, agent pack. Every row sits in one lifecycle state, has one owner General, one human gate, a next gate with a receipt, and a kill rule. The private source of truth is the registry in `frankxai/agentic-ops` (per `STARLIGHT_PORTFOLIO_TOPOLOGY.md`); this directory is the sanitized projection the public sites, `llms.txt` generators and MCP offer tools read.

Schema: `estate-lifecycle.schema.json`. First classified snapshot: `vercel-projects-2026-10-13.{json,md}`.

## States

| State | Name | Entry receipt | TTL / kill |
|---|---|---|---|
| S0 | Idea | registry row with a question | 30 days, then delete |
| S1 | Experiment | hypothesis + metric + token budget; lives in `starlight-agent-lab` or a lab branch | 30 days, exit by scorecard |
| S2 | Incubating | ADR + eval scorecard; own repo, CI green, README truth, estate-guard | 90 days without an S3 receipt → S6 or S7 |
| S3 | Candidate | production deploy READY, npm publish or marketplace listing; traffic pull wired; claims audit clean | 60 days with zero external use → S6 |
| S4 | Product | offer in registry; Polar checkout open; first external payment; webhook → CRM | 90 days with zero payers → S3 |
| S5 | Flagship | 3 months paid use or one signed SOW; full squad; steward budget | demotion note by CEO General |
| S6 | Steward | demotion note naming the metric missed | maintenance lane only: security, links, no features, no SKUs |
| S7 | Archive | recovery tag + redirect README + 7-day objection window in the ops ledger | never deleted without a tag |

Substrate entities (SIP, memory, swarm, payments, evals, agent skills) use the same states; their S4 receipt is "an S4 product depends on this version", never a price.

## Transitions and signatures

| Move | Signs | Capacity pool after |
|---|---|---|
| S0 → S1 | CTO (substrate) or CPO (product) | 10 % experiment |
| S1 → S2 | CAIO + one board lens | 30 % candidate |
| S2 → S3 | CTO + CMO | 30 % candidate |
| S3 → S4 | CFO + CPO; Frank signs the price | 60 % flagship |
| S4 → S5 | CEO; Frank signs | 60 % flagship, protected |
| any → S6 | COO | maintenance |
| any → S7 | COO; Frank for anything with traffic or paid history | none |

Capacity means the three things the fleet meters: local RAM admissions (`pp preflight`, 8,192 MiB floor), model tokens (`fleet/token_planner.py`) and Frank's signing hours. Target split 60 / 30 / 10 across S4–S5 / S2–S3 / S0–S1; the weekly pulse reports the actual split.

## Enforcement

- `estate-guard` CI refuses a repo without a registry row (to be added to the scanner as a `medium` finding, then `high` after pulse #2).
- The claims-audit contract (frankx.ai PR #1000) refuses any public number not present in the row.
- A new Vercel project, npm package or repo without an S0/S1 row is an incident, logged in the ops ledger.

## Cadence

Daily ops-sweep (COO) · weekly pulse (CEO: promotions, demotions, 60/30/10 drift) · monthly close + eval run (CFO + CAIO; a stale scorecard freezes S1→S2) · quarterly portfolio board (six lenses, on the registry as a whole).
