# Agent Purpose Map — Which Agents We Run, For What, How, Why

**Machine:** C940 (`DESKTOP-1B4ICID`) — always-on backend/content/GEO/ops control plane.
**Peer:** Yoga Book — frontend/UI/innovation (currently **OFFLINE**; Packet 4 unbooted).
**Last verified:** 2026-08-29 (real `hermes`, `gh`, `git`, cron, disk output).

The estate is a layered agent system. Three layers, one flywheel:

```
CONTENT (FrankX → frankx.ai)  →  FUNNEL BRIDGE (R1 → GenCreator)  →  PRODUCT (GenCreator/Arcanea/VibeClubs)
        │                                  │                                  │
        └──────── built by the INFRASTRUCTURE FLEET (SIS · ACOS · agentic-ops · crons · bus) ───────┘
```

---

## 1. The runtime workforce (who actually executes)

| Runtime | Verified | Role in fleet | Why |
| --- | --- | --- | --- |
| **Hermes** (default `grok-4.6`) | 12 profiles, 17 crons | Always-on control plane, scheduled loops, profile-isolated lanes | 24/7 backend/content/ops without frontend bloat |
| **Codex CLI** | present | Code changes, repo ops, controlled tool use | Fast, deterministic patches |
| **Claude Code** | present (Max) | High-complexity backend/content when needed | Compatibility + Claude-specific workflows |
| **OpenCode** | present | Complements Codex | Alternate backend runtime |
| **Grok / xAI** | primary model | Reasoning + native image gen (Grok Imagine) | Asset pipeline + content |
| **SIS MCP** (`starlight-sis`) | 13 tools | Durable memory + goal state | Sovereign, local-first memory authority |
| **ACOS** | skills/agents/hooks | Reusable capability factory | Don't rebuild primitives per repo |

**Hermes profiles** (10 stopped, 2 relevant): `default` (grok-4.6, running — general + control plane), `arcanea-agent` (stopped — Arcanea mythic lane), `music-producer` / `publishing-house` (stopped — content lanes), `gemini-35` (stopped). Profiles are isolated lanes; most stay stopped to avoid a second gateway fighting `default`.

---

## 2. The standing agents we run (by purpose)

### A. Infrastructure / control-plane agents (C940-owned)
| Agent | Purpose | How it runs | Why |
| --- | --- | --- | --- |
| **SIS memory maintenance** | Dreaming/consolidation of sovereign memory vaults | `sis-memory-maintenance` cron (Mo–Fr 11:00, LLM, receipted) | Memory is the cross-agent recall layer; must stay fresh |
| **Railway Queen (weekly)** | Read-only review of Railway estate (health, billing, rotation) | `railway-queen-weekly-review` cron (Mon 09:30) | Capacity/cost visibility; no mutation |
| **Railway rotation audit (monthly)** | Secrets/rotation compliance check | `railway-monthly-rotation-audit` cron (1st 10:00) | Security hygiene |
| **Fleet swarm pulse** | Heartbeat + Swarm bulletin | `fleet-swarm-pulse` cron (every 6h, no-agent) | Real+tive liveness to peer + channel |
| **Host watchdog** | C940 uptime/power/health | `c940-always-on-host-watchdog` (every 120m) | Always-on machine must self-report |
| **Security sentinel** | Intrusion/defense posture | `c940-security-sentinel-watchdog` (every 720m) | Early warning |
| **Disk growth guard** | Enforce 35 GiB hard floor | `c940-disk-growth-guard` (every 60m) | Prevent OOS thrash |
| **Safe reclaim worker** | Remove idle cache leaves only | `c940-safe-reclaim-worker` (every 360m, gated) | Recover space without touching source |
| **Topology / storage / brand-media / design / evals / grok-bot / tech-radar / creative watchdogs** | 9 script-only monitors | various cadences | Cheap, reliable, no-agent signal |

### B. Content / funnel agents (C940 content lane — FrankX Professional register)
| Agent | Purpose | Why |
| --- | --- | --- |
| **Content/GEO strategy** | Answer-first SEO+GEO articles, llms.txt, schema, Share-of-Synthesis | Top-of-funnel reach → GenCreator CoE |
| **Image asset pipeline** | Grok Imagine heroes/marketing for frankx.ai/Arcanea/GenCreator | High-converting visuals |
| **Brand GEO audit** | Satellite brands (AnimeLegends/VibeClubs) llms/schema | Visibility in AI answers |
| **PR review swarm** | Tiered PR review across prod/Arcanea/ACOS/SIS | Gate quality before merge |

### C. Product / frontend agents (Yoga Book lane — OFFLINE until Packet 4)
| Agent | Purpose | Why (when online) |
| --- | --- | --- |
| **Frontend/UI builder** (Codex + Antigravity) | frankx.ai / GenCreator / Arcanea UI, R1 CTA UI | Pixel polish C940 can't do |
| **Book heartbeat** | Self heartbeat `yoga-book.json` | Completes the two-machine bus |

### D. Cross-repo judgment (not a bot — a protocol)
| Agent | Purpose | Why |
| --- | --- | --- |
| **Agent Council** | Register / cross-repo / ship / plan-cap verdicts | Stops scope/voice bleed across repos |
| **Starlight Council (brand)** | Arcanea/Starlight brand calls | Brand canon authority |

---

## 3. The fleet bus (how agents coordinate)
- **Heartbeats:** `fleet/bus/heartbeats/{c940,yoga-book}.json` — each machine writes only its own (no forgery).
- **Identity:** `fleet/bus/identity/c940.json` — host/platform proof.
- **Queues:** `fleet/bus/queues/{to-c940,to-book}.json` — command-center dispatch (C940 ↔ Book).
- **Inbox / activity:** one-way status + proposals; private DMs never cross machines (mirror via `fleet_activity.py propose`).
- **Telegram:** DM = work; Starlight Swarm channel = bulletin only (`@mention` required, `busy_input_mode=queue`, anti-thrash filter).

---

## 4. Why this shape (the doctrine)
- **Specialization + controlled sharing:** C940 backend/content/ops; Book frontend. Prevents context bleed and maximizes each machine's strength (DEVICE-STRATEGY.md).
- **One SoT per concern:** status=`OPS-LEDGER.md`, objectives=`objectives-registry.json`, clones=`clone-manifest.json`, crons=`cron-classification.json`, memory=SIS. No second authority.
- **Register boundaries:** FrankX Professional / Arcanea Mythic / SIS-ACOS Neutral — enforced by Agent Council + publish gates.
- **Enhance-never-erase + leases:** dirty trees are fetch-only; never mass-wipe; one agent = one branch.
- **Watchdogs > LLM loops:** reliability; 12 script watchdogs vs 1–2 LLM lanes.
- **Capacity floors are gates:** <35 GiB hard stop, <50 ops RED, ≥80 target.

---

## 5. What "maximized" looks like next (not yet done)
1. **Boot the Yoga Book** (Packet 4) → real two-machine bus; Book claims R1 CTA UI.
2. **Refresh GitHub harness inventory** → register the 214 unregistered operational repos or mark them dormant.
3. **Disk to ≥80 GiB** → unlock safe media/restic/content sprints.
4. **Pin models on all LLM crons** (some still drift to default gateway).
5. **Clean canonical worktree** → enable `llm-evals-weekly-d0-regression` live run.
