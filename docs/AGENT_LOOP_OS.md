# Agent Loop OS

Status: active operating target
Last updated: 2026-06-23
Owner: agentic-ops-hub

## Verdict

The next quality jump is not a better mega-prompt. It is a small number of enforced loops that every coding agent can run: Codex, Claude Code, Cursor, Copilot, Cline, Grok, Antigravity, OpenHands, Aider-style terminal agents, and Starlight queues.

The best public systems converge on the same pattern:

- Portable project instructions.
- A simple inspectable loop.
- Small reusable skills for procedure.
- Hooks or checks for hard gates.
- Repo maps and current code discovery.
- Sandboxed or isolated workspaces for long-running agents.
- Evals, traces, and handoff artifacts.

## Research Synthesis

| Source | What to absorb | What to avoid |
| --- | --- | --- |
| [AGENTS.md](https://github.com/agentsmd/agents.md) | One predictable project instruction file, like a README for agents. | Tool-specific instruction drift. |
| [OpenAI Codex AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md) | Layer global and project instructions with local precedence. | Assuming one global file can know every repo. |
| [Claude Code hooks](https://code.claude.com/docs/en/hooks-guide) | Lifecycle hooks can format, block protected actions, inject context, audit config, and notify. | Putting "must never happen" policies only in markdown. |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Skills load procedure on demand and can be evaluated and iterated. | Stuffing long procedures into always-on context. |
| [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | Strong results can come from a very small, inspectable loop with independent command execution. | Overfitting to ornate agent scaffolding. |
| [SWE-agent](https://swe-agent.com/latest/) | The agent-computer interface and feedback format matter as much as the model. | Hiding repo feedback behind vague tool names. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Always-on and multi-agent work need local/remote/cloud workspace control and backend switching. | Giving full filesystem access to unattended agents without hard isolation. |
| [OpenHands SDK](https://github.com/OpenHands/software-agent-sdk) | Agents, tools, conversations, and workspaces should be composable. | A single monolithic runtime for every job. |
| [Aider](https://github.com/Aider-AI/aider) | Repo maps, git visibility, lint/test feedback, and familiar git recovery are core UX. | Letting agents edit without visible diffs and checks. |
| [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) | Repo-wide and path-specific instruction files make agent guidance discoverable. | Treating Copilot, Cursor, and Cline as afterthoughts. |
| [awesome-copilot](https://github.com/github/awesome-copilot) | Agents, instructions, skills, hooks, workflows, plugins, and `llms.txt` can be indexed for machine use. | Installing giant community bundles without trust review. |

## The Starlight Loop

Every coding agent inherits this loop from `AGENTS.md` and generated projections:

1. Orient: read local instructions, git status, and the smallest relevant source surface.
2. Bound: define success criteria, non-goals, risk gates, and validation.
3. Discover: inspect existing patterns and current external docs before inventing.
4. Execute: make scoped changes and preserve unrelated dirty work.
5. Verify: run relevant tests, type checks, lint, build, smoke, visual, deployment, or doc checks.
6. Red-team: attack false claims, unsafe actions, private data leaks, generated drift, missing tests, and brittle assumptions.
7. Handoff: report changed files, checks, residual risks, and exact next action.

## Routing Rules

Default to one agent when the job is scoped and the validation is local.

Use a subagent when the work is context-heavy but can return a compact answer, or when independent verification is valuable.

Use a Starlight queue when work crosses repos, takes longer than one session, needs multiple worker lanes, or needs a synthesis owner to reconcile findings.

Use an automation when the loop recurs on a schedule or event. Codex owns recurring work that needs judgment and synthesis. n8n or Make owns low-latency event plumbing. MCP owns typed tool access. Hermes/Queen queues own bounded multi-agent execution.

Do not use persona-only agents. A worker must have objective, source context, allowed tools, write scope, stop condition, validation evidence, and handoff format.

## Enforcement Stack

| Layer | Mechanism | Current state |
| --- | --- | --- |
| Portable instructions | `AGENTS.md` | Active. |
| Tool shims | `CLAUDE.md`, Cursor, Cline, Copilot generated files | Active through `scripts/sync-agent-rules.mjs`. |
| Skills | `.claude/skills/coding-guardrails/SKILL.md` and portable skill bundles | Active generated guardrail skill. |
| Hooks | Claude Code hooks, repo hooks, future Codex-compatible lifecycle checks | Recommended for non-negotiable gates. |
| Machine-readable contract | `ops/agent-loop-contract.v1.json` | Added in this pass. |
| Consistency check | `scripts/check-agent-loop.mjs` | Added in this pass. |
| CI | Sync check plus loop contract check | Should fail on drift. |
| Work ledger | `starlight-agent-config/core/tasks/global-progress-ledger.json` | Tracks cross-repo cost and impact. |

## Red-Team Findings

1. The old failure mode was "more prompt, more personas." That creates impressive prose but weak execution. The fix is loop plus evidence.
2. Generated rule drift was a real risk because the repo depends on projections. The sync check and loop check must fail loudly.
3. Hooks are still underused. Markdown can guide; hooks must enforce protected-file, secret, publish, spend, and production gates.
4. Always-on agent systems need isolation. OpenHands-style local/remote workspace separation is the right direction before any unattended write agent.
5. Queue jobs should not claim autonomy. They should produce bounded artifacts for a synthesis owner.
6. Research sources are strong, but some public repos are moving quickly. Any vendor feature claim needs a current source check before implementation.

## Implementation Plan

1. Done: add the core loop to `AGENTS.md` and `templates/AGENTS.md`.
2. Done: project the loop into Cursor, Cline, Copilot, and Claude skill outputs.
3. Done: add a machine-readable loop contract.
4. Done: add a local consistency checker.
5. Next: wire equivalent hook gates for protected files, secret scans, external-action claims, and generated drift.
6. Next: add an eval lane in `starlight-evals` that grades handoffs against the loop contract.
7. Next: make each queue job reference the contract by ID and fail if objective, validation, or handoff format is missing.

## Scorecard

| Dimension | Grade | Reason |
| --- | --- | --- |
| Taste | A- | Small loop, plain language, low ceremony. Needs hook enforcement next. |
| Technical foundation | B+ | Strong source-of-truth and projection model. CI/checks improve it. |
| Cross-agent reach | A- | Codex, Claude, Cursor, Cline, and Copilot are covered. Grok/Antigravity need adapter readbacks. |
| Safety | B | Human approval gates are explicit. Deterministic hooks still need more coverage. |
| Automation readiness | B+ | Clear Codex/n8n/MCP/Queen ownership. Needs recurring eval receipts. |
| Red-team posture | B+ | Failure modes named and checkable. Needs live adversarial evals. |

The target is not "agents obey a beautiful prompt." The target is "agents run a loop whose artifacts make truth visible."
