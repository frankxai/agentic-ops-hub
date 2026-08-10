# 02 — Persona testing + GStack-style gates

## Goal

Stress-test the brief with **target humans** and **multi-role agent reviews** before UI spend.

GStack ([garrytan/gstack](https://github.com/garrytan/gstack)) encodes CEO / eng / design / QA modes as Claude Code skills. Estate policy: **use gstack cognitive modes on Claude**; keep Hermes as orchestrator; do not fork a second home.

## A. Persona SOP

### Create 1–3 personas

Use `templates/PERSONA.md` each:

| Field | Rule |
| --- | --- |
| Name + role | Specific (e.g. “Maya, solo creator, 12k IG”) |
| Context | Tools they already pay for |
| Job success | Observable outcome in minutes |
| Anxiety | What makes them quit in minute 1 |
| Quote | Real or tightly hypothesized language |
| Device | Phone-first vs desktop-first |
| Willing to pay | Range + trigger |

### Persona walkthrough (pre-UI)

Narrate the happy path out loud / in writing:

1. How they discover the product  
2. First 60 seconds  
3. Core job completion  
4. Why they return tomorrow  

Fail if any step needs a tutorial to understand.

### Lightweight human test (when available)

- 5–10 unmoderated tasks OR 3 live calls  
- Script: `templates/PERSONA-TEST-SCRIPT.md`  
- Record: task success, time, confusion points, willingness to pay  

## B. GStack-equivalent gate sequence

Run in order. **No code until Design gate passes or explicitly waived for a spike.**

| # | Mode | Question | Estate how |
| --- | --- | --- | --- |
| 1 | **Office hours** | Is this the right problem framing? | Claude `/office-hours` if gstack installed; else Hermes multi-llm-council with brief |
| 2 | **CEO / product** | Scope cut? Wedge? Revenue path? | `/plan-ceo-review` or council “CEO seat” |
| 3 | **Eng** | Data model, 10× load, edge cases, security | `/plan-eng-review` or grok eng critique |
| 4 | **Design** | Hierarchy, states, AI-slop risk, motion | `/plan-design-review` + SDI `anti-slop-frontend` |
| 5 | **Later: Review** | Implementation hallucinations | `/review` post-PR |
| 6 | **Later: QA** | Browser click-through | gstack `/qa` + Hermes `dogfood` |

### Install gstack (Claude Code) — once per machine

```bash
# Prefer official install from garrytan/gstack README when network allows
gh repo clone garrytan/gstack ~/sources/gstack -- --depth 1
# Follow repo install into Claude Code skills/commands
# Verify: claude then /office-hours appears
```

If install blocked: use `templates/GSTACK-RUN.md` prompts verbatim in Claude or Hermes multi-llm-council.

### Pass/fail rubric

| Gate | Pass means |
| --- | --- |
| Office hours | Problem reframed or confirmed; alternatives listed |
| CEO | Scope ≤ MVP; price hypothesis; non-goals explicit |
| Eng | Architecture sketch; threats; “won’t do v1” list |
| Design | Dimensions scored; gaps fixed in plan; pattern IDs chosen |

**Document all four** in `templates/GSTACK-RUN.md` inside the product repo under `docs/app-factory/` or `.hermes/briefs/`.

## C. Combined “target persona × gstack” session (90 min)

1. Load brief + primary persona  
2. Office hours (15)  
3. CEO cut (20)  
4. Eng constraints (20)  
5. Design plan review (20)  
6. Update brief + write design contract shell (15)  

## Agent orchestration prompt

```text
You are running App Factory phase 2.
Brief: {{path}}
Persona: {{path}}
1) Run office-hours forcing questions.
2) CEO review: cut 50% of features; keep wedge.
3) Eng review: propose minimal architecture for web|expo|aaas.
4) Design review: score hierarchy, typography, states, AI-slop 0-10; define what 10 is.
Output filled GSTACK-RUN.md. No production code.
```

## Outputs

- [ ] Personas (1–3)  
- [ ] GSTACK-RUN.md with decisions  
- [ ] Updated PRODUCT-BRIEF (scope cuts applied)  
- [ ] Go / pivot / kill  
