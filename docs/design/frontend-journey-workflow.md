# Frontend, design and journey workflow

Status: Production book slice verified on 7 October. [PR916](https://github.com/frankxai/frankx.ai-vercel-website/pull/916) merged at e3918f37; Vercel is READY on the canonical hosts and all 25 live route/file checks passed. Final candidate d8199493 passed cloud navigation/capture checks and independent source/image review with advisories. Fifteen screens are imported into [FigJam](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw) with source/code mappings. Figma editing/layout remains quota-blocked. Broader design and journey coverage remains open.

The source-only pilot and its observations below are the preserved baseline. Current implementation evidence and remaining release work are in the continuation of the [7 October session](../../ops/sessions/2026-10-07.md).

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

### Rendered failure and Figma upload boundary

CI37565170026 passed the browser installation and retained four actual desktop PNGs at tested merge dbe7baaff63011992adbc9fd4f32d08652309dad, reviewed head5d2fa75. It failed on returning from a chapter to the book. Inspection of the captured chapter and fixed NavigationMega source showed the reader return header under the global navigation. Candidate10b9fc7fdf98d54428ca37c2927f3c9107ba1d15 offsets that header by the existing56px mobile/64px desktop heights. The runner now verifies the real pointer hit target and waits for the previous chapter title. Changed-component lint,14 targeted tests, script syntax, diff and staged secret checks passed. The BookReader detector's existing prose blockquote border is retained as quotation typography, not introduced card styling. CI37565957085 runs this correction; no passing current capture or production release is claimed yet.

Every baseline PNG's SHA256 and VIS sidecar schema passed. Capture ledgers were appended to the existing estate logs without duplicate lines; memory-vault synchronization remains pending. Figma native upload succeeded200 and placed desktop-first-chapter.png on node11:110 in the existing board. The subsequent use_figma annotation/layout operation returned the Starter quota limit. Image import therefore works; editing/layout and read tools remain blocked. The upload is an unannotated historical failure image, not an accepted design or current screenshot. Saved metadata identifies the node and source; no upgrade or quota evasion was attempted. The actual AI review P1 browser-installer finding was explicitly answered with later fix5d2fa75; required Review Gate is now passing. The current local browser admission held at6346MB free versus8192 required; no new local browser/build or agent started.

## Captured book states

CI37567500746 passed all15 actual screens and26 checks. Reviewed sourced8199493, tested mergebb03d341. Native image imports succeeded for every named source/state/viewport PNG. Canvas annotation/layout remains quota-blocked. See current session for release and review scope.

| State | Desktop1440 | Tablet768 | Mobile375, reduced motion |
| --- | --- | --- | --- |
| shelf | [14:110](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-110) | [14:115](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-115) | [14:120](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-120) |
| wordless-laws | [14:111](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-111) | [14:116](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-116) | [14:121](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-121) |
| first-chapter | [14:112](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-112) | [14:117](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-117) | [14:122](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-122) |
| next-chapter | [14:113](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-113) | [14:118](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-118) | [14:123](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-123) |
| pdf-keyboard-focus | [14:114](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-114) | [14:119](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-119) | [14:124](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw?node-id=14-124) |

Screen-to-code references: shelf -> app/books/page.tsx; book detail -> app/books/[bookSlug]/page.tsx; chapter states -> BookReader.tsx and BookChapterNav.tsx; PDF focus -> BookDownloadGate.tsx, BookDownloadLink.tsx and app/api/download/route.ts. These are image-frame references, not Code Connect component mappings or editable webpage capture. Original source and failure diagrams remain preserved.

### Production release and captured journey: 7 October

[PR916](https://github.com/frankxai/frankx.ai-vercel-website/pull/916) merged normally through protected main at `e3918f37b58e9e45c3c28e1609be07dc10f3efd9`. Reviewed source `d8199493492cc5d0ed7a8d99d62dd75f1d08d589`, tested merge `bb03d3412f0541a1fdbc58ab72ece34d955809fe` and production commit have identical Git tree `5a754efc08276369cd4b53aad47a45a87d33afbc`. All eight required PR checks passed; no admin bypass, changed branch protection or fabricated approval. Original PR810 and its branch/history remain preserved.

Production Vercel deployment `dpl_9s2AxfEvWbGQ1iGGQD6TdYMqPMFb` is READY at that main revision and assigned to frankx.ai/www.frankx.ai. At 03:55:57 UTC, all25 public live checks passed: five reading routes200; seven allowlisted direct downloads307 to exact catalog Blob URLs; seven PDF HEADs200 with attachment headers; four restricted/unknown paths404; initial and repeated anonymous attempt307. Public aggregate count moved0→1 once, stayed1 on retry, and stayed1 after DNT/GPC requests. This establishes observed aggregate behavior, not completed transfers or private-event attribution. No email, purchase or visitor record was accessed.

[CI37567500746](https://github.com/frankxai/frankx.ai-vercel-website/actions/runs/37567500746) passed at the final candidate:15 real PNGs,26 journey checks and no capture failures. All hashes, dimensions and VIS sidecars validate. Final independent Anthropic source/all15-image review returned WARN with no confirmed blocker, minimum4839MB free; receipt and every advisory are preserved. The final header reserves global-navigation space and the return link has a44px target. The focused PDF PNG is captured after real Tab navigation and checked for visibility/obstruction. All15 images were imported natively into [FigJam](https://www.figma.com/board/5ycG7mAq4Qk5D7OxXBKrHw), nodes14:110–14:124, with descriptive filenames and source/code mappings. Native images work; read/edit tools are quota-blocked, so layout and annotations were not verified. These image frames do not establish editable webpage capture or Code Connect.

Preserve failed root installer37564426215, four-screen return failure37565170026, five-screen cached304 failure37565957085 and intermediate passing37566659772. Capture ledgers include all39 historical/current PNGs without invented human taste. Memory-vault synchronization remains pending. Impeccable scanned the actual changed UI files; incumbent palette and editorial quotation findings are retained with dispositions. No full premium design approval is claimed.

Remaining work: pre-existing reader typography/duplicate heading, floating music control obstruction, sticky-header ancestor behavior, deterministic lazy-image/scroll capture states, full chapter keyboard coverage, other estate journeys, editable Design capture and token/component synchronization. Main CI37568682090 attempt3 passed at e3918f37b58e9e45c3c28e1609be07dc10f3efd9: 15 PNGs, 26 checks, no failures. Every PNG hash/dimension and VIS sidecar validates. Attempt1 cancellation and attempt2 Chrome mobile-keyboard timeout with14 valid captures remain preserved; cause is unproven and retry success is not a reliability repair. Protected preview passed seven exact redirects/four denials, and production passed25 checks. Issue809 is closed as completed; PR810 is closed as integrated, with branch and author/source history retained. Broader design, capture reliability and journey work stays open on674/706. No session-owned server, browser or reviewer remains running. Private receipts live in the existing `frontend-journey-map-20261007` report. The broad original goal remains active.

## Journey coverage inventory

This is a source-confirmed starting inventory at production tree5a754efc, not exhaustive route coverage. Only the book row has rendered interaction evidence in this slice. Public page availability does not establish form, payment, recovery or accessibility behavior.

| User goal | Entry and destination | Evidence now | Capture and recovery still needed |
| --- | --- | --- | --- |
| Read a book and obtain a free PDF | /books → book → chapter; /api/download | 15 responsive screens, round-trip clicks/touch, PDF Tab/Enter, reduced motion, abort/no-JS, 25 live checks | Full chapter keyboard traversal; prose/widget/sticky repair; settled capture baselines |
| Join and manage the newsletter | /newsletter → /api/subscribe; confirm/thank-you/preferences/unsubscribe | Source routes exist; separate consent preserved by book repair | Fixture-only validation, pending, failure/retry, confirmation and preference states; no live enrollment |
| Discover a product | /products → /products/[slug] and documentation | Source routes exist; catalog used by download checks | Responsive browse/detail/CTA and unavailable-product recovery |
| Buy and recover checkout | /checkout/[slug] → success/cancel; /api/checkout and polar | Source routes exist; restricted direct download denial verified | Provider-approved isolated fixtures, cancel/retry/error and entitlement states; no live purchase |
| Find relevant content | /search and CommandPalette | Source route and global search component exist | Keyboard opening/navigation, results, empty query/no result and close/focus-return |
| Evaluate research | /research → topic/domain/source pages | Source routes exist | Filter/search, citations, empty states, return navigation and mobile reading |
| Contact Frank | /contact → mailto and existing booking destination | Source outbound anchors exist | Responsive/focus checks and destination validation; no message or booking submission |

Extend this inventory through the owning product issue before claiming all journeys. Add role/data state, terminal condition and failure recovery to each capture manifest; keep private/authenticated journeys in an isolated fixture. Maintain the same source/deployment/node linkage across brands while preserving each registered brand pack.

## Keep review and capture costs bounded

Finalize the PR title/body before merging. In this slice, editing the merged PR triggered the existing ci-main concurrency group and canceled the production push run. Retain each run attempt and its actual conclusion. A successful retry does not repair or erase an earlier browser failure.

On a browser protocol timeout, preserve partial PNGs, their provenance and the failure manifest; inspect the failing viewport/command and server output. Use one unchanged-revision rerun to test repeatability. Diagnose a repeated failure before changing timeout limits or input behavior. Keep assertions for real keyboard traversal, pointer reachability and visible focus. Local browser diagnosis still requires machine admission.

The current book pilot runs on every existing CI build. Broader route selection should account for shared navigation, layout and token changes before narrowing captures; always report the required CI context. Keep source/deployment/evidence linked and use the existing Vercel Git integration.
