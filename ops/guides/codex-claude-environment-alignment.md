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

For v0 usage pagination, retain the initial response's exact `start`, `end` and
`limit` when following its returned cursor. A cursor-only request returned409 in
this session; repeating the matching range and page size recovered the next page
and completed reconciliation. Deduplicate event IDs and preserve the largest
observed token-rate estimate per event across snapshots. Stop new generation if
pagination, model pricing or the approved spending allowance cannot be reconciled.
The token-rate estimate and native charged credit units remain separate measures.

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

## Codex Cloud routing, 12 October

Frank clarified that the setup request targets Codex Cloud and that repository work should move there when local RAM is constrained. Use the native Cloud task workflow for code, dependency setup, builds, browser tests and source reviews. Keep Windows runtime integration, local device/asset access and OAuth sign-ins in their owning local/browser surface. This is a dispatch workflow; no new scheduler, automatic RAM hook or always-on queue collector was installed.

The native CLI 0.162.1 account-visible queue was fully paginated at 11:49 UTC: 143 tasks in eight pages across 16 environment labels, with 141 ready and two error states. There were no pending tasks at that snapshot. The full task URLs and metadata are in the existing private source packet's `cloud-alignment-20261012/CLOUD-TASKS.md` and `queue-complete.json`. This is account-visible Cloud history, not proof of access to every chat, archived task or estate account. A ready task means the worker finished; integration/review/merge/deployment remain separate. Historical environment labels include older organization namespaces and do not establish canonical repository ownership.

Native reads now return task IDs and task URLs; environment IDs still return null. Preserve all original tasks and rejected returns. Use the independently verified FrankX environment `68c9ecc423808191a6dcbb75df22d497`; do not guess an environment from a null field or change the saved SIS default.

```powershell
codex cloud list --json --limit 20
codex cloud list --json --limit 20 --cursor <returned-cursor>
codex cloud list --json --limit 20 --env <verified-environment-id>
codex cloud status <task-id>
codex cloud diff <task-id>
codex cloud exec --env <verified-environment-id> --branch main --attempts 1 <source-bound-prompt>
```

Follow each returned cursor until none remains. Preserve the complete receipt, capture time and coverage. The inspected CLI supports list/status/diff/exec/apply; it has no environment-settings editor or documented Cloud model selector. The local configured model does not prove the remote worker's model. Existing account allowance and network/repository/runtime access can still block remote jobs. No purchases are authorized by the user's existing-credit allowance.

A new [FrankX Cloud build repair](https://chatgpt.com/codex/tasks/task_e_6acccc67836c8320aaa10f145b945d71) was submitted once after the inventory. It returned ready with no diff and stopped before the source checkpoint: the worker could not materialize the large conversational patch as a workspace file. It correctly refused to reconstruct the source. It is a new implementation contract to repair font loading and portable browser QA, rather than repeating the previous unchanged build conditions. It pins today's remote main `c8eeb33f57276d6e909858ebea11bf534d02bdc5` and attempted to supply an exact compressed seven-file Git patch from preserved candidate `debc9a895a13c24b6f39a9dd254d2866e26613ef`. The expected source checkpoint tree is `56922bb52122f51d4a096d4d3b1c4ce583747015`. These files are approved repository inputs; no credential or private runtime file was included. The requested file-hash/tree checkpoint was not materialized or verified in Cloud; no checkpoint, diff, build or browser pass exists from that attempt. The original local candidate and three older Cloud attempts remain unchanged.

The job must use Node 22.23.3, pnpm 10.28.0, frozen dependencies and the real `CI=true pnpm run build`. If Google font access is denied, it must repair the eight existing font-loading files with pinned licensed sources, preserving all ten families, weights, styles, CSS variables and latin/latin-ext coverage. Homepage structure/copy/logos stay outside this build-plumbing scope. The existing GitHub-only QA runner guard stays intact; generic Cloud QA must use an honest separate runner. Required product gates remain type-check, lint, strict language audit, full production build, six-width rendered/recovery proof and exact-revision independent review. A separate [accepted-main font/runtime repair](https://chatgpt.com/codex/tasks/task_e_6accd087feec8320b358d5a87b5d4c65) has now been submitted once. It needs no unpublished payload and owns the font-loading/runtime plumbing already present on the verified remote base. It must return real full build and font/browser evidence. The preserved Foundry candidate still needs separate combined-source validation after that repair. Neither task has established a release-ready result.

At 11:56 UTC local build admission was HOLD: 4008 MiB free against 8192 required, with 29 task runtimes. Fresh disk admission was 80.44 GiB/8.45%, above the hard disk floor. Only bounded source reads, text edits and lightweight CLI calls were used locally; no new local build, install, browser worker or parallel agent was started.

Integrate one return at a time. Verify its source task, immutable base, checkpoint/final head and tree, changed paths, patch, runtime/test evidence and browser artifacts. Run the existing integration preflight and obtain a fresh owned lane before applying once. Reject source drift instead of reconstructing it. Reconcile onto the latest accepted main, obtain exact-revision review, then use draft-first PRs and required CI/protection. Cloud builds do not satisfy unrelated Windows execution or failed required GitHub checks. Configuration PR 112 still has failed required checks at its previously inspected head; no protection waiver was used.

Official behavior is documented in [Codex Cloud](https://learn.chatgpt.com/docs/cloud) and [legacy environment setup](https://developers.openai.com/codex/cloud/environments/). The native inspected task surfaces and exact receipts remain the execution evidence.

The full native queue was refreshed from 12:24:43 through 12:24:52 UTC: 145 unique visible tasks across eight pages and 16 environment labels, with one pending, 142 ready and two error states. The pending task was the accepted-main font/runtime repair. The private report retains every native task URL; live pagination is not an atomic snapshot.
