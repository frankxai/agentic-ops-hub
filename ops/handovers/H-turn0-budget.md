---
id: H-turn0-budget
what: Turn-0 instructions measured at 50k to 83k tokens per harness against an 8k target; ranked cuts and a generated-core design
where: ~/.claude, ~/.codex, ~/.gemini plugins, Hermes skill dirs, starlight/AGENTS.md
owner: unassigned
status: processing
note: held to 20 Nov by the focus window (AGENTS.md guardrail 7): steps outside the spine, or features in a hold repository, wait; 2026-10-18: Codex -9.4k tokens (416 duplicate skill junctions removed), Gemini now loads AGENTS.md, RTK hook installed (Bash tool only), Nucleus doctrine compiler prototype on starlight-agent-config agent/claude/starlight-nucleus 1f20577 (keeping every binding rule needs ~23 KB per core). Hermes deny list and Antigravity plugins are Frank's call.
updated: 2026-10-21
---

## Prompt

Measured read-only on 17 October. The earlier estimate of about 35,000 tokens was low.

| Harness | Turn 0, est. tokens | Largest item |
|---|---:|---|
| Claude Code, home | about 66k (44.7k measured, about 21k MCP tool listing estimated) | agent listing, 12.4k |
| Claude Code, `starlight` | about 83k | `starlight/AGENTS.md` at 61 KB, about 15.3k |
| Codex | 66k to 72k (upper bound) | 537 skills plus 202 from 47 enabled plugins |
| Antigravity | about 50k | 793 plugin skills |
| Hermes | about 78k (upper bound) against a 65,536-token window | 1,267 skills |
| Grok | about 6k | 849 skills disabled |

Ranked cuts, each to be applied as its own reviewed change with a before and after measurement:

1. Hermes: replace the eight external skill directories with an allowlist of about 40 skills, about -70k. The current load
   exceeds its own context window.
2. Codex: merge `~/.codex/skills` and `~/.agents/skills` (450 names in both), then enable about 40, about -41k.
3. Antigravity: disable the `acos-frankx` and `starlight-skills-library` plugins, about -39k.
4. `starlight/AGENTS.md`: an 8 KB core with the rest as reference files, about -13.3k. Codex's default 32 KiB project-doc limit
   currently truncates it, so sections 10 to 13 and the Omotenashi Kernel never reach Codex.
5. Codex: 47 enabled plugins to about 15, about -12k.
6. Claude: drop unused claude.ai connectors (about -9k, estimated), cap agent descriptions (-7k), make the n8n-skills SessionStart
   hook on-demand (it injects a 23 KB SKILL.md, -5.8k; Codex already disables it), trim the ECC rules (-4.9k).
7. One copy of each duplicated doctrine block; "Slice close" exists in five copies.

Even after all cuts Claude sits near 29k because it lists about 1,000 skill names, 117 agents and 1,350 MCP tools. Proposal:
two budgets, 8k for doctrine and 8k for catalog, and one generated core (single source, rendered per harness with each
harness's size limit) instead of hand-maintained copies. Gemini CLI loads no estate doctrine at all (no `GEMINI.md`, and
`AGENTS.md` is not configured as a context file).

Separately, one harness configuration file holds plaintext cloud storage credentials; the founder was told the location
privately. Rotate them and move them to a secret store before any other change to that file.
