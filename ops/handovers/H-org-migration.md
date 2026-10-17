---
id: H-org-migration
what: GitHub org migration state, measured 17 October; 63 org copies made today, no transfers, Registry still says frankxai
where: agentic-ops draft PRs 273 (consolidation plan), 275 (org federation registry), 241 (Starlight org launch); hub draft PR 357
owner: unassigned
status: open
note: first decision is Frank's (copies or transfers); every count below came from gh on 2026-10-17 and goes stale fast
updated: 2026-10-17
---

## Prompt

Pick up the GitHub org migration. Start by re-measuring; do not trust the numbers below after 24 hours.

State on 17 October: earlier today the consolidation plan (agentic-ops PR 273) found six orgs empty and proposed leaving
them dormant. A few hours later an Antigravity lane (agentic-ops PR 275, `registry/github_organizations.yaml`, not merged)
created 63 repository copies across nine orgs as a "dual-remote federation": `origin` stays `frankxai/<repo>` so Vercel
and npm OIDC keep working, and a second `org` remote points at `<Org>/<repo>`. Nothing was transferred. The Registry on
agentic-ops main (`registry/repositories.yaml`, 73 unique repos) still names `frankxai` as owner of every entry and does not
know the copies exist.

The copies are already drifting. Of 69 same-name pairs between `frankxai` and an org, 37 have a different default-branch
HEAD. Of today's 63 copies, 31 differ. Nothing keeps them in sync, and Dependabot opened 28 PRs on the copies within hours.

Do these in order:

1. Ask Frank one question: copies or transfers. A copy that takes its own PRs and issues splits a repo's history in two.
   Recommendation: read-only mirrors for now. Turn off Actions, Dependabot, issues and PRs on each copy, add a README
   banner that names the canonical `frankxai` repo, then pilot one real transfer of a low-dependency public repo by the
   Codex crown audit method (`ops/reviews/arcanea-migration-crown-audit-20261010.md`).
2. Once Frank rules, close the 28 Dependabot PRs on the copies and apply the freeze. Reversible; record an undo line per repo.
3. If mirrors stay, write a sync job and a drift check (default-branch SHA per pair) that writes a heartbeat. If not,
   archive the copies. Archiving or deleting is Frank's call.
4. Reconcile the Registry. Either merge PR 275 together with a mirror role per repo in `repositories.yaml`, or close it.
   Resolve the open `conflict_starlight_intelligence_system_duplicates`: there are now three copies of
   `Starlight-Intelligence-System` (frankxai, Arcanea-Labs, Starlight-Intelligence-Systems).
5. Then return to the consolidation waves (section Waves) and the PR backlog.

Human-only, never agent: transfers, repo visibility, deleting or archiving copies, org base permission, billing and
budgets, branch protection, Vercel project rebinding. Agent-doable: Registry and README edits, mirror banners, drift
report, closing bot PRs once the freeze is agreed, CI and Dependabot config PRs, this handover.

Hub is public: name private repos only if the hub already names them; count the rest.

## Measured per owner

Method: `gh repo list <owner> --limit 1000`, `gh search prs --state open --owner <owner> --limit 1000`, `gh api orgs/<org>`.
"Copies" means repos created 2026-10-17 that share a name with a `frankxai` repo (`.github` excluded).

| Owner | Repos | Public | Private | Archived | Pushed 30d | Copies today (private) | Open PRs |
|---|---|---|---|---|---|---|---|
| frankxai | 414 | 214 | 200 | 68 | 292 | n/a | 801 |
| Arcanea-Labs | 13 | 10 | 3 | 0 | 8 | 7 (2) | 7 |
| FrankX-AI | 11 | 9 | 2 | 0 | 10 | 9 (2) | 0 |
| AI-Architect-Academy | 5 | 1 | 4 | 0 | 2 | 1 (1) | 0 |
| oci-ai-architects | 14 | 13 | 1 | 0 | 7 | 0 | 10 |
| Starlight-Intelligence-Systems | 7 | 6 | 1 | 0 | 7 | 6 (1) | 5 |
| Starlight-Intelligence | 11 | 6 | 5 | 0 | 11 | 9 (4) | 23 |
| GenCreator-ai | 9 | 7 | 2 | 0 | 9 | 8 (2) | 6 |
| Life-Commons | 8 | 7 | 1 | 0 | 8 | 7 (1) | 0 |
| AI-Architect-Studio | 8 | 7 | 1 | 0 | 8 | 7 (1) | 0 |
| Agentic-Income | 10 | 8 | 2 | 0 | 10 | 9 (2) | 9 |

Every org: Free plan, one member (frankxai), zero outside collaborators, base permission `read`. The crown audit of
10 October recorded `none` for Arcanea-Labs. With one member nothing is exposed today, but any future member would get
read access to the 16 private copies. Set base permission to `none` before anyone joins (Frank).

Open PRs, top repos by count. frankxai: agentic-ops 81, agentic-ops-hub 79, arcanea-ai-app 57, gencreator.ai 56,
starlight-agent-config 45, frankx.ai-vercel-website 42, Starlight-Intelligence-System 35, starlightintelligence.ai 27,
FrankX 24, claude-code-config 15. Orgs: Starlight-Intelligence/starlight-command-center 21 (org-native, not a copy).
The 60 open org PRs: 28 Dependabot PRs on today's copies, 21 on starlight-command-center, 10 on oci-ai-architects (all
but one from the 5 October reshape), 1 from 2025 on Arcanea-Labs/Arcanea.

Arcanea-Labs counts 8 repos pushed in 30 days, but those are the 7 copies and `.github`, all pushed today. Its original
repos were last pushed on 27 August, so it is still dormant.

## Planned versus actual

| Source | Says | Actual on 2026-10-17 |
|---|---|---|
| Registry main `repositories.yaml` | Owner of record is `frankxai` for all 73 | True. No repo moved. Copies are unregistered |
| Registry conflict list | `Arcanea-Labs/Starlight-Intelligence-System` unresolved | Still unresolved; a third copy now exists in Starlight-Intelligence-Systems |
| PR 273 plan, section Orgs | Six orgs empty, leave dormant | Superseded the same day by the copies |
| PR 275 federation | Nine orgs dual-remote, org copy kept in step | 37 of 69 pairs out of step; no sync job or heartbeat found |
| Crown audit, 10 October | Hold bulk transfers; pilot one public repo | No transfer and no pilot. Bulk copying went around the hold |
| PR 241 (Codex) | Starlight-Intelligence org identity and publishing standards | Open, not merged |

Repos PR 275 assigns to an org, all still canonical at `frankxai` unless noted. Private repos are named only where the hub
already names them:
- Starlight-Intelligence: starlight-agent-config, starlight-memory, starlight-voice, starlight-technology,
  starlight-design-intelligence, starlight-agent-skills, starlight-evals, starlightintelligence.ai, plus 1 more private.
  starlight-command-center already lives there.
- Starlight-Intelligence-Systems: Starlight-Intelligence-System, starlight-research-hub, starlight-knowledge-tree,
  starlight-cosmos-engine, starlight-swarm, starlight-memory-vault.
- Arcanea-Labs: arcanea-ai-app, arcanea-studio, arcanea-ecosystem, arcanea-agent-skills, arcanea-onchain,
  arcanea-orchestrator (archived fork under frankxai), AnimeLegends. `Arcanea` has a different HEAD in each owner.
- GenCreator-ai: gencreator.ai, GenCreator-OS, GenCreator-Studio, agentic-creator-os, creator-skills, creator-launch-os,
  suno-mcp-server, starlight-creator-mcp.
- FrankX-AI: frankx.ai-vercel-website, FrankX, author-os, publishing-house, prompt-library, claude-skills-library,
  mcp-doctor, claude-code-hooks, visual-intelligence.
- AI-Architect-Studio: ai-architect, ai-coe, agentic-architecture-field-guide, awesome-ai-coe,
  awesome-agent-operating-systems, agentic-operating-system-standard, agentic-ops.
- AI-Architect-Academy: ai-architect-academy, starlight-intelligence-academy, plus 2 private (one exists only in the org).
- Agentic-Income: agenticincome, agenticpassiveincome, awesome-agentic-income, agentic-income-skills,
  agentic-income-template, affiliate-agent-skills, awesome-wealth-agent-skills, awesome-investor-agent-skills, GenInvestor.
- Life-Commons: blue-life-commons, dino-life-commons, ocean-intelligence, health-intelligence-system,
  mind-intelligence-systems, family-intelligence-os, family-history-atlas.
- oci-ai-architects: org-primary already. One private name collision with a `frankxai` repo. Reshape PR 1 still open.

Some copies have stars on the `frankxai` side and none on the copy. claude-skills-library has 47 stars, and it is the
estate's one measured traffic source. Never point inbound links at a copy.

## Waves

From PR 273 (`docs/estate/2026-10-17-consolidation/`), checked against live state:

| Wave | Plan | Status | Who |
|---|---|---|---|
| 1 Archive | 6 verified-dead repos | Done: all 6 archived (re-checked) | Done |
| 2 Held archives | 12 plus 6 forks, one decision each | Not started | Frank, one decision per repo |
| 3 Privatize | 46 candidates, cut to 15 | Partly done: 12 private (re-checked), 3 kept public on purpose, 31 not actioned | Frank (visibility) |
| 4 Consolidate clusters | 86-row destination map | Not started, 0 moves | Agent drafts each move PR after Frank confirms the owner |
| 5 PR backlog | 803 open, budget 10 per repo | Not started: 801 under frankxai, 60 in orgs | Agent lands the 10 ready, then closes the 94 pr-closer proposals after a sample check |
| Orgs | Leave dormant | Replaced by the copy federation, see Prompt | Frank rules first |

Before any transfer or archive, PR 273's local audit says to push or deliberately drop unpushed local work first.
Measured then: 120 clones held commits that are on no remote branch.
