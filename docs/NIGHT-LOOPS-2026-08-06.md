# Night Loops — Control-plane closure pack (2026-08-06)

## Intent

Close the loops already designed in fleet strategy and the agentic-systems review:

1. **Topology health** — declared → installed → scheduled → running receipt (no-agent).
2. **Mission envelope / outcome receipt** — candidate vs verified with independent evaluator.
3. **Council skill** — rare multi-model / multi-seat judgment (not default chat).
4. **Cron repair** — live provider pins; Grok-spend failures held or repinned.
5. **Memory rebalance** — stop ops-vault starvation of strategic/wisdom.
6. **How to use Hermes + coding CLIs** — one operating card.

## Commands

```bash
# Health receipt (exit 2 on RED)
python scripts/topology_health.py --write fleet/reports/topology-health-latest.json

# Mission envelope
python scripts/mission_envelope.py envelope \
  --objective "Ship topology health loop" \
  --repo agentic-ops-hub \
  --branch agent/c940/night-loops-20260806 \
  --path scripts/topology_health.py \
  --out fleet/receipts/env_example.json

# Candidate receipt (worker)
python scripts/mission_envelope.py receipt \
  --envelope-id env_xxx \
  --status candidate \
  --summary "tests green" \
  --evidence "tests/test_topology_health.py"

# Verified only with independent evaluator name
python scripts/mission_envelope.py receipt \
  --envelope-id env_xxx \
  --status verified \
  --evaluator "codex-read-only-reviewer" \
  --summary "acceptance passed" \
  --evidence "pytest log"

python -m unittest discover -s tests -v
```

## Cron wiring (Hermes)

- `topology-health-pulse` — no-agent, hourly or every 6h, script `topology_health_pulse.py` (installed under Hermes scripts). Quiet when GREEN.
- Daily ops-sweep should **read** latest topology receipt rather than re-deriving from chat memory.
- Paused Grok jobs: repin to `openai-codex` / live model **or** leave paused with HOLD in OPS-LEDGER.

## Non-goals

- No second gateway.
- No bulk dirty-tree wipe.
- No production deploy.
- No secret printing.
- No heavy installs while disk < 35GB hard floor.

## Status language

| Status | Who may set |
| --- | --- |
| attempted / failed / blocked / candidate | worker |
| verified | independent evaluator only |
| quarantined | red-team / sentinel |
