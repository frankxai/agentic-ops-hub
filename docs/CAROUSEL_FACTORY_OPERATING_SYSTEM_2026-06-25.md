# Carousel Factory Operating System

Created: 2026-06-25

Channel of record: `#social-carousels` (`C0BCPG55PJB`)

Purpose: produce premium LinkedIn and Instagram carousel assets for FrankX,
AI-Architect, builder/founder education, and agentic work tutorials.

## 2026-06-26 Creative Standard Update

Use `CAROUSEL_FACTORY_CREATIVE_STANDARD_V2_2026-06-26.md` as the mandatory
quality contract for all new runs.

The original factory loop proved that Codex can create briefs, decks, PDFs, and
exports. That is not enough. A carousel is not approval-ready unless it passes
the V2 social-confidence gate at 90/100 or higher and a human-quality review
would be comfortable putting it in a public social queue.

The 2026-06-25 Agentic Coding OS pack is now a learning artifact with verdict
`REBUILD_REQUIRED`, not an approval-ready candidate.

## Verdict

Use one dedicated channel now: `#social-carousels`.

Do not split LinkedIn and Instagram into separate carousel rooms yet. The work
is 80 percent shared: research, thesis, structure, design system, exact slides,
approval, and reuse. Platform differences belong inside the thread:

- LinkedIn: document PDF, 1080x1350, executive/educational framing.
- Instagram: image sequence, 1080x1350 or 1080x1080, tighter hooks and less text.

Split later only if volume exceeds the channel's ability to stay readable.

## Operating Loop

```text
Research signal
  -> learning inputs from prior approvals, QA, and performance
  -> carousel brief
  -> design/taste markdown
  -> deterministic HTML/SVG deck
  -> PDF/PNG export
  -> visual QA
  -> #social-carousels
  -> #social-approvals
  -> human publish/download
  -> performance note
```

## Channel Rules

Top-level posts in `#social-carousels` must use one label:

- `Brief`: new carousel idea or topic.
- `Draft`: produced deck or post candidate.
- `Proof`: final artifact path, PDF, image sequence, or QA note.
- `Approval`: ready for `#social-approvals`.
- `Learning`: performance and next iteration.

Threads hold:

- platform variants
- source checks
- copy edits
- visual QA
- alternate hooks

## Required Files Per Carousel

Each carousel pack should include:

- `BRIEF.md`
- `DESIGN.md`
- `TASTE.md`
- `POST.md`
- `APPROVAL_PACKET.md`
- `LEARNING.md`
- `CREATIVE_DIRECTION.md`
- `DESIGN_REVIEW.md`
- `EXPORTS.md`
- `index.html`
- `deck.pdf`
- `cover-preview.png`
- `contact-sheet.png`
- `exports/png/`
- `evidence.json`

Use image generation for covers or visual metaphors only when useful. Use
deterministic HTML/SVG/Figma/Canva for final slide text.

## Content Lanes

| Lane | Brand | Examples |
| --- | --- | --- |
| Founder AI OS | FrankX | How to run agents, Slack cockpit, approval gates |
| Builder Tooling | Tooling / FrankX | Codex, Claude Code, Antigravity, GitHub workflow |
| AI CoE | AI-Architect | Enterprise AI governance, adoption, spend controls |
| Creator Systems | GenCreator | Content factories, creator OS, templates |
| Research Intel | Mind / Research | Source-backed frameworks and claim labels |

## Quality Gate

V2 gate:

- Social-confidence score must be 90/100 or higher before routing to
  `#social-approvals`.
- The older 30-point score is only a baseline QA check.
- Any public-confidence issue means `REBUILD_REQUIRED`, not "approval-ready with
  notes."

Ship only when:

- one idea per slide
- exact text is deterministic, not image-generated
- first slide hooks in three seconds
- every claim has source or is framed as opinion
- visual hierarchy works on mobile
- no fake screenshots, logos, or private data
- approval gate is explicit

Score using `design-agent-standards/OUTCOMES.md`. Ship at 26/30+.

## Learning Loop

Before choosing the daily carousel, Codex should read:

- new official AI lab/product updates when making topical claims
- prior `#social-approvals` decisions: approve, approve with edits, revise, hold
- Frank's direct edit notes, especially headline, stack, tone, and claim-risk
- prior carousel `evidence.json` scores and design QA notes
- manually collected performance metrics when a post was approved and published
- brand/lane guides under `docs/social-media-team-os/`
- relevant brand packs in `starlight-design-intelligence`

Every new pack should include a short learning note:

```text
Learning input:
- official source signal:
- approval/rejection signal:
- design QA signal:
- performance signal:
- brand guide signal:

Decision:
- make:
- cut:
- carry forward:
```

If no meaningful signal exists, improve an existing candidate or produce a
learning note instead of manufacturing a low-confidence carousel.

## Automation Owner

Codex owns the daily carousel factory automation because it can combine:

- current AI lab/news signals
- repo and Slack context
- brand voice
- deterministic artifact generation
- approval-safe Slack routing
- prior approval/rejection learning
- design QA scores
- performance notes
- brand-specific style guides

n8n or Make.com can later own reminders and form intake. They should not own
the judgment-heavy carousel synthesis loop.
