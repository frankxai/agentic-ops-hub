# Codex, Claude and Cloud environment alignment

Verified on 11 October 2026. This guide records the current setup and the steps
still needed. It does not claim that every environment or running session adopted
a local configuration change.

| Surface | Verified state | Remaining work |
| --- | --- | --- |
| Codex CLI | 0.162.1; local default GPT-6.1 Sol, xhigh reasoning; 27 active hooks pass native discovery | Desktop event adoption is a separate check |
| Claude Code | 2.1.295; Sonnet 5.5, medium effort; existing user and security-plugin CMD wrappers already repaired | Authenticate the newly registered v0 connection |
| Codex v0 | Authenticated team-wide usage read succeeds | Credit units are not dollars; reconcile costs before generation |
| Claude v0 | Native CLI registered HTTP endpoint; readback says `Needs authentication` | `/mcp`, select v0, authenticate, choose Starlight Intelligence |
| FrankX production | Native Vercel deployment `dpl_2XkWbA4guJnUd4gj15gy5zFpZqL7` is READY at `a95fd12bc50189a8a086bf223170e5b311406919`; project runtime is 22.x | This source does not contain the unpushed Foundry candidate |
| FrankX development | `debc9a895a13c24b6f39a9dd254d2866e26613ef`, branch `agent/codex/foundry-environment-alignment-20261011`, is based on that main revision | Full four gates, rendered QA, exact-revision review, protected PR and live proof |
| Codex Cloud | FrankX environment discovered and three actual jobs reconciled | Correct runtime/network settings before another build attempt |
| Browser control | Inventory contains no connected browser or app | Connect a supported browser before UI-dependent setup or visual QA |

The local Claude registration uses [the official v0 OAuth endpoint](https://v0.app/docs/api/v2/guides/mcp-server).
It preserves all other MCP servers and settings. A native CLI readback confirms
the registration, not authentication. Do not copy OAuth credentials between clients
or put a v0 API key into the MCP configuration. Revert registration through
`claude mcp remove v0 -s user` if needed; preserve newer settings rather than
restoring an entire older config file.

## Runtime and Cloud setup

Use a repository's declared runtime. FrankX CI and its Vercel project use Node 22;
the unpushed candidate corrects its `.nvmrc` from 20 to 22. The official task-scoped
Windows Node 22.23.3 runtime is installed and checksum-verified. Global Node 24.16.0
stays available for repositories that require it. The FrankX package manager is
pnpm 10.28.0.

In the existing FrankX Codex Cloud environment, select Node 22 in package versions.
Use this setup script after that selection:

```bash
set -eu
node -e 'if (Number(process.versions.node.split(".")[0]) !== 22) process.exit(1)'
corepack enable
corepack prepare pnpm@10.28.0 --activate
test "$(pnpm --version)" = "10.28.0"
pnpm install --frozen-lockfile
```

The maintenance script can repeat the runtime/package-manager assertions and
`pnpm install --frozen-lockfile`. A setup script's exports do not persist into the
agent phase. Put persistent variables in environment settings when needed.
Changing setup, maintenance or environment settings affects the cached container;
do not reset a shared cache unnecessarily. These are supported mechanisms described
in [OpenAI's Cloud environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environment).
The script above is prepared guidance and has not been saved into the Cloud UI.

For the actual build, use:

```bash
CI=true pnpm run build
```

Generic CI mode correctly skips the optional private AIS sibling when it is absent.
Do not fabricate `GITHUB_ACTIONS`, remove the pre/post-build steps or count a direct
`next build` as the complete production gate.

The third Cloud worker reported a proxy CONNECT403 for `fonts.gstatic.com`.
The earlier exact-source worker also failed fetching fonts. In Cloud's existing
internet settings, narrowly allow the public build dependencies
`fonts.googleapis.com` and `fonts.gstatic.com`, retaining other restrictions and
certificate verification. Verify the actual change and a real build before calling
it fixed. [Cloud internet settings](https://learn.chatgpt.com/docs/cloud/internet-access)
are separate from local CLI networking. No local config change here applied that
remote setting. A reviewed self-hosted-font change is an alternative product change
if remote network access cannot be configured; preserve the actual brand fonts,
licenses, performance and visual evidence.

## Source handoff and release

The original `a7b0c61b7f71b05d67463ef3a1299b33c114f308` candidate and its branch
remain preserved. The new candidate copies the five unchanged implementation/config
blobs, refreshes its pickup and combines the current reader QA with the Foundry
inspection. Both imports and calls remain. Fourteen source-contract tests, two
syntax checks, diff checks and the enabled commit secret scan pass. These checks
do not replace production build or browser acceptance.

Before returning Cloud work to a repository, bind the immutable base, exact file
list, patch digest and expected Git blobs. Apply only after the existing integration
preflight and ownership checks. The second return matched all seven original blobs;
the third return changed six and was rejected. Never adopt a reconstructed source
because its tests pass. The native Cloud CLI does not expose a documented runtime,
network-setting or model-selection command in this inspected version.

The FrankX v0 chat now names the verified main, production deployment and local
candidate. This was a metadata update with readback, producing no new generation
message. Imported workspace files and older source attachments remain dated;
replace them deliberately before further code generation. Previous static reviews
do not attest the combined `debc9a895` tree.

Keep Vercel's native Git integration as the production deployment owner. Local
Codex, Claude, Cloud jobs and v0 return changes to reviewed Git branches. Do not add
an Actions deploy step or let a v0 study silently deploy over a registered site.
v0 is useful for visual alternatives, responsive prototypes and component studies;
the repository owns integration, recovery, full tests and deployment. Figma remains
optional for shared design libraries and review. Native mobile, desktop and CLI
products require their own engineering and device acceptance beyond a web study.

## Shared configuration and continuation

Registry preflight used reviewed commit
`aeb0253c3009579fefc8cd62e87b261648b162e3`, including
`architecture_agent_credentials_and_tools`. Shared configuration remains owned by
`frankxai/starlight-agent-config`; operational handovers stay in this Hub.
Keep Canvas, SIS and Substrate disabled in base configuration and activate them
only for the task that needs them. Start the native harness in the selected verified
repository so its startup instructions load. A shell `cd` does not rebuild an
already-running session's instruction chain.

Reuse the existing setup repairs rather than installing a second orchestrator:

- [PR112](https://github.com/frankxai/starlight-agent-config/pull/112) has an exact-head Antigravity review and installed hook repair; its required Actions jobs failed before starting because of account budget. It remains unmerged.
- [PR80](https://github.com/frankxai/starlight-agent-config/pull/80) restores missing shared guides; it is draft, conflicts with main and retains an unresolved projection owner. Preserve those gates and reconcile the existing source before adoption.
- [PR108](https://github.com/frankxai/starlight-agent-config/pull/108) extends the existing repository shortcuts; independent provider review and real-provider lifecycle checks remain pending.

At 17:07Z, build admission was HOLD with 3949 MiB free against 8192 MiB required;
27 Codex runtimes were observed. No new local agent, build, browser worker or server
was started. Obtain fresh admission before heavier work. Do not kill other tasks or
archive unfinished work to manufacture admission. The earlier 12-hour design window
has expired and its native goal remains blocked; the new setup request does not
silently resume or complete it.

Continue through [config issue46](https://github.com/frankxai/starlight-agent-config/issues/46),
[FrankX issue339](https://github.com/frankxai/frankx.ai-vercel-website/issues/339) and
[design programme48](https://github.com/frankxai/starlight-design-intelligence/issues/48).
The private setup, source-proof and rollback receipts remain in the existing
`.starlight/workspace-bootstrap/cloud-cli-client-20261011/` directory.
