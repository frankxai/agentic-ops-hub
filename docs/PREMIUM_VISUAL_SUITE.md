# Premium GitHub And Website Infographic System

Date: 2026-06-22

## What changed

The first visual wave gave each repo a clear README header and operating map. This second wave upgrades the estate into an eight-image visual storytelling suite:

- **Ecosystem North Star**: Skills, ops, income, payments, swarm, and assurance connected as one governed system.
- **Repo Constellation**: A grouped map of the estate by capability, operations, income, payments, swarm, and evals.
- **Income Engine Flow**: Research demand, publish useful comparisons, bind the catalog, capture email, and audit every link.
- **Website Growth Loop**: The flagship site, forkable template, passive spoke, awesome list, and skills library feed one loop.
- **Payments Safety Spine**: Mandate verification, spend caps, audit records, and human approval before settlement.
- **Swarm Runtime**: Founder command, queen coordination, worker lanes, escalation, and receipts.
- **Red/Blue Assurance**: Red probes, blue controls, scorecards, receipts, and release gates for income/payment flows.
- **Build / Deploy / Verify**: Branch, local gates, PR, CI, preview, main, and live verification as one disciplined path.

## Design decisions

- Imagegen is used for premium text-free backplates.
- Deterministic SVG renders all text, labels, repo names, arrows, and workflow copy.
- Each repo keeps `assets/github/header.svg` and `assets/github/how-it-works.svg`.
- `visual-suite.json` records which master visuals each repo uses.
- The three Next.js sites receive deployable `public/visuals/*` assets, but live publishing still depends on Vercel project/domain linkage.

## Regeneration

Run from `agentic-ops-hub` inside the clean premium workspace:

```bash
node scripts/generate-premium-visual-suite.mjs
```

The script expects sibling checkouts for all 11 repos.
