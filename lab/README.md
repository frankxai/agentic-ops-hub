# Starlight Lab

The estate's experiment registry. Each experiment is an S1 row in the lifecycle (`registry/README.md`): a hypothesis, a metric, a token budget, a 30-day limit, an exit by scorecard.

## Add an experiment

1. Copy an existing `lab/experiments/EXP-00x-*.json` and give it the next id.
2. Fill every field. State the pass rule and the kill rule before any run. The verifier must be a different actor than the owner.
3. List what blocks it in `blocked_by` (ids from `gates.json` or other experiments).
4. Run `python lab/build_lab.py --check`. It fails on a missing kill rule, an unknown pillar or project, a budget over the lab allocation, or a running experiment past 30 days.
5. When it runs, set `status` to `running` and `clock.started`. When it ends, write `lab/results/EXP-00x.md` with the table from receipts, then set `concluded` or `killed`.

## View it

`python lab/build_lab.py` writes `lab/dist/index.html`. Open it in a browser. It is generated and gitignored; edit the JSON, not the page.

Numbers in the "Measured so far" and budget panels come from `fleet/receipts/routing.jsonl` (or `$STARLIGHT_RECEIPTS_DIR`). Synthetic receipts are ignored. No receipts means the page says so.

## Rules

- No claim without a source. Prior evidence is listed with its caveat and is never counted as a result.
- Spend caps are enforced by the gateway key budget, not by this registry. The registry only refuses plans that over-commit.
- Merges, deploys, spend and publishing stay on Frank's button.
