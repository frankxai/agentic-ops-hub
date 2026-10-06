# Starlight execution handoff, 6 October 2026

Source: Frank's request to verify repository placement/dirty state and hand off or launch efficient cloud agents to execute the Starlight vision. This record continues product issue 82, the assessment, rollout issue 95 and accepted Agent Kits issues 74-77. It is a transfer packet in the existing hub, not a new task queue or a completed product release.

## Repository and source placement

| Work | Canonical GitHub owner |
| --- | --- |
| Website, platform journey, demand capture, product roadmap | frankxai/starlightintelligence.ai; issues 82/95/74-77 |
| Activation-router source and package | frankxai/Starlight-Intelligence-System; new issue 300, parent123, existing PR 202 |
| Activation scanning/generated index | frankxai/ai-capability-registry; existing issue 6 |
| Agent Kit runtime/template | frankxai/openclaw-acos-skills-railway-template; release tracked in site issue 74 because runtime issues are disabled |
| Hermes/operator and isolated profiles | frankxai/production-agent-patterns; issues 5/6 |
| Memory / Observatory / Canvas | Their existing repositories; private data is not a cloud job input |
| Estate handover/session/ledger/pickup | frankxai/agentic-ops-hub; existing PR 161 |

The local starlight-intelligence-web origin is a legacy GitHub alias redirecting to starlightintelligence.ai. A second clean checkout named starlightintelligence.ai is on a Hermes branch. Both identify the same remote product, not separate platforms; preserve both lanes and shared remote metadata.

Latest observed main: site cbba15d3f647429fd2e2252943b5ae46fbf6177c; SIS c462fc7b0f0565dfdaa906ac5ef0021e76980eaa; runtime 3ef09c0e4fb712bcd9ac94ce34051a6e3f54fc92. Every worker must recheck before integration.

Important advancement since the assessment: site PR 92/93 are merged mobile/canary fixes; PR 94 already supplies demand capture; PR 87 advanced to 680625 with cancellation-submission and lost-response receipt fixes after PR 91's earlier source integration. PR 96 adds the React19.3/SpeedInsights/Node24 dependency baseline at e770fe68c3af9aefe5615f3789e3a76dce13f99b. Runtime PR 2 proposes an upstream OpenClaw ref update at 9c64a09. These must be reconciled with their owners, not discarded or blindly declared absorbed.

## Dispatched independent cloud jobs

| Job and source prompt | Tracking | Cloud session |
| --- | --- | --- |
| [Site integration](starlight-20261006-site.md) | [Site PR 97](https://github.com/frankxai/starlightintelligence.ai/pull/97), issues 95/82 | 23c11bcc-4e08-4f39-86a3-0f1e85cce18e |
| [Router reliability](starlight-20261006-router.md) | [SIS PR 301](https://github.com/frankxai/Starlight-Intelligence-System/pull/301), issue 300/123 | 9f171e96-795e-4eb9-9acc-21495fba4ee0 |
| [Owned Agent Kit installation/recovery](starlight-20261006-runtime.md) | [Runtime PR 3](https://github.com/frankxai/openclaw-acos-skills-railway-template/pull/3), site issue 74/77 | 9db89700-b9cd-4740-b7d0-28767b8ad5fb |

These are GitHub cloud-agent jobs, not Codex Cloud tasks or local subagents. They use separate repositories and one integrator per repository. Their starting task statuses were queued/in_progress; submission is not implementation acceptance. Read actual session/PR evidence before advancing a milestone.

Codex CLI listed tasks but omitted usable environment IDs; the ID in issue 95 returned environment-not-found. The browser/TUI fallback did not produce a verified launch. Supported gh agent-task provided the actual launch path. The first site request returned504; after verifying no task/PR and succeeding with the other repositories, one bounded retry created PR 97. Only one actual site session is recorded. No other provider/settings/token changes were made.

Each packet contains exact source refs, valuable job, explicit file ownership, preserved work, business/privacy/quality constraints, tests, failure/recovery checks, stop conditions, external dependencies and return contract. Instruction budget: one job, no fanout, up to 90 minutes and one coherent build/test cycle, expanding only for failures/new changes. This budget is not claimed as provider-enforced; actual billed usage remains unknown until provider receipts exist.

## Dirty-state audit and preservation

At 00:23 UTC, router PR301 returned draft head 0f3541a with agent-reported 10 tests and passing security/design/editorial reruns. Full harness is intentionally draft-skipped; independent review and native installation remain open. Site97 and runtime3 remain in_progress. See the session receipt for exact runs and issue links.

Thirteen relevant canonical checkouts plus the owned hub worktree were inspected. Site candidate2cc7fe0 and hub14998e5 were clean, pushed and in their own Codex lanes. Memory, Observatory, creator MCP, Academy, ai-architect and the second site checkout were also clean at inspection. Six checkouts had pre-existing changes:

| Checkout / branch | Observed changes | Required resolver |
| --- | --- | --- |
| agentic-ops-hub / agent/hermes/fleet-task-contract-v1 | untracked .claude/worktrees/ | Existing Hermes/worktree owner; keep PR 161 isolated and preserve hub PR 164 |
| SIS / codex/consolidate | modified .worktrees/claude-site-integrity gitlink | Nested worktree owner; inspect its own status/lease/PR, never reset from the parent |
| starlight-agent-config / agent/grok/placement-on-main |41 untracked entries, chiefly .loop/.claude/.gstack runtime/evidence, core/loops and backup files | Existing Grok/control-plane owner; classify privately before any stage/ignore/archive proposal |
| starlight-agent-canvas / agent/hermes/q-town-second-brain | modified .worktrees/cockpit gitlink and untracked .claude/ | Existing cockpit/Hermes owners; no parent cleanup |
| agentic-ops / agent/claude/c940-vacation-envelope | untracked .claude/worktrees/ | Existing Claude/worktree owner |
| ai-capability-registry / codex/design-discovery-20260916 | modified registry/generated/codex-activation-index.json | Existing issue 6 owner; preserve the working diff and source provenance before refresh |

No foreign changes were staged, reverted, deleted, archived or described as abandoned. Clean does not mean merged/released. The stale index timestamp remained2026-09-22T16:15:16.3060908Z at this inspection. Never commit a whole private scan containing machine paths merely to make status clean.

Local admission measured1529 MiB free, swarms drain-and-handoff, while zero-reserve interactive reads/text remained admitted. No heavy local build, dependency/worktree fanout, new worker/server or browser QA was started. Peak-performance issue 3 already tracks reserve admission/runtime reconciliation; do not open a duplicate or claim the zero-reserve reading exemption is a new defect.

## Integration and remaining execution sequence

1. Site PR 97 is the only new site integrator. It must preserve main mobile/canary, original PR 91, later PR 87, PR 94 and compatible PR 96 changes, then produce exact-head CI and production-built browser/recovery proof. Source PRs remain open until their current heads are accounted for and the reviewed integration lands. PR 89 remains a proposal. Privacy, consent and actual configured storage must match behavior.
2. SIS PR 301 repairs router facts and tests; registry issue 6 owns portable-manifest scanner/configured enablement/freshness. After reviewed source, a local owner performs a clean native install/update/remove and refresh from an owned registry lane. Cloud fixtures do not prove the installed Windows state.
3. Runtime PR 3 handles current pin, usable briefing, install/restart/export/restore and failure behavior. Issue74's independent fresh Railway verifier still needs an approved isolated account/key when absent. Existing production launchpad stays intact. Operator/Hermes work remains production-agent-patterns 5/6.
4. Once integration and a useful Agent Kit artifact are evidenced, continue site issue 82's outcome-led homepage/catalog/start/editor refinement across the existing 38 route families. Use the actual source-derived brief, real installation/recovery, small primary navigation, exact availability, one identity authority and practical developer/MCP docs. Preserve creative labs, free Academy and editorial proof. The canary's contrast/touch/focus reports are unresolved evidence, not automatic PASS.
5. Use site issue 95 to reconcile preview configuration, review and release controls: existing KV plus product-specific Resend segments from PR 94, not a competing Supabase waitlist. Its RESEND_AUDIENCE_ID hand-setup wording is stale against the current per-product segment names. Prepare required GitHub checks/ruleset artifact; an authorized owner applies the reviewed rule and verifies actual enforcement. Current empty rulesets/unprotected branch do not become protected from this document.
6. Obtain exact-revision independent provider/design review and legal review where required. Issue95's claimed Grok comments were not verified in visible PR 91/94 comments/formal reviews. Keep approval pending until an actual receipt is linked.
7. Continue75 paid fulfillment and76 ten activations/three accepted jobs. EUR149 pack and EUR39 maintenance remain hypotheses; manual EUR750 activation conflicts with DIY/no one-to-one services and should become a self-service offer or an explicitly accepted exception. Use existing financial owner/provider settlements, duplicate/refund/expiry tests and marketplace-specific eligibility. No checkout before fresh release/price evidence.
8. Extend proven installation, release/capability evidence and fulfillment infrastructure across other brands through their existing owners. Hosted licensing/auth and public license changes remain proposals. New model/version/framework adapters require current official docs and task-level evidence, not blanket dependency upgrades.

## Pickup and cloud reconciliation

Read the relevant issue and its linked prompt/session, inspect the returned PR/diff and exact base/head, then claim a free local integration lane. Run route_work guard/check and the existing integration_preflight check with source task, immutable base, saved patch and explicit files before applying. Reconcile once; never reapply a partially applied patch. Run the appropriate native and behavioral checks, independent review and one coherent preview. Do not infer integrated/merged/deployed from cloud state.

Append final receipts to the existing issue and hub session/ledger/prompt. Coordinate hub PR 161 with PR 164 so neither session nor other prompts disappear. No new registry, command centre, Linear queue, recurring poller or automatic closure was created.
