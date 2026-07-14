# AGENTS.md
## Unified Agent Configuration - Single Source of Truth

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

## Core Agent Execution Loop

This repo optimizes for reliable loops, not bigger one-off prompts. Every coding agent should run the same loop and leave evidence:

1. **Orient:** read the nearest `AGENTS.md`, tool-specific shim, current `git status`, and the smallest relevant code/doc surface.
2. **Bound:** turn the request into success criteria, explicit non-goals, risk gates, and a validation plan.
3. **Discover:** inspect existing patterns and current docs before inventing a new approach.
4. **Execute:** make scoped changes, preserve unrelated dirty work, and keep one coordinator responsible for synthesis.
5. **Verify:** run the most relevant checks available: unit, type, lint, build, smoke, visual, deployment, or doc consistency.
6. **Red-team:** attack the result for false claims, unsafe external actions, privacy leaks, brittle assumptions, stale generated files, and missing tests.
7. **Handoff:** report changed files, checks run, residual risks, and the exact next action.

Use subagents, queues, or swarms only when they add a real capability: context-heavy research, independent verification, cross-repo work, long-running jobs, or specialized tool access. Do not create persona-only agents. A worker must have input context, allowed tools, write scope, stop condition, validation evidence, and handoff format.

Human approval is required before spending money, sending messages, publishing publicly, changing access, deleting data, rotating secrets, promoting production, or taking any other irreversible external action.

---

## Multi-Agent Coordination Protocol

Multiple agents (Claude, Grok, Gemini, Codex, Cursor, Cline) may work this repo concurrently. Git is the coordination layer:

* **Never two agents committing in the same working tree.** Check `git branch --show-current` + `git status` before starting; read `.agent/active-agents.md` if present.
* **One agent = one branch:** `agent/<harness>/<short-scope>`. For heavy parallel work use a worktree: `git worktree add .worktrees/<name> -b agent/<harness>/<scope>`.
* **Don't edit a file another live agent is mid-rewrite on.** Last-write-wins silently clobbers work. If the tree churns under you, pause and report.
* **Integrate one at a time.** Stage your own scope with explicit pathspecs - never sweep another agent's in-flight changes into your commit.

---

## Quick Reference Commands

| Action | Command |
| :--- | :--- |
| Build project | `npm run build` or `pnpm build` |
| Run tests | `npm test` or `pnpm test` |
| Format code | `npm run format` or `pnpm format` |
| Sync agent rules | `node scripts/sync-agent-rules.mjs` |
| Verify rules in CI | `node scripts/sync-agent-rules.mjs --check` |

## Design Taste Kernel

For any site, app, landing page, dashboard, visual identity, brand, motion, media, social, or frontend task, apply the shared Design Taste Kernel before handoff:

- C:\Users\frank\starlight\repos\DESIGN_TASTE.md
- C:\Users\frank\starlight\repos\WEB_EXPERIENCE_STANDARD.md
- C:\Users\frank\starlight\repos\MOTION_TASTE_RUBRIC.md
- C:\Users\frank\starlight\repos\MULTI_AGENT_DESIGN_COUNCIL.md
- C:\Users\frank\starlight\repos\VISUAL_QA_GATE.md

When motion, scroll, generated media, GIF/video, or premium polish matters, route through the Motion Design Studio plugin/skills and verify the result visually.

<!-- PREMIUM-WEB-OS:START -->
## Premium Intelligence Web OS Adoption

This repo participates in the Starlight Premium Intelligence Web OS.

For any website, app, landing page, dashboard, brand surface, visual asset, motion system, 3D/WebGL scene, generated media, or public-facing UI work:

- Read the estate OS first: `C:\Users\frank\starlight\repos\_intelligence\README.md`.
- Use the activation contract: `C:\Users\frank\starlight\repos\_intelligence\adoption\activation-contract.md`.
- Treat `C:\Users\frank\starlight\repos\_intelligence\` as the source of truth for premium web taste, design, motion, WebGL, copy, assets, and quality gates.
- Use `/pwo` or the `premium-web-os` skill for full builds; use `/mad` for a design council pass.
- Use `/pwo review-pr` before absorbing another agent's PR or branch.
- Use `/pwo absorb-assets` before using external, generated, scientific, audio, video, or 3D assets.
- Use `/pwo motion-score` before shipping cinematic scroll, sound-paired motion, or complex choreography.
- Build static composition first, add Track A local motion second, add Track B GSAP/Lenis scroll only when earned, and add 3D only with fallback and reduced-motion behavior.
- Use VIS through `C:\Users\frank\starlight\repos\visual-intelligence` for asset provenance, curation packets, rights, and publication records.
- Use `C:\Users\frank\starlight\repos\_intelligence\visual-worlds\neural-cosmos.md` for neuroscience, cerebrum, spine, electron, signal, or golden spiral direction.
- Do not copy reference sites or agencies. Deconstruct principles and create original execution.
- Do not ship without responsive, accessibility, performance, reduced-motion, and visual QA checks appropriate to the change.

Repo-local instructions remain authoritative when stricter.
<!-- PREMIUM-WEB-OS:END -->

<!-- STARLIGHT-REPO-CONTRACT:START -->
## Starlight repository contract

Contract: `starlight.repo_profile.v2` · Team: `starlight-platform-team` · Priority: `tier-0`
- Work only in assigned paths and preserve unrelated dirty files.
- Read `SYSTEM.md`, `SCHEMA.md`, and `SKILLS.md` before architectural changes.
- Use the smallest 3–5 role team and an independent verifier for release-affecting work.
- Required handoff: artifacts, checks, verifier verdict, risks, approvals, rollback, and next bounded action.
- Human-gated actions: DNS, secrets, billing, spend, migrations, destructive operations, permissions, legal/IP, brand identity, external sends, and high-risk production changes.
<!-- STARLIGHT-REPO-CONTRACT:END -->
