# ⏭️ Next Prompts — per active front / terminal

> Copy-paste prompts to drop into the terminal sitting in each repo. Keyed by repo (durable) rather than window position. Ordered by leverage. Regenerated each `/ops-sweep`.
>
> **Terminal map** (edit as you reassign windows):
> | Window | Repo | Harness |
> | :--- | :--- | :--- |
> | T1 | `frankx.ai-vercel-website` | _set_ |
> | T2 | `FrankX` | _set_ |
> | T3 | `agentic-creator-os` | _set_ |
> | T4 | `Starlight-Intelligence-System` | _set_ |
> | T5 | `agentic-ops-hub` | _set_ |

---

> **2026-10-01:** three current prompts (fleet control plane added by Claude). Placement review notes are done (starlight-agent-config PR 75, `9c87802`). The Langfuse stack is stopped (this repo PR 86). F0 and F0b, under Highest leverage, came from PR 81, now merged as `977d04a`. The other July prompts were not re-derived.

## Current

**[fleet control plane · agentic-ops + estate]** — land, then grow the queue
```
Read ops/sessions/2026-10-01-fleet-control-plane.md in frankxai/agentic-ops-hub
first, then re-measure every PR it names with gh. Work in this order:
1. Land only through node C:/Users/frank/starlight/tools/pr-gate.mjs
   signoff/merge; the reviewer harness must differ from the author. Never
   force-push or self-merge. hub PR budget is 15 open against 10.
2. agentic-ops#81 (head c9c1a76) and arcanea-ai-app#466 (head 6c4e354) have
   fixes pushed; each needs an exact-head review by a different harness, then
   land. Hub triage table is on agentic-ops-hub#84; close its 5 close-* PRs.
3. Burn down the ~100-PR estate review load: per repo, land what passes CI and
   an independent review, close superseded or stale drafts with a one-line
   reason, rebase what is still wanted. Report counts before and after.
4. Turn the next 3 provable production defects into chain plans: commit a
   planner-owned *.acceptance.js first, prove it fails today and passes a
   throwaway fix, then queue the plan in starlight/queen/chains/.
Human gates in the session file stay with Frank. Do not kill Hermes processes.
```

**[continuation · cloud, Claude Fable 5.1]** — build the next product slices from the open reviews
```
You are Claude Fable 5.1. Pin model id claude-fable-5-1. If this cloud seat
cannot pin that id, use Claude Opus 5.5 and write the id you actually ran
in the PR. Do not request Mythos 5.1.

Read first, then build. This prompt is not permission to merge the queue.
- https://github.com/frankxai/agentic-ops-hub/pull/83
  ops/sessions/2026-10-01-merge-gates-handover.md
- https://github.com/frankxai/agentic-ops-hub/pull/81 merged as 977d04a
- https://github.com/frankxai/agentic-ops-hub/pull/86 Langfuse stop, 3cb34c1
- ops/sessions/2026-10-01.md on this continuation branch

Placement is finished. starlight-agent-config main is squash
9c8780287f472bb1d5568e608722992075c18fe6 (PR 75). This repo's placement
handover is squash 9b04f062359e685f14ddc65451fbcee04833d27e (PR 80).
Do not reopen them. PR 72 merged into agent/grok/repo-placement-gate
(922d94e), not into main. Leave that branch off main.

Use a new branch agent/claude/<scope> from origin/main in a free worktree.
Push with git push origin HEAD:agent/claude/<scope>. Never plain git push.
One writer per worktree.

Leave these checkouts alone:
- agentic-ops-hub primary, agent/hermes/fleet-task-contract-v1, 14f889f
- starlight-agent-config primary, agent/grok/placement-on-main, cb4655e, dirty
- FrankX primary, agent/antigravity/v0-sovereign-creator-engine, 7fe4fde1
- agentic-ops primary, agent/claude/c940-vacation-envelope, 27f18ac
- agent/grok/continue-2026-10-01, agent/grok/placement-review-notes,
  agent/grok/placement-handover-2026-09-30

Do not merge frankx.ai-vercel-website drafts 724 and 725, or Dependabot
major bumps. PR 81 is already merged (977d04a). Leave PR 83 until you have
re-read the diff and the checks are green. PR 83 had an empty check rollup
and mergeStateStatus BLOCKED.
Do not merge the 127 unmerged canonical branches, and do not push the 16
local mains that are not a fast-forward of GitHub. Do not batch-merge drafts.

starlightintelligence.ai 5, 8, 9, 11, 12 and arcanea-ai-app 436 are already
merged. Do not revert them. Leave the 2026-10-01 Starlight voice branches:
starlight-agent-config #74, agentic-ops #131, starlightintelligence.ai #68.

Queen cards in queen/inbox/_hold-missing-agent-20260930/ stay held until
each card has an agent and one child repo, and free RAM is at least 4 GiB.
Do not spawn a local model under that floor.

The Railway Langfuse stack is stopped. Web, worker, Langfuse Postgres, and
ClickHouse were removed on 2026-10-01. Restart policy is NEVER. Disks stayed.
Do not start them. The old health URL returns 404. Create a Langfuse Cloud
project key and do not paste it. LiteLLM stays private until anonymous model
calls are rejected. Do not change the $130 cap. Elasticsearch and Temporal
stay up until Frank names them. Issue 73. Sign the Vercel CLI back in.

Re-query gh before you trust this order. One product at a time. Name the
product you have to beat. After the first draft, one pass whose only job is
quality. A second model reviews the diff. A frankxai review does not count.
Jules cannot approve.

1. frankxai/agentic-ops #116 if the diff still keeps private memory data off
   public surfaces. Run that repo's tests. Land only when green.
2. frankxai/starlightintelligence.ai #66, then the next CLEAN non-draft
   product PR in that repo. Keep drafts as drafts until the spec is on main
   and you have rebased them.
3. Rebase frankxai/gencreator.ai #115 and #117 onto origin/main. Land the
   fail-closed waitlist step after the buyer-route checks pass. Leave #108
   and other major bumps. #130 was UNSTABLE.
4. frankxai/FrankX #239 from a new worktree off origin/main. Do not switch
   the Antigravity primary. Read the diff before merge.
5. After each landed slice, build the buyer-facing gap that PR still leaves,
   in the same repo, on a new branch. Then write the next handover in a free
   agentic-ops-hub worktree: ops/sessions, the top of ops/OPS-LEDGER.md, and
   one prompt here. Do not edit PR 81's branch or PR 83's branch.

starlight-agent-config is the only repo where enforce_admins is off. A green
non-HOLD PR there may be squash-merged with --admin. #32 and #31 are CLEAN
with an empty review and are constitutional doctrine: read them, do not
batch-merge. Do not turn enforce_admins off on any other repo. Elsewhere,
squash without --admin only when the protection rules already allow it.
```

**[applied AI lab · Railway and starlight-agent-config]** — Cloud key and Vercel login, leave the stopped stack down
```
The Railway Langfuse stack is stopped. Langfuse web, the worker, the
Langfuse Postgres, and ClickHouse had their deployments removed on
2026-10-01. Restart policy is NEVER. Disks stayed. Do not start them.
Do not merge starlight-agent-config into origin/main. The record is
c2154ba on agent/grok/repo-placement-gate.

Create a Langfuse Cloud project API key and do not paste it. Do not use
https://langfuse-web-production-840d.up.railway.app. That health URL
returns 404. When the key exists, set LiteLLM success and failure
callbacks to langfuse and set LANGFUSE_HOST to the Cloud URL.

Then sign the Vercel CLI back in. Leave LiteLLM private until you say
to publish it, and only after anonymous model calls are rejected. Do
not change the $130 cap. Elasticsearch and Temporal stay up until you
name them. Issue 73 tracks the Cloud key.
```

## 🥇 Highest leverage first

**[F0c · starlight-command-center]** — make Starlight Home usable by every agent and harness
```
Read docs/starlight-home-plan.md on branch agent/claude/home-feed of frankxai/starlight-command-center
(draft PR #52, issue #53) and build its steps 1-4 in order, one commit each:
1. node ops/home-feed.mjs --commit writes ops/home/feed.json in that private repo, only when content changed.
2. ops/home/state.json written through one rebase-and-retry function.
3. home_feed, home_next, home_mark tools on starlight-tool-plane (127.0.0.1:7317/mcp), harness from x-starlight-agent.
4. Observatory /home reading both files from GitHub, so localhost:4321 and Vercel run the same code.
Never write feed or state into agentic-ops-hub: it is public and the feed names private PRs.
Prove it: Codex and Claude each call home_next and home_mark, and state.json shows both harnesses.
Stop at Frank's gates: Vercel deploy and protection, the read-only GitHub token env var.
```

**[F0 · gencreator-skills]** — list video-social-studio in the Claude plugin directory
```
Done already: live config on main with tier applied; codex/rova landed and pushed (4fd0383, includes
the control-plane patch). Do not rerun land-rova.ps1 or the patch.
gencreator-skills #5 (license + network disclosure) is merged (466d694). Next: submit at
claude.ai/directory/manage -> Submit new -> Plugin bundle -> frankxai/gencreator-skills, folder
video-social-studio -> Validate -> Submit. Expect a Policy hold (Node MCP server in a subfolder).
claude-skills-library stays unsubmitted until Frank picks a license for its imported skills.
```

**[F0a · gencreator.ai]** — take the creator stack hub to production, one landed slice at a time
```
You lead GenCreator to production. Read first: ops/sessions/2026-10-05-gencreator-stack-hub.md (this repo),
gencreator.ai issue #147, PR #148 review + comment, PR #116 go-live comment, starlight TRUTH.md §2, AGENTS.md §5b/5c/5e/13,
~/.starlight/policies/product-outcome-quality.md. Run `pp preflight --workload build`; on HOLD, no local builds:
use GitHub CI + Vercel previews for verification and run only targeted tests locally.

Order. Land each step before starting the next. Never stack a PR on an unmerged branch.
0. Frank gates, as one batched ask at session start:
   - #116: migrations 002 and 001, Firewall rule, merge.
   - #138: surface-approved label.
   - #113: ADR-013 ruling.
   - #139: approval.
   - Promote gencreator-managed-stack into estate graph/products.graph.json.
   Do not wait on them; work the rest.
1. #148 (codex/creator-operations-20261004). If its branch has no commit in the last 24 h, fix it yourself
   (Frank 2026-09-30: any harness may edit; push separate commits, never force). Otherwise post and wait.
   Fixes:
   - P1 CPU blow-up: replace subset enumeration with a bounded greedy or branch-and-bound selection, and lift the
     12-offer cap.
   - A rate limit on /api/creator-operations and /api/mcp.
   - An explicit keep/cut output that flags unused subscriptions.
   - An unlimited-capacity value.
   - Owned tools are never dropped silently.
   - Vendor-checked "included" offers.
   - Server-side freshness against now.
   Then a cross-provider review (Codex or Grok), then pr-gate merge.
2. Rebase agent/claude/creator-offer-catalog and agent/claude/creator-stack-ui onto main.
   - Wire the sourced catalog into the UI OfferSource.
   - Run tests/e2e/creator-stack.spec.ts on mobile and reduced motion, in CI or on a preview.
   - Write queen/reports/craft/gencreator-managed-stack-<date>.md.
   - Have a different provider critique it as a buyer who declined to pay; fix what it finds.
   - Draft PR, then gate, then merge.
   - Verify /creator-studio/stack on production Vercel.
3. #149: a host-owned spend ceiling with a running total; a 401 or 422 marks the job failed, and retry by id is
   allowed. Then review and merge.
4. Social hub v1, as the next build: one creator home that joins the stack audit, Creator Mission (CreatorPack)
   and verified post receipts read from the creator's own Postiz, Buffer or Metricool (#139 reads).
   - BYOK only.
   - No hosted compute and no holding of creator credentials.
   - "Buy" means official and affiliate links with the vendor's own checkout.
   - The managed tier is waitlist-only, with a gift.
5. A monthly catalog refresh as a heartbeat-writing job (staged, off until Frank approves).

Every slice needs:
- research with dated sources;
- a named bar it beats;
- a refinement pass;
- a different-provider critique;
- a craft receipt;
- a draft PR, then pr-gate, then production verification.
Ask reviewers for ONE exhaustive pass. Max 3 parallel builders, one worktree each, under the RAM guard.
Close the session with the hub handover plus a comment on issue #147.
```

**[F0b · starlight-memory R&D]** — make the next memory gain measurable, then win it
```
Read docs/research/memory-rd-brief-2026-10-01.md on starlight-memory main and the session note
ops/sessions/2026-10-01-memory-retrieval-v2.md. Be proactive: run E1 first (grow the real-prompt
held-out set to ~150 by pooled labelling from ~/.starlight/memory/prompts, frozen hash split, Frank
spot-checks 20%), then E2 (Granite embedder; fix the cache key to include the model id first).
Every claim goes through eval/paired.mjs; then run the referee hybrid lane (`node eval/referee/run.mjs --embeddings on`, one run per process) when RAM allows; cite LongMemEval only via receipted scorecards.
```

**[F1 · frankx.ai-vercel-website]** — fixes the broken flywheel (R1/ARC-204)
```
The 28 new articles (Batches A/B/C) have no links to gencreator.ai. Audit every
article published since 2026-06-06, add a contextual GenCreator CoE pivot CTA +
one inline link each, and add a footer nav item. Verify no broken links. This
closes ARC-204 (the broken FrankX→GenCreator flywheel).
```

**[F2 · FrankX]** — resolve branch drift (R3)
```
This repo is on feat/music-intelligence-system but the last 54 commits are content
batches, not music-IS work. Decide: (a) rename branch to content/june-2026 and cut
a fresh feat branch for music intelligence, or (b) merge content to main. Show me
the cleanest path, then execute it. Then summarize what the music-intelligence-system
was actually supposed to deliver so we can resume it.
```

**[F3 · agentic-creator-os]** — land stalled work (R5)
```
feat/workflow-tier has been unmerged since 2026-06-02 with 6 portable workflows +
HITL gates + trajectory memory. List any blockers, run the smoke fixtures, and if
green open a PR to main (or merge). I want the 6 workflows usable from any repo.
```

**[F4 · Starlight-Intelligence-System]** — execute Hero demo assets (R5) and forge extraction
```
We have PR #22 open covering the Web4/Estate Factory delivery and closing the REVISE track. Next: (1) implement the full estate-provision cmd/Steward details, (2) build the Hero demo execution assets (resolving R5), (3) run /sis-forge extraction on Trinity, and (4) set up overnight scheduler loops. Keep highest Frank DNA and "Built on SIP" posture.
```

**[F5 · agentic-ops-hub]** — operationalize this system
```
Run /ops-sweep to refresh the ledger, then sync the 6 open Risk items to Linear
(Arcanea team) as issues linked to the ledger. Schedule a daily morning summary.
```

**[F6 · Arcanea]** — finalize agent-native integration and clean tree
```
We are on the integrate/agent-native-main-2026-06-12 branch. The 13 JPG session captures are stored and synced in the tracker MD. Next: (1) complete the staged fandom/mythology registry additions, (2) reconcile the remaining unstaged edits in book outline/universe classes, (3) verify build and test suites, and (4) merge/PR to main.
```

---

## ⚡ Ops / revenue (non-repo, do directly or delegate)

- **ARC-105** (overdue): request IONOS auth codes for arcanea.ai + realitydiffusion.ai, initiate Vercel transfer.
- **ARC-205**: draft the Founding-50 DM template, pull top-200 engaged FrankX subscribers.
- **ARC-108**: stand up Proton Mail for Business before IONOS WP cancellation kills bundled mail.
