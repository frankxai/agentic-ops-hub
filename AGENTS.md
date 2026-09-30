# AGENTS.md
## Unified Agent Configuration — Single Source of Truth

This file is the canonical instruction set for every coding agent in this repository
(Claude Code, Cursor, Cline, Copilot, Codex, Antigravity/Gemini, Grok).
Edit rules HERE, then run `node scripts/sync-agent-rules.mjs` to fan out to tool-specific formats.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

---

## LLM Behavioral Guardrails (Top Thinkers System)

These guidelines enforce discipline, conceptual clarity, and simplicity:

### 1. Think Before Coding (Karpathy Rules)
* **Don't assume. Don't hide confusion. Surface tradeoffs.**
* State assumptions explicitly. If uncertain, ask.
* If multiple interpretations exist, present them - don't pick silently.
* If a simpler approach exists, push back and prioritize simplicity.

### 2. Feynman Alignment Protocol (Explain Simply)
* **What you cannot explain simply, you do not understand.**
* Before writing code, write a brief description of (a) the core problem in plain English, (b) the mental model/architecture of changes, and (c) the simplest possible solution.
* Avoid buzzwords, jargon, and hand-waving (e.g. do not say "streamline" or "optimize"; describe the exact mechanism).

### 3. Simplicity & Deep Design (Ousterhout & Hickey Rules)
* **Minimum code that solves the problem. Nothing speculative.**
* No speculative abstractions or configurability. No error handling for impossible scenarios.
* **Deep Modules**: Prefer simple interfaces with rich internals. Avoid creating cascades of shallow, single-use helper files/wrappers.
* **De-tangling**: Avoid "easy" copy-paste hacks that entangle components; keep concerns separated.

### 4. Surgical Changes & Readability (Torvalds Rules)
* **Touch only what you must. Clean up only your own mess.**
* Don't "improve" adjacent code, formatting, or comments. Don't refactor things that aren't broken.
* Match existing style, even if you would do it differently.
* If you notice unrelated dead code, mention it - don't delete it.
* **Self-Documenting Code**: Code is read much more than written. Use clear naming. Do not write comments narrating *what* code does; only explain *why* non-obvious choices were made.

### 5. Goal-Driven & Test-Driven (Beck Rules)
* **Define success criteria. Loop until verified.**
* Transform vague requests into verifiable targets.
* **Reproduce First**: Write a reproducing test or run code demonstrating a failure before implementing a bug fix.
* For multi-step tasks, state a brief plan and verification steps before writing code (e.g., `1. [Step] -> verify: [check]`).

### 6. Keep the record current (Karpathy wiki)
* **The ledger is compiled once and kept current. Do not re-derive it from chat.**
* When a slice is finished, suggest both saves, then write them if this checkout is free. Append `ops/sessions/YYYY-MM-DD.md`, refresh `ops/OPS-LEDGER.md`, and put one current prompt in `ops/NEXT-PROMPTS.md`.
* Comment on the product repo's existing GitHub issue. Open one only when the slice is still open and has none. A merged slice with no issue stays in the session file. Linear stays archive unless Frank asks.
* Branch `agent/<harness>/<scope>` from `origin/main`. If the primary checkout is another harness's branch, use a separate worktree. Do not write the handover into `C:/Users/frank/starlight` or `agentic-ops`.
* A file such as FrankX `docs/ops/HANDOVER-*.md`, or the agentic-ops Desktop reboot pack, is the in-repo pickup for the next session in that checkout. The estate record is still this ledger.

---

## Multi-Agent Coordination Protocol

Multiple agents (Claude, Grok, Gemini, Codex, Cursor, Cline) may work this repo concurrently. Git is the coordination layer:

* **Never two agents committing in the same working tree.** Check `git branch --show-current` + `git status` before starting; read `.agent/active-agents.md` if present.
* **One agent = one branch:** `agent/<harness>/<short-scope>`. For heavy parallel work use a worktree: `git worktree add .worktrees/<name> -b agent/<harness>/<scope>`.
* **Don't edit a file another live agent is mid-rewrite on.** Last-write-wins silently clobbers work. If the tree churns under you, pause and report.
* **Integrate one at a time.** Stage your own scope with explicit pathspecs — never sweep another agent's in-flight changes into your commit.

---

## Quick Reference Commands

| Action | Command |
| :--- | :--- |
| Build project | `npm run build` or `pnpm build` |
| Run tests | `npm test` or `pnpm test` |
| Format code | `npm run format` or `pnpm format` |
| Sync agent rules | `node scripts/sync-agent-rules.mjs` |
| Verify rules in CI | `node scripts/sync-agent-rules.mjs --check` |
