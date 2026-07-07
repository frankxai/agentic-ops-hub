# What Goes Where — The Instruction Layering Model

Agent instruction files fragmented across tools. This is the resolution: one universal base, thin tool-specific layers, everything else generated.

## The decision table

| Content | File | Why |
| :--- | :--- | :--- |
| Project overview, build/test commands, conventions | `AGENTS.md` | Every agent needs it; the standard is plain markdown, zero frontmatter |
| Behavioral guardrails (Top Thinkers System) | `AGENTS.md` § LLM Behavioral Guardrails | The sync engine extracts exactly this section |
| Core execution loop | `AGENTS.md` § Core Agent Execution Loop + `ops/agent-loop-contract.v1.json` | Every agent should orient, bound, discover, execute, verify, red-team, and hand off the same way |
| Multi-agent git coordination | `AGENTS.md` | All harnesses must agree on branch/worktree discipline |
| Claude-only behavior (plan mode, subagents, hooks) | `CLAUDE.md` below `@AGENTS.md` | Claude Code natively imports AGENTS.md via `@` syntax (max 5 hops) |
| Glob-scoped or mode-conditional rules | `.cursor/rules/*.mdc` (hand-written, beside the generated one) | Only Cursor's `.mdc` frontmatter supports `globs` / `alwaysApply` |
| Path-scoped Cline rules | `.clinerules/*.md` | Cline directory format supports a `paths` field |
| Auto-activating domain knowledge | `.claude/skills/<name>/SKILL.md` | Skills trigger on description match; rules are always-on |
| Lifecycle enforcement (block bad edits, audit) | hooks ([claude-code-hooks](https://github.com/frankxai/claude-code-hooks)) | Instructions are advisory; hooks are mandatory |

## Rules of the model

1. **`AGENTS.md` is the only file you edit for shared rules.** Generated files carry a tamper-evident header; edits there get overwritten on next sync.
2. **Tool-specific files contain only deltas.** If a line would benefit every agent, it belongs upstream in `AGENTS.md`.
3. **Instructions ≠ enforcement.** Anything that must never happen (force-push, secret exposure) belongs in a hook, not a markdown file an agent can ignore under context pressure.
4. **Skills for knowledge, rules for behavior, contracts for loops.** A 4,000-word domain reference is a skill (loaded on demand); "don't refactor adjacent code" is a rule (always in context); the agent loop is a short rule plus a machine-readable contract.
5. **CI guards the alignment.** `node scripts/sync-agent-rules.mjs --check` in CI means no agent ever runs against stale rules.

## Format status (mid-2026)

| Format | Status |
| :--- | :--- |
| `AGENTS.md` | Cross-tool standard; read by Codex, Cursor, Copilot, Gemini; imported by Claude Code |
| `CLAUDE.md` | Active — Claude Code native, best used as shim over AGENTS.md |
| `.cursor/rules/*.mdc` | Active — current Cursor format |
| `.cursorrules` | Deprecated — still read, don't start new projects with it |
| `.clinerules/` (directory) | Active — current Cline format |
| `.github/copilot-instructions.md` | Active — Copilot repo-wide instructions |
