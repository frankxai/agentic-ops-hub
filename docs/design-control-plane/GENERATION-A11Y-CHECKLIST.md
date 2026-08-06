# Generation Accessibility Checklist

Bolt this into **any** image, video, infographic, animation, or canvas generation before calling the output production-ready.

## Must ship with every asset

| Check | Pass criterion |
| --- | --- |
| **Purpose** | One sentence: what job the asset does for the user |
| **Alt text / caption** | Human-written; not “image of…” filler; empty alt only if pure decoration |
| **Contrast** | Text over fill meets WCAG AA for the intended display size (or mark as decorative) |
| **Text in image** | Prefer live HTML text; if burned in, keep large, high-contrast, non-essential |
| **Color independence** | Meaning not only by color (icons/labels too) |
| **Safe zone** | Critical content inside crop-safe margins for OG/social/mobile |
| **Motion** | If animated/video: no seizure risk; provide static poster; respect reduced-motion in UI embedding |
| **Reading order** | Infographic panels ordered; screen-reader caption summarizes structure |
| **Brand register** | Professional vs mythic not mixed |
| **License** | Fonts/faces inside asset classified; stock/AI provenance recorded |

## UI embedding rules

- Decorative images: `alt=""` + CSS that doesn’t steal focus.
- Informative images: meaningful `alt` ≤ ~140 chars + longer caption if needed.
- Icons with actions: accessible name on the control, not only on the SVG.
- Lottie/video backgrounds: pause when offscreen; never the only path to content/CTA.
- Always provide a non-motion path.

## Fail closed

If alt/contrast/provenance cannot be produced, mark asset **`draft` / research-only** — not production.

## Related

- `web-launch-ux-accessibility-audit`
- `estate-design-excellence`
- `FONT-LICENSING-SOURCES.md`
- `BRAND-MEDIA-OPERATING-SYSTEM.md`
