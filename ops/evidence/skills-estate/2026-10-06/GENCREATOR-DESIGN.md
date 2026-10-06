---
version: alpha
name: GenCreator Territory B
description: New creative publishing. Warm paper and ink, Instrument Serif and Instrument Sans, one spot red per object. Draft 2026-10-06 for review; expands brand-packs/gencreator/DESIGN.md and does not replace the product's ADR-011.
colors:
  paper: "#fbf9f5"
  paper-laid: "#f3f0ea"
  paper-deep: "#e7e3db"
  ink: "#221f1b"
  ink-soft: "#57524b"
  ink-faint: "#6f6a62"
  rule: "#d9d4cb"
  signal: "#c8322a"
  signal-ink: "#a3271f"
  signal-wash: "rgba(200, 50, 42, 0.08)"
  state-ok: "#2f6a45"
  state-warn: "#8a5a00"
  state-info: "#2c5d8a"
  state-error: "#a3271f"
typography:
  display-xl: { fontFamily: Instrument Serif, fontSize: clamp(3.5rem, 8vw, 5.75rem), fontWeight: 400, lineHeight: 1.02, letterSpacing: -0.012em }
  display-l: { fontFamily: Instrument Serif, fontSize: clamp(2.5rem, 5vw, 3.75rem), fontWeight: 400, lineHeight: 1.05, letterSpacing: -0.01em }
  headline: { fontFamily: Instrument Serif, fontSize: 2.25rem, fontWeight: 400, lineHeight: 1.12, letterSpacing: -0.006em }
  title: { fontFamily: Instrument Sans, fontSize: 1.375rem, fontWeight: 500, lineHeight: 1.3, letterSpacing: 0 }
  body-l: { fontFamily: Instrument Sans, fontSize: 1.1875rem, fontWeight: 400, lineHeight: 1.55, letterSpacing: 0 }
  body: { fontFamily: Instrument Sans, fontSize: 1.0625rem, fontWeight: 400, lineHeight: 1.55, letterSpacing: 0 }
  ui: { fontFamily: Instrument Sans, fontSize: 0.9375rem, fontWeight: 500, lineHeight: 1.4, letterSpacing: 0 }
  archival-label: { fontFamily: Instrument Sans, fontSize: 0.8125rem, fontWeight: 400, lineHeight: 1.45, letterSpacing: 0 }
  folio: { fontFamily: Instrument Serif, fontSize: 1rem, fontWeight: 400, lineHeight: 1, letterSpacing: 0.02em }
  proof-mono: { fontFamily: Geist Mono, fontSize: 0.8125rem, fontWeight: 400, lineHeight: 1.5, letterSpacing: 0 }
rounded:
  none: 0px
  sm: 2px
  md: 4px
spacing:
  unit: 4px
  scale: [4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 144px]
  measure: 62ch
  gutter: clamp(1.25rem, 4vw, 3rem)
components:
  button-primary: { backgroundColor: "{colors.ink}", textColor: "{colors.paper}", rounded: "{rounded.sm}", padding: 12px 20px, typography: "{typography.ui}" }
  button-secondary: { backgroundColor: transparent, textColor: "{colors.ink}", border: 1px solid {colors.ink}, rounded: "{rounded.sm}", padding: 12px 20px }
  link: { textColor: "{colors.ink}", underline: 1px {colors.ink-faint}, underlineOffset: 0.18em }
  edition-mark: { textColor: "{colors.signal}", typography: "{typography.folio}" }
  source-note: { backgroundColor: "{colors.paper-laid}", textColor: "{colors.ink-soft}", borderLeft: 2px solid {colors.rule}, padding: 12px 16px, typography: "{typography.archival-label}" }
  review-state: { textColor: "{colors.ink}", typography: "{typography.ui}" }
  input: { backgroundColor: "{colors.paper}", textColor: "{colors.ink}", border: 1px solid {colors.ink-faint}, rounded: "{rounded.sm}", padding: 10px 12px }
---

# GenCreator Territory B

## Overview

Every release is a small cultural object: precise enough to trust, expressive enough to collect, visibly approved by a human. Authority, in order: the product's ADR-011 (`frankxai/gencreator.ai` docs/DECISIONS.md), `docs/brand/GENCREATOR_BRAND_SYSTEM.md` foundation v3, then `starlight-design-intelligence/brand-packs/gencreator/DESIGN.md`. This file expands those into tokens; where it disagrees with them, they win.

References to beat, each in one dimension:
- Stripe Press (press.stripe.com): editorial objects that feel published, not generated.
- Are.na (are.na): source fragments that stay visibly connected.
- Readymag (readymag.com): editorial layout on the web without a card wall.
- It's Nice That (itsnicethat.com): commissioned imagery for creative work.

## Colors

Paper and ink carry at least 90% of any composition. Spot red appears once per object, to register an edition, a source, a state or a signature. It is never a gradient endpoint, never a background wash beyond `signal-wash`, and never the only carrier of meaning.

Measured contrast (WCAG 2.2, against paper `#fbf9f5`): ink 15.6, ink-soft 7.4, ink-faint 5.1, signal-ink 7.0, signal 5.1. On paper-deep `#e7e3db`, ink-faint drops to 4.2 and signal to 4.2, so on that surface use ink-soft for text and keep signal to marks or type 18px and up.

States use their own colour plus a word and, where it helps, an icon: ok `#2f6a45`, warn `#8a5a00`, info `#2c5d8a`, error `#a3271f`. Brand red alone never says "error" or "approved".

Dark mode is an inverse proof surface, not the emotional default: ink background, paper text (15.6), rule `#a8a198` for secondary text (6.4). On ink, red is a mark only.

Drift to resolve before release: the live CSS (`app/globals.css`, `[data-territory='b']`) sets ink to `oklch(0.19 0.012 60)`, which renders `#18130e`, while the brand system's hex `#221f1b` is `oklch(0.241 0.009 75)`. Its `--signal` renders `#d01d21`, more saturated than `#c8322a`. Its `--ink-faint` renders `#8a8581` at 3.5:1 on paper and is used for the 13px archival label; that fails AA. This draft uses the documented hex and a darker ink-faint.

## Typography

Instrument Serif carries releases, essays, edition numbers and cultural scale. It ships in one weight with an italic, so hierarchy comes from size, measure and sequence, never bold. Instrument Sans carries reading, product controls and evidence. Geist Mono, already loaded by the product, is restricted to source IDs, hashes and timestamps.

Scale steps by roughly a perfect fourth (1.333) from the 17px body, with display sizes fluid between clamps. Natural sentence case everywhere; uppercase display labels are banned, and so is wide letter-spacing on small sans. Body measure stays at 62ch. Both families are OFL 1.1, self-hosted through next/font.

## Layout

An editorial grid with one dominant move per object: twelve columns at 1440, eight at 768, four at 375, with `gutter` between. Asymmetric sequencing beats centred stacks. Imagery and type either touch or leave generous paper. Folio numbers, crop marks and source notes belong to the work they identify. Hairlines are allowed only where they do editorial work (a rule above a folio, a source note's left edge), never as a background grid.

Spacing runs on a 4px unit; section rhythm uses 96 and 144, component padding 12 to 24.

## Elevation and depth

Paper does not float. No drop shadows on cards, no glass, no blur. Depth comes from the three paper weights and from a fold: a sheet or panel that turns once to reveal source, proof or approval. Photocopy texture (the existing `.paper-texture`, opacity 0.055, 0.04 under reduced motion) sits on paper surfaces only, never behind running text and never as a full-page filter.

## Shapes

Corners are square or nearly so: 0 for editorial blocks and images, 2px for controls, 4px for inputs and menus. No pills except a status chip that genuinely needs one. The registration mark and the edition number are the brand's recurring shapes.

## Motion

Motion shows authorship moving through the system: source enters, fragments gather, relationships resolve, the creator approves, the edition signs and holds. Use cuts, folds, registration shifts, typesetting and controlled width change.

- Durations: 120ms for press feedback, 240ms for a fold or reveal, 480ms for the signing moment. Nothing loops.
- Easing: `cubic-bezier(0.2, 0, 0, 1)` to enter, `cubic-bezier(0.4, 0, 1, 1)` to leave.
- Reduced motion keeps every state and proof and swaps movement for an instant change or a 120ms opacity step.

## Components

- Edition header: serif display title, folio and edition number in signal, one archival label stating source and date.
- Source note: laid paper, left rule, archival label type; links straight to the source.
- Review state: a word ("Draft ready", "Approved", "Export ready", "Published") that matches the brand system's state definitions, plus the reviewer and time in proof-mono. Never shown without the evidence behind it.
- Constellation: related artifacts drawn as a sequence with visible links back to one source, not a card grid.
- Buttons: ink on paper primary, outlined secondary, one primary per view. Focus ring 2px ink with 2px paper offset.
- Wordmark: none approved. Use the text `GenCreator` in Instrument Sans Medium; do not draw a monogram.

## Do's and don'ts

Do:
- Start from a real source and show it.
- Let one element carry the page; cut the rest.
- Label unavailable capability as unavailable.

Don't (banned patterns):
- Blue, cyan or green gradients, or the legacy loop-arrow presented as the future identity.
- Card walls, bento grids, floating dashboards, chrome blobs, neon brains, generic AI people, faceless laptop stock.
- Ambient glow, perpetual orbit, particle fields, generic scroll-reveal choreography.
- Uppercase eyebrow labels, tracking-wide micro type, more than one red per object.
- A shadcn skin over Territory B surfaces.
- Copy: "effortless", "limitless", "revolutionise", "supercharge", "content at scale", autonomous publishing.
