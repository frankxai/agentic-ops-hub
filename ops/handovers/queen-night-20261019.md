---
id: queen-night-20261019
what: Queen night held the performance card on a foreign checkout
where: starlight/queen inbox; gate commit 24d7fc0 on agent/grok/queen-night-gates-20261019; jev-fail-closed stays at de6f43c
owner: Grok
status: open
note: overnight preflight HOLD, no worker spawned
updated: 2026-10-19
---

## Desk

Author: Grok. Date: 19 October 2026. Revision: 3. Source: heartbeat `20261019-020222`, operator-idle, and two `node tools/queen-reach.mjs` reads after the chair fix.

Last completed tick `20261019-020222` recorded status `idle-held`, dispatched 0, queue depth 8, held count 16, resourceGuard false, free RAM 1979 MB. The operator was away. That empty-candidate path returns before the presence, RAM, and Peak Performance gates.

The reach pair after the chair fix both exited 0 and agreed: status `idle-held`, queue depth 12 on the heartbeat, dispatched 0, resourceGuard false, tick outcome `idle-held`, free RAM 5299 MB, floor 4096 MB, occupied checkouts 1. Neither read started a loop, spawned a worker, or stopped a process.

## Cards

The chair now builds branch, operator presence, and the Peak Performance hold before `steerCard`. One chair run wrote `chair-pulse.json` with `20261019-night-performance` at spawn false, branch `agent/hermes/pp-admission-control-20260811`, foreignBranch true, ppHold true, reason `foreign-branch`.

The performance card records the fresh preflight: HOLD, exit 2, 4328 MB free, 10240 MB required, posture constrain, swarm posture pause-new-swarms, CPU 32 percent, 10 Codex task runtimes over a budget of 6. Do not spawn.

`2026-10-06-compute-guide-publish-gates`, `2026-10-06-health-audit-intake`, and `2026-10-06-sli-94-rebase` moved to `queen/inbox/_hold-night-20261019` with a reason file each. They are absent from the pulse. The other 6 October inbox cards stayed, with `concern` and `estateClass` added and their task `class` kept. Voice run `20261017-201656` stays in `queen/failed`.

The overnight guard was written by `writeOvernightGuardPlan` from a dry plan whose level was already `hold`. `latest.json` is timestamp `2026-10-19T00:59:18.420Z`, level `hold`, `allowNewSwarms` false, swarm posture `pause-new-swarms`.

## Checks

`node --test` of the shipped chair context, the night envelopes, and `queen-steer.test.mjs` passed: 30 tests, 0 failures. A second run of the chair-context and envelope files passed: 4 tests, 0 failures. Learning row `queen-night-20261019` is still one row, outcome `idle-held`, refuse false, floor 4096 MB, and was not appended again. The chair run appended per-card steer rows. Two of those rows refuse the performance card for `foreign-branch`, so the next identical refusal can block it. The floor stayed 4096 MB.

Gate commit `24d7fc0` is pushed on `agent/grok/queen-night-gates-20261019`. A pull request into main would carry the older history, so none was opened. `agent/grok/jev-fail-closed` stays at `de6f43c`. No product repo received a commit, so no product GitHub issue was opened.

## Prompt

When a fresh `pp preflight --workload overnight` returns allow, and `starlight/repos/peak-performance` is a clean checkout on `agent/codex/<scope>`, carry out only `queen/inbox/20261019-night-performance.json`. Stop if that checkout is dirty, foreign, or the guard level is a fresh hold. Leave the 4096 MB floor as it is. Leave personal sessions running. Leave voice run `20261017-201656` in `queen/failed`. Leave hold folders in place. Leave `agent/grok/jev-fail-closed` uncommitted. The gate code is commit `24d7fc0` on `agent/grok/queen-night-gates-20261019`. A different harness reviews before any merge.
