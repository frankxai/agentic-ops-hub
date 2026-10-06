# Starlight continuation: runtime review and recovery
Date: 2026-10-06. State: validated source; live/native/customer release gates open.

## Delivery and exact evidence

[Runtime PR4](https://github.com/frankxai/openclaw-acos-skills-railway-template/pull/4) is stacked on PR3 base `8a25742f0f6c6b400632d7e3e98bdc00c66ca9e5`. Head `21622df80ca0fc0e37885a3b9cc4f1b216e5e775` contains the five independently reviewed files byte-for-byte. The remote receipt is [CONTINUATION-REVIEW](https://github.com/frankxai/openclaw-acos-skills-railway-template/blob/21622df80ca0fc0e37885a3b9cc4f1b216e5e775/docs/CONTINUATION-REVIEW-2026-10-06.md). A publication retry found this matching PR already present; it was preserved, not overwritten or duplicated.

Repairs: authenticate configured HTTP and WebSocket callers before internal Gateway-token delegation; exclusive job-operation locking; reject late cancelled drafts and credential-bearing intervention notes; bind acceptance to current inputs and draft bytes; bounded provider downloads and explicit incomplete-output review; recover a draft surviving SIGKILL before receipt finalization without a second provider request. The inherited anonymous Gateway bypass was dynamically reproduced before correction. Four runner regressions failed before repair.

Lead full suite: 45/45, lint, Railway SDK typecheck, pack verification and whitespace checks passed on the reviewed bytes. Independent same-harness reviewer: 16/16 focused tests and no remaining must-fix findings; earlier 44/44 full run preceded the recovery regression. This is separate-agent review, not independent-provider signoff. After the execution workspace changed, all five original SHA-256 values were reconstructed exactly and the full 45-test suite reran successfully. Remote file contents then matched those reviewed bytes.

[CI37399866536](https://github.com/frankxai/openclaw-acos-skills-railway-template/actions/runs/37399866536) passed Node22/24, 45 tests on each, lint, pack and IaC checks. [Docker37399866528](https://github.com/frankxai/openclaw-acos-skills-railway-template/actions/runs/37399866528) passed. Raw logs identify checkout merge `6c613a5447ad35cab806d51364b11172c4645ca7`, merging exact head21622df into base8a25742. Image build is separate from live deployment/authentication/volume evidence.

## Refreshed source reconciliation

| Owner | Candidate | Evidence and limit |
| --- | --- | --- |
| Website | PR97 `883882e3ba8f78a2513e440e4476f9be8410940c` | Draft; current heads of PR87/91/94/96 all ancestors by compare API, behind0. Vercel preview READY, full rendered QA and independent design review remain open. |
| Router | PR301 `0f3541a5745f8c24bea8c035d6f910b87d6546b0` | Draft; 10/10 targeted tests rerun by lead. Security/design/editorial checks pass; broad harness draft-skipped. Windows/native installation pending. |
| Runtime | PR3 `8a25742` plus PR4 `21622df` | Corrected source and current image build verified; live output and fresh Railway acceptance pending. |
| Estate | Existing hub PR161; separate PR164 `4dd8093` | Session/ledger/pickup updated in PR161 lane; other owner's work preserved. |

Site preview: `dpl_7s3P5k3WZ4LuMhksyaqTEh5Re6Mo`, project `prj_ftKChFdlU15okomAnqWj7FufsEQM`, target preview, exact source883882e3. [Serving candidate](https://starlightintelligence-ai-git-copi-2c3a2a-starlight-intelligence.vercel.app). READY is build evidence, not production/customer/design acceptance. No production change occurred.

## Product and architecture decision

Keep the first job: developer-led automation studios and small product teams turn approved sources into an editable, cited decision brief with recoverable attempts and export. Preserve BYOK, customer-owned data/runtime, self-service, free Academy and existing fulfillment authority.

The direct no-tools CLI is sufficient for this bounded job. Next/Vercel remains discovery/editor/distribution; existing Clerk identity and KV/Resend capture remain canonical. No new Supabase identity, queue or scheduler is justified by this correction. The full OpenClaw image remains an optional broader host; a lighter standalone CLI is a packaging hypothesis requiring distribution/cost evidence. No runtime pin, upstream interface, framework or migration was changed.

Vanilla Codex/Claude is the serious same-task alternative. No legitimate live model/comparison grant was available. Quality, repair effort, elapsed time, observed provider cost and preference remain unmeasured. Source fixtures cannot establish superiority, accepted customer output or price. Keep EUR149/EUR39 as historical hypotheses; no checkout or financial change.

Source inspection of homepage/start/agent-kits/platform confirms: homepage leads with council discovery; start copies a council prompt; Agent Kits provides a source-preview planner/waitlist; Memory Studio exposes editing/export/recovery with cloud gates. After native proof, prioritize the evidence-brief task and actual artifact in discovery, then one install/use/recover/export journey. Preserve all exploratory/creative page families. This is a source-based assessment; no new rendered design acceptance or all-route visual audit was performed.

## Remaining gates and one next action

Integrate the corrected source after applicable exact-revision provider/release review, then perform issue74's independent fresh-host run: actual browser HTTPS/WSS onboarding/reload/reconnect, separate deployment-scoped secrets, one real accepted brief with all attempts/usage/cost, mounted-volume restart, export and fresh restore. Browser WSS depends on cached same-origin HTTP Basic credentials; raw TCP tests do not prove it. Native Windows/router installation, independent provider/design/legal review, baseline comparison and issues75/76 fulfillment/activation acceptance remain open.

Windows PP/route_work/private machine contracts are unavailable in this cloud harness. Admission used isolated checkout, observed9270MiB available RAM and lightweight source/tests; no foreign checkout cleanup, private data upload, live inference, paid resource, template publication or production migration. Test processes were session-owned and stopped.

Rollback preserves private jobs/exports; reverting the correction restores the inherited anonymous proxy bypass and must not expose that wrapper publicly. Rehearse state recovery only in an isolated destination.

Official API sources read2026-10-06: [Node AbortSignal](https://nodejs.org/api/globals.html#abortsignalthrowifaborted), [Node Web Streams](https://github.com/nodejs/node/blob/main/doc/api/webstreams.md), [OpenAI Chat Completions](https://developers.openai.com/api/reference/resources/chat). Existing broader platform references remain in the foundation assessment; no broad framework replacement was undertaken.
