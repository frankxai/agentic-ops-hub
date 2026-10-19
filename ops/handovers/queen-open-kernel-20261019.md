---
id: queen-open-kernel-20261019
what: Take the Queen open kernel from draft starlight-swarm #39 to a checked, placed package and finish the slice (profile, queen-ops pack, consumer PRs)
where: starlight-swarm PR 39 (ccr-7df18fe9-l015ln); agentic-ops issue 289; starlight-agent-config, claude-skills-library and consumer repos on the same branch name
owner: Claude (maker); Codex or Antigravity (checker)
status: open
updated: 2026-10-19
---

## Prompt

Current pickup for the open-kernel slice only; the Queen runtime pickups below
(Ops234 lane, Codex) keep their own objectives and gates.

Read `ops/sessions/2026-10-19.md`. Draft
[starlight-swarm #39](https://github.com/frankxai/starlight-swarm/pull/39) at
`74bd51e` is green locally (510/510 + 29/29, build, dry-run, estate-guard high 0)
and needs an independent checker PASS at that exact head before it is marked ready;
do not self-certify. Watch its CI and review threads.

[Ops289](https://github.com/frankxai/agentic-ops/issues/289) holds the placement
decision (A dedicated repo / B starlight-swarm / C SIS; recommended B now, A later).
If Frank chooses A, move the package with `git subtree split` and update the
Registry records named in the issue; if B, add only the `artifact_queen_open_kernel`
authority id. Either way, decide the `starlight queen` built-in collision from SIS #462.

The rest of the slice is already up as drafts (profile: starlight-agent-config #132; pack:
claude-skills-library #74; consumers: agentic-creator-os #132, frankx.ai-vercel-website #1074,
arcanea #158; skills: starlight-agent-skills). Drive each to a checked head; nothing merges
without an independent seat. What each one is, for reference:
the `starlight-queen` profile and doctrine in starlight-agent-config (text only;
private Actions budget blocked, Frank merges); the `queen-ops` hooks pack in
claude-skills-library (TaskCompleted / TeammateIdle / TaskCreated / PreToolUse /
Stop, tests proving each hook cannot be satisfied by its own reminder text,
install.sh, marketplace and catalog registration); consumer PRs on
agentic-creator-os, frankx.ai-vercel-website and arcanea that delete the vendored
hive-mind queen files and install the pack, and `queen-operator` in
starlight-agent-skills. Hold the SIS truth PR until its open count is under 15 and
the FrankX retirement until its Actions budget returns. Add no queue, scheduler,
daemon or spend authority anywhere; runtime authority stays in agentic-ops.
