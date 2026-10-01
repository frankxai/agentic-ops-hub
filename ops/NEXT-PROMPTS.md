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

> **2026-10-01:** one fleet prompt added at the top. **2026-09-30:** two current prompts. The prompts below them were written in July and were not re-derived.

## Current

**[fleet control plane · agentic-ops + estate]** — land, then grow the queue
```
Read ops/sessions/2026-10-01-fleet-control-plane.md in frankxai/agentic-ops-hub
first, then re-measure every PR it names with gh. Work in this order:
1. Land only through node C:/Users/frank/starlight/tools/pr-gate.mjs
   signoff/merge; the reviewer harness must differ from the author. Never
   force-push or self-merge. hub PR budget is 14 open against 10.
2. Fix the Codex findings on agentic-ops#81, or close it with the evidence.
   Rebase arcanea-ai-app#466 onto main (keep #458's migration).
3. Burn down the ~100-PR estate review load: per repo, land what passes CI and
   an independent review, close superseded or stale drafts with a one-line
   reason, rebase what is still wanted. Report counts before and after.
4. Turn the next 3 provable production defects into chain plans: commit a
   planner-owned *.acceptance.js first, prove it fails today and passes a
   throwaway fix, then queue the plan in starlight/queen/chains/.
Human gates in the session file stay with Frank. Do not kill Hermes processes.
```

**[placement · starlight-agent-config]** — two review notes, fresh branch from `origin/main`
```
PR 51 is already on main as 0ac1d7e. Do not commit in the checkout that is
still on agent/grok/placement-on-main. From origin/main, on a new
agent/grok branch: let the placement tests use a system temp directory, and
make the inventory blocker match the gate when a control-plane worktree
lives outside the control-plane folder. Leave the 127 unmerged branches,
the 16 non-fast-forward mains, repos/.git, and agent/grok/repo-placement-gate
untouched. Do not change enforce_admins on any other repo.
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

**[F0 · gencreator-skills]** — list video-social-studio in the Claude plugin directory
```
Done already: live config on main with tier applied; codex/rova landed and pushed (4fd0383, includes
the control-plane patch). Do not rerun land-rova.ps1 or the patch.
gencreator-skills #5 (license + network disclosure) is merged (466d694). Next: submit at
claude.ai/directory/manage -> Submit new -> Plugin bundle -> frankxai/gencreator-skills, folder
video-social-studio -> Validate -> Submit. Expect a Policy hold (Node MCP server in a subfolder).
claude-skills-library stays unsubmitted until Frank picks a license for its imported skills.
```

**[F0b · starlight-memory R&D]** — make the next memory gain measurable, then win it
```
Read docs/research/memory-rd-brief-2026-10-01.md on starlight-memory main and the session note
ops/sessions/2026-10-01-memory-retrieval-v2.md. Be proactive: run E1 first (grow the real-prompt
held-out set to ~150 by pooled labelling from ~/.starlight/memory/prompts, frozen hash split, Frank
spot-checks 20%), then E2 (Granite embedder; fix the cache key to include the model id first).
Every claim goes through eval/paired.mjs; finish #19 (referee) before citing any benchmark number.
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
