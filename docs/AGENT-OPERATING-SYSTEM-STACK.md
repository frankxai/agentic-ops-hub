# Agent Operating System Stack

`agentic-ops-hub` owns the configuration control plane: the files and generated rule surfaces that keep coding agents aligned before they touch code, tools, memory, or deployment.

For the broader vendor-neutral architecture, use [agentic-architecture-field-guide](https://github.com/frankxai/agentic-architecture-field-guide). For Starlight-specific profile topology and swarm operations, use [starlight-agent-army-architecture](https://github.com/frankxai/starlight-agent-army-architecture).

## Layer Map

| Layer | Owned here | Connects to |
| --- | --- | --- |
| Shared instructions | `AGENTS.md` | Codex, Cursor, Copilot, Gemini, Cline, Claude shim |
| Tool-specific shims | `CLAUDE.md`, `.cursor/rules/*.mdc`, `.clinerules/*.md`, Copilot instructions | Claude Code, Cursor, Cline, Copilot |
| Skills | `.claude/skills/*/SKILL.md`, ACOS skill template | Claude Code, Codex skills, portable skill libraries |
| Hooks and enforcement | Generated guardrails plus `claude-code-hooks` pointers | Lifecycle gates, circuit breakers, audit trails |
| MCP connectivity | Strategy docs and `mcp-doctor` references | Filesystem, browser, GitHub, Vercel, memory, custom tools |
| Runtime orchestration | Coordination protocol in `AGENTS.md` | Codex worktrees, Claude Code subagents, DeepAgents harnesses |
| Local agent fleet | Links and policy, not runtime ownership | Hermes Agent profiles, OpenClaw gateway, Starlight Swarm |

## How It Fits

- Hermes Agent provides durable local worker identities and a kanban-style handoff board.
- OpenClaw exposes approved local agents through chat and mobile channels.
- DeepAgents provides durable harnesses for long-running research or coding work.
- Claude Code consumes `CLAUDE.md`, skills, MCP, and subagents.
- Codex consumes `AGENTS.md`, rules, hooks, skills, MCP, worktrees, and repo-local context.
- `mcp-doctor` checks whether the integration layer is healthy enough for agent work.

This repository should not duplicate runtime documentation for those tools. It should define the common operating contract that all of them inherit.

## Operating Rule

If a behavior should apply to every coding agent, put it in `AGENTS.md` and regenerate downstream rule files. If it is enforcement rather than advice, wire it through hooks. If it is tool access, treat it as MCP or platform configuration with explicit trust boundaries.
