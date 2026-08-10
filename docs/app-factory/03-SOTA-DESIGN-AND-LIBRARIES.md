# 03 — SOTA design standards, libraries, style

## Goal

Lock a **design contract** and **stack** so build is fast without AI-slop.

Authorities (in order):

1. Target repo `AGENTS.md` / `DESIGN.md` / tokens  
2. Brand pack in `starlight-design-intelligence/brand-packs/`  
3. `estate-design-excellence` skill  
4. `~/.agent-harness` (UI-STACK-RADAR, DESIGN-SOURCE-CATALOG, A11Y, FONT)  
5. Pattern library in this folder  

## Default stacks (2026 estate)

| Product type | Stack | Icons | Motion |
| --- | --- | --- | --- |
| Web micro-SaaS / AaaS console | Next.js 15/16 + React 19 + Tailwind 3/4 + **shadcn/Radix** + CVA | **Lucide** | Motion / CSS; reduced-motion |
| Dual-store app | **Expo + RN + EAS** | Lucide RN or SF-ish set via lucide | Reanimated sparingly |
| Marketing site | Next + content MDX + restrained Motion | Lucide | CSS-first |
| Operator / cockpit | Product DS already in-repo (not generic admin cards) | Lucide | Minimal |

**Never:** second primitive family in a live app; Remix inside Next; whole Magic UI theme dumps.

## Style principles (human-tested SaaS 2026)

1. **Clarity over creativity** for B2B/tools; creativity only when brand register demands (Arcanea).  
2. **Role-based progressive disclosure** — dashboards show ≤5 primary metrics.  
3. **One primary CTA** per view.  
4. **States are product** — empty, loading, error, success, offline, permission denied.  
5. **Chat is not the product** unless the job is conversation; prefer structured workflows + optional agent.  
6. **Micro-interactions** only to confirm cause→effect (save, send, generate).  
7. **Typography does hierarchy** — not cards-in-cards.  
8. **Accessibility is default** — focus, contrast, keyboard, touch ≥44px, reduced-motion.  

## Libraries — approved shortlist

### Always OK (after repo check)

- shadcn/ui (copy component-by-component)  
- Radix primitives  
- lucide-react  
- class-variance-authority + tailwind-merge  
- motion / framer-motion (purposeful only)  
- zod + react-hook-form  
- tanstack-query (client server state)  
- next-auth / clerk / workos (pick one auth story per product)  

### Selective (one component)

- Magic UI, Motion Primitives, Tremor (charts reference), assistant-ui (chat shells), 21st.dev named components  

### Research inspiration (do not copy skins)

- [saasui.design](https://www.saasui.design/) pattern library  
- Linear, Notion, Intercom, Figma product patterns  
- Estate examples: SDI `examples/*-before-after.md`  

## Design contract (required before build)

Fill `templates/DESIGN-CONTRACT.md`:

```text
User + JTBD:
Primary outcome / CTA:
Brand register:
One central design idea:
Tokens/primitives to reuse:
Content + responsive + critical states:
Motion / reduced-motion:
Pattern library IDs (≤5):
Verification viewports + commands:
```

## Three-direction rule (flagship surfaces)

For public marketing or new brand shells only:

1. Generate **exactly 3** visual directions (sketch/HTML or Imagine mood — not 30).  
2. Independent editorial + visual pick.  
3. Implement one.  

Product app chrome: **skip** direction theater; extend existing DS.

## AI imagery policy

| Asset | Tool |
| --- | --- |
| Hero/atmosphere/character | Grok Imagine (Hermes/Grok) + a11y checklist |
| UI chrome, tables, settings | Real components |
| Diagrams with real numbers | Code (HTML/SVG) |
| Logo/wordmark | logo-system + vector masters |

## Skills to load

```text
estate-design-excellence
anti-slop-frontend (SDI)
product-ui-polish / landing-page-polish
world-class-web-release
motion-and-interaction
premium-ui-components / twenty-first-component-bridge
image-generation + image-prompt-crafter (heroes only)
```

## Output

- Design contract  
- Token notes or link to brand pack  
- Pattern IDs from `examples/PATTERN-LIBRARY.md`  
- Component shopping list (named shadcn pieces only)  
