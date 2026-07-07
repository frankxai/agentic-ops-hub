# Domain Deployment Radar - 2026-06-28

Run: 2026-06-28T08:38:45+02:00
Mode: read-only. No DNS, deploy, merge, production promotion, spend, gateway, publishing, or external-message action taken.

## Summary

- Total surfaces: 27
- Red: 19
- Yellow: 5
- Green: 3
- Meaningful change vs prior run: True

## Top Risks / Changes

- [red] agenticincome.ai - root not healthy - change: no material change detected vs 2026-06-27 radar
- [red] agenticpassiveincome.ai - root not healthy; www not healthy; missing: deploy target - change: no material change detected vs 2026-06-27 radar
- [red] agenticpassiveincome.com - root not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-06-27 radar
- [red] aiarchitectacademy.com - root not healthy; www not healthy - change: no material change detected vs 2026-06-27 radar
- [red] arcanea.ai - latest Vercel deployment UNKNOWN; local dirty count 91 - change: dirty 88 -> 91
- [red] arcanea.com - root not healthy; missing: provider verification; missing: canonical repo; missing: deploy target - change: no material change detected vs 2026-06-27 radar
- [red] arcanea.dev - root not healthy; www not healthy; latest Vercel deployment UNKNOWN; local dirty count 91; missing: provider verification; missing: deploy target - change: dirty 88 -> 91
- [red] arcanea.io - latest Vercel deployment UNKNOWN; local dirty count 91; missing: provider verification - change: dirty 88 -> 91
- [red] arcanealabs.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-06-27 radar
- [red] arcanean.org - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-06-27 radar
- [red] disruptivepassiveincom.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo - change: no material change detected vs 2026-06-27 radar
- [red] disruptivepassiveincome.de - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-06-27 radar

## Radar Table

| Verdict | Brand | Domain | Root/www | Title signal | DNS/provider | Vercel latest | Repo state | Channel | Change | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | Revenue Network | agenticincome.ai | 308 / 200 |  | Vercel DNS/edge signal | READY / Production / 1d | agent/cleanup-sync dirty=49 head=b07a68a | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticincome) |
| red | Revenue Network | agenticpassiveincome.ai | err / err |  | unknown | READY / Production / 5d | agent/cleanup-sync dirty=10 head=be9ab31 | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://agenticpassiveincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | Revenue Network | agenticpassiveincome.com | 308 / 200 |  | Vercel DNS/edge signal | READY / Production / 5d | agent/cleanup-sync dirty=10 head=be9ab31 | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://agenticpassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | AI Architect Academy | aiarchitectacademy.com | err / err |  | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=9 head=529f63d | #brand-ai-coe | no material change detected vs 2026-06-27 radar | [site](https://aiarchitectacademy.com/) / [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| red | Arcanea | arcanea.ai | 200 / 200 | Arcanea™ — Creative Intelligence Platform | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=91 head=eaf954c3 | #brand-arcanea | dirty 88 -> 91 | [site](https://arcanea.ai/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.com | err / 200 |  | unknown | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-06-27 radar | [site](https://arcanea.com/) |
| red | Arcanea | arcanea.dev | 404 / 404 |  | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=91 head=eaf954c3 | #brand-arcanea | dirty 88 -> 91 | [site](https://arcanea.dev/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.io | 200 / 200 |  | IONOS/UI-DNS signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=91 head=eaf954c3 | #brand-arcanea | dirty 88 -> 91 | [site](https://arcanea.io/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanealabs.com | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-06-27 radar | [site](https://arcanealabs.com/) |
| red | Arcanea | arcanean.org | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-06-27 radar | [site](https://arcanean.org/) |
| red | Revenue Network | disruptivepassiveincom.com | err / err |  | unknown | none mapped | no local repo | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://disruptivepassiveincom.com/) |
| red | Revenue Network | disruptivepassiveincome.de | err / err |  | IONOS/UI-DNS signal | none mapped | main dirty=10 head=c5d8132 | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://disruptivepassiveincome.de/) |
| red | FrankX | frank-riemer.com | err / err |  | IONOS/UI-DNS signal | READY / Preview / 5h | agent/codex/rights-foundation dirty=10 head=67f6c3b2 | #brand-frankx | branch main -> agent/codex/rights-foundation; dirty 0 -> 10 | [site](https://frank-riemer.com/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX | frankx.dev | err / err |  | unknown | READY / Preview / 5h | agent/codex/rights-foundation dirty=10 head=67f6c3b2 | #brand-frankx | branch main -> agent/codex/rights-foundation; dirty 0 -> 10 | [site](https://frankx.dev/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX | frankx.io | 404 / err |  | Vercel DNS/edge signal | READY / Preview / 5h | agent/codex/rights-foundation dirty=10 head=67f6c3b2 | #brand-frankx | branch main -> agent/codex/rights-foundation; dirty 0 -> 10 | [site](https://frankx.io/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX / Music | music-academy.ai | err / err |  | unknown | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-06-27 radar | [site](https://music-academy.ai/) |
| red | Reality Architect | realityarchitect.ai | 308 / 200 |  | Vercel DNS/edge signal | READY / Production / 5d | main dirty=5 head=6476312 | #brand-reality-architect | no material change detected vs 2026-06-27 radar | [site](https://realityarchitect.ai/) / [vercel](https://vercel.com/starlight-intelligence/realityarchitect) |
| red | Reality Architect / Arcanea | realitydiffusion.ai | err / err |  | IONOS/UI-DNS signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-06-27 radar | [site](https://realitydiffusion.ai/) |
| red | Starlight Intelligence Systems | starlight-intelligence.ai | err / err |  | unknown | READY / Production / 2d | main dirty=66 head=88073a2 | #brand-starlight | dirty 65 -> 66 | [site](https://starlight-intelligence.ai/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Product / Other | akamoto.io | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light | IONOS/UI-DNS signal | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-06-27 radar | [site](https://akamoto.io/) |
| yellow | Arcanea / AnimeLegends | animelegends.ai | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, a... | Vercel DNS/edge signal | READY / Production / 10d | main dirty=2 head=053d297 | #brand-anime-legends | no material change detected vs 2026-06-27 radar | [site](https://animelegends.ai/) / [vercel](https://vercel.com/starlight-intelligence/anime-legends) |
| yellow | Revenue Network | go.agenticincome.ai | 200 / n/a | Agentic Income Router | Vercel DNS/edge signal | none mapped | main dirty=0 head=a596ef7 | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://go.agenticincome.ai/) |
| yellow | Starlight Intelligence Systems | starlightintelligence.org | 200 / 200 | Starlight Intelligence — Persistent context for AI agents ·... | Vercel DNS/edge signal | READY / Production / 2d | main dirty=66 head=88073a2 | #brand-starlight | dirty 65 -> 66 | [site](https://starlightintelligence.org/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Arcanea / Experience | vibeclubs.ai | 200 / 200 | Vibeclubs — Host a vibeclub | Vercel DNS/edge signal | READY / Preview / 5d | no local repo | #brand-arcanea | no material change detected vs 2026-06-27 radar | [site](https://vibeclubs.ai/) / [vercel](https://vercel.com/starlight-intelligence/vibeclubs-web) |
| green | Revenue Network | disruptivepassiveincome.com | 200 / 200 | Disruptive Passive Income | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=10 head=c5d8132 | #brand-agentic-income | no material change detected vs 2026-06-27 radar | [site](https://disruptivepassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/disruptivepassiveincome) |
| green | FrankX | frankx.ai | 200 / 200 | FrankX - AI Architect & Creator Systems | Vercel DNS/edge signal | READY / Preview / 5h | agent/codex/rights-foundation dirty=10 head=67f6c3b2 | #brand-frankx | branch main -> agent/codex/rights-foundation; dirty 0 -> 10 | [site](https://frankx.ai/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| green | FrankX / GenCreator | gencreator.ai | 200 / 200 | GenCreator — The Operating System for AI-Native Creators | Vercel DNS/edge signal | READY / Production / 14h | main dirty=1 head=dae2890 | #brand-creator-systems | dirty 2 -> 1 | [site](https://gencreator.ai/) / [vercel](https://vercel.com/starlight-intelligence/gencreator-ai) |

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
- go.agenticincome.ai: missing: Vercel project mapping -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
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

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-06-28\domain-deployment-radar-2026-06-28.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-06-28\DOMAIN_DEPLOYMENT_RADAR_2026-06-28.md
