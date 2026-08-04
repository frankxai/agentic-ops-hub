# Starlight Content Studio — Stage 0

## Working brief

| Field | Decision |
| --- | --- |
| User + job | Frank needs one calm place to browse the evidence, decisions, and original draft packages before he records, edits, or approves anything. |
| Primary action | Select a draft, inspect its provenance/constraints, copy the working draft, or open a source. |
| Register | Professional, precise, warm; Starlight blue signals system state, FrankX violet signals authored work, and emerald signals a review-ready next move. |
| Central design idea | **An editorial workbench, not a marketing dashboard:** the evidence rail stays visible while a selected draft becomes the working surface. |
| Data authority | Canonical policy/research remain in sibling SMIS documents. `studio-data.json` is the versioned Stage 0 read model and draft-seed store for this Studio only. |
| External dependencies | None. Semantic static HTML, CSS, and JavaScript only. |
| Accessibility | Native buttons/links, visible focus, keyboard-operable filters, semantic landmarks, high-contrast text, responsive single-column fallback, and reduced-motion-safe transitions. |
| Stage boundary | No authentication, API calls, write-through publishing, scheduling, account connection, or provider invocation. Clipboard copy is local and user initiated. |

## Start locally

From this directory, run `start-content-studio.cmd` on Windows, or:

```bash
python3 -m http.server 4173
```

Then open [http://127.0.0.1:4173](http://127.0.0.1:4173). A local-only **SMIS Content Studio** desktop shortcut points to the same URL while its local server is running.

## What is saved here

- `studio-data.json` — research/source cards, the current work queue, and three original draft packages;
- `index.html` — local exploration/review surface;
- `content-studio.manifest.json` — versioned artifact record and scope boundary.

The Studio is a **projection**, not a second approval, publishing, or source-of-truth system. Source links and canonical paths are displayed in the interface.