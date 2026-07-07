# Arcanea AI App Grouped Status - 2026-06-26

Status: read-only grouped status for the red repo lane identified in the repo
risk sweep. No edits, cleanup, staging, commits, pushes, installs, builds,
tests, or deploys were performed in `arcanea-ai-app`.

## Repo Contract Read

Repo: `C:\Users\frank\starlight\repos\arcanea-ai-app`

Read: `AGENTS.md`

Important local rules:

- Node 20.x and pnpm only; never npm.
- No PR merges unless changed scope passes build, typecheck, and lint.
- Use design tokens and `DESIGN.md` / `TASTE.md` for visual surfaces.
- If git state is dirty, stage only target files and report unrelated changes.
- Planning files in `planning-with-files/` are the execution control plane.

## Current Git State

| Field | Value |
| --- | --- |
| Branch | `codex/arcanea-homepage-world-engine` |
| Head | `eaf954c3` 34 hours ago, `Polish Arcanea homepage and production build` |
| Dirty tracked files | 26 |
| Untracked files / paths | 30 from earlier sampled sweep; full untracked path view groups to 66 entries because directories expand |
| Risk | Red |

## Grouped Change Areas

| Group | Count signal | Meaning |
| --- | ---: | --- |
| `.claude` | 14 | Hook/runtime governance changes; high coordination risk because it affects agent behavior |
| `.visual-qa` | 16 | Generated or captured QA artifacts; should be reviewed as evidence, not blindly committed |
| `docs` | 14 | Strategy, research, growth, operating system, visual direction docs |
| `.arcanea` | 9 | Lore/canon/project logs; public/private/canon correctness matters |
| `apps` | 9 | Frontend/product surface changes including homepage/v3/genesis/e2e |
| `.grok` | 4 | Tool/harness state; decide if repo-owned or local-only |
| `planning-with-files` | 3 | Execution control plane files; likely important if current direction changed |
| `packages` | 2 | World-engine code/types changed |
| root files | 3+ | `AGENTS.md`, `DESIGN.md`, `TASTE.md`, `.agent-harness.json` |

Tracked diff stat:

```text
26 files changed, 448 insertions(+), 49 deletions(-)
```

## Interpretation

This does not look like one small homepage polish. It appears to contain at
least five overlapping workstreams:

1. Agent/hook governance adoption.
2. Arcanea homepage and v3/frontend product work.
3. Genesis / E2E / visual QA artifact creation.
4. Lore/canon/world-building expansion.
5. World-engine package model changes.

Treat it as a red lane because the blast radius spans app UI, runtime hooks,
canon docs, planning files, and package code.

## Recommended Owner Decision

Choose one:

- `SPLIT`: separate into governance, frontend, canon/docs, QA artifacts, and
  world-engine changes.
- `SHIP AS CAMPAIGN`: if this was one deliberate Arcanea relaunch push, run the
  full verification suite and package the evidence together.
- `HOLD`: pause until the originating agent/human explains intent.

Recommended default: `SPLIT`, unless there is a known Arcanea relaunch thread
that intentionally bundled these surfaces.

## Next Safe Commands

Read-only or local verification only:

```powershell
git -C C:\Users\frank\starlight\repos\arcanea-ai-app status --short --untracked-files=all
git -C C:\Users\frank\starlight\repos\arcanea-ai-app diff --stat
git -C C:\Users\frank\starlight\repos\arcanea-ai-app diff -- apps/web/app/page.tsx apps/web/app/v3
```

Before any install/build/test in this unfamiliar dirty state, run the repo
security intake from the estate instructions or explicitly decide why it is not
needed.

## Do Not Do

- Do not reset, checkout, delete, or clean files.
- Do not stage broad pathspecs.
- Do not deploy or merge.
- Do not treat `.grok`, `.visual-qa`, or hook files as automatically
  repo-owned.
- Do not publish lore/canon/social material without canon proof and approval.

## Slack Route

Post summary to `#repo-command` and route the brand decision to
`#brand-arcanea`.
