# Domain Deployment Radar - 2026-07-04

Generated: 2026-07-04T06:42:34.3015044Z UTC. Mode: read-only. Prior artifact compared: 2026-07-02. Automation last run: 2026-07-03T06:36:48.933Z.

## Summary

- Total domains: 27
- Green / yellow / red: 1 / 10 / 16
- Changed since prior artifact: 17
- Newly observed Vercel deployment surfaces: 4

## Highest Signal

- FrankX has a new READY production deployment on main for the Fable flagship book.
- Arcanea production is READY on main, but the newest deployment event is a BLOCKED backup snapshot, so Arcanea remains red until backup deploy noise is resolved or ignored by policy.
- Starlight has new READY preview deployments, while production remains on the older phase1/foundations deployment.
- Newly observed Vercel projects need classification: blue-life-commons, grok-creative-studio, agentic-intelligence-system, and disruptivepassiveincome.
- Provider ownership verification remains the main registry gap across aliases and backlog domains.

## Domain Radar

| Risk | Brand | Domain | Root | WWW | Vercel | Branch / Dirty | Changed | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yellow | FrankX | [frankx.ai](https://frankx.ai) | 200 | 200 | frankx-ai-vercel-website:READY:main | agent/codex/rights-foundation / 53 | title changed; dirty 22->53; deployment sha changed | P0: repair FrankX to GenCreator bridge across nav, footer, content CTAs, and July launch paths |
| yellow | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai) | 200 | 200 | gencreator-ai:READY:main | codex/main-preserve-20260630 / 1 | no material change observed since 2026-07-02 radar | Add clear offer, waitlist, FrankX referral continuity, and checkout/product access readiness checks |
| red | Arcanea | [arcanea.ai](https://arcanea.ai) | 200 | 200 | arcanea-ai-app:BLOCKED:backup/claude-snapshots | codex/arcanea-homepage-world-engine / 98 | deployment sha changed | Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboarding pass |
| yellow | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org) | 200 | 200 | site:READY:claude/starlight-sis-docs-eclr0l | codex/main-preserve-20260630 / 67 | deployment sha changed | Harden download UX, release manifests, checksums, public/private plugin boundaries, and standard docs |
| yellow | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai) | 200 | 200 | anime-legends:READY:main | main / 2 | no material change observed since 2026-07-02 radar | Run visual intelligence and motion pass; add launch-quality first viewport, OG, and waitlist path |
| yellow | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai) | 200 | 200 | vibeclubs-web:UNKNOWN: | missing | vercel READY->UNKNOWN; deployment sha changed | Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning |
| yellow | Revenue Network | [agenticincome.ai](https://agenticincome.ai) | 200 | 200 | agenticincome:READY:main | codex/production-main-sync / 2 | dirty 49->2; branch agent/cleanup-sync->codex/production-main-sync; deployment sha changed | P0: fix deployment/DNS/404, then connect go-links and spoke network |
| yellow | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com) | 200 | 200 | disruptivepassiveincome:READY:main | main / 2 | dirty 10->2 | Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking |
| yellow | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai) | 200 | 200 | realityarchitect:UNKNOWN: | main / 6 | vercel READY->UNKNOWN; deployment sha changed | Fix deploy or redirect; rebuild public method surface with clear vault boundary |
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com) |  |  | aiarchitectacademy:UNKNOWN: | main / 9 | no material change observed since 2026-07-02 radar | Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer |
| red | Arcanea | [arcanea.io](https://arcanea.io) | 200 | 200 | arcanea-ai-app:BLOCKED:backup/claude-snapshots | codex/arcanea-homepage-world-engine / 98 | deployment sha changed | Verify ownership and decide developer portal vs redirect to arcanea.ai |
| yellow | Product / Other | [akamoto.io](https://akamoto.io) | 200 | 200 | missing |  /  | title changed | Classify as product, client/other, redirect, or retire from launch scope |
| red | Arcanea | [arcanea.dev](https://arcanea.dev) | 404 | 404 | arcanea-ai-app:BLOCKED:backup/claude-snapshots | codex/arcanea-homepage-world-engine / 98 | deployment sha changed | Verify ownership, then redirect or build minimal developer docs shell |
| red | Arcanea | [arcanea.com](https://arcanea.com) |  | 200 | arcanea-ai-app:BLOCKED:backup/claude-snapshots |  /  | no material change observed since 2026-07-02 radar | Confirm ownership; if owned, configure SSL and redirect to arcanea.ai |
| red | Arcanea | [arcanean.org](https://arcanean.org) | 404 | 404 | missing | missing | no material change observed since 2026-07-02 radar | Verify ownership and decide standards portal vs redirect |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com) | 404 | 404 | missing | missing | no material change observed since 2026-07-02 radar | Verify ownership and redirect or park intentionally |
| red | FrankX | [frankx.dev](https://frankx.dev) |  |  | frankx-ai-vercel-website:READY:main | agent/codex/rights-foundation / 53 | dirty 22->53; deployment sha changed | Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell |
| red | FrankX | [frankx.io](https://frankx.io) | 404 |  | frankx-ai-vercel-website:READY:main | agent/codex/rights-foundation / 53 | dirty 22->53; deployment sha changed | Verify ownership and redirect to frankx.ai or park intentionally |
| red | FrankX | [frank-riemer.com](https://frank-riemer.com) |  |  | frankx-ai-vercel-website:READY:main | agent/codex/rights-foundation / 53 | dirty 22->53; deployment sha changed | Verify ownership and configure SSL redirect to frankx.ai/about |
| red | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai) |  |  | missing | missing | no material change observed since 2026-07-02 radar | Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route |
| yellow | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com) | 200 | 200 | agenticpassiveincome:READY:main | codex/production-main-sync / 2 | dirty 10->2; branch agent/cleanup-sync->codex/production-main-sync; deployment sha changed | Verify whether .com or .ai is canonical, then deploy or redirect one to the other |
| red | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai) |  |  | agenticpassiveincome:READY:main | codex/production-main-sync / 2 | dirty 10->2; branch agent/cleanup-sync->codex/production-main-sync; deployment sha changed | Verify ownership and choose .com vs .ai canonical |
| green | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai) | 200 |  | go-agenticincome:READY:main | main / 0 | no material change observed since 2026-07-02 radar | Fix 404, verify redirect service, and connect hub/spokes |
| red | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com) |  |  | missing |  /  | no material change observed since 2026-07-02 radar | Confirm whether typo is owned; if not owned, remove from active launch scope |
| red | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de) |  |  | disruptivepassiveincome:READY:main | main / 2 | dirty 10->2 | Verify ownership and redirect to .com until localization exists |
| red | FrankX / Music | [music-academy.ai](https://music-academy.ai) |  |  | missing | missing | no material change observed since 2026-07-02 radar | Verify ownership and decide whether to activate in July or backlog |
| red | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai) |  |  | site:READY:claude/starlight-sis-docs-eclr0l | codex/main-preserve-20260630 / 67 | deployment sha changed | Verify ownership and redirect to starlightintelligence.org or reserve as product alias |

## Missing Registry Fields

- vibeclubs.ai: missing localPath; next: Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- aiarchitectacademy.com: missing providerOwnershipVerification; next: Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer
- arcanea.io: missing providerOwnershipVerification; next: Verify ownership and decide developer portal vs redirect to arcanea.ai
- akamoto.io: missing canonicalRepo, localPath, githubRepo, vercelProjectMapping, providerOwnershipVerification; next: Classify as product, client/other, redirect, or retire from launch scope
- arcanea.dev: missing providerOwnershipVerification; next: Verify ownership, then redirect or build minimal developer docs shell
- arcanea.com: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification; next: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- arcanean.org: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and decide standards portal vs redirect
- arcanealabs.com: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and redirect or park intentionally
- frankx.dev: missing providerOwnershipVerification; next: Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- frankx.io: missing providerOwnershipVerification; next: Verify ownership and redirect to frankx.ai or park intentionally
- frank-riemer.com: missing providerOwnershipVerification; next: Verify ownership and configure SSL redirect to frankx.ai/about
- realitydiffusion.ai: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- agenticpassiveincome.com: missing providerOwnershipVerification; next: Verify whether .com or .ai is canonical, then deploy or redirect one to the other
- agenticpassiveincome.ai: missing providerOwnershipVerification; next: Verify ownership and choose .com vs .ai canonical
- disruptivepassiveincom.com: missing canonicalRepo, localPath, githubRepo, vercelProjectMapping, providerOwnershipVerification; next: Confirm whether typo is owned; if not owned, remove from active launch scope
- disruptivepassiveincome.de: missing providerOwnershipVerification; next: Verify ownership and redirect to .com until localization exists
- music-academy.ai: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and decide whether to activate in July or backlog
- starlight-intelligence.ai: missing providerOwnershipVerification; next: Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Newly Observed Deployment Surfaces

- blue-life-commons: newly observed in Vercel project list. Next: Classify owner brand, repo, domain, and approval gate before public routing.
- grok-creative-studio: newly observed in Vercel project list. Next: Classify as internal creative tool or public surface before promotion.
- agentic-intelligence-system: newly observed in Vercel project list. Next: Map to Starlight/Tooling repo and decide if public domain is needed.
- disruptivepassiveincome: now present in Vercel project list. Next: Verify production domain binding and affiliate disclosure readiness.

## Approval Gate

No production promotion, deploy, merge, DNS/domain change, spend, public publishing, Hermes gateway start, or external message was performed. Required gate remains #repo-command plus relevant brand/business owner approval before any public/domain/deployment mutation.
