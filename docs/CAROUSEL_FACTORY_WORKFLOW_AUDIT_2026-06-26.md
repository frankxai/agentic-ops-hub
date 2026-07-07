# Carousel Factory Workflow Audit

Date: 2026-06-26

Scope: Starlight Daily Carousel Factory, Agentic Coding OS sample, and the
skills/tools used in the current workflow.

Verdict: the workflow produced artifacts but not top-notch social creative.
The process must be redesigned around creative confidence, not production
completion.

## Root Failure

The workflow confused "complete enough to review" with "strong enough to post."

It generated Markdown, a deterministic deck, image exports, and one generated
cover concept. Those are useful mechanics. They are not sufficient for public
social output.

## Skills And Tooling Audit

| Skill / Tool | What It Did | Failure | New Requirement |
| --- | --- | --- | --- |
| Carousel factory OS | Defined loop and file packet | Quality bar was too low; 26/30 allowed weak public art | V2 social-confidence gate, 90/100+ |
| Social Media Team OS | Defined approval and routing | Protected safety, not enough creative excellence | Add "would a social team post this?" gate |
| FrankX lane guides | Gave voice, palette, and deterministic text rules | Did not force campaign-level identity | Require creative direction and social-native variants |
| `premium-visual-design` skill | Correctly requires references, critique, and scoring | Was not treated as blocking enough after weak output | Any critic "would not post" forces rebuild |
| `imagegen` skill / `image_gen` tool | Generated one cover concept | First-pass generation was treated as improvement, not draft | Generate 3+ distinct directions for important covers; inspect and score all |
| Chrome/Pillow export | Produced PNG/JPG sequence and contact sheet | Export mechanics had footer/crop defect | Export defects block approval routing |
| Evidence JSON | Recorded artifacts and 27/30 score | Evidence rewarded completeness more than creative quality | Add 100-point social-confidence score and rebuild verdict |
| Slack approval process | Prevented queue noise | Prior packet still said approval-ready too long | `REBUILD_REQUIRED` must override approval-ready language |

## Failure Modes Observed

- Markdown and file completeness became a proxy for creative readiness.
- Generated cover art was not campaign-defining.
- The deck looked like a dark internal docs export.
- Repeated panels and small labels weakened social rhythm.
- LinkedIn and Instagram were treated as export formats, not separate creative
  surfaces.
- "Pass with notes" hid public-confidence problems.
- The approval packet overstated readiness.

## New Workflow

1. Learn from approvals, QA, performance, brand guides, and official sources.
2. Decide whether to create, improve, or only learn.
3. Write the editorial thesis.
4. Write `CREATIVE_DIRECTION.md`.
5. Produce three cover/mood directions if generated imagery is used.
6. Build deterministic exact-text deck.
7. Export PNG masters, contact sheet, and PDF.
8. Run multi-critic review in `DESIGN_REVIEW.md`.
9. Score with the 100-point social-confidence gate.
10. Route to `#social-approvals` only at 90/100+.

## Stop Conditions

Stop and rebuild when:

- Frank says the art is not good enough.
- Any critic says "would not post."
- The first frame does not feel campaign-worthy.
- Generated imagery looks generic or prompt-style.
- Platform variants are not intentionally designed.
- Export defects remain.
- Evidence does not include visual inspection.

## Immediate Policy Change

The Agentic Coding OS sample is now:

- production proof: yes
- source-backed draft: yes
- approval-ready social creative: no
- required status: `REBUILD_REQUIRED`

The next carousel automation should not create another approval packet until it
can produce a creative system that passes the V2 gate.
