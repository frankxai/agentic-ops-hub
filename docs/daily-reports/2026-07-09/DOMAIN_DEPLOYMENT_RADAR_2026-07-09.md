# Domain Deployment Radar - 2026-07-09

Run: 2026-07-09T20:24:09+02:00
Mode: read-only. No DNS, deploy, merge, production promotion, spend, gateway, publishing, or external-message action taken.

## Summary

- Total surfaces: 27
- Red: 20
- Yellow: 3
- Green: 4
- Meaningful change vs prior run: True

## Top Risks / Changes

- [red] agenticincome.ai - latest Vercel deployment ERROR - change: verdict green -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/comparison-sprint
- [red] agenticpassiveincome.ai - root not healthy; www not healthy; latest Vercel deployment ERROR; missing: deploy target - change: latest Vercel  -> ERROR; branch  -> agent/claude/shared-package-migration
- [red] agenticpassiveincome.com - latest Vercel deployment ERROR; missing: deploy target - change: verdict yellow -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/shared-package-migration
- [red] aiarchitectacademy.com - root not healthy; www not healthy - change: branch  -> main
- [red] arcanea.ai - latest Vercel deployment UNKNOWN - change: latest Vercel BLOCKED -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15
- [red] arcanea.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo; missing: deploy target - change: no material change detected vs 2026-07-08 radar
- [red] arcanea.dev - root not healthy; www not healthy; latest Vercel deployment UNKNOWN; missing: provider verification; missing: deploy target - change: root status  -> 404; latest Vercel  -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15
- [red] arcanea.io - latest Vercel deployment UNKNOWN; missing: provider verification - change: verdict yellow -> red; latest Vercel  -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15
- [red] arcanealabs.com - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: root status  -> 404
- [red] arcanean.org - root not healthy; www not healthy; missing: provider verification; missing: deploy target - change: root status  -> 404
- [red] disruptivepassiveincom.com - root not healthy; www not healthy; missing: provider verification; missing: canonical repo - change: no material change detected vs 2026-07-08 radar
- [red] disruptivepassiveincome.com - latest Vercel deployment ERROR - change: verdict green -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/voice-actors-post

## Radar Table

| Verdict | Brand | Domain | Root/www | Title signal | DNS/provider | Vercel latest | Repo state | Channel | Change | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | Revenue Network | agenticincome.ai | 200 / 200 | Agentic Income — The AI-tool income desk. | Vercel DNS/edge signal | ERROR / Preview / 2d | agent/claude/comparison-sprint dirty=1 head=b629df7 | #brand-agentic-income | verdict green -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/comparison-sprint | [site](https://agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticincome) |
| red | Revenue Network | agenticpassiveincome.ai | err / err |  | unknown | ERROR / Preview / 2d | agent/claude/shared-package-migration dirty=1 head=d6282e5 | #brand-agentic-income | latest Vercel  -> ERROR; branch  -> agent/claude/shared-package-migration | [site](https://agenticpassiveincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | Revenue Network | agenticpassiveincome.com | 200 / 200 | Agentic Passive Income — Set it once, let it run. | Vercel DNS/edge signal | ERROR / Preview / 2d | agent/claude/shared-package-migration dirty=1 head=d6282e5 | #brand-agentic-income | verdict yellow -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/shared-package-migration | [site](https://agenticpassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| red | AI Architect Academy | aiarchitectacademy.com | err / err |  | IONOS/UI-DNS signal | mapped, no rows parsed | main dirty=1 head=45ea108 | #brand-ai-coe | branch  -> main | [site](https://aiarchitectacademy.com/) / [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| red | Arcanea | arcanea.ai | 200 / 200 | Arcanea™ — Creative Intelligence Platform | Vercel DNS/edge signal | UNKNOWN / Preview / 2d | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | #brand-arcanea | latest Vercel BLOCKED -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15 | [site](https://arcanea.ai/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.com | err / err |  | unknown | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-08 radar | [site](https://arcanea.com/) |
| red | Arcanea | arcanea.dev | 404 / 404 |  | Vercel DNS/edge signal | UNKNOWN / Preview / 2d | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | #brand-arcanea | root status  -> 404; latest Vercel  -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15 | [site](https://arcanea.dev/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanea.io | 200 / 200 |  | IONOS/UI-DNS signal | UNKNOWN / Preview / 2d | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | #brand-arcanea | verdict yellow -> red; latest Vercel  -> UNKNOWN; branch  -> codex/arcanea-homepage-world-engine; dirty 1 -> 15 | [site](https://arcanea.io/) / [vercel](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| red | Arcanea | arcanealabs.com | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | root status  -> 404 | [site](https://arcanealabs.com/) |
| red | Arcanea | arcanean.org | 404 / 404 |  | Vercel DNS/edge signal | none mapped | no local repo | #brand-arcanea | root status  -> 404 | [site](https://arcanean.org/) |
| red | Revenue Network | disruptivepassiveincom.com | err / err |  | unknown | none mapped | no local repo | #brand-agentic-income | no material change detected vs 2026-07-08 radar | [site](https://disruptivepassiveincom.com/) |
| red | Revenue Network | disruptivepassiveincome.com | 200 / 200 | Disruptive Passive Income | IONOS/UI-DNS signal | ERROR / Preview / 2d | agent/claude/voice-actors-post dirty=1 head=a5f8cb3 | #brand-agentic-income | verdict green -> red; latest Vercel READY -> ERROR; branch  -> agent/claude/voice-actors-post | [site](https://disruptivepassiveincome.com/) / [vercel](https://vercel.com/starlight-intelligence/disruptivepassiveincome) |
| red | Revenue Network | disruptivepassiveincome.de | err / err |  | IONOS/UI-DNS signal | none mapped | agent/claude/voice-actors-post dirty=1 head=a5f8cb3 | #brand-agentic-income | branch  -> agent/claude/voice-actors-post | [site](https://disruptivepassiveincome.de/) |
| red | FrankX | frank-riemer.com | err / err |  | IONOS/UI-DNS signal | none mapped | codex/frankx-v-template-studio dirty=13 head=2ca24a9f | #brand-frankx | branch  -> codex/frankx-v-template-studio; dirty 1 -> 13 | [site](https://frank-riemer.com/) |
| red | FrankX | frankx.dev | err / err |  | unknown | none mapped | codex/frankx-v-template-studio dirty=13 head=2ca24a9f | #brand-frankx | branch  -> codex/frankx-v-template-studio; dirty 1 -> 13 | [site](https://frankx.dev/) |
| red | FrankX | frankx.io | 404 / err |  | Vercel DNS/edge signal | none mapped | codex/frankx-v-template-studio dirty=13 head=2ca24a9f | #brand-frankx | root status  -> 404; branch  -> codex/frankx-v-template-studio; dirty 1 -> 13 | [site](https://frankx.io/) |
| red | Revenue Network | go.agenticincome.ai | 200 / n/a | Agentic Income Router | Vercel DNS/edge signal | ERROR / Preview / 2d | main dirty=1 head=9ef6fa8 | #brand-agentic-income | verdict yellow -> red; latest Vercel READY -> ERROR; branch  -> main | [site](https://go.agenticincome.ai/) / [vercel](https://vercel.com/starlight-intelligence/go-agenticincome) |
| red | FrankX / Music | music-academy.ai | err / err |  | unknown | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-08 radar | [site](https://music-academy.ai/) |
| red | Reality Architect / Arcanea | realitydiffusion.ai | err / err |  | IONOS/UI-DNS signal | none mapped | no local repo | #brand-arcanea | no material change detected vs 2026-07-08 radar | [site](https://realitydiffusion.ai/) |
| red | Starlight Intelligence Systems | starlight-intelligence.ai | err / err |  | unknown | READY / Preview / 2d | codex/main-preserve-20260630 dirty=6 head=46fd844 | #brand-starlight | latest Vercel  -> READY; branch  -> codex/main-preserve-20260630; dirty 1 -> 6 | [site](https://starlight-intelligence.ai/) / [vercel](https://vercel.com/starlight-intelligence/site) |
| yellow | Product / Other | akamoto.io | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light | IONOS/UI-DNS signal | none mapped | no local repo | #brand-frankx | no material change detected vs 2026-07-08 radar | [site](https://akamoto.io/) |
| yellow | Arcanea / AnimeLegends | animelegends.ai | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, a... | Vercel DNS/edge signal | READY / Production / 4d | main dirty=1 head=d44094e | #brand-anime-legends | verdict green -> yellow; branch  -> main | [site](https://animelegends.ai/) / [vercel](https://vercel.com/starlight-intelligence/anime-legends) |
| yellow | Arcanea / Experience | vibeclubs.ai | 200 / 200 | Vibeclubs — Host a vibeclub | Vercel DNS/edge signal | READY / Preview / 4d | no local repo | #brand-arcanea | verdict green -> yellow; dirty 1 ->  | [site](https://vibeclubs.ai/) / [vercel](https://vercel.com/starlight-intelligence/vibeclubs-web) |
| green | FrankX | frankx.ai | 200 / 200 | FrankX - AI Architect & Creator Systems | Vercel DNS/edge signal | READY / Preview / 1h | codex/frankx-v-template-studio dirty=13 head=2ca24a9f | #brand-frankx | branch  -> codex/frankx-v-template-studio; dirty 1 -> 13 | [site](https://frankx.ai/) / [vercel](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| green | FrankX / GenCreator | gencreator.ai | 200 / 200 | GenCreator — The Operating System for AI-Native Creators | Vercel DNS/edge signal | READY / Production / 4d | codex/main-preserve-20260630 dirty=1 head=d1f2da3 | #brand-creator-systems | branch  -> codex/main-preserve-20260630 | [site](https://gencreator.ai/) / [vercel](https://vercel.com/starlight-intelligence/gencreator-ai) |
| green | Reality Architect | realityarchitect.ai | 200 / 200 | Reality Architect — Build the systems that build the life y... | Vercel DNS/edge signal | READY / Preview / 2d | main dirty=1 head=b70f10c | #brand-reality-architect | branch  -> main | [site](https://realityarchitect.ai/) / [vercel](https://vercel.com/starlight-intelligence/realityarchitect) |
| green | Starlight Intelligence Systems | starlightintelligence.org | 200 / 200 | Starlight Intelligence — Persistent context for AI agents ·... | Vercel DNS/edge signal | READY / Preview / 2d | codex/main-preserve-20260630 dirty=6 head=46fd844 | #brand-starlight | verdict yellow -> green; latest Vercel CANCELED -> READY; branch  -> codex/main-preserve-20260630; dirty 1 -> 6 | [site](https://starlightintelligence.org/) / [vercel](https://vercel.com/starlight-intelligence/site) |

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

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-09\domain-deployment-radar-2026-07-09.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-09\DOMAIN_DEPLOYMENT_RADAR_2026-07-09.md
