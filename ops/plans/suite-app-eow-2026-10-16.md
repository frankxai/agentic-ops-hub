# Command Center and desktop Suite: Friday review

Review date: Friday 16 October 2026, Europe/Amsterdam. Frank assigned Codex the whole Starlight Command Center and desktop Suite, including native ChatGPT sign-in, on 12 October. Other Queen programme work stays with the owners Frank assigns to Claude. This is a saved review date, not a scheduled job or a promise that every release gate will pass by Friday.

Product issue: [Command Center73](https://github.com/frankxai/starlight-command-center/issues/73). Implementation: [draft PR74](https://github.com/frankxai/starlight-command-center/pull/74), source `9cca6baaacdb4770d45a53c516a233408b4e8c95`. Estate handover: existing [Hub draft PR250](https://github.com/frankxai/agentic-ops-hub/pull/250). Preserve other Voice, mission, collection and Queen work; app ownership does not authorize rewriting their branches or declaring them complete.

## Current delivery

Native main-process source implements dynamic OAuth registration, PKCE/state/nonce, issued-client/returning-subject binding, JOSE ID verification, an actual loopback callback, an Electron safeStorage account vault, account-scoped IPC/model discovery, serialized rotating refresh and revocation recovery. Unknown refresh holds the session for reauthorization. Preload has no credential-returning method. The desktop include rules and both locks declare pinned MIT JOSE6.2.12. Source and package declarations are not a verified installation.

Twenty focused checks and JavaScript syntax checks pass. Providers, identity verification and encryption are fixtures; callback tests use real short-lived loopback HTTP. Normal ownership and staged secret hooks pass:57.58KB scanned, no leaks. Every test listener and temporary directory closes. Actual OpenAI consent/JWKS, OS keychain, packaged app and account-model artifact creation remain unverified. No app release, scheduler, permanent server or paid fallback was activated.

Frozen source review returned REVISE. Eight findings and lead reconciliation are retained; several proposed changes conflict with the documented dynamic-client/discovery flow or checks already present. Lead reconciliation is not independent approval. A second provider timed out. The completed review reported21,620tokens and cost0; native session, CI, human review and timed-out billing are not established by that receipt.

Build PP at12:47UTC was HOLD:2,626MiB free,8,192MiB required. Disk was79.6GiB/8.4%, TIGHT under the current machine contract; no additional worktree/install/build/browser workload was started. The storage sensor's separate label does not override the actual GiB/percent floor. One new app worktree was admitted at80.1GiB; existing SIS and Hub lanes were reused. No foreign process or work was stopped.

## Goals and measurements

| Goal / metric | Baseline as of 12 October | Friday evidence to review |
| --- | --- | --- |
| Native sign-in completions / attempts | Real-account use unmeasured | Dated numerator/denominator, OS/account scope, sanitized failure codes; count consent decline separately |
| Complete accepted app journeys | Unmeasured | At least one connect → create → edit → export → restart/resume journey accepted by Frank |
| Time to first usable artifact | Unmeasured | Same brief in Suite and native Codex; include repair and owner-review time |
| Recovery and account isolation |20 focused fixture checks pass | Real interruption, expiry, revoke, wrong-account and unknown-refresh evidence; preserve failures |
| Credential/privacy boundary | Fixture denial tests, no live audit | Zero token-bearing renderer/MCP/log receipts or cross-account completion in the tested matrix |
| Cost per accepted artifact | Unknown | Separate plan use, paid API, cloud, repair/review time and unallocated cost |
| User usefulness and ROI | Unmeasured | Frank acceptance, baseline time and measured costs before any ROI/savings claim |
| Installation and production | Unreleased draft source | Separate candidate SHA, package artifact, clean install, checks/review and release receipt |

Targets guide review. Passing tests, agent counts and source declarations do not establish useful app output, paying demand or ROI.

## Open issues and next work

1. Resolve the applicable account-screen design contract and add controls to the existing app. Five legacy root design-guide pointers are missing; issue69 records Frank's shared-policy/Emil choice for Voice, but that does not automatically ratify every new screen. Keep native plan credentials out of browser-only Command Center.
2. Install and verify the real JOSE dependency and signed-JWKS/issuer/audience/nonce/expiry rejection under fresh admission. Prove real OS encryption and account switching.
3. Resolve the pre-existing electron-builder manifest/lock mismatch, verify supported Electron/runtime versions, build/package and clean installation. The push warning reported119 default-branch dependency alerts,39high; this is untriaged reported baseline data. App release requires actual dependency/security review.
4. Connect the accepted SIS plan transport or an independently reviewed supported adapter. SIS358 remains a separate transport draft. Prove current-account inference, explicit scope, refresh/revoke and interruption without a silent paid API fallback.
5. Produce and inspect a useful editable/exportable app artifact, preserve source/task identity, and verify restart/resume. Measure the same task in native Codex.
6. Obtain independent approval and exact-revision app/UX/install/release evidence. Preserve REVISE/timeout receipts and all other owners' work.

The broad Queen programme stays open. Codex's current execution scope is the app and native sign-in; Claude's other workstreams keep their existing owners and issue contracts. The original private objective queue was preserved; this record and issue73 carry the current app goals rather than creating a competing queue.
