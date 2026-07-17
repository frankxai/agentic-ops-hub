# Six-Hour Swarm Retrospective and Campaign Retrofit

**Date:** 2026-07-17

**Mission window reviewed:** 05:35–11:35 Europe/Amsterdam

**Verdict:** under-delivered; orchestration activity was mistaken for an engineering campaign.

## Executive truth

Frank is right: the result was far too small for the mandate and available subscriptions.

The preserved mission delivered:

- one draft documentation PR in `starlight-communities`;
- one architecture review comment on SIS PR #42;
- no code-bearing product fix;
- no new regression test;
- no CI, security, dependency, or performance improvement;
- no merge or deployment;
- no acknowledged C940 implementation receipt.

The 30-minute driver was configured for 11 ticks but ran only 2 and was paused at 07:10. The founder handoff job was also paused and never ran. Scheduling a six-hour window was not the same as executing six hours of work.

The README PR was valid and the SIS review was useful, but together they were not proportional to the requested cross-portfolio engineering and executive mission.

## What I did wrong

### 1. I optimized for low-collision work instead of highest-value outcomes

I selected a clean documentation target because it was safe. That reduced conflict risk, but it also avoided the highest-impact product, revenue, activation, reliability, and testing work. Safety was a valid constraint; choosing a low-impact deliverable as the primary campaign outcome was my decision.

### 2. I treated agent diversity as an objective

Claude, Codex, OpenCode, Grok, AGY, and Dcode were invoked or probed, but several were assigned duplicate reviews or vague executive perspectives. Agent count is not portfolio progress. Every paid lane should have owned a distinct artifact or independently verified one.

### 3. I had no objective graph

The mission was not compiled from:

`estate outcome → selected campaign objective → repo → maker → verifier → artifact → test → receipt`

Without that chain, the scheduler could not distinguish useful work from motion. The new `objectives-registry.json` restores the missing front door for all 23 current estate outcomes.

### 4. I did not plan subscription windows

Live quota at retrofit time:

| Pool | Plan | Remaining | Decision |
|---|---|---:|---|
| Claude | Max 20x | 78% weekly / 93% session | Under-used; allocate to hard implementation and high-judgement review |
| Codex | Pro | 55% current window | Healthy; make this the primary implementation/integration lane |
| Grok Build | subscription pool | 2% weekly | Stop new Grok work until reset; use only when uniquely necessary |
| OpenCode | unmetered/free route | not quota-tracked | Scout, low-risk batch work, and independent verification |
| AGY | installed/authenticated but unmetered by tracker | unknown | Use only after a bounded real-response smoke test; one retry then fallback |
| Dcode | no working provider auth | unavailable | Remove from campaign capacity until health check passes |

I routed work to Grok while its pool was almost exhausted and left most Claude/Codex capacity unused. That is the opposite of subscription optimization.

### 5. I used cost-equivalent budgets as if they were subscription controls

The existing Token Planner used dollar envelopes. Those are useful for API-equivalent accounting, but they do not control Claude Max or Codex Pro quota windows. The retrofit keeps the envelopes for comparison while adding live remaining-percentage floors and per-agent quota ownership.

### 6. I accepted reports as completion

The old planner marked any non-empty report file complete. That rewards prose and permits audit theater. Campaign mode now requires:

- matching mission and objective IDs;
- `outcome_status: VERIFIED`;
- `execution_status: ok`;
- every required artifact to exist and be non-empty;
- every required verification ID to be present with `status: passed` and a command;
- a machine-readable receipt.

A report without proof now returns `missing-receipt`.

### 7. I had no hard failure/fallback matrix

AGY timed out twice, Dcode was unauthenticated, one Codex lane exited `-1`, and Grok produced weak/no captured output. I retried but did not immediately reassign each failed artifact contract to a healthy fallback. Failures consumed the timebox without preserving outcomes.

### 8. I did not capture agent output durably

Several CLI calls returned collapsed output. A successful exit without a report, diff, test result, or receipt is not auditable. Future prompts must write their result and receipt to paths inside the selected worktree before the process exits.

### 9. I overused orchestration surfaces

The current one-day Hermes aggregate—not attributable solely to this mission—shows:

- 4,341 tool calls;
- 1,803 terminal calls;
- 1,493 file reads;
- 840 skill loads;
- 590 todo calls;
- 229 whole-file writes and 196 patches;
- 78 cron sessions;
- 107 distinct skills loaded.

The corresponding Hermes accounting reports 205.7M total tokens; Tokscale reports 424.0M tokens and $308.75 of API-equivalent usage across a wider client/cache boundary. The mismatch itself proves that usage is not yet attributed consistently to objectives and receipts.

The problem is not merely “too many tokens.” It is that tokens, tools, and cron sessions were not tied to verified outcomes.

### 10. I dispatched into an offline queue

C940 had no live heartbeat or acknowledged implementation receipt. The durable bus contained many pending packets. Adding more packets to an unavailable machine created dispatch theater, not parallelism.

### 11. I failed to verify the autonomous campaign after launch

My handoff said the mission was live. That was technically true for the schedule at that moment, but it implied sustained execution. I should have said “scheduled, not yet demonstrated,” and I should not have treated it as complete until the final receipt existed.

## Constraints that were real—but not excuses

- C: started around 35.7 GiB free, below the CRITICAL threshold.
- Storage later recovered above 50 GiB and measured 250.51 GiB free at the current campaign admission.
- Several flagship repositories already had active or dirty lanes.
- C940 was offline.
- AGY, Dcode, and some CLI output capture failed.

These conditions justified narrower concurrency and no unsafe fanout. They did not justify spending the available time mostly on review and coordination. Once storage recovered, I should have opened one bounded code-bearing lane in the highest-value available repository and used a second healthy model only as verifier.

## The replacement operating system

### 1. Objective registry

`objectives-registry.json` now enumerates all 23 current estate outcomes from the canonical repo-contract catalog. Every campaign selects no more than three top-level objectives. Tier-0 outcomes must receive a verified progress receipt at least weekly; `now` outcomes at least every 14 days.

This does not mean editing 23 repositories every week. It means the scoreboard makes neglect visible and forces explicit sequencing.

### 2. Campaign contract

Every mission must declare:

- objective ID and measurable outcome;
- executive owner;
- repo, exact branch, role, and quota pool;
- maker or verifier responsibility;
- required artifacts;
- verification IDs;
- turn, time, and quota envelope;
- report and receipt paths;
- wave number and stop conditions.

### 3. Subscription-aware router

Before every wave:

1. Read live Tokscale quota.
2. Block pools below their remaining-percentage floor.
3. Route to the first healthy fallback with an explicit agent profile.
4. Preserve quota snapshot in run state without account identity.
5. Compare before/after quota by campaign and objective.

Current floors are Claude 15%, Codex 15%, and Grok 10%. OpenCode is marked unmetered; AGY is allowed only as unmeasured capacity after a real-response smoke test.

### 4. Comparative-advantage assignments

| Lane | Default responsibility | Not allowed to substitute for |
|---|---|---|
| Hermes | Objective selection, admission, routing, receipts, escalation | Product implementation |
| Claude | Hard multi-file implementation; architecture; independent high-judgement review | Repetitive repo surveys |
| Codex | Primary implementation, tests, integration, deterministic repair | Generic executive commentary |
| OpenCode | Cheap scouting, small low-risk tasks, independent diff verification | Security-critical production decisions |
| Grok | Current research, CMO/CEO signal, image/video direction when quota is healthy | Routine orchestration while depleted |
| AGY | Large-context or visual lane after health smoke | Repeated headless retries |
| Dcode | No assignments until auth and smoke pass | Nominal roster coverage |
| C940 | Backend, GitOps, CI, long-running tests after acknowledged lease | Unacknowledged queue accumulation |
| Yogabook | Frontend, premium UX, command center, final integration | Heavy backend fanout when RAM is constrained |

### 5. Maker/verifier pairing

One agent writes; a different agent verifies the diff and tests. Never spend Claude and Codex on two generic reviews of the same unchanged surface. The verifier begins only when a code or design artifact exists.

### 6. Wave scheduler

A six-hour campaign becomes:

| Time | Wave | Required result |
|---:|---|---|
| 0:00–0:15 | Admission | live quota, disk/RAM, heartbeat, repo ownership, selected objectives |
| 0:15–1:45 | Maker wave 1 | code/design artifact plus local tests |
| 1:45–2:15 | Verifier 1 | independent diff/test verdict and bounded fixes |
| 2:15–3:45 | Maker wave 2 | second objective or integration follow-up |
| 3:45–4:15 | Verifier 2 | proof, review, regression gate |
| 4:15–5:15 | Product/executive lane | pricing, UX, GTM, data, or observability artifact connected to shipped product proof |
| 5:15–6:00 | Integrator | receipts, draft PRs, issues for holds, objective scoreboard, founder handoff |

On Yogabook, default `max_concurrency` is 1 when RAM is tight and 2 only when capacity is healthy. C940 adds capacity only after heartbeat and lease acknowledgement.

### 7. Token allocation rules

- Maximum 15% of a campaign's model budget for discovery and repo mapping.
- Maximum one planning pass before implementation starts.
- No second review model until an artifact exists.
- Reserve 20% of each healthy paid pool for verifier/integration work.
- Use Claude for complexity, Codex for throughput, OpenCode for cheap breadth, Grok for unique current-signal work.
- Stop or fallback after one bounded retry.
- Context packs contain only the objective contract, repo instructions, relevant definitions/usages, and test command—not the full estate history.
- Track tokens per verified artifact, per accepted PR, and per objective—not only per client.

### 8. Outcome scoreboard

The weekly dashboard must show:

- verified outcomes by objective;
- objectives with no receipt inside their SLO;
- PRs opened, accepted, merged, or held;
- tests added and regressions prevented;
- cycle time from mission admission to receipt;
- tokens and quota percentage points per verified outcome;
- maker/verifier rework rate;
- agent timeout and fallback rate;
- unacknowledged swarm packets and expired leases.

## Definition of a successful six-hour campaign

A future six-hour run is successful only if it returns at least:

- two verified objective receipts;
- at least one code-, test-, design-, or revenue-bearing artifact;
- one independent verifier verdict per consequential artifact;
- one reviewable draft PR or an explicit HOLD with reproducible blocker and issue-ready acceptance criteria;
- live before/after subscription snapshots;
- no duplicate writers, unsafe branches, red CI merge, unauthorized deploy, or fabricated peer heartbeat.

“Agents invoked,” “tokens spent,” and “reports written” are diagnostic metrics, never the headline.

## Current retrofit evidence

Implemented on `agent/hermes/objective-campaign-v2-20260717`, based on current `origin/main`, in the canonical `agentic-ops-hub` worktree:

- campaign-mode objective validation;
- quota-aware fallback routing;
- live Tokscale parsing for both installed JSON shapes;
- account-identity stripping;
- strict artifact and verification receipts;
- lowest-incomplete-wave sequential launch on Yogabook;
- safe Codex `workspace-write` sandbox;
- 50 GiB minimum disk gate;
- role and quota-pool contracts;
- complete estate objective registry;
- 23 focused planner/runner tests passing before the full-suite gate.

This file is evidence of the retrospective, not evidence that the retrofit is complete. Completion requires the test, dry-run, diff, and independent review receipts listed in the campaign manifest.
