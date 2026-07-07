# Domain And Deployment Radar - 2026-06-26

Run time: 2026-06-26T13:34:48+02:00
Mode: read-only. No deploys, DNS/domain changes, merges, production promotions, spending, gateway starts, publishing, or external messaging performed.

## Executive Signal

- Total mapped surfaces checked: 27 (17 red, 9 yellow, 1 green).
- Meaningful change: yes. Arcanea now has latest BLOCKED plus recent ERROR Vercel deployments; FrankX has fresh preview churn; several aliases/backlog domains remain provider-verification gaps.
- Main risk is deployment and ownership mapping drift, not a broad site-down incident.

## Red / Yellow Focus

| Verdict | Brand | Domain | Root | WWW | Vercel latest | Local repo | Channel | Next action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| red | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai/) |  |  | READY / production / main / cd658a4 | agent/cleanup-sync dirty=10 | #brand-agentic-income | root not healthy |
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com/) |  |  | not mapped/unknown | main dirty=9 | #brand-ai-coe | root not healthy |
| red | Arcanea | [arcanea.ai](https://arcanea.ai/) | 200 | 200 | BLOCKED /  / backup/claude-snapshots / 2d1b070 | codex/arcanea-homepage-world-engine dirty=87 | #brand-arcanea | latest Vercel deployment BLOCKED |
| red | Arcanea | [arcanea.com](https://arcanea.com/) |  | 200 | not mapped/unknown | not local/unknown | #brand-arcanea | root not healthy |
| red | Arcanea | [arcanea.dev](https://arcanea.dev/) | 404 | 404 | BLOCKED /  / backup/claude-snapshots / 2d1b070 | codex/arcanea-homepage-world-engine dirty=87 | #brand-arcanea | root not healthy; latest Vercel deployment BLOCKED |
| red | Arcanea | [arcanea.io](https://arcanea.io/) | 200 | 200 | BLOCKED /  / backup/claude-snapshots / 2d1b070 | codex/arcanea-homepage-world-engine dirty=87 | #brand-arcanea | latest Vercel deployment BLOCKED |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com/) | 404 | 404 | not mapped/unknown | not local/unknown | #brand-arcanea | root not healthy |
| red | Arcanea | [arcanean.org](https://arcanean.org/) | 404 | 404 | not mapped/unknown | not local/unknown | #brand-arcanea | root not healthy |
| red | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com/) |  |  | not mapped/unknown | not local/unknown | #brand-agentic-income | root not healthy |
| red | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de/) |  |  | not mapped/unknown | main dirty=10 | #brand-agentic-income | root not healthy |
| red | FrankX | [frank-riemer.com](https://frank-riemer.com/) |  |  | READY /  / claude/premium-ops-ruxnO / 495542d | codex/ahmad-founder-creator-kit dirty=267 | #brand-frankx | root not healthy |
| red | FrankX | [frankx.dev](https://frankx.dev/) |  |  | READY /  / claude/premium-ops-ruxnO / 495542d | codex/ahmad-founder-creator-kit dirty=267 | #brand-frankx | root not healthy |
| red | FrankX | [frankx.io](https://frankx.io/) | 404 |  | READY /  / claude/premium-ops-ruxnO / 495542d | codex/ahmad-founder-creator-kit dirty=267 | #brand-frankx | root not healthy |
| red | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai/) | 404 | n/a | not mapped/unknown | main dirty=24 | #brand-agentic-income | root not healthy |
| red | FrankX / Music | [music-academy.ai](https://music-academy.ai/) |  |  | not mapped/unknown | not local/unknown | #brand-frankx | root not healthy |
| red | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai/) |  |  | not mapped/unknown | not local/unknown | #brand-arcanea | root not healthy |
| red | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai/) |  |  | READY / production /  / unknown | main dirty=65 | #brand-starlight | root not healthy |
| yellow | Revenue Network | [agenticincome.ai](https://agenticincome.ai/) | 200 | 200 | READY /  / agent/cleanup-sync / b07a68a | agent/cleanup-sync dirty=39 | #brand-agentic-income | local dirty count 39 |
| yellow | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com/) | 200 | 200 | READY / production / main / cd658a4 | agent/cleanup-sync dirty=10 | #brand-agentic-income | missing: provider verification |
| yellow | Product / Other | [akamoto.io](https://akamoto.io/) | 200 | 200 | not mapped/unknown | not local/unknown | #brand-frankx | missing: provider verification, canonical repo |
| yellow | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai/) | 200 | 200 | READY / production / main / 053d297 | main dirty=2 | #brand-anime-legends | recent Vercel error/blocked deployments present |
| yellow | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com/) | 200 | 200 | not mapped/unknown | main dirty=10 | #brand-agentic-income | missing: Vercel project mapping |

## Deployment Signals

| Project | Latest state | Target | Branch/ref | Commit | Created | Inspect |
| --- | --- | --- | --- | --- | --- | --- |
| agenticincome | READY |  | agent/cleanup-sync | b07a68a | 2026-06-26 04:39:58 +02:00 | [agenticincome](https://vercel.com/starlight-intelligence/agenticincome) |
| agenticpassiveincome | READY | production | main | cd658a4 | 2026-06-23 04:04:35 +02:00 | [agenticpassiveincome](https://vercel.com/starlight-intelligence/agenticpassiveincome) |
| aiarchitectacademy | unknown | unknown | unknown | unknown | unknown | [aiarchitectacademy](https://vercel.com/starlight-intelligence/aiarchitectacademy) |
| anime-legends | READY | production | main | 053d297 | 2026-06-18 13:54:03 +02:00 | [anime-legends](https://vercel.com/starlight-intelligence/anime-legends) |
| arcanea-ai-app | BLOCKED |  | backup/claude-snapshots | 2d1b070 | 2026-06-26 06:44:35 +02:00 | [arcanea-ai-app](https://vercel.com/starlight-intelligence/arcanea-ai-app) |
| frankx-ai-vercel-website | READY |  | claude/premium-ops-ruxnO | 495542d | 2026-06-26 05:38:56 +02:00 | [frankx-ai-vercel-website](https://vercel.com/starlight-intelligence/frankx-ai-vercel-website) |
| gencreator-ai | READY |  | codex/gencreator-intelligence-os | 1d2fecc | 2026-06-19 03:01:33 +02:00 | [gencreator-ai](https://vercel.com/starlight-intelligence/gencreator-ai) |
| realityarchitect | READY | production | main | 6476312 | 2026-06-23 04:05:21 +02:00 | [realityarchitect](https://vercel.com/starlight-intelligence/realityarchitect) |
| site | READY | production |  | unknown | 2026-06-26 02:42:20 +02:00 | [site](https://vercel.com/starlight-intelligence/site) |
| vibeclubs-web | READY |  | main | 1565f4d | 2026-06-23 17:38:50 +02:00 | [vibeclubs-web](https://vercel.com/starlight-intelligence/vibeclubs-web) |

## Missing Mapping / Provider Verification

- `disruptivepassiveincome.com`: missing: Vercel project mapping. Next: Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- `akamoto.io`: missing: provider verification, canonical repo. Next: Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- `agenticpassiveincome.com`: missing: provider verification. Next: Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.

## Approval Gates

- No domain edits without #repo-command approval
- No production deploys without brand/business owner approval
- No merge-to-main from radar automation
- No public claim that a site changed unless Vercel/Git evidence proves it
- No spend, purchase, transfer, DNS change, production promotion, Hermes gateway start, or external message from this automation

## Direct Artifacts

- JSON: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\night-ops\2026-06-26\domain-deployment-radar-2026-06-26.json`
- Visual: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\night-ops\2026-06-26\visuals\09-domain-deployment-radar.svg`


