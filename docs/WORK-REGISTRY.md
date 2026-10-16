# Work registry — every prompt, session and run bound to one mission id, reconciled in GitHub

**Date:** 2026-10-16 · **Status:** proposed wiring plan, composes accepted decisions · **Owner:** COO General (loops), CTO General (placement), Frank gates

One question: how does every prompt, chat, cloud session, routine and swarm run get registered automatically, land on the right runtime and machine, roll up into one queue against the estate's objectives, and stay observable from anywhere, including from inside a cloud session?

The answer is not a new system. Eight of the nine primitives already exist in this estate. What is missing is a **join key** that every runtime carries, a **capture hook** at the prompt boundary, and **one reconciler** that turns those into one board. This document names what exists, what to wire, and the three things that are genuinely Starlight tech.

## Decision

1. **GitHub is the registry.** One issue per mission, one org-level Project v2 as the view, PRs and receipts as the proof. Not Linear (archive, per `ops/README.md`), not Notion, not a new cockpit (`CONTROL_PLANE.md` lock), not a second orchestrator (`SWARM-RUNTIME-ARCHITECTURE.md`).
2. **The mission id is the join key.** `M-YYYYMMDD-xxxxxx`, minted once, carried by every branch, PR, cloud session title, routine run, queue item and receipt. Without the key, a session is untracked by definition and the observer lists it as a stray.
3. **Prompts are captured locally, outcomes are published remotely.** Prompt text never leaves the machine (vault, like `starlight-memory`). GitHub gets the mission, the runtime, the hashes, the receipt verdict. This keeps private chat work private and the registry public-safe.
4. **The hub reconciles; it does not execute.** `agentic-ops-hub` already runs the off-machine dead-man (`fleet-watch.yml`), the CI watch, and the merge steward. The reconciler is one more scheduled job in the same shape: read everything, write one digest issue, never poll from a chat session.
5. **Observation from a cloud session is a routine, not a habit.** Claude Code Remote exposes `list_sessions`, `list_events`, `list_triggers`, `get_session`, `subscribe_pr_activity`. One fresh-session routine sweeps them every six hours into the digest. A human or an interactive session reads the digest.

## What already exists

| Primitive | Where | State | What it gives the registry |
|---|---|---|---|
| Ops ledger, sessions, next prompts | `ops/OPS-LEDGER.md`, `ops/sessions/`, `ops/NEXT-PROMPTS.md`, `/ops-sweep` | LIVE, manual at session end | The narrative layer and the ranked queue of next work |
| Machine queues and heartbeats | `fleet/bus/queues/to-*.json`, `pulse/<machine>` branches, `scripts/fleet_bus.py` | LIVE (c940), Book stale | Durable assign/claim per machine, liveness over git |
| Queue reconciliation | `scripts/queue_reconcile.py` | LIVE in `fleet-watch.yml` | TTL expiry, source-PR-closed rejection, stale-peer dispatch block |
| Mission envelope and outcome receipt | `scripts/mission_envelope.py`, `fleet/receipts/` | LIVE helper, used once (night loops 2026-08-06) | Candidate vs verified receipts with an independent evaluator rule |
| Signed run receipt v1 | SIS `protocol/run-receipt.v1.schema.json`, `src/run-receipt.ts`, MCP `sis.receipt.issue` / `sis.receipt.verify` | LIVE, tests in `run-receipt.yml` | The unit of proof: stages, cost, decisions, evidence hashes, DSSE signature |
| Off-machine watches | `.github/workflows/fleet-watch.yml`, `estate-ci-watch.yml` | LIVE, 6h and daily, sticky issues | The pattern every reconciler job copies: scheduled, durable issue, no polling |
| Merge steward | `.github/workflows/merge-steward.yml`, `merge-steward/` | LIVE on allow-listed repos | PR queue split by risk; approval ledger as hub issues |
| Estate ops governance | `docs/ESTATE-OPS-GOVERNANCE.md`, `scripts/rollout-ops-governance.mjs` | Built, `ESTATE_AUTONOMY` off in most repos | Per-PR sticky status, tiering, one estate digest issue |
| Routine contract and digest | FrankX `docs/ops/ROUTINE-CONTRACT.md`, `scripts/ops/routine-digest.mjs`, pack `claude-skills-library/packs/routine-contract` | LIVE for FrankX routines | Preflight, three-bullet digest, exit non-zero if the sink is unreachable |
| Trajectory memory | FrankX `scripts/workflow-trajectory.mjs` | LIVE for FrankX workflows | Recall at start, record at end |
| Multi-CLI dispatch with audit log | SIS `commands/dispatch.md`, routing `~/.starlight/routing.toml`, `routing.jsonl` | LIVE locally | Which CLI took which intent, already logged |
| Project board spec | SIS `docs/boards/PROJECT_BOARD_SPEC.md` | SPEC only, never applied (needs `project` token scope) | Column and label vocabulary for the Project v2 |
| Local memory gateway and signed read-only cloud projection | `starlight-memory` | LIVE locally, cloud projection locally verified | The privacy model the prompt vault copies |
| Spec-trace daemon on the tailnet | SIS `tools/spec-trace-daemon/` behind `tailscale serve` | LIVE local | The pattern for exposing a local read endpoint to phone and Book |
| Queen intake with issue-bound task envelopes | private `agentic-ops` `lifecycle/slack-queen.py`, admission, controller (Ops234) | MERGED_NOT_LIVE, activation held on RAM and cost gates | The eventual durable owner of long-running missions; not a dependency of this plan |
| Runtime placement doctrine | `docs/SWARM-RUNTIME-ARCHITECTURE.md`, FrankX `docs/ops/RUNTIME-STRATEGY.md` | Accepted | The rule that decides local vs CCR vs Cloudflare vs Vercel vs Railway |

## What is missing

- **No join key.** A local Claude tab, a CCR session, a Codex Cloud task, a FrankX routine and a queue item in `to-c940.json` describe the same work with five unrelated identifiers. Nothing joins them.
- **No capture at the prompt boundary.** Session history lives in each harness's own `.jsonl`; the estate only learns about a session when someone runs `/ops-sweep` and reads git. Work that produced no commit is invisible.
- **No session index across runtimes.** CCR sessions, Vercel agent runs (`list_agent_runs`), Cloudflare workflow instances and local tabs are each listable from their own API and from nowhere else.
- **No single view.** The board spec exists; the Project was never created. `NEXT-PROMPTS.md` is the queue, but it is prose and only one harness can edit it at a time.
- **Objectives are implicit.** `fleet/clone-manifest.json` `production_targets` P1..P6 is the only ranked objective list. Nothing ties a session to a target, so "which team executes where against which goal" is a question answered by reading.

## Architecture

```
 PROMPT BOUNDARY (local, private)            RUNTIMES (replaceable execution)          REGISTRY (GitHub)
 ┌───────────────────────────────┐           ┌───────────────────────────────┐          ┌──────────────────────────────┐
 │ Claude Code / Codex / Gemini  │ mission   │ CCR sessions + routines       │ receipt  │ issue  <mission id>           │
 │ Grok / Antigravity on c940,   │──id────▶  │ Codex Cloud, Jules, Managed   │──PR/────▶│ labels: mission, runtime:*   │
 │ Book: hooks mint/claim id,    │           │ Cloudflare Workflows (Queens) │ comment  │ Project v2 fields            │
 │ append prompts.jsonl, emit    │           │ Vercel Workflows (per app)    │          │ receipts/ in hub or SIS      │
 │ receipt draft on Stop         │           │ Railway workers               │          └──────────────┬───────────────┘
 └──────────────┬────────────────┘           └───────────────────────────────┘                         │
                │ pulse/<machine> heartbeat + mission summary (git, no secrets)                        │ 6h
                ▼                                                                                      ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ RECONCILER (agentic-ops-hub, scheduled Actions, public repo so it fires when private Actions budget is 0)  │
 │ fleet-watch (liveness) · queue_reconcile (TTL, PR state, issue state) · project_sync (issues → Project)    │
 │ session-index (CCR + Vercel runs → missions) · one sticky "Estate digest" issue · Slack DM on red          │
 └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                │ tailnet only: spec-trace daemon, mission-ledger read endpoint (tailscale serve), Tailscale SSH Book→c940
```

Placement stays as decided: a mission's **durable owner** is Git for interactive work, Cloudflare Workflows for anything that must survive a machine being off, Vercel Workflows for a job of one app, Railway for replaceable workers. The registry does not move work; it records where work is and whether it finished.

### The mission envelope v1

A mission is a GitHub issue whose body opens with one fenced block. The same object is the `active[]` item shape in `fleet/bus/queues/to-*.json` (it already requires unique id, repo/branch/path bindings, TTL and content hash) and the `subject` of a run receipt.

```yaml
mission: M-20261016-7f3a2c
objective: P2            # clone-manifest production_targets id, or `ops` / `research`
runtime: local-c940      # local-c940 | local-book | ccr | codex-cloud | cloudflare | vercel | railway
lane: claude-max         # subscription lane per fleet/CLI-MAX-SWARM.md
repo: frankxai/FrankX
branch: agent/claude/gencreator-bridge
tier: STANDARD           # risk tier from the estate classifier
ttl_hours: 72
owner: queen:content | human:frank
receipt: null            # sha256 of the latest run receipt, set by the Stop hook or the routine digest
```

Status is a Project field, not issue text, so a bot can move it without rewriting prose. Labels mirror the two axes the board filters on: `runtime:*` and `objective:P*`.

### Prompt capture (the vault side)

`~/.starlight/missions/<mission>/prompts.jsonl`, one line per submitted prompt: `ts, harness, repo, branch, session, prompt_sha256, prompt`. Append-only, machine-local, never committed. The Stop hook writes `receipts/<session>.json` next to it, an unsigned run-receipt v1 draft (stages: prompts seen, files touched, commits, tests run with exit codes). `starlight-memory` indexes the folder like any vault folder, so `memory_recall` answers "what did I ask about X in July" from any harness. The only thing that leaves the machine is the receipt hash on the pulse branch and, when a mission issue exists, one comment with the three-bullet digest.

## Who already built what we need

| Need | Adopt | Why this and not our own |
|---|---|---|
| Registry, board, cross-repo queue | GitHub Issues, Project v2 (`gh project`, GraphQL), sub-issues, issue types | Already the action record per `ops/README.md`; `project-board-sync` and `github-project-management` skills exist in the library |
| Off-machine scheduler that survives a dark c940 | GitHub Actions `schedule` in this public hub | Proven by `fleet-watch.yml`; public repo keeps firing when private Actions minutes are exhausted |
| Cloud sessions and routines, observable by API | Claude Code Remote (`list_sessions`, `list_events`, `list_triggers`, `send_later`, `subscribe_pr_activity`, `create_trigger`) | It is the runtime this plan is written from; routines already obey the routine contract |
| Delegated bounded builds | Codex Cloud, Jules, Claude managed agents, Copilot coding agent (`assign_copilot_to_issue`) | Replaceable execution under `SWARM-RUNTIME-ARCHITECTURE.md`; returns a PR, which the registry already tracks |
| Durable long-lived agent state | Cloudflare Workflows + Agents SDK + Durable Objects | Accepted 2026-10-04; a Queen per stream, a steward per registry row |
| Per-app jobs and sandboxed steps | Vercel Workflows, Vercel Sandbox, Vercel agent runs (`list_agent_runs`, `get_agent_run_trace`) | Accepted; runs are already listable, so the session index can read them |
| Replaceable workers and crons | Railway | Accepted as workers only; each job ends in a receipt or it did not run |
| Local reachability, phone and Book access | Tailscale (`tailscale serve` for read endpoints, Tailscale SSH for Book→c940, Funnel only for a signed read-only projection) | Already the pattern for the spec-trace daemon; Tailscale is transport, never the registry |
| Prompt-boundary hooks | Claude Code hooks (`SessionStart`, `UserPromptSubmit`, `Stop`), Codex `notify`, the pack `install.sh` pattern | Three packs already ship this way (`web-excellence`, `estate-guard`, `routine-contract`) |
| Session telemetry | Claude Code OpenTelemetry export to a collector on the tailnet, Langfuse EU for traces and cost | Thin-overlay doctrine in SIS `THIN_INFRASTRUCTURE_CHECKLIST.md`: rent observability |
| Signed proof | SIS run receipt v1 (DSSE, in-toto, Ed25519) | Already implemented and tested; nothing to invent |

Nothing in that table needs to be written from scratch. The three Starlight pieces below are the glue and the policy.

## Starlight tech to build

1. **`packs/mission-ledger`** in `claude-skills-library`. Hooks plus one CLI (`starlight mission start|prompt|stop|claim`) so every harness can register the same way even where hooks differ. `SessionStart` resolves the mission from `STARLIGHT_MISSION`, from the branch name, or by claiming the top entry of `ops/NEXT-PROMPTS.md` and minting an issue when none exists. `UserPromptSubmit` appends to the vault. `Stop` writes the receipt draft, updates the pulse branch, and comments the digest on the issue if one is bound. Vendored copies land in each repo through `install.sh`, tests stay upstream, exactly like `estate-guard`.
2. **`scripts/session_index.py` + `scripts/project_sync.py`** in this hub, run by one new `work-registry.yml` on the `fleet-watch` cadence. `session_index` lists CCR sessions and triggers, Vercel agent runs, open PRs with `Mission:` in the body, pulse heartbeats and receipts, and maps each to a mission or flags it as a stray. `project_sync` ensures every `mission` issue is on the Project with fields set from the envelope, and moves Status from receipt verdicts (PASS with a merged PR → Done, FAIL → Blocked, TTL elapsed → Expired). Both extend `queue_reconcile.py` rather than replacing it, and write one sticky issue, "Estate digest", the same way `fleet-watch` does.
3. **The observer routine.** One CCR trigger, fresh session per fire, every six hours, prompt: run the two scripts' read-only mode against the live APIs the hub cannot reach without secrets (CCR session list, Vercel runs), commit the index under `fleet/reports/sessions/<date>.json`, update the digest issue, Slack DM only on red. It obeys the routine contract: preflight, no `Workflow({...})`, digest last, non-zero if nothing persisted.

## Wiring plan

Each phase ends in a durable sink. Phases 1 and 2 need no new credentials. Phase 3 needs one token with `project` scope in the hub's environment, the same shape as the merge steward. Nothing here starts a local worker, so the c940 RAM HOLD does not block it.

| Phase | Do | Sink | Gate |
|---|---|---|---|
| 0. Vocabulary | Land this doc; add `mission:`, `runtime:*`, `objective:P*` labels to the hub; add the envelope block to `ops/NEXT-PROMPTS.md` entries going forward | this PR | none |
| 1. Capture | Build `packs/mission-ledger` (hooks, CLI, tests); install into `agentic-ops-hub`, `FrankX`, `Starlight-Intelligence-System` first; prompts stay in `~/.starlight/missions/` | PR in `claude-skills-library`, one install PR per repo | estate-guard scan on the hook files |
| 2. Index and reconcile | `session_index.py`, `project_sync.py --dry-run`, `work-registry.yml`; extend `queue_reconcile.py` with `source_issue`; first run writes `fleet/reports/sessions/` | hub PR, then the sticky "Estate digest" issue | hub CI |
| 3. Board | Create the org Project from `PROJECT_BOARD_SPEC.md` columns with the fields above; store the `project`-scoped token in a `work-registry` environment restricted to `main`; flip `project_sync` to write | the Project, one issue per active mission | Frank creates the token (human gate, same as merge steward) |
| 4. Cloud runtimes | CCR session titles carry `[M-…]`; routine prompts include `--mission`; Vercel Workflows and Railway jobs end with `sis.receipt.issue`; Cloudflare Queens write their row's receipt on every tick | receipts in `fleet/receipts/` or the issue | each runtime's own PR |
| 5. Observe from anywhere | The observer routine; `tailscale serve` for a read endpoint of the local index on c940; Book and phone read it; cloud reads the digest issue | `fleet/reports/sessions/`, digest issue, Slack DM | routine contract preflight |
| 6. Learn | Trajectory record per mission (`workflow-trajectory.mjs` pattern generalised to the mission folder); `memory_recall` over the prompt vault; weekly COO pulse reads the Project instead of the ledger prose | vault, `ops/sessions/` | none |

## Observing from a cloud session (this session's tools)

A chat session does not poll. It reads the digest and acts once. The calls it has, when it does need live state: `list_sessions` (titles carry the mission id), `get_session` (status bucket, served model), `list_events` with `kinds: [user, assistant, result]` to read what a sibling did, `list_triggers` for the routine registry, `subscribe_pr_activity` for the PRs it owns, `send_later` for one safety-net check-in. The observer routine is the only thing allowed to call these on a schedule.

## Guardrails

- No new cockpit, no second hub, no second orchestrator. The view is a GitHub Project; the human dashboard stays `starlight-command-center`.
- Prompt text, transcripts and vault contents never enter an issue, a PR or a public branch. Hashes and digests only. A pack that leaks prompt text fails its own test.
- The registry records; it never dispatches. Dispatch stays with the queue files, the Queen admission once live, and the human.
- A run with no receipt is not done. A green run that committed nothing is red (routine contract).
- Secrets live in hub environments restricted to `main`, never in target repos.
- L7 hard stops are unchanged: money, newsletter sends, social posts, production force-pushes stay human.

## Acceptance

The plan is live when, for one real week:

1. Every CCR session and every local session on c940 appears in `fleet/reports/sessions/<date>.json` with a mission id or as a named stray, and the stray count trends to zero.
2. The Project shows every open mission with runtime, objective and status, and the status moved at least once without a human editing it.
3. `memory_recall` answers a question about a prompt that produced no commit.
4. The digest issue was updated by the reconciler on schedule while c940 was off at least once.
5. Nothing in GitHub contains prompt text.

## Related

`CONTROL_PLANE.md` · `SWARM-RUNTIME-ARCHITECTURE.md` · `ESTATE-OPS-GOVERNANCE.md` · `MERGE-STEWARD.md` · `fleet/activity/README.md` · `fleet/FLEET-OPS.md` · FrankX `docs/ops/ROUTINE-CONTRACT.md` and `SCHEDULED-ROUTINES.md` · SIS `docs/boards/PROJECT_BOARD_SPEC.md` and `protocol/run-receipt.v1.schema.json` · `starlight-memory` `docs/CLOUD_GATEWAY.md`
