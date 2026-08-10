# 00 — Pipeline overview

```text
 IDEA SPARK
    │
    ▼
 ┌──────────────────┐
 │ 1 IDEATE         │  wedge, JTBD, unfair edge, kill criteria
 │  product brief   │  → templates/PRODUCT-BRIEF.md
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ 2 PERSONA        │  1–3 target personas, day-in-life, objections
 │  + GSTACK GATES  │  office-hours → CEO → eng → design reviews
 └────────┬─────────┘  → templates/PERSONA.md + GSTACK-RUN.md
          ▼
 ┌──────────────────┐
 │ 3 SOTA DESIGN    │  stack, tokens, pattern library, design contract
 │  libraries/style │  → estate-design-excellence + SDI skills
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ 4 RAPID BUILD    │  Expo or Next scaffold → shadcn → states → motion
 │  CLIs in parallel│  grok -w + hermes + claude gstack skills
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ 5 HUMAN QA       │  persona walkthrough, dogfood, a11y, mobile
 │  browser + real  │  screenshot library + scorecard
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ 6 PACKAGE        │  micro-SaaS pricing OR AaaS tool surface
 │  metering/auth   │  MCP/AppFunctions/Intents as needed
 └────────┬─────────┘
          ▼
 ┌──────────────────┐
 │ 7 LAUNCH         │  Play + App Store and/or web
 │  disclosure/AI   │  receipts → bus/ACTIVITY-LOG
 └──────────────────┘
```

## Time boxes (default sprint)

| Phase | Solo + agents | Output |
| --- | --- | --- |
| Ideate | 30–90 min | Brief + kill criteria |
| Persona + GStack | 1–3 h | Pass/fail + scope cuts |
| Design contract | 1–2 h | Tokens, 3 directions max, pattern picks |
| Spike UI | 2–8 h | Clickable primary path |
| Build MVP | 1–5 days | Working core loop |
| Human QA | 0.5–2 days | Scorecard ≥ ship bar |
| Package + store | 1–7 days | Listings, builds, policy |

## Blade map (who does what)

| Blade | Best for |
| --- | --- |
| **Hermes** | Orchestration, research, image gen, bus, Queen sprints, this skill |
| **Grok Build** | Fast product code in worktrees, Imagine heroes, polish |
| **Claude Code + gstack** | CEO/eng/design/review/QA cognitive modes |
| **Codex** | Overnight bounded implementation |
| **Gemini CLI** | Alternate long-context critique |
| **SDI skills** | Anti-slop, release gates, brand packs |
| **dogfood skill** | Exploratory QA with evidence |

## Decision tree — web vs store vs AaaS

```text
Is the primary job mobile-native (camera, push, offline, OS agents)?
  YES → Expo dual-store (+ AppFunctions/Intents if agentic)
  NO  → Is the buyer a team paying monthly for a workflow?
          YES → Next.js micro-SaaS (web-first)
          NO  → Is value "agent that does the work via tools"?
                  YES → AaaS (API + thin client + MCP tools)
                  NO  → Content/tool site or waitlist first
```

## Exit criteria before coding

- [ ] One sentence JTBD  
- [ ] One wedge vs status quo  
- [ ] Primary persona named  
- [ ] Kill criteria written  
- [ ] Scope cut list from CEO/eng gate  
- [ ] Design contract filled  
- [ ] Pattern IDs from library chosen (≤5)  
