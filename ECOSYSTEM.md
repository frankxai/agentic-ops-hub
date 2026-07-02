# The Agentic Income Ecosystem — Canonical Map

> One picture of how every repo fits together: the layers, what each repo is for, what state it's in, and how income flows from intelligence to settlement.
> This file is the **contract**. When a repo's purpose is in doubt, this map wins. Reconcile with `frankx.ai-vercel-website/data/repos-manifest.json` (the public 50-repo manifest) — this file is the income/agentic-systems slice with operating detail.

Last audited: **2026-06-14**. Branch of record for the consolidation wave: `claude/agentic-repos-audit-68tqqv`.

---

## The Layer Model (L0–L7)

Every repo owns exactly one layer. Capabilities live below, money moves above, assurance wraps the whole stack.

```
L7 ASSURANCE      starlight-evals (red/blue lane) · ACOS safety hooks · santa-method
                  ▲ proves the rest is safe before it touches money
L6 SWARM RUNTIME  starlight-swarm (queens + workers + cockpit)
                  ▲ executes the income streams under governance
L5 PAYMENTS       payment-intelligence-system (vertical + MCP) · awesome-payment-agent-skills
                  ▲ authorizes + settles money (AP2 mandate / x402 rail / ACP checkout)
L4 INCOME ENGINE  affiliate-agent-skills (ext engine) → agentic-income-skills (brain)
                  → agenticincome (hub) + agenticpassiveincome (spoke) + agentic-income-template
                  ▲ generates active + passive income streams
L3 OS FAMILY      agentic-business-os · agentic-creator-os · investor OS (shipped as
                  agentic-business-os/packs/investor-os-pack + the engine at
                  SIS verticals/investment-intelligence; dedicated repo deferred)
                  ▲ packages capability into installable operating systems (5-file contract)
L2 CONFIG         agentic-ops-hub  ← YOU ARE HERE
                  ▲ one AGENTS.md source of truth, fanned out to every agent format
L1 CAPABILITY     agentic-creator-os (75+ skills, 38 agents, safety) · claude-skills-library
                  · agentic-creator-skills · starlight-agent-skills (substrate skills)
                  ▲ what agents can do
L0 SUBSTRATE      Starlight-Intelligence-System (SIP, vaults, attestation, MCP)
                  · second-brain-os (private memory)
                  ▲ memory, identity, governance — the ground everything stands on
```

**Reading the stack:** an income stream is a vertical slice. It draws *capability* from L1, is *configured* coherently by L2, *packaged* as an OS at L3, *generates* revenue at L4, *settles* money at L5, *runs* as a governed swarm at L6, and is *continuously attacked and defended* at L7 — all *remembering* through L0.

---

## Repo-by-repo status

Legend: 🟢 production · 🟡 real scaffold · 🔴 seeded this wave (was empty) · ⚪ out of income scope

| Repo | Layer | State | Purpose | This-wave action |
|---|---|---|---|---|
| `Starlight-Intelligence-System` | L0 | 🟢 v8.2.0+ | SIP substrate: agents, skills, vaults, MCP (`sis_*`), Wealth IS (ACL manifest), Crypto IS, **Investment Intelligence vertical + trade-gate MCP** (2026-07-02 board) | (consumer) |
| `second-brain-os` | L0 | 🟢 v0.2.0 | Private two-vault memory, SIP-composing, 37 tests | — |
| `agentic-creator-os` | L1 | 🟢 v11 | Canonical skills/agents/safety hub; 7 own MCP servers | (safety source) |
| `claude-skills-library` | L1 | 🟢 | 107 portable skills, CI link/frontmatter validation | — |
| `agentic-creator-skills` | L1 | 🟢 | 7-plugin ACOS marketplace | — |
| `starlight-agent-skills` | L1 | 🔴→🟡 | Substrate-level portable skills feeding SIS | **WP4** seed skills |
| `agentic-ops-hub` | L2 | 🟢 | Config control plane (this repo) + **this blueprint** | **WP0** blueprint |
| `agentic-business-os` | L3 | 🟢 v0.1.2 | OS for running a business with agents; 5-file contract | — |
| `agentic-income-skills` | L4 | 🟢 | The operating brain: `agentic-income` + `affiliate-audit` skills | (source for WP4) |
| `agenticincome` | L4 | 🟢 | Flagship hub site (3 posts, 15-program catalog) | **WP1** CI |
| `agentic-income-template` | L4 | 🟢 | Clone-and-deploy starter | **WP1** CI |
| `awesome-agentic-income` | L4 | 🟢 | Curated list (CC0) | **WP1** CI |
| `agenticpassiveincome` | L4 | 🔴→🟡 | Passive/AI-architect spoke (was README-only stub) | **WP5** scaffold |
| `payment-intelligence-system` | L5 | 🔴→🟡 | Payments vertical + MCP scaffold (AP2/x402/ACP) | **WP2** seed |
| `awesome-payment-agent-skills` | L5 | 🔴→🟡 | Curated payments-protocol/tooling list | **WP3** seed |
| `starlight-swarm` | L6 | 🔴→🟡 | Queen/worker income-swarm runtime + cockpit | **WP6** seed |
| `starlight-evals` | L7 | 🟢 | Whole-system eval; gaining Income & Payments Safety lane | **WP7** red/blue lane |
| `agentic-intelligence-system` | side | 🟡 v0.1 | AEO/GEO discoverability substrate (sibling) | — |
| `music-intelligence-systems` | ⚪ | 🔴 | Music vertical (same seed pattern, not income) | (future) |
| `ocean-intelligence-system` | ⚪ | 🔴 | Ocean vertical (same seed pattern) | (future) |
| `vibe-os` | ⚪ | 🟢 | Music state-change (research-backed) | — |

> **External dependency:** `affiliate-agent-skills` is the L4 engine (catalog + audit pipeline + business plan). It is the upstream source for `data/programs.json` and the `agentic-income` brain. It is **not** in this session's repo scope — treat it as a stable external.

---

## How income flows (the money path)

```
  INTELLIGENCE                 GENERATION                 SETTLEMENT
  ────────────                 ──────────                 ──────────
  L0 SIS Wealth IS    ──┐   (investment side: SIS verticals/investment-intelligence —
  (thesis, gate ladder) │    11-agent engine → trade-gate MCP: human token above DCA,
                        │    paper-first; brokers wired operator-local only)
                        ▼
  L4 income engine  ───────►  affiliate links (recurring)  ─┐
     agentic-income-skills    digital products              │
     (brain) → agenticincome  content → traffic → trust     │
                        │                                   ▼
  L6 starlight-swarm  ──┘    queens run the streams   ──►  L5 payments
     (Affiliate/Products/    workers do the work           AP2 mandate (was this authorized?)
      Content/Payments                                     x402 rail (settle onchain USDC)
      queens)                                              ACP checkout (Shared Payment Token)
                                                            │
  L7 starlight-evals  ◄───────────────────────────────────┘
     red team attacks every hop; blue team must hold
     before any of it touches real funds
```

**Two income modes, one engine:**
- **Active income** — workshops, products, consulting surfaced through L3 OS family + L4 content. Human in the loop per transaction.
- **Passive income** — affiliate recurring revenue (`agenticincome` hub + `agenticpassiveincome` spoke), compounding via the four self-improving loops in the `agentic-income` brain. Agents draft and optimize; humans approve structural changes.

---

## Sibling maps
- `docs/MCP-STRATEGY.md` — which MCP servers we own vs adopt, and the build-vs-adopt rule.
- `docs/AGENT-STACK.md` — founder agent vs stream queens vs workers, and the escalation contract.
- `docs/PROTECTION-LAYERS.md` — defense-in-depth for humans, agents, and wealth.
- `docs/RED-BLUE-CHARTER.md` — what red team attacks, what blue team defends, the cadence.
