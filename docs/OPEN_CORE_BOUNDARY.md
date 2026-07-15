# Open-core boundary: Agentic Ops public vs private

**Locked:** 2026-07-16

**Agentic Ops** is the discipline. Two GitHub repos implement it:

| Repo | Visibility | Role |
|------|------------|------|
| **[frankxai/agentic-ops-hub](https://github.com/frankxai/agentic-ops-hub)** (this repo) | **Public** | Brand, doctrine, `AGENTS.md` sync, ecosystem map, **sanitized** multi-machine patterns |
| **[frankxai/agentic-ops](https://github.com/frankxai/agentic-ops)** | **Private** | Live control plane: multi-machine bus, ASPH runtime, secrets wrappers, real task envelopes |

## Rule

> **Share the system. Keep the control plane private.**

Do **not** flip `agentic-ops` public. Do **not** invent a third bus repo (`starlight-swarm-bus` is deprecated). Do **not** put live fleet queues in token-tracker.

## What belongs here (public hub)

- Universal `AGENTS.md` + multi-harness rule sync
- Ecosystem maps and layer models
- Multi-machine **architecture patterns** (git bus + dual human bots + optional runtime mirror)
- Envelope **schema examples** with fake/demo data only
- Safety / red-blue / protection doctrine
- ASPH concepts described without private session dumps

## What must never land here

- Real `.env`, API tokens, bot tokens, SSH keys
- Live task prompts that name private repos, credentials, or customer data
- Personal machine paths as hard-required product config
- Real claim/processed/outbox bus traffic from a production fleet
- Infisical project secrets or gateway tokens

## Multi-machine pattern (sanitized)

```
You (human)
 ├─ Telegram Bot A → Machine A Hermes (gateway)
 └─ Telegram Bot B → Machine B Hermes (gateway)

Machine A  ◄── git pull/push ──►  private ops repo / multi-machine/hermes-bus  ◄──► Machine B
Machine A  ◄── optional fast mirror ──►  local runtime cache  ◄──► Machine B
```

| Layer | Purpose | Public? |
|-------|---------|---------|
| Git private bus | Durable agent↔agent tasks | Pattern yes; live tree no |
| Local runtime cache | Fast claim/complete when online | Local only |
| Dual Telegram bots | Human talks to each machine | Pattern yes |
| Joint group | Human visibility only | Optional UX |
| Bot→bot messaging | **Does not work** (Telegram API) | Document the limitation |

### Envelope schema (example — fictional)

```json
{
  "id": "00000000-0000-4000-8000-000000000001",
  "version": 1,
  "createdAt": "2026-01-01T00:00:00+00:00",
  "from": "machine-a",
  "to": "machine-b",
  "priority": 3,
  "status": "pending",
  "title": "Example peer task",
  "prompt": "Do the work. Leave evidence path.",
  "doneCondition": "Evidence file exists and report sent to human.",
  "repo": null,
  "maxMinutes": 30,
  "allowDangerous": false,
  "skills": ["todo-discipline"],
  "resultRef": null,
  "telegramNotify": true,
  "tags": ["swarm"]
}
```

### Operator rules

1. Prefer **one bot token per machine gateway** (shared token + two gateways = getUpdates fights).
2. Agent↔agent control plane = **git bus** (private), not chat history.
3. Completion requires a **resultRef** (evidence path).
4. Product work stays in product repos; this hub is config + doctrine.

## Agent routing cheat sheet

| Need | Open |
|------|------|
| How agents should behave in a repo | This hub (`AGENTS.md` templates + sync) |
| Live dual-laptop task queue | Private `agentic-ops` `multi-machine/` |
| Token/cost reports | Separate product (not the bus) |
| Profile registry UI | Separate cockpit product |

## Related docs in this hub

- [`ECOSYSTEM.md`](../ECOSYSTEM.md) — portfolio map
- [`docs/AGENT-OPERATING-SYSTEM-STACK.md`](AGENT-OPERATING-SYSTEM-STACK.md)
- [`docs/PROTECTION-LAYERS.md`](PROTECTION-LAYERS.md)
- [`docs/MULTI_MACHINE_AGENTIC_OPS.md`](MULTI_MACHINE_AGENTIC_OPS.md) — expanded multi-machine pattern
