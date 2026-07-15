# Multi-machine Agentic Ops (public pattern)

Sanitized operating model for running **two (or more) coding agents on different machines** with a human in the loop.

For the **live** Frank estate implementation, use the private control plane  
[`frankxai/agentic-ops`](https://github.com/frankxai/agentic-ops) → `multi-machine/`.  
This document is the **shareable system** only. Boundary: [`OPEN_CORE_BOUNDARY.md`](OPEN_CORE_BOUNDARY.md).

## Problem

You run Hermes (or similar) on laptop A and laptop B. You want:

1. Each machine reachable from your phone/chat.
2. Agents that can assign durable work to each other over Wi‑Fi or internet.
3. No dependency on always-on LAN/SSH.

## Hard constraint (Telegram)

**Bots cannot receive messages from other bots.**  
Therefore “Bot A tags Bot B” is **not** an agent control plane. Telegram is for **you**.

## Recommended stack

| Channel | Role |
|---------|------|
| **Private git bus** | Durable agent↔agent task envelopes (SSOT) |
| **Optional file mirror** of a *runtime cache only* | Faster claim/complete when both online |
| **One Telegram bot per machine** | Human ↔ each agent |
| **Optional joint group** | Human sees both reports; not agent networking |
| **SSH** | Emergency shell only |

## Task envelope principles

- `priority` is an **integer** (lower = more urgent).
- Every task has a **doneCondition**.
- Completion requires a **resultRef** (path to evidence).
- Prefer draft-safe GitOps and fail-closed money/secrets paths.

See schema example in [`OPEN_CORE_BOUNDARY.md`](OPEN_CORE_BOUNDARY.md).

## Daily cadence (pattern)

| Cadence | Machine A | Machine B |
|---------|-----------|-----------|
| Always | Gateway bot A | Gateway bot B |
| Every 10–15 min | Pull/sync bus; claim inbox A | Pull/sync bus; claim inbox B |
| Peer work | Enqueue to B + push | Enqueue to A + push |
| Heartbeats | Write heartbeat A | Write heartbeat B |

## Anti-patterns

| Don’t | Why |
|-------|-----|
| One bot token, two gateways | getUpdates conflict |
| Chat history as the only queue | Lost on compress/reset |
| Syncthing entire git worktrees | Corrupts indexes |
| Public repo for live envelopes | Leaks prompts/paths/ops state |
| New ad-hoc “swarm-bus” product repo | Splits SSOT; use private ops home |

## Where this fits in the public stack

| Layer | Public repo |
|-------|-------------|
| Config control plane | **agentic-ops-hub** (this repo) |
| Live private ops | agentic-ops (private) |
| Capabilities | agentic-creator-os |
| Lifecycle hooks | claude-code-hooks |
| Machine health | peak-performance |

---

*This is doctrine for builders adopting Agentic Ops. It deliberately omits private paths, tokens, and live fleet state.*
