# Estate convergence: one rail, one spine, one drain

Written 21 October 2026 by Claude from three read-only inventories of the 57 repositories attached to this session, a digest
of this hub's records to 19 October, and the Vercel lifecycle snapshot of 13 October (`registry/vercel-projects-2026-10-13.md`).
Frank delegated the five decisions on 21 October ("U suggest"); the recommendations below are now rulings. What was executed
and what still needs Frank's own accounts is in the last section.

## The call

For the next 30 days the estate has one job: **take the first payments through one merchant rail, on the surfaces that
already have pages and prices.** A short list of repositories (the spine) gets agent work. Everything else is frozen: no new
PRs, no new repositories, no new Vercel projects. When CI runners return, agents drain the queue before they build anything
new.

Why this order: the binding constraint is founder minutes (approvals, account setup, review), not agent output. Today every new
agent PR competes for the same minutes as the decisions that would produce revenue. One account setup unblocks more priced
products than any amount of new code.

## What the numbers say

| Signal | Measured | Source |
|---|---|---|
| Vercel projects with revenue (S4/S5) | 0 of 62 | lifecycle snapshot, 13 Oct |
| Priced products that cannot be bought | frankx.ai 15 SKUs all waitlisted; agenticincome 7 SKUs gated on Polar (readiness 503); realityarchitect $39 edition closed; arcanea.ai edition unavailable; gencreator.ai checkout on hold | same snapshot |
| Open PRs, the 57 repos in this session | about 360 (agentic-ops-hub 85, Starlight-Intelligence-System 32, gencreator.ai 30, frankx.ai 23, arcanea-ai-app 22, starlightintelligence.ai 18) | inventories, 21 Oct |
| Open PRs, whole frankxai account | 803 on 17 Oct against a budget of 10 per repository | `sessions/2026-10-17.md` |
| Drafts | about three in four | inventories |
| Harnesses opening PRs | Codex, Claude (plus remote sessions), Grok, Antigravity, Jules, Gemini, Cursor, Copilot | head-ref prefixes |
| One overnight fan-out | the remote session branch `ccr-30cf70e3-tha5nf` holds open drafts in 17 repositories | inventories |
| Unrecorded drains | 119 PRs closed in four repositories since 19 Oct 12:00Z, none in this ledger | digest, live check |
| Merge mechanisms | three: Merge Steward (never live), pr-gate (used), estate-pr-guardian | digest |
| CI | personal-account private repositories blocked by the Actions budget; org budgets hard-stop at $0; jobs fail before any step | `sessions/2026-10-18.md`, CI runs |

The same product exists more than once:

| Cluster | Copies |
|---|---|
| Founder launch engine | #179 and #180 in starlightintelligence.ai (resolved 21 Oct: one engine, #180) |
| Skill libraries | claude-skills-library, starlight-agent-skills, agentic-creator-os |
| Agent runtimes | starlight-swarm, Starlight-Intelligence/starlight-factory, starlight-kernel |
| Income sites | agenticincome, agenticpassiveincome, agentic-income-template |
| Starlight sites | starlightintelligence.org (`site`) and starlightintelligence.ai |
| Ocean | blue-life-commons, ocean-intelligence-system, marine-mcp, marine-agent-skills |
| OCI skills | oci-ai-architect, claude-code-oci-ai-architect-skills, oci-ai-coe-starter-kit, plus copies inside ai-architect-academy |
| Academies | ai-architect-academy, saas-ai-architect-academy |
| Mind | agentic-mind-os, starlight-mind-os-pro, human-mind-intelligence-system |

## Goals, in order

1. **The rail is live (week 1).** One merchant of record for Frank's own digital sales. This unblocks every gated SKU above at
   once. Ruled 21 October: Polar, which the 13 October snapshot already proposes for frankx.ai, agenticincome, realityarchitect
   and the SIS pricing page, and which starlightintelligence.ai#163 already verifies. Polar pays out through Stripe, so the
   Stripe account still needs its business and bank onboarding finished. Stripe Managed Payments was the alternative
   considered. Plain Stripe Checkout or Billing for Frank's own sales was not chosen: it makes the BV the seller of record,
   so it registers and files EU VAT (OSS) and handles US sales tax itself. Stripe still has a role: founders who build with
   the launch factory sell through their own Stripe Payment Link, with their own account as merchant
   (starlightintelligence.ai#180).

   The ruling settles a disagreement in the starlightintelligence.ai records: `docs/ROADMAP.md` says "Settled: Polar", its
   `README.md` names Stripe plus Metronome as the proposed target, and `docs/FOUNDATIONAL_TECH_DECISIONS.md` says Stripe. The
   README and the decisions file still need a docs fix to match. For Starlight's own credits, starlightintelligence.ai#175 is
   the Polar boundary (signed webhooks, idempotent grants on the existing ledger,
   default off). Before it takes money it needs: offers that can grant `starlight.factory` (today only `starlight.curator`,
   so a buyer could not start a factory run), refund revoking the entitlement, a dispute rule, and one sandbox
   purchase-to-run receipt.
2. **First sales on traffic that exists (by 4 November).** frankx.ai Blueprint at $67 and agenticincome as the single store
   (agenticpassiveincome folds into it, as the snapshot proposes). frankx.ai analytics were broken from July until
   frankx.ai-vercel-website#1068; the first week of real numbers decides which offer leads.
3. **Starlight's first customer-validated launch (by 20 November).** The launch factory builds Starlight's own founding-offer
   page, with a `checkout` call to action pointing at a Polar checkout link (starlightintelligence.ai#180 accepts
   `https://buy.polar.sh/polar_cl_<id>` beside founders' Stripe Payment Links since `536f9dd`), and one managed run is
   settled on the budget ledger for a funded tenant. This is the platform bet; it depends on 1.

**Hold** (security, bugs and the named S4 gate only, no new features): gencreator.ai (Companion alpha stays on hold),
arcanea-ai-app (the EUR 99 edition only once a buyer asks), Starlight-Intelligence-System (substrate fixes and the pricing
page's TODO links).

**Freeze** (no agent lanes for 30 days, open PRs parked or closed with a reopen note): the mind, ocean, music and payment
intelligence repositories, the `awesome-*` catalogs, starlight-cosmos-engine, vibe-os, the academies, the OCI skill
repositories, starlight-swarm and starlight-factory.

## The spine: the only repositories agents may open PRs in

| Repository | Why it is on the spine | Cap on open agent PRs |
|---|---|---|
| starlightintelligence.ai | Launch factory, managed runs, the funding boundary | 5 |
| frankx.ai-vercel-website | Audience and the first sale | 5 |
| agenticincome | The single store | 3 |
| realityarchitect | The $39 edition, one switch | 2 |
| Starlight-Intelligence-System | Substrate and pricing page; hold rules | 3 |
| claude-skills-library | Source of the gates every repository installs | 3 |
| agentic-ops-hub | This record; drain only | 3 |
| gencreator.ai, arcanea-ai-app | Hold: security and S4 gate only | 2 each |

Every other repository is read-only to agents until 20 November. A security fix a frozen repository needs goes through the
drain owner, not a new lane: the drain owner may open and merge it, one narrowly scoped PR per fix. The drain owner may also
merge the two cost-cut PRs named below and close PRs on the approved close list.

## Operating rules for the 30 days

- **One drain owner.** One named harness drains at a time and records every close or merge in this ledger the same day. A
  second lane that closes PRs without recording them is stopped.
- **One merge mechanism: pr-gate.** The maker never checks its own head; the checker signs the exact head, and a new commit
  voids the sign-off. Claude-written spine PRs are checked by Codex, Grok or Antigravity and merged by a non-Claude harness or
  Frank. The other two paths are held until 20 November, or earlier if Frank revises this ruling: the Merge Steward docs
  (`docs/MERGE-STEWARD.md` and its rollout) carry a "not in use" banner, and no repository runs `estate-pr-guardian` at
  `ESTATE_AUTONOMY=auto`, whose trivial-tier auto-merge would bypass pr-gate (`docs/ESTATE-OPS-GOVERNANCE.md` says so). The
  variable is a repository setting, so Frank changes it; the drain owner first lists the repositories where it is `auto`.
- **Drafts do not run CI.** Copy gencreator.ai's pattern (drafts defer every job; `ready_for_review` starts them) to each
  spine repository. Three in four PRs are drafts, so this is the largest single cut in Actions minutes. The drain owner may
  open one PR per spine repository for this rule even when that repository is over its cap; it is drain step 1, not new
  work.
- **No new repositories, Vercel projects or cross-repo fan-outs** (one branch opening drafts in many repositories) for 30
  days. The drain owner's draft-CI PRs (one per spine repository) and security-fix PRs are the named exceptions.
- **Budgets hold.** 10 open PRs per repository estate-wide, the caps above on the spine. A repository over budget gets no new
  PR from any harness, with three exceptions, all opened by the drain owner: the draft-CI PR above, a narrowly scoped
  security-fix PR, and in this repository one open ledger PR at a time carrying only the same-day close and merge records.

## The drain, in order

1. Runners first. Frank sets a bounded personal-account Actions budget for one drain month; the Railway `CI_RUNNER` toggle
   drafts are the fallback. No drain step can run CI before this. The first minutes go to the Actions cost cuts already
   drafted (gencreator.ai#253, arcanea-platform#47) and the draft-CI rule above, which merge before any other PR runs CI.
2. Security PRs: Next.js advisory upgrades and the open security fixes in five repositories. The list is not here, because
   some of these repositories are live and private. It is in step 2 of the drain order in Frank's private Claude Docs
   document "Estate convergence: decisions" (https://claude.ai/artifact/Lkmk7X4qBygrq8zh1psFrT, readable only from Frank's
   account). Check that each cited advisory ID exists before merging.
3. Spine PRs in dependency order. For starlightintelligence.ai: #180 (launch factory, now carrying #183 and #187), then #175
   (default-off; its funding fixes land before `STARLIGHT_COMMERCE_ENABLED` is set), then #174 (docs hub) and #177 (import
   integrity). Three PRs wait for Frank, not for the drain:
   - #172 makes the Starlight Kernel the homepage product and publishes `/waitlist` for the first time. It needs Frank's
     `surface-approved` label, the waitlist's KV environment variable on Vercel, and the runtime decision under
     consolidation proposals below, since it presumes the Kernel.
   - #184 adds a Founder AI Lab coaching page at `/founders`. Its waitlist reports `open:false` in production, so it needs
     Frank's yes to offer coaching and the same KV variable.
   - #185 adds `/meet/frank`, `/connect` and the `/c/*` card redirects. It has no READY preview yet (both builds failed the
     homepage film check), and the new cards are not printed until those routes serve in production.
4. Dependabot minor and patch groups in the spine repositories that are not on hold. Hold repositories (gencreator.ai,
   arcanea-ai-app, Starlight-Intelligence-System) and frozen repositories take only security updates until 20 November. Major bumps (TypeScript 7, zod 4, Sentry 11, openai 7) wait for their own PRs.
5. Close, each with a one-line reason and "reopen if still needed": PRs older than 30 days outside the spine, except
   agentic-income-template#8, which was reopened on purpose on 10 September to keep its work; the drafts from
   the `ccr-30cf70e3-tha5nf` fan-out in frozen repositories; duplicate cross-repo pointer and error-boundary PRs. The existing
   pr-closer list (94 proposed closes, in `agentic-ops`) goes first, but only as a pinned snapshot: before closing anything
   from it, the drain owner records its path and commit in the ledger and checks a 10-PR sample. A list generated later is
   a new proposal, not the approved one.
6. Branches: delete a branch only when its PR merged and the branch meets the existing reaper rule (clean, merged, bundled
   and unclaimed). A PR closed without merging keeps its branch, which is what "reopen if still needed" relies on.

## Consolidation proposals (rename and archive, never delete)

The first two rows were ruled on 21 October as archive batch 1 (last section); they need only Frank's archive action in
repository settings, not another yes. Every other row still needs Frank's yes.

| Proposal | Basis |
|---|---|
| Archive `ai-architectures-observatory` | Empty: no commits, no branches |
| Archive `oci-ai-architects/oci-ai-life-sciences` | Unmodified fork; every commit is upstream |
| Fold agenticpassiveincome into agenticincome; keep the domain as a redirect | Snapshot already proposes S6 |
| Fold ocean-intelligence-system's `mcp/` into marine-mcp; remove the mock dashboard figures | Snapshot next action |
| One Starlight site: decide which of starlightintelligence.org and starlightintelligence.ai is the product and which redirects | Snapshot next action, overdue since 20 Oct |
| One skill library: claude-skills-library stays canonical; starlight-agent-skills freezes and points to it | Both are portable SKILL.md libraries; the gates install from claude-skills-library |
| One runtime decision among starlight-swarm, starlight-factory and starlight-kernel | Three runtimes, no receipt that any one runs paid work; needs Frank |
| saas-ai-architect-academy freezes behind ai-architect-academy | Same name and scope |

## Local machine

The restart pack from 17 October already holds the runbook, the at-risk manifest and the reaper rule. Two founder decisions
unblock it: the private home for prompts and intents, and the worktree-root policy. After that, the reaper removes only
worktrees that are clean, merged, bundled and unclaimed, and writes a receipt per removal.

## Decisions, ruled 21 October

| Decision | Ruling | Done | Needs Frank's account |
|---|---|---|---|
| Rail | Polar for Frank's own sales; founders' own Stripe Payment Links for pages the factory builds | Ruling recorded on starlightintelligence.ai#175; Stripe Payment Link and Polar checkout link support in #180 | Polar organization, products and webhook secret; finish Stripe business and bank onboarding for payouts; a Codex cloud environment for starlightintelligence.ai, so Codex can make #175's funding fixes |
| Spine | The table above, until 20 November | Focus window added to this repository's `AGENTS.md` and the handover prompt | None |
| Runners | A bounded personal-account Actions budget for November; the cost cuts are the first PRs to run CI and merge | Ruled; the budget itself is not set yet | Set the budget in GitHub billing; the Railway `CI_RUNNER` toggle drafts (starlightintelligence.ai#147 and its sibling PRs, runners in `railway-ci-runners`) stay the fallback |
| Close sweep | Wave 1: PRs open more than 30 days in frozen repositories, plus two stale starlightintelligence.ai PRs | 11 closed with a reason and the branch kept: nine in frozen repositories, two in starlightintelligence.ai (list in the 21 October session) | The 94-PR pr-closer list lives in `agentic-ops`, which this session cannot read; it is pinned by path and commit in the ledger before use |
| Archive batch 1 | ai-architectures-observatory, oci-ai-architects/oci-ai-life-sciences | Not done: archiving is a human-only action under the federation rules | Archive both in repository settings |
