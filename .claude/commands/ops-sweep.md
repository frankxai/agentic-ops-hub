---
description: Sweep all repos/sessions via git deltas and refresh the Agentic Ops Ledger (low-token). Use at session end, or when asked to update the ledger, document progress, or recommend next prompts.
---

# /ops-sweep — refresh the Agentic Ops Ledger

You are running the end-of-session sweep. Be **token-disciplined**: git is the signal, scrollback is not.

## Protocol

1. **Read current state** — `ops/OPS-LEDGER.md` and the latest `ops/sessions/*.md`. Note the date of the last sweep.

2. **Pull git deltas (cheap, primary signal).** For each active repo under `~/starlight/repos/`, run one batched command:
   ```
   for r in <active repos>; do
     git -C "$r" log --since="<last sweep date>" --pretty="%ad %s" --date=short
     git -C "$r" branch --show-current; git -C "$r" status --short
   done
   ```
   This yields what was done (commit subjects = the "why"), the active branch, and uncommitted work — without reading any terminal.

3. **GitHub issue on the product repo.** Comment on the issue that already tracks the slice. Open one only when the slice is still open and has none. A merged slice with no issue stays in the session file. Pull Linear only if Frank asks. Do not mass-read.

4. **Only read a terminal** if git can't explain a front (interactive/REPL state) AND the user asks. Request access, take ONE screenshot, map window→repo. Never poll.

5. **Update files:**
   - Append `ops/sessions/<today>.md` — what happened, signals, decisions, carried-open.
   - Refresh `ops/OPS-LEDGER.md` — active fronts table, Recently Done, Open/Risks. Keep it tight; archive stale done-items.
   - Refresh `ops/NEXT-PROMPTS.md` — ranked next prompt per repo/front. Update the terminal map if changed.

6. **Obsidian reads `ops/` in this repo.** Do not copy the ledger into FrankX while that checkout is dirty or on another harness's branch.

7. **Linear stays archive** unless Frank asks. The action record is the GitHub issue from step 3.

8. **Commit on a free branch.** `agent/<harness>/<scope>` from `origin/main`, explicit paths, push that branch, open or update a PR. Do not commit onto another harness's checkout. Do not push `main` from the sweep.

## Output to the user
A 4-line summary: what landed, what's newly open, the single highest-leverage next prompt, and the ledger path plus the GitHub issue. Nothing more.
