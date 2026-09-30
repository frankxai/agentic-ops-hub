# ops/ — Agentic Ops Ledger System

Rolling, low-token documentation of all work across every repo and terminal session.

## Files
- **`OPS-LEDGER.md`** — single source of truth. Bigger picture, active fronts, done, open/risks. The product repo's GitHub issue is the action record.
- **`NEXT-PROMPTS.md`** — copy-paste next prompt per repo/terminal, ranked by leverage. Includes the terminal→repo map.
- **`sessions/YYYY-MM-DD.md`** — append-only session log. One entry per sweep.
- **`/ops-sweep`** (`.claude/commands/ops-sweep.md`) — the repeatable protocol that refreshes everything.

## Surfaces
| Surface | Role | Cost |
| :--- | :--- | :--- |
| Git markdown (here) | Source of truth | Free (local read/write) |
| Obsidian (FrankX vault) | Reads `ops/` here. Copy only when that checkout is clean and on the assigned branch. | ≈0 |
| Linear (Arcanea team) | Archive. The action record is the product repo's GitHub issue. | Only if Frank asks |

## Why it's cheap — the token economy
The expensive way is OCR-ing terminal scrollback every session. The cheap way, used here:
1. **Git is the primary signal.** `git log --since=<last sweep>` across repos says what was done, why (commit messages), and where — for near-zero tokens.
2. **Delta, not full re-read.** A sweep reads the existing ledger + new commits, then appends. It never re-derives history.
3. **No idle polling.** Sweeps fire on an explicit trigger (session end), never on a timer that burns tokens while you're away.
4. **Scrollback only on request.** Reading a terminal window is opt-in, for cases git can't explain (interactive debugging, REPL state).
5. **Linear stays archive.** The narrative stays in markdown. Sync Linear only if Frank asks.

## Running a sweep
```
/ops-sweep
```
Or ask: "sweep my sessions and update the ledger." At session end, it:
1. Reads `OPS-LEDGER.md` (current state).
2. Pulls git deltas since the last session file.
3. Appends `sessions/<today>.md`, refreshes `OPS-LEDGER.md` + `NEXT-PROMPTS.md`.
4. Obsidian reads `ops/` here. Copy into FrankX only when that checkout is clean and on the assigned branch.
5. Commits on `agent/<harness>/<scope>` from `origin/main` and opens or updates a PR. The product repo's GitHub issue is the action record. Linear only if Frank asks.

## Who suggests it

Any harness that finishes a slice suggests this sweep in its closing reply, then writes it when the checkout is free. The suggestion names two saves: this ledger, and the product repo's existing GitHub issue. Open a GitHub issue only when the slice is still open and has none. A merged slice with no issue stays in the session file. Linear stays archive unless Frank asks. The primary checkout of this repo is often another harness's branch; use a worktree from `origin/main` rather than committing onto that branch.
