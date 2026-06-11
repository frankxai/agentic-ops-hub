<div align="center">

![Agentic Operations Hub Banner](images/hero-banner.png)

# 🚀 Agentic Operations Hub

### The Configuration Control Plane for AI Coding Agents
**Claude Code · Codex · Copilot · Cursor · Cline · Antigravity · Grok**

One source of truth (`AGENTS.md`), one sync engine, every agent aligned — plus a curated index of the operational layer that keeps autonomous coding agents safe, fast, and consistent.

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![AGENTS.md Standard](https://img.shields.io/badge/AGENTS.md-Standard-8b5cf6?style=for-the-badge)](https://agents.md)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-0ea5e9?style=for-the-badge)](https://modelcontextprotocol.io)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-f59e0b?style=for-the-badge)](#-partnerships--collaboration)

**Aligned with the official agent platforms:**

[![Anthropic](https://img.shields.io/badge/Anthropic-Claude_Code-191919?style=flat-square&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code/overview)
[![OpenAI](https://img.shields.io/badge/OpenAI-Codex-412991?style=flat-square&logo=openai&logoColor=white)](https://developers.openai.com/codex)
[![GitHub Copilot](https://img.shields.io/badge/GitHub-Copilot-24292f?style=flat-square&logo=githubcopilot&logoColor=white)](https://docs.github.com/en/copilot)
[![xAI Grok](https://img.shields.io/badge/xAI-Grok-000000?style=flat-square&logo=x&logoColor=white)](https://docs.x.ai)
[![Google Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4?style=flat-square&logo=google&logoColor=white)](https://antigravity.google)
[![Cursor](https://img.shields.io/badge/Cursor-Rules-111111?style=flat-square)](https://docs.cursor.com/context/rules)
[![Cline](https://img.shields.io/badge/Cline-Rules-1e293b?style=flat-square)](https://docs.cline.bot)

[**⚡ Quick Start**](#-quick-start) · [**📚 Official Core Truths**](#-official-core-truths) · [**🧠 Layering Model**](#-the-layering-model) · [**🏛️ Curated Index**](#%EF%B8%8F-curated-agentic-ops-index) · [**🤝 Partners**](#-partnerships--collaboration)

</div>

---

## 🎯 Agentic Ops ≠ AIOps

This repository exists to draw — and own — an exact distinction:

| | **AIOps** (the old term) | **Agentic Ops** (this repo) |
| :--- | :--- | :--- |
| **What it operates** | Enterprise IT infrastructure: logs, metrics, alerts | Autonomous AI coding agents: Claude Code, Cursor, Cline, Codex, Grok |
| **Core mechanism** | ML models detecting anomalies in telemetry | Rules, guardrails, hooks, skills, and MCP servers governing agent behavior |
| **Who runs it** | SRE / platform teams | Developers and creators running multi-agent fleets |
| **Failure mode prevented** | Outages, alert fatigue | Drifted instructions, rogue edits, clobbered worktrees, token waste |
| **Unit of config** | Dashboards, runbooks | `AGENTS.md`, `SKILL.md`, hooks, rule files |

**AIOps** uses machine learning to monitor infrastructure. **Agentic Ops** is the developer-centric discipline of configuring, orchestrating, guarding, and aligning the AI agents that write your code. Different layer, different operator, different failure modes. This repository is the home of Agentic Ops.

---

## 📚 Official Core Truths

Agentic Ops only works if every layer traces back to **primary, official documentation** — not folklore. These are the canonical sources this hub aligns to, per vendor:

| Vendor | Agent | Official Docs (the core truth) | Config files this hub manages |
| :--- | :--- | :--- | :--- |
| **Anthropic** | [Claude Code](https://www.claude.com/product/claude-code) | [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview) · [Memory & CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory) · [Agent Skills](https://docs.anthropic.com/en/docs/claude-code/skills) · [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | `CLAUDE.md`, `.claude/skills/`, hooks |
| **OpenAI** | [Codex](https://developers.openai.com/codex) | [Codex docs](https://developers.openai.com/codex) · [AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md) · [Agents platform](https://platform.openai.com/docs/guides/agents) | `AGENTS.md` (read natively) |
| **GitHub** | [Copilot](https://github.com/features/copilot) | [Copilot docs](https://docs.github.com/en/copilot) · [Custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot) · [Copilot coding agent](https://docs.github.com/en/copilot/concepts/about-copilot-coding-agent) | `.github/copilot-instructions.md` |
| **xAI** | [Grok](https://x.ai/grok) | [xAI docs](https://docs.x.ai) · [Grok API](https://docs.x.ai/docs/overview) | `AGENTS.md` (read natively) |
| **Google** | [Antigravity](https://antigravity.google) | [Antigravity docs](https://antigravity.google/docs) · [Gemini API](https://ai.google.dev/gemini-api/docs) | `AGENTS.md` (read natively) |
| **Cursor** | [Cursor](https://cursor.com) | [Rules docs](https://docs.cursor.com/context/rules) | `.cursor/rules/*.mdc` (generated) |
| **Cline** | [Cline](https://cline.bot) | [Cline rules docs](https://docs.cline.bot/features/cline-rules) | `.clinerules/*.md` (generated) |
| **Standards** | — | [AGENTS.md standard](https://agents.md) · [Model Context Protocol](https://modelcontextprotocol.io) | `AGENTS.md`, MCP configs |

> When a vendor doc and a community convention disagree, **the vendor doc wins**. The [Curated Agentic Ops Index](#%EF%B8%8F-curated-agentic-ops-index) below layers community best practices *on top of* these core truths — never instead of them.

---

## 🧠 The Layering Model

Agent instruction files fragmented into a dozen formats. The 2026 resolution is layered:

```
AGENTS.md                      ← universal base (the agents.md standard, plain markdown)
 ├─ CLAUDE.md                  ← thin shim: @AGENTS.md + Claude-only additions
 ├─ .cursor/rules/*.mdc        ← generated (frontmatter, alwaysApply / glob-scoped)
 ├─ .clinerules/*.md           ← generated (directory format)
 ├─ .github/copilot-instructions.md ← generated
 └─ .claude/skills/coding-guardrails/SKILL.md ← generated (auto-activating skill)
```

You edit **one file**. The sync engine generates the rest with tamper-evident headers. CI verifies nothing drifted (`--check`).

> `.cursorrules` (single file) is deprecated — Cursor still reads it, but new projects should use `.cursor/rules/*.mdc`. The sync script emits the legacy file only with `--legacy`.

---

## ⚡ Quick Start

```bash
# 1. Copy the canonical source + sync engine into your project
cp templates/AGENTS.md  /path/to/project/AGENTS.md
cp templates/CLAUDE.md  /path/to/project/CLAUDE.md
mkdir -p /path/to/project/scripts
cp scripts/sync-agent-rules.mjs /path/to/project/scripts/

# 2. Fan out to all agents
cd /path/to/project && node scripts/sync-agent-rules.mjs

# 3. (CI) Fail the build if any generated rule file drifted
node scripts/sync-agent-rules.mjs --check
```

Templates ship the **Top Thinkers Guardrails** (Karpathy, Feynman, Ousterhout, Hickey, Torvalds, Beck) and a **Multi-Agent Coordination Protocol** for running several harnesses against one repo without clobbering each other.

---

## 🌌 Position in the FrankX Ecosystem

Agentic Ops is a stack. Each repo owns one layer — agentic-ops-hub is the **config control plane** that aligns them:

| Layer | Repo | Owns |
| :--- | :--- | :--- |
| **Config control plane** | **agentic-ops-hub** (you are here) | Rule source-of-truth, cross-agent sync, the Agentic Ops index |
| Capability system | [agentic-creator-os](https://github.com/frankxai/agentic-creator-os) | 90+ skills, 65+ commands, 38 agents — what agents *can do* |
| Lifecycle enforcement | [claude-code-hooks](https://github.com/frankxai/claude-code-hooks) | Quality gates, circuit breakers, audit trails — what agents *may do* |
| Integration health | [mcp-doctor](https://github.com/frankxai/mcp-doctor) | Diagnose/optimize MCP servers — what agents *connect to* |
| Machine health | [peak-performance](https://github.com/frankxai/peak-performance) | System auditing for agent-heavy machines — what agents *run on* |
| Memory substrate | [second-brain-os](https://github.com/frankxai/second-brain-os) · [Starlight-Intelligence-System](https://github.com/frankxai/Starlight-Intelligence-System) | Persistent knowledge + the SIP protocol — what agents *remember* |
| Prompt layer | [prompt-engine](https://github.com/frankxai/prompt-engine) · [prompt-library](https://github.com/frankxai/prompt-library) | Evaluated, red-teamed prompts — what agents *are told* |
| Domain expertise | [claude-skills-library](https://github.com/frankxai/claude-skills-library) | Deep research-backed domain skills — what agents *know* |

Rule of thumb: **capabilities live in ACOS, enforcement lives in hooks, configuration alignment lives here.** If a file tells multiple agents how to behave in a repo, this hub owns its lifecycle.

---

## 🏛️ Curated Agentic Ops Index

The best **community** repositories, toolkits, and skills for operating AI coding agents — layered on top of the [Official Core Truths](#-official-core-truths) above:

### 1. Behavior & Guardrails
* [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — The original viral Karpathy rules for Claude Code.
* [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel's official prompt library for coding agents.
* [wsimmonds/claude-nextjs-skills](https://github.com/wsimmonds/claude-nextjs-skills) — Evaluators and NextJS testing patterns.

### 2. Standards
* [agentsmd/agents.md](https://github.com/agentsmd/agents.md) — The AGENTS.md standard: one plain-markdown file, every agent reads it.
* [modelcontextprotocol](https://modelcontextprotocol.io) — MCP, the integration standard for agent ↔ tool connectivity.

### 3. Operational Frameworks & CLI Tools
* [affaan-m/ECC](https://github.com/affaan-m/ECC) — Everything Claude Code. Commands, skills, and security audits via `AgentShield`.
* [smithery-ai/mcp-servers](https://smithery.ai) — Index of MCP integrations.
* [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) — Operational scripting and helper toolkits.

### 4. Skill Registries
* [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — 500+ skills for Antigravity, Grok, and Codex environments.

---

## 📁 Repository Structure

* `/templates` — `AGENTS.md` (canonical source), `CLAUDE.md` (shim), legacy `.cursorrules`/`.clinerules`, ACOS `SKILL.md`.
* `/scripts` — `sync-agent-rules.mjs`: fan-out + `--check` CI verification + `--legacy` compat.
* `/docs` — `layering.md`: what goes in which file, and why.

---

## 🤝 Partnerships & Collaboration

Agentic Ops Hub is being built **in the open, with intent** — we want this to become the shared control plane for agent operators across communities.

**Current posture:**
* 🔭 **Open to building together.** Communities, toolmakers, and agent platform teams who want to align on `AGENTS.md`-first configuration are welcome — open an [issue](https://github.com/frankxai/agentic-ops-hub/issues) or [discussion](https://github.com/frankxai/agentic-ops-hub/discussions) to start the conversation.
* 🧪 **Curated, not yet free-for-all.** While the foundation stabilizes, direct collaboration is invitation-based. Index suggestions and fixes via PR are welcome; larger contributions should be discussed first.
* 🛡️ **Protected by design.** The project is [MIT-licensed](LICENSE) — free to use, fork, and distribute, with copyright retained by FrankX and no warranty liability. Vendor names and logos referenced here belong to their respective owners (Anthropic, OpenAI, GitHub, xAI, Google, Cursor, Cline) and are used only to identify the platforms this hub configures — no affiliation or endorsement is implied.

**Partner with FrankX:**

[![Partner with FrankX](https://img.shields.io/badge/🌌_Partner_with_FrankX-frankx.ai/partners-7c3aed?style=for-the-badge)](https://frankx.ai/partners)
[![FrankX Ecosystem](https://img.shields.io/badge/Explore_the_Ecosystem-frankx.ai-0ea5e9?style=for-the-badge)](https://frankx.ai)

---

## 📜 License

[MIT License](LICENSE) © FrankX. Free to use, fork, and distribute — attribution retained, no warranty. See [Partnerships & Collaboration](#-partnerships--collaboration) for how to build with us.

<div align="center">

**Built by [FrankX](https://frankx.ai)** · part of the [FrankX Agentic Ops stack](#-position-in-the-frankx-ecosystem)

</div>
