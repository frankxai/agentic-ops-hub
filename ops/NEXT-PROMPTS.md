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

> **2026-10-01:** two current prompts. The placement review-notes prompt is done (starlight-agent-config PR 75, `9c87802`). The July prompts under "Highest leverage first" were not re-derived. PR 81, still open, inserts two prompts above F1. This file does not copy them.

## Current

**[continuation · cloud, Claude Fable 5.1]** — build the next product slices from the open reviews
```
You are Claude Fable 5.1. Pin model id claude-fable-5-1. If this cloud seat
cannot pin that id, use Claude Opus 5.5 and write the id you actually ran
in the PR. Do not request Mythos 5.1.

Read first, then build. This prompt is not permission to merge the queue.
- https://github.com/frankxai/agentic-ops-hub/pull/83
  ops/sessions/2026-10-01-merge-gates-handover.md
- https://github.com/frankxai/agentic-ops-hub/pull/81
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

Do not merge frankx.ai-vercel-website drafts 724 and 725, Dependabot major
bumps, PR 81, or PR 83 until you have re-read the diff and the checks are
green. PR 83 had an empty check rollup and mergeStateStatus BLOCKED.
Do not merge the 127 unmerged canonical branches, and do not push the 16
local mains that are not a fast-forward of GitHub. Do not batch-merge drafts.

starlightintelligence.ai 5, 8, 9, 11, 12 and arcanea-ai-app 436 are already
merged. Do not revert them. Leave the 2026-10-01 Starlight voice branches:
starlight-agent-config #74, agentic-ops #131, starlightintelligence.ai #68.

Queen cards in queen/inbox/_hold-missing-agent-20260930/ stay held until
each card has an agent and one child repo, and free RAM is at least 4 GiB.
Do not spawn a local model under that floor.

Lab doors stay with Frank. Langfuse sign-in, Vercel CLI sign-in, LiteLLM
private until anonymous model calls are rejected, Railway cap $130 unchanged.
If the estimate climbs through $125, say so. Do not paste keys. Issue 73.

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

**[applied AI lab · Railway and starlight-agent-config]** — finish the human doors, leave main alone
```
The lab is already running on Railway project perceptive-curiosity.
Do not merge starlight-agent-config PR 72 into main. Its base is
agent/grok/repo-placement-gate. Sign in to Langfuse at
https://langfuse-web-production-840d.up.railway.app, create a project
API key, and do not paste it. Then sign the Vercel CLI back in.
Leave LiteLLM private until you say to publish it, and only after
anonymous model calls are rejected. If the Railway estimate climbs
through $125, say so. Do not change the $130 cap. Issue 73 tracks this.
```

## 🥇 Highest leverage first

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
