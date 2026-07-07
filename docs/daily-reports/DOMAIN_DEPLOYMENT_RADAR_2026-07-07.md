# Domain Deployment Radar - 2026-07-07

Run: 2026-07-07T08:44:21+02:00  
Mode: read-only. No DNS, deployment, merge, spend, promotion, or external messaging actions performed.

## Summary

- Domains checked: 27
- Verdicts: 7 green / 5 yellow / 15 red
- Meaningful change: yes
- Main changed signals: FrankX production READY changed, Arcanea backup remains BLOCKED with a same-branch ERROR, Starlight latest preview CANCELED while production READY, and author-os is newly active/unmapped.

## Top Risks

- arcanea.ai: latest Vercel BLOCKED on backup/claude-snapshots
- aiarchitectacademy.com: root not healthy, www not healthy
- arcanea.dev: root not healthy, www not healthy, missing: deploy target
- arcanea.com: root not healthy, www not healthy, missing: provider verification
- arcanean.org: root not healthy, www not healthy, missing: deploy target
- arcanealabs.com: root not healthy, www not healthy, missing: deploy target
- frankx.dev: root not healthy, www not healthy, missing: provider verification
- frankx.io: root not healthy, www not healthy, missing: deploy target
- frank-riemer.com: root not healthy, www not healthy, missing: deploy target
- realitydiffusion.ai: root not healthy, www not healthy, missing: deploy target

## Radar Table

| Verdict | Brand | Domain | Health | Vercel latest | Repo state | Changed since prior | Owner / Channel |
| --- | --- | --- | --- | --- | --- | --- | --- |
| green | FrankX | [frankx.ai](https://frankx.ai/) | root 200; www 200; description present | frankx-ai-vercel-website READY production main 273d53fe |  dirty=1 head= | dirty 35 -> 1; latest sha a49436e9 -> 273d53fe | frankx / #brand-frankx |
| green | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai/) | root 200; www 200; description present | gencreator-ai READY production main fe3b38ec |  dirty=1 head= | latest Vercel  -> READY | gencreator / #brand-creator-systems |
| red | Arcanea | [arcanea.ai](https://arcanea.ai/) | root 200; www 200; description present | arcanea-ai-app BLOCKED preview backup/claude-snapshots 66c84acd |  dirty=1 head= | dirty 36 -> 1; latest sha 6e0a799f -> 66c84acd | arcanea / #brand-arcanea |
| yellow | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org/) | root 200; www 200; description present | site CANCELED preview dependabot/github_actions/gha-actions-15235898a0 19a1a795 |  dirty=1 head= | dirty 74 -> 1; latest Vercel  -> CANCELED | starlight / #brand-starlight |
| green | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai/) | root 200; www 200; description present | anime-legends READY production main 0cf5956a |  dirty=1 head= | verdict yellow -> green; dirty 2 -> 1; latest Vercel  -> READY | arcanea / #brand-arcanea |
| green | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai/) | root 200; www 200; description present | vibeclubs-web READY preview codex/vibeclubs-runtime-proof 3346864e |  dirty=1 head= | verdict yellow -> green; latest Vercel  -> READY | arcanea / #brand-arcanea |
| green | Revenue Network | [agenticincome.ai](https://agenticincome.ai/) | root 200; www 200; description present | agenticincome READY production main 2c3a9a2a |  dirty=1 head= | dirty 35 -> 1; latest Vercel  -> READY | income / #brand-agentic-income |
| green | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com/) | root 200; www 200; description present | disruptivepassiveincome READY production main d035a60e |  dirty=1 head= | dirty 22 -> 1; latest Vercel  -> READY | income / #brand-agentic-income |
| green | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai/) | root 200; www 200; description present | realityarchitect READY production main 89f7b552 |  dirty=1 head= | dirty 4 -> 1; latest Vercel  -> READY | reality / #brand-reality-architect |
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com/) | root ; www ; description missing/unknown | aiarchitectacademy    n/a |  dirty=1 head= | dirty 9 -> 1 | aicoe / #brand-ai-coe |
| yellow | Arcanea | [arcanea.io](https://arcanea.io/) | root 200; www 200; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | verdict red -> yellow; dirty 36 -> 1; latest Vercel BLOCKED ->  | arcanea / #brand-arcanea |
| yellow | Product / Other | [akamoto.io](https://akamoto.io/) | root 200; www 200; description present | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | frankx / #brand-frankx |
| red | Arcanea | [arcanea.dev](https://arcanea.dev/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 36 -> 1; latest Vercel BLOCKED ->  | arcanea / #brand-arcanea |
| red | Arcanea | [arcanea.com](https://arcanea.com/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | arcanea / #brand-arcanea |
| red | Arcanea | [arcanean.org](https://arcanean.org/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | arcanea / #brand-arcanea |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | arcanea / #brand-arcanea |
| red | FrankX | [frankx.dev](https://frankx.dev/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 35 -> 1 | frankx / #brand-frankx |
| red | FrankX | [frankx.io](https://frankx.io/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 35 -> 1 | frankx / #brand-frankx |
| red | FrankX | [frank-riemer.com](https://frank-riemer.com/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 35 -> 1 | frankx / #brand-frankx |
| red | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | arcanea / #brand-arcanea |
| yellow | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com/) | root 200; www 200; description present | agenticpassiveincome READY production main 9ce0ecf8 |  dirty=1 head= | dirty 19 -> 1; latest Vercel  -> READY | income / #brand-agentic-income |
| red | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 19 -> 1 | income / #brand-agentic-income |
| yellow | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai/) | root 200; www ; description present | go-agenticincome READY production main ddc474a3 |  dirty=1 head= | verdict green -> yellow; latest Vercel  -> READY | income / #brand-agentic-income |
| red | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | income / #brand-agentic-income |
| red | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 22 -> 1 | income / #brand-agentic-income |
| red | FrankX / Music | [music-academy.ai](https://music-academy.ai/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence | no local git path | no material change detected vs 2026-07-06 radar | frankx / #brand-frankx |
| red | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai/) | root ; www ; description missing/unknown | unmapped/no Vercel evidence |  dirty=1 head= | dirty 74 -> 1 | starlight / #brand-starlight |

## Unmapped / Decision Surfaces

- author-os: new active Vercel project with 19 deployments since July 6; no domain mapping in registry. Latest: READY preview.
- arcanea-ai-appx: parallel Arcanea project repeatedly BLOCKED/ERROR; not canonical. Latest: BLOCKED backup.
- web: unmapped generic project with repeated production ERROR deployments. Latest: ERROR production.
- aiarchitectacademy: project exists but connector returned zero deployments. Latest: none.

## Missing Registry Fields

- arcanea.io: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- akamoto.io: missing: canonical repo, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.dev: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.com: missing: provider verification, missing: canonical repo, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanean.org: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanealabs.com: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.dev: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.io: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frank-riemer.com: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- realitydiffusion.ai: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.com: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.ai: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincom.com: missing: provider verification, missing: canonical repo -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincome.de: missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- music-academy.ai: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- starlight-intelligence.ai: missing: provider verification, missing: deploy target -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.

## Approval Gate

- No domain edits without #repo-command approval
- No production deploys without brand/business owner approval
- No merge-to-main from radar automation
- No public claim that a site changed unless Vercel/Git evidence proves it
- No spend, purchase, transfer, DNS change, production promotion, Hermes gateway start, or external message from this automation

## Artifacts

- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-07-07.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\DOMAIN_DEPLOYMENT_RADAR_2026-07-07.md
