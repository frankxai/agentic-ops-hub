# 🚀 Agentic Operations Hub (agentic-ops-hub)
### The Unified Command Center for AI Coding Agents: Claude Code, Antigravity, Cursor, Cline, Codex & Grok

A curated aggregator index and operational template suite to establish a single source of truth for all AI coding assistants in your projects.

---

## 🏛️ Curated Ecosystem Index

Here is a curated directory of the absolute best repositories, toolkits, and skills for AI coding agents:

### 1. Behavior & Guardrails
*   [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — The original viral Karpathy rules for Claude Code.
*   [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel's official prompt library for coding agents.
*   [wsimmonds/claude-nextjs-skills](https://github.com/wsimmonds/claude-nextjs-skills) — Evaluators and NextJS testing patterns.

### 2. Operational Frameworks & CLI Tools
*   [affaan-m/ECC](https://github.com/affaan-m/ECC) — Everything Claude Code. A powerful framework for organizing commands, skills, and running security audits via `AgentShield`.
*   [smithery-ai/mcp-servers](https://smithery.ai) — Index of Model Context Protocol (MCP) integrations.
*   [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) — Operational scripting and helper toolkits.

### 3. ACOS Ecosystem (Agentic Creator OS)
*   [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — The flagship registry containing over 500+ skills for Antigravity, Grok, and Codex environments.

---

## ⚡ Quick Start: Synchronize Workspace Rules

This repository provides ready-to-use **Top Thinkers Guardrails Templates** (incorporating Karpathy, Feynman, Ousterhout, Hickey, Torvalds, and Beck rules) and a portable synchronization script to align all active agents (Claude Code, Cursor, Cline, ACOS/Gemini) in under 10 seconds.

### Installation & Sync Setup

1.  **Copy the sync script and rules template** into your target project:
    ```bash
    cp templates/CLAUDE.md /path/to/your/project/CLAUDE.md
    cp scripts/sync-agent-rules.mjs /path/to/your/project/scripts/sync-agent-rules.mjs
    ```

2.  **Run the sync script** inside your project:
    ```bash
    node scripts/sync-agent-rules.mjs
    ```

This script extracts the rules section from `CLAUDE.md` and generates matching configs for:
*   **Cursor**: `.cursorrules` (root)
*   **Cline / Roo-Code**: `.clinerules` (root)
*   **Antigravity / ACOS**: `.claude/skills/coding-guardrails/SKILL.md` (project skill)

---

## 📁 Repository Structure

*   `/templates` — Reference configurations for `CLAUDE.md`, `.cursorrules`, `.clinerules`, and ACOS `SKILL.md`.
*   `/scripts` — Node synchronization script templates.
*   `/docs` — Platform-specific guides and best practices for configuring agents.

---

## 📜 License
MIT License. Free to use, fork, and distribute. Contribution PRs are welcome!
