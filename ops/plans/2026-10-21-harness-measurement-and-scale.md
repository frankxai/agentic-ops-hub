# Harness measurement and scale (plan, 2026-10-21)

Author: Claude Code. Status: proposal for Frank. Registry entries: `lab/harnesses.json`, `lab/packs.json`, EXP-008, EXP-009. Nothing here spends money; every run needs the gates in `lab/gates.json`.

Question this answers: how good is our harness today, how do we compare **now** (opencode + OmO + routing brain), **OmO** (stock), **OmS** (oh my starlight) and **starlight-ai-harness** (the public template), and how do we run tests, playbooks, skills and experiments across many harnesses at large scale without fooling ourselves.

## 1. The four names are four layers (already decided)

From `agentic-ops/fleet/HARNESS-STACK.md` (v1, 2026-10-21): L0 commodities (opencode, OmO plugin, gateway, models, Claude, Codex), L1 SIS memory, L2 routing brain (the moat), L3 **OmS** (our packaged config, governance and receipts layer, no fork of OmO), L4 **starlight-ai-harness** (public template repo: OmS plus playbooks, evals, setup docs). "now" is L0 plus L2 as installed today. This plan keeps that naming and adds no new layer.

## 2. Honest state and quality today

Grades are my judgement from what exists, not measurements. A means evidence supports it, C means it exists but is unproven, F means missing or broken.

| Part | What exists | Quality | Why |
|---|---|---|---|
| Routing Brain design (classes, chains, ZDR, reserve/settle) | Built and live on one box | **C+** | Good design, but 4 Codex rounds each found new leaks (65 -> 71 tests). Only 5 test receipts, no real measurement. |
| Classifier | Fail-closed rewrite on PR 377 | **C** | Verb lists lost the game every round; policy decision pending (Option A in progress). |
| Harness battery (`harness_eval.py`) | **Unverified in this branch:** reported as 4 toy tasks, 16 stored rows, n=1 per cell. `fleet/harness_eval.py` and the stored rows are not tracked here or in PR 377's tree, so the figures are not bound to a source SHA | **D** (unverified) | Calls the gateway, so it ranks **models**, not harnesses. No software, website or content tasks. One line in the file has a merged comment (`_check_code# ---`), a sign it was not reviewed. |
| SIS Model Arena (`tools/arena`) | Rounds R1-R5 as receipts, pre-registration, blind judge, traps | **A- for method** | Best method in the estate. Claude-subagent only, not harness-neutral. We reuse its rules. |
| "now" OmO config | Installed 5.1.40; `~/.omo/omo.jsonc` is the old generator output | **C-** | Stale; PR 377 changes fallbacks; not regenerated. |
| OmS | `gen_omo_config.py` exists, profiles not split | **F (not built)** | No package, no free versus Token Pass profile, no battery gate. |
| starlight-ai-harness | Nothing | **F (not built)** | Phase 3 in HARNESS-STACK; blocked by OmS evals. |
| Receipts | Three schemas (routing.jsonl, SIS run-receipt v1, Queen's signed receipt) | **C** | Cannot compare across harnesses until one schema is chosen (`dec-receipt-schema`). |
| Cloud worker | Plan only | **F** | EXP-004 and the ledger's `railway-ci-runners` overlap; reuse the ledger's findings. |
| Skills and playbooks | Skill Foundry has `claude plugin eval --ablation with-without` | **C** | Tooling exists; the three playbooks are not written; no saved evals. |

The headline: **we have good method and good design, and almost no measurement.** The first job is to produce real numbers, not more architecture.

## 3. What "accepted" means (the unit of measure)

A task is **accepted** only when a verifier that is a different actor than the maker has passed it: a test suite, a script, a mechanical gate, or a blind judge from another model family. "The agent said it passed" never counts. Every accepted task has a receipt carrying: harness id, model, class, cost, wall time, attempts, tool calls, human interventions, ZDR status, verifier id.

Primary metric: **cost per accepted task**. Secondary: accepted rate, first-try accepted rate, trap pass rate, median wall seconds, interventions per task. Guardrails (any breach stops the run): a ZDR task on a non-ZDR model, a secret-shaped string in a changed file, spend over cap, a receipt that fails recomputation.

Subscription harnesses (Claude Code) are not metered by the router. Compare them on accepted rate and wall time, report cost as "not metered", and never mix them into cost-per-accepted tables.

## 4. How we compare now, OmO, OmS and the template

EXP-008 is the direct test: arms `opencode-bare` (control), `omo-stock` (stock OmO, no routing brain), `now` (OmO plus the routing brain as installed today), `oms` (routing brain chain per class). Same packs, same order, same per-task wall budget, paired comparison. Pre-registered before data. The pass rule is in the experiment; in short, OmS is kept as a named layer only if it holds accepted rate within 3 points of stock OmO (the `omo-stock` arm), costs 30% less per accepted task, has zero ZDR violations and complete receipts, and does not do worse on traps. If it only matches on cost, we say the value is governance and receipts, not quality.

starlight-ai-harness is not an arm. It is the **output**: it ships only after OmS passes EXP-008, and its README claims only what the result file shows.

Statistics rules: at least 10 runs per harness and task cell before any claim (SIS doctrine A2); below that the report says "directional" and decides nothing. Report intervals from a paired bootstrap, not just means. Watch contamination: public benchmarks may be in training data, so core-v0 replays private repo PRs. Record judge family and keep the judged share of any pack at or below half.

## 5. What the harness must help build, and how each is checked

| Capability | Pack | Playbook | Mechanical checks | Project |
|---|---|---|---|---|
| Software | `starlight-core-v0` | build-a-product | The PR's own test, no regressions, diff scope | agentic-ops, sis, acos |
| Websites | `web-v0` | build-a-website | Playwright structure, axe zero serious, no horizontal scroll at 390 and 1280 px, Lighthouse floor, blind visual judge (capped) | frankx, arcanea |
| Content | `content-v0` | (content playbook, later) | Constraint script, every citation resolves, no cross-brand terms, blind voice judge for ties | frankx, arcanea |
| Agentic safety | `agentic-traps-v0` | n/a | Governance trap, injection, lying docs, contradictory spec, secret in config | all |
| Experiments | n/a | run-an-experiment | `build_lab.py --check` passes and a kill rule is stated | agentic-ops |

One real example of why the website gate matters: our own lab dashboard overflowed at 400 px and the first screenshot hid it. The `web-responsive` check would have caught that at build time.

## 6. Playbooks and skills

Lifecycle, using Skill Foundry: draft the playbook, save its eval, run `claude plugin eval --ablation with-without` by a judge that did not write it, then pair it with a pack task (EXP-009). A playbook enters the default prompt only if it passes at n of at least 10 per arm and stays inside the 8,000-token listing cap. Skills that never trigger are retired. Nothing goes into the default prompt without a saved eval (estate override).

## 7. Scale protocol (how we get to "massive" safely)

Cost is the constraint, so size every run before starting it: `runs = harnesses x tasks x n`, `cost = runs x cost per attempt`.

Illustration, with caveats: 3 arms x 20 tasks x 10 runs = 600 attempts. A public leaderboard lists DeepSeek V4 Flash at about $0.01 per test and Kimi K3 at about $0.76 per test (Vals, mini-SWE-agent, archived; different task, different harness, unverified for our tasks). At those rates 600 attempts cost roughly $6 versus roughly $456. The lab allocation is $30 of Token Pass, so **the model choice decides whether n can be 10**. EXP-001 (Flash against GLM) comes first because it sets the unit cost for everything after.

| Tier | Size | Where | Cost guard | Purpose |
|---|---|---|---|---|
| T0 smoke | 4-10 tasks, 1 run | Free rail, nightly | $0 | Liveness: did a model or harness break |
| T1 pack | 1 pack, n=10 per cell | Railway worker, one arm at a time (EXP-001, 006, 007, 009 are T1; EXP-002 and EXP-008 are T2; EXP-003 is T3; EXP-004 and EXP-005 are T0). EXP-001 and EXP-006 are first designed as one-run-per-cell directional pilots (`design.decision_effect` none): they change no routing until a 10-per-cell confirmation runs | reserve/settle cap per run | First real numbers (EXP-006 free-only first, then EXP-001) |
| T2 compare | 3-4 arms, paired, n=10-30 | Railway, serial or low parallelism | experiment cap ($4-8) | Decisions (EXP-008, EXP-002) |
| T3 massive | n of 100 or more, swarm arms (EXP-003) | Railway or another cloud, never the laptop | only after cost per accepted is known and Frank sets the cap | Genius-scale sweeps and training the routing table |

Rules for every tier: runs are preregistered; each run reserves budget before it starts; the runner stops on the first guardrail breach; the laptop (YELLOW zone, below its RAM floor) never runs T1 or higher; results are files in `lab/results/` generated from receipts, never typed.

## 8. Order of work

1. Close PR 377 (Option A classifier and ledger fixes in progress, then a signed SHA from a different harness).
2. Decide the receipt schema (`dec-receipt-schema`).
3. Build the harness-neutral runner (`harness-runner`). Until it exists, nothing can rank harnesses.
4. Curate `starlight-core-v0` (`suite-curation`) and author `web-v0` and `content-v0` (`pack-authoring`).
5. Run T1: EXP-006 (free-only, $0) then EXP-001 (Flash against GLM).
6. Pre-register and run EXP-008, then EXP-002 and EXP-003 if the runner supports them.
7. Draft and ablate the three playbooks (EXP-009). Package OmS only after EXP-008. Publish starlight-ai-harness last.

Known gaps and risks: native omo, pi and fx headless modes are unverified; checker tools (axe, Playwright, Lighthouse) are not confirmed in the worker image; the Token Pass key and Railway cap are Frank's; `agentic-traps-v0` needs a harness-neutral runner before it can compare harnesses.
