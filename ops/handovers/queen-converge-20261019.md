---
id: queen-converge-20261019
what: Land the Queen as she runs (starlight-estate PR 60), then open the seat-phase follow-up
where: starlight-estate PR 60 (agent/claude/queen-converge-20261019); branch agent/claude/queen-seat-phase-20261019
owner: Claude (maker); Codex or Grok (checker)
status: open
evidence: https://github.com/frankxai/starlight-estate/pull/60#issuecomment-6265474280
updated: 2026-10-19
---

## Prompt

Continue the Queen convergence from 19 October. Read starlight-estate PR 60 first, then this file.

State on 19 October, 12:30 local:

- `StarlightQueenLoop` runs every five minutes from `C:\Users\frank\starlight\tools`, a checkout on
  `agent/grok/jev-fail-closed`. That code matched no commit: modules were split across
  `agent/grok/queen-chair-away` (PR 55) and `agent/grok/queen-night-gates-20261019` (pushed to the
  wrong remote, no PR), and the loop script (+172/-14), `queen-reclaim-ram` and several test edits
  existed only on disk. PR 60 puts the running copy on `main` byte for byte, plus:
  - two stale test assertions corrected (they described a dirty checkout spawning local `codex exec`,
    which the routing table and commit 49c451c both rule out);
  - the RAM reclaimer no longer treats a live Cursor window's renderers as reclaimable, and its test
    no longer overwrites `queen/state/ram-reclaim-latest.json`;
  - the hub viewer hardening from the unpushed `agent/claude/hub-viewer-hardening` branch, and the
    desk now shows the real 4096 MB floor instead of "1 GB" and no longer force-closes Cursor.
- The effective RAM floor can only be raised above 4096 MB. A 1 GB floor is not reachable.
- Grok wrote most of the Queen modules, so Claude reviewed them; Codex and Antigravity reviewed the
  assembly. See PR 60 comments for both verdicts and what was fixed.

Next, in order:

1. PR 60 is ready and gate-clear at `6546de2` (Codex PASS after three rounds; Antigravity passed round
   two). A non-Claude harness or Frank merges it:
   `node tools/pr-gate.mjs merge --repo frankxai/starlight-estate --pr 60 --squash`. If a commit lands
   on it first, the sign-off stops counting and a new review is needed.
2. Bring the root checkout to the merged code only with its owner (Grok holds that branch), then
   restart the hub viewer from the merged file. It is still the as-found copy (pid 41328 at 01:46).
3. After PR 60 is on main, PR 55 shrinks to what PR 60 does not cover: the base commits it shares
   with PR 52 (`AGENTS.md`, intel brief, routing docs), the generated `queen/SIS-CHAIR-CONTRACT.md`
   and a `tools/harness-passport.mjs` change. Grok decides whether it stays open.
4. Open the seat-phase PR from `agent/claude/queen-seat-phase-20261019` (9651063, based on main).
   `node tools/queen-seats.mjs` names each live Claude seat's phase from its own status in
   `~/.claude/sessions`, the memory a finished seat still holds, and its resume command. It starts
   and stops nothing. Then wire its receipt into the chair pulse so the overnight Queen can report
   "closable N MB" instead of only refusing at the floor.
5. Ask Frank for a ruling before any version closes a seat itself. Today she never does.
6. Deferred from Codex round three (P2): cap the `/api/dispatch` request body in the hub viewer at 16 KB,
   answer 413 and release the slot. Do it in the follow-up PR, not on PR 60.

Do not lower the floor, do not close tabs or sessions, and do not push the estate root to `origin`.
