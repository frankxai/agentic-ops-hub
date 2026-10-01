# 2026-09-29/30 — Skill foundry, GenCreator video pack, marketplace repair (Claude, session 1277335d)

## Shipped (merged via cross-harness gate: Claude built, Codex and Grok reviewed, Grok signed via tools/pr-gate.mjs)

| Repo | PR | Merge | What |
|---|---|---|---|
| claude-code-config | #15 | 498a37b | Skill foundry (`scripts/skill-foundry/foundry.mjs`: scan, usage, index, tier, market, brands, graph, report), 7 forged agents (skill-foundry-lead, skill-smith, skill-judge, skill-scout, marketplace-manager, gencreator-product-lead, creator-dogfood-tester), `.loop/skill-foundry-weekly`, discovery hook, foundry MCP server, frontier + competitive references, control-plane patch in docs/handoffs |
| claude-code-config | #21 | 7d00851 | `docs/handoffs/land-rova.ps1` — dry-run-first landing of the codex/rova estate tree |
| gencreator-skills (renamed from agentic-creator-skills) | #3, #4 | 96ed690, rename | `video-social-studio` plugin (local ffmpeg video editor + social manager + MCP server); marketplace renamed |
| claude-skills-library | #38 | bd2407e | Strict-valid multi-brand catalog + agent-readable `catalog/skills.json` |
| starlight-agent-config | #52, #54 | admin-merged by Frank | 16 core skills restored (pp, windows-phone-link-search-safety, …), bless gate hardening; team profiles + 13-brand routing |
| mind-palace-agent-skills #6, arcanea-marketplace #2, claude-code-oracle-skills #2, agentic-creator-os #80, arcanea-spellbound #2 | | | Marketplace strict-validation fixes; stray `$null` removal |

## Measured

- Live skills: ~28.5k Turn-0 listing tokens vs 8k gateway cap; 44 of 402 skills invoked in 30 days; 331 loaded skills unowned in graph/skills.graph.json.
- Evals: first real `claude plugin eval` runs in the estate (ui-ux-design-expert 6/6 recall, 0/5 false fires; video-social-studio 35/36).
- Grok caught 5 real defects in video-social-studio that Claude and Codex missed.

## Open (owner → action)

- claude-code-config #22 (reconcile live config onto main, ~4,500-file snapshot, `.gitleaksignore` 6 entries) → Frank reviews allowlist; Grok review requested. After merge run the guarded switch in the PR body so `~/.claude` loads from main.
- Estate root codex/rova (3,820 dirty: 1,360 runtime, 1,724 generated, 46 media, 5 junk, ~768 real) → Frank runs `pwsh -File repos/claude-code-config/docs/handoffs/land-rova.ps1` (dry run), then `-Apply`. Never push until CONVERGENCE §7 desk 6 is ruled.
- Control-plane patch (AGENTS/SYSTEM/WORKFLOW/SOUL, agent registry, resolver 124→467 skills) → apply after codex/rova lands: `git apply --3way --ignore-whitespace repos/claude-code-config/docs/handoffs/skill-foundry-control-plane.patch`.
- `foundry.mjs tier --apply` (~17.6k tokens/session saved) → after the live checkout is on main.
- Distribution: list gencreator-skills and claude-skills-library via clau.de/plugin-directory-submission; skills.sh indexes on `npx skills add` installs.
- starlight-agent-config branch protection requires 1 review; with one GitHub account every merge needs `--admin`. Decide: drop the rule (pr-gate + Grok is the gate) or add a reviewer account.

## Local cleanup done

Removed 20 merged/empty worktrees and 2 merged clones (+11 GiB); local excludes for tool folders in 5 repos; stray `$null` removed in 6 repos; live skill links repaired by restoring tracked copies.

## Later on 2026-09-30

- Frank ran the admin merges (#52, #54), renamed agentic-creator-skills -> gencreator-skills, merged #4. Install: `/plugin marketplace add frankxai/gencreator-skills`.
- Live config: claude-code-config #22 (reconcile, Grok pass) merged; live checkout switched from codex/hook-context-review to main with the guarded procedure (old branch kept on origin).
- Tier live: #24 (118 cold skills -> /command only, git-based skill age), #25 (untier 2 junctioned skills), #27 (discovery hook matches hidden tier). Turn-0 listing 28,841 -> 18,653 tokens. `foundry-skill-suggest.js` registered in ~/.claude/settings.json (UserPromptSubmit); settings backup kept in the session tmp.
- Estate root: `docs/handoffs/land-rova.ps1` merged (#21, Grok pass after a personal-state fix). Frank runs it; agents are blocked from the root by verify-lane.
- 2026-10-01: codex/rova landed locally (3,826 dirty -> 11, 32 commits incl. 4fd0383 control-plane patch: resolver 476 names, 7 agents registered). Not pushed; push = Frank's ruling on CONVERGENCE section 7 desk 6. Held back: 7 tracked queen runtime files, velora-named files, graph/agents.atlas.json (>5 MB). Ignored: ops/automation-audit/*.json (captured tokens: rotate), raw supplier HTML scrapes.
- 2026-10-01: Frank pushed codex/rova to frankxai/starlight-command (private), 469e3d6..4fd0383. Estate root is clean except 11 deliberate holdbacks.
