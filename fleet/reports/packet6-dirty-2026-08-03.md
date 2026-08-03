# Packet 6 Dirty Steward — 2026-08-03

**Machine:** C940 · enhance-never-erase · no wipe/reset/deploy

## frankx.ai-vercel-website
- Path: `C:\Users\frank\frankx.ai-vercel-website`
- Status: `## agent/claude/content-integrity-gate...origin/agent/claude/content-integrity-gate [gone]`
- Dirty entries: **434**

| Top path | Count | Class | Suggested commit name |
|---|---:|---|---|
| `public` | 418 | commit-candidate (scoped feature commits) | `feat(frankx.ai-vercel-website): checkpoint public WIP` |
| `"public` | 6 | worktree-split recommended before commit | `chore(frankx.ai-vercel-website): checkpoint "public` |
| `data` | 5 | worktree-split recommended before commit | `chore(frankx.ai-vercel-website): checkpoint data` |
| `.frankx` | 1 | commit-candidate or worktree-split (agent harness/meta) | `chore(frankx.ai-vercel-website): sync .frankx agent harness state` |
| `BRAND_IDENTITY.md` | 1 | worktree-split recommended before commit | `chore(frankx.ai-vercel-website): checkpoint BRAND_IDENTITY.md` |
| `lib` | 1 | worktree-split recommended before commit | `chore(frankx.ai-vercel-website): checkpoint lib` |
| `taste.md` | 1 | worktree-split recommended before commit | `chore(frankx.ai-vercel-website): checkpoint taste.md` |
| `content` | 1 | commit-candidate (scoped feature commits) | `feat(frankx.ai-vercel-website): checkpoint content WIP` |

### Sample lines
```
 M public/reading/.agent/workflows/create-blog-post.html
 M public/reading/.agent/workflows/deploy-production.html
 M public/reading/.agent/workflows/new-book-chapter.html
 M "public/reading/001-FrankX-AI-Investment Team/README.html"
 M "public/reading/001-FrankX-AI-Investment Team/agent.html"
 M "public/reading/001-FrankX-AI-Investment Team/claude.html"
 M data/inventories/profiles.json
 M data/route-index.json
 M data/vault-manifest.json
 M .frankx/identity.md
 M BRAND_IDENTITY.md
 M lib/social-links.ts
 M taste.md
?? content/kit-amplifier-update.md
```

## FrankX
- Path: `C:\Users\frank\FrankX`
- Status: `## main...origin/main [ahead 49, behind 137]`
- Dirty entries: **128**

| Top path | Count | Class | Suggested commit name |
|---|---:|---|---|
| `docs` | 32 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint docs WIP` |
| `scripts` | 20 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint scripts WIP` |
| `.claude` | 16 | commit-candidate or worktree-split (agent harness/meta) | `chore(FrankX): sync .claude agent harness state` |
| `public` | 13 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint public WIP` |
| `app` | 9 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint app WIP` |
| `components` | 7 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint components WIP` |
| `data` | 6 | worktree-split recommended before commit | `chore(FrankX): checkpoint data` |
| `content` | 5 | commit-candidate (scoped feature commits) | `feat(FrankX): checkpoint content WIP` |
| `tests` | 4 | worktree-split recommended before commit | `chore(FrankX): checkpoint tests` |
| `lib` | 3 | worktree-split recommended before commit | `chore(FrankX): checkpoint lib` |
| `.frankx` | 2 | commit-candidate or worktree-split (agent harness/meta) | `chore(FrankX): sync .frankx agent harness state` |
| `.intake` | 1 | commit-candidate or worktree-split (agent harness/meta) | `chore(FrankX): sync .intake agent harness state` |
| `AGENTS.md` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint AGENTS.md` |
| `BRAND_IDENTITY.md` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint BRAND_IDENTITY.md` |
| `OPS-INDEX.md` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint OPS-INDEX.md` |
| `README.md` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint README.md` |
| `package.json` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint package.json` |
| `pnpm-lock.yaml` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint pnpm-lock.yaml` |
| `taste.md` | 1 | worktree-split recommended before commit | `chore(FrankX): checkpoint taste.md` |
| `.agent` | 1 | commit-candidate or worktree-split (agent harness/meta) | `chore(FrankX): sync .agent agent harness state` |

### Sample lines
```
 M docs/ops/AGENT-HARNESS-STATUS.md
 M docs/ops/GITHUB-HARNESS-INVENTORY.md
 M docs/ops/HARNESS-ROLLOUT-BOARD.md
 M scripts/agents/audit-agent-quality.mjs
 M scripts/agents/github-harness-inventory.mjs
 M scripts/agents/repo-registry.mjs
 M .claude/agents/autoresearcher.md
 M .claude/agents/content-hook-engineer.md
 M .claude/agents/content-hook-learner.md
 M public/images/priority-2026-04-25/BATCH_REPORT.md
?? public/images/frankx-architecture.png
?? public/images/qr/
 M app/newsletter/archive/page.tsx
?? app/ai-architecture/[partner]/
?? app/api/workshops/
 M components/newsletter/WeeklyIssueCallout.tsx
?? components/ai-architecture/LatestReleases.tsx
?? components/ai-architecture/ReferenceArchitectures.tsx
 M data/inventories/profiles.json
 M data/sprint-current.json
 M data/vault-manifest.json
?? content/ai-architecture/
?? content/artifacts/
?? content/strategy/artifact-system-2026.md
```

## Ship posture
- `frankx.ai-vercel-website` on orphaned `content-integrity-gate` with heavy dirty = **NO-SHIP** from this checkout.
- Production changes must use **clean worktree from `origin/main`** + PR gates.
- FrankX `main` ahead/behind diverge = authoring only; do not treat as deploy source.
