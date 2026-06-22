# Agentic Income GitHub Visual System

Date: 2026-06-22

This repo owns the repeatable visual system for the agentic-income GitHub estate.

## Design Thinking

- First read: each README banner must answer what the repo is, where it sits in L0-L7, and what safety or income job it performs.
- Specificity beats polish: diagrams show the actual operating contract, not abstract AI decoration.
- Text is deterministic SVG. Generated raster art may provide atmosphere, but never exact labels.
- GitHub readability wins over spectacle: high contrast, large type, no tiny baked text, no cards inside cards.

## Asset Contract

- `assets/github/header.svg`: 1280 x 640 README banner.
- `assets/github/how-it-works.svg`: 1280 x 720 repo operating map.
- `assets/github/provenance.json`: design sources, generated prompt, and visual-system version.
- `assets/github/ecosystem-map.svg`: only in `agentic-ops-hub`; the L0-L7 estate map.
- `assets/github/ecosystem-backplate.png`: only in `agentic-ops-hub`; text-free imagegen style frame.

## Palette Roles

- L1 capability: cyan and emerald.
- L2 config: cyan and violet.
- L4 income: blue, teal, emerald, amber.
- L5 payments: amber and cyan.
- L6 swarm: violet and cyan.
- L7 assurance: red and cyan.

## Regeneration

Run from `agentic-ops-hub`:

```bash
node scripts/generate-github-visuals.mjs
```

The generator expects sibling checkouts for the named repos in the same parent directory.
