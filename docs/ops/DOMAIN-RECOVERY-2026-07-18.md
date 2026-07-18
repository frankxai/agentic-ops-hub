# Domain Recovery and Design Swarm — 2026-07-18

Scope: Vercel team `starlight-intelligence` and GitHub owner `frankxai`.

## Execution receipt

- Four promoted `codex/launch-frontdoor` deployments were reconciled through merged PRs; all four Vercel production targets now report `READY` from `main`.
- `arcanea.dev`, `arcanean.org`, and `arcanealabs.com` (plus `www`) are attached to `arcanea-domain-portals` and serve distinct verified production surfaces.
- `cecilia.chat` (plus `www`) is attached to `cecilia-chat` and serves the verified bilingual privacy-first surface.
- All four `www` aliases issue verified HTTP 308 redirects to their canonical apex (`arcanea.dev`, `arcanean.org`, `arcanealabs.com`, and `cecilia.chat`) instead of serving duplicate 200 responses.
- Mobile Lighthouse baseline: Arcanea developer/community/labs each scored 100/100/100/100; Cecilia scored 98 performance and 100 accessibility/best-practices/SEO. All four had CLS `0`.
- Arcanea Academy release hardening merged through `frankxai/arcanea-academy#3` at main commit `e055baab`; production deployment `dpl_GbjEsi9KEbW2jomc4rfjpPoCfbo6` is `READY`. Its live 11-route contract, deterministic five-file ZIP, privacy/provenance boundaries, metadata, 404 handling, and security headers passed.
- Arcanea agent-discovery hygiene merged through `frankxai/arcanea-domain-portals#3` at main commit `90b7c323`; production deployment `dpl_gjDJTmXR6i6meiM9QrhpYXHgV3N6` is `READY`. All three apex hosts now serve host-specific, read-only `/agents.md` contracts with Markdown content types.
- Cecilia release hygiene merged through `frankxai/cecilia-chat#2` at main commit `8a388314`; production deployment `dpl_EYUvimvyJ8wBj6Nd8HjcQreHhpys` is `READY`. CSP/HSTS/COOP/CORP and related headers apply to the page, Next assets, `/agents.md`, and `/llms.txt`; the live bilingual reflection and copy flows remained browser-local with zero interaction requests.
- Production path/query probes reconfirmed direct 308 `www`→apex redirects and HTTPS for all four intended `www` aliases after the hygiene deployments.
- The two IONOS-hosted domains below remain blocked on registrar access; their live A and AAAA records and the absence of all three expected IONOS credential variables were rechecked before this document was finalized.

## Acceptance standard

1. Every live domain resolves to the intended Vercel project and GitHub repository.
2. Production aliases are backed by `main`, not a manually promoted feature branch.
3. New surfaces meet responsive, accessibility, performance, metadata, schema, robots, sitemap, `llms.txt`, and factual read-only `agents.md` gates.
4. Design uses restrained Apple/Linear/Vercel principles with brand-specific register; no generic AI gradients or copied trademarks/assets.
5. No force pushes, destructive cleanup, secret exposure, or unverified production changes.

## Swarm lanes

- Drift lane: `ocean-intelligence`, `starlight-intelligence-academy`, `gencreator-community`, `arcanea-academy` — reviewed and elevated from feature deployments through merged PRs.
- Arcanea domain lane: one low-ops host-aware production surface for `arcanea.dev`, `arcanean.org`, and `arcanealabs.com`.
- Cecilia/DNS lane: `cecilia.chat` plus exact IONOS remediation for `aiarchitectacademy.com` and `disruptivepassiveincome.com`.

## Verified DNS remediation

### aiarchitectacademy.com

- Intended Vercel project: `aiarchitectacademy`
- Intended GitHub: `frankxai/ai-architect-academy`, root `redirect-bridge`
- Current external nameservers: IONOS `ui-dns.*`
- Current apex/www A: `217.160.0.152`
- Current apex/www AAAA: `2001:8d8:100f:f000::253`
- Current live state: apex HTTP serves legacy Apache; HTTPS fails.
- Vercel config: `misconfigured=true`
- Exact current Vercel CLI recommendation: set apex `@` A and `www` A to `76.76.21.21`.
- Delete the legacy apex and `www` AAAA records so IPv6 cannot continue reaching IONOS.
- Rollback: restore both A records to `217.160.0.152` and both AAAA records to `2001:8d8:100f:f000::253`.

### disruptivepassiveincome.com

- Intended Vercel project: `dpi-open-core`
- Intended GitHub: `frankxai/dpi`, root `site`
- Current external nameservers: IONOS `ui-dns.*`
- Current apex/www A: `217.160.0.99`
- Current apex/www AAAA: `2001:8d8:100f:f000::226`
- Current live state: Apache/PHP/WordPress, not the GitHub/Vercel build.
- Vercel config: `misconfigured=true`
- Exact current Vercel CLI recommendation: set apex `@` A and `www` A to `76.76.21.21`.
- Delete the legacy apex and `www` AAAA records so IPv6 cannot continue reaching IONOS.
- Rollback: restore both A records to `217.160.0.99` and both AAAA records to `2001:8d8:100f:f000::226`.

For both domains: preserve MX/TXT/CAA and all unrelated records; replace only the four web-hosting records (apex A, apex AAAA, `www` A, `www` AAAA); use TTL `600`; verify DNS over both IPv4 and IPv6, Vercel certificate issuance, apex/www HTTP behavior, and expected page identity; retain the rollback records until acceptance passes. Changing the nameservers wholesale to Vercel is an alternative shown by the CLI, but the four-record cutover is the lower-blast-radius path.

## Human credential boundary

No `IONOS_API_KEY`, `IONOS_TOKEN`, or `IONOS_DNS_API_KEY` is present on this machine. Live IONOS DNS writes require an authenticated IONOS session/API credential and must not be fabricated.

### Smallest remaining human action

1. In IONOS DNS, apply the four-record change under each domain exactly as listed above; do not modify MX, TXT, CAA, nameservers, or unrelated subdomains.
2. Keep the rollback values available and leave TTL at `600` until acceptance passes.
3. Tell the release lead that the records are saved. The release lead must then recheck public A/AAAA with `1.1.1.1`, Vercel domain configuration, TLS, apex/`www` redirects, and page identity before the cutover is declared complete.

Last public-resolver recheck: `1.1.1.1` still returned both legacy IONOS A and AAAA records for all four hosts. `aiarchitectacademy.com` still failed HTTPS; `disruptivepassiveincome.com` still served the legacy origin over both IPv4 and IPv6.
