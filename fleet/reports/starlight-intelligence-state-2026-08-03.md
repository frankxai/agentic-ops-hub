# Starlight Intelligence System — Current-State and Interconnection Report

**As of:** 2026-08-03

**Audit owner:** Starlight Queen on Yoga Book 9i (`Starlight`)

**Evidence posture:** live local commands + canonical manifests + GitHub API/CLI + public HTTP probes

**Report home:** `frankxai/agentic-ops-hub` because this is a fleet/runtime alignment report, not a change to the SIS product substrate.

## Executive verdict

Starlight is already a substantial working estate, not a concept:

- The public Starlight protocol/site, FrankX, GenCreator, Arcanea, Academy, and Blue Life Commons surfaces are live.
- The canonical SIS repo contains a real TypeScript runtime, built MCP artifacts, 147 tracked agent markdown files, 92 tracked skill markdown files, 84 activation rules, and 121 Claude command files.
- The Yoga Book Hermes command center is operational: the gateway is running at login, Telegram is configured, 23 of 29 cron jobs are active, and the default agent uses OpenAI Codex.
- The estate control manifest classifies 118 repos across eight lanes; GitHub contains 349 repositories in total.

The main weakness is not lack of capability. It is **truth and wiring drift between capable parts**:

1. Hermes itself has no MCP servers registered, while Claude, Codex, Gemini, and OpenCode each expose different MCP states.
2. The canonical SIS MCPs are disabled in Codex and absent from Hermes/Gemini; a connected `starlight-bridge` still points outside the canonical repo estate.
3. C940 has no fresh, independently verified runtime receipt in the evidence inspected. Its public heartbeat is stale, its latest architecture PR remains draft, and 38 inherited Yoga Book→C940 tasks were pending with no result references before this audit enqueued one priority-0 consolidation request.
4. Syncthing is installed on Yoga Book but is not running; Tailscale is not installed. The mobile/fleet sync architecture is therefore documented, not operationally proved.
5. Public adoption is real but early: modest GitHub stars/forks and npm downloads, with almost no verified human contribution to the core repos.
6. Public install truth is inconsistent: SIS repo/docs say v8.3.0, the latest GitHub release is v8.2.1, and npm currently serves v6.0.1.

**Overall:** strong substrate and production web plane; mixed local runtime integration; red cross-machine alignment; early community adoption.

---

## 1. Observation boundary

This report distinguishes:

- **Observed:** proved by a live command, HTTP request, GitHub API, or current file read on Yoga Book.
- **Declared:** described in a checked-in manifest or guide but not proved running.
- **Scaffolded:** code or configuration exists but is disabled, incomplete, unauthenticated, or not published.
- **Unknown:** requires execution on C940 or a mobile device. Yoga Book must not forge that evidence.

The audit did not inspect or print credentials, private message bodies, private memory contents, or phone files. It did not recursively search `C:\`, the user profile, Phone Link, OnePlus/MTP, Desktop, Documents, Downloads, or OneDrive.

---

## 2. Canonical system map

### 2.1 Sources of truth

| Plane | Canonical source | Current finding |
|---|---|---|
| Estate routing | `starlight-agent-config/core/estate/repo-estate.control.json` | Observed; updated 2026-07-10 |
| SIS protocol/product | `Starlight-Intelligence-System` | Observed; public; active |
| Public fleet state | `agentic-ops-hub/fleet/` | Observed; public but stale for C940 |
| Private runtime bus | `C:/Users/frank/.starlight/swarm-bus/` through `swarm_bus.py` | Observed locally |
| Yoga Book runtime | Hermes default profile + gateway | Observed running |
| Private memory/runtime | `C:/Users/frank/.starlight/` | Declared private; contents intentionally not audited broadly |
| Device registry | `starlight-devices` | Observed but materially stale against current swarm policy |

### 2.2 Estate manifest

The manifest contains **118 unique entries**:

| Lane | Entries | Purpose |
|---|---:|---|
| `starlight-core` | 16 | SIS, memory, swarm, communities, devices |
| `site` | 11 | Public sites and product surfaces |
| `agent-config` | 18 | Skills, hooks, MCP/tooling, runtime doctrine |
| `design` | 5 | Design standards and visual intelligence |
| `frankx` | 12 | FrankX and commercial/productization work |
| `arcanea` | 13 | Arcanea creative intelligence estate |
| `experimental` | 37 | Research, templates, awesome lists, incubators |
| `archive-candidate` | 6 | Explicit review before archive/delete |

Priority distribution is 25 `now`, 49 `next`, 35 `later`, and 9 `watch`. Two declared repos, `Ana` and `ana-companion`, do not currently have local directories. This is not necessarily an error, but the manifest should label remote-only/uncloned state explicitly.

### 2.3 GitHub estate

Live GitHub owner totals:

- **349 repositories**
- **212 public**, **137 private**
- **59 archived**
- **34 forks**
- Public repos collectively show **113 stars** and **21 forks**
- **180** public repos have Issues enabled
- Only **3** public repos have Discussions enabled

The manifest is therefore a curated working estate, not a complete mirror of the GitHub account. That distinction should be explicit in the schema and dashboard.

### 2.4 Useful GitHub repository types

The estate currently contains these different GitHub product shapes:

1. **Protocol/substrate repos** — SIS, SIP, memory, orchestration, governance.
2. **Production websites** — FrankX, Arcanea, GenCreator, Starlight, Academy, Commons.
3. **Agentic OS products** — creator, business, music, fitness, finance, domain verticals.
4. **Agent/runtime configuration** — skills, hooks, profiles, cross-agent adapters.
5. **MCP and developer tools** — MCP Doctor, Suno MCP, memory MCP, bridges.
6. **Discovery/community repos** — `awesome-*`, starter kits, examples, curated indexes.
7. **Private operations repos** — fleet, runtime, ledgers, internal automation.
8. **Incubators and archive candidates** — experiments that need promotion or retirement decisions.

The taxonomy is good. The problem is the portfolio is too large for humans to infer maturity from repository names alone. Every public repo needs a generated status badge such as `production`, `beta`, `reference`, `incubator`, or `archived`.

---

## 3. SIS core: what exists

Live inventory of `frankxai/Starlight-Intelligence-System`:

- 2,629 tracked files
- 147 tracked agent markdown files
- 92 tracked skill markdown files
- 84 entries in `skills/skill-rules.json`
- 121 command markdown files under `.claude/commands/`
- built `dist/mcp-server.js` present
- public protocol site and research surface live
- latest observed `main` Harness Check succeeded on 2026-07-28

The repo presents:

- SIP protocol and attestation model
- six semantic vaults
- local/event-sourced memory
- council and governance agents
- multi-agent orchestration
- cross-harness adapters
- SAGE execution/healing concepts
- public research and proving-ground surfaces
- onboarding, contribution, security, and code-of-conduct documentation

The repo's own `AGENTS.md` claims 144 named agents. The 147 tracked agent markdown files are directionally consistent, but public metrics should be generated from the registry rather than manually maintained prose.

### Agent files and control files

There are several distinct agent-file layers:

| File/surface | Function |
|---|---|
| `AGENTS.md` | Cross-agent repo instructions |
| `CLAUDE.md` | Claude-specific operating context |
| `SOUL.md` | Identity/values layer |
| `MEMORY.md` | Curated state/decision context |
| `SKILL.md` and skill markdown | Reusable procedures/capabilities |
| `agents/*.md` | Named roles and specialists |
| `skills/skill-rules.json` | Activation routing |
| `.claude/commands/*.md` | Command surface |
| `.agent-harness.json` | Repo execution/governance contract |

This is powerful, but multiple overlapping files can drift. Generated registries and conformance tests must own all public counts.

---

## 4. Yoga Book Hermes runtime

### 4.1 Operational state

Observed on Yoga Book:

- Hostname: `Starlight`
- Storage: **44.66 GiB free — CRITICAL under the current ≥50 GiB floor**
- Hermes Agent: `0.2.0`
- Active provider/model: OpenAI Codex / `gpt-5.6-sol`
- Hermes gateway: running, installed as a Windows login item
- Telegram: configured
- Slack credentials: configured, but Slack remains a degraded/non-authoritative plane by fleet policy
- Scheduled jobs: 23 active, 29 total
- Active Hermes sessions: 60
- Computer use driver: installed at 0.8.3; 0.17.0 is available
- Native Hermes MCP registry: **no configured servers**
- Non-bundled plugin list: empty; xAI provider plugin is present in the broader registry
- xAI OAuth refresh: failed with `invalid_grant`; no xAI API key is configured
- Hermes configuration schema: valid at version 33

The command center is running, but it is operating primarily through native Hermes tools/skills rather than an SIS MCP attachment.

### 4.2 Skills

The installed skills registry reports:

- **249 enabled skills**
- **187 local**
- **62 built-in**
- **0 Hub-installed**
- **0 disabled**

The profile summary separately reports 261 skills. That discrepancy should be resolved; likely causes include aliases, duplicate names, profile expansion, or counting of loaded plugin skills.

Strengths:

- broad coverage across orchestration, GitHub, design, content, research, finance, media, devices, and product development;
- rich Starlight-specific policy and machine adapters;
- strong safety instructions for workspace routing, storage, and Phone Link.

Risks:

- every skill is enabled, which increases routing ambiguity and prompt/tool overhead;
- legacy redirect skills and duplicate names remain visible;
- `hermes skills check` validates Hub-installed skills only, so it returned no meaningful health result for the 187 local skills;
- the local skill fleet needs its own schema/lint/dependency/duplicate validator.

Recommended profile split:

- `queen-command`: fleet, GitHub, operations, research, Telegram;
- `frontend-queen`: frontend, premium design, visual QA, browser/computer use;
- `backend-c940`: backend, GitOps, Railway, databases, CI;
- `media-studio`: image/video/music generation;
- `finance-private`: finance tools only, with a separate private policy boundary.

---

## 5. MCP: installed versus actually wired

### 5.1 Current host matrix

| Harness | Current MCP state | Verdict |
|---|---|---|
| Hermes | No configured MCP servers | SIS MCP not wired |
| Claude Code | Vercel needs auth; `starlight-bridge` connected; Headroom failed; `starlight-v0` pending approval | Mixed and drifted |
| Codex | Headroom, node REPL, SBO brain files, and `starlight-bridge` enabled; cloud connectors vary; canonical `starlight-sis` and `starlight-substrate` are disabled | Capable, but SIS authority disabled |
| Gemini CLI | No MCP servers configured | Not wired |
| OpenCode | Railway MCP connected | Narrowly wired |
| MCP Doctor | executable exists but crashes because `dist/cli.js` is missing | Broken local install |

### 5.2 Canonicality problem

Claude and Codex both point `starlight-bridge` to:

`C:/Users/frank/agentic-ops/server.js`

That path is outside the canonical `C:/Users/frank/starlight/repos/<repo>` estate. It may be a working legacy bridge, but it is not acceptable as the long-term source of truth. The bridge must be rebuilt or relocated into the canonical repo, verified, then the legacy path removed from configs.

Codex already has canonical SIS definitions, but both are disabled:

- `starlight-sis` → `Starlight-Intelligence-System/dist/mcp-server.js`
- `starlight-substrate` → `Starlight-Intelligence-System/dist/starlight-mcp.js`

This is the clearest high-leverage fix: prove the canonical servers, enable one minimal authority path per harness, and remove duplicates.

### 5.3 MCP packages and publication truth

| Package/repo | Repo version/state | Registry state | Last-month downloads |
|---|---|---|---:|
| `@arcanea/starlight-intelligence-system` | repo/docs say 8.3.0; latest GitHub release 8.2.1 | npm 6.0.1 | 44 |
| `@frankxai/mcp-doctor` | repo available | npm 0.4.1; local global install broken | 85 |
| `@starlight-intelligence/memory` | package 0.2.0 in repo | not published | n/a |
| `@frankxai/suno-mcp-server` | package 0.1.0; README says early development | not published | n/a |

Downloads are requests, not unique users. They prove registry activity, not active production adoption.

### 5.4 MCP product maturity

- **SIS MCP:** built and documented; package/version truth is stale; not wired into current Hermes.
- **Starlight Memory MCP:** real source and three-tool design; package not published; operational relationship to SIS remains transitional.
- **MCP Doctor:** strongest community-facing utility; published, but the local install is currently unusable.
- **Suno MCP:** early-development scaffold, not a production server and not published.
- **Starlight Voice MCP:** explicitly pending in the repo; do not describe it as complete.

---

## 6. Production state

### 6.1 Live public surfaces

HTTP probes returned 200 for:

- <https://starlightintelligence.org/>
- <https://starlightintelligence.org/protocol>
- <https://starlightintelligence.org/research/proving-ground>
- <https://www.frankx.ai/>
- <https://gencreator.ai/>
- <https://www.arcanea.ai/>
- <https://starlight-intelligence-academy.vercel.app/>
- <https://blue-life-commons.vercel.app/>

`https://starlightintelligence.ai/` did not resolve/respond in the live probe. If it is intended as a redirect, DNS/redirect configuration is incomplete; otherwise it should be removed from public references.

### 6.2 CI and release health

- SIS `main`: latest observed Harness Check succeeded on 2026-07-28.
- Agentic Creator OS: scheduled ecosystem monitor succeeded on 2026-08-03; recent PR CI succeeded.
- Starlight Memory: latest observed `main` CI succeeded on 2026-07-28.
- Starlight Agentic OS: scheduled status refresh succeeded on 2026-08-03.
- Agentic Ops Hub: recent PR CI succeeded.
- Starlight Voice: latest observed `main` CI succeeded on 2026-06-16, but the product explicitly remains incomplete.
- Awesome Hermes Agent Skills: the weekly Link Checker failed on four consecutive observed runs through 2026-08-02.

### 6.3 Open work that is not production

SIS currently has 13 open draft PRs. Several are clean, but draft state correctly means they are not production. PRs include community-platform, foundry, observability, mesh, and knowledge-tree work. The platform has a large amount of promising branch-only definition; branch-only content must not be reported as shipped.

---

## 7. Community adoption

### 7.1 Current signal

Top public GitHub signals include:

- `claude-skills-library`: 28 stars, 5 forks
- `Starlight-Intelligence-System`: 6 stars, 2 forks
- `agentic-creator-os`: 6 stars, 1 fork
- `arcanea`: 6 stars
- `awesome-hermes-agent-skills`: 4 stars, 1 fork
- `frankx.ai-vercel-website`: 3 stars, 1 fork

The account-wide 113 stars across 212 public repos are spread thinly. This is **early ecosystem discovery**, not yet strong community adoption.

### 7.2 Human contribution evidence

The core repos have no verified external human contributor activity in the sampled contributor/PR data. Apparent external contributors on SIS, ACOS, and Arcanea were AI/bot identities such as Copilot or Claude.

Two human-origin PR signals were observed on the discovery repos:

- `awesome-hermes-agent-skills`: `runapi-builder`
- `awesome-hermes-agents`: `kriptoburak`

That is useful: the `awesome-*` repositories are currently the best community ingress surface. They should funnel contributors toward small, well-scoped core issues.

### 7.3 How the system is made for adopters

The public product already has good adoption mechanics:

- MIT licensing for code/spec surfaces
- quick-start installation paths
- explicit MCP registration examples for Claude, Cursor, Codex, Gemini, Antigravity, and Hermes
- a two-layer contribution model: operational changes follow normal OSS flow; substrate changes use a board pre-pass
- Code of Conduct and Security policy
- starter/adoption kits and vertical templates
- `Built on SIP` attribution and sovereignty model
- public protocol, research, and proving-ground pages

The weak points are discoverability and proof:

- SIS Discussions are not enabled despite `CONTRIBUTING.md` pointing users there “if enabled”.
- There is no single compatibility matrix showing the last verified version and command for each harness/OS.
- The npm package is materially behind repo/release truth.
- There is no public telemetry dashboard for installs, successful quick-start runs, starter forks, active adopters, or issue response time.
- There are too many public repos without lifecycle labels.

### 7.4 Community strategy

Treat community as a funnel, not as 212 separate public repos:

1. **Discover:** `claude-skills-library`, `awesome-hermes-*`, public research.
2. **Understand:** `starlightintelligence.org`, protocol, architecture explainer.
3. **Try:** one version-pinned `npx` quick start with a five-minute conformance check.
4. **Adopt:** starter repo, local-core memory, one MCP, one example workflow.
5. **Contribute:** 10–15 `good first issue` tasks with test fixtures and expected output.
6. **Compose:** vertical/adaptation kit with SIP attestation.
7. **Show proof:** public adopter gallery only with explicit consent and verifiable repository links.

---

## 8. Yoga Book ↔ C940 alignment

### 8.1 Intended roles

Current swarm policy assigns:

- **Yoga Book 9i / Starlight:** command center, frontend, premium UX, human Telegram gateway receive, multi-machine orchestration.
- **Yoga C940 / DESKTOP-1B4ICID:** backend, GitOps, overnight jobs, backups/restic, peer execution.

Only Yoga Book should run the primary Telegram receive gateway.

### 8.2 Observed evidence

Yoga Book:

- gateway running and autostarted;
- private swarm bus available;
- current local evidence generated in this report.

C940:

- public `fleet/c940.json` heartbeat is from 2026-07-16 and the file was last updated 2026-07-17;
- last public `fleet/activity/c940.json` update is 2026-07-17;
- `agent/c940/starlight-intelligence-architecture` PR #27 is still open/draft, last updated 2026-07-23;
- 38 private bus tasks addressed to C940 are still `pending`, from 2026-07-15 through 2026-08-03;
- zero of those tasks contain a `resultRef`;
- no inbound tasks to Yoga Book were present in the same queue view.

This does **not** prove C940 is offline. It proves there is no fresh completion evidence in the inspected public fleet and private task planes. Telegram or another channel could be alive while Git/task state is stale.

Audit action: priority-0 task `339bac19-e6b9-4a42-8e78-7e284878d1d4` was enqueued for a physical-C940 current-state receipt. It explicitly supersedes stale rejoin requests, requires C940-authored identity/heartbeat/MCP/gateway/sync evidence, prohibits broad searches and mutation, and remains `pending` with no `resultRef`. The queue therefore contains 39 pending tasks after this audit action.

### 8.3 Alignment drift

`starlight-devices` conflicts with current swarm policy:

- it calls C940 a secondary portable workstation instead of backend/GitOps owner;
- its Syncthing spec names Yoga 2 and OnePlus as peers but does not name C940;
- it assigns heavy substrate development to Yoga Book rather than the current frontend/command role split.

The device registry must be updated from the swarm machine registry, not maintained independently.

---

## 9. Mobile-device interconnection

### 9.1 Current observed state

- OnePlus 15R is declared the primary mobile cockpit.
- Telegram is configured and the Yoga Book gateway is running.
- Syncthing 2.1.2 is installed on Yoga Book but is not running; ports 8384, 22000, and 21027 were closed.
- No active Syncthing configuration was available to prove folders or peer devices.
- Tailscale is not installed on Yoga Book.
- WhatsApp and Signal are not configured as Hermes gateways.
- The Samsung S9 is declared an air-gapped security vault and must remain outside the active sync mesh.

### 9.2 Recommended mobile topology

```text
OnePlus 15R
  ├─ Telegram: commands, approvals, status, voice-note intake
  ├─ GitHub app: PR/issue review only
  └─ Syncthing: curated inbox + notes only
             │
             ▼
Yoga Book 9i / Starlight
  ├─ sole primary Telegram receiver
  ├─ validates human identity and approval class
  ├─ writes durable task envelope to private swarm bus
  ├─ owns frontend/UX and command-center state
  └─ routes backend/GitOps tasks to C940
             │
             ▼
Yoga C940
  ├─ backend/GitOps/overnight execution
  ├─ writes its own heartbeat and receipt
  └─ returns Git/CI/report evidence, never just chat claims
```

### 9.3 Mobile rules

1. **Phone is a cockpit, not a canonical repo node.** Do not clone the estate or run broad searches on the OnePlus.
2. **Telegram is the human command/approval plane.** Every execution request becomes a durable bus envelope before peer work starts.
3. **Sync only curated state.** Recommended folders: `starlight-inbox` and `starlight-notes`; keep repos, `.git`, runtime databases, secrets, and caches off Syncthing.
4. **Do not sync live SQLite databases.** Export append-only events or snapshots; index locally on each machine.
5. **Keep the S9 air-gapped.** It holds TOTP/keys and should not join Syncthing, Tailscale, Hermes, MCP, or Telegram bot automation.
6. **Use Huawei P30 as QA target only.** No privileged credentials and no control-plane role.
7. **Use a private overlay only when needed.** If remote access beyond Telegram is required, add Tailscale with explicit device ACLs, not public ports.
8. **Separate liveness from authority.** A phone notification or bot reply is not completion; require Git/CI/receipt evidence.

### 9.4 Mobile implementation sequence

1. Restore Syncthing as a managed background service on Yoga Book.
2. Pair OnePlus only to `inbox` and `notes`; verify ignore rules and conflict behavior.
3. Add C940 as a peer for append-only vault exports and receipts, not repos.
4. Add a signed `mobile-capture.v1` envelope: device, user, timestamp, intent, requested risk class, attachment hashes.
5. Build a Telegram status command returning: Yoga Book liveness, C940 evidence age, queue depth, last completed receipt, and human gates.
6. Add Tailscale only if direct private APIs are required; deny mobile access to file shares and admin endpoints by default.
7. Run an end-to-end drill: OnePlus request → Yoga Book envelope → C940 dry-run → receipt → Telegram result.

---

## 10. Priority fixes

### P0 — integrity and runtime alignment

1. **Restore disk above 50 GiB before any worktree, clone, bulk install, or media fanout.** Current free space is 44.66 GiB.
2. **Rejoin C940 with proof.** Require a machine-local heartbeat, current branch/origin/status, queue acknowledgement, gateway ownership check, and a receipt linked to PR/report/CI.
3. **Choose one canonical SIS MCP path.** Prove it locally, enable it in Hermes/Claude/Codex/Gemini as appropriate, then remove or disable duplicate legacy bridges.
4. **Remove noncanonical runtime dependence.** Replace `C:/Users/frank/agentic-ops/server.js` with a verified path under one canonical child repo.
5. **Repair MCP Doctor.** The global executable currently points to a missing `dist/cli.js`.
6. **Resolve SIS version truth.** Align repo `8.3.0`, GitHub release `8.2.1`, npm `6.0.1`, and all quick-start docs.
7. **Keep the primary Telegram receiver unique.** Verify C940 is sender/worker only.

### P1 — fleet and product quality

1. Update `starlight-devices` from the current machine registry and add C940 to the sync topology.
2. Restore Syncthing as a service; prove folder and peer state with a redacted receipt.
3. Fix the failing Awesome Hermes link checker.
4. Enable GitHub Discussions on SIS and ACOS; publish scoped good-first-issue templates.
5. Add lifecycle metadata to every public repo and generate a portfolio catalog.
6. Build a local-skill validator for the 187 local skills; reconcile the 249-versus-261 count.
7. Upgrade `cua-driver` after compatibility validation.
8. Reauthenticate xAI only if Grok-native media is required; keep media work fail-closed until a live output is verified.

### P2 — adoption and compounding

1. Publish one canonical five-minute adopter path with pinned versions and CI-tested commands.
2. Publish Starlight Memory only after package, privacy, cross-device, and recall-eval gates pass.
3. Keep Suno MCP labeled early development until API, licensing, and end-to-end generation are verified.
4. Add privacy-preserving community telemetry: quick-start success, package downloads, starter forks, issue response, returning contributors.
5. Convert successful adopter implementations into consented case studies.
6. Add a public compatibility matrix covering OS, harness, version, MCP transport, auth method, and last verification date.

---

## 11. 30/60/90-day operating plan

### 0–30 days: make truth match reality

- Recover disk above the safety floor.
- Reconnect C940 and drain/triage the stale 38-task queue.
- Prove one canonical SIS MCP path across Yoga Book harnesses.
- Fix MCP Doctor and the Awesome Hermes link checker.
- Align npm/release/docs versions.
- Correct the device registry and restore Syncthing for curated folders.

### 31–60 days: create an adopter-grade product

- Release a pinned installer and conformance test.
- Enable Discussions and launch 10–15 good-first issues.
- Generate public lifecycle/status badges across repos.
- Publish the compatibility matrix and a mobile cockpit guide.
- Run the first full OnePlus→Book→C940 receipt drill.

### 61–90 days: prove community and fleet compounding

- Measure successful external installs and returning contributors.
- Publish two consented adopter case studies.
- Promote only validated MCPs/adapters; archive or label abandoned experiments.
- Add a fleet dashboard with evidence age, queue depth, receipt links, and machine ownership.
- Run monthly cross-device disaster-recovery and mobile approval drills.

---

## 12. Definition of “interconnected and running well”

Starlight should not call itself fully interconnected until all checks below are green:

- [ ] One canonical registry maps every active repo, runtime, device, MCP, skill pack, and production surface.
- [ ] Yoga Book and C940 each publish their own fresh signed/attributed heartbeat.
- [ ] Every peer task has a state transition and a result reference.
- [ ] Only Yoga Book receives the primary Telegram bot.
- [ ] The canonical SIS MCP passes a real tool-call test in each supported harness.
- [ ] No active MCP points to an ungoverned home-root implementation.
- [ ] Syncthing runs with only approved folders and ignore rules.
- [ ] Mobile devices have explicit identities, scopes, and revocation paths.
- [ ] Package, release, documentation, and production versions agree.
- [ ] Public repos expose lifecycle state and a clear contribution path.
- [ ] Community metrics distinguish downloads/stars from verified active adopters.
- [ ] Storage remains above the active safety floor before fanout.

---

## 13. Evidence index

### Local canonical evidence

- `C:/Users/frank/starlight/WORKSPACE_MAP.md`
- `C:/Users/frank/starlight/repos/starlight-agent-config/core/estate/repo-estate.control.json`
- `C:/Users/frank/starlight/queen/swarm/PROTOCOL.md`
- `C:/Users/frank/starlight/queen/swarm/MACHINES.md`
- `C:/Users/frank/starlight/repos/agentic-ops-hub/fleet/ALIGNMENT.md`
- `C:/Users/frank/starlight/repos/agentic-ops-hub/fleet/c940.json`
- `C:/Users/frank/starlight/repos/Starlight-Intelligence-System/AGENTS.md`
- `C:/Users/frank/starlight/repos/Starlight-Intelligence-System/CONTRIBUTING.md`
- `C:/Users/frank/starlight/repos/Starlight-Intelligence-System/docs/guides/MCP-SETUP-GUIDE.md`
- `C:/Users/frank/starlight/repos/starlight-memory/README.md`
- `C:/Users/frank/starlight/repos/starlight-devices/README.md`
- `C:/Users/frank/starlight/repos/starlight-devices/SYNC-SPEC.md`
- `C:/Users/frank/starlight/repos/starlight-voice/README.md`
- `C:/Users/frank/starlight/repos/mcp-doctor/README.md`
- `C:/Users/frank/starlight/repos/suno-mcp-server/README.md`

### Public evidence

- <https://github.com/frankxai/Starlight-Intelligence-System>
- <https://github.com/frankxai/agentic-creator-os>
- <https://github.com/frankxai/starlight-memory>
- <https://github.com/frankxai/mcp-doctor>
- <https://github.com/frankxai/awesome-hermes-agent-skills>
- <https://github.com/frankxai/awesome-hermes-agents>
- <https://github.com/frankxai/agentic-ops-hub/pull/27>
- <https://www.npmjs.com/package/@arcanea/starlight-intelligence-system>
- <https://www.npmjs.com/package/@frankxai/mcp-doctor>
- <https://hermes-agent.nousresearch.com/docs>

### Live commands used

- `hermes status`, `hermes gateway status`, `hermes config check`
- `hermes profile show`, `hermes skills list`, `hermes mcp list`, `hermes tools list`, `hermes plugins list`
- `claude mcp list`, `codex mcp list`, `gemini mcp list`, `opencode mcp list`
- `gh repo list`, `gh api`, `gh pr list`, `gh run list`, `gh release list`
- public HTTP GET probes
- `syncthing --version`, `syncthing paths`, local port/process checks
- `swarm_bus.py list --to c940`

---

**Queen decision:** Preserve the strong public/product work, but stop describing Starlight as fully unified until the MCP authority path, C940 evidence loop, version truth, and mobile sync plane are proved end to end.
