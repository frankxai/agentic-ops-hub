---
id: starlight-web-studio-20261020
what: Take the Starlight Web Studio plugin from pushed branch to its first real studio runs
where: frankxai/claude-skills-library, branch agent/claude/web-studio, plugins/starlight-web-studio/
owner: claude
status: open
note: draft PRs claude-skills-library#77 (plugin) and agenticincome#80 (first fix); both need a non-Claude reviewer
updated: 2026-10-20
---

## State

- Built by Claude (Opus 5.5), reviewed read-only by Codex. Branch `agent/claude/web-studio`
  (5 commits on `origin/main` 93c4aad). No PR: the repo is over its open-PR budget, so it waits
  for Frank to land or close PRs, or to say open it anyway.
- The plugin: 11 agents, 8 skills (`studio-protocol`, `studio-audit`, `answer-engine`, `copy-desk`,
  `cinematic-motion`, `media-desk`, `signature`, `proactive-sweep`), `/studio`, `/studio-sweep`,
  the workflow `/starlight-web-studio:studio-audit`, `bin/studio-scan.mjs`, `bin/studio-sweep.mjs`,
  `bin/studio-doctor.mjs`, 3 plugin eval cases, and a marketplace entry.
- Evidence: `claude plugin validate plugins/starlight-web-studio` passes; 30 node tests pass
  (scanner, RFC 9309 robots, sweep ranking, the real workflow against stub agents). `pack-tests.yml`
  now also runs `plugins/*/tests`. The 35 failing tests in `packs/*` fail the same on this machine
  without this branch (secret-scan and workflow-lint suites).
- Codex findings: 10 P1, 4 P2, no P0. Engineering ones fixed with a regression test each. Open:
  a client-project record (approvals, revisions, asset rights) and one complete worked case.
- First sweep of the 24 live properties: 24 scanned, 0 failed. go.agenticincome.ai serves
  noindex in meta and X-Robots-Tag (confirm intent). frankx.ai ships 53 elements at inline
  opacity:0. arcanea.ai is 30/30 for crawlers. Eye scores date from 2026-08-03 and are stale.
- Proposal page: https://claude.ai/artifact/QoHMrm19fxTPgAMytLLLf1 (private).
- Eye pass done on all 9 tier-1 and tier-2 sites (real 360 px screenshots, desktop for frankx.ai; remote capture because
  `pp preflight` held local browsers). Scores /50: animelegends 36, gencreator 35, aiarchitectacademy 33,
  gencreator.community 31, arcanea 30, starlightintelligence.org 28, realityarchitect 26, agenticincome 25, frankx 24.
  Report `starlight/logs/excellence/eye-pass-2026-10-20.md`; scoreboard appended; issue #76 commented.
- Daily sweep staged, not registered: `schedule/Register-StudioSweep.ps1` (dry run by default, `-Register` turns it on).
- Not run: `claude plugin eval` (needs a signed-in headless Claude), motion and second-theme observation, any site edit.

## Round two (same day)

- Eye pass extended to all 25 live sites (tier-3 at 360 px, desktop 1440 for every site); tier-3 scores 29 to 37.
- realityarchitect.ai corrected 26 to 29: the blank capture was a CSS scroll-driven scene; studio-audit now
  requires a source check before scoring a blank capture.
- go.agenticincome.ai `noindex` is intended (redirect utility).
- Draft PR claude-skills-library#77 opened with the over-budget reason in its body.
- First studio-built fix: agenticincome#80 (buyer labels; sale gate untouched; verified on the Vercel preview).

## Round three (same day)

- Daily sweep registered as Windows task `StarlightStudioSweep` (07:10, model-free, read-only fetches, local logs only),
  per Frank's goal to make the team proactive. First runs exit 0, heartbeat `logs/heartbeats/heartbeat-studio-sweep.json`
  ok, `--accept go-agenticincome:noindex`. Remove with `Register-StudioSweep.ps1 -Unregister`. It runs the copy in the
  web-studio worktree; re-register after #77 merges.
- Codex review: #77 PASS after six rounds (52 tests), #80 PASS after three rounds (7 tests). Relayed as PR comments,
  not as pr-gate sign-offs; a non-Claude harness must sign off itself before merge.
- agenticincome GitHub Actions fail in 2 to 3 s with no steps (account Actions budget); Vercel preview builds pass.

## Round four (same day): worked case

- `plugins/starlight-web-studio/examples/frankx-homepage/` on #77 (c2992f4, 9ed3d73, e770e16): one full R4 run on
  the frankx.ai homepage: signature, brief, three directions, decision (B, no WebGL), motion score, and a GSAP + CSS
  liquid-glass prototype. Hero media came from Codex image generation with provenance sidecars; the first render
  failed its packet and was regenerated.
- Codex critique, two rounds, both "revise"; every finding fixed and recorded in `critique.md`. Round 3 not run.
  Safari and a real phone remain unverified (`handoff.md`).
- Prototype: https://claude.ai/artifact/QS11b2xvgueZ7FziESXczw (v6). Claude Design canvas with A, B, C and the B phone
  board: https://claude.ai/artifact/7yMQrAGTkVfBDpUM8SFicc (v8). Both private to Frank.
- The panel's fourth row ("waiting for a person to approve") goes false when #77 merges or closes; update it then.

## Round five (same day): capability gaps

- three.js liquid-glass lab `examples/gpu-glass/` (28a1840, e1db0cf): it is the gpu-artist reference wrapper, with a tested gate,
  a frame-budget probe and a single teardown. It runs at 0.05 to 0.40 ms per frame on one device, for 167 KB extra. The homepage keeps CSS glass.
- Higgsfield `/hf-plan` for a 5 s seamless hero loop, costed at 24.5 credits (cap 25). Nothing was uploaded or generated.
- Claude Motion is unavailable on this account (no Motion artifact type). Tests: 59/59.

## Round six (2026-10-21): PR 77 review to merge-ready

- Another Claude session (Fable) added `bin/materials-gate.mjs` overnight (91 tests, frozen at e7d9889, lanes in
  `docs/next-prompts-Claude-Fable-2026-10-21.md`). This round reviewed the whole PR at db7217b.
- Checkers: Codex CLI read-only (relayed verbatim on the PR) and the Codex GitHub app (its own reviews; triggered by
  commenting `@codex review` on a draft). Antigravity: quota, resets ~2026-10-24.
- Fixed with regressions, commits 8863d3f, c006b52, eedd331, f5685af, d3ea928 and 9202137:
  - scanner SSRF: per-hop checks, pinned connection, IPv6 allowlist, absolute deadline, stream pipeline;
  - gate counts renderer instances, and a non-Next app with no route graph fails coverage;
  - catalog regenerated, Medium link-check 403 ignored;
  - ten P2s.
- Verdicts: Codex CLI PASS at d3ea928; the app reported no major issues at f5685af. CI: 5/5 green on 9202137, 501 tests.
  17 app threads answered and resolved.
- Lane 1 (gencreator.ai materials pass) not started: C: at 48.7 GiB is CRITICAL (no new worktrees), the gencreator
  checkout is on an Antigravity branch with 6 dirty files, and cloud sessions need the app on screen and the repo named.

## Founder decisions

1. Mark #77 ready and merge it (a first public marketplace listing); a non-Claude harness records the pr-gate sign-off.
2. `claude plugin validate .` rejects the existing marketplace plugin name `claude-skills-library`
   as reserved by Anthropic. Renaming breaks current installs.
4. Keep or remove the registered daily sweep.
5. Go or no-go on the frankx.ai R4 homepage cut (removes over half the page).
6. Approve or skip the Higgsfield hero loop (upload one file, ≤ 25 credits).

## Prompt

Continue the Starlight Web Studio from branch `agent/claude/web-studio` in
`frankxai/claude-skills-library` (worktree `.worktrees/web-studio`). Read this handover and
`plugins/starlight-web-studio/README.md`. If Frank has ruled on the PR budget, open the draft PR and
have a non-Claude harness review it through `tools/pr-gate.mjs`. Then run the studio's first real
jobs from `starlight/logs/excellence/eye-pass-2026-10-20.md`: the agenticincome.ai R3 copy fix (status strings
under prices), a live-scroll check of the realityarchitect.ai pinned scene, and R2 hygiene draft PRs for the
JSON-LD gaps on the board. Run `studio-doctor.mjs` in each repo first. Never merge, publish a route or touch go.agenticincome.ai noindex without
Frank's word.
