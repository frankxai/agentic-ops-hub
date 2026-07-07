# Domain Deployment Radar - 2026-07-06

Run: 2026-07-06T08:37:10+02:00
Mode: read-only. No DNS, deploy, merge, production promotion, spend, gateway, publishing, or external-message action taken.

## Summary

- Total surfaces: 27
- Red: 16
- Yellow: 5
- Green: 6
- Meaningful change vs prior run: True

## Top Risks / Changes

- [red] agenticpassiveincome.ai - root not healthy; www not healthy; missing: deploy target - change: branch codex/production-main-sync -> agent/claude/shared-package-migration; dirty 2 -> 19
- [red] aiarchitectacademy.com - root not healthy; www not healthy - change: latest Vercel UNKNOWN -> 
- [red] arcanea.ai - latest Vercel deployment UNKNOWN - change: latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36
- [red] arcanea.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo; missing: deploy target - change: latest Vercel BLOCKED -> 
- [red] arcanea.dev - root not healthy; www not healthy; latest Vercel deployment UNKNOWN; missing: provider verification; missing: deploy target - change: latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36
- [red] arcanea.io - latest Vercel deployment UNKNOWN; missing: provider verification - change: latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36
- [red] arcanealabs.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-05 radar
- [red] arcanean.org - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: no material change detected vs 2026-07-05 radar
- [red] disruptivepassiveincom.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo - change: no material change detected vs 2026-07-05 radar
- [red] disruptivepassiveincome.de - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: latest Vercel READY -> ; dirty 6 -> 22
- [red] frank-riemer.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: latest Vercel READY -> ; dirty 36 -> 35
- [red] frankx.dev - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: latest Vercel READY -> ; dirty 36 -> 35

## Radar Table

| Verdict | Brand | Domain | Root/www | Title signal | DNS/provider | Vercel latest | Repo state | Channel | Change | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | Revenue Network | agenticpassiveincome.ai | err / err |  | unknown | READY / Production / 16h | agent/claude/shared-package-migration dirty=19 head=9ce0ecf | #brand-agentic-income | branch codex/production-main-sync -> agent/claude/shared-package-migration; dirty 2 -> 19 | [site](https://agenticpassiveincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | AI Architect Academy | aiarchitectacademy.com | err / err |  | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=9 head=529f63d | #brand-ai-coe | latest Vercel UNKNOWN ->  | [site](https://aiarchitectacademy.com/) / [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| red | Arcanea | arcanea.ai | 200 / 200 | Arcanea™ — Creative Intelligence Platform | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=36 head=db357ef0 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36 | [site](https://arcanea.ai/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.com | err / err |  | unknown | none mapped | no local repo | #brand-arcanea | latest Vercel BLOCKED ->  | [site](https://arcanea.com/) |
| red | Arcanea | arcanea.dev | 404 / 404 |  | Vercel DNS/edge signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=36 head=db357ef0 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36 | [site](https://arcanea.dev/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.io | 200 / 200 |  | IONOS/UI-DNS signal | UNKNOWN / Preview / 2h | codex/arcanea-homepage-world-engine dirty=36 head=db357ef0 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN; dirty 59 -> 36 | [site](https://arcanea.io/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanealabs.com | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-05 radar | [site](https://arcanealabs.com/) |
| red | Arcanea | arcanean.org | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-05 radar | [site](https://arcanean.org/) |
| red | Revenue Network | disruptivepassiveincom.com | err / err |  | unknown | none mapped | no local repo | #brand-agentic-income | no material change detected vs 2026-07-05 radar | [site](https://disruptivepassiveincom.com/) |
| red | Revenue Network | disruptivepassiveincome.de | err / err |  | IONOS/UI-DNS signal | none mapped | agent/claude/voice-actors-post dirty=22 head=d035a60 | #brand-agentic-income | latest Vercel READY -> ; dirty 6 -> 22 | [site](https://disruptivepassiveincome.de/) |
| red | FrankX | frank-riemer.com | err / err |  | IONOS/UI-DNS signal | none mapped | codex/frankx-v-template-studio dirty=35 head=a49436e9 | #brand-frankx | latest Vercel READY -> ; dirty 36 -> 35 | [site](https://frank-riemer.com/) |
| red | FrankX | frankx.dev | err / err |  | unknown | none mapped | codex/frankx-v-template-studio dirty=35 head=a49436e9 | #brand-frankx | latest Vercel READY -> ; dirty 36 -> 35 | [site](https://frankx.dev/) |
| red | FrankX | frankx.io | 404 / err |  | Vercel DNS/edge signal | none mapped | codex/frankx-v-template-studio dirty=35 head=a49436e9 | #brand-frankx | latest Vercel READY -> ; dirty 36 -> 35 | [site](https://frankx.io/) |
| red | FrankX / Music | music-academy.ai | err / err |  | unknown | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-05 radar | [site](https://music-academy.ai/) |
| red | Reality Architect / Arcanea | realitydiffusion.ai | err / err |  | IONOS/UI-DNS signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-05 radar | [site](https://realitydiffusion.ai/) |
| red | Starlight Intelligence Systems | starlight-intelligence.ai | err / err |  | unknown | READY / Preview / 7h | codex/main-preserve-20260630 dirty=74 head=f8b1ea5 | #brand-starlight | dirty 72 -> 74 | [site](https://starlight-intelligence.ai/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Revenue Network | agenticpassiveincome.com | 200 / 200 | Agentic Passive Income — Set it once, let it run. | Vercel DNS/edge signal | READY / Production / 16h | agent/claude/shared-package-migration dirty=19 head=9ce0ecf | #brand-agentic-income | branch codex/production-main-sync -> agent/claude/shared-package-migration; dirty 2 -> 19 | [site](https://agenticpassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| yellow | Product / Other | akamoto.io | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light | IONOS/UI-DNS signal | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-05 radar | [site](https://akamoto.io/) |
| yellow | Arcanea / AnimeLegends | animelegends.ai | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, a... | Vercel DNS/edge signal | READY / Production / 15h | main dirty=2 head=053d297 | #brand-anime-legends | no material change detected vs 2026-07-05 radar | [site](https://animelegends.ai/) / [vercel](https://vercel.com/starlight-intelligence/anime-legends) |
| yellow | Starlight Intelligence Systems | starlightintelligence.org | 200 / 200 | Starlight Intelligence — Persistent context for AI agents ·... | Vercel DNS/edge signal | READY / Preview / 7h | codex/main-preserve-20260630 dirty=74 head=f8b1ea5 | #brand-starlight | dirty 72 -> 74 | [site](https://starlightintelligence.org/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Arcanea / Experience | vibeclubs.ai | 200 / 200 | Vibeclubs — Host a vibeclub | Vercel DNS/edge signal | READY / Preview / 14h | no local repo | #brand-arcanea | latest Vercel UNKNOWN -> READY | [site](https://vibeclubs.ai/) / [vercel](https://vercel.com/starlight-intelligence/vibeclubs-web) |
| green | Revenue Network | agenticincome.ai | 200 / 200 | Agentic Income — The AI-tool income desk. | Vercel DNS/edge signal | READY / Production / 21h | agent/claude/comparison-sprint dirty=35 head=c4e4594 | #brand-agentic-income | verdict yellow -> green; dirty 15 -> 35 | [site](https://agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticincome) |
| green | Revenue Network | disruptivepassiveincome.com | 200 / 200 | Disruptive Passive Income | IONOS/UI-DNS signal | READY / Production / 3d | agent/claude/voice-actors-post dirty=22 head=d035a60 | #brand-agentic-income | verdict yellow -> green; dirty 6 -> 22 | [site](https://disruptivepassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/disruptivepassiveincome) |
| green | FrankX | frankx.ai | 200 / 200 | FrankX - AI Architect & Creator Systems | Vercel DNS/edge signal | READY / Preview / 6h | codex/frankx-v-template-studio dirty=35 head=a49436e9 | #brand-frankx | verdict yellow -> green; latest Vercel BUILDING -> READY | [site](https://frankx.ai/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| green | FrankX / GenCreator | gencreator.ai | 200 / 200 | GenCreator — The Operating System for AI-Native Creators | Vercel DNS/edge signal | READY / Production / 18h | codex/main-preserve-20260630 dirty=1 head=dae2890 | #brand-creator-systems | verdict yellow -> green | [site](https://gencreator.ai/) / [vercel](https://vercel.com/starlight-intelligence/gencreator-ai) |
| green | Revenue Network | go.agenticincome.ai | 200 / n/a | Agentic Income Router | Vercel DNS/edge signal | READY / Production / 3d | main dirty=1 head=ddc474a | #brand-agentic-income | verdict yellow -> green; dirty 0 -> 1 | [site](https://go.agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/go-agenticincome) |
| green | Reality Architect | realityarchitect.ai | 200 / 200 | Reality Architect — Build the systems that build the life y... | Vercel DNS/edge signal | READY / Production / 20h | main dirty=4 head=6476312 | #brand-reality-architect | verdict yellow -> green; branch codex/realityarchitect-hero-map -> main | [site](https://realityarchitect.ai/) / [vercel](https://vercel.com/starlight-intelligence/realityarchitect) |

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
- agenticpassiveincome.com: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
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

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-06\domain-deployment-radar-2026-07-06.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-06\DOMAIN_DEPLOYMENT_RADAR_2026-07-06.md

## Connector Verification Addendum

- Vercel team: Starlight Intelligence (	eam_q6LNT6rnFRlqlcjBJ2Wxz6PE); 50 projects observed through connector.
- FrankX: latest rankx-ai-vercel-website event is READY on codex/frankx-v-template-studio; production READY on main also observed after prior run.
- Arcanea: latest rcanea-ai-app event is BLOCKED on ackup/claude-snapshots; multiple same-day codex/arcanea-homepage-world-engine previews are READY; root/www health remains 200, so no production outage is proven.
- Unmapped or classification-needed Vercel projects: g-student-os, lue-life-commons, grok-creative-studio, gentic-intelligence-system, gentmail-template-starkhq, rcanea-ai-appx, rcanea-web, rcanea-2, web.
