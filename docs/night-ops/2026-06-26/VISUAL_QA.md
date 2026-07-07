# Visual QA - Nightly Agentic Team Packet

Date: 2026-06-26

## Scope

Eleven deterministic SVG operating cards:

- `01-slack-agent-cockpit.svg`
- `02-agent-swarm-map.svg`
- `03-social-image-factory.svg`
- `04-tonight-action-board.svg`
- `05-portfolio-business-signal-board.svg`
- `06-arcanea-red-lane-map.svg`
- `07-slack-proof-loop-scorecard.svg`
- `08-social-approval-backlog-board.svg`
- `09-domain-deployment-radar.svg`
- `10-slack-channel-anchor-matrix.svg`
- `11-arcanea-weekly-proof.svg`

These are internal Slack/ops visuals. They are not final public campaign assets.
SVG sources were rendered to PNG with Chrome headless and inspected in the
Codex image viewer.

## Standards Loaded

- `DESIGN_TASTE.md`
- `WEB_EXPERIENCE_STANDARD.md`
- `MOTION_TASTE_RUBRIC.md`
- `MULTI_AGENT_DESIGN_COUNCIL.md`
- `VISUAL_QA_GATE.md`
- `design-agent-standards/DESIGN.md`
- `design-agent-standards/AGENTIC_DESIGN_LOOP.md`
- `design-agent-standards/ULTIMATE_AGENTIC_LOOPS.md`
- `design-agent-standards/RED_TEAM_CHECKLIST.md`
- `design-agent-standards/OUTCOMES.md`
- `design-agent-standards/best-practices/image-logo-visual-generation.md`
- `starlight-design-intelligence/DESIGN_AGENT_OPERATING_SYSTEM.md`
- `starlight-design-intelligence/evals/generated-asset-quality-gate.md`
- `agentic-ops-hub/docs/social-media-team-os/frankx-ai-architect-builder-education/*`

## QA Notes

### First Read

Pass. Each visual answers one operating question:

- What Slack rooms exist and what is missing?
- Which agents own which business lanes?
- How does social/image content move from signal to approval?
- What must happen tonight?
- How each business lane routes through Slack and proof.
- Why Arcanea is the current red repo lane and what decision is required.
- Whether the first Slack proof-loop is useful enough to keep.
- Which social approval candidates need decisions before adding more assets.
- Which domains are live, which website lanes need governance, and where
  Arcanea/domain ownership requires a decision.
- Which Slack rooms hold intake, truth, execution, executive signal, content,
  brand cadence, and approval gates.
- How the Arcanea weekly proof routes between `#brand-arcanea`,
  `#repo-command`, `#daily-report`, and `#execution-room`.

### Brand Fit

Pass with notes. Uses Starlight/FrankX dark technical language with cyan,
emerald, amber, and proof-green. Avoids generic purple AI gradient and avoids
fake logos.

### Text And Layout

Pass after iteration. Text is deterministic SVG text, not model-generated text.
Two overflow issues were found during PNG inspection and fixed:

- Card 01 guardrail copy was split into two lines.
- Card 03 image-generation rule copy was shortened.
- Card 06 was re-rendered at its native 1800 x 1200 viewport after an initial
  taller screenshot introduced extra whitespace.
- Card 07 initially had two dense labels that overflowed the top cards; labels
  were shortened and re-rendered.
- Card 08 passed inspection as rendered in `visuals/png`.
- Card 09 initially had two top-row label overflows; copy was shortened and
  re-rendered before inspection passed.
- Card 10 passed inspection as rendered in `visuals/png`.
- Card 11 initially had one Slack-route line collision; labels were split into
  three readable columns and re-rendered before inspection passed.

Cards are dense by design because they are internal operating maps. For public
  social, split each into a multi-slide carousel.

Card 11 is suitable for internal Slack proof. Its value is accuracy and routing,
not cinematic public art.

### Accuracy

Pass. Reflects current observed state: Hermes gateway stopped, 7 ready / 4
blocked kanban cards, social approval backlog, and Founder Operating Room pack
ready but not approval-routed.

### Risk

Medium if used publicly without simplification. Low for internal Slack proof.

## 30 Point Score

| Dimension | Score | Note |
| --- | --- | --- |
| First read and hierarchy | 5 | Clear operating titles and section grouping |
| Brand fit and distinctiveness | 4 | Strong enough for internal; public would need richer art direction |
| Craft, typography, spacing, composition | 4 | Dense but readable after overflow fixes; public version should breathe more |
| Accessibility, contrast, surface fit | 5 | High contrast and readable in inspected PNG exports |
| Accuracy, provenance, no artifacts | 5 | Deterministic and current-state grounded |
| Usefulness for intended surface | 5 | Directly useful for Slack/team operations and business-lane routing |
| Total | 28 | Pass for internal proof |

## Verdict

Pass with notes for internal Slack and nightly operations. Do not use as final
public carousel art without splitting and re-composing each card.
