# Generation Accessibility Checklist

**Apply this checklist to** any image, video, infographic, animation, or canvas generation before calling the output production-ready.

## Must ship with every asset

| Check | Pass criterion |
| --- | --- |
| **Purpose** | One sentence: what job the asset does for the user |
| **Alt text / caption** | Human-written; not “image of…” filler; empty alt only if pure decoration |
| **Contrast** | Text over fill meets WCAG AA for the intended display size. Skip AA only when purely decorative and no information/interaction depends on the asset; otherwise revise until compliant |
| **Text in image** | Prefer live HTML text; if burned in, keep large, high-contrast, non-essential |
| **Color independence** | Meaning not only by color (icons/labels too) |
| **Safe zone** | Critical content inside crop-safe margins for OG/social/mobile |
| **Motion** | If animated/video: no more than three flashes per second in any one-second period (WCAG 2.3.1); provide static poster; embedded UI must honor `prefers-reduced-motion` |
| **Reading order** | Infographic panels ordered; screen-reader caption summarizes structure |
| **Brand register** | Professional vs mythic not mixed |
| **License** | Fonts/faces inside asset classified; stock/AI provenance recorded |

## UI embedding rules

- Decorative images: `alt=""` + CSS that doesn’t steal focus.
- Informative images: meaningful `alt` ≤ ~140 chars + longer caption if needed.
- Icons with actions: accessible name on the control, not only on the SVG.
- Lottie/video backgrounds: pause when offscreen; never the only path to content/CTA.
- Always provide a non-motion path.

## If a required check is missing

Set status to `draft` or `research-only` and **block production release** until fixed.

## Related

- `web-launch-ux-accessibility-audit`
- `estate-design-excellence`
- `FONT-LICENSING-SOURCES.md`
- `BRAND-MEDIA-OPERATING-SYSTEM.md`
