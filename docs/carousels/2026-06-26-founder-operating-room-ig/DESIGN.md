# Design - Founder Operating Room

## Production Method

Hybrid deterministic social deck:

- Generated source frames: text-free cinematic metaphors only.
- Final slide copy: deterministic Python/Pillow render already exported to `exports/png/` and `exports/jpg/`.
- PDF wrapper: deterministic `index.html` prints the exact slide PNGs into a LinkedIn-ready document.

## Format

- Instagram: 8 slides, 1080 x 1350, 4:5 portrait.
- LinkedIn: same slide sequence exported as PDF for document carousel review.
- Cover preview: slide 1 copied to `cover-preview.png`.

## Visual Direction

FrankX / Starlight editorial operating room:

- dark operational foundation
- restrained gold signal for judgment and approval
- cyan/blue technical accents for systems and proof
- tactile artifacts instead of generic AI abstraction
- visible rooms, cards, proof paths, platform cuts, and human approval

## Layout Rules

- One primary idea per slide.
- Large readable type.
- No exact text inside generated source imagery.
- Same crop across all slides.
- Keep UI-like labels as deterministic overlays.
- Use diagrams to explain how work moves, not to decorate.

## Platform Variants

LinkedIn:

- Use `deck.pdf`.
- Longer caption from `CAPTION.md` is acceptable.
- Best framed as founder operating model / AI team workflow.

Instagram:

- Use `exports/jpg/` or the existing zip.
- Use short caption variant from `CAPTION.md`.
- Stronger visual rhythm; do not add source footnotes onto the images.

## Accessibility Notes

- High contrast white text on dark foundation.
- Important text stays inside safe margins.
- Slide 7 has smaller aspect-ratio labels but they are supporting labels, not required body text.
- Contact sheet inspected for composition and sequence legibility.
