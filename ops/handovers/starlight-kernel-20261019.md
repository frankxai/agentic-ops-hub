---
id: starlight-kernel-20261019
what: Starlight Kernel v0: get a clean cross-vendor re-review, run the live demos, then land
where: prompt below
owner: claude
status: open
note: frankxai/starlight-kernel PR 1 at a7686e1, 46/46 tests; issue 2 tracks the rest
evidence: https://github.com/frankxai/starlight-kernel/pull/1
updated: 2026-10-19
---

## Prompt

Continue the Starlight Kernel slice in `frankxai/starlight-kernel` (private). Draft PR 1, branch `agent/claude/kernel-slice`, head `a7686e1`; local worktree `starlight/repos/starlight-kernel/.claude/worktrees/agent+claude+kernel-slice`. Tracking issue 2. Read the repo `README.md` and `AGENTS.md` first.

The kernel is an acceptance engine across vendor coding agents. An operator writes an immutable, content-addressed contract. A maker (Claude Code, Codex or Antigravity through its official CLI) works in an independent clone. Acceptance materializes the artifact from blobs and writes the contract's protected tests over it. A grader from a different vendor reviews the diff in an empty directory, and an Ed25519 receipt is bound to artifact, target, contract, evaluator and policy and fails closed. It also covers combined candidates (`merge-tree`), judging external PRs (operator CLI only), `publish` (commit status, no Actions minutes), an MCP server that hides contract creation and lesson adoption, retries that feed findings to the next maker, cost budgets, and opt-in fail-closed container isolation for acceptance.

Reviews so far:
- Codex on `923383d`: FAIL, 8 findings.
- Antigravity (Google) on `a5cc045`: FAIL, 8 findings.
- Antigravity on `e9ce295`: 4 confirmed, 4 partial, 5 new.
- All are fixed in `b41a2d0` and `a7686e1`, each with a regression test (`test/review2.test.mjs`, `test/review3.test.mjs`).

Next, in this order, each only when `pp preflight` admits it (free RAM under 4 GiB stopped this session three times):
1. **Re-review `a7686e1`** with Antigravity in read-only plan mode via stream-json (prompt pattern in the PR comments) or with Codex. Fix every finding with a test. Re-review until PASS.
2. **Live demo:** `node demo/run-demo.mjs --maker claude --grader antigravity`. This verifies the direct `claude.exe` path, the Antigravity grader end to end, and real cost capture. The 19 October attempt was killed for memory after `attempt.intent`.
3. **Live container acceptance** on a machine with Podman or Docker (this laptop has no WSL2). Use `acceptance.isolation: "container"`.
4. **Dogfood** `task create --artifact` plus `publish` on a real estate PR.

Merging: a different provider must sign off on the exact head. Private repos under the personal account get no Actions jobs (budget), while Starlight-Intelligence org repos run on the org's allowance, so moving the kernel and `starlight-memory` into the org would unblock their CI. That transfer is Frank's call under the federation ruling.

Open and stated in the README:
- Makers still run as the user.
- The Grok adapter is grader-only and its tool restrictions are unverified.

Related:
- `starlight-memory` PR 42: embedder fallback reason and a 6x faster change check. Blocked on Actions.
- The Impeccable plugin hook ran `cmd /c` under Git Bash and executed the content of every written file. It was the source of the zero-byte junk files. Fixed locally with `.bak` backups; the upstream report needs Frank's OK.
