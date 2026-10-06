---
version: alpha
name: Starlight operator
description: Proposed token system for Starlight, the intelligence substrate. Instrument-panel calm, provenance as a visual property, no neon. Draft 2026-10-06 for review.
colors:
  void: "#07090a"
  void-raised: "#0d1113"
  surface: "#111719"
  surface-raised: "#182024"
  line: "rgba(218, 233, 235, 0.14)"
  line-strong: "rgba(218, 233, 235, 0.28)"
  text: "#e8efef"
  text-muted: "#91a1a4"
  text-faint: "#6f7f82"
  signal-live: "#7bdde2"
  signal-live-deep: "#163d41"
  signal-attention: "#e2a15c"
  signal-attention-deep: "#4b2f18"
  state-ok: "#91d1af"
  state-danger: "#e38d7c"
  seam-from: "#c5a26f"
  seam-to: "#e8d5a3"
  frontier: "#a78bfa"
  light-bg: "#eef3f3"
  light-text: "#0e1416"
  light-muted: "#4a5a5e"
  light-live: "#0f6f76"
  light-attention: "#9a5a14"
  light-ok: "#2f6a45"
  light-danger: "#a8402f"
typography:
  horizon-display: { fontFamily: Newsreader, fontSize: clamp(2.75rem, 6vw, 4.5rem), fontWeight: 400, lineHeight: 1.05, letterSpacing: -0.015em }
  h1: { fontFamily: Inter, fontSize: 2.4375rem, fontWeight: 600, lineHeight: 1.15, letterSpacing: -0.02em }
  h2: { fontFamily: Inter, fontSize: 1.9375rem, fontWeight: 600, lineHeight: 1.2, letterSpacing: -0.015em }
  h3: { fontFamily: Inter, fontSize: 1.5625rem, fontWeight: 600, lineHeight: 1.25, letterSpacing: -0.01em }
  title: { fontFamily: Inter, fontSize: 1.25rem, fontWeight: 600, lineHeight: 1.3, letterSpacing: -0.005em }
  body: { fontFamily: Inter, fontSize: 1rem, fontWeight: 400, lineHeight: 1.6, letterSpacing: 0 }
  ui: { fontFamily: Inter, fontSize: 0.875rem, fontWeight: 500, lineHeight: 1.4, letterSpacing: 0 }
  label: { fontFamily: Inter, fontSize: 0.8125rem, fontWeight: 500, lineHeight: 1.35, letterSpacing: 0 }
  data: { fontFamily: JetBrains Mono, fontSize: 0.8125rem, fontWeight: 400, lineHeight: 1.45, letterSpacing: 0, fontVariantNumeric: tabular-nums }
  metric: { fontFamily: JetBrains Mono, fontSize: 1.75rem, fontWeight: 500, lineHeight: 1.1, letterSpacing: -0.01em, fontVariantNumeric: tabular-nums }
rounded:
  chip: 4px
  control: 6px
  panel: 10px
spacing:
  unit: 4px
  scale: [4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px]
  row-dense: 32px
  row: 40px
  gutter: clamp(1.1rem, 4vw, 4.5rem)
  content-max: 1440px
components:
  panel: { backgroundColor: "{colors.surface}", border: 1px solid {colors.line}, rounded: "{rounded.panel}", padding: 16px 20px }
  status-chip: { backgroundColor: "{colors.surface-raised}", textColor: "{colors.text}", rounded: "{rounded.chip}", padding: 2px 8px, typography: "{typography.label}" }
  metric-tile: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", typography: "{typography.metric}", caption: "{typography.data}" }
  button-primary: { backgroundColor: "{colors.text}", textColor: "{colors.void}", rounded: "{rounded.control}", padding: 8px 14px, typography: "{typography.ui}" }
  button-quiet: { backgroundColor: transparent, textColor: "{colors.text}", border: 1px solid {colors.line-strong}, rounded: "{rounded.control}", padding: 8px 14px }
  focus-ring: { outline: 2px solid {colors.signal-live}, outlineOffset: 2px }
---

# Starlight operator

## Overview

No token-level Starlight design system existed before this draft. What exists: the ops material doctrine in `C:/Users/frank/starlight/design.md` section 10, the behavioural brand pack `starlight-design-intelligence/brand-packs/sis/DESIGN.md` (which defers exact tokens to a pack that was never written), and two live sites that disagree. The Lab (`starlightintelligence.ai/app/globals.css`) runs cool ink with cyan and amber signals; the Protocol (`Starlight-Intelligence-System/site/src/app/globals.css`) runs violet `#a78bfa` and fuchsia `#f0abfc` with an ambient mesh drift and a dot grid. Both values were read from local checkouts that may predate main. This draft takes the Lab direction because it already matches the doctrine, and demotes violet to the frontier accent the brand pack describes.

The register is an instrument panel: calm until something changes, and then exact about what changed, when, and on what evidence. Operator mode is the default. Horizon, academy and cultural modes from the brand pack layer on top of these tokens; they do not replace them.

References to beat, each in one dimension:
- Linear (linear.app): calm density and keyboard-first navigation.
- Vercel dashboard, Observability tab: system state legible in one glance.
- Langfuse trace view (langfuse.com): agent traces; beat it on provenance and readable hierarchy.
- Stripe docs (docs.stripe.com): protocol documentation a stranger can act on.
- Anthropic research pages (anthropic.com/research): the institutional horizon register.

## Colors

Signal colours keep one operational meaning everywhere: live (cyan) means fresh, connected, or actionable now; attention (amber) means stale, waiting on a human, or near a limit; ok and danger mean what they say. Each state also carries a word, so colour is never the only channel. Violet `frontier` appears only in horizon or cultural mode, for research frontiers and imagination; it never colours operator chrome.

Neutrals are tinted toward the cool ink, never dead gray. One metal seam per view: a 1px directional gradient from `seam-from` to `seam-to` on the dominant panel, per section 10. No other gradient on a card.

Measured contrast on void `#07090a`: text 17.1, text-muted 7.5, signal-live 12.6, signal-attention 9.0, state-ok 11.4, state-danger 8.0, text-faint 4.8. On surface-raised, text-faint drops to 4.0, so it is for metadata on void only. Light mode, on `#eef3f3`: light-text 16.6, light-muted 6.4, light-live 5.3, light-attention 4.9, light-ok 5.7, light-danger 5.5.

Light mode is for academy and institutional pages; operator surfaces default dark and honour the user's scheme.

## Typography

Inter for interface and reading, JetBrains Mono with tabular numerals for data, IDs, timestamps and metrics, Newsreader for horizon display only. Both sites already load Inter and JetBrains Mono. The Lab also loads Poppins and Playfair Display; the proposal drops them, which removes two font downloads and one competing voice.

The scale is a major third (1.25) from 16px, which keeps dense panels tight. Sentence case throughout, including labels and chips; no forced uppercase and no wide tracking. The Protocol site's production design canary already fails a build on forced uppercase; the Lab's only reports it.

## Layout

A 12-column grid at 1440, 8 at 768, 4 at 375, content capped at 1440px. Operator views use a stable frame: left navigation, primary pane, optional inspector pane on the right. Density is earned: tables and timelines use 32px rows, forms and settings 40px. Wide tables scroll inside their container; the page body never scrolls horizontally, at 360px included.

No decorative hairline or dot grids (Frank's ruling, 2026-10-04). Lines separate data, never decorate a background.

## Elevation and depth

Flat ink on void is the default. Glass is an information channel: at most three surfaces per view earn `backdrop-filter`, and on a pulse panel clarity encodes freshness (fresh: blur 8px, saturation 1.15; stale: blur 22 to 26px, saturation 0.55). Elevation otherwise comes from the void, void-raised, surface, surface-raised steps and a 1px line. No drop shadows on informational cards.

## Shapes

Chips 4px, controls 6px, panels 10px. No pills except a live indicator dot. Icons are one system: 16px inline SVG at stroke 1.5, or a two-letter mono chip. No emoji on any surface.

## Motion

- Motion marks a real transition only: a state change, data arriving, a listening or speaking indicator.
- One curve, `cubic-bezier(0.4, 0, 0.2, 1)`. Durations: 160ms for state and hover colour, 240ms for a panel or inspector, 400ms ceiling.
- Never animate a static number; count-up on baked data misrepresents freshness.
- No hover lift on informational cards, no ambient mesh, no perpetual drift in operator mode. Horizon mode may hold one slow image move, stopped under reduced motion.
- `prefers-reduced-motion` removes all movement and keeps every state.

## Components

- Status chip: dot, word, and "as of" time in data type. The word carries the meaning; the dot repeats it.
- Metric tile: value in metric type, a caption naming the source and bake time, a stale treatment in attention when past its freshness window.
- Provenance path: the chain from claim to command or file, each hop linkable.
- Timeline and trace row: time, actor, action, result, evidence link, in a 32px row.
- Inspector pane: the selected item's full state and the decision that belongs to the operator.
- Command bar: keyboard-first, sentence-case results, recent commands first.
- Header: "baked <age> ago" computed live from the bake timestamp.

## Do's and don'ts

Do:
- Show what is happening, why it matters, and which decision is the operator's.
- Put "as of" on every baked number.
- Remove a motion before adding one.

Don't (banned patterns):
- Neon, cyan overload, pure black or pure white, purple-to-blue gradients, full-surface card gradients.
- Glass as a default skin, decorative grids, the Protocol site's dot grid and mesh drift in operator views.
- Count-up numbers, hover-lift cards, emoji, uppercase eyebrows.
- Anonymous robots at laptops, decorative brains, generic astronauts, random neon cities, stock "technology" images.
- Seeded counts, invented benchmarks, or a status without evidence behind it.
