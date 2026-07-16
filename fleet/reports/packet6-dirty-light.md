# Packet 6 light — Dirty classification (C940) — 2026-07-16

**Constraints honored:** no reset, no wipe, no force-push, no ship.

## Top dirty trees

| Repo | Branch | Approx dirty | Classification | Recommended next |
| --- | --- | ---: | --- | --- |
| `frankx.ai-vercel-website` | `agent/claude/content-integrity-gate` | ~427 | **WIP / do-not-ship** — integrity-gate branch, mass M (route-index, vault, public/reading likely) | Packet 6 full: split commit vs worktree vs discard-safe; **no prod merge** until green gate |
| `FrankX` | `main` (check) | ~111 | **Authoring WIP** — content/meta-os; not prod deploy source | Commit named scopes on `agent/c940/content-*` worktrees; sync only intentional files to prod repo |
| `Arcanea` | `integrate/agent-native-main-2026-06-12` | ~100 | **Feature integrate WIP** | Stay on integrate branch; commit lore/docs vs code separately; Book takes UI only after C940 backend claim |
| `agentic-ops` | `main` (ahead 3 behind 4) | staged fleet + untracked docs | **Control plane** — fleet multi-agent align staging | Commit fleet align now; rebase origin before push; leave unrelated untracked docs unstaged |
| `SIS` | `main` | ~22 | Light WIP | Fetch-only if dirty; optional small commits |
| `Business` | `main` | ~23 | Sensitive, **NO_ORIGIN** | Backup-only; never Book |

## Recommended commit names (only — not executed on dirty prod)

1. `chore(prod): regenerate route-index + vault-manifest` (if intentional)  
2. `feat(gate): content-integrity-gate remaining surfaces`  
3. `docs(ops): fleet multi-agent driver + bus queues` (agentic-ops — this session)  
4. `content(frankx): <single-topic> batch` (never mega-commit 111 files)

## Ship gate

- frankx.ai / gencreator.ai both **HTTP 200** (live probe this session).  
- **Do not ship** content-integrity-gate dirty tree as production.  
- R1: Footer external CTA exists; primary nav still heavily `/gencreator` internal — **YELLOW**, not RED.

Report path: `fleet/reports/packet6-dirty-light.md`
