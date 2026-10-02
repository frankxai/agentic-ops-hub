# Queen: purpose, product and participation

Decision brief, October 2, 2026. This records founder direction and a product
hypothesis. It does not establish a deployed Queen service, paying customers,
market size or a released adoption package. Implementation status is in
[Queen foundations](QUEEN-FOUNDATIONS-AND-NEXT-GOALS.md) and the
[October 2 receipt](../ops/sessions/2026-10-02.md). The existing private Registry
owns portfolio and runtime decisions; this public guide is its sanitized consumer.

## Why this work matters

Starlight's purpose is to help people and organizations use advanced intelligence
to become more creative and capable. Queen serves that purpose by keeping work
understandable and recoverable while agents operate. A founder should be able to
leave a useful task running, return to an inspectable result and understand what
it cost, what changed and what still needs judgment. Time recovered should create
room for making, learning and relationships.

Our operating principle is to regulate the state of work: requested, admitted,
running, held, verified and delivered. Each transition needs evidence and an owner.
This makes the mission concrete. The technology follows from the human consequence:
one task identity across tools, bounded authority, observable progress, verified
artifacts and a recovery path when a provider or machine stops.

The narrative should show actual work. Lead with the creator's job, demonstrate the
artifact and its limits, explain the mechanism, then offer a reproducible way to
participate. Avoid claims of inevitable wealth, universal autonomy or industry
leadership before evidence exists. This direction follows the
[Starlight brand pack at revision c7a58f1](https://github.com/frankxai/starlight-design-intelligence/blob/c7a58f112b46ddd8ba85844ba03c31a1308bc5eb/brand-packs/sis/BRAND.md).

## The first valuable job

Focus on a technical founder or small product team already using GitHub, Slack
and more than one agent client. They have an issue they want resolved and spend
time moving context, checking progress, reviewing changes and recovering failed
runs. The first promise to prove is: send one bounded issue from Slack and receive
one useful, independently reviewed result with its source revision, cost state
and recovery record in the same thread.

The first demonstration must investigate an observed workflow failure and deliver
an actionable, checked repair artifact. An agent register, manifest or
dashboard supports this job; it cannot substitute for the result. A successful
health probe alone does not prove the complete coding or workflow repair loop.
The first live proof is a non-code investigation and checked repair artifact.
Coding through Slack follows only after Git isolation and full adapter execution
are proved; neither coding nor automatic workflow publication is available now.

The initial pilot is our own operating estate. It establishes internal usefulness
and exposes integration failures. External operators must subsequently reproduce
the job before we claim portability. Paying customers must establish willingness
to pay before we claim commercial value.

## Who might use it

These are testable audience hypotheses, ordered by proximity to the first job.

| Audience | Job and current behavior | Evidence to seek | Acquisition hypothesis |
|---|---|---|---|
| Technical founders and small software teams | Move issues between agents, then manually inspect investigations, changes and failures | Useful non-code investigations first; accepted coding fixes after isolation proof; less review/recovery time and continued use | Reproducible GitHub examples, coding-agent communities and founder build logs |
| n8n operators with several business workflows | Distinguish active configuration from actual execution health, recover duplicates/timeouts and maintain credentials | Accurate failure detection, lower repair time, zero duplicate external actions | n8n community failure studies and shared fault fixtures |
| Platform engineers managing agent use | Control delegated identity, repositories, spending and audit evidence | Cross-provider controls pass their threat model and maintenance requirements | Open engineering specifications and reviewable integration cases |
| Technical educators and AI creators | Teach reliable workflows and produce useful reusable artifacts | An independent learner reproduces and repairs the task using the package | Starlight Academy lessons, operator labs and contributed examples |

Current signals support investigating reliability. In the 2025 Stack Overflow
survey, 46% distrusted AI accuracy and 66% reported frustration with almost-correct
answers. These are developer survey results, not Queen buyer counts or purchase
intent. [Survey source](https://survey.stackoverflow.co/2025/ai).
The [n8n community](https://community.n8n.io/) contains operator discussions about
silent production failures, observability and duplicate webhook recovery. Those
discussions inform experiments; they do not prove demand for our implementation.

Size the addressable market from observed qualified organizations and deployment
fit. A useful model is qualified organizations × activation rate × paid conversion
× annual realized revenue per organization. Each input is currently unknown.
Separate the serviceable segment we can actually support from a broad category
of AI users. Use interview and activation cohorts to populate the model, retaining
sample size, consent and uncertainty. Do not publish a fabricated billion-dollar TAM.

## Build on existing runtimes

Keep Queen's SOUL and working profile versioned in agent config, with execution,
admission and evidence in private Ops. Use upstream Hermes profiles and extensions
before taking on a fork. Hermes provides separate profile configuration and data
directories and a SOUL loading mechanism. Host tools share the real OS-user home by
default; profile separation does not establish a security boundary. Our host still
has to prove native tool permissions and writer boundaries.
[Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles),
[SOUL](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes).

A separate `starlight-queen` repository becomes justified when it has an independent
distribution audience, release cadence or permission boundary approved through
the Registry. A name alone does not establish that boundary. Public adoption
material currently belongs here; runtime configuration and private deployment
details stay with their owners.

| Same-task alternative | What to reuse | What Queen must additionally demonstrate |
|---|---|---|
| An unmodified Hermes profile | Conversation, tools, gateway and separate profile configuration/data | Issue/repository admission, native execution isolation, verified allowances, exact-result review and durable operating evidence across delegated workers |
| Existing n8n Slack routing with a human operator | Deterministic routing and integrations that already exist | Authenticated task identity, truthful execution state, bounded delegation, duplicate recovery and result acceptance |
| A coding-agent Slack integration | Supported provider-native task entry and progress | A measured reason to add cross-provider admission, independent acceptance and cost/recovery records |

Run the same job with the selected alternative. Record usable output, defects,
repair effort, elapsed time, human review minutes and full cost. Retain the simpler
route if it achieves the outcome more reliably. These are comparison questions;
we have not established that another product lacks a specific control.

OpenAI's current documentation describes Dots as a cloud agent, with
supported Slack messaging and delegation to cloud or connected-computer tasks.
Connected-computer work requires that computer to be online with the app open;
messaging does not automatically grant app or computer permissions. Account rollout
and permissions still need verification. We should evaluate it as
a delegated responsibility with an explicit owner and proof boundary, then measure
whether it removes more operating work than it adds.
[Official Dots documentation](https://learn.chatgpt.com/docs/dots).
The OpenAI Agents API supplies a managed Codex harness and recovery. Our architectural
choice is to compare that managed service with a self-hosted SDK application; this
comparison is our interpretation of the integration options. Both still need
account, cost, data and cancellation/reconciliation admission.
[Official Agents API documentation](https://developers.openai.com/api/docs/guides/agents-api/overview).

Claude managed agents, supported local clients and future Matrix transport follow
the same task identity and acceptance authority. Verify current vendor contracts
before each adapter. Do not create a second orchestrator because a vendor offers
one, or treat subscription authentication as portable credentials for every API.

## How the technology earns trust

The useful operating chain is request → owning issue → host admission → worker
claim → meaningful progress → independent checks → independent review → accepted
artifact and cost/recovery record. Slack is the first interface. Matrix can later
project the same identities and state. Transport choice must not create another
queue, policy source or completion authority.

The host owns task-specific checks and dispatch snapshots. Workers cannot choose
their own acceptance authority. Non-code check inputs must be pinned and isolated
from worker edits. Completion binds the exact task, contract, receipt and artifacts;
review provenance must be authenticated outside the worker's write boundary.
Missing proof, expired admission, uncertain spending and revoked review hold work.
Required recovery includes interruption, duplicate intake, ambiguous sends and
repair followed by a new review. These controls apply only where the runtime
actually invokes and enforces them. Loading AGENTS.md is not universal enforcement.

Public contracts and evaluation fixtures can graduate to the intelligence and
skills repositories after their existing contracts and unfinished work are
reconciled. Public distribution requires dependency/license review and removal of
private prerequisites. Maintain exact source provenance rather than copying an
ever-growing private installation into a public product.

## Monetization hypotheses

The business direction is scalable software, digital products and media/IP.
These routes require evidence and suitable dependency rights before a launch.
No pricing, checkout, paid managed session or customer promise is activated here.

| Route | Paid value to establish | Release evidence | Recurring burden |
|---|---|---|---|
| Versioned operator and workflow kits | A reproducible complete job with failure fixtures and maintenance guidance | Independent installation, useful output, editing/recovery and license review | Updates for supported provider/runtime versions |
| Team operations software subscription | Shared admission, evidence, cost reconciliation and recovery across approved tools | Tenant isolation, actual live tasks, billing controls, customer retention and measured reliability | Hosted operations, security, support and integration maintenance |
| Education and team learning licenses | Learners become able to implement, diagnose and repair the workflow | Independent learner outcomes, accurate materials and consented case studies | Curriculum and dependency updates |
| Partner/embedded capability licensing | Another product delivers a verified operating outcome through a supported interface | Tested SDK/contract, partner demand, dependency rights and maintenance agreement | Compatibility, release support and clear responsibility boundaries |

Free source-derived examples and fault fixtures can let people evaluate the work
and contribute. Decide which material is free or paid from usefulness and rights,
not manufactured scarcity. n8n distribution/hosting and Hermes/runtime dependencies
need current license review before any commercial package. No right to resell a
dependency is inferred from its installation or this guide.

Start within EUR100/month incremental pilot commitments, separate from existing
subscriptions. Prefer deterministic execution and supported verified subscription
allowances. Admit paid work only with reconciled commitments and a bounded reserve.
Quota exhaustion queues work unless that task has explicit authorized paid fallback.
Expand the ceiling after accepted outcomes and credible economics, never a revenue
forecast alone. Count human review, rework, provider charges and hosting costs.

## Community as shared practice

Use the existing hub and educational surfaces first. Publish a reproducible task,
its failure cases and repair, with source revision and scope. Invite contributions
through the repository's existing issue/PR path. Do not announce a new community
platform or imply existing members, partners or ambassadors without evidence.

After the first live receipt and release-candidate review, propose a founding
operator cohort of five people from the first two audience hypotheses. The founder
approves invitations and public outreach. Observe their installation and first
use, collect consented feedback, and keep a visible defect log. The target is useful
participation: someone reproduces a job, improves a fixture or teaches a recovery.
Membership and follower counts alone cannot establish that value.

The movement's practice should be understandable: create work people can inspect,
share what failed, repair it, and make the next operator more capable. Recognition
can follow useful contributions, documented learning and consented case studies.
Apply the same quality expectation to our own outputs. Public stories use reviewed
artifacts and observed outcomes, with human approval for live/premium publishing.

## Next delivery decisions

With founder-approved invitations, consented problem interviews can run alongside
the engineering work. Record existing behavior and repair effort before asking
about our proposed product; a favorable reaction alone is weak demand evidence.

1. Restore supported n8n management/editor access and resolve the execution
   connector's required-field contract before attempting live corrections. Validate,
   re-read and test disabled changes before publication.
2. Finish reviewed host acceptance and Queen profile integration. Prove controller
   ownership, native tool permissions, supported authentication and cost accounting
   before enabling a worker. A source pack does not complete deployment.
3. Prove one authenticated Slack task through real execution, review, result and
   restart/duplicate recovery. Record the exact deployment and remaining failures.
4. Over the first 14 live days, attempt 20 bounded tasks and report acceptance,
   rework, human review time and cost per accepted result. The proposed target is
   at least 90% acceptance with complete evidence/cost coverage and no unauthorized
   external actions; publish failures as well as successes.
5. After the live receipt and rights review, release a reproducible adoption
   candidate. Have an independent operator complete and repair its task using only
   that package. Test demand through consented operator interviews and the existing
   demand-capture surface, recording the job, willingness to pay and reasons to
   decline. Use those observations to test the five-person cohort hypothesis.

These are ordered work packets, not authorization to launch extra agents under
machine constraints. Keep the existing product issue open until the running outcome
is proved. Save the current receipt and pickup in this hub and the owning issue.
