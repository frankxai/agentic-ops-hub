# 06 — Micro-SaaS and Agentic-as-a-Service (AaaS)

## Micro-SaaS packaging

### Product shape that works (2026)

- **One painful workflow**, agent-accelerated  
- Seat or usage pricing, not vague “AI unlimited”  
- Data the user creates becomes the lock-in  
- Time-to-value < 5 minutes after signup  

### Pricing skeleton

| Tier | Includes | Target |
| --- | --- | --- |
| Free / trial | 1 job path, hard caps | Activation |
| Pro | Higher caps, history, export | Solo $15–49/mo class |
| Team | Seats, shared workspace, SSO later | $29–99/seat class |

Document in brief; implement Stripe (or estate standard) only after primary path works.

### Must-build SaaS surfaces

1. Auth  
2. Billing portal stub  
3. Usage meter display  
4. Settings / API keys if applicable  
5. Admin kill-switch for abusive generations  

## AaaS — Agentic as a Service

### Definition (estate)

A product whose core value is an **agent that takes actions via tools** on behalf of the user, not only chat.

### Architecture

```text
Client (web or mobile)
  → Your API (auth, policy, metering)
    → Agent runtime (Hermes profile / custom)
      → Allowlisted tools (MCP servers, AppFunctions, Intents, HTTP)
        → Side effects (CRM, calendar, deploy, content)
  ← Receipts + audit log to user
```

### Non-negotiable safety

- Allowlist tools; no raw shell to tenants  
- Human confirm for money, delete, external publish, irreversible  
- Per-tenant secrets isolation  
- Full tool-call audit log  
- Rate limits + budget caps  
- Clear AI disclosure in UI and stores  

### Exposure options

| Surface | When |
| --- | --- |
| In-app agent panel | Default UX |
| API + SDK | Developer buyers |
| MCP server | Power users / other agents |
| Android AppFunctions / iOS App Intents | OS agent discovery |
| Slack/Telegram bot | Workflow chat — thin, not system of record |

### AaaS MVP checklist

- [ ] One hero tool chain (3–7 tools max)  
- [ ] Policy engine (allow/deny/confirm)  
- [ ] Metering  
- [ ] Receipts UI  
- [ ] Eval set of 10 golden tasks  

## Micro-SaaS idea filters (estate-aligned)

Prefer ideas that leverage:

- Creator OS / GenCreator workflows  
- Starlight ops / memory / evals  
- Domain verticals (health, ocean, music, resorts) with real data  
- Affiliate + tool comparison only if differentiated ops  

Avoid: generic “ChatGPT frontend”, unbounded computer-use tenants, clone of Linear without wedge.

## Output

- Packaging choice: micro-SaaS | AaaS | hybrid  
- Pricing hypothesis  
- Tool allowlist (AaaS)  
- Metering events list  
