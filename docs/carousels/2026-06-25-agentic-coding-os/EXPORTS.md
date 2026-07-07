# Carousel Exports

Generated: 2026-06-26

Source: `index.html`

Renderer: local Chrome headless via `export-slide.html`, 1080x1350 viewport.

## Visual Assets

| Asset | Path | Notes |
| --- | --- | --- |
| Contact sheet | `contact-sheet.png` | Visual review sheet for all 10 slides |
| PNG sequence | `exports/png/` | 10 deterministic 1080x1350 slide images |
| JPG sequence | `exports/jpg/` | 10 compressed posting/review images |
| JPG ZIP | `agentic-coding-os-carousel-jpg.zip` | Packaged JPG sequence |
| Premium cover concept | `assets/generated/agentic-coding-os-premium-cover-concept.png` | Built-in `image_gen` cover/metaphor image, no exact slide text |
| LinkedIn PDF | `deck.pdf` | Document carousel export |
| Cover preview | `cover-preview.png` | First-slide preview |

## Exported Files

- `exports/png/01-agentic-coding-os.png`
- `exports/png/02-agentic-coding-os.png`
- `exports/png/03-agentic-coding-os.png`
- `exports/png/04-agentic-coding-os.png`
- `exports/png/05-agentic-coding-os.png`
- `exports/png/06-agentic-coding-os.png`
- `exports/png/07-agentic-coding-os.png`
- `exports/png/08-agentic-coding-os.png`
- `exports/png/09-agentic-coding-os.png`
- `exports/png/10-agentic-coding-os.png`

- `exports/jpg/01-agentic-coding-os.jpg`
- `exports/jpg/02-agentic-coding-os.jpg`
- `exports/jpg/03-agentic-coding-os.jpg`
- `exports/jpg/04-agentic-coding-os.jpg`
- `exports/jpg/05-agentic-coding-os.jpg`
- `exports/jpg/06-agentic-coding-os.jpg`
- `exports/jpg/07-agentic-coding-os.jpg`
- `exports/jpg/08-agentic-coding-os.jpg`
- `exports/jpg/09-agentic-coding-os.jpg`
- `exports/jpg/10-agentic-coding-os.jpg`

## QA Notes

- Contact sheet inspected in Codex.
- Slide 1 inspected at full size.
- Premium `image_gen` cover concept inspected in Codex.
- Text is deterministic and generated from the HTML source, not baked by an image
  generator.
- Generated cover concept is a visual metaphor only. Exact title/copy should be
  overlaid in deterministic HTML/SVG/Figma/Canva before use.
- Known polish note: the current source layout leaves a dark footer band on the
  slide PNG/JPG exports. The sequence is usable for review, but the next visual
  pass should tighten the export crop or source slide height before final
  posting.
