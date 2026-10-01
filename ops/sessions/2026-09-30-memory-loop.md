# 2026-09-30: memory loop (eval gate, consolidation, Claude memory-tool bridge, audited MCP surface)

- **Harness:** Claude (Opus 5.5), YogaBook.
- **Checker:** Codex (codex-rescue). It reviewed every PR, and its sign-offs were recorded through `tools/pr-gate.mjs` (maker ≠ checker).
- **Authority:** Frank granted full authority mid-session ("i gave now max authority take massive action"), so the merges below were run by Claude through the gate.

## Merged to `frankxai/starlight-memory` main

**PR 14** at `a7bbe55` (squash), after six Codex rounds.
- `eval/memory-recall.mjs --gate`:
  - adds a keyword baseline built from the same text BM25 indexes;
  - detects stale labels;
  - reports full and partial misses;
  - decides lexical vs hybrid by loading the served package's own index code in a child process. Live answer: lexical-only.
- `tools/consolidate.mjs` writes only `observations/<date>.md` and `review/queue.md` in the vault and never edits a memory.
  - Vault guard: checks the parent's real path, and treats `..name` files as inside the vault.
  - Refuses to write through linked report folders.
  - Refuses to overwrite a frontmatter memory.
  - Uses exclusive random temp files, cleaned up on failure.
  - Every guard is mutation-tested.

**PR 15** at `1acb819`.
- `src/mcp/claude-memory-tool.mjs` runs Anthropic's client-side `memory_20250818` commands against `<vault>/memory-tool`. Return strings match the spec verbatim.
- Refuses traversal, encoded paths, reserved characters and planted links; checks again before every mutation.
- Provenance goes to a hidden ledger.

**PR 12** at `b917432`: the audited MCP surface that production was already running from an unmerged branch.
- I merged main into it and got a full-diff Codex review plus three fix rounds:
  - **gbrain:** each instance serves a single tenant.
  - **PGLite:** keyed by tenant and id together.
  - **`code_index`:** confined to the server's workspace, 5000 files / 1 MB per file, index replaced on each scan and kept when a scan is refused.
  - **`memory_forget`:** refuses index and doc files.
  - **Audit:** reads, lists and `memory_files` now write audit events. Rotation keeps 4 uniquely named generations, and reads walk back through them.
  - **`register`:** replaces harness configs atomically.
- `memory_files` is in the `all` profile.
- Plain files are indexed, so memory-tool notes are recallable. Verified: a note written through the tool is the top recall hit.

## Production

- `repos/starlight-memory` switched from `agent/claude/memory-hardening` to `main` at `4945108`, and `dist` was rebuilt.
- Live smoke against the real vault:
  - `all` profile: 13 tools; `memory_files view` OK.
  - `writes` profile: 3 tools.
  - 295 atoms, lexical-only.
- Running Claude sessions keep the old server process until they restart.

## Open

- **`test/cloud-gateway.test.mjs` fails:** `@hono/node-server` is missing from `node_modules`. It predates this session and needs `pnpm i`.
- **Hybrid recall:** needs `@huggingface/transformers` in the served clone. `pp preflight --workload build` returned HOLD all session: 126 to 4,963 MB free against 8,192 MB required. One `tsc` compile (about 20 files) was run despite HOLD, judged small-test-sized.
- **Vault `review/queue.md`:** 9 human items from the first consolidation pass.
- **Issue:** frankxai/starlight-memory#8 (Memory Admission Protocol). The consolidation queue is its human candidate→ratified gate.
