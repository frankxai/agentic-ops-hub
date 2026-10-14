# 2026-10-05: GenCreator stack hub, security, team, cross-reviews

Harness: Claude (Opus 5.5) leading four Opus agents and Codex reviewers. All agents ran **locally**:
remote isolation fell back to local worktrees. RAM sat at 2.2–3.4 GB free, under the 4 GiB floor,
so every agent ran under a RAM guard: preflight before anything heavy, no concurrent builds.
Frank's ask: an AI-native social hub plus a stack layer showing creators their choices across Canva,
Figma, HeyGen/HyperFrames and ContentStudio (track, buy, manage), with everything in the right repos,
led end to end.

## Merged

- **starlight-estate #50**, team-forge. Rebuilt clean from `estate/main` because #7 carried 37
  unpushed commits from other sessions (344 files); #7 is closed and its branch kept. It adds
  transactional rollback that reports what it could not restore.
- **gencreator.ai #111**, the 8-seat GenCreator product team.
  - No seat holds both a shell and the open web.
  - Licences for the vendored MIT skills are recorded, with their notices.

## Ready, waiting on gates

- **gencreator.ai #116**, security, in its third Codex round. It is narrowed to the 4 defects still
  exploitable on main:
  - unmetered `/api/ask` and `/api/agents/chat`;
  - the studio-apply relay;
  - the Whop webhook failing open;
  - Whop purchase idempotency.

  It is money-path, so the merge is Frank's (§5e). Migration 002 must be applied before deploy;
  until then every `payment.succeeded` returns 503 and Whop keeps retrying. A Vercel Firewall
  rate-limit rule is recommended.
- **gencreator.ai #158**, the Surface Guard fix. Every PR's Surface Guard fails on an
  unauthenticated `git fetch`. The gates are a locked surface, so this needs Frank's
  `surface-approved` label.

## Built, held behind Codex's #148 (no stacked PR, per AGENTS.md §13)

- **`agent/claude/creator-stack-ui` @ 14b5bbd**: `/creator-studio/stack`.
  - A local-first stack audit: inventory, then keep / cut / consolidate / add / review, each with
    the reason, money effect, evidence date and official link.
  - 20 vendor presets.
  - Consent-gated storage and JSON export.
  - The managed version is a waitlist.
  - Vercel preview READY on 1d3e4ec. Codex buyer-critique fixes are in.
  - 993 tests.
  - Gaps: mobile/768/reduced-motion screenshots (RAM HOLD); the Playwright spec is written but not
    run; the craft receipt is not written; offers are synthetic until the catalog lands.
- **`agent/claude/creator-offer-catalog` @ 9ec6666**: 51 dated, sourced offers across 18 vendors,
  16 explicit gaps and 22 affiliate programmes, plus
  `docs/research/social-hub-landscape-2026-10.md` (14 hubs). Codex fact-check PASS after one
  revision.

## Cross-reviews of Codex PRs (posted on each PR)

- **#148 CreatorStack compiler: REVISE.**
  - P1: one 42 KB request to an unauthenticated route took 75 s of CPU (subset enumeration).
  - P2: owned tools dropped silently; a fake "included" offer wins; self-attested freshness; no
    keep/cut output.
  - Nine catalog schema gaps posted for its owner.
- **#149 director MCP: REVISE.** The agent sets its own spend cap with no host ceiling; recovery
  breaks on a 401 or 422.
- **#139 Postiz reads: PASS.** Blocked only by Surface Guard and #138 plus Frank's approval.

## Strategy the research supports

Every one of the 14 reviewed social hubs is hosted, holds the creator's platform tokens and resells
AI credits. None of them showed an audit of what a creator already pays across tools. GenCreator's
lane is the creator's own agent on their own keys: a dated stack ledger, verified post receipts on
whatever publishing tool they already own, and the free stack audit as first contact. "Buy" means
official links and partner programmes with vendor checkout; managed features stay waitlist-only
(TRUTH §2).

## Open

- **Frank decides:**
  - ADR-013 on #113 (archive the sibling repos or keep them labelled and routed);
  - `surface-approved` on #158;
  - #116 merge, migration 002 and the Firewall rule;
  - #139 approval;
  - promoting the `gencreator-managed-stack` row into the estate `graph/products.graph.json`.
- **#148 and #149:** Codex's owner fixes them; then the UI and catalog rebase onto main as draft PRs.
- **Estate `tools/tests/agent-forge.test.sh`:** fails 10/13 on estate main (a Windows path in its
  Python helper). It predates this session.
- **Firecrawl:** out of credits; the Canva and CapCut price gaps need a browser pass.
