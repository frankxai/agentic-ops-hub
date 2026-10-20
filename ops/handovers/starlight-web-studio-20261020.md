---
id: starlight-web-studio-20261020
what: Take the Starlight Web Studio plugin from pushed branch to its first real studio runs
where: frankxai/claude-skills-library, branch agent/claude/web-studio, plugins/starlight-web-studio/
owner: claude
status: open
note: branch pushed, PR held by the repo's PR budget (14 open vs 10)
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

## Founder decisions

1. Open the PR over budget, or land or close others first.
2. `claude plugin validate .` rejects the existing marketplace plugin name `claude-skills-library`
   as reserved by Anthropic. Renaming breaks current installs.
3. go.agenticincome.ai noindex: deliberate or a leak.
4. Whether to run `Register-StudioSweep.ps1 -Register` for the daily sweep.
5. Go or no-go on the frankx.ai R4 homepage cut (removes over half the page).

## Prompt

Continue the Starlight Web Studio from branch `agent/claude/web-studio` in
`frankxai/claude-skills-library` (worktree `.worktrees/web-studio`). Read this handover and
`plugins/starlight-web-studio/README.md`. If Frank has ruled on the PR budget, open the draft PR and
have a non-Claude harness review it through `tools/pr-gate.mjs`. Then run the studio's first real
jobs from `starlight/logs/excellence/eye-pass-2026-10-20.md`: the agenticincome.ai R3 copy fix (status strings
under prices), a live-scroll check of the realityarchitect.ai pinned scene, and R2 hygiene draft PRs for the
JSON-LD gaps on the board. Run `studio-doctor.mjs` in each repo first. Never merge, publish a route or touch go.agenticincome.ai noindex without
Frank's word.
