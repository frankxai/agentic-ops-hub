# Domain Deployment Radar - 2026-07-02

Run: 2026-07-02T08:38:31+02:00
Mode: read-only. No DNS, deploy, merge, production promotion, spend, gateway, publishing, or external-message action taken.

## Summary

- Total surfaces: 27
- Red: 16
- Yellow: 7
- Green: 4
- Meaningful change vs prior run: True

## Top Risks / Changes

- [red] agenticpassiveincome.ai - root not healthy; www not healthy; missing: deploy target - change: no material change detected vs 2026-07-01 radar
- [red] aiarchitectacademy.com - root not healthy; www not healthy - change: no material change detected vs 2026-07-01 radar
- [red] arcanea.ai - latest Vercel deployment UNKNOWN; local dirty count 98 - change: dirty 96 -> 98
- [red] arcanea.com - root not healthy; missing: provider verification; missing: canonical repo; missing: deploy target - change: no material change detected vs 2026-07-01 radar
- [red] arcanea.dev - root not healthy; www not healthy; latest Vercel deployment UNKNOWN; local dirty count 98; missing: provider verification; missing: deploy target - change: dirty 96 -> 98
- [red] arcanea.io - latest Vercel deployment UNKNOWN; local dirty count 98; missing: provider verification - change: dirty 96 -> 98
- [red] arcanealabs.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-01 radar
- [red] arcanean.org - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-01 radar
- [red] disruptivepassiveincom.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo - change: no material change detected vs 2026-07-01 radar
- [red] disruptivepassiveincome.de - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-01 radar
- [red] frank-riemer.com - root not healthy; www not healthy; recent Vercel error/blocked/unknown deployments present; missing: provider verification; missing: deploy target - change: dirty 19 -> 22
- [red] frankx.dev - root not healthy; www not healthy; recent Vercel error/blocked/unknown deployments present; missing: provider verification; missing: deploy target - change: dirty 19 -> 22

## Radar Table

| Verdict | Brand | Domain | Root/www | Title signal | DNS/provider | Vercel latest | Repo state | Channel | Change | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | Revenue Network | agenticpassiveincome.ai | err / err |  | unknown | READY / Production / 9d | agent/cleanup-sync dirty=10 head=be9ab31 | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://agenticpassiveincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | AI Architect Academy | aiarchitectacademy.com | err / err |  | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=9 head=529f63d | #brand-ai-coe | no material change detected vs 2026-07-01 radar | [site](https://aiarchitectacademy.com/) / [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| red | Arcanea | arcanea.ai | 200 / 200 | Arcanea™ — Creative Intelligence Platform | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | dirty 96 -> 98 | [site](https://arcanea.ai/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.com | err / 200 |  | unknown | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-01 radar | [site](https://arcanea.com/) |
| red | Arcanea | arcanea.dev | 404 / 404 |  | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | dirty 96 -> 98 | [site](https://arcanea.dev/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.io | 200 / 200 |  | IONOS/UI-DNS signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=98 head=eaf954c3 | #brand-arcanea | dirty 96 -> 98 | [site](https://arcanea.io/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanealabs.com | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-01 radar | [site](https://arcanealabs.com/) |
| red | Arcanea | arcanean.org | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-01 radar | [site](https://arcanean.org/) |
| red | Revenue Network | disruptivepassiveincom.com | err / err |  | unknown | none mapped | no local repo | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://disruptivepassiveincom.com/) |
| red | Revenue Network | disruptivepassiveincome.de | err / err |  | IONOS/UI-DNS signal | none mapped | main dirty=10 head=c5d8132 | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://disruptivepassiveincome.de/) |
| red | FrankX | frank-riemer.com | err / err |  | IONOS/UI-DNS signal | READY / Preview / 1h | agent/codex/rights-foundation dirty=22 head=67f6c3b2 | #brand-frankx | dirty 19 -> 22 | [site](https://frank-riemer.com/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX | frankx.dev | err / err |  | unknown | READY / Preview / 1h | agent/codex/rights-foundation dirty=22 head=67f6c3b2 | #brand-frankx | dirty 19 -> 22 | [site](https://frankx.dev/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX | frankx.io | 404 / err |  | Vercel DNS/edge signal | READY / Preview / 1h | agent/codex/rights-foundation dirty=22 head=67f6c3b2 | #brand-frankx | dirty 19 -> 22 | [site](https://frankx.io/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| red | FrankX / Music | music-academy.ai | err / err |  | unknown | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-01 radar | [site](https://music-academy.ai/) |
| red | Reality Architect / Arcanea | realitydiffusion.ai | err / err |  | IONOS/UI-DNS signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-01 radar | [site](https://realitydiffusion.ai/) |
| red | Starlight Intelligence Systems | starlight-intelligence.ai | err / err |  | unknown | READY / Production / 6d | codex/main-preserve-20260630 dirty=67 head=88073a2 | #brand-starlight | dirty 66 -> 67 | [site](https://starlight-intelligence.ai/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Revenue Network | agenticpassiveincome.com | 200 / 200 |  | Vercel DNS/edge signal | READY / Production / 9d | agent/cleanup-sync dirty=10 head=be9ab31 | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://agenticpassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| yellow | Product / Other | akamoto.io | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light | IONOS/UI-DNS signal | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-01 radar | [site](https://akamoto.io/) |
| yellow | Arcanea / AnimeLegends | animelegends.ai | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, a... | Vercel DNS/edge signal | READY / Production / 14d | main dirty=2 head=053d297 | #brand-anime-legends | no material change detected vs 2026-07-01 radar | [site](https://animelegends.ai/) / [vercel](https://vercel.com/starlight-intelligence/anime-legends) |
| yellow | FrankX | frankx.ai | 200 / 200 | FrankX - AI Architect & Creator Systems | Vercel DNS/edge signal | READY / Preview / 1h | agent/codex/rights-foundation dirty=22 head=67f6c3b2 | #brand-frankx | dirty 19 -> 22 | [site](https://frankx.ai/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| yellow | Revenue Network | go.agenticincome.ai | 200 / n/a | Agentic Income Router | Vercel DNS/edge signal | none mapped | main dirty=0 head=62f7fe7 | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://go.agenticincome.ai/) |
| yellow | Starlight Intelligence Systems | starlightintelligence.org | 200 / 200 | Starlight Intelligence — Persistent context for AI agents ·... | Vercel DNS/edge signal | READY / Production / 6d | codex/main-preserve-20260630 dirty=67 head=88073a2 | #brand-starlight | dirty 66 -> 67 | [site](https://starlightintelligence.org/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Arcanea / Experience | vibeclubs.ai | 200 / 200 | Vibeclubs — Host a vibeclub | Vercel DNS/edge signal | READY / Preview / 9d | no local repo | #brand-arcanea | no material change detected vs 2026-07-01 radar | [site](https://vibeclubs.ai/) / [vercel](https://vercel.com/starlight-intelligence/vibeclubs-web) |
| green | Revenue Network | agenticincome.ai | 200 / 200 |  | Vercel DNS/edge signal | READY / Production / 5d | agent/cleanup-sync dirty=49 head=b07a68a | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticincome) |
| green | Revenue Network | disruptivepassiveincome.com | 200 / 200 | Disruptive Passive Income | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=10 head=c5d8132 | #brand-agentic-income | no material change detected vs 2026-07-01 radar | [site](https://disruptivepassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/disruptivepassiveincome) |
| green | FrankX / GenCreator | gencreator.ai | 200 / 200 | GenCreator — The Operating System for AI-Native Creators | Vercel DNS/edge signal | READY / Production / 5d | codex/main-preserve-20260630 dirty=1 head=dae2890 | #brand-creator-systems | no material change detected vs 2026-07-01 radar | [site](https://gencreator.ai/) / [vercel](https://vercel.com/starlight-intelligence/gencreator-ai) |
| green | Reality Architect | realityarchitect.ai | 200 / 200 |  | Vercel DNS/edge signal | READY / Preview / 3h | main dirty=6 head=6476312 | #brand-reality-architect | dirty 5 -> 6 | [site](https://realityarchitect.ai/) / [vercel](https://vercel.com/starlight-intelligence/realityarchitect) |

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

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-02\domain-deployment-radar-2026-07-02.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-02\DOMAIN_DEPLOYMENT_RADAR_2026-07-02.md

## Connector Validation

- Arcanea latest Vercel deployment: CLI reported UNKNOWN for rcanea-ai-40or8q0sk-starlight-intelligence.vercel.app; Vercel connector _list_deployments resolved deployment dpl_2fdMgtqU9Y48mXw2Jk42uwKseoLS as BLOCKED on ackup/claude-snapshots at e0b450. Treat Arcanea backup/snapshot deployments as the active red decision bottleneck until excluded or fixed.

