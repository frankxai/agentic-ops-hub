# Domain Deployment Radar - 2026-07-02

Generated: 2026-07-02T06:43:45.341Z

Mode: read-only. No production promotion, deploy, merge, DNS/domain transfer, spend, publish, Hermes gateway start, or external message was performed.

## Summary
- Total domains checked: 27
- Risk verdicts: 1 green, 10 yellow, 16 red
- Changed since prior run: 12
- Newly mapped: 0

## Changed Since 2026-07-01
- frankx.ai [yellow]: dirty 19->22
- arcanea.ai [red]: dirty 96->98
- starlightintelligence.org [yellow]: dirty 66->67
- realityarchitect.ai [yellow]: dirty 5->6
- arcanea.io [red]: dirty 96->98
- akamoto.io [yellow]: www fail->200
- arcanea.dev [red]: dirty 96->98
- frankx.dev [red]: dirty 19->22
- frankx.io [red]: dirty 19->22
- frank-riemer.com [red]: dirty 19->22
- go.agenticincome.ai [green]: www 200->fail; dirty ->0; local branch ->main
- starlight-intelligence.ai [red]: dirty 66->67

## Red / Decision Required
- arcanea.ai (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboarding pass
- aiarchitectacademy.com (AI Architect Academy): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer
- arcanea.io (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and decide developer portal vs redirect to arcanea.ai
- arcanea.dev (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership, then redirect or build minimal developer docs shell
- arcanea.com (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- arcanean.org (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and decide standards portal vs redirect
- arcanealabs.com (Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and redirect or park intentionally
- frankx.dev (FrankX): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- frankx.io (FrankX): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and redirect to frankx.ai or park intentionally
- frank-riemer.com (FrankX): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and configure SSL redirect to frankx.ai/about
- realitydiffusion.ai (Reality Architect / Arcanea): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- agenticpassiveincome.ai (Revenue Network): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and choose .com vs .ai canonical
- disruptivepassiveincom.com (Revenue Network): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Confirm whether typo is owned; if not owned, remove from active launch scope
- disruptivepassiveincome.de (Revenue Network): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and redirect to .com until localization exists
- music-academy.ai (FrankX / Music): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and decide whether to activate in July or backlog
- starlight-intelligence.ai (Starlight Intelligence Systems): domain unavailable/provider-verification required or latest Vercel deployment blocked. Next: Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Yellow / Proof Gaps
- frankx.ai (FrankX): provider/deploy/dirty-state proof still needs review. Next: P0: repair FrankX to GenCreator bridge across nav, footer, content CTAs, and July launch paths
- gencreator.ai (FrankX / GenCreator): provider/deploy/dirty-state proof still needs review. Next: Add clear offer, waitlist, FrankX referral continuity, and checkout/product access readiness checks
- starlightintelligence.org (Starlight Intelligence Systems): provider/deploy/dirty-state proof still needs review. Next: Harden download UX, release manifests, checksums, public/private plugin boundaries, and standard docs
- animelegends.ai (Arcanea / AnimeLegends): provider/deploy/dirty-state proof still needs review. Next: Run visual intelligence and motion pass; add launch-quality first viewport, OG, and waitlist path
- vibeclubs.ai (Arcanea / Experience): localPath. Next: Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- agenticincome.ai (Revenue Network): provider/deploy/dirty-state proof still needs review. Next: P0: fix deployment/DNS/404, then connect go-links and spoke network
- disruptivepassiveincome.com (Revenue Network): vercelProjectMapping. Next: Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking
- realityarchitect.ai (Reality Architect): provider/deploy/dirty-state proof still needs review. Next: Fix deploy or redirect; rebuild public method surface with clear vault boundary
- akamoto.io (Product / Other): canonicalRepo, localPath, githubRepo, vercelProjectMapping, providerOwnershipVerification. Next: Classify as product, client/other, redirect, or retire from launch scope
- agenticpassiveincome.com (Revenue Network): providerOwnershipVerification. Next: Verify whether .com or .ai is canonical, then deploy or redirect one to the other

## Domain Radar Table
| Brand | Domain | Root | WWW | DNS/provider | Vercel latest | Local repo | Changed | Risk | Channel | Inspect |
|---|---|---:|---:|---|---|---|---|---|---|---|
| FrankX | frankx.ai | 200 | 200 | no public DNS record observed | frankx-ai-vercel-website / READY /  / claude/premium-ops-ruxnO / 6ec0f9e | frankx.ai-vercel-website: agent/codex/rights-foundation, dirty 22 | dirty 19->22 | yellow | #brand-frankx | [root](https://frankx.ai) [www](https://www.frankx.ai) [vercel](https://frankx-ai-vercel-website-1ze37sxwn-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/frankx.ai-vercel-website) |
| FrankX / GenCreator | gencreator.ai | 200 | 200 | no public DNS record observed | gencreator-ai / READY / production / main / dae2890 | gencreator.ai: codex/main-preserve-20260630, dirty 1 | no material change observed since 2026-07-01 | yellow | #brand-frankx | [root](https://gencreator.ai) [www](https://www.gencreator.ai) [vercel](https://gencreator-2f67dhubl-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/gencreator.ai) |
| Arcanea | arcanea.ai | 200 | 200 | no public DNS record observed | arcanea-ai-app / BLOCKED /  / backup/claude-snapshots / 712dd8d | arcanea-ai-app: codex/arcanea-homepage-world-engine, dirty 98 | dirty 96->98 | red | #brand-arcanea | [root](https://arcanea.ai) [www](https://www.arcanea.ai) [vercel](https://arcanea-ai-40or8q0sk-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/arcanea-ai-app) |
| Starlight Intelligence Systems | starlightintelligence.org | 200 | 200 | no public DNS record observed | site / READY / production / phase1/foundations / 63a434f | Starlight-Intelligence-System: codex/main-preserve-20260630, dirty 67 | dirty 66->67 | yellow | #brand-starlight | [root](https://starlightintelligence.org) [www](https://www.starlightintelligence.org) [vercel](https://site-kmww93egw-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/Starlight-Intelligence-System) |
| Arcanea / AnimeLegends | animelegends.ai | 200 | 200 | no public DNS record observed | anime-legends / READY / production / main / 053d297 | AnimeLegends: main, dirty 2 | no material change observed since 2026-07-01 | yellow | #brand-arcanea | [root](https://animelegends.ai) [www](https://www.animelegends.ai) [vercel](https://anime-legends-h44ykveue-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/AnimeLegends) |
| Arcanea / Experience | vibeclubs.ai | 200 | 200 | no public DNS record observed | vibeclubs-web / READY /  / main / 1565f4d | missing local repo | no material change observed since 2026-07-01 | yellow | #brand-arcanea | [root](https://vibeclubs.ai) [www](https://www.vibeclubs.ai) [vercel](https://vibeclubs-nfydq1936-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/vibeclubs) |
| Revenue Network | agenticincome.ai | 200 | 200 | no public DNS record observed | agenticincome / READY / production / agent/cleanup-sync / b07a68a | agenticincome: agent/cleanup-sync, dirty 49 | no material change observed since 2026-07-01 | yellow | #brand-agentic-income | [root](https://agenticincome.ai) [www](https://www.agenticincome.ai) [vercel](https://agenticincome-qlgi3o7tr-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/agenticincome) |
| Revenue Network | disruptivepassiveincome.com | 200 | 200 | no public DNS record observed | unmapped | disruptivepassiveincome: main, dirty 10 | no material change observed since 2026-07-01 | yellow | #brand-agentic-income | [root](https://disruptivepassiveincome.com) [www](https://www.disruptivepassiveincome.com) [github](https://github.com/frankxai/disruptivepassiveincome) |
| Reality Architect | realityarchitect.ai | 200 | 200 | no public DNS record observed | realityarchitect / READY / production / main / 6476312 | realityarchitect: main, dirty 6 | dirty 5->6 | yellow | #brand-reality-architect | [root](https://realityarchitect.ai) [www](https://www.realityarchitect.ai) [vercel](https://realityarchitect-6kayu4pdn-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/realityarchitect) |
| AI Architect Academy | aiarchitectacademy.com | fail | fail | no public DNS record observed | aiarchitectacademy / UNKNOWN /  / unknown /  | ai-architect-academy: main, dirty 9 | no material change observed since 2026-07-01 | red | #brand-ai-coe | [root](https://aiarchitectacademy.com) [www](https://www.aiarchitectacademy.com) [vercel](https://vercel.com/starlight-intelligence/aiarchitectacademy) [github](https://github.com/frankxai/ai-architect-academy) |
| Arcanea | arcanea.io | 200 | 200 | no public DNS record observed | arcanea-ai-app / BLOCKED /  / backup/claude-snapshots / 712dd8d | arcanea-ai-app: codex/arcanea-homepage-world-engine, dirty 98 | dirty 96->98 | red | #brand-arcanea | [root](https://arcanea.io) [www](https://www.arcanea.io) [vercel](https://arcanea-ai-40or8q0sk-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/arcanea-ai-app) |
| Product / Other | akamoto.io | 200 | 200 | no public DNS record observed | unmapped | missing local repo | www fail->200 | yellow | #brand-frankx | [root](https://akamoto.io) [www](https://www.akamoto.io) |
| Arcanea | arcanea.dev | 404 | 404 | no public DNS record observed | arcanea-ai-app / BLOCKED /  / backup/claude-snapshots / 712dd8d | arcanea-ai-app: codex/arcanea-homepage-world-engine, dirty 98 | dirty 96->98 | red | #brand-arcanea | [root](https://arcanea.dev) [www](https://www.arcanea.dev) [vercel](https://arcanea-ai-40or8q0sk-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/arcanea-ai-app) |
| Arcanea | arcanea.com | fail | 200 | no public DNS record observed | arcanea-ai-app / BLOCKED /  / backup/claude-snapshots / 712dd8d | missing local repo | no material change observed since 2026-07-01 | red | #brand-arcanea | [root](https://arcanea.com) [www](https://www.arcanea.com) [vercel](https://arcanea-ai-40or8q0sk-starlight-intelligence.vercel.app) |
| Arcanea | arcanean.org | 404 | 404 | no public DNS record observed | unmapped | missing local repo | no material change observed since 2026-07-01 | red | #brand-arcanea | [root](https://arcanean.org) [www](https://www.arcanean.org) [github](https://github.com/frankxai/arcanean-library) |
| Arcanea | arcanealabs.com | 404 | 404 | no public DNS record observed | unmapped | missing local repo | no material change observed since 2026-07-01 | red | #brand-arcanea | [root](https://arcanealabs.com) [www](https://www.arcanealabs.com) [github](https://github.com/frankxai/Arcanea-Labs) |
| FrankX | frankx.dev | fail | fail | no public DNS record observed | frankx-ai-vercel-website / READY /  / claude/premium-ops-ruxnO / 6ec0f9e | frankx.ai-vercel-website: agent/codex/rights-foundation, dirty 22 | dirty 19->22 | red | #brand-frankx | [root](https://frankx.dev) [www](https://www.frankx.dev) [vercel](https://frankx-ai-vercel-website-1ze37sxwn-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/frankx.ai-vercel-website) |
| FrankX | frankx.io | 404 | fail | no public DNS record observed | frankx-ai-vercel-website / READY /  / claude/premium-ops-ruxnO / 6ec0f9e | frankx.ai-vercel-website: agent/codex/rights-foundation, dirty 22 | dirty 19->22 | red | #brand-frankx | [root](https://frankx.io) [www](https://www.frankx.io) [vercel](https://frankx-ai-vercel-website-1ze37sxwn-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/frankx.ai-vercel-website) |
| FrankX | frank-riemer.com | fail | fail | no public DNS record observed | frankx-ai-vercel-website / READY /  / claude/premium-ops-ruxnO / 6ec0f9e | frankx.ai-vercel-website: agent/codex/rights-foundation, dirty 22 | dirty 19->22 | red | #brand-frankx | [root](https://frank-riemer.com) [www](https://www.frank-riemer.com) [vercel](https://frankx-ai-vercel-website-1ze37sxwn-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/frankx.ai-vercel-website) |
| Reality Architect / Arcanea | realitydiffusion.ai | fail | fail | no public DNS record observed | unmapped | missing local repo | no material change observed since 2026-07-01 | red | #brand-reality-architect | [root](https://realitydiffusion.ai) [www](https://www.realitydiffusion.ai) [github](https://github.com/frankxai/realitydiffusion) |
| Revenue Network | agenticpassiveincome.com | 200 | 200 | no public DNS record observed | agenticpassiveincome / READY / production / main / cd658a4 | agenticpassiveincome: agent/cleanup-sync, dirty 10 | no material change observed since 2026-07-01 | yellow | #brand-agentic-income | [root](https://agenticpassiveincome.com) [www](https://www.agenticpassiveincome.com) [vercel](https://agenticpassiveincome-8tqugohg6-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/agenticpassiveincome) |
| Revenue Network | agenticpassiveincome.ai | fail | fail | no public DNS record observed | agenticpassiveincome / READY / production / main / cd658a4 | agenticpassiveincome: agent/cleanup-sync, dirty 10 | no material change observed since 2026-07-01 | red | #brand-agentic-income | [root](https://agenticpassiveincome.ai) [www](https://www.agenticpassiveincome.ai) [vercel](https://agenticpassiveincome-8tqugohg6-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/agenticpassiveincome) |
| Revenue Network | go.agenticincome.ai | 200 | fail | no public DNS record observed | go-agenticincome / READY / production / main / 94fba60 | go-agenticincome: main, dirty 0 | www 200->fail; dirty ->0; local branch ->main | green | #brand-agentic-income | [root](https://go.agenticincome.ai) [www](https://www.go.agenticincome.ai) [vercel](https://go-agenticincome-bw9b01fkj-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/go-agenticincome) |
| Revenue Network | disruptivepassiveincom.com | fail | fail | no public DNS record observed | unmapped | missing local repo | no material change observed since 2026-07-01 | red | #brand-agentic-income | [root](https://disruptivepassiveincom.com) [www](https://www.disruptivepassiveincom.com) |
| Revenue Network | disruptivepassiveincome.de | fail | fail | no public DNS record observed | unmapped | disruptivepassiveincome: main, dirty 10 | no material change observed since 2026-07-01 | red | #brand-agentic-income | [root](https://disruptivepassiveincome.de) [www](https://www.disruptivepassiveincome.de) [github](https://github.com/frankxai/disruptivepassiveincome) |
| FrankX / Music | music-academy.ai | fail | fail | no public DNS record observed | unmapped | missing local repo | no material change observed since 2026-07-01 | red | #brand-frankx | [root](https://music-academy.ai) [www](https://www.music-academy.ai) [github](https://github.com/frankxai/ai-music-academy) |
| Starlight Intelligence Systems | starlight-intelligence.ai | fail | fail | no public DNS record observed | site / READY / production / phase1/foundations / 63a434f | Starlight-Intelligence-System: codex/main-preserve-20260630, dirty 67 | dirty 66->67 | red | #brand-starlight | [root](https://starlight-intelligence.ai) [www](https://www.starlight-intelligence.ai) [vercel](https://site-kmww93egw-starlight-intelligence.vercel.app) [github](https://github.com/frankxai/Starlight-Intelligence-System) |

## Missing Registry / Mapping Fields
- vibeclubs.ai (Arcanea / Experience): localPath -> Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- disruptivepassiveincome.com (Revenue Network): vercelProjectMapping -> Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking
- arcanea.io (Arcanea): providerOwnershipVerification -> Verify ownership and decide developer portal vs redirect to arcanea.ai
- akamoto.io (Product / Other): canonicalRepo, localPath, githubRepo, vercelProjectMapping, providerOwnershipVerification -> Classify as product, client/other, redirect, or retire from launch scope
- arcanea.dev (Arcanea): providerOwnershipVerification -> Verify ownership, then redirect or build minimal developer docs shell
- arcanea.com (Arcanea): canonicalRepo, localPath, githubRepo, providerOwnershipVerification -> Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- arcanean.org (Arcanea): localPath, vercelProjectMapping, providerOwnershipVerification -> Verify ownership and decide standards portal vs redirect
- arcanealabs.com (Arcanea): localPath, vercelProjectMapping, providerOwnershipVerification -> Verify ownership and redirect or park intentionally
- frankx.dev (FrankX): providerOwnershipVerification -> Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- frankx.io (FrankX): providerOwnershipVerification -> Verify ownership and redirect to frankx.ai or park intentionally
- frank-riemer.com (FrankX): providerOwnershipVerification -> Verify ownership and configure SSL redirect to frankx.ai/about
- realitydiffusion.ai (Reality Architect / Arcanea): localPath, vercelProjectMapping -> Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- agenticpassiveincome.com (Revenue Network): providerOwnershipVerification -> Verify whether .com or .ai is canonical, then deploy or redirect one to the other
- disruptivepassiveincom.com (Revenue Network): canonicalRepo, localPath, githubRepo, vercelProjectMapping, providerOwnershipVerification -> Confirm whether typo is owned; if not owned, remove from active launch scope
- disruptivepassiveincome.de (Revenue Network): vercelProjectMapping, providerOwnershipVerification -> Verify ownership and redirect to .com until localization exists
- music-academy.ai (FrankX / Music): localPath, vercelProjectMapping, providerOwnershipVerification -> Verify ownership and decide whether to activate in July or backlog
- starlight-intelligence.ai (Starlight Intelligence Systems): providerOwnershipVerification -> Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Approval Gate
No DNS/domain/deploy/merge/promotion action without #repo-command plus relevant brand/business owner approval.

## Artifacts
- JSON: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-07-02.json
- Markdown: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\DOMAIN_DEPLOYMENT_RADAR_2026-07-02.md
- Visual board: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-07-02.svg
- PNG board: C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-07-02.png