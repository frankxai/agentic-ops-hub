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

**[F4 · Starlight-Intelligence-System]** — unstrand the reconcile (R4)
```
docs/drift-fixes-2026-05-26 has been unmerged 10+ days holding the 47→54 agent
reconcile + dreaming pipeline. Diff it against main, resolve any drift, and land it
(PR or merge). Confirm agent counts are consistent across CLAUDE.md / GEMINI.md / docs.
```

**[F5 · agentic-ops-hub]** — operationalize this system
```
Run /ops-sweep to refresh the ledger, then sync the 6 open Risk items to Linear
(Arcanea team) as issues linked to the ledger. Schedule a daily morning summary.
```

---

## ⚡ Ops / revenue (non-repo, do directly or delegate)

- **ARC-105** (overdue): request IONOS auth codes for arcanea.ai + realitydiffusion.ai, initiate Vercel transfer.
- **ARC-205**: draft the Founding-50 DM template, pull top-200 engaged FrankX subscribers.
- **ARC-108**: stand up Proton Mail for Business before IONOS WP cancellation kills bundled mail.
