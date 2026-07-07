# Design: Agent Workbench OS

## Production Method

Deterministic HTML/CSS/SVG deck at 1080x1350. Exact slide text, labels, source
notes, and diagrams are rendered in code. No generated image is used as final
slide art in this version.

## Tokens

```text
bg: #05060A
surface: #0B0F14
surface-2: #111827
ink: #F8FAFC
muted: #94A3B8
border: #1A1F2E
tech: #14B8A6
cyan: #06B6D4
approval: #F59E0B
proof: #72E6AC
danger: #FF7A90
```

## Typography

- Display: system geometric sans, 76-96px.
- Slide headline: 58-78px.
- Body: 28-38px.
- Small labels: 18-24px, not required for comprehension.
- Letter spacing: 0.

## Grid

- 1080x1350 canvas.
- 76px outer margin.
- Large left-aligned type on most slides.
- Workbench diagrams use stable lanes and fixed cards.
- Every slide has a different composition role to prevent deck monotony.

## Visual Grammar

- Work rails show movement.
- Gate lines show approval.
- Proof packets show evidence.
- Ledger/shelf surfaces show durable memory.
- Amber appears only where judgment or approval matters.
- Cyan/emerald appears only where active agent work or source proof matters.

## LinkedIn Variant

The PDF and PNG sequence are the primary LinkedIn asset. It can carry source
notes on slide 10 and a restrained product/source signal on slide 8.

## Instagram Variant

Use the same exported PNG/JPG sequence for review. Before external posting,
trim the caption and reduce slide 8 source detail in a copy-only pass if needed.

## QA Targets

- No crop/footer band.
- No clipped text.
- No fake UI.
- No text baked into generated images.
- Contact sheet must be inspectable at a glance.
- Social confidence target: >=90/100 before approval routing.
