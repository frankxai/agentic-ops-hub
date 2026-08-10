# Top-Tier CLI · Image · Design · Skills · Swarm Playbook

**Status:** active estate operating playbook  
**Verified:** 2026-08-11 (Book / Windows host)  
**Canonical repo:** [`frankxai/agentic-ops-hub`](https://github.com/frankxai/agentic-ops-hub) → `docs/TOP-TIER-CLI-DESIGN-IMAGE-SWARM-PLAYBOOK-2026-08.md`  
**Design SoT companion:** [`frankxai/starlight-design-intelligence`](https://github.com/frankxai/starlight-design-intelligence) → `playbooks/top-tier-cli-image-design-swarm.md`  
**App Factory (ideate → persona/gstack → SOTA UI → micro-SaaS/AaaS → stores):** `docs/app-factory/` · Hermes skill `app-factory-pipeline`  
**Harness mirrors:** `~/.agent-harness/UI-STACK-RADAR.md`, `DESIGN-SOURCE-CATALOG.md`, `GENERATION-A11Y-CHECKLIST.md`, `APP-FACTORY.md`

This document answers: what are the **best 2026 workflows** for Grok CLI + the rest of Frank’s CLIs, native image gen, open design tools/icons/templates, and the **most successful agent skills + swarms** — mapped to **this machine’s installed reality**, not a shopping list.

---

## 0. Decision in one page

| Layer | Default (estate) | When to deviate |
| --- | --- | --- |
| **Primary coding agent (Grok lane)** | **Grok Build CLI** `grok` + SuperGrok OAuth | Heavy Claude-only review → Claude Code; long autonomous code → Codex workspace-write |
| **Primary ops / multi-agent home** | **Hermes** (default profile = xai-oauth / Grok) | Queen profiles (`starlight-creative`, publishing-house, railway) |
| **Secondary coding CLIs** | Claude Code, Codex, OpenCode, Gemini CLI | Task-fit; never second “homes” that fork memory |
| **Image gen** | **Grok Imagine** via Hermes `image_gen` (`xai` + `grok-imagine-image-quality`) **and** Grok Build `image_gen` / `image_edit` / Imagine skill | Exact UI/charts/text → **code** (HTML/CSS), not diffusion |
| **Video** | Hermes `video_gen` (xAI Imagine) + Grok Build image→video shot pipeline | Opt-in; confirm entitlement before batches |
| **Product UI stack** | Next.js + React + Tailwind + **shadcn/Radix** + **Lucide** + Motion | Never mix second primitive family into a live app |
| **Icons** | **Lucide** default | Phosphor/Tabler only if brand pack says so |
| **Design judgment SoT** | `starlight-design-intelligence` skills + brand packs | `awesome-design-agent-skills` = **curation only** |
| **Swarm control plane** | Hermes profiles + `delegate_task` + Kanban + bus + Starlight Queens | Ruflo/Paperclip = optional depth on WSL/Linux; not Windows-default |
| **Skills hub (public)** | `frankxai/awesome-hermes-agent-skills` + `starlight-agent-skills` | External awesome lists = research; install only after license + trust gate |

**Do not** install every GitHub skill dump. Success comes from a **narrow production runtime** + **broad research library**.

---

## 1. Machine inventory (2026-08-11)

### 1.1 CLIs present

| CLI | Path / notes | Role |
| --- | --- | --- |
| `grok` | `~/.grok/bin` · v**0.2.118** | Grok Build TUI/agent; Imagine tools; MCP; plugins; worktrees |
| `hermes` | AppData Local hermes-agent venv | Primary multi-tool agent, image/video gen, swarms, gateway |
| `claude` | `~/.local/bin/claude` | Claude Code |
| `codex` | npm global | OpenAI Codex |
| `opencode` | npm global | OpenCode |
| `gemini` | npm global | Google Gemini CLI |
| `gh` | GitHub CLI (auth: frankxai) | Repos, PRs, Actions |
| `bun` / `node` / `pnpm` / `npm` | present | JS toolchain |
| `expo` | **was missing** → install path below | RN dual-store apps |
| `flutter` | missing (optional heavy) | Only if Flutter product lane starts |

### 1.2 Grok Build config (live)

```toml
# ~/.grok/config.toml (excerpt)
[models]
default = "grok-composer-2.5-fast"   # coding default on this host; models list also exposes grok-4.5

[marketplace]
# xAI Official: https://github.com/xai-org/plugin-marketplace.git

[ui]
permission_mode = "always-approve"
```

**Bundled / installed Grok skills of note:** `imagine`, `impeccable`, `code-review`, `create-skill`, office pack (`docx`/`pptx`/`xlsx`), `starlight-dev-server-supervisor`.

**Auth note (2026-08-11):** `grok models` reported **not authenticated** on this check. Re-auth before production media/coding:

```bash
grok login
# or: grok doctor
```

### 1.3 Hermes media (live)

```yaml
# hermes config (excerpt)
model:
  provider: xai-oauth
image_gen:
  provider: xai
  model: grok-imagine-image-quality
# toolsets: image_gen ✓, video_gen ✓, vision ✓
```

One SuperGrok / xai-oauth credential powers text + Imagine image + video + TTS in Hermes when plugins/toolsets are enabled.

---

## 2. Top-tier Grok CLI workflows

### 2.1 Daily coding (Grok Build)

```bash
# Interactive in repo
cd /path/to/repo && grok

# One-shot
grok -p "Summarize open TODOs and propose a minimal PR plan"

# Worktree isolation (parallel features)
grok -w feat/hero-polish "Implement hero polish per DESIGN.md"

# Resume
grok -c
grok -r "session title or id"

# Inspect discovery for cwd
grok inspect
grok doctor
```

**Best practices**

1. Prefer **worktrees** (`-w`) for parallel agents / risky edits.  
2. Keep **plan mode** on for multi-file product work; disable only for tiny fixes.  
3. Load Imagine skill implicitly when generating media; do **not** invent tool params.  
4. Pair with estate harness: `.agent-harness` FONT/A11Y + brand DESIGN.md.  
5. For Hermes dual-home tasks: **Grok CLI = deep code/media in repo**; **Hermes = orchestration, bus, cron, multi-CLI**.

### 2.2 Native image / video inside Grok Build

Grok’s first-party **Imagine** skill (`~/.grok/skills/imagine/SKILL.md`) is the gold standard:

| Goal | Tool |
| --- | --- |
| New scene / character / mood | `image_gen` |
| Restyle, fix, consistency, real person (with ref) | `image_edit` + reference |
| Exact charts, UI chrome, long text, data | **Build with HTML/CSS code**, not Imagine |
| Video | Plan **shots** → `image_gen`/`image_edit` per frame → `image_to_video` (verify tools exist) |

**Prompt order (Grok official craft):**  
subject → action/pose → setting → style → composition → lighting/mood → key details · **2–5 sentences** · positive language · front-load subject.

**Consistency:** one base image → all variants via `image_edit`, never re-roll identity from scratch.

**Aspect ratios:** `1:1` avatar · `16:9` hero/OG · `9:16` stories · `auto` when unsure.

**API-level models (xAI docs, 2026):**

| Model | Use |
| --- | --- |
| `grok-imagine-image` | Fast / cheaper (~$0.02/img class) |
| `grok-imagine-image-quality` | Default production quality (Hermes configured here); sharper text / instruction following (Image 2.0 quality mode era) |
| Video family | text/image→video, edit/extend via Imagine API / Hermes video_gen |

**CLI examples (chat-driven tools, not separate binary):**

```text
grok "Generate a premium dark hero still for Starlight SIS — calm command-center aesthetic, teal/gold accents, no fake UI text"
grok "Edit ./assets/hero.png into a 9:16 story crop with more negative space top for captions"
grok "Animate ./assets/cover.jpg into a 6s cinematic push-in"
```

### 2.3 Hermes image workflows (orchestration lane)

Load skills in order:

1. `hermes-image-generation` / `image-generation`  
2. `image-prompt-crafter`  
3. Brand: `brand-identity-strategy` → `logo-system` (identity, not gallery spam)  
4. Batch: `image-workflow-orchestrator` + a11y checklist  

```bash
# Config (already set on this host)
hermes config set image_gen.provider xai
hermes config set image_gen.model grok-imagine-image-quality

# In-session: use image_generate tool
# For 50–100 branded assets: delegate leaf agents with image_gen toolset + DESIGN.md tokens
```

**Hard rule from estate skills:** tool result `model` field is authoritative. Config alone does not prove quality route ran. Gallery ≠ brand canon. Complete `GENERATION-A11Y-CHECKLIST.md` before production.

### 2.4 Multi-CLI orchestration (most successful pattern on this estate)

```text
Hermes Queen / session
  ├─ grok -w …          # Grok Build code + Imagine in worktree
  ├─ claude …           # deep review / GStack-style critique when needed
  ├─ codex …            # overnight workspace-write (not danger-full-access)
  ├─ gemini / opencode  # alternate lenses
  └─ delegate_task      # short parallel leaves (image, research, patch)
```

**Memory doctrine:** Hermes / SIS local-first; CLIs are **execution blades**, not second memory homes.

---

## 3. Open best design tools · icons · templates (2026)

### 3.1 Production foundation (estate default)

Aligned with `UI-STACK-RADAR` + `DESIGN-SOURCE-CATALOG`:

| Piece | Choice | Why it wins |
| --- | --- | --- |
| Components | **shadcn/ui** (copy into repo) + **Radix** | Owned source, accessible, 100k+★ class ecosystem |
| Icons | **Lucide** (`lucide-react`) | Default with shadcn; consistent stroke; light |
| Variants | **CVA** + `tailwind-merge` | Local variants without new styling religion |
| Motion | **Motion** (`motion/react` / framer-motion path) | Purposeful UI motion; reduced-motion required |
| App framework | **Next.js** (existing products) | Do not force Remix into Next apps |
| Tokens | repo `DESIGN.md` / brand packs | Brand separation: FrankX ≠ Arcanea ≠ SIS |

### 3.2 Selective (one component at a time)

- **Magic UI** — single marketing/interaction pattern  
- **Motion Primitives** — micro-interaction ideas  
- **Tremor** — dashboard composition *reference* if charts already Recharts  
- **Google Labs Stitch skills** — design→React/shadcn loops (MCP)  
- **21st.dev / twenty-first-component-bridge** (already a Hermes skill) — named missing components only  

### 3.3 Icons shortlist

| Library | Use |
| --- | --- |
| **Lucide** | Default product UI |
| Phosphor | Friendlier consumer apps (only if brand pack chooses) |
| Tabler / Remix Icon | Dense dashboards (selective) |
| Heroicons | Legacy compatibility only on older surfaces |

### 3.4 Templates that actually ship

**Most successful dual-store / web patterns 2026:**

| Goal | Template / stack |
| --- | --- |
| Dual Play + App Store product | **Expo + React Native + EAS** |
| Polished multi-platform UI | Flutter / FlutterFlow (secondary) |
| Marketing / SaaS web | Next + shadcn starter **adapted to brand pack** |
| Agent-facing desktop | Hermes Desktop / Starlight Command Center patterns |
| Design system extraction | `starlight-design-intelligence` skills (`design-system-extractor`, `world-class-web-release`) |

**Avoid:** dumping entire template visual languages onto Arcanea/FrankX. Templates are **scaffolds**; brand packs are **law**.

### 3.5 Design agent skills (owned vs curated)

| Repo | Role |
| --- | --- |
| `frankxai/starlight-design-intelligence` | **SoT** skills, brand packs, evals, release contracts |
| `frankxai/awesome-design-agent-skills` | Public **curation / rankings only** |
| `.agent-harness` | FONT, A11Y, UI stack radar, component source gates |

Install design skills from SDI; do not promote curated lists to runtime authority.

---

## 4. Most successful agent skills (GitHub research + estate map)

### 4.1 External catalogs worth monitoring (research library)

| Source | Why |
| --- | --- |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ curated, multi-runtime (Claude/Codex/Gemini/Cursor) |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Practical Claude skill index |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | Large agentic catalog + local control-plane angle |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Official design→code skills (shadcn, loop, taste) |
| anthropics official skills (docx, web-artifacts-builder, …) | High trust document/UI artifact skills |
| xAI `imagine` + plugin marketplace | First-party Grok media craft |

### 4.2 Estate skills that already match “top tier” outcomes

**Creative / image**

- `hermes-image-generation`, `image-generation`, `image-prompt-crafter`, `image-workflow-orchestrator`  
- `brand-identity-strategy`, `logo-system`, `claude-design`, `popular-web-designs`, `baoyu-infographic`, `excalidraw`  
- Grok skill: `imagine`

**Swarms / queens**

- `starlight-queen-swarm`, `starlight-creative-queen`, `railway-infra-swarm`, `railway-starlight-queen`  
- `multi-llm-council`, `starlight-token-planner`, `content-swarm-production`  
- `estate-pr-review-swarm`, `agent-profile-distributions`

**Product / design excellence**

- SDI skills: `world-class-web-release`, `anti-slop-frontend`, `product-ui-polish`, `motion-and-interaction`, …  
- Hermes: `estate-design-excellence` patterns, `twenty-first-component-bridge`, `figma-design-to-code`

**Install policy**

```text
1. Prefer frankxai + hermes hub skills
2. External skill → inspect SKILL.md, license, network/credential claims
3. hermes skills install <id|url>  OR  copy into profile skills/
4. Pin critical skills (curator)
5. Never bulk-install untrusted mega-zips
```

---

## 5. Agent swarms — what actually works in 2026

### 5.1 Framework landscape (success signals)

| Framework | Signal | Estate use |
| --- | --- | --- |
| **Hermes** native `delegate_task` + profiles + cron + kanban | Production home | **Default** |
| **LangGraph** | Enterprise stateful graphs, high downloads | Product backends if needed — not desktop ops default |
| **OpenAI Agents SDK** | Lightweight multi-agent + tracing | Optional Python services |
| **CrewAI** | Role crews | Prototypes; map roles → Hermes generals |
| **AutoGen / AG2** | Conversation multi-agent | Research |
| **kyegomez/swarms** | Enterprise hierarchical swarms | Pattern reference |
| **Ruflo** (ruvnet) | Large specialized swarms, memory, federation | Optional deep coding swarms (prefer non-Windows) |
| **Paperclip** | Company OS / org charts | Governance layer; WSL/Linux deploy |

### 5.2 Estate swarm topology (proven)

```text
                    ┌─────────────────────┐
                    │  Starlight Queen    │  Hermes profile + skill
                    │  (orchestrator)     │  multi-llm-council gates
                    └─────────┬───────────┘
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      General A          General B          General C
   (orchestrator)     (orchestrator)     (orchestrator)
            │                 │                 │
      leaf specialists   leaf specialists   leaf specialists
      grok -w / codex    image_gen batch    research / PR
```

**Coordination surfaces**

- Git bus: `agentic-ops/bus`, `fleet/bus`  
- Activity: `fleet/activity/ACTIVITY-LOG.md`  
- Kanban: Hermes kanban  
- Thin Telegram; deep work in DMs  
- Templates: `agentic-ops/generalized-starlight-swarms/STARLIGHT-QUEEN-TEMPLATE.md`

### 5.3 Queen roster (current doctrine)

| Queen | Focus | Primary blades |
| --- | --- | --- |
| C940 / Infra | Railway, secrets, health | railway-* skills, Hermes |
| Creative | Images, video, Suno, brand assets | Grok Imagine, Hermes image_*, music skills |
| Product / Frontend | UI, a11y, Vercel | SDI skills, grok/claude, shadcn |
| Research | Radar, synthesis | web, arxiv, awesome-repo-control-plane |
| Growth | GEO, publishing, satellites | content-swarm, publishing-house |

### 5.4 Swarm run recipe (copy/paste)

```bash
# 1) Queen session
hermes -p starlight-creative -s starlight-creative-queen,image-generation,image-prompt-crafter

# 2) In parallel worktrees (separate terminals)
cd ~/some-repo && grok -w sprint/visuals "..."
cd ~/some-repo && codex ...   # overnight only with workspace-write

# 3) Report
# Write receipts to fleet/activity + bus; never silent END banners on Telegram no-ops
```

---

## 6. App templates for “best apps” (store + web)

| Rank | Pattern | Stack | Notes |
| --- | --- | --- | --- |
| 1 | Dual-store consumer/creator | **Expo + RN + EAS** + native bridges | Fastest credible path to Play + App Store |
| 2 | Flagship web product | **Next 15/16 + shadcn + Lucide + Motion** | Estate baseline |
| 3 | Pixel-perfect multi-OS | Flutter | When UI engine control > RN ecosystem |
| 4 | Agentic desktop | Hermes Desktop / Electron command centers | Ops, not consumer stores |
| 5 | AI MVP builders | Expo Agent / Emergent / FlutterFlow | Graduate to owned code before scale |

**Agentic mobile (from prior research):** Android **AppFunctions** + iOS **App Intents** for OS agents; MCP for backend tools — not unbounded phone agents in stores.

---

## 7. Install set (safe, high value)

### 7.1 Already good — do not thrash

- Hermes + image_gen/video_gen + design/creative skills  
- Grok Build + `imagine` skill + marketplace source  
- Claude / Codex / OpenCode / Gemini  
- gh, bun, pnpm, node  

### 7.2 Recommended adds (this playbook’s install pass)

```bash
# Expo (dual-store apps) — global CLI helper
npm install -g expo

# shadcn stays npx (no global required)
# npx shadcn@latest init

# Optional: xAI Python SDK for scripts (API key path; OAuth preferred in Hermes/Grok)
# pip install xai-sdk

# Optional research clones (read-only catalogs)
# gh repo clone VoltAgent/awesome-agent-skills ~/sources/awesome-agent-skills -- --depth 1
```

### 7.3 Auth / health checklist

```bash
grok login && grok doctor
hermes doctor
hermes auth list
hermes tools list | rg 'image_gen|video_gen|vision'
gh auth status
```

### 7.4 Explicitly NOT bulk-installed

- Random 1000-skill mega packs without review  
- Flutter SDK (large; install on product demand)  
- Parallel primitive UI kits into live Next apps  
- Paperclip/Ruflo full daemons on Windows git-bash (use WSL/Linux node)

---

## 8. Golden workflows (copy these)

### A. Brand hero still (production)

1. Load brand pack + `image-prompt-crafter` + a11y checklist.  
2. Hermes `image_generate` **or** `grok` Imagine `image_gen` with structured prompt.  
3. Vision QA → `image_edit` for crops/consistency.  
4. Register asset; alt text; fail closed if illegible burned-in type.  
5. Promote only via brand-image-system / portfolio rules.

### B. Exact UI mock that must be right

1. **Code** HTML/CSS or real React/shadcn screen.  
2. Screenshot.  
3. Optional Imagine polish **only** for atmosphere — never for real copy.

### C. Feature PR with dual agents

1. `grok -w feat/x "implement …"`  
2. Hermes/Claude review skill / `github-code-review`.  
3. `gh pr create` via github-pr-workflow skill.  
4. Receipts in ACTIVITY-LOG.

### D. Creative Queen sprint (2h)

1. Profile `starlight-creative` + creative queen skill.  
2. Delegate visuals / copy / music generals (bounded).  
3. Taste gate (`music-taste-review` / multi-llm-council).  
4. Bus + ledger update.

### E. New dual-store app greenfield

1. `npx create-expo-app@latest`  
2. Design tokens from brand pack.  
3. Lucide + accessible navigation.  
4. EAS build/submit.  
5. Agent tools: AppFunctions / App Intents when agentic.

---

## 9. Repo ownership map

| Artifact | Repo |
| --- | --- |
| This playbook (ops) | `frankxai/agentic-ops-hub` `docs/` |
| Design playbook pointer + SDI skills | `frankxai/starlight-design-intelligence` |
| Public Hermes skills awesome | `frankxai/awesome-hermes-agent-skills` |
| Portable substrate skills | `frankxai/starlight-agent-skills` |
| Design curation only | `frankxai/awesome-design-agent-skills` |
| Agent OS index | `frankxai/awesome-agent-operating-systems` |
| UI/FONT/A11Y gates | `~/.agent-harness` (+ claude-code-config harness mirror) |
| Queen templates | `agentic-ops/generalized-starlight-swarms/` |

---

## 10. Success metrics (honest)

A workflow is **top tier** here only if it produces:

1. **Receipts** (paths, PR URLs, asset registry IDs)  
2. **Brand-legal** outputs (fonts, logo lockups, a11y)  
3. **Bounded autonomy** (no unbounded spend/agents)  
4. **Single memory plane** (SIS/Hermes; CLIs are blades)  
5. **Store/review safe** behavior for mobile agents  

Stars on GitHub are research signal — **shipping with evidence** is the estate score.

---

## 11. Changelog

| Date | Change |
| --- | --- |
| 2026-08-11 | Initial playbook from live CLI inventory, Grok Imagine skill, Hermes image config, SDI/harness SoTs, and 2026 GitHub skill/swarm research. |

---

*Maintainer: Hermes Agent on FrankX estate. Patch this file when models, CLIs, or Queen topology change.*
