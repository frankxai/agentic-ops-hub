# Carousel Factory Creative Standard V2

Created: 2026-06-26

Status: mandatory operating contract for Starlight Daily Carousel Factory runs.

This supersedes the weaker interpretation of the carousel factory where a
legible HTML deck, PDF, contact sheet, or first-pass generated image could be
called approval-ready. The factory now optimizes for social-team confidence:
something a strong brand/social team would be comfortable showing publicly after
human approval.

Companion audit:
`CAROUSEL_FACTORY_WORKFLOW_AUDIT_2026-06-26.md`

Nothing in this document approves publishing, scheduling, customer messages,
spend, deploys, merges, Slack access changes, or Hermes gateway activation.

## Verdict

The current Agentic Coding OS carousel is useful as internal proof, but it is
not top-notch social creative. It must be treated as `REBUILD_REQUIRED`, not as
an approval-ready asset.

Why:

- The visual system feels like an internal technical deck, not a confident
  social campaign.
- The slide sequence is too templated: repeated dark panels, small labels, weak
  rhythm, little editorial surprise.
- The generated cover concept is not bad, but it is generic and not
  campaign-defining.
- The export has a visible footer/crop issue.
- The package proves production mechanics, not creative excellence.

## New Definition Of Done

A carousel run is only complete when it produces a full creative packet:

- `BRIEF.md`: source-backed insight, audience, claim risk, and approval boundary.
- `CREATIVE_DIRECTION.md`: one concept, visual thesis, references, keep/cut,
  signature visual behavior, and why this is worth posting.
- `DESIGN.md`: typography, grid, color, imagery, composition, and platform
  variants.
- `TASTE.md`: multi-critic notes and final taste verdict.
- `POST.md`: LinkedIn, Instagram, and optional X/Threads copy.
- `APPROVAL_PACKET.md`: final decision request only if the social-confidence
  gate passes.
- `DESIGN_REVIEW.md`: creative director, visual designer, social strategist,
  source editor, and production QA review.
- `LEARNING.md`: official source, approval/rejection, design QA, performance,
  and brand-guide learning.
- `index.html` or editable design source: deterministic exact-text deck.
- `deck.pdf`: LinkedIn document carousel when Chrome export is available.
- `exports/png/`: PNG master slide sequence.
- `exports/jpg/`: compressed sequence only for handoff/posting.
- `contact-sheet.png`: all slides visible at a glance.
- `cover-preview.png`: final cover, not just a screenshot of slide 1.
- `assets/generated/`: generated cover/mood concepts, if used.
- `evidence.json`: full evidence trace and scores.

Markdown-only output is a failure. JPEG-only output is a failure. A single
generated image without critic iteration is a failure.

## Production Phases

### Phase 0: Intake Gate

Before making anything, decide whether the run should create a new carousel,
improve an existing one, or only write a learning note.

No new approval candidate may be created while the approval queue is blocked
unless it explicitly replaces a waiting item.

### Phase 1: Editorial Thesis

Output:

- one sharp audience
- one problem or opportunity
- one mechanism
- one proof object
- one approval boundary
- one reason this belongs on social now

Reject:

- generic AI commentary
- "AI will change everything" copy
- tool-name soup with no operating mechanism
- content that only restates internal docs

### Phase 2: Creative Direction

Output `CREATIVE_DIRECTION.md` with:

- first-frame hook
- visual thesis
- signature motif
- image system
- typography posture
- mobile crop behavior
- references and anti-references
- what must stay still
- what must be cut

Minimum references:

- brand pack
- one prior Starlight/FrankX artifact or approved direction
- one social/editorial design reference category
- one platform-specific crop or readability consideration

### Phase 3: Premium Visual Generation

Use generated images only for covers, metaphors, thumbnails, mood frames, or
background plates. Exact slide text, diagrams, source labels, and UI claims stay
deterministic.

Minimum expectation:

- create at least three distinct cover directions when a generated cover matters
- inspect every generated output
- reject anything generic, foggy, fake-text-heavy, malformed, or stock-like
- keep the best one only if it is campaign-defining
- record prompt, file path, critique, and score

Generated visuals must be judged as art direction, not as proof that an image
tool ran.

### Phase 4: Deterministic Deck Craft

The deck must feel designed, not templated.

Requirements:

- no visible crop/footer/export defects
- no tiny labels required for comprehension
- no repeated dark card grid without rhythm change
- every slide has a distinct composition role
- cover is memorable at phone size
- slides 2-9 have movement in pacing: contrast, scale, diagram, proof, checklist
- source notes are legible but not visually dominant
- exact title/copy is deterministic
- PNG master sequence exists before approval routing

### Phase 5: Social Confidence Review

Run a multi-critic review before any `#social-approvals` routing:

- Creative Director: is the idea and visual concept strong enough?
- Visual Designer: is composition, crop, hierarchy, and type social-grade?
- Social Strategist: will this stop the right audience in-feed?
- Source Editor: are claims source-backed or clearly framed as opinion?
- Production QA: are exports complete, clean, and inspectable?

If any critic says "would not post," the packet is `REBUILD_REQUIRED`.

### Phase 6: Approval Routing

Only route to `#social-approvals` when:

- social-confidence score is 90/100 or higher
- all required assets exist
- visual QA is pass, not pass-with-notes on core quality
- the approval packet states exact decision language
- the item is not adding noise to an already blocked approval queue

Otherwise post only a workroom `Learning` or `Proof` note to `#social-carousels`.

## Social Confidence Score

Use this 100-point gate for social assets. The older 30-point gate remains a
baseline visual QA check, not the approval threshold.

| Dimension | Points | Approval Standard |
| --- | ---: | --- |
| Editorial hook and usefulness | 15 | clear, specific, saves or teaches something real |
| Creative concept and memorability | 20 | first frame feels campaign-worthy, not generic |
| Visual craft and typography | 20 | type, spacing, crop, rhythm, and hierarchy are polished |
| Platform fit | 15 | LinkedIn and Instagram variants are intentionally different |
| Brand fit | 10 | FrankX/AI-Architect tone, palette, and behavior are distinct |
| Factual provenance | 10 | claims are sourced, softened, or labeled as opinion |
| Production evidence | 10 | exports, contact sheets, QA, and paths are complete |

Decision:

- `95-100`: flagship social candidate.
- `90-94`: approval-ready candidate.
- `80-89`: workroom proof only; iterate before approval.
- `70-79`: internal draft; rebuild the creative system.
- `<70`: restart from brief and references.

No carousel below 90 may be called approval-ready.

## Rebuild Triggers

Restart or redesign when any of these are true:

- Frank or reviewer says the art is not post-worthy.
- Output looks like an internal deck, not a public social asset.
- Generated image looks generic, stock-like, or prompt-style.
- First slide could be mistaken for any AI consultant's carousel.
- The strongest asset is the Markdown, not the visual.
- The sequence relies on tiny labels, repeated boxes, or dense source cards.
- There are crop defects, footer bands, clipped text, blank media, or artifacts.
- Evidence claims "pass with notes" but notes affect public confidence.
- There is no contact sheet or actual visual inspection.

## Output Expectations By Surface

LinkedIn:

- PDF plus PNG contact sheet.
- Executive/builder education pacing.
- Can carry more text, but not dense technical note cards.
- Strong source note on final slide.

Instagram:

- PNG image sequence first, not PDF-first thinking.
- 30-50 percent fewer words than LinkedIn.
- Stronger visual rhythm and fewer source footnotes.
- Square variant only when it improves legibility.

Cover/thumbnail:

- Must work as a standalone image.
- Exact title must be overlaid deterministically.
- Generated cover must be inspected and scored.
- No fake UI, fake logos, or fake text-heavy panels.

## Current Sample Verdict

Pack:
`C:\Users\frank\starlight\repos\agentic-ops-hub\docs\carousels\2026-06-25-agentic-coding-os\`

Verdict: `REBUILD_REQUIRED`.

Social confidence score: 68/100.

Reason:

- useful mechanism and source discipline
- insufficient social art direction
- weak campaign identity
- generic generated cover
- deck craft too templated
- visible export polish issue

Next acceptable step:

Do not patch this version into approval-readiness. Rebuild from the editorial
thesis, creative direction, and a stronger visual system.
