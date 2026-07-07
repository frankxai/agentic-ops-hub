# Domain Deployment Radar - 2026-06-29

Generated: 2026-06-29T08:46:47
Mode: read-only. No deploys, DNS changes, promotions, merges, purchases, gateway starts, or external messages beyond internal Slack proof posts.

## Summary

- Total domains/subdomains: 27
- Green: 0; Yellow: 24; Red: 3
- Changed since prior run: 17; Newly mapped: 0
- Primary changed signal: new `arcanea-ai-app` Vercel deployment is still `BLOCKED` on `backup/claude-snapshots`.
- AI Architect Academy root and www checks failed during this run and still need provider/SSL verification.
- Provider ownership remains evidence-gated where registry confidence is `needs-provider-verification`.

## Red / Decision Bottlenecks

- **arcanea.ai** (Arcanea) - latest mapped Vercel deployment is BLOCKED; change: root 200->307; deployment dpl_42HrgnddRvzFPWkeZgtLzYzTS6Nv->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha d4ee7cb->6ae7467; next: Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboarding pass
- **aiarchitectacademy.com** (AI Architect Academy) - P0 root and www are not healthy; provider/SSL verification required; change: no material change observed since 2026-06-28; next: Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer
- **arcanea.dev** (Arcanea) - latest mapped Vercel deployment is BLOCKED; change: deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467; next: Verify ownership, then redirect or build minimal developer docs shell

## Changed Since Prior Run

- **frankx.ai** - root 200->307
- **arcanea.ai** - root 200->307; deployment dpl_42HrgnddRvzFPWkeZgtLzYzTS6Nv->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha d4ee7cb->6ae7467
- **animelegends.ai** - root 200->307
- **agenticincome.ai** - verdict yellow->red; root 200->308
- **disruptivepassiveincome.com** - www 200->301
- **realityarchitect.ai** - verdict yellow->red; root 200->308
- **arcanea.io** - deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467
- **akamoto.io** - www 200->301
- **arcanea.dev** - deployment ->dpl_B63mPxS1BXBSvn2ySTGj1FnFgX7V; sha 6a4774f->6ae7467
- **arcanea.com** - root ->302; www 200->410
- **arcanean.org** - verdict yellow->red
- **arcanealabs.com** - verdict yellow->red
- **frankx.dev** - deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84
- **frankx.io** - deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84
- **frank-riemer.com** - deployment ->dpl_H6DxSpNvE4sbFYQc5NTRzXHiPesH; sha 2ee3d30->7fbbd84
- **agenticpassiveincome.com** - verdict yellow->red; root 200->308
- **go.agenticincome.ai** - www ->307; branch main->; dirty 0->

## Radar Table

| Verdict | Brand | Domain | Root | WWW | Title / metadata signal | Vercel state | Repo branch / dirty | Channel | Missing proof | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yellow | FrankX | [frankx.ai](https://frankx.ai) | 307 | 200 | none | frankx-ai-vercel-website READY | agent/codex/rights-foundation / dirty 10 | #brand-frankx | none | P0: repair FrankX to GenCreator bridge across nav, footer, content CTAs, and July launch paths |
| yellow | FrankX / GenCreator | [gencreator.ai](https://gencreator.ai) | 200 | 200 | none | gencreator-ai READY | main / dirty 1 | #brand-creator-systems | none | Add clear offer, waitlist, FrankX referral continuity, and checkout/product access readiness ch |
| red | Arcanea | [arcanea.ai](https://arcanea.ai) | 307 | 200 | none | arcanea-ai-app BLOCKED | codex/arcanea-homepage-world-engine / dirty 91 | #brand-arcanea | none | Verify canonical www/non-www, then run premium first-viewport, copy, motion, and creator onboar |
| yellow | Starlight Intelligence Systems | [starlightintelligence.org](https://starlightintelligence.org) | 200 | 200 | none | site READY | main / dirty 66 | #brand-starlight | none | Harden download UX, release manifests, checksums, public/private plugin boundaries, and standar |
| yellow | Arcanea / AnimeLegends | [animelegends.ai](https://animelegends.ai) | 307 | 200 | none | anime-legends READY | main / dirty 2 | #brand-arcanea | none | Run visual intelligence and motion pass; add launch-quality first viewport, OG, and waitlist pa |
| yellow | Arcanea / Experience | [vibeclubs.ai](https://vibeclubs.ai) | 200 | 200 | Vibeclubs — Host a vibeclub | unmapped unknown | not cloned/missing | #brand-arcanea | localPath | Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium commun |
| yellow | Revenue Network | [agenticincome.ai](https://agenticincome.ai) | 308 | 200 | Agentic Income — The AI-tool income desk. | agenticincome READY | agent/cleanup-sync / dirty 49 | #brand-agentic-income | none | P0: fix deployment/DNS/404, then connect go-links and spoke network |
| yellow | Revenue Network | [disruptivepassiveincome.com](https://disruptivepassiveincome.com) | 200 | 301 | none | unmapped unknown | main / dirty 10 | #brand-agentic-income | none | Polish copy, add hub cross-links, verify affiliate disclosures and go-link tracking |
| yellow | Reality Architect | [realityarchitect.ai](https://realityarchitect.ai) | 308 | 200 | Reality Architect — Build the systems that build the life you want. | realityarchitect READY | main / dirty 5 | #brand-reality-architect | none | Fix deploy or redirect; rebuild public method surface with clear vault boundary |
| red | AI Architect Academy | [aiarchitectacademy.com](https://aiarchitectacademy.com) | fail | fail | none | aiarchitectacademy UNKNOWN | main / dirty 9 | #brand-frankx | none | Verify SSL/domain provider, choose canonical repo, and align with enterprise AI CoE offer |
| yellow | Arcanea | [arcanea.io](https://arcanea.io) | 200 | 200 | none | arcanea-ai-app BLOCKED | codex/arcanea-homepage-world-engine / dirty 91 | #brand-arcanea | providerOwnershipVerification | Verify ownership and decide developer portal vs redirect to arcanea.ai |
| yellow | Product / Other | [akamoto.io](https://akamoto.io) | 200 | 301 | none | unmapped unknown | not cloned/missing | #brand-frankx | canonicalRepo, localPath, githubRepo, providerOwnershipVerification | Classify as product, client/other, redirect, or retire from launch scope |
| red | Arcanea | [arcanea.dev](https://arcanea.dev) | 404 | 404 | none | arcanea-ai-app BLOCKED | codex/arcanea-homepage-world-engine / dirty 91 | #brand-arcanea | providerOwnershipVerification | Verify ownership, then redirect or build minimal developer docs shell |
| yellow | Arcanea | [arcanea.com](https://arcanea.com) | 302 | 410 | none | unmapped unknown | not cloned/missing | #brand-arcanea | canonicalRepo, localPath, githubRepo, providerOwnershipVerification | Confirm ownership; if owned, configure SSL and redirect to arcanea.ai |
| yellow | Arcanea | [arcanean.org](https://arcanean.org) | 404 | 404 | none | unmapped unknown | not cloned/missing | #brand-arcanea | localPath, vercelProjectMapping, providerOwnershipVerification | Verify ownership and decide standards portal vs redirect |
| yellow | Arcanea | [arcanealabs.com](https://arcanealabs.com) | 404 | 404 | none | unmapped unknown | not cloned/missing | #brand-arcanea | localPath, vercelProjectMapping, providerOwnershipVerification | Verify ownership and redirect or park intentionally |
| yellow | FrankX | [frankx.dev](https://frankx.dev) | fail | fail | none | frankx-ai-vercel-website READY | agent/codex/rights-foundation / dirty 10 | #brand-frankx | providerOwnershipVerification | Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell |
| yellow | FrankX | [frankx.io](https://frankx.io) | 404 | fail | none | frankx-ai-vercel-website READY | agent/codex/rights-foundation / dirty 10 | #brand-frankx | providerOwnershipVerification | Verify ownership and redirect to frankx.ai or park intentionally |
| yellow | FrankX | [frank-riemer.com](https://frank-riemer.com) | fail | fail | none | frankx-ai-vercel-website READY | agent/codex/rights-foundation / dirty 10 | #brand-frankx | providerOwnershipVerification | Verify ownership and configure SSL redirect to frankx.ai/about |
| yellow | Reality Architect / Arcanea | [realitydiffusion.ai](https://realitydiffusion.ai) | fail | fail | none | unmapped unknown | not cloned/missing | #brand-arcanea | localPath, vercelProjectMapping | Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route |
| yellow | Revenue Network | [agenticpassiveincome.com](https://agenticpassiveincome.com) | 308 | 200 | Agentic Passive Income — Set it once, let it run. | agenticpassiveincome READY | agent/cleanup-sync / dirty 10 | #brand-agentic-income | providerOwnershipVerification | Verify whether .com or .ai is canonical, then deploy or redirect one to the other |
| yellow | Revenue Network | [agenticpassiveincome.ai](https://agenticpassiveincome.ai) | fail | fail | none | agenticpassiveincome READY | agent/cleanup-sync / dirty 10 | #brand-agentic-income | none | Verify ownership and choose .com vs .ai canonical |
| yellow | Revenue Network | [go.agenticincome.ai](https://go.agenticincome.ai) | 200 | 307 | Agentic Income Router | go-agenticincome READY | None / dirty None | #brand-agentic-income | localRepoGitState | Fix 404, verify redirect service, and connect hub/spokes |
| yellow | Revenue Network | [disruptivepassiveincom.com](https://disruptivepassiveincom.com) | fail | fail | none | unmapped unknown | not cloned/missing | #brand-agentic-income | canonicalRepo, localPath, githubRepo, providerOwnershipVerification | Confirm whether typo is owned; if not owned, remove from active launch scope |
| yellow | Revenue Network | [disruptivepassiveincome.de](https://disruptivepassiveincome.de) | fail | fail | none | unmapped unknown | main / dirty 10 | #brand-agentic-income | vercelProjectMapping, providerOwnershipVerification | Verify ownership and redirect to .com until localization exists |
| yellow | FrankX / Music | [music-academy.ai](https://music-academy.ai) | fail | fail | none | unmapped unknown | not cloned/missing | #brand-frankx | localPath, vercelProjectMapping, providerOwnershipVerification | Verify ownership and decide whether to activate in July or backlog |
| yellow | Starlight Intelligence Systems | [starlight-intelligence.ai](https://starlight-intelligence.ai) | fail | fail | none | site READY | main / dirty 66 | #brand-starlight | providerOwnershipVerification | Verify ownership and redirect to starlightintelligence.org or reserve as product alias |

## Missing Registry / Evidence Fields

- **vibeclubs.ai**: localPath. Next: Clone or attach canonical repo, verify deploy, add Stripe/waitlist readiness and premium community positioning
- **arcanea.io**: providerOwnershipVerification. Next: Verify ownership and decide developer portal vs redirect to arcanea.ai
- **akamoto.io**: canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Next: Classify as product, client/other, redirect, or retire from launch scope
- **arcanea.dev**: providerOwnershipVerification. Next: Verify ownership, then redirect or build minimal developer docs shell
- **arcanea.com**: canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Next: Confirm ownership; if owned, configure SSL and redirect to arcanea.ai
- **arcanean.org**: localPath, vercelProjectMapping, providerOwnershipVerification. Next: Verify ownership and decide standards portal vs redirect
- **arcanealabs.com**: localPath, vercelProjectMapping, providerOwnershipVerification. Next: Verify ownership and redirect or park intentionally
- **frankx.dev**: providerOwnershipVerification. Next: Verify ownership/DNS, then redirect to frankx.ai/dev or build docs shell
- **frankx.io**: providerOwnershipVerification. Next: Verify ownership and redirect to frankx.ai or park intentionally
- **frank-riemer.com**: providerOwnershipVerification. Next: Verify ownership and configure SSL redirect to frankx.ai/about
- **realitydiffusion.ai**: localPath, vercelProjectMapping. Next: Verify ownership/DNS and decide Reality Architect vs Arcanea visual engine route
- **agenticpassiveincome.com**: providerOwnershipVerification. Next: Verify whether .com or .ai is canonical, then deploy or redirect one to the other
- **go.agenticincome.ai**: localRepoGitState. Next: Fix 404, verify redirect service, and connect hub/spokes
- **disruptivepassiveincom.com**: canonicalRepo, localPath, githubRepo, providerOwnershipVerification. Next: Confirm whether typo is owned; if not owned, remove from active launch scope
- **disruptivepassiveincome.de**: vercelProjectMapping, providerOwnershipVerification. Next: Verify ownership and redirect to .com until localization exists
- **music-academy.ai**: localPath, vercelProjectMapping, providerOwnershipVerification. Next: Verify ownership and decide whether to activate in July or backlog
- **starlight-intelligence.ai**: providerOwnershipVerification. Next: Verify ownership and redirect to starlightintelligence.org or reserve as product alias

## Artifacts

- JSON: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-06-29.json`
- Markdown: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\DOMAIN_DEPLOYMENT_RADAR_2026-06-29.md`
- SVG: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-06-29.svg`
- PNG: `C:\Users\frank\starlight\repos\agentic-ops-hub\docs\daily-reports\domain-deployment-radar-2026-06-29.png`

## Approval Gates

- Production deploy/promotion: `#repo-command` plus brand/business owner approval.
- DNS/domain changes: explicit human approval required.
- Public claims/publication: source proof plus relevant brand approval; sanitizer before private-to-public movement.
