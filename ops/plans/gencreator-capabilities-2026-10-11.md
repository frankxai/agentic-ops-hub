# GenCreator capabilities and release status

Observation: 11 October 2026. These are source and verification facts, not a
claim that the full managed product or the wider Starlight programme is complete.

## Who the first workflow serves

An author, educator, speaker or founder brings an essay, interview or other source
they have permission to use. They want the argument and voice to survive when
they turn it into a newsletter, social draft or presentation. The useful object
is editable work with its source and decisions still available for review.

| Capability | Workflow and benefit | Current evidence |
| --- | --- | --- |
| Creator Studio | Open permitted source, work with drafts, review the actual writing and export a local project. Keeping the project supports later edits and recovery. | Public production at `e540062`; 22 deployed smoke checks pass. Actual creator acceptance of the full managed journey remains open. |
| Public MCP transforms | A compatible host supplies source/project data to compile, prepare revision, preview edits and apply selected changes. The host authors the writing; the public server performs stateless transforms. This lets a creator work from their existing assistant. | Existing revision engine accepted through PR200; protocol, discovery, compile and peer-feedback smoke pass. These calls do not run managed model inference, persist a workspace, publish content or establish authenticated human approval. |
| Downloadable plugin | Focused skills and scripts carry the source/review/export workflow into a host. They help developers and capable creators keep inputs and outputs together. | Published0.5.1 archive verified at29,714bytes and exact SHA256. A supported host's actual installation/interaction is a separate acceptance question. |
| Revision CLI0.5.3 | Prepare a source-bound request, let the host write a proposal, inspect preview, select edits, apply against current source and verify checkpoints. New output directories preserve original work and support interrupted review. Each network command requires explicit source-sharing consent. | PR201 `a7cc25f`: 13 native Windows steps and3 live stateless calls pass on the extracted candidate; original and unrelated drafts preserved. Local116 focused tests and exact independent general/security source reviews pass. The candidate is unpublished and full release CI is budget blocked. |
| Managed Companion and account link | Planned activation adds authenticated workspace state and deliberately proven Starlight identity mapping. This matters for tenant isolation, durable approvals, recovery and accountability when teams collaborate. | Supabase-session plus explicit linking code accepted; fresh backend metadata shows `gencreator_companion` absent and production project env metadata is empty. Schema, server credentials, real OAuth registration, retention/delete review and actual two-account creator acceptance are still required. |
| Starlight SDK/client adoption | Developers should reuse published SDK8.5.1 and existing MCP/router/memory contracts, then prove one connected creator task with a receiving owner. | SDK publication/cold-install evidence belongs to the separate SIS owner. Creator-MCP publication, connected adoption and native desktop/mobile acceptance remain separate unfinished gates. |

## A usable revision workflow

1. Keep your source and current project locally. Confirm your source rights.
2. Prepare the request only after agreeing to send complete source/draft material
   to GenCreator. Infrastructure retention remains unverified.
3. Give the retained brief and request to your existing host. Have it write the
   actual proposal from the source.
4. Preview the proposal against the current project. Inspect the writing and
   source references, then select only the edits you want.
5. Apply into a new checkpoint and verify it. Import the resulting project into
   Studio for continued review and export. A file checksum proves byte integrity;
   unsigned local confirmations do not establish an authenticated approval.

The alternative is the same host writing with hand-assembled HTTP requests and
loose JSON files. The candidate's controlled checks show preserved original and
unrelated drafts, overwrite denial and detected checksum drift. They do not show
market demand, universal host support, lower total authoring cost or a customer's
approval of the resulting writing.

## Release and cost workflow

One coordinator currently owns the product release, CI cost and hub record in
separate checkouts. Machine admission allows one bounded interactive workload
and prohibits new local swarms. Poolside supplies independent static review;
this does not start additional local agent workers or prove runtime acceptance.
The [production plan](gencreator-starlight-production-2026-10-11.md) retains the
phased identity/data, creator experience and later client/router/memory lanes.

[PR202](https://github.com/frankxai/gencreator.ai/pull/202) defers draft validation
and moves the short aggregate to GitHub's lightweight runner. Its34 local
aggregate tests and five-file independent source review pass at `17ea4b3`.
GitHub reports four validation jobs skipped on the draft; the aggregate could
not start because the Actions budget is exhausted. The change is not on `main`,
and hosted execution and total spending reductions remain unmeasured. Ready PRs
and `main` still require lint/typecheck, unit, build and browser E2E success.

Land PR201 first after actual current checks pass. Verify receiving `main`,
production source/domain binding and published0.5.3 bytes and consumer behavior.
Then refresh PR202 against that main, mark it ready and run all checks before
ordinary protected integration. Native Codex review credits are exhausted;
current exact-source independent general/security reviews are the documented
alternative permitted by the repository contract. Preserve all prior findings,
Review Gate, Surface Guard, security, editorial and design checks.

The full account, app, cloud, memory, commercial and customer-adoption programme
remains open. No public checkout or autonomous publication is activated by these
draft and source-review workflows.
