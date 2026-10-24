---
id: docs-platform-live-20261023
what: Attach two DNS records on IONOS, decide repo visibility for frankxai/docs-platform, then registry rows; the platform itself is live and frankx.ai/docs serves FrankX docs on production
where: prompt below
owner: frank
status: open
note: three of five brand hosts live and verified 23 Oct; frankx.ai/docs live and 15/15 e2e verified 24 Oct (PR #1090); the atlas serves on docs-platform-nine.vercel.app
evidence: https://github.com/frankxai/docs-platform/pull/1 ; https://github.com/frankxai/frankx.ai-vercel-website/issues/1091
updated: 2026-10-24
---

## Prompt

The docs platform is live: `https://docs-platform-nine.vercel.app` (atlas) plus `docs.gencreator.ai`,
`docs.akamoto.io` and `docs.starlightintelligence.ai`, all verified serving brand-scoped pages, search and agent
feeds. On 24 October FrankX got its surface too: `https://frankx.ai/docs` (frankx.ai-vercel-website#1090,
squash `98733b04`) proxies the platform's `frankx` brand with markdown negotiation, `.md` suffix, brand-scoped
feeds and search, 15/15 production e2e green. What remains for full coverage:

1. **Frank (DNS):** on the IONOS gateway for `frankx.ai` and `arcanea.ai`, add CNAME `docs.` →
   `cname.vercel-dns.com` (or the record Vercel assigns under the project's Domains tab). Both domains are already
   listed as intended in the project; the two records are all that keeps them from live. Once `docs.frankx.ai`
   serves at the root the /docs-path-mount's one remaining limitation (dynamically loaded route chunks resolve
   against the host's own `/_next/`, declined-with-concurrence in #1090) disappears by itself.
2. **Frank (visibility):** `frankxai/docs-platform` is PRIVATE (`gh repo view` measured 23 Oct) while every docs page
   renders a "View on GitHub" link into it. Either make the repo public — repo visibility is Frank's call, §5e — or
   say so and the link goes to the estate's public mirror instead.
3. **Next agent (registries):** add the `docs-platform` row to `starlight/graph/products.graph.json` (buyer, mustBeat
   from the receipt's Mintlify/Fern/portison research, listType `platform`) and the repo to
   `starlight/ecosystem.json`. Both are estate-root files and stay out of repo lanes until Frank's estate-root push
   ruling.
4. **Next agent (verification after 1):** `curl -H "Host: docs.frankx.ai" https://docs-platform-nine.vercel.app/intro`
   and the same for `docs.arcanea.ai` with `the-gates`; re-check `/sitemap.xml` picks the hosts up (it reads
   `lib/brands.ts`, no deploy needed once DNS resolves).

Links: craft receipt `ops/craft/receipt-20261023.md` in the repo; session records `ops/sessions/2026-10-23.md`
and `ops/sessions/2026-10-24.md` in this hub.
