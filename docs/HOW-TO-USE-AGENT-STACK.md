# How to use Hermes + coding agents on this estate

Last updated: 2026-08-06 (night loops).

## Default posture

You talk to **one** agent home: **Hermes default** (Desktop, CLI, or Telegram DM).  
That agent orchestrates. It does not need a twin gateway.

```text
You
 └─ Hermes Queen (default gateway)
      ├─ skills (load on need)
      ├─ SIS MCP (memory)
      ├─ delegate_task (short leaves)
      ├─ Codex / Claude Code (heavy code, leased worktree)
      ├─ computer_use (UI only, e.g. Suno)
      └─ cron (always-on loops)
```

## What to say (triggers that work)

| You want | Say / do | What fires |
| --- | --- | --- |
| Deep multi-repo ops | DM Hermes; mention OPS-LEDGER / fleet | `agentic-fleet-strategy` + live scripts |
| Song / meditation / Suno | “make a song…” / “generate in Suno” | `music-producer-os` (+ one Create max) |
| Code feature/fix | “implement X in repo Y” | Hermes routes to Codex/Claude in a worktree |
| PR review | “review open Tier-1 PRs” or wait for 15:00 cron | `pr-review-swarm` |
| Hard ship decision | “convene council on …” | `multi-llm-council` |
| Capture knowledge | “capture this into second brain” | `second-brain-capture` + SIS |
| Health of the machine | “topology health” / cron every 6h | `topology_health_pulse.py` |

## Autonomy you already granted vs still human

| Class | Examples | Who decides |
| --- | --- | --- |
| A0–A1 | read, plan, draft | Agent |
| A2 | leased worktree code, tests, local commits | Agent (with evidence) |
| A3 | draft PR, feature-branch push when pre-approved | Agent with receipt |
| H1 | merge main, production deploy, public publish, money, secrets, bulk delete | **You** |

## Closed loops now installed

1. **Topology health** — `python %LOCALAPPDATA%\hermes\scripts\topology_health.py`  
   Cron: `topology-health-pulse` every 6h at :15 (no-agent; silent when GREEN).
2. **Mission receipts** — `mission_envelope.py envelope|receipt|validate`  
   Worker = `candidate` only. `verified` requires named independent evaluator (not self).
3. **Council** — skill `multi-llm-council` for rare stakes.
4. **Memory maintenance** — daily 11:00 on `openai-codex`.
5. **PR review swarm** — weekdays 15:00 on `openai-codex`.

## Brand / design identity path (2026-08-06)

```text
brand-identity-strategy  →  logo-system  →  tokens/design-md  →  UI
         │                      │
         │                      └─ FONT-LICENSING-SOURCES.md
         └─ REGISTER-BOUNDARIES.md

Figma → figma-design-to-code (auth gate first)
21st  → twenty-first-component-bridge (named component only)
Gen   → GENERATION-A11Y-CHECKLIST.md before production
```

Doctrine: `.agent-harness\DESIGN-EXCELLENCE.md` · audit: `brand-design-audit-20260806.md`

## Disk law (live)

- **<35GB free:** HARD RED — no heavy clones, full builds, image batches, or new worktrees unless reclaim first.
- **<50GB free:** RED ops — prefer script-only and thin docs.
- Target **≥80GB**.

Check: topology receipt field `disk_free_gb`.

## Profiles

| Profile | Gateway | Use |
| --- | --- | --- |
| `default` | **running** | Daily driver / Telegram |
| `music-producer` | stopped | Focused music Desktop/CLI |
| `publishing-house` / `arcanea-agent` | stopped | Branded personas |
| `gemini-35` | stopped | Gemini lane when wanted |

Never start a second gateway on the shared bot token.

## MCP

Live default: **starlight-memory**, **starlight-substrate** only.  
Own control surfaces; adopt commodity connectors only with profile allowlists.

## Red / blue

- Red: probe injection, self-verify, dual-gateway, secret leakage, spend bypass.
- Blue: deterministic tests, candidate≠verified, one gateway, pinned crons, disk floor.
- Money paths: `RED-BLUE-CHARTER.md` + Payments MCP fail-closed (when used).

## Verification snacks

```bash
python %LOCALAPPDATA%/hermes/scripts/topology_health_pulse.py --force
hermes mcp test starlight-memory
hermes cron list --all
python -m unittest discover -s tests -v   # in night-loops worktree or music-os
```

## What not to do

- Dual-@ two machine bots for the same task in Swarm channel  
- Treat Kanban as cross-machine SoT (git bus + OPS-LEDGER are)  
- Call worker Markdown “verified”  
- Run council or MoA on every message  
- Ship from dirty prod trees  
