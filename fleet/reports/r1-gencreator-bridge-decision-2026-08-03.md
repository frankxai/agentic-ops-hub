# R1 FrankX → GenCreator Bridge Decision — 2026-08-03

**Register:** Professional · Evidence-only · No deploy from dirty tree

## Verdict: **YELLOW**

External product CTAs exist on `origin/main`, but primary chrome still steers many journeys to on-site `/gencreator` hub. Live HTTP is healthy; conversion path is not fully product-domain-primary.

## Evidence
- `origin/main` files containing `https://gencreator.ai`: **51**
- `origin/main` source files mentioning `/gencreator`: **99**
- Live: www.frankx.ai and gencreator.ai returned 200 in prior Packet 1 sweep

### Footer / chrome (origin/main)
```
      { label: 'GenCreator Hub', href: '/gencreator' },
      { label: 'GenCreator.AI', href: 'https://gencreator.ai', external: true, accent: 'emerald' },
```

### Sample external CTA files
- `app/business-plan/page.tsx`
- `components/Footer.tsx`
- `components/home/MindPalaceAtlas.tsx`
- `content/blog/aeo-playbook-get-cited-by-ai-2026.mdx`
- `content/blog/agentic-os-family-foundry-launch.mdx`
- `content/blog/ai-image-video-generation-playbook-2026.mdx`
- `content/blog/ai-model-routing-guide.mdx`
- `content/blog/best-ai-affiliate-programs-2026.mdx`
- `content/blog/best-ai-browser-2026.mdx`
- `content/blog/best-ai-coding-tools-for-beginners-2026.mdx`
- `content/blog/best-ai-headshot-generator-2026.mdx`
- `content/blog/best-ai-logo-maker-2026.mdx`
- `content/blog/best-ai-meeting-assistant-2026.mdx`
- `content/blog/best-ai-note-taking-tools-2026.mdx`
- `content/blog/best-ai-presentation-maker-2026.mdx`
- `content/blog/best-ai-product-photography-2026.mdx`
- `content/blog/best-ai-resume-builder-2026.mdx`
- `content/blog/best-ai-shorts-tiktok-tools-2026.mdx`
- `content/blog/best-ai-superpowers-stack-2026.mdx`
- `content/blog/best-ai-video-editor-2026.mdx`
- `content/blog/best-ai-video-generators-2026-x-aggregated.mdx`
- `content/blog/best-ai-writing-tools-vs-claude-2026.mdx`
- `content/blog/best-cheap-ai-music-generator-2026.mdx`
- `content/blog/best-elevenlabs-alternatives-2026.mdx`
- `content/blog/best-local-llm-2026.mdx`
- `content/blog/best-no-code-ai-agent-builders-2026.mdx`
- `content/blog/chatgpt-vs-claude-vs-gemini-2026.mdx`
- `content/blog/cheapest-frontier-model-access-2026.mdx`
- `content/blog/claude-code-pricing-explained-2026.mdx`
- `content/blog/claude-fable-5-analysis-2026.mdx`

### Sample on-site hub files
- `.claude/agents/meta-handover.md`
- `app/api/cohort/apply/route.ts`
- `app/business-plan/page.tsx`
- `app/consulting/ConsultingClient.tsx`
- `app/gencreator/blueprints/layout.tsx`
- `app/gencreator/blueprints/page.tsx`
- `app/gencreator/handbook/page.tsx`
- `app/gencreator/manifesto/page.tsx`
- `app/gencreator/page.tsx`
- `app/gencreator/principles/page.tsx`
- `app/gencreator/soul/layout.tsx`
- `app/gencreator/soul/page.tsx`
- `app/intelligence-map/page.tsx`
- `app/linktree/linktree-data.ts`
- `app/students/cohort/COHORT-STRATEGY.md`
- `app/students/cohort/CohortClient.tsx`
- `app/work-with-me/StudioClient.tsx`
- `components/Footer.tsx`
- `components/MobileNavOverlay.tsx`
- `components/NavigationMega.tsx`
- `components/gencreator/GenCreatorNav.tsx`
- `components/home/MindPalaceAtlas.tsx`
- `components/intelligence-map/IntelligenceMapShell.tsx`
- `content/blog/aeo-playbook-get-cited-by-ai-2026.mdx`
- `content/blog/agentic-os-family-foundry-launch.mdx`
- `content/blog/ai-image-video-generation-playbook-2026.mdx`
- `content/blog/ai-model-routing-guide.mdx`
- `content/blog/ai-video-generation-2026-sora-runway-kling-veo.mdx`
- `content/blog/arcanea-building-worlds-ai-agents.mdx`
- `content/blog/best-ai-affiliate-programs-2026.mdx`

## Decision
1. **Primary chrome CTA** (nav + homepage): label Open GenCreator → `https://gencreator.ai` with UTM `utm_source=frankx&utm_medium=nav&utm_campaign=r1_bridge`.
2. **Keep** on-site `/gencreator` as education hub, not the only conversion door.
3. **Implement only on clean worktree from origin/main** via PR; never commit into orphaned content-integrity-gate dirty tree.
4. **Book** owns visual polish if layout risk; C940 can land link target + copy honesty.
5. **Acceptance:** homepage+nav show external product CTA; footer remains external; a11y; Vercel preview green; human approve merge.

## Top 3 actions
1. Open clean worktree `r1-primary-cta` from `origin/main` and patch Nav/Hero/CommandPalette targets.
2. Keep analytics consistent with existing patterns — do not invent metrics.
3. Preserve Packet 6 dirty trees untouched while PR lands on clean lane.
