# Domain Deployment Radar - 2026-07-05

Generated: 2026-07-05T06:49:44.580747+00:00 UTC  
Mode: read-only, no deploy/DNS/domain/promotion/merge actions taken.

## Summary

- Total domains: 27
- Green: 0
- Yellow: 11
- Red: 16
- Changed since 2026-07-04 radar: 14
- Newly observed Vercel project needing classification: ag-student-os

## High-Signal Changes

- FrankX: root/www healthy; newest Vercel preview is BUILDING on codex/frankx-v-template-studio, while latest production is READY on main. Local repo moved to that branch/head and dirty count is 35.
- Arcanea: root/www healthy; newest Vercel event remains red because backup/claude-snapshots is BLOCKED. Latest production on main is READY. Local dirty count dropped 98 -> 56.
- Starlight: public domain healthy; newest preview READY, with one earlier preview ERROR since prior run. Local dirty count rose 67 -> 72.
- Reality Architect: new READY preview deployments for codex/realityarchitect-hero-map; no production promotion.
- Vercel estate: ag-student-os is newly observed and unmapped; blue-life-commons, grok-creative-studio, and agentic-intelligence-system remain unmapped.

## Domain Radar

| Risk | Brand | Domain | Root / WWW | Title Signal | Vercel | Local Repo | Changed | Next Action |
|---|---|---|---|---|---|---|---|---|
| yellow | FrankX | [frankx.ai](https://frankx.ai) | 200/200 | FrankX - AI Architect &amp; Creator Systems | frankx-ai-vercel-website BUILDING codex/frankx-v-template-studio | frankx.ai-vercel-website / codex/frankx-v-template-studio / dirty 35 | title changed; dirty 53->35; branch agent/codex/rights-foundation->codex/frankx-v-template-studio; head 67f6c3b2->fefe9593; deployment sha changed; deployment READY->BUILDING | P0: repair FrankX to GenCreator bridge across nav, footer, content CTAs, and July launch paths |
| yellow | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai) | 200/200 | GenCreator — The Operating System for AI-Native Creators | gencreator-ai READY main | gencreator.ai / codex/main-preserve-20260630 / dirty 1 | no material change observed since 2026-07-04 radar | Add clear offer, waitlist, FrankX referral continuity, and checkout/product access readiness checks |
| red | Arcanea | [arcanea.ai](https://arcanea.ai) | 200/200 | Arcanea™ — Creative Intelligence Platform | arcanea-ai-app BLOCKED backup/claude-snapshots | arcanea-ai-app / codex/arcanea-homepage-world-engine / dirty 59 | dirty 98->59; head eaf954c3->97093bf5; deployment sha changed | Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboarding pass |
| yellow | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org) | 200/200 | Starlight Intelligence — Persistent context for AI agents · Built on SIP | site READY claude/starlight-sis-docs-eclr0l | Starlight-Intelligence-System / codex/main-preserve-20260630 / dirty 72 | dirty 67->72; head 88073a2->f8b1ea5; deployment sha changed | Harden download UX, release manifests, checksums, public/private plugin boundaries, and standard docs |
| yellow | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai) | 200/200 | AnimeLegends.ai — Where legends are remembered, measured, and born. | anime-legends READY main | AnimeLegends / main / dirty 2 | no material change observed since 2026-07-04 radar | Run visual intelligence and motion pass; add launch-quality first viewport, OG, and waitlist path |
| yellow | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai) | 200/200 | Vibeclubs — Host a vibeclub | vibeclubs-web UNKNOWN None | missing local mapping | no material change observed since 2026-07-04 radar | Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning |
| yellow | Revenue Network | [agenticincome.ai](https://agenticincome.ai) | 200/200 | Agentic Income — The AI-tool income desk. | agenticincome READY main | agenticincome / agent/claude/comparison-sprint / dirty 15 | dirty 2->15; branch codex/production-main-sync->agent/claude/comparison-sprint | P0: audit affiliate disclosure, checkout/signup tracking, and hub-to-spoke/go-link routes now that HTTPS returns 200 |
| yellow | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com) | 200/200 | Disruptive Passive Income | disruptivepassiveincome READY main | disruptivepassiveincome / agent/claude/voice-actors-post / dirty 6 | dirty 2->6; branch main->agent/claude/voice-actors-post | Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking |
| yellow | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai) | 200/200 | Reality Architect — Build the systems that build the life you want. | realityarchitect READY codex/realityarchitect-hero-map | realityarchitect / codex/realityarchitect-hero-map / dirty 4 | dirty 6->4; branch main->codex/realityarchitect-hero-map; head 6476312->493793d; deployment sha changed; deployment UNKNOWN->READY | Audit public method surface, vault boundary, CTA, signup, and checkout/readiness now that HTTPS returns 200 |
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com) | None/None |  | aiarchitectacademy UNKNOWN None | ai-architect-academy / main / dirty 9 | no material change observed since 2026-07-04 radar | Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer |
| red | Arcanea | [arcanea.io](https://arcanea.io) | 200/200 |  | arcanea-ai-app BLOCKED backup/claude-snapshots | arcanea-ai-app / codex/arcanea-homepage-world-engine / dirty 59 | dirty 98->59; head eaf954c3->97093bf5 | Verify ownership and decide developer portal vs redirect to arcanea.ai |
| yellow | Product / Other | [akamoto.io](https://akamoto.io) | 200/200 | Akamoto - The forgotten Prophecies of Darkness &amp; Light | unmapped | missing local mapping | title changed | Classify as product, client/other, redirect, or retire from launch scope |
| red | Arcanea | [arcanea.dev](https://arcanea.dev) | 404/404 |  | arcanea-ai-app BLOCKED backup/claude-snapshots | arcanea-ai-app / codex/arcanea-homepage-world-engine / dirty 59 | dirty 98->59; head eaf954c3->97093bf5 | Verify ownership, then redirect or build minimal developer docs shell |
| red | Arcanea | [arcanea.com](https://arcanea.com) | None/200 |  | arcanea-ai-app BLOCKED backup/claude-snapshots | missing local mapping | no material change observed since 2026-07-04 radar | Confirm ownership; if owned, configure SSL and redirect to arcanea.ai |
| red | Arcanea | [arcanean.org](https://arcanean.org) | 404/404 |  | unmapped | missing local mapping | no material change observed since 2026-07-04 radar | Verify ownership and decide standards portal vs redirect |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com) | 404/404 |  | unmapped | missing local mapping | no material change observed since 2026-07-04 radar | Verify ownership and redirect or park intentionally |
| red | FrankX | [frankx.dev](https://frankx.dev) | None/None |  | frankx-ai-vercel-website READY main | frankx.ai-vercel-website / codex/frankx-v-template-studio / dirty 36 | dirty 53->36; branch agent/codex/rights-foundation->codex/frankx-v-template-studio; head 67f6c3b2->fefe9593 | Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell |
| red | FrankX | [frankx.io](https://frankx.io) | 404/None |  | frankx-ai-vercel-website READY main | frankx.ai-vercel-website / codex/frankx-v-template-studio / dirty 36 | dirty 53->36; branch agent/codex/rights-foundation->codex/frankx-v-template-studio; head 67f6c3b2->fefe9593 | Verify ownership and redirect to frankx.ai or park intentionally |
| red | FrankX | [frank-riemer.com](https://frank-riemer.com) | None/None |  | frankx-ai-vercel-website READY main | frankx.ai-vercel-website / codex/frankx-v-template-studio / dirty 36 | dirty 53->36; branch agent/codex/rights-foundation->codex/frankx-v-template-studio; head 67f6c3b2->fefe9593 | Verify ownership and configure SSL redirect to frankx.ai/about |
| red | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai) | None/None |  | unmapped | missing local mapping | no material change observed since 2026-07-04 radar | Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route |
| yellow | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com) | 200/200 | Agentic Passive Income — Set it once, let it run. | agenticpassiveincome READY main | agenticpassiveincome / codex/production-main-sync / dirty 2 | no material change observed since 2026-07-04 radar | Decide .com versus .ai canonical route, then add redirect/cross-link, affiliate disclosure, and analytics proof |
| red | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai) | None/None |  | agenticpassiveincome READY main | agenticpassiveincome / codex/production-main-sync / dirty 2 | no material change observed since 2026-07-04 radar | Verify ownership and choose .com vs .ai canonical |
| yellow | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai) | 200/None | Agentic Income Router | go-agenticincome READY main | go-agenticincome / main / dirty 0 | no material change observed since 2026-07-04 radar | Audit redirect routes, affiliate disclosure, campaign tracking, and hub/spoke links now that HTTPS returns 200 |
| red | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com) | None/None |  | unmapped | missing local mapping | no material change observed since 2026-07-04 radar | Confirm whether typo is owned; if not owned, remove from active launch scope |
| red | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de) | None/None |  | disruptivepassiveincome READY main | disruptivepassiveincome / agent/claude/voice-actors-post / dirty 6 | dirty 2->6; branch main->agent/claude/voice-actors-post | Verify ownership and redirect to .com until localization exists |
| red | FrankX / Music | [music-academy.ai](https://music-academy.ai) | None/None |  | unmapped | missing local mapping | no material change observed since 2026-07-04 radar | Verify ownership and decide whether to activate in July or backlog |
| red | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai) | None/None |  | site READY claude/starlight-sis-docs-eclr0l | Starlight-Intelligence-System / codex/main-preserve-20260630 / dirty 72 | dirty 67->72; head 88073a2->f8b1ea5; deployment sha changed | Verify ownership and redirect to starlightintelligence.org or reserve as product alias |

## Missing Registry / Provider Fields

- vibeclubs.ai: missing localPath; next: Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- aiarchitectacademy.com: missing providerOwnershipVerification; next: Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer
- arcanea.io: missing providerOwnershipVerification; next: Verify ownership and decide developer portal vs redirect to arcanea.ai
- akamoto.io: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification; next: Classify as product, client/other, redirect, or retire from launch scope
- arcanea.dev: missing providerOwnershipVerification; next: Verify ownership, then redirect or build minimal developer docs shell
- arcanea.com: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification; next: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- arcanean.org: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and decide standards portal vs redirect
- arcanealabs.com: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and redirect or park intentionally
- frankx.dev: missing providerOwnershipVerification; next: Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- frankx.io: missing providerOwnershipVerification; next: Verify ownership and redirect to frankx.ai or park intentionally
- frank-riemer.com: missing providerOwnershipVerification; next: Verify ownership and configure SSL redirect to frankx.ai/about
- realitydiffusion.ai: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- agenticpassiveincome.ai: missing providerOwnershipVerification; next: Verify ownership and choose .com vs .ai canonical
- disruptivepassiveincom.com: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification; next: Confirm whether typo is owned; if not owned, remove from active launch scope
- disruptivepassiveincome.de: missing providerOwnershipVerification; next: Verify ownership and redirect to .com until localization exists
- music-academy.ai: missing localPath, vercelProjectMapping, providerOwnershipVerification; next: Verify ownership and decide whether to activate in July or backlog
- starlight-intelligence.ai: missing providerOwnershipVerification; next: Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Deployment Surfaces Needing Classification

- ag-student-os: newly observed in Vercel project list. Next: Classify owner brand, repo, domain, and approval gate before public routing.
- blue-life-commons: previously newly observed; still unmapped. Next: Classify owner brand, repo, domain, and approval gate before public routing.
- grok-creative-studio: previously newly observed; still unmapped. Next: Classify as internal creative tool or public surface before promotion.
- agentic-intelligence-system: previously newly observed; still unmapped. Next: Map to Starlight/Tooling repo and decide if public domain is needed.

## Approval Gate

No DNS/domain/deploy/merge/promotion/spend/publish action without #repo-command plus relevant brand/business owner approval. Proof required remains source artifact, repo or Slack record, and rollback/stop path.
