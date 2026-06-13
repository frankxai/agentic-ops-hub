# Slack Agentic Operating Map

Created: 2026-06-12  
Workspace owner: Frank (`U09CE1K62AY`)  
Source of truth repo: `agentic-ops-hub`

This map connects Slack channels, local repos, and agentic teams so Codex, Claude, and future agents have a shared operating surface.

## Channel Inventory

| Channel | Slack ID | Role |
| --- | --- | --- |
| `#ops` | `C0B9M0AM2BZ` | Daily command center, blockers, cross-business decisions, end-of-day scans. |
| `#repo-command` | `C0BA49F2BRP` | Repo status, PRs, branches, build failures, sweep outputs, handoffs. |
| `#arcanea` | `C0ABKPJE74P` | Existing Arcanea channel. Keep Arcanea product and Linear status here. |
| `#agentic-creator-os` | `C0ABXNQN5E1` | Existing ACOS channel. Use for ACOS repo planning and skill/agent library work. |
| `#starlight-systems` | `C0BAWNP2C80` | Starlight system layer, cockpit, swarm, intelligence, devices, knowledge. |
| `#agentic-income` | `C0B9W3F3UEP` | Agentic Income, passive income, affiliate, DPI, revenue templates. |
| `#ai-coe` | `C0BA0C8G4UW` | AI Center of Excellence, academy, enterprise playbooks, AI architecture. |
| `#frankx-growth` | `C0B9M0EEJSK` | FrankX brand, public site, growth, campaigns, content, conversion. |
| `#creator-systems` | `C0BAWNSTAE4` | Creator workflows, Author OS, GenCreator, prompt systems, skill libraries. |
| `#reality-architect` | `C0B9W3JGJSF` | Reality Architect product, vault, mythology, knowledge product system. |
| `#anime-legends` | `C0BAWPYB1K2` | Anime Legends IP/product channel. |
| `#agent-teams` | `C0BA2FF6JTC` | Agent rosters, delegation patterns, ownership, handoffs, hiring/synthetic team design. |
| `#prompt-systems` | `C0B9M1NKSMD` | Prompt engines, prompt libraries, evals, reusable prompt infrastructure. |
| `#mcp-integrations` | `C0BA2FHNP2N` | MCP servers, LiteLLM, tool connectivity, integration health. |
| `#knowledge-systems` | `C0B9W4SNR0B` | Memory, vaults, knowledge trees, second brain, retrieval layers. |
| `#design-intelligence` | `C0B9W4TE5K5` | Design intelligence, visual intelligence, design agent skills. |
| `#revenue-ops` | `C0B9W4UKYP5` | Monetization, checkout, offers, analytics, affiliate and funnel operations. |
| `#content-comms` | `C0B9W4W4SLB` | Public updates, launches, social/content calendars, internal comms drafts. |

## Channel Topology

Use three layers of Slack channels:

1. Command channels: `#ops`, `#repo-command`, `#agent-teams`.
2. Business channels: `#arcanea`, `#agentic-creator-os`, `#starlight-systems`, `#agentic-income`, `#ai-coe`, `#frankx-growth`, `#creator-systems`, `#reality-architect`, `#anime-legends`.
3. Workflow channels: `#prompt-systems`, `#mcp-integrations`, `#knowledge-systems`, `#design-intelligence`, `#revenue-ops`, `#content-comms`.

Routing rule:
- If the work changes the business direction, post in the business channel.
- If the work changes code, branch, CI, deploy, or repo state, post in `#repo-command`.
- If the work changes the agent roster, ownership model, or delegation protocol, post in `#agent-teams`.
- If the work is a reusable capability across multiple businesses, post in the matching workflow channel.
- If the work blocks more than one business or needs Frank's decision, post in `#ops`.

## Repo Clusters

## Complete Repo Routing Table

| Repo | Primary channel | Secondary channel | Business / function |
| --- | --- | --- | --- |
| `affiliate-agent-skills` | `#agentic-income` | `#revenue-ops` | Affiliate skills and revenue automation. |
| `agentic-creator-skills` | `#creator-systems` | `#agent-teams` | Creator skill packs: brand, content, design, intelligence, product launch, music, visual studio. |
| `agentic-creator-os` | `#agentic-creator-os` | `#agent-teams` | ACOS capability system, commands, skills, agents. |
| `agentic-income-skills` | `#agentic-income` | `#revenue-ops` | Agentic income skill library. |
| `agentic-income-template` | `#agentic-income` | `#revenue-ops` | Reusable income product templates. |
| `agentic-ops-hub` | `#ops` | `#repo-command` | Agentic ops control plane and fleet map. |
| `agenticincome` | `#agentic-income` | `#revenue-ops` | Main Agentic Income property. |
| `agenticpassiveincome` | `#agentic-income` | `#revenue-ops` | Passive-income product/site. |
| `ai-architect-academy` | `#ai-coe` | `#content-comms` | AI architecture education. |
| `ai-coe` | `#ai-coe` | `#content-comms` | AI Center of Excellence. |
| `AnimeLegends` | `#anime-legends` | `#content-comms` | Anime Legends IP/product. |
| `arcanea-agent-skills` | `#arcanea` | `#agent-teams` | Arcanea agent skills. |
| `arcanea-ai-app` | `#arcanea` | `#repo-command` | Arcanea app. |
| `arcanea-claw` | `#arcanea` | `#agent-teams` | Arcanea agent/runtime layer. |
| `arcanea-ecosystem` | `#arcanea` | `#knowledge-systems` | Arcanea ecosystem docs and strategy. |
| `arcanea-orchestrator` | `#arcanea` | `#repo-command` | Arcanea orchestration layer. |
| `arcanea-studio` | `#arcanea` | `#content-comms` | Arcanea studio/product surface. |
| `author-os` | `#creator-systems` | `#content-comms` | Author workflow system. |
| `awesome-agentic-income` | `#agentic-income` | `#content-comms` | Curated market/research list. |
| `awesome-ai-coe` | `#ai-coe` | `#content-comms` | AI CoE curated list. |
| `awesome-cosmos-ai-agents` | `#ai-coe` | `#agent-teams` | Agent ecosystem research. |
| `awesome-design-agent-skills` | `#design-intelligence` | `#creator-systems` | Design-agent skill research. |
| `claude-code-config` | `#ops` | `#agent-teams` | Claude/Codex/Grok config layer. |
| `claude-code-hooks` | `#ops` | `#repo-command` | Hooks, gates, and lifecycle enforcement. |
| `claude-skills-library` | `#creator-systems` | `#agent-teams` | Reusable skill library. |
| `disruptivepassiveincome` | `#agentic-income` | `#revenue-ops` | DPI business/product. |
| `dpi` | `#agentic-income` | `#revenue-ops` | DPI implementation repo. |
| `FrankX` | `#frankx-growth` | `#content-comms` | FrankX brand and site/app surface. |
| `frankx.ai-vercel-website` | `#frankx-growth` | `#repo-command` | frankx.ai website. |
| `gencreator.ai` | `#creator-systems` | `#revenue-ops` | GenCreator product/site. |
| `hermes-cockpit` | `#starlight-systems` | `#repo-command` | Cockpit/control interface. |
| `kura` | `#frankx-growth` | `#content-comms` | Growth/content product. |
| `litellm-agent-platform` | `#mcp-integrations` | `#ai-coe` | LiteLLM agent platform/integration. |
| `mcp-doctor` | `#mcp-integrations` | `#ops` | MCP diagnostics and health. |
| `peak-performance` | `#ops` | `#repo-command` | Machine and developer environment health. |
| `prompt-engine` | `#prompt-systems` | `#creator-systems` | Prompt runtime/evaluation engine. |
| `prompt-library` | `#prompt-systems` | `#content-comms` | Prompt library and reusable assets. |
| `realityarchitect` | `#reality-architect` | `#content-comms` | Reality Architect product. |
| `realityarchitect-vault` | `#reality-architect` | `#knowledge-systems` | Reality Architect knowledge vault. |
| `second-brain-os` | `#knowledge-systems` | `#ops` | Personal/team memory substrate. |
| `sentinel-swarm-cockpit` | `#starlight-systems` | `#repo-command` | Sentinel cockpit. |
| `starlight-agent-skills` | `#starlight-systems` | `#agent-teams` | Starlight skill layer. |
| `starlight-command-center` | `#starlight-systems` | `#repo-command` | Command center. |
| `starlight-cosmos-engine` | `#starlight-systems` | `#knowledge-systems` | Cosmos engine. |
| `starlight-design-intelligence` | `#design-intelligence` | `#starlight-systems` | Design intelligence layer. |
| `starlight-devices` | `#starlight-systems` | `#repo-command` | Device integration. |
| `Starlight-Intelligence-System` | `#starlight-systems` | `#knowledge-systems` | Starlight intelligence/memory system. |
| `starlight-knowledge-tree` | `#knowledge-systems` | `#starlight-systems` | Knowledge tree. |
| `starlight-swarm` | `#starlight-systems` | `#agent-teams` | Starlight swarm and delegation. |
| `suno-mcp-server` | `#mcp-integrations` | `#content-comms` | Suno MCP/music integration. |
| `visual-intelligence` | `#design-intelligence` | `#starlight-systems` | Visual intelligence tooling. |
| `workflow-tier-plugin` | `#ops` | `#repo-command` | Workflow/plugin tier. |

### Ops And Agent Control Plane

Primary channels: `#ops`, `#repo-command`

Repos:
- `agentic-ops-hub`
- `claude-code-config`
- `claude-code-hooks`
- `mcp-doctor`
- `workflow-tier-plugin`
- `peak-performance`
- `second-brain-os`

Agent team:
- Operator: runs repo sweeps, tracks open loops, updates ledgers.
- Release manager: checks branches, CI, deploy readiness, and changelog gaps.
- Comms manager: turns sweeps into Slack updates and reply drafts.
- Safety reviewer: watches for destructive ops, secrets, and cross-repo drift.

### Arcanea

Primary channel: `#arcanea`

Repos:
- `arcanea-agent-skills`
- `arcanea-ai-app`
- `arcanea-claw`
- `arcanea-ecosystem`
- `arcanea-orchestrator`
- `arcanea-studio`

Agent team:
- Product lead agent: decisions, scope, roadmap.
- Build agent: implementation and PRs.
- Content/world agent: lore, studio, public-facing materials.
- Launch agent: Linear closure, changelog, deploy/readiness.

### Agentic Income

Primary channel: `#agentic-income`

Repos:
- `agentic-income-skills`
- `agentic-income-template`
- `agenticincome`
- `agenticpassiveincome`
- `affiliate-agent-skills`
- `awesome-agentic-income`
- `disruptivepassiveincome`
- `dpi`

Agent team:
- Offer architect: product ladder, pricing, templates.
- Affiliate operator: campaigns, partner assets, distribution.
- Revenue ops agent: checkout, Gumroad/Stripe, analytics, conversion.
- Research curator: updates awesome lists and market intelligence.

### Agentic Creator OS And Creator Systems

Primary channels: `#agentic-creator-os`, `#creator-systems`

Repos:
- `agentic-creator-skills`
- `agentic-creator-os`
- `author-os`
- `gencreator.ai`
- `prompt-engine`
- `prompt-library`
- `claude-skills-library`
- `awesome-design-agent-skills`

Agent team:
- Skill architect: skill taxonomy, quality bar, compatibility.
- Creator workflow agent: authoring, publishing, campaign workflows.
- Prompt evaluator: prompt tests, red-team checks, reusable patterns.
- Docs agent: onboarding, examples, release notes.

### Starlight Systems

Primary channel: `#starlight-systems`

Repos:
- `starlight-agent-skills`
- `starlight-command-center`
- `starlight-cosmos-engine`
- `starlight-design-intelligence`
- `starlight-devices`
- `Starlight-Intelligence-System`
- `starlight-knowledge-tree`
- `starlight-swarm`
- `hermes-cockpit`
- `sentinel-swarm-cockpit`
- `visual-intelligence`

Agent team:
- Systems architect: architecture, interfaces, memory protocol.
- Swarm coordinator: agent routing, delegation, handoffs.
- Device/cockpit agent: command surfaces and local operations.
- Visual intelligence agent: design/image/video intelligence workflows.

### AI CoE

Primary channel: `#ai-coe`

Repos:
- `ai-coe`
- `ai-architect-academy`
- `awesome-ai-coe`
- `awesome-cosmos-ai-agents`
- `litellm-agent-platform`

Agent team:
- Curriculum architect: academy modules, enterprise playbooks.
- Platform engineer: model gateway, evaluation, multi-model ops.
- Research curator: market scan, benchmarks, best practices.
- Client delivery agent: templates, workshops, implementation plans.

### FrankX Growth

Primary channel: `#frankx-growth`

Repos:
- `FrankX`
- `frankx.ai-vercel-website`
- `kura`
- `suno-mcp-server`

Agent team:
- Brand strategist: positioning, narrative, offers.
- Web agent: site implementation, SEO, analytics.
- Content agent: posts, campaigns, audio/video experiments.
- Conversion agent: landing pages, funnels, lead magnets.

### Reality Architect

Primary channel: `#reality-architect`

Repos:
- `realityarchitect`
- `realityarchitect-vault`

Agent team:
- Product/story architect: core doctrine and product packaging.
- Vault librarian: knowledge organization and retrieval.
- Experience agent: rituals, interfaces, journeys, publication assets.

### Anime Legends

Primary channel: `#anime-legends`

Repos:
- `AnimeLegends`

Agent team:
- IP/product agent: owns world, offer, format, and roadmap.
- Content agent: turns product beats into posts, scripts, and launch materials.
- Build agent: implements any app/site/game surface.
- Community agent: tracks audience feedback, channels, and release moments.

## Cross-Cutting Workflow Channels

### Agent Teams

Primary channel: `#agent-teams`

Owns:
- Agent rosters by business.
- Delegation trees.
- Role charters.
- Handoff contracts.
- Multi-agent process improvements.

Default roles every business should have:
- CEO/strategy agent: narrows priorities and decisions.
- Product/build agent: turns decisions into repo changes.
- Growth/comms agent: turns progress into external/internal updates.
- Ops/release agent: closes loops in repo state, changelog, docs, and Slack.
- Research/knowledge agent: maintains evidence, memory, and market context.

### Prompt Systems

Primary channel: `#prompt-systems`

Repos:
- `prompt-engine`
- `prompt-library`

Owns prompt assets, evals, reusable patterns, model instructions, red-team loops, and prompt distribution across businesses.

### MCP And Integrations

Primary channel: `#mcp-integrations`

Repos:
- `mcp-doctor`
- `suno-mcp-server`
- `litellm-agent-platform`

Owns tool connectivity, MCP health, model gateway experimentation, and integration diagnostics.

### Knowledge Systems

Primary channel: `#knowledge-systems`

Repos:
- `second-brain-os`
- `starlight-knowledge-tree`
- `Starlight-Intelligence-System`
- `realityarchitect-vault`

Owns durable memory, vaults, retrieval, taxonomies, and knowledge graph alignment across businesses.

### Design Intelligence

Primary channel: `#design-intelligence`

Repos:
- `starlight-design-intelligence`
- `visual-intelligence`
- `awesome-design-agent-skills`

Owns visual intelligence, design QA, design-agent capabilities, image/video analysis, and reusable design workflows.

### Revenue Ops

Primary channel: `#revenue-ops`

Owns:
- Product ladder and pricing.
- Stripe/Gumroad/checkout readiness.
- Affiliate systems.
- Lead magnets and conversion assets.
- Revenue analytics and experiment logs.

### Content Comms

Primary channel: `#content-comms`

Owns:
- Launch posts.
- Status updates.
- Email/social drafts.
- Public-facing release notes.
- Internal recap messages.

## Operating Protocol

Use `#ops` for:
- Daily priority decisions.
- Blockers that affect more than one business.
- Human approvals and strategy calls.
- End-of-day milestone scans.

Use `#repo-command` for:
- Repo status checks.
- Branch/PR/build/deploy reports.
- Cross-repo sweeps.
- Agent handoffs that include files, commands, or next prompts.

Use each business channel for:
- Business-specific roadmap and execution.
- Agent-team updates.
- Customer/content/product notes.
- Decisions that only affect that business.

## Agent Update Format

Every agent update should be short and structured:

```md
**Status**
- Shipped:
- Blocked:
- Next:

**Repos touched**
- `repo-name`: branch/commit/PR/status

**Decision needed**
- Owner:
- Deadline:
```

## Daily Cadence

Morning:
- `#ops`: choose the top 1-3 outcomes for the day.
- `#repo-command`: run a repo sweep if yesterday had active coding.

During work:
- Business channel: post meaningful decisions, blockers, or handoffs.
- `#repo-command`: post code/build/deploy state only when it changes.

End of day:
- `#ops`: summarize shipped, blocked, next.
- `#repo-command`: update ledger, changelog, and next prompts.

## Current Slack Triage Notes

As of 2026-06-12:
- Recent DM and direct mention search returned no hits for the last-week window.
- `#agentic-creator-os` has June 7 messages asking Codex/Claude to check GitHub status and align the repo/channel plan.
- `#arcanea` contains older automation posts repeatedly noting that `#ops` was missing. `#ops` now exists.
- Existing FrankX project channels were empty or inactive in the recent read.
