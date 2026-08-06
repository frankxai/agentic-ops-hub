# Font & Typeface Licensing Sources — Estate Policy

**Status:** active machine doctrine  
**Canonical location:** `C:\Users\frank\.agent-harness\FONT-LICENSING-SOURCES.md`  
**Last reviewed:** 2026-08-06  
**Companion:** `UI-COMPONENT-SOURCES.md` (components) · `BRAND-MEDIA-OPERATING-SYSTEM.md` (media) · `DESIGN-EXCELLENCE.md` (loop)

## Purpose

Gate **every typeface** used in production web/app/print/marketing the same way we gate UI components: classify before shipping. A Google Fonts name in a skill, a CDN `@import`, or a “premium SaaS substitute” mapping is **not** a commercial-use authorization.

This closes the independent brand audit gap (2026-08-06): component licensing was mature; **font licensing was absent**.

## Required agent behavior

Before adding or changing a font in any production or shippable surface:

1. Read target repo `AGENTS.md` / `design.md` / `taste.md` and existing token/font stack.
2. Identify the **exact family + files/weights** (not just marketing name).
3. Classify using the table below.
4. Record in the PR/implementation note:
   - family name + weights/styles used
   - canonical license (OFL / SIL / Apache / proprietary EULA URL)
   - source (Google Fonts, foundry, self-host package, system stack)
   - embedding method (self-host woff2, `next/font`, CDN, system-ui stack)
   - commercial/web/app embedding rights summary (one sentence)
   - fallback stack
5. Prefer **self-host** or framework font loaders over anonymous CDNs when the license allows.
6. Never map a proprietary face (Söhne, Circular, Cereal, San Francisco display, etc.) to a free CDN substitute **without labeling it as a substitute** and keeping the proprietary name out of production CSS `font-family` claims.

## Source states

| State | Meaning | Production action |
| --- | --- | --- |
| **approved** | License verified for intended embedding (web/app/desktop) | May ship within recorded terms |
| **research-only** | Useful reference; license or embedding rights unresolved | Do not ship; use system stack or approved OFL face |
| **blocked** | Incompatible EULA, stolen/rehosted files, or brand-forbidden | Do not use or redistribute |
| **unknown** | Cannot name license URL | Stop; resolve before any ship |

## Default approved families (web)

These are commonly safe when loaded from **official** sources and used per their license. Still record weights used.

| Family | Typical license | Preferred load | Notes |
| --- | --- | --- | --- |
| **Inter** | OFL | `next/font/google` or self-host woff2 | Default UI sans for many products |
| **IBM Plex Sans / Mono** | OFL | self-host or official package | Good professional stack |
| **Source Serif / Source Sans / Source Code** | OFL | official | Adobe OFL faces |
| **Geist / Geist Mono** | SIL OFL (Vercel) | official package | Confirm current license file in package |
| **JetBrains Mono** | OFL | official | Code only |
| **system-ui stack** | OS | `system-ui, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif` | Zero font files; preferred when brand allows |

**Google Fonts is not a blank check.** Each family has its own license page; some are OFL, some are not free for all embedding. Check the family page before shipping.

## Explicitly research-only / high-risk until licensed

| Family / class | Why |
| --- | --- |
| **Söhne, Circular, Cereal, Satoshi (commercial cuts), Neue Haas, Akkurat** | Proprietary foundry faces — do not CDN-substitute silently |
| **SF Pro / San Francisco / New York** | Apple system fonts — restricted embedding outside Apple platforms |
| **Any “free download” from random GitHub/zip blogs** | Often illegal redistributions |
| **Fontshare / Indian Type Foundry free tier** | Often free for commercial use **with** conditions — read current EULA per face |
| **Adobe Fonts / monotype subscriptions** | Project must hold active entitlement; web kit rules apply |

## Skill & generation rules

1. **UI UX Pro Max / popular-web-designs / theme-factory** may *suggest* pairings. Suggestions are **research-only** until classified here or in the repo design tokens.
2. When a skill maps a proprietary face → free substitute, the implementation note must say `substitute for research reference X; not claiming X license`.
3. Generation skills (image, deck, canvas) that rasterize type still need a production type path for live UI — bitmaps do not clear web font rights.
4. Arcanea mythic vs FrankX professional registers may use different approved stacks; do not cross-port faces across `REGISTER-BOUNDARIES.md` without a design decision.

## Verification checklist (ship)

- [ ] Family + weights listed
- [ ] License URL or SPDX recorded
- [ ] Embedding method matches license (self-host vs CDN vs system)
- [ ] Fallback stack defined
- [ ] No proprietary name claimed without entitlement
- [ ] `prefers-reduced-motion` and legibility checked at target sizes
- [ ] Repo design tokens updated (not one-off CSS islands)

## MCP / CDN policy

Font CDNs and design MCPs are **discovery channels**, not approval channels.  
Same rule as `UI-COMPONENT-SOURCES.md` MCP policy.

## Related

- Component gate: `UI-COMPONENT-SOURCES.md`
- Design loop: `DESIGN-EXCELLENCE.md`
- Logo construction: Hermes skill `logo-system`
- Independent audit: `%LOCALAPPDATA%\hermes\state\brand-design-audit-20260806.md`
