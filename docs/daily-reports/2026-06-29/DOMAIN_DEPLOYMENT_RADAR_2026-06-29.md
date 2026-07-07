# Domain Deployment Radar - 2026-06-29

Generated: 2026-06-29T08:46:47 Europe/Amsterdam
Mode: read-only. No deploy, DNS, domain, merge, promotion, spend, public publish, Hermes gateway, or external message action was taken.

## Summary

- Total surfaces: 27
- Verdicts: 0 green, 19 yellow, 8 red
- Changed since prior run: 17
- Newly mapped: 0
- Main red item: Arcanea Vercel deployment remains BLOCKED, now at dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V / 6ae74672 on backup/claude-snapshots.
- Persistent policy issue: root 308 -> www 200 canonical redirects remain red under current radar policy until Frank changes that scoring rule.

## Changed / Decision Items

- **YELLOW** frankx.ai (FrankX): root 200->307. Next: P0: repair FrankX to GenCreator bridge across nav, footer, content CTAs, and July launch paths
- **RED** arcanea.ai (Arcanea): root 200->307; deployment dpl_42HrgnddRvzFPWkeZgtLzYzTS6Nv->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha d4ee7cb->6ae7467. Next: Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboarding pass
- **YELLOW** animelegends.ai (Arcanea / AnimeLegends): root 200->307. Next: Run visual intelligence and motion pass; add launch-quality first viewport, OG, and waitlist path
- **RED** agenticincome.ai (Revenue Network): verdict yellow->red; root 200->308. Next: P0: fix deployment/DNS/404, then connect go-links and spoke network
- **YELLOW** disruptivepassiveincome.com (Revenue Network): www 200->301. Next: Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking
- **RED** realityarchitect.ai (Reality Architect): verdict yellow->red; root 200->308. Next: Fix deploy or redirect; rebuild public method surface with clear vault boundary
- **RED** arcanea.io (Arcanea): deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467. Next: Verify ownership and decide developer portal vs redirect to arcanea.ai
- **YELLOW** akamoto.io (Product / Other): www 200->301. Next: Classify as product, client/other, redirect, or retire from launch scope
- **RED** arcanea.dev (Arcanea): deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467. Next: Verify ownership, then redirect or build minimal developer docs shell
- **YELLOW** arcanea.com (Arcanea): root ->302; www 200->410. Next: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- **RED** arcanean.org (Arcanea): verdict yellow->red. Next: Verify ownership and decide standards portal vs redirect
- **RED** arcanealabs.com (Arcanea): verdict yellow->red. Next: Verify ownership and redirect or park intentionally

## Radar Table

| Verdict | Brand | Domain | Root | WWW | Vercel | Local repo | Changed | Missing proof |
|---|---|---|---:|---:|---|---|---|---|
| yellow | FrankX | [frankx.ai](https://frankx.ai) | 307 | 200 | READY / claude/ai-architecture-templates-65188c / 7fbbd845 | agent/codex/rights-foundation dirty=10 | root 200->307 | none |
| yellow | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai) | 200 | 200 | READY / main / dae2890c | main dirty=1 | no material change observed since 2026-06-28 | none |
| red | Arcanea | [arcanea.ai](https://arcanea.ai) | 307 | 200 | BLOCKED / backup/claude-snapshots / 6ae74672 | codex/arcanea-homepage-world-engine dirty=91 | root 200->307; deployment dpl_42HrgnddRvzFPWkeZgtLzYzTS6Nv->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha d4ee7cb->6ae7467 | none |
| yellow | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org) | 200 | 200 | READY / phase1/foundations / 63a434f7 | main dirty=66 | no material change observed since 2026-06-28 | none |
| yellow | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai) | 307 | 200 | READY / main / 053d297d | main dirty=2 | root 200->307 | none |
| yellow | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai) | 200 | 200 | unmapped | missing | no material change observed since 2026-06-28 | localPath |
| red | Revenue Network | [agenticincome.ai](https://agenticincome.ai) | 308 | 200 | READY / agent/cleanup-sync / b07a68a6 | agent/cleanup-sync dirty=49 | verdict yellow->red; root 200->308 | none |
| yellow | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com) | 200 | 301 | unmapped | main dirty=10 | www 200->301 | none |
| red | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai) | 308 | 200 | READY / main / 64763120 | main dirty=5 | verdict yellow->red; root 200->308 | none |
| yellow | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com) |  |  | UNKNOWN / unknown / n/a | main dirty=9 | no material change observed since 2026-06-28 | none |
| red | Arcanea | [arcanea.io](https://arcanea.io) | 200 | 200 | BLOCKED / backup/claude-snapshots / 6ae74672 | codex/arcanea-homepage-world-engine dirty=91 | deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467 | providerOwnershipVerification |
| yellow | Product / Other | [akamoto.io](https://akamoto.io) | 200 | 301 | unmapped | missing | www 200->301 | canonicalRepo, localPath, githubRepo, providerOwnershipVerification |
| red | Arcanea | [arcanea.dev](https://arcanea.dev) | 404 | 404 | BLOCKED / backup/claude-snapshots / 6ae74672 | codex/arcanea-homepage-world-engine dirty=91 | deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467 | providerOwnershipVerification |
| yellow | Arcanea | [arcanea.com](https://arcanea.com) | 302 | 410 | unmapped | missing | root ->302; www 200->410 | canonicalRepo, localPath, githubRepo, providerOwnershipVerification |
| red | Arcanea | [arcanean.org](https://arcanean.org) | 404 | 404 | unmapped | missing | verdict yellow->red | localPath, vercelProjectMapping, providerOwnershipVerification |
| red | Arcanea | [arcanealabs.com](https://arcanealabs.com) | 404 | 404 | unmapped | missing | verdict yellow->red | localPath, vercelProjectMapping, providerOwnershipVerification |
| yellow | FrankX | [frankx.dev](https://frankx.dev) |  |  | READY / claude/ai-architecture-templates-65188c / 7fbbd845 | agent/codex/rights-foundation dirty=10 | deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84 | providerOwnershipVerification |
| yellow | FrankX | [frankx.io](https://frankx.io) | 404 |  | READY / claude/ai-architecture-templates-65188c / 7fbbd845 | agent/codex/rights-foundation dirty=10 | deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84 | providerOwnershipVerification |
| yellow | FrankX | [frank-riemer.com](https://frank-riemer.com) |  |  | READY / claude/ai-architecture-templates-65188c / 7fbbd845 | agent/codex/rights-foundation dirty=10 | deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84 | providerOwnershipVerification |
| yellow | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai) |  |  | unmapped | missing | no material change observed since 2026-06-28 | localPath, vercelProjectMapping |
| red | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com) | 308 | 200 | READY / main / cd658a4f | agent/cleanup-sync dirty=10 | verdict yellow->red; root 200->308 | providerOwnershipVerification |
| yellow | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai) |  |  | READY / main / cd658a4f | agent/cleanup-sync dirty=10 | no material change observed since 2026-06-28 | none |
| yellow | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai) | 200 | 307 | READY / main / 94fba60e |  dirty= | www ->307; branch main->; dirty 0-> | localRepoGitState |
| yellow | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com) |  |  | unmapped | missing | no material change observed since 2026-06-28 | canonicalRepo, localPath, githubRepo, providerOwnershipVerification |
| yellow | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de) |  |  | unmapped | main dirty=10 | no material change observed since 2026-06-28 | vercelProjectMapping, providerOwnershipVerification |
| yellow | FrankX / Music | [music-academy.ai](https://music-academy.ai) |  |  | unmapped | missing | no material change observed since 2026-06-28 | localPath, vercelProjectMapping, providerOwnershipVerification |
| yellow | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai) |  |  | READY / phase1/foundations / 63a434f7 | main dirty=66 | no material change observed since 2026-06-28 | providerOwnershipVerification |

## Missing Registry / Mapping Fields

- vibeclubs.ai: missing localPath. Recommended next action: Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- arcanea.io: missing providerOwnershipVerification. Recommended next action: Verify ownership and decide developer portal vs redirect to arcanea.ai
- akamoto.io: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Recommended next action: Classify as product, client/other, redirect, or retire from launch scope
- arcanea.dev: missing providerOwnershipVerification. Recommended next action: Verify ownership, then redirect or build minimal developer docs shell
- arcanea.com: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Recommended next action: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- arcanean.org: missing localPath, vercelProjectMapping, providerOwnershipVerification. Recommended next action: Verify ownership and decide standards portal vs redirect
- arcanealabs.com: missing localPath, vercelProjectMapping, providerOwnershipVerification. Recommended next action: Verify ownership and redirect or park intentionally
- frankx.dev: missing providerOwnershipVerification. Recommended next action: Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- frankx.io: missing providerOwnershipVerification. Recommended next action: Verify ownership and redirect to frankx.ai or park intentionally
- frank-riemer.com: missing providerOwnershipVerification. Recommended next action: Verify ownership and configure SSL redirect to frankx.ai/about
- realitydiffusion.ai: missing localPath, vercelProjectMapping. Recommended next action: Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- agenticpassiveincome.com: missing providerOwnershipVerification. Recommended next action: Verify whether .com or .ai is canonical, then deploy or redirect one to the other
- go.agenticincome.ai: missing localRepoGitState. Recommended next action: Fix 404, verify redirect service, and connect hub/spokes
- disruptivepassiveincom.com: missing canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Recommended next action: Confirm whether typo is owned; if not owned, remove from active launch scope
- disruptivepassiveincome.de: missing vercelProjectMapping, providerOwnershipVerification. Recommended next action: Verify ownership and redirect to .com until localization exists
- music-academy.ai: missing localPath, vercelProjectMapping, providerOwnershipVerification. Recommended next action: Verify ownership and decide whether to activate in July or backlog
- starlight-intelligence.ai: missing providerOwnershipVerification. Recommended next action: Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Approval Gate

No DNS/domain/deploy/merge/promotion action without #repo-command plus relevant brand/business owner approval. Required public/production proof remains: human approval, source/proof artifact, repo or Slack record, rollback/stop path.
