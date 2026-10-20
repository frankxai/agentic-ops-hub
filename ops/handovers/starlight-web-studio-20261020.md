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
- Not run: `claude plugin eval` (needs a signed-in headless Claude), the visual eye pass, any site edit.

## Founder decisions

1. Open the PR over budget, or land or close others first.
2. `claude plugin validate .` rejects the existing marketplace plugin name `claude-skills-library`
   as reserved by Anthropic. Renaming breaks current installs.
3. go.agenticincome.ai noindex: deliberate or a leak.
4. Whether to schedule a daily `/studio-sweep`.

## Prompt

Continue the Starlight Web Studio from branch `agent/claude/web-studio` in
`frankxai/claude-skills-library` (worktree `.worktrees/web-studio`). Read this handover and
`plugins/starlight-web-studio/README.md`. If Frank has ruled on the PR budget, open the draft PR and
have a non-Claude harness review it through `tools/pr-gate.mjs`. Then run the studio's first real
job: `node plugins/starlight-web-studio/bin/studio-doctor.mjs` in each tier-1 repo, then the scout
eye pass (screenshots at 375, 768, 1440; 50-point rubric) on frankx.ai, arcanea.ai and gencreator.ai,
appending to `starlight/logs/excellence/scoreboard.jsonl`. After that, R2 hygiene draft PRs for the
JSON-LD gaps on the board. Never merge, publish a route or touch go.agenticincome.ai noindex without
Frank's word.
