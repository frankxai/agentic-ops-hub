# Research lab and cloud workers (plan, 2026-10-21)

Author: Claude Code. Status: proposal for Frank's approval. Nothing here spends money or installs software.

## What was decided and why

| Question | Answer | Evidence and limits |
|---|---|---|
| Fork or rebuild OmO? | No. Build **oh-my-starlight** as a config, governance and receipts pack that targets upstream OmO and opencode. | OmO's licence (SUL-1.0) allows internal use and free non-commercial distribution only, so a public fork can never be part of a commercial product. It releases several times a week, so a fork is permanent merge debt on code that is not our moat. |
| Is OmO's swarm reachable? | Yes, through the native `omo` binary (built on senpi, a pi fork), not the opencode plugin we run today. | Read from the OmO 5.1.40 package README. Headless mode and Gateway support are unverified, so EXP-002 tests them. |
| Is DeepSeek V4.1 Flash good enough to use? | Use it now for bulk and as a candidate default coder. Do not make it the code primary until EXP-001 passes. | A leaderboard (vals.ai, mini-SWE-agent) lists V4 Flash 0731 at 88.8% on SWE-bench Verified for about $0.01 per test, against Kimi K3 at 93.4% for $0.76 and GLM 5 at 71.4%. That benchmark is public and archived, the version name differs from our route (v4.1-flash), and one user report prefers GLM on design bugs. It is a strong reason to test and not proof. |
| Which harness on Railway? | opencode headless first, because it already runs with free and Gateway models and has a receipts wrapper. pi, native omo and fx are challengers in EXP-002. | The only pi-versus-omp number is a vendor blog on one model. The experiment replaces it with ours. |
| Always-on or activated workers? | Start activated (webhook or cron), one worker, hard caps. Measure before choosing. | Railway sleep and pricing behaviour are unverified. EXP-004 measures them. |
| Where do we track all this? | Git is the record. A generated private HTML page is the dashboard. An Artifact is a shareable snapshot. Not Notion. | One source per concern. A page generated from reviewed JSON cannot drift from the registry, and CI fails if the registry breaks its own rules. |

## The lab

`lab/` is a registry of S1 experiments in the estate lifecycle (`registry/README.md`: hypothesis, metric, token budget, 30-day limit, exit by scorecard).

- `lab/goals.json`: north star, four pillars (routing brain, harness tech, cloud workers, ecosystem) and the estate projects.
- `lab/experiments/EXP-*.json`: one file per experiment. Every one has a hypothesis, arms, a pass rule, a kill rule, spend caps, a verifier who is not the owner, and the decision it feeds.
- `lab/gates.json`: decisions that need Frank and work items that block experiments.
- `lab/budget.json`: Token Pass allocation, Railway cap, gateway key caps.
- `lab/build_lab.py`: validates the registry (`--check`) and renders the dashboard. CI runs both.

Build the page: `python lab/build_lab.py` writes `lab/dist/index.html` (gitignored). Add `--artifact` for a fragment to publish.

The dashboard shows measured numbers only from real receipts in `fleet/receipts/routing.jsonl`. Synthetic and malformed lines are counted and ignored. With no receipts it says so.

## Experiments

| Id | Question | Cap | Blocked by |
|---|---|---|---|
| EXP-001 | Flash vs GLM 5.3 as default coder | $6 + $1 infra | key rotation, PR 377, suite, worker Phase 0 |
| EXP-002 | Harness bake-off on one model (opencode, pi, omo, fx) | $8 + $3 infra | key, suite, worker Phase 0 |
| EXP-003 | OmO swarm vs best single agent | $4 + $1 infra | EXP-002 |
| EXP-004 | Always-on vs activated worker | $3 infra | Railway cap approval, worker Phase 0 |
| EXP-005 | Cost of strict ZDR routing | $0 | PR 377, ZDR decision |
| EXP-006 | Ceiling of free-only models (one free arm, no paid reference) | $0 + $1 infra | suite, worker Phase 0 |
| EXP-007 | Eve vs Railway worker for issue to draft PR | $5 | what "software factory" means, EXP-004 |

Committed caps: $27 of the $30 Token Pass lab allocation, $11 of the proposed $20 Railway cap. The validator rejects a registry that goes over.

## Cloud worker phases

- **Phase 0 (no spend beyond caps):** container with opencode headless, entrypoint that takes a task and a task class, its own Token Pass key with a $30 budget, receipts written out and pulled into the ledger. Needs PR 377 merged and the key created.
- **Phase 1:** trigger by GitHub issue label or cron, output is a draft PR on `agent/<harness>/<scope>`, a different harness signs the SHA, weekly digest from receipts. No auto-merge.
- **Phase 2 (only if EXP-004 and EXP-007 justify it):** second worker lane, Eve on Vercel, always-on lane.

## Safety rules that apply to every experiment

- The worker gets its own Token Pass key and cap. The exposed key is rotated first.
- Install harnesses in the container, from pinned packages, with telemetry off. Never `curl | sh`.
- Do not run `omo setup` against a config that holds live keys.
- Merges, deploys, spend and publishing stay on Frank's button.

## Follow-up PRs (not in this one)

1. Experiment runner (`lab/run_experiment.py`): replay a task at its parent commit in a temp worktree, run a harness headless, run the task's test, write a receipt with `experiment` and `harness` fields. Needs PR 377 merged for the receipt API.
2. Suite `starlight-core-v0`: 12 closed estate PRs with tests, spread over the task classes.
3. `gen_omo_config.py --profile free|tokenpass`.
4. Worker Phase 0 container.
