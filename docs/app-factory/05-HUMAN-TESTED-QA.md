# 05 — Human-tested QA SOP

## Goal

Prove a human can complete the job without you in the room.

## Layers

| Layer | Method | Evidence |
| --- | --- | --- |
| Automated | unit/e2e smoke | CI log |
| Agent dogfood | Hermes `dogfood` skill | bug list + screenshots |
| GStack QA | Claude `/qa` browser | pass/fail steps |
| Persona walkthrough | scripted tasks | times + quotes |
| A11y | keyboard, contrast, reduced-motion | checklist |
| Performance | LCP/INP basics | lighthouse or web-vitals note |

## Persona test script (core)

Use `templates/PERSONA-TEST-SCRIPT.md`.

Minimum tasks:

1. Land and understand value in 10 seconds  
2. Complete primary job without help  
3. Recover from a forced error (wrong input / API fail)  
4. Find settings / sign out  
5. (Mobile) complete job one-handed where relevant  

## Scorecard (ship bar)

Score each 0–10. **Ship requires average ≥8 and no 0–4 on critical.**

| Dimension | Critical? |
| --- | --- |
| Job completion success rate | Yes |
| Time-to-value | Yes |
| Hierarchy / clarity | Yes |
| Trust (copy, AI disclosure) | Yes |
| States / errors | Yes |
| Accessibility | Yes |
| Motion restraint | No |
| Visual distinctiveness | Brand-dependent |
| Performance feel | Yes if >3s LCP |

Use SDI: `evals/ui-quality-scorecard.md`, `anti-slop-checklist.md`, `web-release-gate.md`.

## Screenshot pack (required for ship)

Per `examples/SCREENSHOT-CAPTURE-PROTOCOL.md`:

- Desktop home / job  
- Desktop result  
- Mobile home / job  
- Empty state  
- Error state  
- Settings  
- (Store) 6.7" and 5.5" marketing frames if mobile  

Store under product repo `docs/evidence/YYYY-MM-DD/` and optionally mirror notable patterns into `agentic-ops/docs/app-factory/examples/screenshots/`.

## Dogfood agent prompt

```text
Load dogfood + app-factory-pipeline.
Base URL: {{url}}
Persona: {{name}}
Run primary job + error recovery.
Return: severity-ranked issues, screenshots paths, ship/no-ship.
```

## Output

- Filled scorecard  
- Issue list (P0/P1/P2)  
- Screenshot pack  
- Go / fix-forward / no-ship  
