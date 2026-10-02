# Pull-request recommendations

Across 16 PRs: **0 MERGE / 3 REBASE / 2 CLOSE / 11 ASK FRANK**. All are drafts authored by `frankxai` (`is_bot: false`), including agent-generated work and the automatically opened InfoGenius catcher; there is no Dependabot cluster. The main themes are overlapping canon/brand/product proposals needing owner decisions, useful technical work blocked by conflicts or failing checks, and two abandoned June drafts. No PR meets the non-draft MERGE requirement.

As of **2026-09-16**, using only the supplied JSON. **Age d** means UTC calendar days since creation; inactivity uses `updatedAt`, not creation. Ordered MERGE, REBASE, CLOSE, ASK FRANK, then youngest first. Failure counts include failed check runs and status contexts; skipped, cancelled, neutral, and absent checks are not passes. REBASE includes repairing failing checks even when Git reports MERGEABLE. Human decisions take precedence over technical repair; the explicit 60-day inactivity rule takes precedence for abandoned drafts.

| Repo | PR | Age d | Recommendation | Reason (max 15 words) |
| --- | --- | ---: | --- | --- |
| agentic-creator-os | #54 | 5 | REBASE | Preserve 11-commit InfoGenius skill; CONFLICTING, conflict files unspecified; no checks; founder approval before merge. |
| agentic-creator-os | #53 | 6 | REBASE | Useful portability allowlist; CONFLICTING, conflict files unspecified; one failure: eval-gate; draft pending rebase and CI. |
| arcanea | #124 | 8 | REBASE | Hook fix; three failures: claude-review, Code Quality & Linting, Test & Build Apps. |
| arcanea | #78 | 85 | CLOSE | Abandoned: no update for 85 days; draft, CONFLICTING, five failures despite stated protocol value. |
| arcanea | #75 | 87 | CLOSE | Abandoned: no update for 87 days; Season One draft has three failures. |
| arcanea | #126 | 2 | ASK FRANK | Recent, mergeable validation brief; zero failures, but draft readiness and workflow scope need confirmation. |
| arcanea | #122 | 13 | ASK FRANK | Explicit canon-authority and Starlight naming decisions block this otherwise mergeable draft; zero failures. |
| arcanea | #117 | 19 | ASK FRANK | Editorial brand contract plus CI draft-gating policy; mergeable, zero failures, heavy checks intentionally skipped. |
| arcanea | #116 | 20 | ASK FRANK | Canon, rights, flagship naming require owner approval; CONFLICTING, zero failures; updated 19 days ago. |
| agentic-creator-os | #46 | 25 | ASK FRANK | GenCreator identity requires explicit SOUL.md consent; CONFLICTING, zero failures; updated 24 days ago. |
| arcanea | #104 | 31 | ASK FRANK | Creator must decide Yggdrasil relationship and emblem doctrine; three failures; updated 31 days ago. |
| arcanea | #90 | 43 | ASK FRANK | Transmedia product, staging canon, and asset provenance need approval; CONFLICTING, four failures; idle 40 days. |
| agentic-creator-os | #43 | 61 | ASK FRANK | Useful portability fix remains draft; mergeable, zero failures; idle 38 days; July checks need refreshing. |
| arcanea | #82 | 65 | ASK FRANK | Polar monetization and compliance strategy need owner decisions; two failures; updated 31 days ago. |
| agentic-creator-os | #32 | 66 | ASK FRANK | 1,040-file licensing/product reset removes 254K lines; CONFLICTING, zero failures; updated 18 days ago. |
| arcanea | #76 | 86 | ASK FRANK | New Leviathan canon and game design need approval; CONFLICTING, four failures; updated 18 days ago. |

Arcanea #75, #90, #104, #116, and #122 overlap in story/canon scope, but the JSON does not establish that they are duplicates or superseded. #126 explicitly preserves other work's ownership. #124 says it supersedes #109, which is absent from these lists. The two closures therefore rely on inactivity, not inferred replacement. CONFLICTING identifies branch-level conflicts only; the JSON supplies no conflicting filenames. Body claims about pre-existing failures are not independently verified.

## Do first

1. **agentic-creator-os #32 ? ASK FRANK:** Decide the large reset's scope, prioritizing its reported private-data exposure and licensing issues.
2. **arcanea #122 ? ASK FRANK:** Resolve canon authority and Starlight naming before reconciling overlapping lore proposals.
3. **arcanea #124 ? REBASE:** Repair the three named checks for the narrowly scoped React hook correctness fix.
4. **agentic-creator-os #53 ? REBASE:** Resolve branch conflicts and `eval-gate` to recover the explicit portability allowlist.
5. **arcanea #82 ? ASK FRANK:** Decide the payment strategy and assign follow-up for the compliance work its body reports unshipped.
