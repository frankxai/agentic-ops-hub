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

3. **Pull Linear deltas (gated).** Only if open items may have changed: `list_issues assignee=me state=started,unstarted` on the Arcanea team. Do not mass-read.

4. **Only read a terminal** if git can't explain a front (interactive/REPL state) AND the user asks. Request access, take ONE screenshot, map window→repo. Never poll.

5. **Update files:**
   - Append `ops/sessions/<today>.md` — what happened, signals, decisions, carried-open.
   - Refresh `ops/OPS-LEDGER.md` — active fronts table, Recently Done, Open/Risks. Keep it tight; archive stale done-items.
   - Refresh `ops/NEXT-PROMPTS.md` — ranked next prompt per repo/front. Update the terminal map if changed.

6. **Mirror to Obsidian** — copy `OPS-LEDGER.md` + `NEXT-PROMPTS.md` into the FrankX vault `Ops/` folder (file write, ~0 tokens).

7. **Sync to Linear (only if asked)** — create/update issues for new Risk items on the Arcanea team, linking back to the ledger.

8. **Commit + push** — on this Windows machine git must run host-side (the sandbox mount blocks file deletes and has no GitHub creds). Write a `.bat` that clears `.git/index.lock`, adds/commits/pushes with output to a log, run it via File Explorer address bar, then read the log to confirm.

## Output to the user
A 4-line summary: what landed, what's newly open, the single highest-leverage next prompt, and the ledger/Obsidian links. Nothing more.
