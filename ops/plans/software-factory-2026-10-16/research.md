# Research decisions and capability candidates

Research read on 16 October 2026. Vendor documentation describes possibilities; account entitlement, implemented integration and measured benefit remain separate. No provider call, new subscription, sandbox or deployment was started for this research.

## Evidence and implications

| Primary source | Finding used | Decision for this program |
| --- | --- | --- |
| [Anthropic: effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Long work needs continuity artifacts and incremental verified progress; a high-level build instruction is insufficient | Reuse issues, immutable source, progress and behavioral acceptance across sessions. Preserve unfinished work and the original customer result |
| [Anthropic: demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent evaluation must account for multi-turn behavior and changing state | Freeze normal/difficult/failure tasks; inspect actual outcomes, traces, repair and repeatability. Structural checks are supporting evidence |
| [Anthropic: building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflows and dynamically directed agents serve different needs; more complexity carries cost and latency tradeoffs | Keep deterministic release/lifecycle gates; use bounded judgment for research, design and diagnosis. Add specialists only on independently useful work |
| [Vercel: Deployment Checks](https://vercel.com/docs/deployment-checks) | Production build and promotion can be separated through deployment checks | Inspect each project's actual configuration. A configured source file or READY build is not proof that our production promotion is protected |
| [GitHub: deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments) | Environments can restrict branches, gate jobs and control secret access | Reuse repository protection and environments where supported. Verify the actual account/repository rules; do not assume plan-dependent approval features exist |
| [Vercel: Sandbox snapshots](https://vercel.com/docs/vercel-sandbox/concepts/snapshots) | Snapshot-based sandbox lifecycle is documented | Candidate for bounded restartable software tasks. Benchmark effective isolation, export, teardown and total cost before adopting; never use it to bypass host/resource or spend policy |

Sources are summarized, not copied. The linked long-running-agent article is a 2025 design study, not a current model benchmark or evidence that our own fleet works. The 2026 evaluation article informs acceptance design, not measured performance claims.

## Architecture decisions already governing adoption

Inspected Registry main: `149dd3c652edf6c3868e25ebd2dba8a69e0b70d1`. Use `architecture_authority_model`, `architecture_experience_plane`, `architecture_persistent_entity_runtime`, `architecture_durable_execution_boundary`, `architecture_managed_agent_delegation`, `architecture_media_fabric_v2`, `architecture_agent_credentials_and_tools`, `architecture_observability_and_cost_contract`, `architecture_portability_contract` and `architecture_federated_product_studios`.

Important correction: the generic cross-agent policy still mentions an R2 asset lake. The reviewed Registry's media-fabric-v2 decision supersedes that default for new Vercel-delivered media. No storage migration is performed here.

The related proposal [PR244 at 5c0fcf4](https://github.com/frankxai/agentic-ops/tree/5c0fcf419b2fd88dd332ca8a6dd5e7f3eca6609f/docs) already researches Workflows, Sandbox, Connect, Queues, Daemons and Cloudflare agent tooling. Preserve its data, identity and provider boundaries. Their appearance in documentation or beta navigation does not prove our credentials, quota, plans or production suitability.

## Serious alternatives and experiments

For each customer job compare the current direct/native workflow, one strong lead using the same tools, and a bounded specialist route. Keep input corpus, tools, allowed effort and grading comparable. Record all attempts, rejected outputs, output quality, user repair time, latency, supplier cost and operator/support effort. Do not claim that a fleet wins because it generated more text or used more agents.

Useful experiments include claim/counterevidence research, verified architecture-to-reference-code generation, source-faithful editorial revision, canon-coherent world creation, cross-client memory recovery, and interruptible multimodal production. They share methods but keep product content, identity and permissions separate.

Start with the existing frozen federation and receiving-user cases where applicable; retain their original thresholds and missing evidence. Define additional brand-specific cases only for actual gaps. Candidate research is not a new parallel business backlog.

## Design guidance status

Selected and read: installed Emil design engineering; owning FrankX, Arcanea, GenCreator and SIS brand material; current Starlight voice and product-guide excerpts. Applied: the plan's frequency-sensitive motion, brand distinctions, visible errors, focus/touch/reduced-motion and interruption acceptance. Verified: no new rendered interface in this slice. Product-specific complete instruction scopes, pinned tokens and live desktop/mobile evaluation remain prerequisites for each implementation lane.

The newer recorded Starlight voice asks for curiosity, confidence, warmth and playfulness, including technical products. Its source is `starlight-design-intelligence@3d6fc8fdd38b5db69a16db1078e30d454e891af1`, carried by the website as PROPOSAL_PREVIEW. Preserve that provenance and avoid presenting candidate slogans as already approved or deployed copy.

Generated by AI Architect · https://www.frankx.ai/ai-architect
