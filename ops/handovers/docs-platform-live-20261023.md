---
id: docs-platform-live-20261023
what: Attach two DNS records on IONOS, decide repo visibility for frankxai/docs-platform, then registry rows; the platform itself is live and verified
where: prompt below
owner: frank
status: open
note: three of five brand hosts live and verified 23 Oct; docs-platform-nine.vercel.app serves the atlas
evidence: https://github.com/frankxai/docs-platform/pull/1
updated: 2026-10-23
---

## Prompt

The docs platform is live: `https://docs-platform-nine.vercel.app` (atlas) plus `docs.gencreator.ai`,
`docs.akamoto.io` and `docs.starlightintelligence.ai`, all verified serving brand-scoped pages, search and agent
feeds. What remains for full coverage:

1. **Frank (DNS):** on the IONOS gateway for `frankx.ai` and `arcanea.ai`, add CNAME `docs.` →
   `cname.vercel-dns.com` (or the record Vercel assigns under the project's Domains tab). Both domains are already
   listed as intended in the project; the two records are all that keeps them from live.
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

Links: craft receipt `ops/craft/receipt-20261023.md` in the repo; session record `ops/sessions/2026-10-23.md` in this hub.
