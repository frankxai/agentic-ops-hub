I have enough verified evidence to synthesize. Below is the audit. Note the method constraint up front: I confirmed every skill by reading files on disk; MCP servers (Figma, Canva, Higgsfield, Whimsical, Miro, Playwright) only *connected* this session — that is not proof they are authenticated or wired into any workflow, so I treat them as discovery channels, not active capabilities.

---

# Brand-Systems & Design-Engineering Capability Audit
**Scope:** `.claude/skills` (~145), `.codex/skills` (12+.system), `hermes/skills` (~141), `.agent-harness` (governance). Read-only. Evidence cutoff = files as they exist today.

## Headline verdict

You have a **world-class governance layer** and a **strong-but-fragmented generation layer**, sitting on top of a **near-absent identity-foundations layer**. The estate can *style* and *generate* extremely well; it cannot yet *construct a brand identity from strategy* or *clear it for licensed production* without a human. The single most repeated gap across all three roots: **no logo-system skill and no font/typeface-licensing gate anywhere.**

## 1. Governance layer — the estate's real differentiator (installed, current, excellent)

| Doc | Path | Role | Assessment |
|---|---|---|---|
| Design Excellence | `.agent-harness\DESIGN-EXCELLENCE.md` | Mandatory design loop + handoff contract | Best-in-class; rivals Vercel Web Interface Guidelines conceptually |
| UI Component Sources | `.agent-harness\UI-COMPONENT-SOURCES.md` | License/provenance source-gate (approved/research/blocked) | Stronger than most agencies' own policy |
| UI Stack Radar | `.agent-harness\UI-STACK-RADAR.md` | Evidence-backed per-repo stack inventory + component ladder | Excellent; prevents dependency sprawl |
| Design Source Catalog | `.agent-harness\DESIGN-SOURCE-CATALOG.md` | Role-gated research library (shadcn, Magic UI, Playwright, axe, Lighthouse…) | Excellent |
| Brand Media OS | `.agent-harness\BRAND-MEDIA-OPERATING-SYSTEM.md` + `brand-media-registry.json` | Asset lifecycle, provenance, storage authority, swarm roles | Excellent |

These are mirrored into three enforcement skills (`software-development\estate-design-excellence`, `premium-ui-components`, `brand-media-ops`), so the doctrine is actually executable, not just documentation. **This is your moat.** No leader below (Anthropic official, UI UX Pro Max, Emil Kowalski) ships governance this mature.

## 2. Evidence table — capability by domain

Legend: **✅ installed** (verified on disk) · **⚠ duplicated/stale** · **❌ missing**

| Domain | Installed (exact path) | Duplicated / stale | Missing | Recommended role | Leader / primary source to match |
|---|---|---|---|---|---|
| **Brand strategy → identity** | `.codex\skills\brand\SKILL.md`; `.claude\skills\brand-voice`; `hermes\...\brand-media-ops` | `brand` (codex) ↔ `brand`/`design` (claude) overlap | **No strategy→identity pipeline** (positioning, naming, identity system) | Keep `brand` for voice/tokens; **build identity-strategy skill** | Anthropic `brand-guidelines`; Impeccable |
| **Logo systems** | Only AI one-offs: `.codex\skills\design` (55 Gemini styles); `brand\references\logo-usage-rules.md` | — | **❌ No logotype construction** (grid, clear-space, lockups, favicon/app-icon set, monochrome/reverse) | **Highest-impact new skill** | Figma logo workflows; corp identity systems |
| **Typography / font licensing** | Selection only: `.codex\skills\ui-ux-pro-max` (57 pairings, 743 KB google-fonts.csv); `anthropic\theme-factory`; `hermes\creative\pretext` (kinetic type) | `popular-web-designs` maps Söhne/Circular/Cereal → CDN substitutes **with no licensing caveat** | **❌ No font-licensing gate** (OFL vs proprietary, webfont embedding rights, foundry terms) | **Highest-impact new gate** (mirror the component-source gate) | Foundry EULAs; Google Fonts license-per-family |
| **Design tokens** | `.codex\skills\design-system` (3-layer); `hermes\creative\design-md` (Google DESIGN.md + WCAG lint); `.claude\skills\community\design-systems`; `anthropic\theme-factory` | **4 token skills** (`design-system` ×codex/claude, `community\design-systems`, arcanea) + arcanea `design-system` marked **DEPRECATED** | Figma Variables ↔ code token sync | Consolidate to one canonical + `design-md` for validation | Figma Variables; Style Dictionary |
| **UI/UX system design** | `.codex\skills\ui-ux-pro-max` (46 KB, 250 rules — the global brain); `ui-styling` (shadcn/Radix); `.claude\skills\ui-ux-design-expert`, `web-design-expert` | **4 overlapping UI/UX skills** (WCAG+tokens+components each) | — | Make `ui-ux-pro-max` canonical; demote the 3 others to references | UI UX Pro Max (this *is* it); Taste Skill |
| **UI component sourcing** | `ui-styling`, `einui`, `anthropic\artifacts-builder` (all shadcn); `hermes\...\component-library-integration` + `premium-ui-components` (license gates) | shadcn logic repeated across 3 | **❌ No 21st.dev skill** (doctrine names 21st CLI but no skill wires it); **no Figma design-to-code skill** | Add thin 21st + Figma-context skills | 21st.dev; Figma Dev Mode / Code Connect |
| **Image / media generation** | Deep & redundant: `.codex\skills\.system\imagegen` (gpt-image), `acos-visual-gen` (Nano Banana), `arcanea-book-cover` (NB2), `higgsfield-*` (×4), `partner-google`, `hermes\creative\{comfyui,image-generation,baoyu-infographic}`, `image-prompt-crafter` | **6+ entry points to the same Gemini/Nano-Banana/GPT-Image backends** | Unified router / model-selection front door | Consolidate behind one dispatcher | Gemini Nano Banana; Higgsfield |
| **Infographics / data-viz** | `.codex\skills\infogenius` (stub), `arcanea-infogenius`, `acos-visual-gen`, `hermes\creative\baoyu-infographic`, `.claude\skills\slides`, `dataviz` | **InfoGenius appears ~4×**; `.codex\infogenius` is a prompt-only stub with no assets | — | Retire `.codex\infogenius`; keep `baoyu-infographic`+`dataviz` | — |
| **Accessibility** | Strong: `.claude\skills\ui-ux-design-expert`, `web-design-expert` (WCAG 2.2); `hermes\...\web-launch-ux-accessibility-audit` (Playwright/CDP), `design-md` (AA/AAA lint); `accessibility-auditor` agent | 3 overlapping a11y auditors | **❌ Zero a11y in ALL generation skills** (image-gen, infographics, animation → no contrast/alt/reduced-motion) | Bolt a11y checklist into generation skills | axe-core; Vercel guidelines |
| **Rendered / visual QA** | `anthropic\webapp-testing` (Playwright); `development\playwright-testing` (fork); `gstack\design-review` + `ios-design-review` + `qa`; `hermes\...\web-launch-ux-accessibility-audit` | `playwright-testing` is an explicit **duplicate fork** of `anthropic\webapp-testing`; 3 design-review variants | Single visual-regression owner | Pick one Playwright QA owner | Playwright; Lighthouse |
| **Figma workflow** | **MCP only** (connected this session: `get_design_context`, `use_figma`, Code Connect, generate_design) | — | **❌ No Figma skill on disk** in any root | Add design-to-code + tokens-sync skill around the MCP | Official Figma MCP + `/figma-*` skills |
| **Release governance (design)** | `.agent-harness` docs + `brand-media-ops` lifecycle; `arcanea-nft-pfp` QA gates | — | No approval-gate tying rendered design → ship (only media assets are gated) | Extend media lifecycle to code/UI | — |
| **Motion / animation** | `.claude\skills\{gsap,animejs,css-animations,waapi,lottie}` (all HyperFrames adapters); Framer Motion (doctrine) | 5 adapters overlap; only useful with HyperFrames | Emil-Kowalski-style *interaction-craft* guidance (spring feel, gesture, orchestration) | Add a motion-taste skill, not more runtimes | Emil Kowalski; Motion (motion.dev) |
| **Official Anthropic design skills** | ✅ Present: `.claude\skills\anthropic\{brand-guidelines, theme-factory, canvas-design, algorithmic-art, artifacts-builder, webapp-testing}` | Nested self-duplicate `anthropic\anthropic\...` copies | Anthropic `frontend-design` / `slackgpt`-style skills not confirmed | Keep as brand/canvas baseline | Anthropic Skills repo |
| **"Claude Design" (frontend/canvas)** | `hermes\creative\claude-design` — **third-party MIT re-adaptation** (author BadTechBandit), *not* the hosted Anthropic skill; hosted tool plumbing stripped | — | The genuine hosted canvas skill | Treat as taste reference, label clearly | Anthropic hosted Claude Design |

## 3. Structural hygiene issues (stale/duplicated — verified)

- **Nested self-duplicate folders** (same skill shipped twice inside itself): `web-design-expert\web-design-expert\`, `ui-ux-design-expert\ui-ux-design-expert\`, `framer-expert\framer-expert\`, `anthropic\anthropic\{webapp-testing,pptx,artifacts-builder}`, plus several non-design ones. Cleanup candidates.
- **`arcanea\design-system` marked DEPRECATED** but still on disk.
- **`.codex\skills\infogenius`** — prompt-only stub, zero assets; superseded by richer paths.
- **`social-media-strategy`** (`.claude`) — 9-line stub; real capability lives in `higgsfield-*`/`banner-design`.
- **`arcanea-infogenius`** — **no YAML frontmatter**, so it will not auto-trigger reliably.
- **Path-resolution risk:** `.codex\skills\design` references `~/.claude/skills/...` for its scripts while living under `.codex` — bundled scripts may not resolve as documented.

## 4. Comparison against current leaders

| Leader | You have equivalent? | Gap |
|---|---|---|
| **Anthropic official (brand/canvas/frontend)** | ✅ `anthropic\brand-guidelines, theme-factory, canvas-design, artifacts-builder, webapp-testing` | Hosted "Claude Design" canvas only present as 3rd-party re-adaptation |
| **UI UX Pro Max** | ✅ Installed & deep (`.codex\skills\ui-ux-pro-max`, 46 KB, offline DB) — this is genuinely the real thing | No font-licensing, no Figma/21st/Playwright wiring |
| **Impeccable / Taste Skill** | Partial — `ui-ux-pro-max` anti-slop rules + `gstack\design-review` + `claude-design` "ten tells" | No single consolidated taste-critique skill |
| **Emil Kowalski (design-engineering / motion craft)** | ❌ Runtimes yes, *craft judgment* no | Interaction-feel, spring/gesture orchestration guidance |
| **Vercel Web Interface Guidelines** | ✅ Conceptually matched by `DESIGN-EXCELLENCE.md` + `UI-STACK-RADAR.md` | Not packaged as a lintable checklist |
| **Figma workflows** | ⚠ MCP connected, **no skill** | Design-to-code, Variables↔tokens, Code Connect skills |

## 5. Highest-impact gaps blocking end-to-end brand creation (ranked)

1. **Logo / mark construction system** — you can *generate* a logo image but cannot build a *system* (grid, clear-space, lockups, favicon/app-icon exports, mono/reverse). This is the biggest hole between "strategy" and "identity."
2. **Font / typeface licensing gate** — you rigorously gate component and media licensing but have **zero** font-licensing discipline; one skill actively substitutes proprietary faces to CDN with no caveat. This is a real legal exposure in production.
3. **Brand strategy → identity pipeline** — no skill takes positioning/audience → naming → identity system. `brand`/`brand-voice` cover voice only. Strategy is the missing front end.
4. **Figma + 21st.dev skills** — both are named as canonical in your own doctrine but exist only as an MCP (Figma) or an unwired CLI reference (21st). The design-to-code bridge is not executable as a skill.
5. **Accessibility inside generation** — a11y is excellent in *audit* skills and absent in *every* generation skill (image, infographic, animation). No alt-text/contrast/reduced-motion at the point of creation.
6. **Consolidation debt** — 4 UI/UX skills, 4 token skills, 6+ image-gen entry points, 3 Playwright QA variants, ~4 InfoGenius copies, plus nested self-duplicates. This dilutes triggering and creates conflicting guidance.

## Caveats on "installed ≠ active"
- Every skill above was verified by reading its file. The MCP design servers (**Figma, Canva, Higgsfield, Whimsical, Miro, Descript, Semrush, Playwright**) only *connected* in this session — that is not evidence they are authenticated or used in any workflow. Several other connectors (Excalidraw, Jam) **require auth** and are unavailable until authorized via claude.ai connector settings.
- Per your own doctrine, **21st CLI is installed but unauthenticated**, and **Framer Motion is project-local, not global** — I did not treat either as an active capability.

---

Want me to turn the top-2 gaps into concrete skill scaffolds — a `logo-system` skill and a `font-licensing` source-gate modeled on your existing `UI-COMPONENT-SOURCES.md` policy? That would be the fastest path to closing strategy→production. I can also save this gap-list to project memory if you want it to persist.