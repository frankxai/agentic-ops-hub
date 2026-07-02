# MCP Strategy — Own vs Adopt

> Which Model Context Protocol servers the ecosystem **builds and owns** versus **adopts from third parties**, and the rule for deciding which.

Last updated: 2026-06-14.

---

## The build-vs-adopt rule

Build an MCP server only when **all three** hold:

1. **It encodes our proprietary substrate** — vaults, attestation, income logic, payment governance. Things no vendor will ever model the way we need.
2. **It is a control surface, not a data source** — it gates, authorizes, or governs an action (not just fetches data a generic connector already provides).
3. **We can keep it small and verifiable** — a handful of tools, testable, auditable. The moment it sprawls, split it.

Otherwise **adopt**. A vendor maintains it, ships updates, carries the security burden. We wire it through the tool-agnostic placeholder pattern (`CONNECTORS.md`) so any equivalent can swap in — no lock-in.

---

## Servers we own

| Server | Repo | Tools (representative) | Why we own it |
|---|---|---|---|
| **SIS Vault MCP** | `Starlight-Intelligence-System/src` | `sis_vault_search`, `sis_append_entry`, `sis_confirm`, `sis_contradict`, `sis_stale` (10 total) | Proprietary memory substrate + attestation. The ground truth no vendor models. |
| **ACOS servers (7)** | `agentic-creator-os/mcp-servers` | creator, evaluator, browser, database, email, filesystem, website | Creator-specific automation + quality scoring + audit. Optional, ship-as-built. |
| **Payments MCP** (new, WP2) | `payment-intelligence-system/mcp` | `verify_mandate`, `check_spend_cap`, `record_audit_entry`, `require_human_approval` | **Control surface for money.** Governs authorization — must be ours, small, and auditable. ⚠️ v0.1 scaffold, unaudited, not for live funds. |
| **Cockpit MCP** | `Starlight-Intelligence-System/cockpit/mcp` | workspace topology, session mgmt | Internal orchestration surface. |

**Owned-server discipline:** each owned MCP ships its `mcp.json` per SIP Layer 3, has unit tests, and a README stating its trust boundary. Control-surface servers (Payments) must **fail closed** — reject on ambiguity, never silently pass.

---

## Servers we adopt (third-party)

| Server | Source | Used for | Swappable with |
|---|---|---|---|
| **Higgsfield** | `mcp.higgsfield.ai` (HTTP) | Image/video/character gen (Soul, Flux, Kling, Veo, Sora) | any `~~image/video generation` MCP |
| **claude-flow** | `npx @claude-flow/cli` | Swarm topology, queen/hierarchical coordination, agent IAM | (orchestration backbone) |
| **Notion** | `@notionhq/notion-mcp-server` | Knowledge base, brand docs | any `~~knowledge base` MCP |
| **Slack** | `@modelcontextprotocol/server-slack` | Approvals, announcements | any `~~chat` MCP |
| **Resend** | `resend-mcp` | Email marketing, newsletter | any `~~email` MCP |
| **Figma** | `@figma/mcp-server` | Design system, brand tokens | any `~~design` MCP |
| **Stripe / ACP** | Stripe Agentic Commerce Protocol | Card settlement via Shared Payment Token | ACP-compliant processor |
| **Coinbase x402** | x402 Foundation | Onchain USDC settlement (Base/Solana) | any x402 facilitator |
| **Supabase / Vercel / GA** | vendor MCPs | DB, deploy, analytics | equivalents |

---

## Payments: the three protocols we wire (June 2026 state)

These are **adopted standards**, not servers we reimplement. Our Payments MCP sits *above* them as a governance layer.

| Protocol | Owner / License | Role in our stack | Status (2026) |
|---|---|---|---|
| **AP2** (Agent Payments Protocol) | Google, Apache 2.0 | **Authorization layer** — cryptographically signed mandates prove a user authorized a specific purchase. Does not move money. | v0.2.0 (Apr 2026). Python + TS/Kotlin/Go refs. Partners: Mastercard, Amex, PayPal, Adyen, Coinbase. |
| **x402** | Coinbase + Cloudflare Foundation | **Settlement rail** — HTTP 402 → agent signs USDC stablecoin tx onchain (Base/Solana). | Live, low real volume. Core members incl. Google, Visa, AWS, Circle, Anthropic, Vercel. |
| **ACP** (Agentic Commerce Protocol) | OpenAI + Stripe, beta | **Checkout rail** — Shared Payment Token lets an agent pay without seeing card details; OAuth 2.0 delegated auth. | Beta. Powers ChatGPT Instant Checkout. |

**How they compose:** AP2 answers *"was this authorized?"* (mandate) → x402 *or* ACP answers *"how does the money move?"* (onchain USDC vs tokenized card). AP2 + x402 already integrate. Our Payments MCP verifies the AP2 mandate and enforces spend caps **before** any rail settles.

Full protocol detail: `payment-intelligence-system/docs/PAYMENT-PROTOCOLS.md`.

---

## Investing: broker MCP policy (July 2026 state)

Same build-vs-adopt logic as payments: brokers are **adopted official MCPs**, never reimplemented — and they sit *below* our own governance layer, the **trade-gate MCP** (`Starlight-Intelligence-System/verticals/investment-intelligence/mcp/trade-gate/` — caps + single-use human approval token above the DCA whitelist + append-only audit; paper broker default; live adapters ship as NOT_WIRED stubs).

| Server | Source | Used for | Gate posture |
|---|---|---|---|
| **Alpaca MCP V2** | official `alpacahq/alpaca-mcp-server` (MIT) | stocks/ETF/options/crypto orders + data; `ALPACA_PAPER_TRADE=True` by default | wired operator-local only; paper parity before any live key |
| **IBKR AI integrations** | Interactive Brokers | EU/NL live path; its "AI Instructions" review tab is a broker-side human gate | composes with (never replaces) the trade-gate token |
| **Coinbase for Agents / AgentKit** | Coinbase (Apache-2.0) | crypto with MPC wallet, session caps, per-tx limits | custody never self-built |
| **OpenBB ODP · Ghostfolio · Actual Budget · Langfuse** | self-hosted (AGPL/AGPL/MIT/MIT) | data · portfolio · ledger · agent traces | T0 sovereign tier; read-only tokens for agents |

**Skip-list (reviewed 2026-07-02):** FinGPT/FinRL (research-grade), hummingbot (off-mission HFT), Maybe Finance (dead), Monarch (redundant), LangSmith (closed SaaS; Langfuse covers it), Nous Portal (OpenRouter is the machine route). freqtrade runs as a GPL appliance for backtests — never merged.

Routing tiers + data-classification rule (balances are local-only): `Starlight-Intelligence-System/verticals/investment-intelligence/ROUTING.md`.

---

## Configuration by operator profile

| Operator | MCP stack to enable |
|---|---|
| **Founder** (full control) | SIS Vault · Payments · ACOS-7 · claude-flow · Higgsfield · Notion · Slack · Stripe/x402 |
| **Individual creator** | SIS Vault (read) · Higgsfield · Notion · Resend — no Payments control surface |
| **Income swarm** (`starlight-swarm`) | SIS Vault · Payments (verify only) · claude-flow · Slack (approvals) |
| **Community / OSS user** | claude-skills-library + adopted MCPs only; owned control surfaces stay private |

Wiring: each repo declares its MCP set in `.mcp.json`; placeholders resolve per `CONNECTORS.md`. Never ship secrets in `.mcp.json` — env-injected only.
