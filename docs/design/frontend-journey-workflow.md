# Frontend, design and journey workflow

Status: proposed operating workflow with one source-backed FrankX pilot. This document is adoption guidance. It installs no agent, synchronization, browser runner or release gate.

## Ownership

Use one technical lead, `nextjs-vercel-deployment`, for a complete journey. Load `ui-ux-design-expert` for journey/design-system decisions; use the existing design, accessibility and performance reviewers at actual review gates. `frankx-website-builder` is available for FrankX-specific work. Do not start every role or one standing agent per website.

GitHub owns source, versioned components/tokens, tests, issues and PR decisions. `frankxai/starlight-design-intelligence` owns the shared design protocol and brand packs. Product repositories consume their own registered pack. Figma Design holds editable screen studies; FigJam holds linked journeys and decisions. Vercel supplies the running revision. The hub holds sanitized handovers.

Resolve portfolio identity from `frankxai/agentic-ops/registry`. This pilot read Registry commit `cf99c95559b741c6ed372c06f1030d2bd731913b`, exclusions, repository/artifact ownership and `design_frankx`. It introduces no new framework authority.

## The pilot

- Product: `frankxai/frankx.ai-vercel-website`.
- Production source: `ca096f3281fae6bb08badaf08928cb7f6ce0281e`.
- Vercel project: `frankx-ai-vercel-website`; READY deployment `dpl_7Qx221ZrojjXyj7kuBjbPjzqzQhA`.
- [Journey and verified failure in FigJam](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw).
- [Existing book delivery issue #809](https://github.com/frankxai/frankx.ai-vercel-website/issues/809).

The journey is `/books` → `/books/the-wordless-laws` → `/invitation` → `/the-one-who-decides`, with previous-chapter and book-return links. All four public page GETs returned 200. These are server-response checks; clicks, layout and hydration have not been verified.

The detail page includes `BookDownloadGate` and email-required copy. GET `https://www.frankx.ai/api/download?product=the-wordless-laws` returned 404 with `{"error":"Product not found"}`. The pinned `data/products.json` has no matching slug. POST uses the same catalog lookup after email validation; its failure is source-derived, and no production POST or email submission was performed. Verify an owned PDF before repairing delivery or promising a download.

The local checkout at `ed4f501` is a different revision on an existing direct-download lane. Its `BookDownloadLink.tsx` is absent from the pinned production source. Preserve the lane; do not report it as deployed.

## Capture and update procedure

1. Select an existing product issue and consequential journey. Define entry point, user goal, success and failure/recovery states.
2. Resolve the exact repository, branch, file owner, Git commit and Vercel deployment. Check routes against that revision. Prefer an existing preview. Never substitute the latest unrelated READY preview.
3. Run machine/storage admission before a local browser or build. Use a supported admitted cloud runner when available; record its revision and inputs. Do not launch a browser on a local HOLD.
4. Read the product's current design tokens and brand pack. Load Emil for interface work. Verify focus, touch, reduced motion and interrupted transitions on the actual UI before a single Impeccable finish.
5. Capture each meaningful state at 375, 768 and 1440 CSS pixels. Preserve natural content, scroll position, role and data fixture. Include loading, empty, validation, error/retry and terminal states where they exist.
6. For a screenshot, save the PNG with route/state/viewport/commit in its metadata. For editable live capture, use `figma_generate_figma_design` in an existing **Figma Design** file. A FigJam board cannot be its capture target. Load the create-file skill if a Design file is needed. Follow the returned injection/poll instructions; this tool was discovered but not run in the pilot.
7. Link the screen frames from the FigJam journey. Record source commit, deployment ID/URL, route, role, state, viewport, timestamp, PNG SHA-256 and Figma file/node IDs. Preserve failure evidence and mark unobserved paths pending.
8. To build or update native design-system components, inspect the existing screens/library references first, discover available libraries and reuse the brand's components and variables. Match names and props to the actual code. A captured layer tree does not establish component-library linkage or automatic synchronization.
9. Review the exact revised artifact. Track fixes in the product issue/PR and save the hub session, ledger and one current pickup prompt. Production promotion follows the repository's release gate.

Your connected Figma account is Starter. Official Code Connect needs Organization or Enterprise and a Full or Dev seat. Begin with a versioned node-to-code mapping; do not upgrade or claim automatic bidirectional synchronization from tool availability.

## Efficient maintenance and reference research

Capture affected journeys on reviewable changes. Keep approved visual baselines in the owning product repository, bounded routine captures in CI artifacts and traces on failure/retry. Reuse existing Vercel git integration; do not add a duplicate deployment workflow. Maintain a coverage inventory before claiming all user journeys.

For established products, code-first capture preserves the existing implementation and exposes discrepancies, as this pilot's missing download did. Figma-first composition is useful for a new or substantially changed journey; it requires implementation and live verification afterwards. Compare the two on the same task using useful output, repair effort, time and recovery.

Use Geist and Primer as documented pattern references. Record the source, observed behavior, abstract principle and brand-specific adaptation. Raw third-party screenshots and HTML stay in the private evidence store under Observatory governance. Preserve distinctive brand tokens, marks, assets and compositions. Borrowing a principle does not grant reuse rights.

Sources: [Figma code to canvas](https://developers.figma.com/docs/figma-mcp-server/code-to-canvas/), [Code Connect requirements](https://developers.figma.com/docs/code-connect/), [Vercel Git integration](https://vercel.com/docs/git), [Playwright screenshots](https://playwright.dev/docs/test-snapshots), [trace viewer](https://playwright.dev/docs/trace-viewer), [Geist](https://vercel.com/geist/introduction), [Primer](https://primer.style/).

## Evidence and remaining work

Figma created the journey and appended the failure diagram to the same board. Exact-commit GitHub reads, Vercel metadata, four route GETs and the failing download GET are verified. Mermaid sidecars validate against the owning VIS schema; generation and workflow/taste records are appended locally.

Local browser preflight held at 4,989 MB free versus 8,192 required, with 55 task runtimes. Disk was about 133 GiB free, BOUNDED under machine policy v1.2. The old design-sight script still reports a stricter disk rule and assumes the Grok harness; that output is discovery evidence, not this Codex session's admission policy.

PNG export hit the secret guard on Figma's signed AWS URL; the unsigned thumbnail returned AccessDenied. No screenshot or visual inspection is claimed. Both diagrams have exact Mermaid/prompt sidecars in the private report `frontend-journey-map-20261007`. Memory-vault synchronization remains pending; no shared memory provider was enabled.

The named skills were read and applied to this bounded source-map workflow. Focus, touch, reduced motion, interrupted transitions, live capture, token synchronization, independent provider/design review and the PDF repair remain pending. No product code, production deployment or standing automation changed.
