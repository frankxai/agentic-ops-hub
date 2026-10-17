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

<!-- handover-index:start -->
| Id | What | Where | Owner | Status |
|---|---|---|---|---|
| [agy-implementation-20261012](handovers/agy-implementation-20261012.md) | AGY: verify the committed operator workflow | prompt below | unknown | open-unverified; not reconciled since the split |
| [autonomous-ops-20261011](handovers/autonomous-ops-20261011.md) | Operations: verify adoption and finish one useful cost or production improvement | prompt below | unknown | open-unverified; not reconciled since the split |
| [claude-queen-second-identity-20261014](handovers/claude-queen-second-identity-20261014.md) | Queen: create the second identity, then make one accepted recoverable task | prompt below | unknown | open-unverified; not reconciled since the split |
| [estate-lifecycle-pulse-1-20261013](handovers/estate-lifecycle-pulse-1-20261013.md) | Run estate pulse #1 against the lifecycle registry | prompt below | unknown | open-unverified; not reconciled since the split |
| [H-2026-10-17-triage](handovers/H-2026-10-17-triage.md) | Restart triage, unified lane map, foundation, swarm, migration, launch prompts | branch `agent/claude/restart-pack-20261017`; local pack in an untracked scratch folder | Claude | processing; split+lint in cbbd3fb; 34 worktree stubs pruned, 4 clean merged worktrees reaped, 182 stale scratch folders archived (receipts in ~/.starlight/operations/cleanup-receipts); restart pack stays in scratch until the founder picks a private home (it holds raw prompts and private paths) |
| [H-ai-team-products](handovers/H-ai-team-products.md) | Free / EUR 1 / EUR 7 AI team product ladder | `agent/codex/product-lifecycle-handover-20261017`; FrankX issue 279, draft PR 280 | Codex | open |
| [H-arcanea-backlog](handovers/H-arcanea-backlog.md) | Arcanea 57-PR backlog triage | local file in an untracked scratch folder | Claude | open; needs relocation |
| [H-asset-intelligence](handovers/H-asset-intelligence.md) | Asset intelligence | `agent/codex/asset-intelligence-handover-20261016` (7 commits unpushed) | Codex | open; not unpushed: local 19b9e19 equals the origin branch; its upstream is wrongly set to origin/main |
| [H-browser](handovers/H-browser.md) | Browser session audit and protection | `agent/codex/browser-session-audit-20261016`, `agent/codex/browser-session-protection-20261016` | Codex | open |
| [H-codemode](handovers/H-codemode.md) | Code-mode seats | `agent/grok/codemode-handover-20261016` | Grok | open |
| [H-estate-consolidation](handovers/H-estate-consolidation.md) | Estate audit, waves, undo receipts | agentic-ops draft PR 273, hub draft PR 357 | Claude | claimed |
| [H-github-org-federation-20261017](handovers/H-github-org-federation-20261017.md) | 10-Org GitHub federation, Sovereign Memory Eval-50 (100% Hit@10), 2h/12h/1w Horizon automation, and Unified HTML5 Agentic Command Center | branches `agent/antigravity/github-org-federation-20261017` (SIS PR #451), `agent/antigravity/org-federation-20261017` (agentic-ops PR #275), `agent/antigravity/org-federation-handover-20261017` (hub PR #362) | Antigravity | open; 10 orgs federated (71/71 repos aligned); Sovereign Memory 1,106 atoms at Hit@10=1.000; 2h/12h/1w Windows Tasks green (Exit 0); Unified HTML5 Command Center & Master Plan shipped |
| [H-infisical-langfuse](handovers/H-infisical-langfuse.md) | Secrets and tracing | `agent/codex/infisical-langfuse-20261016`, `agent/codex/langfuse-native-20261016` | Codex | open |
| [H-marketplace](handovers/H-marketplace.md) | Marketplace budget review | `agent/codex/marketplace-budget-review-20261016` | Codex | open |
| [H-mcp-health](handovers/H-mcp-health.md) | Five MCP servers failed at Claude start-up on 17 October; two need an owner change, one needs billing | starlight-memory-vault, Prisma plugin config, Langfuse plan, desktop-commander plugin | unassigned | open; tool plane recovered by its watchdog; desktop-commander connects warm |
| [H-n8n](handovers/H-n8n.md) | n8n agent architecture | `agent/grok/n8n-agent-architecture-20261016`, `agent/grok/n8n-2437-pin` | Grok | open |
| [H-overnight-lead](handovers/H-overnight-lead.md) | Reviews, gate blocks, queued Queen cards | `queen/inbox`, pull request comments | Claude | processing; partly processed |
| [H-preservation](handovers/H-preservation.md) | Preservation-first restart closure, native checkpoints | branch `agent/codex/memory-architecture-20261016` | Codex | processing |
| [H-product-studio](handovers/H-product-studio.md) | GenCreator Product Studio: master brief of the founder's prompts and vision, a visual start page with concept images, and a restart prompt | Codex session 01a146b1, files untracked in the `frankx-product-lifecycle-20261017` worktree under `docs/strategy/portfolio-productization/weekend-ai-team-20261017/` (START-HERE.html, GENCREATOR-PRODUCT-STUDIO-MASTER-BRIEF.md, RESTART-PROMPT.md, visuals/); images under `cms-dam/assets/gencreator/product-studio-20261017` | Codex | processing; committed and pushed in FrankX af54c12b; 46 remaining dirty files are line-ending noise only |
| [H-queen](handovers/H-queen.md) | Queen cost, demand, native task, recovery | handovers queen-*-2026101x and claude-queen-second-identity-20261014; agentic-ops draft PR 234 | Claude, Codex | open-unverified |
| [H-sis-review](handovers/H-sis-review.md) | Review and merge of SIS PR 406 and 407 | handovers sis-swarm-topology-and-demand-doors-20261014 and sis-executive-and-queen-lifecycle-20261013 | any non-maker | processed; PR 406 merged 6db1f9d and PR 407 merged f07db00 on 2026-10-14 (verified with gh 2026-10-17) |
| [H-startup-coherence](handovers/H-startup-coherence.md) | Make the start-up path name the Registry, lane claim and this index; resolve nine doctrine contradictions | starlight/AGENTS.md, ~/.starlight/workspace-bootstrap (unversioned), starlight/ops contract files | unassigned | open; audited 2026-10-17 read-only; doctrine edits need a non-Claude reviewer |
| [H-turn0-budget](handovers/H-turn0-budget.md) | Turn-0 instructions measured at 50k to 83k tokens per harness against an 8k target; ranked cuts and a generated-core design | ~/.claude, ~/.codex, ~/.gemini plugins, Hermes skill dirs, starlight/AGENTS.md | unassigned | open; measured 2026-10-17 from disk, tokens = bytes/4 (likely 10 to 25 percent low); harness built-in prompts excluded |
| [H-unified-ai-os](handovers/H-unified-ai-os.md) | Unified AI OS | `agent/codex/unified-ai-os-handover-20261016`; content-os draft PR 7 | Codex | open |
| [H-v0-npm](handovers/H-v0-npm.md) | v0 design programme, npm ecosystem and activation | ops/archive/prompts/2026-10-17-next-prompts-legacy.md (marker v0-design-programme-20261011 plus the repeated npm sections) | unknown | open-unverified; likely superseded |
| [H-voice-journey](handovers/H-voice-journey.md) | Voice studio journey | `agent/codex/estate-operating-map-20261016` (hub 3 and agent-config 2 commits unpushed); `agent/codex/voice-studio-journey-20261017` has no upstream | Codex | open; at risk: starlight-command-center agent/codex/voice-studio-journey-20261017 (f345a33, 49 commits) has no upstream; hub estate-operating-map 3880fc0 and agent-config 6c428c1 each 1 unpushed |
| [H-voice-x](handovers/H-voice-x.md) | X-voice and live face | `agent/grok/x-voice-clap` (gate BLOCK at 0334b56); `agent/grok/voice-live-face-handover` | Grok | open |
| [queen-agent-manager-recovery-20261013](handovers/queen-agent-manager-recovery-20261013.md) | Claude: finish Queen recovery and one protected native task | prompt below | unknown | superseded; by queen-bus-live-gaps-20261014; not reconciled since the split |
| [queen-budget-dispatch-20261014](handovers/queen-budget-dispatch-20261014.md) | Continue Queen from budgeted contained dispatch to protected live proof | prompt below | unknown | superseded; by queen-bus-live-gaps-20261014; not reconciled since the split |
| [queen-bus-live-gaps-20261014](handovers/queen-bus-live-gaps-20261014.md) | Resume full Queen goal from verified admission and protected runtime | prompt below | unknown | open-unverified; not reconciled since the split |
| [queen-cost-demand-20261014](handovers/queen-cost-demand-20261014.md) | Continue the active multi-layer Queen, cloud and demand goal | prompt below | unknown | superseded; by queen-bus-live-gaps-20261014; not reconciled since the split |
| [queen-evolution-doctor-20261013](handovers/queen-evolution-doctor-20261013.md) | Continue Queen from verified diagnosis to one protected native result | prompt below | unknown | superseded; by queen-bus-live-gaps-20261014; not reconciled since the split |
| [queen-native-session-20261011](handovers/queen-native-session-20261011.md) | Queen: assemble one accepted recoverable native task | prompt below | unknown | superseded; by queen-bus-live-gaps-20261014; not reconciled since the split |
| [sis-executive-and-queen-lifecycle-20261013](handovers/sis-executive-and-queen-lifecycle-20261013.md) | Starlight: Independent review and sequential merge of PR #406 and PR #407 | prompt below | unknown | processed; not reconciled since the split |
| [sis-swarm-topology-and-demand-doors-20261014](handovers/sis-swarm-topology-and-demand-doors-20261014.md) | Starlight: Independent review, merge of PR #406 / #407, and Demand Reporting Run | prompt below | unknown | open-unverified; not reconciled since the split |
| [starlight-delivery-20261010](handovers/starlight-delivery-20261010.md) | Starlight: review and release Supabase auth, then prove live account activation | prompt below | unknown | open-unverified; not reconciled since the split |
| [v0-design-programme-20261011](handovers/v0-design-programme-20261011.md) | Deliver one accepted agent/Cloud pilot and design slice | prompt below | unknown | open-unverified; not reconciled since the split |
<!-- handover-index:end -->

The table above is generated from `ops/handovers/*.md`; edit those files, then run `node scripts/handover.mjs index`.

## Rules (each gets a command or it is not a rule)

1. Live since 17 October: a new handover is one file `ops/handovers/<id>.md` with frontmatter (id, what, where, owner,
   status, note, supersedes, superseded_by, evidence, updated) and its pickup prompt under `## Prompt`. `NEXT-PROMPTS.md` is a
   generated list that links to those files; nothing is embedded in it.
2. Live since 17 October: `node scripts/handover.mjs new|claim|process|supersede|status|index|lint`. `lint` exits 1 on a stale
   index or prompt list, a `NEXT-PROMPTS.md` section over 60 lines or file over 300 lines, a repeated heading, `processed`
   without evidence, `superseded` without a target, or an id that does not match its file. CI runs it.
3. Proposed: every harness start-up reads `AGENT_START_OVERVIEW.md`, which points here. Test it by starting a fresh session in each harness
   and checking that it names the lane-claim and handover rules before any write.
4. Proposed. Worktrees: register every root in the placement inventory, claim a lane for each live one, and treat an unclaimed dirty tree as
   KEEP. Reap only trees that are clean, merged, bundled and unclaimed. No new top-level folders under the home directory.
5. Proposed. Checkpoints are snapshots (bundle plus a pinned ref), never commits on a shared branch.

## Open decisions for the founder

- Private durable home for raw prompts and the intent ledger: starlight-memory-vault (private, synced) is the recommendation.
- Whether harness-default worktree roots stay (registered) or migrate to one root over time.
- Approval to archive processed prompt sections out of `NEXT-PROMPTS.md` and to prune broken worktree stubs.
