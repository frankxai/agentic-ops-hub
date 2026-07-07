# Image Generation Guide: FrankX / AI-Architect / Builder Education

## Verdict

Use image generation for cinematic covers, metaphors, thumbnails, mood frames,
and campaign concepts. Use deterministic HTML/SVG/Figma/Canva for exact text,
diagrams, PDFs, source notes, UI claims, and final carousel slides.

## Tool Boundary

In Codex, use the local imagegen skill. The local skill says:

- built-in `image_gen` is the default for ordinary raster generation and edits
- generated images should be inspected before use
- project-bound images must be moved into the workspace
- CLI/model-specific behavior requires explicit path choice and may require
  `OPENAI_API_KEY`

Do not rely on model-specific behavior or name a model as a guarantee unless the
current local skill/docs and official model docs have been checked. The workflow
does not require GPT Image 2 specifically; it requires a controlled loop.

## Use Generated Images For

- cinematic cover art
- visual metaphors: cockpit, control plane, operating room, map, radar, workbench
- thumbnails
- mood frames for a later deterministic deck
- non-text-heavy scene concepts
- background plates where exact overlay text will be added separately

## Do Not Use Generated Images For

- final slide text
- dense diagrams
- product UI that claims to be real
- final source citations
- precise channel maps
- logos or brand marks as final assets
- screenshots of private systems

## Prompt Pattern

```text
Use case: ads-marketing
Asset type: LinkedIn carousel cover
Primary request: <single idea>
Audience: <founder / AI architect / builder>
Scene/backdrop: <specific metaphor>
Subject: <what must read in 3 seconds>
Style/medium: premium editorial-tech, obsidian base, restrained cyan/emerald and amber accents
Composition/framing: 4:5 portrait, mobile-safe, room for exact text overlay
Lighting/mood: crisp, high-contrast, not foggy or generic
Text: none, or only exact short title if explicitly needed
Constraints: no fake logos, no private data, no tiny labels, no malformed UI, no watermark
Avoid: purple-blue generic AI gradient, fake dashboards, illegible text, clutter
```

## Cover Workflow

1. Create `BRIEF.md` first.
2. Decide whether the cover needs an image at all. Many technical decks are
   stronger with deterministic diagram covers.
3. If generating, produce at least three meaningfully different concepts for
   important public-facing work.
4. Inspect every actual output.
5. Reject generic, stock-like, fake-text-heavy, malformed, or weakly cropped
   generations.
6. Add title/subtitle outside the generated image.
7. Score with the V2 social-confidence gate, not only the 30-point gate.
8. Store prompt, file path, critique, score, and iteration decision in
   `evidence.json`.

No first-pass generated cover may be treated as final. If the best generated
image is merely acceptable, do not use it as the campaign cover; build a
deterministic high-design graphic instead.

## Canva vs Local

Use Canva when:

- Frank or a human designer needs quick editing
- brand-kit assets and social export presets matter
- a campaign family needs many manual variants
- the artifact is mostly marketing packaging

Use local HTML/SVG/PDF when:

- exact text or diagrams matter
- the deck should be reproducible
- the file needs code review or template reuse
- the artifact becomes a client/community operating-system template

## QA Checklist

- subject reads in 3 seconds
- crop works at target aspect ratio
- no fake text or malformed UI
- no fake logos
- no private/internal data
- visual style fits the brand lane
- exact title/copy added outside generator when needed
- artifact saved in repo if used by a pack
- score and critique recorded
