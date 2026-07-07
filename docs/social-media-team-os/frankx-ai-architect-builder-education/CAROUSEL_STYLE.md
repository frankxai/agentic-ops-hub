# Carousel Style Guide: FrankX / AI-Architect / Builder Education

## Format

Primary:

- LinkedIn document carousel
- 1080x1350 portrait
- deterministic HTML/CSS source
- PDF export

Secondary:

- Instagram carousel
- 1080x1350 or 1080x1080
- PNG sequence
- 30-40 percent less text than LinkedIn

## Required Pack Files

Each carousel pack should include:

- `BRIEF.md`
- `DESIGN.md`
- `TASTE.md`
- `POST.md`
- `APPROVAL_PACKET.md`
- `index.html`
- `deck.pdf`
- `cover-preview.png`
- `evidence.json`

## Slide Structure

Default 10-slide educational deck:

1. Category or strong mechanism hook
2. Old way / failure mode
3. New model
4. Architecture or lanes
5. Step-by-step workflow
6. Guardrails or approval gates
7. Operating packet or template
8. Source-backed current signal
9. Starter setup or checklist
10. Save/CTA and source note

## Design Tokens

Use FrankX / Starlight dark technical defaults unless a pack overrides:

```text
bg: #05060A
surface: #0A0C14
border: #1A1F2E
ink: #F1F3F9
muted: #8A90A8
accent: #6EA8FE
tech: #14B8A6
approval: #F6C86B
proof: #72E6AC
danger: #FF7A90
```

## Typography

- Headline: 62-82px, heavy, line-height near 1.0
- Body: 30-42px, high contrast
- Meta: 20-26px
- Captions/sources: 20-24px, only where legible
- Letter spacing: 0

Use Instrument Sans, Geist, or a system stack. Avoid tiny mono labels unless
they are purely decorative and not necessary for comprehension.

## Composition

- One idea per slide.
- First read in 3 seconds.
- Strong top-left or centered headline.
- Use rails, lanes, gates, proof chips, and diagram blocks as recurring motifs.
- Keep mobile-safe margins.
- Make every block large enough to read on a phone.
- Use diagrams to teach mechanism, not decorate.

## Exact Text Rule

Final carousel text must be deterministic:

- HTML/CSS
- SVG
- Figma
- Canva
- slides

Generated images may be used for cover mood or metaphor, but exact slide text,
source notes, channel names, tool names, and diagrams must be produced outside
the generator.

## LinkedIn vs Instagram

LinkedIn:

- can carry more explanation
- use PDF
- source note can live on final slide
- B2B/education tone

Instagram:

- reduce text density
- stronger visual rhythm
- less source footnote text
- clearer single hook per image
- consider square variant when diagram density is high

## QA Score

Use `OUTCOMES.md` 30-point gate:

- 5 first read and hierarchy
- 5 brand fit and distinctiveness
- 5 craft, typography, spacing, composition
- 5 accessibility, contrast, responsiveness
- 5 factual accuracy, provenance, no artifacts
- 5 usefulness on intended surface

Baseline pass remains 26/30 or higher, but this is not enough for approval
routing.

Use `CAROUSEL_FACTORY_CREATIVE_STANDARD_V2_2026-06-26.md` for the actual social
approval threshold:

- 90/100+ social-confidence score is required for `#social-approvals`.
- 80-89 is workroom proof only.
- below 80 requires creative rebuild.
- Any "would not post this" critic verdict means `REBUILD_REQUIRED`.

Do not call a deck approval-ready because it is legible, exported, or
source-backed. It must feel designed, social-native, and brand-confident.

## Common Fixes

- If the deck feels generic, add a concrete workflow or artifact.
- If it feels too Slack-specific, reframe channels as generic operating spaces.
- If it feels too enterprise, add founder-useful implementation steps.
- If it feels too tactical, add the strategic reason the workflow matters.
- If it feels too dense, split the slide or remove one idea.
