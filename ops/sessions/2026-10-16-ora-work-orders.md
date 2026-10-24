# Ora work orders, 2026-10-16

Scans run this session with `npx ax audit --max-age 86400`. Every line below was served from Ora's cache, so it is a scan from the last 24 hours, not a new force scan. is-agentic.com stores a completed report for frankx.ai only (`https://is-agentic.com/scan/frankx.ai`, score 63, scanned 2026-10-15 18:41). The other domains return 404 from `GET /api/v1/report` until an is-agentic scan is started. is-agentic does not have a write API. Its CLI would spend the same Ora scan budget a second time. Ora's burst limit is 10 scans a minute per IP, and the free daily budget is about 30 scans plus 6 force scans.

Production code was not edited and not deployed. C: was at 70.4 GiB free, 7.4 percent. That is under the 8 percent floor, so a fetch, worktree, install, build, or deploy is refused. `starlightintelligence.ai` local checkout is `agent/hermes/launch-quad-domains` at a 17 Sep 2026 commit. `agentic-ops-hub` local checkout is `agent/hermes/fleet-task-contract-v1` with uncommitted ops files. This file was committed from `origin/main` on its own branch so those trees stay as they are.

## How the team works

One writer per repo. Grok holds the scan ledger and the git lane on this machine. The implementer for a repo is whoever has that repo's primary checkout free, on a branch `agent/<harness>/<scope>` from that repo's `origin/main`. Claude reviews the diff as a buyer. Hermes does not write. eve is not the runner: it is a beta durable-agent runtime and would bill Functions, Workflows, and model calls to read an HTTP score.

Do not add empty WebMCP tools, empty OpenAPI files, or empty SDKs to chase a point value. A check is in scope only when the site already has the thing the check describes.

Order:

1. starlightintelligence.ai. It already has `/api/v1` and `/mcp`. Publish OpenAPI, one JSON error shape, and WebMCP tools that call those existing reads.
2. frankx.ai. Build a real public read API of the product that already exists, then publish the spec. The is-agentic report also wants a markdown body on the real 404.
3. One brand site after that, arcanea.ai or gencreator.ai, and only the homepage text plus a spec for an API that already exists.
4. Every other domain waits. WebMCP showing +9 points is not a reason to register fake tools.

## Scores and the first three fixes

| Domain | Ora | First fixes | Work order |
| --- | --- | --- | --- |
| starlightintelligence.ai | 68 C | openapi-spec +3.9, webmcp +3.3, json-error-responses +2.6 | Write the spec for the live API. JSON errors for unknown `/api/*`. WebMCP for real catalog and install reads. |
| oceanintelligence.app | 63 C | webmcp +13.1, brand-search-accuracy +9.5, ard-catalog +3.2 | Do not edit until ownership is confirmed. The `.ai` name was unverified in the properties registry. |
| starlightintelligence.org | 62 C | webmcp +4.8, agentic-search-specific +4, openapi-spec +4 | Spec only if a public API already exists. |
| starlightintelligence.academy | 62 C | openapi-spec +4, agentic-search-specific +3.7, public-api +3.7 | Same rule. No spec before the API. |
| frankx.ai | 61 C | public-api +5, openapi-spec +3.8, agentic-search-specific +3.7 | is-agentic 63. Essential 45/80. Also: markdown 404, JSON errors, public API docs. |
| starlight.domains | 61 C | webmcp +9.7, mcp-app-registry +7.7, json-ld +3.3 | JSON-LD for the real organization. WebMCP only with a real tool. |
| gencreator.community | 60 C | webmcp +9.7, brand-search-accuracy +9.5, mcp-app-registry +7.7 | Homepage must say what the community is, in server-rendered text. |
| arcanea.academy | 60 C | webmcp +9.7, brand-search-accuracy +9.5, mcp-app-registry +7.7 | Same. Name the school in fetchable text before any tool registry. |
| starlight.technology | 59 C | webmcp +11.7, brand-search-accuracy +9.5, json-ld +3.3 | JSON-LD if the organization is real and public. |
| arcanean.org | 58 C | webmcp +9.7, cli-tool +5.8, rest-sdk-packages +5.8 | Do not publish an SDK or CLI that has no product behind it. |
| arcanea.ai | 56 C | brand-search-accuracy +5.1, openapi-spec +4, agentic-search-specific +3.4 | First viewport states the product. Spec follows an existing API. |
| gencreator.ai | 55 C | brand-search-accuracy +5.1, openapi-spec +4, oauth-support +3.6 | Same. OAuth only if accounts already exist. |
| starlight.you | 52 C | webmcp +9.7, brand-search-accuracy +9.5, mcp-app-registry +7.7 | Fetchable product sentence. No empty tool registry. |
| aiarchitectacademy.com | 51 C | webmcp +8.9, brand-search-accuracy +8.3, rest-sdk-packages +5.3 | No SDK. Fix the page agents can quote. |
| arcanealabs.com | 51 C | webmcp +9.7, brand-search-accuracy +8.3, cli-tool +5.8 | No CLI. Fix the page. |
| arcanea.dev | 50 C | webmcp +9.7, brand-search-accuracy +8.3, cli-tool +5.8 | No CLI. Fix the page. |
| akamoto.io | 49 C | webmcp +9.7, brand-search-accuracy +9.5, mcp-app-registry +7.7 | Fetchable product sentence. |
| vibeclubs.ai | 49 C | brand-search-accuracy +6.1, mcp-server +5.1, webmcp +4.3 | An MCP server only if the product has tools. Otherwise it is a costume. |
| go.agenticincome.ai | 48 C | webmcp +13.1, robots-ai-policy-quality +7.4, agent-friendly-404 +5.2 | Stop blocking agent crawlers if the robots file is the cause. Markdown 404. |
| agenticincome.ai | 46 D | brand-search-accuracy +5.6, openapi-spec +4, webmcp +3.9 | Product sentence, then API, then spec. |
| cecilia.chat | 46 D | brand-search-accuracy +8.3, public-api +6.3, mcp-server +5.4 | Confirm this is a product surface before a public API. |
| realityarchitect.ai | 42 D | brand-search-accuracy +8.3, webmcp +8.2, mcp-app-registry +6.6 | Product sentence. No tool registry yet. |
| agenticpassiveincome.com | 42 D | brand-search-accuracy +5.6, public-api +5.5, openapi-spec +4 | Product sentence, then a real read API. |
| realitydiffusion.ai | 42 D | brand-search-accuracy +8.3, webmcp +8.2, mcp-app-registry +6.6 | Product sentence. |
| bluelifecommons.org | 42 D | public-api +7.8, agentic-search-specific +6.7, webmcp +5.6 | A public read of what the commons actually publishes. |
| animelegends.ai | 39 D | agentic-search-specific +6.1, brand-search-accuracy +6.1, public-api +6 | Product sentence and a discoverable docs or API page. |
| disruptivepassiveincome.com | unreachable | Ora could not reach the domain | Fix DNS or stop listing it. No scan, no code. |

## frankx.ai is-agentic detail

Report: https://is-agentic.com/scan/frankx.ai

Essential 45 of 80 (4 of 8 passing). Recommended 13.5 of 20 (11 of 18 passing). Bonus 4.9 from 21 positive signals. Label: important blockers remain.

The failed essentials called out in the stored report:

- Keep HTTP 404, and return markdown when the client sends `Accept: text/markdown`.
- Publish OpenAPI at `/openapi.json` only after a public API exists.
- JSON error bodies with a code, a message, and a resolution.
- Markdown negotiation on the homepage, with `Vary: Accept`.
- A public REST or GraphQL API.
- API docs at a discoverable path.
- Organization JSON-LD with `contactPoint` and `address` only for facts that are already public.

## What clears the next write

About 6 GiB free on C: reaches the 8 percent line (about 76 GiB). A new worktree still waits until 80 GiB. The first branch is `agent/grok/ora-public-api` from `origin/main` of `frankxai/starlightintelligence.ai`, in the primary checkout once that checkout is not on another harness's branch. Production deploy stays a separate approval after the diff exists and a second seat has reviewed it.

Page speed is not in these scores. That stays on Vercel Speed Insights and Analytics.
