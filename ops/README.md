# ops/ — Agentic Ops Ledger System

Rolling, low-token documentation of all work across every repo and terminal session.

## Files
- **`OPS-LEDGER.md`** — single source of truth. Bigger picture (3 layers), active fronts, done, open/risks, Linear action map.
- **`NEXT-PROMPTS.md`** — copy-paste next prompt per repo/terminal, ranked by leverage. Includes the terminal→repo map.
- **`ecosystem-sprint-2026-06-18.json`** — machine-readable sprint, milestones, repo risks, and agent protocol for the 267-repo estate.
- **`../docs/ECOSYSTEM_COMMAND_CENTER_2026-06-18.md`** — human-readable portfolio command center and weekly review agenda.
- **`sessions/YYYY-MM-DD.md`** — append-only session log. One entry per sweep.
- **`/ops-sweep`** (`.claude/commands/ops-sweep.md`) — the repeatable protocol that refreshes everything.

## Surfaces
| Surface | Role | Cost |
| :--- | :--- | :--- |
| Git markdown (here) | Source of truth | Free (local read/write) |
| Obsidian (`Ops/` in FrankX vault) | Daily human glance + graph | ≈0 (file copy) |
| Linear (Arcanea team) | Action surface — open items only, on demand | MCP tokens (gated) |

## Why it's cheap — the token economy
The expensive way is OCR-ing terminal scrollback every session. The cheap way, used here:
1. **Git is the primary signal.** `git log --since=<last sweep>` across repos says what was done, why (commit messages), and where — for near-zero tokens.
2. **Delta, not full re-read.** A sweep reads the existing ledger + new commits, then appends. It never re-derives history.
3. **No idle polling.** Sweeps fire on an explicit trigger (session end), never on a timer that burns tokens while you're away.
4. **Scrollback only on request.** Reading a terminal window is opt-in, for cases git can't explain (interactive debugging, REPL state).
5. **Linear writes are gated.** Only changed open items sync; the narrative stays in markdown.

## Running a sweep
```
/ops-sweep
```
Or ask: "sweep my sessions and update the ledger." At session end, it:
1. Reads `OPS-LEDGER.md` (current state).
2. Pulls git deltas since the last session file.
3. Appends `sessions/<today>.md`, refreshes `OPS-LEDGER.md` + `NEXT-PROMPTS.md`.
4. Mirrors to Obsidian; syncs changed open items to Linear if asked.
5. Commits + pushes.
