---
id: H-mcp-health
what: Five MCP servers failed at Claude start-up on 17 October; two need an owner change, one needs billing
where: starlight-memory-vault, Prisma plugin config, Langfuse plan, desktop-commander plugin
owner: unassigned
status: open
note: tool plane recovered by its watchdog; desktop-commander connects warm
updated: 2026-10-17
---

## Prompt

Diagnosed read-only on 17 October; nothing was killed or reconfigured.

- `starlight-memory` exits at start: `atoms/starlight-taste-feedback-ledger-index.md` in the memory vault is 251 KB against the
  128 KB per-file limit in `vault-store.mjs`, and it carries uncommitted changes from another lane. Its generator must split or
  cap it; the Codex preservation coordinator already holds an offline three-shard candidate for the oversized index
  (H-preservation). `check-mcp-health.mjs` reports PASS for this server because it only checks that the script exists, so the
  health check fails open: make it send an `initialize` and require a reply.
- `Prisma-Local` never answers: `npx -y prisma mcp` now resolves to `prisma@8.0.0-rc.23` (npm `latest`), which has no `mcp`
  command. Pin the plugin args to the last 7.x that still has it (check `npx -y prisma@7.10.1 mcp --help` first) or disable it
  and keep Prisma-Remote. Synced plugin files may be overwritten by the next sync, so fix it at the plugin source.
- `langfuse` returns 403 "usage threshold exceeded": a plan limit. Upgrade, or remove the project-scoped entry.
- `desktop-commander` timed out on a cold `npx @latest` install (cached since); pin a version or raise `MCP_TIMEOUT`.
- `starlight-tool-plane` was down 16:35 to 16:40 and its `StarlightToolPlaneWatchdog` relaunched it; reconnect in `/mcp`.

The fail-open check is fixed on estate-root branch `agent/claude/mcp-health-handshake` (commit 8dd9ce2, based on
`estate/main` because `tools/check-mcp-health.mjs` is not on `origin/main`; not pushed, since the estate root's write target is
the founder's call). It now performs a real `initialize` over stdio and HTTP; 16 tests, including the old fail-open case.
Its first real run against the registry: starlight-memory FAIL (vault budget), starlight-bridge FAIL (`src/mcp/server.mjs`
missing), starlight-sis FAIL (`mcp-server.mjs` missing), cdp-multiplexer DOWN (nothing on 9223), nano-banana-mcp FAIL (missing
dependency), github FAIL at 15 s and PASS at 60 s (npx cold start; the package is deprecated), starlight-gdrive PASS.
