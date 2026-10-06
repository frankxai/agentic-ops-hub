# Frontier landscape: agent security and always-on agents (compiled 2026-10-05)

## Method and caveats (read first)

- Tags: **[P]** = page fetched and read this session (primary). **[S]** = seen only in a search-result summary, page not fetched. Treat [S] as a lead to verify, not a fact.
- The sandbox egress proxy blocked these primary hosts, so their content is [S] or absent: genai.owasp.org, modelcontextprotocol.io (spec pages), docs.github.com, github.blog, developers.openai.com, vercel.com (docs read through the Vercel docs-search tool instead), ycombinator.com, cursor.com, docs.devin.ai, docs.openclaw.ai, techcrunch.com, fortune.com. GitHub repo metadata came from the GitHub search API on 2026-10-05 (stars, license, last push are exact for that day).
- Vendor docs pages carry no publish date. "Live doc 2026-10-05" means the page said this on the day I read it.
- Pricing for Devin, Cursor, Codex and Jules comes from third-party blogs ([S], low confidence). Anthropic pricing is [P].

---

## 1. Agent-security standards (2025-2026)

### 1a. OWASP and MCP

| Item | What it says | Source | Date | Tag |
|---|---|---|---|---|
| OWASP Top 10 for Agentic Applications 2026 | First edition, ASI01-ASI10: Agent Goal Hijack, Tool Misuse and Exploitation, Identity and Privilege Abuse, Agentic Supply Chain, Unexpected Code Execution (RCE), then memory poisoning, inter-agent communication, cascading failures, human-agent trust, rogue agents. 100+ contributors. | https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026 (official page https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ not reachable) | announced 2025-12-09 | S |
| OWASP Top 10 for LLM Applications 2026 | Published 2026-08-04. Same 10 areas as 2025, 8 moved, 1 renamed. Order: Prompt Injection, Sensitive Information Disclosure, Excessive Agency (up to #3), Supply Chain, Data and Model Poisoning, Unbounded Consumption, Misinformation, Hidden Context Exposure, Vector and Embedding Weaknesses, Improper Output Handling. First list to mix votes (75%) with incident data (25%). | https://www.helpnetsecurity.com/2026/08/06/owasp-2026-llm-top-10-released/ | 2026-08-06 article | S |
| OWASP MCP Security Cheat Sheet | Cheat sheet for MCP: confused deputy, token passthrough, tool poisoning, SSRF via connectors, rogue server registration. | https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html | undated | S |
| MCP spec 2025-11-25 | Client ID Metadata Documents replace reliance on Dynamic Client Registration; SEP-1024 client security requirements for local server install (consent, visibility); SEP-835 default scopes; SEP-990 enterprise IdP policy (cross-app access); SEP-1036 URL-mode elicitation so credentials never transit the client; Tasks (experimental). | https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ | 2025-11-25 | P |
| MCP spec 2026-07-28 (current) | Stateless core: no `initialize` handshake, no `Mcp-Session-Id`. Authorization hardening: clients must validate `iss` (RFC 9207), declare OIDC `application_type`, bind credentials to the authorization server, re-register on resource migration. New `Mcp-Method`/`Mcp-Name` headers (server rejects header/body mismatch). Roots, Sampling and Logging deprecated. RC locked 2026-05-21. | https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ | 2026-07-28 | P |
| MCP Enterprise-Managed Authorization | Extension declared stable ("zero-touch OAuth"). | https://blog.modelcontextprotocol.io/posts/ (index) | 2026-06-18 | P (index only) |
| MCP roadmap | Updated roadmap post. | https://blog.modelcontextprotocol.io/posts/ (index) | 2026-08-22 | P (index only) |
| MCP security best-practices page | Normative page in the spec repo (confused deputy, token passthrough, session hijack, scope minimization). Content not read. | https://modelcontextprotocol.io/specification/draft/basic/security_best_practices | draft | unread |
| Tool poisoning research | Peer-reviewed/preprint threat model of prompt injection through tool metadata. Tool poisoning is a research finding, not a spec requirement. | https://arxiv.org/html/2603.22489v1 | 2026-03 | S |

### 1b. Anthropic (Claude Code, Agent SDK, Managed Agents)

| Item | What it says | Source | Date | Tag |
|---|---|---|---|---|
| Claude Code security | Auto mode (separate classifier model reviews actions) is the default start mode for interactive terminal and VS Code sessions; Manual mode starts read-only. Sandboxed bash with filesystem and network isolation. `curl`/`wget` never auto-approved. Fail-closed command matching. WebFetch summarised by a second model call. `ConfigChange` hooks can audit or block settings changes. Anthropic reviews connectors but does not audit MCP servers. | https://code.claude.com/docs/en/security | live doc 2026-10-05 | P |
| Auto mode engineering post | Two layers: server-side prompt-injection probe on tool outputs, and a transcript classifier (Sonnet 4.6) on each action. Numbers: 0.4% false-positive on 10,000 real actions; 17% false-negative on 52 real overeager actions; 5.7% false-negative on 1,000 synthetic exfiltration cases. Halts after 3 consecutive or 20 total denials. Anthropic itself says 17% is acceptable only versus skipping permissions entirely. | https://anthropic.com/engineering/claude-code-auto-mode | 2026-03-25 | P |
| Auto-mode bypass research | Indirect prompt injection against Claude Code on Opus 5 with auto mode. | https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/ | 2026 (exact date unknown) | S |
| Secure deployment guide (Agent SDK) | Threat model: prompt injection or model error. Proxy pattern: credentials live outside the agent boundary, proxy injects them. Isolation ladder: sandbox-runtime (bubblewrap/Seatbelt, shares host kernel, no TLS inspection, domain fronting possible), Docker hardened (`--cap-drop ALL`, `--network none`, Unix-socket proxy), gVisor, Firecracker VMs over vsock. Warns that read-only mounts still expose `.env`, `~/.aws`, `.npmrc`. | https://code.claude.com/docs/en/agent-sdk/secure-deployment | live doc 2026-10-05 | P |
| Sandbox runtime (open source) | OS-level fs and network restriction for Bash only. File tools, MCP servers and hooks run outside it. Not available on native Windows. | https://code.claude.com/docs/en/sandboxing ; https://github.com/anthropics/sandbox-runtime | live doc 2026-10-05 | P |
| Cloud sessions security | Isolated Anthropic VM per session; network limited by default (Trusted allowlist); GitHub credentials never enter the VM (proxy attaches them); proxy rejects branch deletions and tag pushes; audit logging. Warns that a PR comment reply by auto-fix can trigger `issue_comment` automation. | https://code.claude.com/docs/en/claude-code-on-the-web | live doc 2026-10-05 | P |
| Managed Agents vaults | `environment_variable` credentials are stored in the sandbox as opaque placeholders and substituted at egress; scope with `networking.allowed_hosts` and `injection_location` (header only is the narrow setting). Gap: exchange flows (OAuth client-credentials) return real tokens into the sandbox. Max 20 credentials per vault. | https://platform.claude.com/docs/en/managed-agents/vaults | live doc 2026-10-05 | P |
| Routine fire-payload handling | Text sent to a routine's `/fire` endpoint is wrapped in `<routine-fire-payload>` and labelled untrusted data; the saved prompt must opt in to acting on it. Routines run with no permission-mode picker and all included connectors usable without approval. | https://code.claude.com/docs/en/routines | live doc 2026-10-05 | P |

### 1c. OpenAI, GitHub, Vercel

| Item | What it says | Source | Date | Tag |
|---|---|---|---|---|
| OpenAI "Safety in building agents" | Keep untrusted data away from driving agent behaviour; extract only structured fields from external input; guardrails nodes (PII, moderation, jailbreak/prompt-injection detection) are not sufficient alone. | https://developers.openai.com/api/docs/guides/agent-builder-safety | undated | S |
| OpenAI guardrails bypass | Research showing LLM-judge guardrails fall to the same injection as the model they police. | https://www.hiddenlayer.com/research/same-model-different-hat ; https://labs.zenity.io/p/breaking-down-agentkit-s-guardrails | 2025 (exact dates unknown) | S |
| GitHub Copilot cloud agent risks and mitigations | Only users with write access can trigger the agent; comments from users without write access never reach it; hidden characters (HTML comments) stripped; firewall, env filtering, secret scanning. Research found env filtering bypassable via `ps auxeww` on the parent process (RoguePilot). | https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations ; https://orca.security/resources/blog/roguepilot-github-copilot-vulnerability/ | undated | S |
| GitHub Actions: `actions/checkout` v7 | Refuses to check out fork PR code under `pull_request_target` and `workflow_run` unless `allow-unsafe-pr-checkout: true`. Effective 2026-06-18; backported to v3-v6 on 2026-07-16. | https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/ ; https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html | 2026-06-18 / 2026-07-16 | S |
| GitHub Actions hardening baseline | Pin third-party actions to full SHA (tags are movable: tj-actions, trivy-action); read-only default `GITHUB_TOKEN`; OIDC over long-lived cloud secrets; avoid `pull_request_target` on public repos. Only trivy-action v0.35.0 survived tag poisoning because it was an immutable release. | https://www.wiz.io/blog/github-actions-security-guide ; https://phoenix.security/trivy-supply-chain-attack-team-pcp/ | 2026-03 | S |
| Vercel Deployment Protection | Vercel Authentication (SSO) scopes: all, preview, or prod URLs plus previews; password protection (eligible plans); automation bypass secret sent as `x-vercel-protection-bypass` header (`VERCEL_AUTOMATION_BYPASS_SECRET`); a dedicated "automated agent access" page exists. | https://vercel.com/docs/deployment-protection/automated-agent-access ; https://vercel.com/docs/security/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation | live docs 2026-10-05 | P (via docs search) |
| Vercel Firewall and bots | Custom rules (deny, challenge, log, bypass, rate_limit, redirect) via CLI/API; Attack Mode (1h/6h/24h); system DDoS mitigations. Bot Protection managed ruleset in challenge mode skips verified bots. Separate AI-bots managed ruleset is inactive by default. Verified-bot directory checks IP, reverse DNS and signatures. | https://vercel.com/docs/vercel-firewall ; https://vercel.com/changelog/bot-protection-is-now-generally-available ; https://vercel.com/docs/vercel-firewall/vercel-waf/managed-rulesets | live docs 2026-10-05 | P/S mix |
| Vercel Sandbox network policy | `deny-all` or `custom` mode with `allowedDomains`, `allowedCIDRs`, `deniedCIDRs`, and `injectionRules` (credential header injection per domain). Isolated microVM. | https://vercel.com/docs/sandbox/cli-reference ; https://vercel.com/docs/rest-api/sdk/sandboxes/update-network-policy | live docs 2026-10-05 | P (via docs search) |

---

## 2. Always-on agent infrastructure

| Platform | Persistence and scheduling | Isolation | Cost model | Source | Date | Tag |
|---|---|---|---|---|---|---|
| Anthropic Managed Agents | Stateful sessions (history, filesystem, outputs stored server-side). Scheduled deployments: POSIX cron plus IANA timezone, minute granularity, jitter up to 15% of interval (max 9 min), 1,000 per org, per-run budget cap, pause/unpause/archive, run records and webhooks. Memory stores, vaults. "Dreaming" and MCP tunnels are research preview. | Anthropic-managed cloud sandbox, or self-hosted sandbox. Not eligible for ZDR or HIPAA BAA. | Tokens at model rates plus $0.08 per session-hour (only `running` time). Web search $10 per 1,000. No Batch discount. Public beta (header `managed-agents-2026-04-01`); launch reported 2026-04-08. | https://platform.claude.com/docs/en/managed-agents/overview ; .../scheduled-deployments ; https://platform.claude.com/docs/en/about-claude/pricing | live docs 2026-10-05 | P |
| Claude Code cloud sessions | Survive laptop closing; move with `--cloud` and `--teleport`; `claude -p ... --cloud <id>` queues follow-ups. VM reclaimed after inactivity; history restored, background processes not. | Isolated Anthropic VM per session, or self-hosted environment; Trusted-network default. | Counts against subscription limits; "no separate compute charge". Pro, Max, Team, Enterprise (premium seats). | https://code.claude.com/docs/en/claude-code-on-the-web | live doc 2026-10-05 | P |
| Claude Code Routines (research preview) | Triggers: schedule (min interval 1 hour, one-off allowed), API POST (`/fire`, per-routine bearer token, beta header `experimental-cc-routine-2026-04-01`), GitHub (pull_request, release). Limits: 100 scheduled runs/hour per account, 30 manual-or-API fires/hour per routine. Green status means infra started, not that the task worked. | Full cloud session; no permission picker; connectors all enabled by default. | Subscription usage; overage only with usage credits. | https://code.claude.com/docs/en/routines | live doc 2026-10-05 | P |
| OpenAI AgentKit, ChatKit, Agents SDK | AgentKit (Agent Builder visual canvas, ChatKit, Guardrails, Evals, Connector Registry) announced at DevDay 2025-10-06: ChatKit and Evals GA, Agent Builder beta, Connector Registry limited beta. Agents SDK update 2026-04-15 added native sandbox execution (7 cloud providers), model-native harness, snapshotting and rehydration of long-running state; Python first. | Sandbox providers, not OpenAI-hosted VMs (as described). | Token pricing; no per-hour fee seen. | https://techcrunch.com/2025/10/06/openai-launches-agentkit-to-help-developers-build-and-ship-ai-agents ; https://openai.com/index/the-next-evolution-of-the-agents-sdk/ ; https://www.helpnetsecurity.com/2026/04/16/openai-agents-sdk-harness-and-sandbox-update/ | 2025-10-06 / 2026-04-15 | S |
| OpenAI Codex cloud | Per-task cloud environment preloaded with the repo. Bundled into ChatGPT plans: Plus $20 (10-60 cloud tasks and 20-50 reviews per 5-hour window), Pro $100/$200, Business $25/user. Credit-based token metering. Internet-access policy not confirmed. | Separate cloud environment per task. | Plan-bundled plus credits. | https://www.eesel.ai/blog/openai-codex-pricing ; https://www.morphllm.com/codex-pricing | 2026 (undated) | S, low confidence |
| Nous Research Hermes Agent | Persistent memory, self-created skills, cron scheduling where jobs carry output into later runs, 20+ messaging platforms, six terminal backends (local, Docker, SSH, Singularity, Modal, Daytona) plus a Vercel Sandbox backend, isolated profiles, MCP, automatic migration from OpenClaw. MIT. 251,416 stars. Latest tag v0.21.5 (2026-09-24, ~460 PRs rolled up). | Whatever backend you pick; local backend has no sandbox. | Free software; you pay hosting and model costs. | https://github.com/NousResearch/hermes-agent/releases ; https://vercel.com/docs/sandbox/ecosystem/hermes | 2026-09-24 | P |
| OpenClaw | Self-hosted gateway daemon; heartbeat reads `HEARTBEAT.md` every 30 min by default; 20+ channels (Discord, Slack, Telegram, WhatsApp, iMessage...); skills run arbitrary code; sandboxing guide. MIT, 391k stars, stewarded by an independent 501(c)(3) foundation. | Optional sandbox; default is your host. See incidents (ClawHavoc, CVE-2026-25253). | Free; model costs. | https://github.com/openclaw/openclaw ; https://nebius.com/blog/posts/openclaw-security | 2026-10-05 | P (repo) / S (heartbeat) |
| Devin (Cognition) | Cloud VM agent with scheduled tasks and parallel sessions. New pricing from 2026-04-14: Free, Pro $20, Max $200, Teams $80 minimum plus $40 seats, Enterprise; self-serve moved from ACUs to dollar quota plus on-demand credits (1 ACU about 15 minutes of work). Conflicting older figure of $500 for 250 ACUs seen. Cognition raised $2B+ Series E at $48B on 2026-09-08. | Per-session cloud VM. | Subscription plus usage. | https://pensero.ai/blog/devin-pricing ; https://techcrunch.com/2026/09/08/cognition-hits-48b-valuation-signaling-investors-believe-ai-coding-is-far-from-a-winner-take-all-market/ | 2026-04-14 / 2026-09-08 | S |
| Cursor cloud agents and Automations | Each cloud agent gets its own Linux VM with browser and desktop and returns a PR with video/screenshots (Feb 2026 "computer use" update). Automations trigger agents from GitHub PRs, Slack, PagerDuty. TypeScript SDK with sandboxed cloud VMs, subagents, hooks, token pricing (2026-04-29). Plans as of 2026-08-31: Pro $20, Pro+ $60, Ultra $200, Teams $40/user. | Dedicated VM per agent. | Plan plus API-rate usage. | https://www.marktechpost.com/2026/04/29/cursor-introduces-a-typescript-sdk-for-building-programmatic-coding-agents-with-sandboxed-cloud-vms-subagents-hooks-and-token-based-pricing/ ; https://www.morphllm.com/cursor-background-agents | 2026-04-29 / 2026-08-31 | S |
| Google Jules and Antigravity | Jules: async tasks; free 15 tasks per 24h, Pro about $19.99 (100/day), Ultra tiers; scheduled tasks reported. Antigravity: agent-first IDE, CLI and agent manager; no standalone plan, rides Google AI Pro $19.99 / Ultra $99.99 / $199.99; repriced 2026-05-19. Antigravity agent API page exists but was not readable. | Jules runs in cloud VMs (not verified). | Google AI subscription tiers. | https://www.cloudzero.com/blog/google-antigravity-pricing/ ; https://ai.google.dev/gemini-api/docs/antigravity-agent | 2026-05-19 | S, low confidence |

---

## 3. Open-source agent-security tooling

Stars, license and last push from the GitHub search API on 2026-10-05 [P] unless a note says otherwise.

| Category | Repo | License | Stars | Last push | Note |
|---|---|---|---|---|---|
| MCP/skill scanner | https://github.com/snyk/agent-scan | Apache-2.0 | 3,111 | 2026-10-05 | "Security scanner for AI agents, MCP servers and agent skills". Lineage: Invariant Labs `mcp-scan`; Snyk acquired Invariant in June 2025 [S: https://www.startupticker.ch/en/news/snyk-acquires-invariant-labs-to-accelerate-agentic-ai-security-innovation]. The `invariantlabs-ai/mcp-scan` repo did not resolve in search; I could not confirm a rename. |
| MCP scanner | https://github.com/cisco-ai-defense/mcp-scanner | Apache-2.0 | 1,084 | 2026-10-05 | Scans MCP servers for threats. |
| Skill scanner | https://github.com/cisco-ai-defense/skill-scanner | NOASSERTION | 2,574 | 2026-10-05 | Scanner for agent skills; directly relevant to a skills-heavy estate. |
| Secrets | https://github.com/gitleaks/gitleaks | MIT | 29,700 | 2026-09-30 | |
| Secrets | https://github.com/trufflesecurity/trufflehog | AGPL-3.0 | 28,290 | 2026-10-05 | Verifies whether found credentials are live. |
| Actions static analysis | https://github.com/zizmorcore/zizmor | MIT | 6,639 | 2026-10-05 | Finds `pull_request_target`/template-injection patterns. |
| Actions linting | https://github.com/rhysd/actionlint | MIT | 4,295 | 2026-07-16 | Syntax and type checks, not a security scanner. |
| Actions runtime | https://github.com/step-security/harden-runner | Apache-2.0 | 1,277 | 2026-10-05 | Egress monitoring/blocking on runners. |
| Supply chain posture | https://github.com/ossf/scorecard | Apache-2.0 | 5,738 | 2026-10-02 | |
| Vuln/secret/IaC scanner | https://github.com/aquasecurity/trivy | Apache-2.0 | 38,244 | 2026-10-02 | Its GitHub Action was tag-poisoned 2026-03-19; pin by SHA (see section 6). |
| Prompt-injection model | https://github.com/meta-llama/PurpleLlama (Llama Prompt Guard 2, 86M and 22M) | NOASSERTION | 4,419 | 2026-09-29 | mDeBERTa-based classifiers; 512-token context. PINT benchmark figures (Lakera 98.1%, Prompt Guard 90.4%) are vendor-adjacent [S: https://appsecsanta.com/lakera]. |
| Prompt-injection / input scanners | https://github.com/protectai/llm-guard | MIT | 3,213 | 2026-07-08 | One source says the codebase is frozen after Palo Alto bought Protect AI; verify before depending on it. |
| Prompt-injection detector | https://github.com/protectai/rebuff | Apache-2.0 | 1,526 | 2024-08-07 | Stale. Do not use. |
| Prompt-injection (commercial) | Lakera Guard | closed | n/a | n/a | Acquired by Check Point, now "Check Point AI Guardrails" [S: https://www.securityweek.com/check-point-to-acquire-ai-security-firm-lakera/]. |
| LLM red-team | https://github.com/promptfoo/promptfoo | MIT | 25,728 | 2026-10-05 | Red teaming and eval of prompts/agents/RAG. |
| LLM red-team | https://github.com/NVIDIA/garak | Apache-2.0 | 9,438 | 2026-10-02 | |
| LLM red-team | https://github.com/microsoft/PyRIT | MIT | 4,579 | 2026-10-05 | |
| Policy | https://github.com/open-policy-agent/opa | Apache-2.0 | 12,324 | 2026-10-05 | General policy engine. |
| Policy | https://github.com/cedar-policy/cedar | Apache-2.0 | 1,763 | 2026-10-05 | Authorization language; fits per-tool allow/deny. |
| Sandbox | https://github.com/google/gvisor | Apache-2.0 | 19,551 | 2026-10-05 | Userspace kernel; strong isolation, 10-200x slower on heavy file I/O (Anthropic guide). |
| Sandbox | https://github.com/firecracker-microvm/firecracker | Apache-2.0 | 37,178 | 2026-10-05 | microVMs, boots under 125 ms (Anthropic guide). |
| Sandbox | https://github.com/e2b-dev/E2B | Apache-2.0 | 14,182 | 2026-10-05 | Hosted agent sandboxes; one billion starts by 2026-06-03 [S: https://bex.co/blog/2026/09/11/ai-sandbox-funding-modal-daytona-e2b]. |
| Sandbox | https://github.com/daytonaio/daytona | none detected by API | 71,649 | 2026-07-24 | Reported to have moved its production codebase to closed source in June 2026; public repo frozen at the last AGPL-3.0 release, community fork `nightona-co/nightona` [S: https://bex.co/blog/2026/09/12/daytona-closed-source-agent-sandbox-oss-risk]. |
| Sandbox | https://github.com/vercel/sandbox | Apache-2.0 | 208 | 2026-09-30 | SDK/CLI for Vercel Sandbox microVMs. |
| Sandbox (Anthropic) | https://github.com/anthropics/sandbox-runtime | not queried | not queried | n/a | Referenced by the Agent SDK secure-deployment guide [P]. |

---

## 4. YC and VC signal (2025-2026)

### 4a. YC companies

Batch labels follow what the source states. YC renamed batches (Spring, Summer, Fall); "P26"/"X26" labels appear in third-party lists. Source for most S26 rows is a search summary of YC directory pages [S].

| Company | Batch | What it does | Source |
|---|---|---|---|
| Silmaril | Spring 2026 (P26) | Runtime firewall for agents: blocks prompt injection, context poisoning, dangerous tool calls in ~20 ms; retrains on new attacks. Claims 96% blocked vs 61% for leading guardrails (self-reported). | https://www.ycombinator.com/companies/silmaril |
| Arga Labs | Spring 2026 (Demo Day 2026-06-16) | Digital-twin sandboxes of SaaS APIs (Stripe, Slack) for testing agents. $10M seed led by General Catalyst. | https://techcrunch.com/2026/06/18/the-11-standout-startups-from-ycs-demo-day-according-to-vcs/ ; https://pulse2.com/arga-labs-raises-10-million-seed-funding-as-ai-agent-simulator-clones-saas-environments-in-under-12-hours/ |
| Indexable | Spring 2026 (P26) | Agent sandboxes that fork a live environment (files, processes, memory) in ~26 ms; custom KVM VMM. | https://ycombinator.com/companies/indexable |
| Blaxel | Spring 2025 | Perpetual microVM sandboxes that hibernate to zero cost and resume under 25 ms; $7.3M seed led by First Round. | https://blaxel.ai/ai-information.md |
| Inkbox | Summer 2026 | Identity for agents: own email, phone, iMessage, 2FA vault. | https://yespress.io/inkbox-yc-s26 |
| OneCLI | Summer 2026 | Identity gateway: agents see placeholder tokens, real secrets injected at the network layer (same pattern as Managed Agents vaults). | https://lemstudio.co/yc-companies/onecli-33320 |
| Agentcard | Summer 2026 | Single-use virtual cards for agent purchases. | search summary of YC S26 list |
| Archal | Summer 2026 | Sandboxes with API environments for CI, tests, evals. | search summary of YC S26 list |
| HyperProbe | Summer 2026 | Lets coding agents drop non-breaking probes into running services to debug live. | https://lemstudio.co/yc-companies/hyperprobe-33177 |
| Trident | Summer 2026 | Agentic pentester that chains vulnerabilities into verified attack paths. | search summary of YC security list |
| Agnost AI | Summer 2026 | Reads agent conversations to find silent failures; builds custom models. | search summary of YC monitoring list |
| Magma | Summer 2026 | Monetizes agent traces. | search summary of YC list |
| Mem0 | Summer 2024 | Memory layer for agents; $24M seed plus Series A (Basis Set lead); 41k stars at Oct 2025 per TechCrunch, now 66,606. | https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps |
| Laminar | Summer 2024 | Open-source observability and evals for agents. | https://www.ycombinator.com/companies/laminar |
| Langfuse | Winter 2023 | LLM tracing and evals; acquired by ClickHouse January 2026. | https://www.ycombinator.com/companies/langfuse |
| Helicone | Winter 2023 | Open-source LLM observability gateway. | https://ycombinator.com/companies/helicone |
| Respan | Winter 2024 | Control plane to trace and evaluate agents. | search summary of YC monitoring list |

Excluded: Maritime ("Fall 2026 batch, founded September 2026") because the dates look wrong for 2026-10-05.

### 4b. Funding rounds and M&A (agent security and infra)

| Date | Company | Event | Source | Tag |
|---|---|---|---|---|
| 2026-09-08 | Cognition (Devin) | $2B+ Series E at $48B valuation (a16z, Accel lead). Earlier: $1B at $25B pre-money on 2026-05-27. | https://techcrunch.com/2026/09/08/cognition-hits-48b-valuation-signaling-investors-believe-ai-coding-is-far-from-a-winner-take-all-market/ | S |
| 2026-09-29 | Reco | $55M raise, total $140M; TechCrunch headline says AI agent security startups "crowd the market". | https://techcrunch.com/2026/09/29/reco-raises-55m-as-ai-agent-security-startups-crowd-the-market/ | S |
| 2026-09-17 | Comp AI | $34M Series A (agentic compliance; adjacent, not agent security). | https://techcrunch.com/2026/09/17/comp-ai-sets-eyes-on-a-continiously-agentic-future-for-security-and-complaince/ | S |
| 2026-05 | Modal | $355M Series C, $4.65B valuation (Redpoint, General Catalyst). | https://bex.co/blog/2026/09/11/ai-sandbox-funding-modal-daytona-e2b | S |
| 2026-05-28 | Geordie AI | $30M Series A, security and governance for agents. | https://fortune.com/2026/05/28/geordie-security-governance-ai-agents/ | S |
| 2026-02 | Daytona | $24M Series A led by FirstMark. | https://bex.co/blog/2026/09/11/ai-sandbox-funding-modal-daytona-e2b | S |
| 2026-01-13 | WitnessAI | $58M led by Sound Ventures. | https://www.prnewswire.com/news-releases/witnessai-raises-58-million-for-global-expansion-and-announces-new-ways-to-secure-ai-agents-302659319.html | S |
| 2025-10-28 | Mem0 | $24M total (seed plus Series A). | https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps | S |
| 2025-07 | Noma Security | $100M Series B led by Evolution Equity Partners. | https://www.securityweek.com/noma-security-raises-100-million-for-ai-security-platform/ | S |
| 2025-07 | E2B | $21M Series A led by Insight Partners. | https://bex.co/blog/2026/09/11/ai-sandbox-funding-modal-daytona-e2b | S |
| 2025-06 | Browserbase | $40M Series B at $300M post-money (Notable Capital). No later round found. | https://sacra.com/c/browserbase | S |
| M&A | Snyk/Invariant Labs (2025-06); Palo Alto/Protect AI (closed 2025-07-22); SentinelOne/Prompt Security (2025-08); CrowdStrike/Pangea (2025-09); Check Point/Lakera (2025-09); ClickHouse/Langfuse (2026-01); Cisco/Astrix (announced 2026-05-04). | https://pipelab.org/blog/ai-agent-security-acquisition-wave-2026/ | S |

Reading: standalone prompt-injection filters (Lakera, Protect AI, Prompt Security) were absorbed within about a year. The surviving standalone categories are agent identity and credential brokering, sandboxes, and runtime policy.

---

## 5. Top open-source agent projects by traction

Stars, license and last-push date from the GitHub search API on 2026-10-05 [P]. "Last push" is not "last release"; I did not read release pages except Hermes (v0.21.5, 2026-09-24).

| Repo | Stars | License | Last push | Category |
|---|---|---|---|---|
| openclaw/openclaw | 391,442 | MIT | 2026-10-05 | Personal always-on agent gateway |
| affaan-m/ECC | 273,565 | MIT | 2026-10-05 | Agent harness: skills, instincts, memory |
| NousResearch/hermes-agent | 251,416 | MIT | 2026-10-05 | Self-improving agent, cron, memory |
| anomalyco/opencode | 211,876 | MIT | 2026-10-05 | Terminal coding agent |
| n8n-io/n8n | 206,725 | NOASSERTION (fair-code) | 2026-10-05 | Workflow automation with agents |
| langgenius/dify | 157,895 | NOASSERTION | 2026-10-05 | Agentic workflow and RAG platform |
| anthropics/claude-code | 149,513 | none stated | 2026-10-05 | Coding agent |
| langchain-ai/langchain | 147,476 | MIT | 2026-10-05 | Agent framework |
| openai/codex | 127,937 | Apache-2.0 | 2026-10-05 | Coding agent CLI |
| browser-use/browser-use | 117,205 | MIT | 2026-10-03 | Browser agents |
| google-gemini/gemini-cli | 107,238 | Apache-2.0 | 2026-10-05 | Coding agent CLI |
| thedotmack/claude-mem | 96,574 | Apache-2.0 | 2026-10-05 | Session memory for agents |
| modelcontextprotocol/servers | 91,022 | NOASSERTION | 2026-10-05 | Reference MCP servers |
| OpenHands/OpenHands | 90,046 | MIT | 2026-10-05 | Coding agent platform |
| ruvnet/ruflo | 73,931 | MIT | 2026-10-05 | Swarm harness (claude-flow lineage, unverified) |
| cline/cline | 69,890 | Apache-2.0 | 2026-10-05 | Coding agent SDK/IDE/CLI |
| mem0ai/mem0 | 66,606 | Apache-2.0 | 2026-10-05 | Memory layer |
| microsoft/autogen | 61,265 | CC-BY-4.0 | 2026-04-15 | Framework; no push since April |
| crewAIInc/crewAI | 59,373 | MIT | 2026-10-05 | Multi-agent framework |
| aaif-goose/goose | 54,966 | Apache-2.0 | 2026-10-05 | Coding agent (moved under Agentic AI Foundation) |
| Aider-AI/aider | 49,385 | Apache-2.0 | 2026-05-22 | Pair-programming agent; slowing |
| langchain-ai/langgraph | 42,744 | MIT | 2026-10-05 | Stateful agent graphs |
| agno-agi/agno | 42,566 | Apache-2.0 | 2026-10-05 | Agent runtime |
| langfuse/langfuse | 35,405 | NOASSERTION | 2026-10-05 | Observability and evals |
| getzep/graphiti | 31,456 | Apache-2.0 | 2026-10-05 | Temporal knowledge-graph memory |
| openai/openai-agents-python | 29,846 | MIT | 2026-10-05 | Agents SDK |
| huggingface/smolagents | 29,689 | Apache-2.0 | 2026-09-30 | Code-writing agents |
| mastra-ai/mastra | 28,574 | NOASSERTION | 2026-10-05 | TypeScript agent framework |
| promptfoo/promptfoo | 25,728 | MIT | 2026-10-05 | Evals and red teaming |
| letta-ai/letta | 25,029 | Apache-2.0 | 2026-09-10 | Stateful agents with memory |
| google/adk-python | 21,713 | Apache-2.0 | 2026-10-05 | Agent Development Kit |
| pydantic/pydantic-ai | 20,420 | MIT | 2026-10-05 | Typed agent framework |
| UKGovernmentBEIS/inspect_ai | 2,942 | MIT | 2026-10-05 | Eval harness |

Flag: `deepseek-ai/deepseek-harness` (243,972 stars, MIT, pushed 2026-10-03) and `DietrichGebert/ponytail` (155,910) appear in the API results; I did not verify them and star counts that high on young repos deserve a sanity check before you cite them.

---

## 6. Incidents (2025-2026)

| Date | Incident | What happened | Source | Tag |
|---|---|---|---|---|
| 2025-07-17 (pulled 07-19) | Amazon Q Developer VS Code extension 1.84.0 | A malicious commit into the open-source repo put a prompt in the extension telling the agent to wipe local files and AWS resources. Payload failed because of formatting errors. AWS issued an advisory; 1.85.0 replaced it. | https://www.theregister.com/2025/07/24/amazon_q_ai_prompt/ | S |
| 2025-08-26 | Nx "s1ngularity" | Malicious `nx` versions live about 5 hours (4.6M weekly downloads). Payload ran local `claude`, `gemini` and `q` CLIs to inventory secrets; 2,349 credentials leaked to public GitHub repos. Root cause: workflow added 2025-08-21 where a crafted PR title injected code. | https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware ; https://thehackernews.com/2025/08/malicious-nx-packages-in-s1ngularity.html | S |
| 2025-09-17 / 09-25 | `postmark-mcp` on npm | First reported malicious MCP server. v1.0.16 added a BCC of every outgoing email to an attacker address; 15 clean versions first; ~1,643 downloads. | https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html ; https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/ | S |
| 2025-09 and 2025-11-24 | Shai-Hulud npm worms | Phished maintainers, post-install credential theft, self-propagating publishes. Wave 1: 500+ packages (CISA alert 2025-09-23). Wave 2: 700+ packages, 27,000+ malicious GitHub repos, ~14,000 secrets across 487 orgs. | https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem ; https://unit42.paloaltonetworks.com/npm-supply-chain-attack/ | S |
| 2025-11 (detected mid-Sep) | GTG-1002, AI-orchestrated espionage | Anthropic reports a state-linked group drove Claude Code instances as autonomous pentest agents against ~30 targets; AI did an estimated 80-90% of tactical work. | https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf | S |
| 2026-01-31 to 2026-02 | OpenClaw: CVE-2026-25253 and ClawHavoc | One-click RCE (CVSS 8.8): Control UI trusted a `gatewayUrl` query parameter and sent the gateway token to it; fixed in 2026.1.29. Koi Security found 341 of 2,857 ClawHub skills malicious (335 from one campaign, Atomic Stealer); later scans reported 824+ of 10,700+. 40,000+ exposed instances reported. | https://www.wiz.io/vulnerability-database/cve/cve-2026-25253 ; https://conscia.com/blog/the-openclaw-security-crisis/ | S |
| 2026-02-27 to 03-24 | Trivy action poisoning then LiteLLM | Account `hackerbot-claw` (self-described autonomous agent) exploited a `pull_request_target` misconfiguration in Trivy's workflow. On 2026-03-19 TeamPCP force-pushed 76 of 77 tags of `aquasecurity/trivy-action` with a credential stealer. A stolen PyPI token then published LiteLLM 1.82.7/1.82.8 on 2026-03-24; PyPI quarantined within ~3 hours; ~47,000 downloads. LiteLLM sits under CrewAI, DSPy and others. | https://phoenix.security/trivy-supply-chain-attack-team-pcp/ ; https://www.bleepingcomputer.com/news/security/popular-litellm-pypi-package-compromised-in-teampcp-supply-chain-attack/ ; https://www.helpnetsecurity.com/2026/03/25/teampcp-supply-chain-attacks/ | S |
| 2026-04-15 | "Comment and Control" | One prompt-injection pattern (PR titles, issue bodies, hidden HTML comments) leaked secrets from Claude Code Security Review, Gemini CLI Action and GitHub Copilot agent running in Actions. Three enabling conditions: untrusted GitHub text in the prompt, secrets in the runner, ability to post comments. Bounties: Anthropic $100 (CVSS 9.4), Google $1,337, GitHub $500 ("architectural limitation"). | https://github.com/vectara/awesome-agent-failures/blob/main/docs/case-studies/comment-and-control-prompt-injection.md [P] ; https://labs.cloudsecurityalliance.org/research/csa-research-note-comment-control-github-prompt-injection-20/ | P (case study), S (CSA) |
| 2026-05-07 | Semantic Kernel RCE | CVE-2026-26030 (Python in-memory vector store, `eval()` on model-controlled input, fixed in 1.39.4) and CVE-2026-25592 (.NET SessionsPythonPlugin arbitrary file write, fixed in 1.71.0). Lesson from Microsoft: the model is not a security boundary; tool parameters are attacker-controlled. | https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/ | P |
| 2026-01 and others | Agent-tool CVEs | claude-code-action permission bypass (`checkWritePermissions` trusted any GitHub App actor, CVSS 4.0 7.8, reported by RyotaK); Cursor CVE-2026-22708 (allowlisted commands such as `git branch` carry payloads); Codex CLI CVE-2025-59532 (agent output could redefine sandbox boundary). | https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/ ; https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026 | S |

---

## Decision-relevant reading for a 48-repo estate

1. The recurring failure is one pattern: untrusted text in a prompt, plus secrets in the same runner, plus a write channel. Comment and Control, Nx, Trivy and claude-code-action all fit it.
2. Pin every third-party Action by SHA and drop `pull_request_target` where you can; Trivy shows even security tooling is a supply-chain entry.
3. Credential brokering is converging: Managed Agents vaults, Vercel Sandbox `injectionRules`, OneCLI and Anthropic's proxy guidance all keep real secrets out of the agent.
4. Auto mode has a published 17% miss rate on real overeager actions; treat it as a speed tool and put network and filesystem limits underneath it.
5. Routines run with every connector enabled and no permission picker; trim connectors per routine.
6. Skill and MCP registries are now attack surface (ClawHub, postmark-mcp); `snyk/agent-scan` and `cisco-ai-defense/skill-scanner` are the open-source scanners to trial on your skills.
7. MCP 2026-07-28 changed authorization and removed sessions; re-check any MCP server you maintain against the new `iss` validation and header rules.
8. Standalone prompt-injection filters were mostly acquired; Rebuff is stale and LLM Guard may be frozen, so do not build on them.
9. Daytona's reported closed-sourcing is a reminder to prefer sandboxes with a supported open license (Firecracker, gVisor, E2B, Anthropic sandbox-runtime).
