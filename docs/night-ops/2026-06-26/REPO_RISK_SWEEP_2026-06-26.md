# Repo Risk Sweep - 2026-06-26

Status: read-only. No branch changes, cleanup, staging, commits, pushes, merges,
installs, builds, tests, or deploys were performed.

## Sweep Scope

Flagship and active portfolio repos under
`C:\Users\frank\starlight\repos`.

Risk scoring used in this sweep:

- `Green`: no dirty or untracked files.
- `Yellow`: some dirty or untracked files.
- `Red`: more than 20 dirty files or more than 30 untracked files.

This is a triage signal, not a quality judgment.

## Summary

- Red: 1 repo
- Yellow: 13 repos
- Green: 0 repos in this sampled set
- Highest immediate risk: `arcanea-ai-app`
- Most important operating note: do not run broad cleanup. Assign owners and
  close one lane at a time.

## Repo Table

| Repo | Branch | Head | Dirty | Untracked | Risk |
| --- | --- | --- | ---: | ---: | --- |
| `agentic-ops-hub` | `codex/ecosystem-command-center-main` | `9060ad6` 8 days ago, docs: add ecosystem command center | 13 | 22 | Yellow |
| `frankx.ai-vercel-website` | `codex/jojo-hospitality-intelligence` | `e55e56f5` 13 hours ago, feat(blog): sync batch 22 premium heroes and resolve metadata type-safety | 0 | 2 | Yellow |
| `gencreator.ai` | `codex/gencreator-intelligence-os` | `1d2fecc` 7 days ago, fix: calm homepage navigation and cursor | 9 | 0 | Yellow |
| `agentic-creator-os` | `agent/cleanup-sync` | `b512c81` 3 days ago, feat: implement and register Agent Service Bureau skill | 18 | 11 | Yellow |
| `arcanea-ai-app` | `codex/arcanea-homepage-world-engine` | `eaf954c3` 34 hours ago, Polish Arcanea homepage and production build | 26 | 30 | Red |
| `Starlight-Intelligence-System` | `main` | `88073a2` 34 hours ago, feat(site): Knowledge Tree explorer | 8 | 23 | Yellow |
| `starlight-agent-config` | `main` | `71c1ac8` 8 days ago, feat: create cross-agent config foundation | 8 | 24 | Yellow |
| `hermes-cockpit` | `main` | `db8d520` 8 days ago, chore: update gitignore for temp files | 1 | 2 | Yellow |
| `claude-skills-library` | `agent/cleanup-sync` | `111e584` 8 days ago, chore: update gitignore for temp files | 0 | 2 | Yellow |
| `awesome-hermes-agents` | `main` | `c2f00fa` 8 days ago, chore: update gitignore for temp files | 0 | 2 | Yellow |
| `ai-coe` | `main` | `0e40ad1` 8 days ago, chore(sync): sync local changes | 0 | 2 | Yellow |
| `agenticincome` | `agent/cleanup-sync` | `b07a68a` 8 days ago, chore(sync): sync local changes | 13 | 18 | Yellow |
| `AnimeLegends` | `main` | `053d297` 8 days ago, chore(sync): sync local changes | 0 | 2 | Yellow |
| `realityarchitect` | `main` | `6476312` 8 days ago, chore: update gitignore for temp files | 3 | 2 | Yellow |

## Triage

### P1: `arcanea-ai-app`

Why: 26 dirty files and 30 untracked files on a product/frontend branch.

Recommended next step:

1. Read repo-local `AGENTS.md`.
2. Run the repo security intake before installs/builds if needed.
3. Produce a file-level grouped status: hooks/config, app/page work, design docs,
   generated assets, and tests/build output.
4. Decide whether this is one coherent change set or must be split.

Do not:

- reset
- checkout
- delete generated files
- run production deploy
- merge to main

### P2: `agentic-ops-hub`

Why: current work is intentionally accumulating docs, reports, and visual
assets. This should be grouped into one coherent operations/social buildout
change set when ready.

Recommended next step:

- Keep adding proof artifacts here until the night-ops pass has a clear
  boundary, then review/stage as one packet.

### P2: `starlight-agent-config`

Why: central agent config repo has dirty and untracked files, including
sensitive-looking config areas seen in earlier scans.

Recommended next step:

- Run a deliberate secret-aware review. Do not print or inspect secret values in
  broad commands.

### P2: `agenticincome`

Why: revenue lane has meaningful dirty/untracked state and should be connected
to the revenue blocker monitor.

Recommended next step:

- Run a conversion-path read-only sweep: offer clarity, checkout path, trust
  proof, deployment owner, and next blocked revenue action.

## Slack Route

Post summary to `#repo-command`, with the full report path and no request for
cleanup until an owner is assigned.
