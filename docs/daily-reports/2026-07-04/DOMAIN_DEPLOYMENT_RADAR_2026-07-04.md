# Domain Deployment Radar - 2026-07-04

Run: 2026-07-04T08:44:38+02:00
Mode: read-only. No DNS, deploy, merge, production promotion, spend, gateway, publishing, or external-message action taken.

## Summary

- Total surfaces: 27
- Red: 16
- Yellow: 6
- Green: 5
- Meaningful change vs prior run: True

## Top Risks / Changes

- [red] agenticpassiveincome.ai - root not healthy; www not healthy; missing: deploy target - change: branch agent/cleanup-sync -> codex/production-main-sync; dirty 10 -> 2
- [red] aiarchitectacademy.com - root not healthy; www not healthy - change: latest Vercel UNKNOWN -> 
- [red] arcanea.ai - latest Vercel deployment UNKNOWN; local dirty count 98 - change: latest Vercel BLOCKED -> UNKNOWN
- [red] arcanea.com - root not healthy; missing: provider verification; missing: canonical repo; missing: deploy target - change: latest Vercel BLOCKED -> 
- [red] arcanea.dev - root not healthy; www not healthy; latest Vercel deployment UNKNOWN; local dirty count 98; missing: provider verification; missing: deploy target - change: latest Vercel BLOCKED -> UNKNOWN
- [red] arcanea.io - latest Vercel deployment UNKNOWN; local dirty count 98; missing: provider verification - change: latest Vercel BLOCKED -> UNKNOWN
- [red] arcanealabs.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-03 radar
- [red] arcanean.org - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-03 radar
- [red] disruptivepassiveincom.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo - change: no material change detected vs 2026-07-03 radar
- [red] disruptivepassiveincome.de - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: dirty 10 -> 2
- [red] frank-riemer.com - root not healthy; www not healthy; local dirty count 53; missing: provider verification; missing: deploy target - change: latest Vercel READY -> ; dirty 22 -> 53
- [red] frankx.dev - root not healthy; www not healthy; local dirty count 53; missing: provider verification; missing: deploy target - change: latest Vercel READY -> ; dirty 22 -> 53

## Radar Table

| Verdict | Brand | Domain | Root/www | Title signal | DNS/provider | Vercel latest | Repo state | Channel | Change | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | Revenue Network | agenticpassiveincome.ai | err / err |  | unknown | READY / Production / 1d | codex/production-main-sync dirty=2 head=eba102b | #brand-agentic-income | branch agent/cleanup-sync -> codex/production-main-sync; dirty 10 -> 2 | [site](https://agenticpassiveincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | AI Architect Academy | aiarchitectacademy.com | err / err |  | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=9 head=529f63d | #brand-ai-coe | latest Vercel UNKNOWN ->  | [site](https://aiarchitectacademy.com/) / [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| red | Arcanea | arcanea.ai | 200 / 200 | Arcanea™ — Creative Intelligence Platform | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN | [site](https://arcanea.ai/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.com | err / 200 |  | unknown | none mapped | no local repo | #brand-arcanea | latest Vercel BLOCKED ->  | [site](https://arcanea.com/) |
| red | Arcanea | arcanea.dev | 404 / 404 |  | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN | [site](https://arcanea.dev/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.io | 200 / 200 |  | IONOS/UI-DNS signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN | [site](https://arcanea.io/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanealabs.com | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-03 radar | [site](https://arcanealabs.com/) |
| red | Arcanea | arcanean.org | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-03 radar | [site](https://arcanean.org/) |
| red | Revenue Network | disruptivepassiveincom.com | err / err |  | unknown | none mapped | no local repo | #brand-agentic-income | no material change detected vs 2026-07-03 radar | [site](https://disruptivepassiveincom.com/) |
| red | Revenue Network | disruptivepassiveincome.de | err / err |  | IONOS/UI-DNS signal | none mapped | main dirty=2 head=d035a60 | #brand-agentic-income | dirty 10 -> 2 | [site](https://disruptivepassiveincome.de/) |
| red | FrankX | frank-riemer.com | err / err |  | IONOS/UI-DNS signal | none mapped | agent/codex/rights-foundation dirty=53 head=67f6c3b2 | #brand-frankx | latest Vercel READY -> ; dirty 22 -> 53 | [site](https://frank-riemer.com/) |
| red | FrankX | frankx.dev | err / err |  | unknown | none mapped | agent/codex/rights-foundation dirty=53 head=67f6c3b2 | #brand-frankx | latest Vercel READY -> ; dirty 22 -> 53 | [site](https://frankx.dev/) |
| red | FrankX | frankx.io | 404 / err |  | Vercel DNS/edge signal | none mapped | agent/codex/rights-foundation dirty=53 head=67f6c3b2 | #brand-frankx | latest Vercel READY -> ; dirty 22 -> 53 | [site](https://frankx.io/) |
| red | FrankX / Music | music-academy.ai | err / err |  | unknown | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-03 radar | [site](https://music-academy.ai/) |
| red | Reality Architect / Arcanea | realitydiffusion.ai | err / err |  | IONOS/UI-DNS signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-03 radar | [site](https://realitydiffusion.ai/) |
| red | Starlight Intelligence Systems | starlight-intelligence.ai | err / err |  | unknown | READY / Preview / 14h | codex/main-preserve-20260630 dirty=67 head=88073a2 | #brand-starlight | no material change detected vs 2026-07-03 radar | [site](https://starlight-intelligence.ai/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Revenue Network | agenticpassiveincome.com | 200 / 200 | Agentic Passive Income — Set it once, let it run. | Vercel DNS/edge signal | READY / Production / 1d | codex/production-main-sync dirty=2 head=eba102b | #brand-agentic-income | branch agent/cleanup-sync -> codex/production-main-sync; dirty 10 -> 2 | [site](https://agenticpassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| yellow | Product / Other | akamoto.io | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light | IONOS/UI-DNS signal | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-03 radar | [site](https://akamoto.io/) |
| yellow | Arcanea / AnimeLegends | animelegends.ai | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, a... | Vercel DNS/edge signal | READY / Production / 16d | main dirty=2 head=053d297 | #brand-anime-legends | no material change detected vs 2026-07-03 radar | [site](https://animelegends.ai/) / [vercel](https://vercel.com/starlight-intelligence/anime-legends) |
| yellow | FrankX | frankx.ai | 200 / 200 | FrankX - AI Architect & Creator Systems | Vercel DNS/edge signal | READY / Production / 5h | agent/codex/rights-foundation dirty=53 head=67f6c3b2 | #brand-frankx | dirty 22 -> 53 | [site](https://frankx.ai/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| yellow | Starlight Intelligence Systems | starlightintelligence.org | 200 / 200 | Starlight Intelligence — Persistent context for AI agents ·... | Vercel DNS/edge signal | READY / Preview / 14h | codex/main-preserve-20260630 dirty=67 head=88073a2 | #brand-starlight | no material change detected vs 2026-07-03 radar | [site](https://starlightintelligence.org/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Arcanea / Experience | vibeclubs.ai | 200 / 200 | Vibeclubs — Host a vibeclub | Vercel DNS/edge signal | READY / Preview / 11d | no local repo | #brand-arcanea | no material change detected vs 2026-07-03 radar | [site](https://vibeclubs.ai/) / [vercel](https://vercel.com/starlight-intelligence/vibeclubs-web) |
| green | Revenue Network | agenticincome.ai | 200 / 200 | Agentic Income — The AI-tool income desk. | Vercel DNS/edge signal | READY / Production / 1d | codex/production-main-sync dirty=2 head=c4e4594 | #brand-agentic-income | verdict yellow -> green; branch agent/cleanup-sync -> codex/production-main-sync; dirty 49 -> 2 | [site](https://agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticincome) |
| green | Revenue Network | disruptivepassiveincome.com | 200 / 200 | Disruptive Passive Income | IONOS/UI-DNS signal | READY / Production / 1d | main dirty=2 head=d035a60 | #brand-agentic-income | verdict yellow -> green; latest Vercel  -> READY; dirty 10 -> 2 | [site](https://disruptivepassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/disruptivepassiveincome) |
| green | FrankX / GenCreator | gencreator.ai | 200 / 200 | GenCreator — The Operating System for AI-Native Creators | Vercel DNS/edge signal | READY / Production / 7d | codex/main-preserve-20260630 dirty=1 head=dae2890 | #brand-creator-systems | verdict yellow -> green | [site](https://gencreator.ai/) / [vercel](https://vercel.com/starlight-intelligence/gencreator-ai) |
| green | Revenue Network | go.agenticincome.ai | 200 / n/a | Agentic Income Router | Vercel DNS/edge signal | READY / Production / 1d | main dirty=0 head=ddc474a | #brand-agentic-income | no material change detected vs 2026-07-03 radar | [site](https://go.agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/go-agenticincome) |
| green | Reality Architect | realityarchitect.ai | 200 / 200 | Reality Architect — Build the systems that build the life y... | Vercel DNS/edge signal | READY / Preview / 1d | main dirty=6 head=6476312 | #brand-reality-architect | verdict yellow -> green | [site](https://realityarchitect.ai/) / [vercel](https://vercel.com/starlight-intelligence/realityarchitect) |

## Missing Fields / Provider Verification Needed

- arcanea.io: missing: provider verification -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- akamoto.io: missing: provider verification, missing: canonical repo, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.dev: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.com: missing: provider verification, missing: canonical repo, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanean.org: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanealabs.com: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.dev: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.io: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frank-riemer.com: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- realitydiffusion.ai: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.com: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.ai: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincom.com: missing: provider verification, missing: canonical repo -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincome.de: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- music-academy.ai: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- starlight-intelligence.ai: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.

## Approval Gates Honored

- No domain edits without #repo-command approval
- No production deploys without brand/business owner approval
- No merge-to-main from radar automation
- No public claim that a site changed unless Vercel/Git evidence proves it
- No spend, purchase, transfer, DNS change, production promotion, Hermes gateway start, or external message from this automation

## Artifact Links

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-04\domain-deployment-radar-2026-07-04.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-04\DOMAIN_DEPLOYMENT_RADAR_2026-07-04.md
