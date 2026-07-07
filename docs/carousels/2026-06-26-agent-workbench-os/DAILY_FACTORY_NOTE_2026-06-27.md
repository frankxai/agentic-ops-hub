# Daily Factory Note: Agent Workbench OS

Run: 2026-06-27
Automation: Starlight Daily Carousel Factory
Decision: improve and route an existing replacement candidate, not create a new
topic.

## Learning Input

Official source signal:

- OpenAI Codex and Codex cloud docs support conservative source context for
  coding-agent workflows.
- Anthropic Claude Code overview supports conservative source context for
  agentic coding workflows.
- No benchmark, ranking, autonomous-public-action, or unsupported product claim
  was added.

Approval/rejection signal:

- `#social-approvals` still has an explicit queue-hygiene rule: decide or
  replace waiting items before adding more live candidates.
- The prior Agentic Coding OS direction is not the model to copy; the V2
  creative standard marks that class of output as rebuild-required unless it
  clears 90/100 social confidence.

Design QA signal:

- Contact sheet and cover preview were inspected again.
- The deck remains deterministic exact text with no generated-image text.
- Visual QA remains 27/30; social-confidence remains 91/100.

Performance signal:

- No published-post metrics were available in the checked Slack signals.

Brand guide signal:

- FrankX / Builder Education should stay direct, mechanism-first, proof-aware,
  and explicit about human approval for irreversible moves.
- The stronger framing is "workbench" rather than "more prompts" or
  Slack-specific operations.

## Decision

Make:

- Treat Agent Workbench OS as the replacement candidate for the waiting revised
  Agentic Coding OS item.
- Route the packet with explicit `APPROVE`, `APPROVE WITH EDITS`, `REVISE`, or
  `HOLD` language.

Cut:

- A net-new carousel topic today.
- Any implication that Slack is the strategy.
- Any claim that public publishing, production deploys, Hermes gateways,
  customer messages, spend, access changes, or domain actions are approved.

Carry forward:

- Intake -> workspace -> truth -> proof -> approval -> learning.
- Agents prepare the work. Humans approve irreversible moves.
- Generated images can support covers and metaphors only; exact text remains
  deterministic.
