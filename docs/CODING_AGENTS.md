# 🏛️ Curated Coding Agents Index & Orchestration Guide

This document is a first-principles guide for selecting, running, and orchestrating the AI coding agents available on this workstation. By understanding the relative strengths, architecture, and interfaces of each agent, you can delegate tasks to the tool best suited for the job.

---

## 📋 Coding Agents Inventory

| Agent | CLI / IDE | Primary Model | Strength | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | CLI | `claude-3-5-sonnet` | Deep reasoning, tool discovery, git & CLI autonomy | Multi-file refactors, debugging test failures, library upgrades |
| **DeepAgent (dcode)** | CLI | Model-agnostic (Anthropic, OpenAI, Gemini) | Long-horizon planning, sub-agent delegation, remote sandboxing | Complex multi-stage research + coding, isolated sandbox runs |
| **Cursor** | IDE (VS Code Fork) | GPT-4o, Claude 3.5, custom | Visual inline editing, codebase chat, multi-file edits (Composer) | Frontend UI, daily feature building, human-in-the-loop editing |
| **Codex** | CLI | OpenAI GPT-4 / GPT-5 | Raw benchmark-grade execution and automation | Standard developer tasks requiring high accuracy |
| **Grok CLI** | CLI | xAI Grok-2 | Fast terminal operations, real-time web access | Fast terminal scripting, checking real-time API changes |
| **OpenCode** | CLI | Groq llama-4-scout | Speed and zero-cost local/cloud model integration | Rapid scratchpad edits, speed-coding, and testing APIs |
| **Antigravity (agy)** | CLI | Custom Gemini / OS-level | High-velocity OS & creator workspace automation (YOLO) | Fast system scripting, cross-repo synchronization, workspace ops |

---

## 🔍 First-Principles Selection Matrix

To orchestrate these agents effectively, apply these four selection axes:

```
                      Autonomy Axis
             High Autonomy (Set & Forget)
                         │
                         │    [DeepAgent]
                         │
                         │    [Claude Code]
                         │
CLI-First ───────────────┼─────────────── IDE-First (Visual)
                         │
     [OpenCode]          │    [Cursor]
                         │
     [Antigravity]       │    [Cline]
                         │
             Low Autonomy (Interactive)
```

### 1. The Interface Choice: CLI vs. IDE
* **Use CLI-first agents (Claude Code, DeepAgent, OpenCode)** when you want the agent to operate like a junior developer in the terminal: executing commands, reading compiler errors, running test loops, and updating git status autonomously.
* **Use IDE-first agents (Cursor, Cline)** when you need a visual editor. These are optimal for frontend work (CSS/HTML/React layout changes), side-by-side diff reviews, and interactive file editing.

### 2. Autonomy Level: Interactive vs. YOLO/Autonomous
* **Low-autonomy (Cursor, OpenCode):** Best when you want to review every line as it's written. Prevents the model from going down "rabbit holes."
* **High-autonomy (Claude Code, DeepAgent):** Best when you can write a comprehensive prompt, set a goal, and let the agent write code, compile, run tests, and iterate until success.

### 3. Context & Token Management
* **Claude Code** uses a massive context window (Sonnet 3.5), making it excellent for searching across large codebases.
* **DeepAgent** includes aggressive context compaction (summarizing past history and writing files/tool outputs to disk) which enables it to handle long-running, multi-hour threads without overflowing context limits.

### 4. Sandboxing & Security
* **DeepAgent (dcode)** is built with first-class remote sandboxing (LangSmith, Daytona, Runloop, Modal). Use it when executing untrusted code or when you need a reproducible environment.
* **Claude Code & OpenCode** run natively on the host workstation. Use them for trusted internal repositories.

---

## 📦 Sources & Installation Guide

If you need to install or update these agents on a new machine or environment, use these canonical packages:

### 1. DeepAgent (Deep Agents Code)
* **Website/GitHub:** [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
* **Installation:**
  ```bash
  uv tool install deepagents-code
  # OR (natively on macOS/Linux)
  curl -LsSf https://langch.in/dcode | bash
  ```

### 2. Claude Code
* **Website/GitHub:** [anthropic-ai/claude-code](https://github.com/anthropic/claude-code)
* **Installation:**
  ```bash
  npm install -g @anthropic-ai/claude-code
  ```

### 3. OpenCode
* **Website/GitHub:** [opencode-ai/opencode](https://github.com/opencode-ai/opencode)
* **Installation:**
  ```bash
  npm install -g opencode-ai
  ```

### 4. Cursor
* **Website:** [cursor.sh](https://cursor.sh)
* **Installation:** Download desktop app for Windows/macOS/Linux.

### 5. Antigravity (agy)
* **Ecosystem Path:** Local binary managed via ACOS (`C:\Users\frank\agentic-creator-os`).

---

## ⚡ Starlight Orchestration

To run these agents instantly in their respective repository contexts, use the **Starlight Command Grid** in PowerShell:

* Launch **Claude Code**: `cl <repo>` or shortcut (`clsis`, `clfx`, `clarc`, `clapp`, `clacos`)
* Launch **Codex**: `cd <repo>` or shortcut (`cdsis`, `cdfx`, `cdarc`, `cdapp`, `cdacos`)
* Launch **Grok**: `gr <repo>` or shortcut (`grsis`, `grfx`, `grarc`, `grapp`, `gracos`)
* Launch **OpenCode**: `oa <repo>` or shortcut (`oasis`, `oafx`, `oarc`, etc.)
* Launch **DeepAgent (dcode)**: `da <repo>` or shortcut (`dasis`, `dafx`, `daarc`, etc.)
* Launch **Antigravity**: `ay <repo>` or shortcut (`agysis`, `agyfx`, `agyarc`, etc.)
