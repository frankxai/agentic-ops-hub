# 04 — Rapid build SOP

## Goal

Ship a **clickable primary path** fast with genius-feeling UX — without architecture debt that blocks v1.1.

## Preconditions

- [ ] PRODUCT-BRIEF + kill criteria  
- [ ] Persona + GStack gates passed or waived in writing  
- [ ] DESIGN-CONTRACT filled  
- [ ] Channel chosen: `next` | `expo` | `aaas-api`  

## Scaffold

### Web micro-SaaS / AaaS console

```bash
# In products root
npx create-next-app@latest {{name}} --ts --tailwind --eslint --app --src-dir
cd {{name}}
npx shadcn@latest init
npx shadcn@latest add button card input label tabs dialog sheet dropdown-menu sonner separator avatar badge
npm i lucide-react class-variance-authority tailwind-merge clsx zod react-hook-form @hookform/resolvers
```

### Dual-store

```bash
npx create-expo-app@latest {{name}} -t expo-template-blank-typescript
cd {{name}}
npx expo install react-native-safe-area-context react-native-screens
# navigation, lucide-react-native as needed
```

### AaaS API core

```bash
# Prefer existing estate backend patterns (Railway) over new frameworks
# Thin Next route handlers or FastAPI + MCP server exposing tools
```

## Build order (never reverse)

1. **Information architecture** — routes for: marketing (optional), auth, home/job, result, settings, billing stub  
2. **Semantic content** — real copy slots, not lorem  
3. **Primary path components** — one happy path end-to-end  
4. **All states** on that path  
5. **Auth + persistence** minimal  
6. **Agent/tools** if AaaS (allowlist)  
7. **Polish** motion, empty illustrations, Imagine hero on marketing only  
8. **Instrumentation** — one analytics path + error boundary  

## Parallel agent build (recommended)

```text
Terminal A: grok -w feat/core-path "Implement primary JTBD path per DESIGN-CONTRACT.md"
Terminal B: hermes -s app-factory-pipeline,estate-design-excellence "Review IA and copy; no drive-by refactors"
Terminal C (later): claude  → /review or /qa on running URL
```

Hermes orchestrator prompt:

```text
Phase 4 rapid build for {{product}}.
Contract: {{path}}
Stack: {{next|expo}}
Delegate: (1) scaffold checklist (2) core path components (3) state coverage.
Use grok worktrees for code. Stop at demoable primary path.
```

## Definition of “rapid nice UI”

- Typography scale consistent (≤2 font families; licensed)  
- Spacing on 4/8 grid  
- One accent color from brand tokens  
- Cards only when content is a unit — not decoration  
- Sonner/toasts for async confirmation  
- Skeleton loaders on slow paths  
- Mobile nav that doesn’t hide the job  

## Anti-slop blacklist

- Purple gradient AI blobs as identity  
- Bento grids with no hierarchy  
- Fake charts / fake activity feeds  
- Infinite “Loading…” without SSR/data  
- Hover-only critical actions  
- Wall of features before the job  

## Output

- Running dev server URL  
- Primary path demo script (5 bullets)  
- Open questions list ≤5  
- Commit on feature branch  
