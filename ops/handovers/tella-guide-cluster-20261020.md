---
id: tella-guide-cluster-20261020
what: Take the frankx.ai Tella and demo-video guide cluster (PR 1076) from draft to merge
where: frankxai/frankx.ai-vercel-website PR 1076, branch agent/claude/tella-guide-cluster
owner: Frank (merge, first-time publication); any non-Claude harness (review signoff)
status: open
note: preview verified 2026-10-21 except browser-only checks; no GitHub issue
updated: 2026-10-21
---

## State

Draft [PR 1076](https://github.com/frankxai/frankx.ai-vercel-website/pull/1076), head `544983eca`, opened 2026-10-20.
Eight guides under `/guides`, `/go/tella` referral route, `/guide` and `/tella` aliases, a "Demos and video"
category on `/guides`, and `/downloads/demo-video-script-template.md`. Codex critiqued the cluster read-only and
every finding was fixed in `544983eca`. A local `pnpm build` was not run (`pp preflight` hold, CPU 87%); the Vercel
preview build is the full build and it is READY.

No GitHub issue tracks this slice, and none was opened: the PR itself carries the open items below.

## Preview verification, 2026-10-21 (Claude, against `544983eca`)

Preview is behind Vercel Authentication; checked with a temporary share link.

- Pass: all eight guides return 200 with title, one h1, `section#decision-matrix`, an FAQ heading and FAQPage JSON-LD.
- Pass: `/go/tella` 302 to `https://refer.tella.com/frankx`; `/guide` 308 to `/guides`; `/tella` 308 to `/guides/tella-guide`.
- Pass: `/guides` shows "Demos and video" and links all eight guides; the template download returns 200 `text/markdown`.
- Pass: embeds are click-to-load (`components/embeds/UniversalEmbed.tsx`) and load `https://www.youtube.com/embed/<id>`;
  the CSP `frame-src` allows `https://www.youtube.com`. All 18 referenced video IDs return oEmbed 200.
- Not verified: clicking an embed in a real browser, and no horizontal scroll at 375px on the pillar.
  `pp preflight --workload browser-qa` returned HOLD (136 MB free RAM, CPU 87%). Static evidence only: every
  content table sits in an `overflow-x-auto` wrapper.

## Open items (Frank)

1. Merge is Frank's call: first-time publication of a new cluster. Repo was over its PR budget (16 open vs 10).
2. Record one real Tella video for the pillar; the guides make no first-hand usage claim today.
3. Reconcile Tella's two affiliate terms (30% recurring vs $20 per customer) in the Dub dashboard.
4. Confirm or edit the shared disclosure string "I only recommend tools I actually use or have tested" in
   `data/affiliate/programs.json` (renders on `/superpowers`, not on these guides).

## Prompt

Pick up frankx.ai-vercel-website PR 1076 (Tella and demo-video guide cluster). Read this handover first.
1. When `pp preflight --workload browser-qa` allows, open the Vercel preview (get a share link through the Vercel
   MCP `get_access_to_vercel_url`), click one embed on `/guides/tella-guide` and confirm it plays, then set the
   viewport to 375px and confirm `document.documentElement.scrollWidth <= 375` on the pillar.
2. If the head moved past `544983eca`, re-run the checks above against the new head.
3. A harness other than Claude reviews and signs off: `node tools/pr-gate.mjs verify|signoff`.
4. Do not mark ready or merge without Frank: this is a first-time publication.
