# App Factory — 12-hour + 24-hour token and CLI plan

**Status:** human-approved planning artifact; **does not launch agents**  
**Date:** 2026-08-11  
**Reference product:** **Creator Product Engine** — implemented first in/alongside the GenCreator product family; extract a reusable kit only after delivery evidence.  
**Goal:** produce one beautiful, human-tested, production-shaped primary path—not several half-built generic templates.

## Capacity truth

The estate uses flat-subscription/CLI lanes where possible. Therefore **tokens are not a reliable or enforceable budget unit**. Use named outcomes, exact turn caps, sandbox, timeout, receipt, and provider cost telemetry.

- The current planner declares a **night cap of $40** per unattended window.
- Claude supports hard `--max-budget-usd` and `--max-turns` controls.
- Codex's dollar figure is an **envelope**, not a hard CLI enforcement; use exact repo, `workspace-write`, named model, timeout, acceptance commands, and a sequential watchdog.
- Do not assume a CLI is ready from installation. `grok`, Claude, Codex, OpenCode, Gemini and Hermes are installed, but every lane needs one minimal live inference/auth probe immediately before assignment.
- This chat is running **OpenAI Codex `gpt-5.6-terra`**. The historical Hermes/Grok routing is not a live xAI-capacity guarantee; xAI must be probed and was previously credit-blocked for X search.

## Allocation summary

| Window | Hermes | Claude Code | Codex | Gemini | OpenCode | Declared metered/telemetry envelope |
|---|---:|---:|---:|---:|---:|---:|
| First 12h | 8 orchestration turns | max 20 turns / **$20 hard cap** | max 14 turns / **$15 envelope** | 1 readiness probe only | ≤10 low-stakes turns | **$35** |
| Hours 12–24 (only if gate passes) | 8 orchestration turns | max 15 turns / **$15 hard cap** | max 20 turns / **$20 envelope** | max 5 turns / **$5 envelope** | ≤10 low-stakes turns | **$40** |
| 24h total maximum | 16 turns | 35 turns / $35 hard cap | 34 turns / $35 envelope | 6 turns / $5 envelope | 20 turns free lane | **$75 across two separate windows** |

`$75` is not a charge forecast and not a license to burn tokens. The first window must produce verified artifacts before the second is allocated. No more than **one heavy coding CLI at a time on C940**.

## CLI roles — use every lane only where it has a comparative advantage

| CLI / lane | Role in this plan | Exact rule |
|---|---|---|
| **Hermes / Terra** | product lead, orchestration, gates, receipt synthesis | no unbounded code-writing loop; maintain brief/decision log |
| **Claude Code Sonnet** | architecture, difficult multi-file implementation, tests | `--max-budget-usd 20`, max 20 turns first window; worktree only |
| **Codex `gpt-5.6-terra`** | UI implementation, component assembly, mechanical fixes, verification | `workspace-write`, exact `-C`, named model/reasoning, timeout; no `danger-full-access` |
| **Gemini 3.5** | one bounded large-context architecture/reference survey, only if live-ready | no build ownership; it produces a concise map with source paths |
| **Grok Build / Imagine** | visual concepts/hero asset only after brand/design contract | live auth probe first; no generated UI chrome; no spend if quota fails |
| **OpenCode** | low-risk docs/test-case/metadata candidates | no production security, billing, auth or store compliance decisions |
| **`gh` / Playwright / package scripts** | deterministic repository, test, screenshot, and CI receipts | no LLM substitutes for tool evidence |

## Product boundary for this 24-hour cycle

### Build now

A **reference Creator Product Engine primary path**:

```text
Landing / value clarity
  → short creator-product diagnosis
    → recommended launch path
      → structured project brief
        → visible next action / saved artifact
```

Required UX patterns: `P-JOB-01` single-job home, `P-JOB-02` 3-step wizard, `P-EMPTY-01`, `P-ERR-01`, `P-A11Y-01`, `P-MOTION-01`.

### Explicitly not in this cycle

- broad agent marketplace
- full autonomous publishing
- payments/checkout implementation
- store submission
- multi-tenant SaaS admin
- an abstract starter-template platform
- client data integrations

The reusable app kit is **extracted after** this reference path has passed persona tests and screenshot evidence. This prevents selling a blank template disguised as a product.

---

# Window A — next 12 hours

## A0 · readiness and no-token preflight (0:00–0:40)

**Owner:** Hermes + deterministic CLIs  
**Budget:** none / one-turn probes only after system resource gate

1. Confirm exact product repo and dedicated worktree; do not edit a dirty shared tree.
2. Inspect `AGENTS.md`, `CLAUDE.md`, design/taste docs, existing routes/components, package scripts.
3. Check disk/RAM and repository status.
4. Run **one minimal live model probe** per candidate lane:
   - Claude read-only/plan probe
   - Codex read-only probe with `gpt-5.6-terra`
   - Gemini optional one-turn probe
   - Grok only if an image concept is required
5. If probe/auth fails, reassign **once**; do not retry-loop or silently fall back to a metered key.

**Receipts:** chosen repo/worktree, CLI readiness matrix, source paths, baseline test command.  
**Stop:** dirty owner worktree, disk below 50GB operations floor, or no bounded sandbox.

## A1 · commercial and human gate (0:40–2:00)

**Owner:** Hermes/Terra, optional Gemini survey  
**Budget:** Hermes ≤4 turns; Gemini ≤1 probe + ≤5 turns only if live-ready.

1. Copy/complete `VERTICAL-WEDGE`, `PRODUCT-BRIEF`, `PERSONA`, and `GSTACK-RUN` in the product repo.
2. Define primary persona: expert/creator with knowledge but no repeatable product-launch path.
3. Define one 60-second job and the v1 outcome.
4. Design contract: desktop/mobile layouts, exact copy, empty/error/loading states, typography/tokens, 5 pattern IDs max.
5. Decide **GO / PIVOT / KILL** before code.

**Acceptance:** no vague “AI assistant”; one primary CTA and a measurable primary job.

## A2 · design and template composition (2:00–3:30)

**Owner:** Codex/Terra (or Grok visual concept only if ready)  
**Budget:** Codex ≤4 turns; Grok ≤2 concept iterations only if the visual need is contractual.

1. Reuse the product’s existing design system.
2. Compose shadcn/Radix + Lucide primitives into the journey.
3. Create component/page inventory, states, responsive rules, and real draft content.
4. If needed, create **one** Grok Imagine marketing/atmospheric asset; exclude it from functional UI.
5. Capture a static reference frame before implementation.

**Acceptance:** structure, interactions, and states are understood without a model-generated mockup.

## A3 · primary-path implementation (3:30–8:00)

**Owner:** Codex/Terra + Claude sequentially—not concurrently on one heavy node  
**Budget:** Codex ≤10 turns / $12 envelope; Claude ≤12 turns / $15 hard cap.

1. Codex scaffolds/implements the primary journey in its isolated worktree.
2. Claude handles only hard cross-file state, validation, accessibility, or test gaps surfaced by Codex—not a rewrite.
3. Add deterministic tests before polish where feasible.
4. Implement explicit loading, empty, error, keyboard and mobile states.

**Acceptance commands:** repo-defined lint, typecheck, targeted tests, production build where practical.

## A4 · independent quality pass (8:00–10:00)

**Owner:** Claude or Codex reviewer—different implementer family  
**Budget:** Claude ≤8 turns / remaining $5 hard cap; Codex ≤2 review turns if Claude implemented.

Review only:

- primary job completion
- broken/ambiguous states
- mobile 390px and desktop 1280px
- accessible heading/focus/form errors
- AI-slop/density/CTA critique
- security/truth claims

**Acceptance:** prioritized P0/P1 list with fixes applied or explicit hold.

## A5 · evidence, integration, and decision (10:00–12:00)

**Owner:** Hermes + deterministic QA  
**Budget:** Hermes ≤4 turns; OpenCode ≤10 low-risk turns only for test-case/documentation candidates.

1. Run full relevant commands.
2. Capture screenshot pack to the product repo under `docs/evidence/YYYY-MM-DD/`.
3. Fill human persona test scorecard.
4. Commit only scoped work; do not merge/ship production automatically.
5. Write `EMPIRE-DECISION.md`: **proceed / pivot / hold**.

**Window A pass gate:**

- primary path works locally/preview;
- no P0; persona score ≥8/10 or specific repair list;
- screenshots exist;
- scoped commit + test receipts exist;
- at least 70% is visibly reusable as a future kit module.

---

# Window B — hours 12–24 (only after Window A PASS)

## B1 · extract the reusable template seam (12:00–15:00)

**Owner:** Claude Sonnet  
**Budget:** max 15 turns / $15 hard cap.

Extract only proven common pieces:

- project brief schema
- journey state machine
- design tokens/component boundaries
- persona test fixture
- screenshot/evidence scripts
- agent policy/receipt UI patterns

**Do not** publish a generic starter yet. First make the reference product stronger.

## B2 · polish, performance, mobile (15:00–18:00)

**Owner:** Codex/Terra  
**Budget:** max 12 turns / $12 envelope.

- polish only after all states work;
- test 390 / 768 / 1280;
- performance and focus checks;
- reduce motion behavior;
- eliminate generic component-grid visuals.

## B3 · Expo/store feasibility spike (18:00–20:30)

**Owner:** Codex/Terra, optional Gemini survey  
**Budget:** Codex max 8 turns / $8 envelope; Gemini max 5 turns / $5 envelope only if live-ready.

Do not build full iOS/Android app. Decide whether the validated path belongs in:

- web-first Next product;
- Expo shared shell;
- native-only surface.

Create a documented decision with store-policy/data/AI disclosure requirements and the smallest viable Expo screen if mobile is justified.

## B4 · adversarial QA and commercial asset (20:30–22:30)

**Owner:** alternate model-family reviewer + Hermes  
**Budget:** no new heavy implementation unless a P0; Hermes ≤4 turns.

- run persona test script;
- check claims, permissions, agent boundaries;
- package one "proof" page or demo walkthrough;
- update Outcome Kit checklist—not a public checkout.

## B5 · morning / 24-hour debrief (22:30–24:00)

**Owner:** Hermes + deterministic CLI  
**Budget:** Hermes ≤4 turns.

Return a receipt with:

```text
CREATED: files / preview / branch
VERIFIED: command results, screenshots, persona score
DELIVERED: commit / PR / integration state
SPEND: declared vs observed telemetry (unknown is null, never zero)
DECISION: next 7-day mission or kill/pivot
```

## Do-not-launch conditions

Do not launch unattended tasks if any of these are true:

- no selected product repo/worktree;
- CLI inference/auth probe fails;
- resource gates fail;
- previous mission has an unreviewed, unintegrated outcome;
- prompt requires main push, production deploy, payment/store publication, destructive cleanup, or credential access;
- external app-store credentials/permissions dialog appears.

## Exact handoff prompt for the first execution window

```text
Load app-factory-pipeline, estate-design-excellence, and starlight-token-planner.

Reference product: Creator Product Engine.
Repo: {{confirmed dedicated worktree}}.
Outcome: an expert/creator completes a short diagnosis and receives a structured,
saved product-launch brief with one visible next action.

Execute Window A from:
docs/digital-product-empire/08-APP-FACTORY-12H-24H-TOKEN-AND-CLI-PLAN.md

Hard rules:
- preflight exact model/auth, repo/worktree, disk/RAM and sandbox before coding;
- work only in the assigned worktree; no main push, force-push, reset, deploy,
  store submission, credentials, payments, or unbounded external agent actions;
- use current product design docs and ≤5 App Factory pattern IDs;
- exact UI in components; Grok Imagine only for one optional atmospheric asset;
- provide CREATED, VERIFIED, DELIVERED, test receipts, screenshot paths,
  declared/observed spend and GO/PIVOT/HOLD decision.
```
