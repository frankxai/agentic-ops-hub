# Domain Deployment Radar - 2026-07-10

Run at: 2026-07-10T12:12:56+02:00
Mode: read-only. No deploys, DNS changes, merges, domain transfers, spend, public publishing, Hermes gateway starts, or external messages performed.

## Summary
- Surfaces checked: 34 total; 8 green, 0 yellow, 26 red.
- Meaningful change vs prior radar: True.
- Newly mapped: oceanintelligence.app, starlightintelligence.academy, gencreator.community, arcanea.academy, bluelifecommons.org, anaceciliacancino.com, cecilia.chat

## Top Risks
- arcanea.ai: latest Vercel deployment BLOCKED
- agenticincome.ai: latest Vercel deployment ERROR
- disruptivepassiveincome.com: latest Vercel deployment ERROR
- aiarchitectacademy.com: root not healthy, www not healthy, missing: provider verification
- arcanea.io: latest Vercel deployment BLOCKED, missing: provider verification, missing: deploy target / domain attachment proof
- akamoto.io: missing: provider verification, missing: canonical repo, missing: deploy target / domain attachment proof
- arcanea.dev: root not healthy, www not healthy, latest Vercel deployment BLOCKED, missing: provider verification, missing: deploy target / domain attachment proof
- arcanea.com: root not healthy, www not healthy, missing: provider verification, missing: canonical repo, missing: deploy target / domain attachment proof
- arcanean.org: root not healthy, www not healthy, missing: provider verification, missing: deploy target / domain attachment proof
- arcanealabs.com: root not healthy, www not healthy, missing: provider verification, missing: deploy target / domain attachment proof
- frankx.dev: root not healthy, www not healthy, missing: provider verification, missing: deploy target / domain attachment proof
- frankx.io: root not healthy, www not healthy, missing: provider verification, missing: deploy target / domain attachment proof

## Radar
| Verdict | Brand | Domain | Root/www | Title / metadata | DNS/provider | Vercel latest | Local repo | Change | Channel |
|---|---|---|---|---|---|---|---|---|---|
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com/) | fail / fail | none; description missing/unknown | IONOS/UI-DNS signal | no latest parsed | main dirty=1 head=45ea108 | no material change detected vs prior radar | #brand-ai-coe |
| red | Ana Cecilia companion concept | [cecilia.chat](https://cecilia.chat/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | none mapped | none mapped | newly mapped in registry/radar | #brand-frankx |
| red | Arcanea | [arcanea.ai](https://arcanea.ai/) | 200 / 200 | Arcanea™ — Creative Intelligence Platform; description present | Vercel DNS/edge signal | BLOCKED /  / backup/claude-snapshots / 67686629 | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | latest Vercel UNKNOWN -> BLOCKED | #brand-arcanea |
| red | Arcanea | [arcanea.com](https://arcanea.com/) | fail / fail | none; description missing/unknown | unknown | none mapped | none mapped | no material change detected vs prior radar | #brand-arcanea |
| red | Arcanea | [arcanea.dev](https://arcanea.dev/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | BLOCKED /  / backup/claude-snapshots / 67686629 | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | latest Vercel UNKNOWN -> BLOCKED | #brand-arcanea |
| red | Arcanea | [arcanea.io](https://arcanea.io/) | 200 / 200 | none; description missing/unknown | IONOS/UI-DNS signal | BLOCKED /  / backup/claude-snapshots / 67686629 | codex/arcanea-homepage-world-engine dirty=15 head=1570e0b8 | latest Vercel UNKNOWN -> BLOCKED | #brand-arcanea |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | none mapped | none mapped | no material change detected vs prior radar | #brand-arcanea |
| red | Arcanea | [arcanean.org](https://arcanean.org/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | none mapped | none mapped | no material change detected vs prior radar | #brand-arcanea |
| red | Arcanea Academy | [arcanea.academy](https://arcanea.academy/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | READY /  / codex/launch-frontdoor / c6d90da7 | codex/launch-frontdoor dirty=0 head=c6d90da | newly mapped in registry/radar | #brand-arcanea |
| red | Blue Life Commons / Starlight marine lane | [oceanintelligence.app](https://oceanintelligence.app/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | READY /  / codex/launch-frontdoor / db3d21d6 | codex/launch-frontdoor dirty=0 head=db3d21d | newly mapped in registry/radar | #brand-arcanea |
| red | FrankX | [frank-riemer.com](https://frank-riemer.com/) | fail / fail | none; description missing/unknown | IONOS/UI-DNS signal | READY /  / agent/claude/operator-scorecard / 3cd1a367 | codex/frankx-v-template-studio dirty=11 head=2ca24a9f | latest Vercel  -> READY; dirty 13 -> 11 | #brand-frankx |
| red | FrankX | [frankx.dev](https://frankx.dev/) | fail / fail | none; description missing/unknown | unknown | READY /  / agent/claude/operator-scorecard / 3cd1a367 | codex/frankx-v-template-studio dirty=11 head=2ca24a9f | latest Vercel  -> READY; dirty 13 -> 11 | #brand-frankx |
| red | FrankX | [frankx.io](https://frankx.io/) | 404 / fail | none; description missing/unknown | Vercel DNS/edge signal | READY /  / agent/claude/operator-scorecard / 3cd1a367 | codex/frankx-v-template-studio dirty=11 head=2ca24a9f | latest Vercel  -> READY; dirty 13 -> 11 | #brand-frankx |
| red | FrankX / Music | [music-academy.ai](https://music-academy.ai/) | fail / fail | none; description missing/unknown | unknown | none mapped | none mapped | no material change detected vs prior radar | #brand-frankx |
| red | GenCreator Community | [gencreator.community](https://gencreator.community/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | READY /  / codex/launch-frontdoor / 5094099e | codex/launch-frontdoor dirty=0 head=5094099 | newly mapped in registry/radar | #brand-creator-systems |
| red | Product / Other | [akamoto.io](https://akamoto.io/) | 200 / 200 | Akamoto - The forgotten Prophecies of Darkness & Light; description present | IONOS/UI-DNS signal | none mapped | none mapped | verdict yellow -> red | #brand-frankx |
| red | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai/) | fail / fail | none; description missing/unknown | IONOS/UI-DNS signal | none mapped | none mapped | no material change detected vs prior radar | #brand-arcanea |
| red | Revenue Network | [agenticincome.ai](https://agenticincome.ai/) | 200 / 200 | Agentic Income — The AI-tool income desk.; description present | Vercel DNS/edge signal | ERROR /  / agent/claude/comparison-sprint / b629df7f | agent/claude/comparison-sprint dirty=1 head=b629df7 | no material change detected vs prior radar | #brand-agentic-income |
| red | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai/) | fail / fail | none; description missing/unknown | unknown | ERROR /  / agent/claude/shared-package-migration / d6282e50 | agent/claude/shared-package-migration dirty=1 head=d6282e5 | no material change detected vs prior radar | #brand-agentic-income |
| red | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com/) | 200 / 200 | Agentic Passive Income — Set it once, let it run.; description present | Vercel DNS/edge signal | ERROR /  / agent/claude/shared-package-migration / d6282e50 | agent/claude/shared-package-migration dirty=1 head=d6282e5 | no material change detected vs prior radar | #brand-agentic-income |
| red | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com/) | fail / fail | none; description missing/unknown | unknown | none mapped | none mapped | no material change detected vs prior radar | #brand-agentic-income |
| red | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com/) | 200 / 200 | Disruptive Passive Income; description present | IONOS/UI-DNS signal | ERROR /  / agent/claude/voice-actors-post / a5f8cb3d | agent/claude/voice-actors-post dirty=1 head=a5f8cb3 | no material change detected vs prior radar | #brand-agentic-income |
| red | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de/) | fail / fail | none; description missing/unknown | IONOS/UI-DNS signal | ERROR /  / agent/claude/voice-actors-post / a5f8cb3d | agent/claude/voice-actors-post dirty=1 head=a5f8cb3 | latest Vercel  -> ERROR | #brand-agentic-income |
| red | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai/) | 200 / n/a | Agentic Income Router; description present | Vercel DNS/edge signal | ERROR /  / dependabot/npm_and_yarn/typescript-6.0.3 / a1cd1f50 | main dirty=1 head=9ef6fa8 | no material change detected vs prior radar | #brand-agentic-income |
| red | Starlight Intelligence Academy | [starlightintelligence.academy](https://starlightintelligence.academy/) | 404 / 404 | none; description missing/unknown | Vercel DNS/edge signal | READY /  / codex/launch-frontdoor / 787cd329 | codex/launch-frontdoor dirty=0 head=787cd32 | newly mapped in registry/radar | #brand-starlight |
| red | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai/) | fail / fail | none; description missing/unknown | unknown | READY /  / codex/main-preserve-20260630 / 46fd8443 | codex/main-preserve-20260630 dirty=7 head=46fd844 | dirty 6 -> 7 | #brand-starlight |
| green | Ana Cecilia Cancino | [anaceciliacancino.com](https://anaceciliacancino.com/) | 200 / 200 | Ana Cecilia Cancino; description present | Vercel DNS/edge signal | READY / production / main / d5fc6161 | main dirty=0 head=d5fc616 | newly mapped in registry/radar | #brand-frankx |
| green | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai/) | 200 / 200 | AnimeLegends.ai — Where legends are remembered, measured, and born.; description present | Vercel DNS/edge signal | READY / production / main / 0cf5956a | main dirty=1 head=d44094e | verdict yellow -> green | #brand-arcanea |
| green | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai/) | 200 / 200 | Vibeclubs — Host a vibeclub; description present | Vercel DNS/edge signal | READY /  / codex/vibeclubs-runtime-proof / 3346864e | codex/vibeclubs-runtime-proof dirty=0 head=3346864 | verdict yellow -> green; local repo now mapped | #brand-arcanea |
| green | Blue Life Commons | [bluelifecommons.org](https://bluelifecommons.org/) | 200 / 200 | Blue Life Commons — The open intelligence commons for ocean life; description present | Vercel DNS/edge signal | READY / production / main / 089a1748 | main dirty=0 head=089a174 | newly mapped in registry/radar | #brand-arcanea |
| green | FrankX | [frankx.ai](https://frankx.ai/) | 200 / 200 | FrankX - AI Architect & Creator Systems; description present | Vercel DNS/edge signal | READY /  / agent/claude/operator-scorecard / 3cd1a367 | codex/frankx-v-template-studio dirty=11 head=2ca24a9f | dirty 13 -> 11 | #brand-frankx |
| green | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai/) | 200 / 200 | GenCreator — The Operating System for AI-Native Creators; description present | Vercel DNS/edge signal | READY / production / main / fe3b38ec | codex/main-preserve-20260630 dirty=1 head=d1f2da3 | no material change detected vs prior radar | #brand-creator-systems |
| green | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai/) | 200 / 200 | Reality Architect — Build the systems that build the life you want.; description present | Vercel DNS/edge signal | READY /  / agent/claude/ci-bootstrap / 98b8be5d | main dirty=1 head=b70f10c | no material change detected vs prior radar | #brand-reality-architect |
| green | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org/) | 200 / 200 | Starlight Intelligence — Persistent context for AI agents · Built on SIP; description present | Vercel DNS/edge signal | READY /  / codex/main-preserve-20260630 / 46fd8443 | codex/main-preserve-20260630 dirty=7 head=46fd844 | dirty 6 -> 7 | #brand-starlight |

## Missing Registry / Proof Fields
- aiarchitectacademy.com: missing: provider verification -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.io: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- akamoto.io: missing: provider verification, missing: canonical repo, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.dev: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.com: missing: provider verification, missing: canonical repo, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanean.org: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanealabs.com: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.dev: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frankx.io: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- frank-riemer.com: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- realitydiffusion.ai: missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.com: missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- agenticpassiveincome.ai: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincom.com: missing: provider verification, missing: canonical repo, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- disruptivepassiveincome.de: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- music-academy.ai: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- starlight-intelligence.ai: missing: provider verification, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- oceanintelligence.app: missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- starlightintelligence.academy: missing: canonical repo -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- gencreator.community: missing: canonical repo -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- arcanea.academy: missing: canonical repo -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.
- cecilia.chat: missing: canonical repo, missing: deploy target / domain attachment proof -> Verify provider/project owner and update ecosystem/domain-command registry; no automation mutation.

## Approval Gates
- No domain edits without #repo-command approval
- No production deploys without brand/business owner approval
- No merge-to-main from radar automation
- No public claim that a site changed unless Vercel/Git evidence proves it
- No spend, purchase, transfer, DNS change, production promotion, Hermes gateway start, or external message from this automation

## Direct Artifacts
- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-10\domain-deployment-radar-2026-07-10.json
- SVG visual board: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-10\visuals\domain-deployment-radar-2026-07-10.svg
- PNG visual board: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\2026-07-10\visuals\domain-deployment-radar-2026-07-10.png

