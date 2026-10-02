# Queen foundations and next-agent goals

Status recorded on October 2, 2026: **MERGED_NOT_LIVE**. This is a sanitized navigation and planning guide. The private operational Registry remains authoritative; follow-up targets below are proposals, not completed integrations or measured service guarantees.

## What exists and where

| Deliverable | Location and evidence | Remaining boundary |
|---|---|---|
| Signed Slack intake, actor allowlists, issue-bound task envelopes, deduplication and threaded progress | Private `agentic-ops`: `lifecycle/slack-queen.py`; [PR135](https://github.com/frankxai/agentic-ops/pull/135), merge `7d3424916a7cb1794cd045244fd951c5b43199cd` | `/queen` is unregistered. No provider transport or shell dispatcher is supplied by this helper. |
| Subscription-first route admission and atomic cost reservations | Private `agentic-ops`: `lifecycle/queen-admission.py`, example configurations and tests | Workflows and routes default to held. A trusted supervisor and reconciler must exclusively own ledger writes. |
| Private state, malformed-result and redirect hardening | [PR138](https://github.com/frankxai/agentic-ops/pull/138), merge `7585db643af86ca404e397489355e3c767f89f1b`; 36 Slack plus 16 admission tests passed at that reviewed head | Local tests and successful CI do not prove deployed execution. |
| Operational blueprint, provider boundaries, Slack runbook and dated n8n audit | Private `agentic-ops`: `docs/QUEEN-OPERATIONS-BLUEPRINT.md`, `docs/SLACK-QUEEN.md`; private audit evidence stays with its operational owner | Provider eligibility, account allowances and actual billing need verification before activation. |
| Host-bound non-code task acceptance and durable artifact recovery | [Ops PR150](https://github.com/frankxai/agentic-ops/pull/150), merge `d1d39191f13e1f62c0cfdd76ba7a63ae63c558ad`; independent source-only APPROVE at `0251b10a95fcd465af35e0cb5f1060c836388cdf`, 146 total cloud regressions pass, including 12 adapter tests also run locally; post-merge CI 37006792719 passes | MERGED_NOT_LIVE. Controller authentication/ACLs and actual dispatch integration remain required; git-write is held pending isolation and full adapter proof. |
| Queen's own SOUL, operating contract and held source capabilities | [Config PR90](https://github.com/frankxai/starlight-agent-config/pull/90), reviewed `c9b9c24d3ec61895c58b6ef12da72a28d3764d1a`; validator, required doctor checks and CI pass | UNMERGED / REVIEW_REQUIRED. Independent source-only APPROVE. Main requires one native approving GitHub review; source is not merged or installed. Existing generic Hermes SOUL and credentials are preserved. |
| Slack channel standard, operating desk, agent register and progress/evidence conventions | Existing workspace posts and threads; summarized in the [October 1 Queen Slack receipt](../ops/sessions/2026-10-01.md#queen-slack-workspace-and-command-bridge-codex) | Human/connector posts do not establish an authenticated Queen bot or always-on executor. |
| Sanitized handover, ledger and activation pickup prompt | [Hub PR99](https://github.com/frankxai/agentic-ops-hub/pull/99), merge `df9d13880de5280dc3c1775d5d1ffe39409499d9`; `ops/sessions/`, `ops/OPS-LEDGER.md`, `ops/NEXT-PROMPTS.md` | Preserve other unfinished work and current file owners when refreshing these records. |

The PR150 reviewer ran no commands and relied on recorded runner environment
scrubbing and snapshot roots. Reviewed head and merge have the same Git tree
`94afefbac51b79ea1bf7573888ed02871f1b24bd`; exact-main CI verifies the merged
revision. These are source and test observations, not live control proof.

Private links require repository access. The broader outcome stays open in [agentic-ops issue134](https://github.com/frankxai/agentic-ops/issues/134). As of the October 2 receipt, supported n8n management/editor access was unavailable to the session. Previous health observations established reachability only. No live workflow edits, new recurring worker, paid managed session, Matrix adapter or authenticated end-to-end Queen task were proved by these slices.

The later October 2 audit restores read-only n8n connector access: 46 workflows
are visible and no Queen-specific workflow matched. Management API authentication
still returns HTTP401. The connector's execute method rejects the existing health
workflow request with `executionMode: Required` before returning an execution ID;
the exposed schema does not accept that required field. No workflow execution or
edit is proved. Restore the supported management/editor path and connector contract
before retrying. This supersedes the earlier session's unavailable read inventory.

[Queen purpose and product](QUEEN-PURPOSE-AND-PRODUCT.md) records the first user job,
serious alternatives, monetization hypotheses, community practice and delivery
order. It is a decision brief, not proof of a live or paid product.

The initial pilot ceiling is EUR100 per month for incremental API/cloud commitments, as recorded in the [merged October 2 handover](../ops/sessions/2026-10-02.md). Reconcile all pilot commitments before admission; unknown cost stays held. Prefer deterministic work and supported, verified subscription allowances. The private blueprint specifies that quota exhaustion queues work unless that workflow has explicit bounded paid fallback authorization. Budget increases require an explicit revision supported by outcomes.

## Which repository owns each foundation

Placement source: reviewed private `agentic-ops` Registry at `98f20458a295fb8bde06e7f4519a9c9fb611e470`, specifically `registry/manifest.yaml`, `repositories.yaml`, `exclusions.yaml`, `artifact_authorities.yaml` and `architecture_decisions.yaml`. [PR148](https://github.com/frankxai/agentic-ops/pull/148) places the Queen identity profile in config and the Slack work adapter in Ops, with the public hub as a sanitized consumer. Both placement records remain planned/not deployed. They do not import a canonical agent identity, create another repository or move runtime policy into config. SIS and skills additions still require reconciliation and review.

| Repository | Role summarized from Registry | Queen work to keep or propose there |
|---|---|---|
| [agentic-ops](https://github.com/frankxai/agentic-ops) (private) | Operational control plane and portfolio Registry | Keep runtime implementation, orchestration policy, admission, deployment runbooks and private operational evidence here. |
| [agentic-ops-hub](https://github.com/frankxai/agentic-ops-hub) (public) | Doctrine, governance templates and sanitized projections | Keep this map, adoption blueprints, public examples and sanitized session receipts here. Link to private authority rather than copying live configurations. |
| [Starlight-Intelligence-System](https://github.com/frankxai/Starlight-Intelligence-System) (public) | Intelligence protocols, provenance, governance and evaluations | Propose portable task/event/identity/evidence contracts and fault-evaluation fixtures after reconciling existing contracts and open work. Runtime adapters remain with their operational owner. |
| [starlight-agent-config](https://github.com/frankxai/starlight-agent-config) (private) | Executable agent configuration and release policy | Own the versioned Queen SOUL/working profile. Route activation, native permissions and actual deployment remain separate gates. |
| [starlight-agent-skills](https://github.com/frankxai/starlight-agent-skills) (public) | Shared capability and skill sources | Propose portable operator skills and adoption checklists using sanitized examples and declared dependencies. |

Once the priority 6 public package is published and license-reviewed, educational and business-facing surfaces can consume it and cite its version. That package does not exist yet. A new repository needs a distinct product, permission, release or storage boundary approved through the Registry. Slack and later Matrix are interfaces to the same task identities and evidence. Preserve one durable orchestrator per workflow and one authoritative policy source.

## What the next agents should build

Execute sequentially while machine admission allows only one worker. These are bounded work packets for future owners, not authorization to launch a swarm or activate providers. Each packet starts with the current issue, exact base commit, explicit owned files, placement and lane checks, and the relevant release gate. Read current official provider documentation before implementation. Packets 2 and 4 can begin with local fixtures while packet 1 waits for the owner to restore supported access.

| Priority and owner | Artifact to build | Proposed acceptance target and clock |
|---|---|---|
| 1. Runtime operator; `agentic-ops`, issue134 | First live Slack task: restored supported n8n access, disabled workflow corrections, approved Queen app/HTTPS ingress, private state and an owned supervisor | Within seven days after required access and deployment admission are available, first probe one sandbox executor, then prove one issue-bound envelope, one worker claim, meaningful progress in one thread and final artifact/acceptance evidence. Test replay, stale/unauthorized intake and restart recovery. Record exact deployment SHA, owner, observation time and rollback. Only then admit the deterministic health pilot. |
| 1b. Execution isolation owner; `agentic-ops`, issue134 | Code-task adapter using isolated Git configuration and host-pinned acceptance inputs | Before enabling coding through Slack, prove a real pushed-code task and independent review; deny planted Git hooks/config, checker substitution, wrong refs and stale evidence. Run the existing verifier regressions and full adapter success/failure/restart paths. The current new adapter explicitly holds git-write; its local non-code fixtures cannot close this packet. |
| 2. Admission/accounting owner; `agentic-ops`, config projection only where needed | Trusted supervisor around the existing admission library, fresh auth/quota observations, invoice reconciliation and immutable final receipts | Before the first paid call, prove every paid operation reserves all-in cost; unknown creation/timeout remains held; concurrent admission cannot exceed caps; models cannot settle costs. Prove daily/monthly rollover and that zero-charge settlement requires evidence. Start within the EUR100/month pilot ceiling. |
| 3. Runtime inventory owner; `agentic-ops` plus reviewed config projections | A truthful agent register with executable/version, owner, supported auth method, allowance source, heartbeat and proof links | Within the first live pilot week, enumerate every executor admitted to the pilot. Proposed heartbeat freshness is 300 seconds, a pilot target to validate separately from the Slack observation TTL. Active status requires a fresh verified receipt; stale or missing evidence becomes unknown. Installation and provider deployment success never substitute for task execution. |
| 4. Protocol/evaluation owner; SIS contracts, Ops implementation | Reconcile portable task/event/artifact/cost schemas with existing contracts; build crash, duplicate, timeout and unauthorized-input fixtures | Before a second transport or paid provider route, pass at least 20 controlled fault cases with zero duplicate launches, claims or reservations. Every accepted result binds its issue, source version, artifact, reviewer and cost receipt. Do not merge unrelated SIS checkpoints. |
| 5. Pilot outcome owner; `agentic-ops` | Two-week scoreboard for lead time, acceptance, rework, founder review minutes and cost per accepted outcome | Over the first 14 days after live activation, attempt 20 issue-bound tasks drawn from the admitted deterministic health pilot and explicitly admitted research/review routes. Target at least 90% acceptance, and require 100% evidence/cost coverage for accepted tasks and zero unauthorized external actions. Report failures and uncertain costs. Publish a scale, repair or hold decision within the ceiling. |
| 6. Hub adoption owner; skills repo consumes reviewed outputs | A versioned business adoption pack: architecture, minimal manifests, workflow example, fixtures, deployment/rollback checklist and operating worksheet | After the first live receipt, complete dependency/license review and an independent synthetic-task rehearsal on the release candidate before publication; both remain required. After publication, have an independent operator reproduce that task within 60 minutes using only the public package. Record actual elapsed time and defects. Make no estate-specific secrets or private source prerequisites part of the public exercise. |

OpenAI Dots, Codex/ChatGPT tasks, OpenAI Agents API/SDK, Claude Managed Agents, n8n and Matrix all remain in scope for evaluation. Add a route only when supported account access, data fit, cost reservation, cancellation/reconciliation and meaningful progress receipts are proved for its exact use case. Reuse the existing queue and task IDs. Provider-local sessions remain delegated workers.

Dots is now established in [current official documentation](https://learn.chatgpt.com/docs/dots),
including cloud operation, Slack messaging and delegation. This does not verify
the estate account's access, usage allowance or a Queen-to-Dots adapter. Compare
its supported native flow with Hermes on the same job before choosing a deployment.

Every two weeks, rank admitted workflows by accepted outcomes, full cost, reliability, rework and founder time recovered. Expand investment only through a recorded decision with a new ceiling and a stop rule. Revenue forecasts need customer evidence; these targets do not imply revenue, profit or a demonstrated autonomous business.

## Pickup and record

Start with [issue134](https://github.com/frankxai/agentic-ops/issues/134), the private runtime runbook and the [current pickup prompts](../ops/NEXT-PROMPTS.md). Report the observed state as IN_PROGRESS, PR_READY, MERGED_NOT_LIVE, LIVE_VERIFIED or BLOCKED with its exact proof. Save the handover in this hub and update the existing product issue; check file ownership before changing the shared ledger or prompts.
