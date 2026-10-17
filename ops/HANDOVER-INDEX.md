# Handover index

One place that says which handovers exist, where each lives, and whether it has been processed. Proposed 17 October 2026 after a
triage found the same facts spread over a 280 KB prompt file, a 519 KB ledger, unmerged branches and untracked scratch folders.
This file is the index only: the narrative stays in `ops/sessions/`, the ledger in `OPS-LEDGER.md`, the current prompt in
`NEXT-PROMPTS.md`. Statuses below are what was read on 17 October, not verified outcomes. `open-unverified` means nobody has
recorded that it was processed.

## Lifecycle

`open` -> `claimed` (a lane claim names the owner) -> `processing` -> `processed` (evidence link: merged PR, receipt or issue
comment) -> `archived`. Side exits: `superseded-by <id>` and `abandoned` (only with the founder's yes). A prompt section whose
handover is `processed` or `superseded` is moved out of `NEXT-PROMPTS.md` into `ops/archive/prompts/` in the same change.

## Where each kind of artifact belongs

| Artifact | Home | Visibility |
|---|---|---|
| Slice narrative | `ops/sessions/YYYY-MM-DD.md` in this hub | public: no private details |
| The one current pickup prompt per slice | `ops/NEXT-PROMPTS.md` | public |
| What changed, in the ledger | `ops/OPS-LEDGER.md` | public |
| This index | `ops/HANDOVER-INDEX.md` | public |
| Founder's own prompts, intent ledger, proposed `reality.md` | a private durable repository (ruling pending; see decisions) | private |
| Machine receipts, snapshots, bundles | `~/.starlight/` private runtime | local |
| Queued work | `queen/inbox` cards with integer priority and a `resultRef` | local |
| Product plans | `product-plans` | private |
| Authority for repositories and artifacts | `agentic-ops/registry` | private |
| Never a home | scratch folders, chat, memory notes, home-level folders | none |

## Measured state, 17 October 2026

- `NEXT-PROMPTS.md`: 2,056 lines, 280 KB, 14 section markers. One heading appears 15 times, a near-identical one 6 times and
  "Earlier prompts retained for provenance" 7 times. No agent can load it within a Turn-0 budget.
- `OPS-LEDGER.md`: 3,191 lines, 519 KB. 27 session files.
- This repository: 75 open pull requests, 67 drafts, budget 10. The primary checkout sits on another harness's branch with
  uncommitted ledger edits; use a separate worktree.
- Local work locations swept: 815 (317 repository folders, 241 under `starlight/worktrees`, 49 repo-local `.worktrees`, 52 Hermes,
  36 Codex, 5 Grok, 78 repo-local `.claude/worktrees`, 23 under `starlight/.claude/worktrees`, 13 in a home-level `copilot-worktrees`
  folder, 1 other). 672 are valid git; 143 have no `.git` inside (79 are plain folders under `repos/`, the rest broken stubs).
- Real unsaved changes (line-ending-only changes excluded): 133. Unpushed commits: 48. Branches with commits and no upstream: 93.
  No commit in 30+ days: 271. Active in the last 3 days: 37.

## Known handovers

| Id | What | Where | Owner | Status |
|---|---|---|---|---|
| H-2026-10-17-triage | Restart triage, unified lane map, foundation, swarm, migration, launch prompts | branch `agent/claude/restart-pack-20261017`; local pack in an untracked scratch folder | Claude | open; pack needs relocation |
| H-preservation | Preservation-first restart closure, native checkpoints | branch `agent/codex/memory-architecture-20261016` | Codex | processing |
| H-ai-team-products | Free / EUR 1 / EUR 7 AI team product ladder | `agent/codex/product-lifecycle-handover-20261017`; FrankX issue 279, draft PR 280 | Codex | open |
| H-product-studio | GenCreator Product Studio: master brief of the founder's prompts and vision, a visual start page with concept images, and a restart prompt | Codex session 01a146b1, files untracked in the `frankx-product-lifecycle-20261017` worktree under `docs/strategy/portfolio-productization/weekend-ai-team-20261017/` (START-HERE.html, GENCREATOR-PRODUCT-STUDIO-MASTER-BRIEF.md, RESTART-PROMPT.md, visuals/); images under `cms-dam/assets/gencreator/product-studio-20261017` | Codex | processing; uncommitted |
| H-voice-journey | Voice studio journey | `agent/codex/estate-operating-map-20261016` (hub 3 and agent-config 2 commits unpushed); `agent/codex/voice-studio-journey-20261017` has no upstream | Codex | open; unpushed |
| H-voice-x | X-voice and live face | `agent/grok/x-voice-clap` (gate BLOCK at 0334b56); `agent/grok/voice-live-face-handover` | Grok | open |
| H-unified-ai-os | Unified AI OS | `agent/codex/unified-ai-os-handover-20261016`; content-os draft PR 7 | Codex | open |
| H-asset-intelligence | Asset intelligence | `agent/codex/asset-intelligence-handover-20261016` (7 commits unpushed) | Codex | open; unpushed |
| H-infisical-langfuse | Secrets and tracing | `agent/codex/infisical-langfuse-20261016`, `agent/codex/langfuse-native-20261016` | Codex | open |
| H-n8n | n8n agent architecture | `agent/grok/n8n-agent-architecture-20261016`, `agent/grok/n8n-2437-pin` | Grok | open |
| H-browser | Browser session audit and protection | `agent/codex/browser-session-audit-20261016`, `agent/codex/browser-session-protection-20261016` | Codex | open |
| H-codemode | Code-mode seats | `agent/grok/codemode-handover-20261016` | Grok | open |
| H-marketplace | Marketplace budget review | `agent/codex/marketplace-budget-review-20261016` | Codex | open |
| H-estate-consolidation | Estate audit, waves, undo receipts | agentic-ops draft PR 273, hub draft PR 357 | Claude | open |
| H-arcanea-backlog | Arcanea 57-PR backlog triage | local file in an untracked scratch folder | Claude | open; needs relocation |
| H-queen | Queen cost, demand, native task, recovery | `NEXT-PROMPTS.md` sections `queen-*` (6), agentic-ops draft PR 234 | Claude, Codex | open-unverified |
| H-sis-review | Review and merge of SIS PR 406 and 407 | `NEXT-PROMPTS.md` sections `sis-*` | any non-maker | open-unverified |
| H-v0-npm | v0 design programme, npm ecosystem and activation | `NEXT-PROMPTS.md` marker `v0-design-programme-20261011` with 28 repeated sections | unknown | open-unverified, likely superseded |
| H-overnight-lead | Reviews, gate blocks, queued Queen cards | `queen/inbox`, pull request comments | Claude | partly processed |

## Proposed rules (each gets a command or it is not a rule)

1. A new handover adds one row here and one file `ops/handovers/<id>.md` with frontmatter (id, scope, repo, branch, owner,
   status, supersedes, evidence). `NEXT-PROMPTS.md` links to it instead of embedding it.
2. `tools/handover.mjs new|claim|process|supersede|index|lint` writes the frontmatter and regenerates this table. `lint` fails
   on a prompt section over 60 lines, a repeated heading, a missing evidence link on `processed`, or an index row with no file.
3. Every harness start-up reads `AGENT_START_OVERVIEW.md`, which points here. Test it by starting a fresh session in each harness
   and checking that it names the lane-claim and handover rules before any write.
4. Worktrees: register every root in the placement inventory, claim a lane for each live one, and treat an unclaimed dirty tree as
   KEEP. Reap only trees that are clean, merged, bundled and unclaimed. No new top-level folders under the home directory.
5. Checkpoints are snapshots (bundle plus a pinned ref), never commits on a shared branch.

## Open decisions for the founder

- Private durable home for raw prompts and the intent ledger: starlight-memory-vault (private, synced) is the recommendation.
- Whether harness-default worktree roots stay (registered) or migrate to one root over time.
- Approval to archive processed prompt sections out of `NEXT-PROMPTS.md` and to prune broken worktree stubs.
