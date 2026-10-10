# GenCreator capabilities and release status

Observation: 11 October 2026. The portable CLI release is verified in production.
Managed accounts, native apps and the wider adoption programme remain unfinished.

## Who the first workflow serves

An author, educator, speaker or founder brings an essay, interview or other source
they have permission to use. They want the argument and voice to survive when
they turn it into a newsletter, social draft or presentation. They need editable
work with its source and decisions available for later review.

| Capability | Workflow and benefit | Evidence and limits |
| --- | --- | --- |
| Creator Studio | Work from permitted source, inspect and edit drafts, and export a local project for continued work and recovery. | Public production verified, with 22 HTTP/protocol smoke checks passing. Real creator acceptance of the full managed journey remains open. |
| Public MCP transforms | An assistant supplies source/project data to compile, prepare revision, preview edits and apply a selection. The host writes the content; GenCreator performs stateless transformations. | Accepted engine through PR200; deployed discovery, protocol, compile and peer-feedback checks pass. These calls establish neither managed inference nor authenticated human approval. |
| Plugin and revision CLI 0.5.3 | Retain a source-bound request, inspect host-written proposals, selectively apply edits and verify a new checkpoint. Original files and unrelated drafts survive. | [PR201](https://github.com/frankxai/gencreator.ai/pull/201) merged as `47a798a`. Actual downloaded Windows consumer passes 13 steps and three live calls; all 17 archive files and 41,460 bytes match source. Candidate and receiving-main lint/typecheck, unit, build, browser E2E and CI Status passed. General/security independent source reviews passed at `a7cc25f`; 116 focused local tests passed. Supported-host installation and customer judgment remain separate acceptance gates. |
| Managed Companion and account link | Verified Supabase sessions and deliberately proven Starlight links support tenant isolation, durable state and accountable collaboration. | Linking code is accepted, but the fresh backend has no `gencreator_companion` namespace and production env metadata is empty. Schema activation, server credentials, real Clerk OAuth registration, backup/recovery, retention/delete review and two-account acceptance remain required. |
| Starlight SDK/client adoption | Reuse published SDK 8.5.1 and existing MCP/router/memory contracts, then prove one connected creator task with its receiving owner. | SDK publication/cold-install evidence belongs to the SIS owner. Connected adoption, Creator-MCP publication and actual desktop/mobile acceptance remain unfinished. |

Current accepted `main` is `f12797b`, after the CI cost change. Vercel reports a
READY production deployment at that source. Final domain/archive/smoke and
receiving-main gate results belong in the current session handover. The released
archive and runtime implementation are unchanged by the four-file CI/doc change.

## A usable revision workflow

1. Export and retain your current project. Confirm the actual source rights.
2. Prepare a request with explicit consent to send the complete supplied source
   and drafts. GenCreator's host/infrastructure retention is unverified; use
   Studio's local file handoff for private material.
3. Give the retained brief/request to your assistant under its data policy. Ask
   it to write a proposal while preserving the request and protected phrases.
4. Preview against the current project. Inspect claims, rights, quotations and
   voice, then select only the edits you want.
5. Apply into a new checkpoint and verify it. Import the resulting project into
   Studio for continued review/export. Import clears source permission, which
   must be confirmed again. Unsigned local checksums establish byte integrity;
   they do not authenticate authorship or a human approval.

The serious alternative is the same assistant writing with manually assembled
HTTP requests and loose JSON files. Controlled checks show original/unrelated
work preservation, overwrite denial and checksum-drift detection. Customer time,
writing quality, repair effort, total cost and demand still need measurement.

## Work without Actions and control release cost

Implementation, focused local tests, independent source review, package building
and public smoke checks can run without GitHub Actions. The current protected
merge path requires `CI Status`; it must represent successful execution. An
external trusted check service could supply checks under a separately reviewed
contract. No such migration or unattended self-hosted runner was installed.

[PR202](https://github.com/frankxai/gencreator.ai/pull/202) is merged. Drafts defer
all four validation jobs. Its hosted draft actually skipped them and ran the
aggregate on `ubuntu-slim`; the aggregate rejected skipped dependencies as
designed. Marking ready triggered all five jobs without another source commit,
and they passed. All 34 local aggregate cases and a five-file independent source
review passed at `3078739`. Automatic native code and security reviews completed
at that head with no inline findings. Receiving-main validation is recorded in
[run 38095053367](https://github.com/frankxai/gencreator.ai/actions/runs/38095053367).

Keep work in a draft, run the smallest useful local check when admitted, batch
coherent changes and mark ready once. Security, design, editorial, Review Gate,
Surface Guard and full ready/main validation stay enabled. Other draft workflows
and Vercel previews can still cost money. Overall savings have not been measured.
At equal rounded duration, GitHub's short aggregate runner is $0.002/minute
versus $0.006/minute for standard Linux. [Runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing).

PR201's manual native-review requests returned a quota limit. Its documented
independent exact-source alternative retained all 21 earlier findings and their
fixes, plus every actual release gate. PR202's later automatic native reviews
completed. These are separate observations; no review-credit purchase or
synthetic successful status was used.

## Team and remaining work

One Codex lead owns the release, CI cost and hub record in separate checkouts.
Poolside supplied independent static code reviews; GitHub supplied actual hosted
checks and native reviews. Fresh swarm preflight still prohibits new parallel
agents: CPU 83%, 25 task runtimes and `pause-new-swarms`, despite recovered RAM.

The [production plan](gencreator-starlight-production-2026-10-11.md) phases later
work into identity/data and creator-experience writers, then client/router/memory
integration, with one independent review slot after admission. Shared contracts
and sequential main merges reduce conflicting edits and expose failures before
another client depends on them. Existing SIS, Creator-MCP and Starlight owners
retain their branches and unfinished work. The full account, app, cloud,
commercial and customer-adoption programme stays open.
