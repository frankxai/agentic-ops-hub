# 01 — Ideate apps (SOP)

## Goal

Turn a spark into a **product brief** worth building — or kill it cheaply.

## Inputs

- Pain observed (your day, customer chat, store review, Reddit, support ticket)
- Estate brand register (FrankX / Arcanea / SIS / GenCreator / Vibeclubs / …)
- Channel: web SaaS · dual-store · AaaS · hybrid

## Process

### Step 1 — Capture the spark (10 min)

Fill `templates/IDEA-CARD.md`:

- Working title  
- One-sentence problem  
- Who hurts (role, not “everyone”)  
- Current workaround  
- Why now (tech or market shift)

### Step 2 — JTBD + wedge (20 min)

Answer in the brief:

1. **When** [situation], **I want to** [motivation], **so I can** [outcome].  
2. **Wedge:** the 10× better moment vs Google Sheet / ChatGPT tab / incumbent.  
3. **Unfair edge:** data, distribution, brand, agent fleet, domain skill, or speed.

### Step 3 — Micro-SaaS / AaaS fitness (15 min)

Score 1–5 each (need ≥18/25 to continue):

| Signal | 1–5 |
| --- | --- |
| Pain is frequent (weekly+) | |
| Budget exists (time or money) | |
| Narrow enough for MVP in ≤2 weeks agent-assisted | |
| Retention hook (habit, data lock-in, workflow seat) | |
| Differentiation not “another chat UI” | |

### Step 4 — Kill criteria (mandatory)

Write 3 conditions that stop the project, e.g.:

- 10 persona interviews → no one will pay or switch  
- Cannot complete core job in <60s after onboard  
- Store policy / AI disclosure makes core loop illegal or untrustworthy  
- Unit economics: CAC > 3 months LTV at $X price  

### Step 5 — Competitive glance (30 min, not a thesis)

- 3 alternatives (incumbent, AI wrapper, manual)  
- Screenshot or note their **primary path** only  
- Steal structure, not skin — log into `examples/patterns/` if reusable  

### Step 6 — Output

- Completed `templates/PRODUCT-BRIEF.md`  
- Optional: Hermes research sprint for market quotes  
- Gate: CEO-style challenge next (`02-PERSONA-AND-GSTACK.md`)

## Agent prompt (copy)

```text
Load app-factory-pipeline + product brief template.
Idea: {{idea}}
Brand register: {{brand}}
Channel: web | expo | aaas
Produce: IDEA-CARD + PRODUCT-BRIEF with kill criteria and fitness scores.
Do not write code.
```

## Anti-patterns

- Feature laundry lists before JTBD  
- “AI platform for everyone”  
- Skipping kill criteria  
- Designing mythology before the job (except Arcanea creative products with explicit mythic brief)  
