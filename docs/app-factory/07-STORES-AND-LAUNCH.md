# 07 — App stores and web launch

## Web launch

1. Production deploy (Vercel/estate standard)  
2. `world-class-web-release` + web-release-gate  
3. OG image (Imagine or designed) + metadata  
4. Analytics + error tracking  
5. AI disclosure if generative  
6. Receipts → ACTIVITY-LOG / bus  

## Google Play

### Engineering

- Expo EAS Build production Android  
- Target API per current Play policy  
- Data safety form complete  
- Third-party AI = User Data policy (disclosure + consent)  

### Generative AI

- Follow Play AI-Generated Content policy  
- In-app report/flag for generated content  
- No prohibited categories  

### Listing

- Short/long description honest about AI  
- Screenshots from QA pack (phone + optional tablet)  
- Feature graphic  
- Privacy policy URL live  

## Apple App Store

### Engineering

- EAS Build iOS  
- Privacy nutrition labels  
- App Intents if agentic OS integration  

### Policy posture (2026)

- Disclose AI-generated content  
- Bounded agent behavior (no self-modifying mini-app shells that violate guidelines)  
- Predictable capabilities post-review  
- Permission strings human-readable  

### Listing

- Screenshots 6.7" + 5.5" (and iPad if supported)  
- Preview video optional  
- Review notes: test account + agent behavior explanation  

## Dual-store release checklist

Use `checklists/SHIP-GATE.md`.

## Store + agentic features matrix

| Feature | Play | iOS |
| --- | --- | --- |
| Cloud agent chat | OK with disclosure | OK with disclosure |
| On-device tools | AppFunctions | App Intents |
| Unbounded device control | High reject risk | High reject risk |
| IAP for subscriptions | Play Billing | StoreKit |
| External AI APIs | Declare data sharing | Declare data sharing |

## Post-launch

- Crash-free monitoring 72h  
- Persona follow-up (5 users)  
- Kill or double-down per kill criteria  
- Pattern screenshots → example library if novel UX wins  

## Output

- Store listings draft  
- Build numbers  
- Policy attestation notes  
- Launch receipt  
