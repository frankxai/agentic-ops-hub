import { copyFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const opsRoot = join(__dirname, '..')
const estateRoot = dirname(opsRoot)
const today = '2026-06-22'
const version = '2026.06-premium'

const generatedRoot = 'C:/Users/frank/.codex/generated_images/019eee93-7525-7c43-bb1f-836e174dd5cb'

const visualList = [
  {
    slug: 'ecosystem-north-star',
    title: 'Ecosystem North Star',
    kicker: 'L0-L7 OPERATING SYSTEM',
    story: 'Skills, ops, income, payments, swarm, and assurance connected as one governed system.',
    steps: ['L1 Skills', 'L2 Ops hub', 'L4 Income', 'L5 Payments', 'L6 Swarm', 'L7 Evals'],
    homes: ['All READMEs', 'agentic-ops-hub docs', 'site OG'],
    accent: '#22d3ee',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390d6c55d481938ea5635d4248a50f.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Ecosystem North Star backplate for a Starlight agentic income operating system: a layered L0-L7 architecture made of luminous operational planes, governed nodes, and precise pathways connecting skills, ops, income, payments, swarm, and assurance.
Scene/backdrop: deep graphite command-space with a crisp dimensional systems map, not outer space, not fantasy.
Subject: one central luminous systems spine with seven subtly separated horizontal layers and a few visible proof nodes.
Style/medium: high-end editorial 3D systems illustration, precise developer-tool craft, premium technical keynote still.
Composition/framing: wide landscape with strong central structure, generous clean negative space in upper-left and lower-right for deterministic overlay text later.
Lighting/mood: intelligent, trustworthy, operational, high-agency; luminous without being dark or murky.
Color palette: charcoal, graphite, cyan, emerald, amber, restrained violet and signal red accents; avoid one-note purple-blue gradient dominance.
Materials/textures: translucent glass planes, fine grid lines, brushed dark metal, crisp light traces, subtle depth.
Text (verbatim): none.
Constraints: absolutely no words, no letters, no numbers, no logo marks, no watermarks, no finance symbols, no coins, no UI screenshots, no humans, no decorative orbs, no bokeh blobs.
Avoid: fake labels, unreadable glyphs, generic AI cloud, stock-photo look, clutter, heavy blur, dark cropped mystery.`
  },
  {
    slug: 'repo-constellation',
    title: 'Repo Constellation',
    kicker: 'WHICH REPO DOES WHAT',
    story: 'A grouped map of the estate by capability, operations, income, payments, swarm, and evals.',
    steps: ['Capability libraries', 'Ops control', 'Income engines', 'Payments guardrails', 'Swarm runtime', 'Evals lane'],
    homes: ['agentic-ops-hub', 'all README maps'],
    accent: '#34d399',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390dae457081939df56d8f365316cd.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Repo Constellation backplate: a precise map of interconnected software repositories as grouped operational districts, showing capability libraries, ops hub, income engines, payments governance, swarm runtime, and evals assurance as distinct clusters.
Scene/backdrop: dark developer command board with luminous pathways and grouped repositories represented as clean abstract modules, not stars in space.
Subject: six clearly separated clusters connected by routed traces, with one subtle central control hub.
Style/medium: premium editorial technical illustration, high-trust systems cartography, glass-and-metal depth.
Composition/framing: wide landscape, central constellation occupies middle band, clean margins for future labels and repo names, no tiny details that look like text.
Lighting/mood: calm, intelligent, organized, source-grounded.
Color palette: graphite, cyan, emerald, amber, restrained violet, small red assurance signals; balanced, not monochrome.
Materials/textures: etched grid, translucent panels, precise connection traces, subtle node glow, crisp edges.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no fake glyphs, no finance icons, no humans, no decorative orbs, no bokeh.
Avoid: galaxy/starfield look, fake UI labels, cluttered circuit-board noise, generic SaaS gradient.`
  },
  {
    slug: 'income-engine-flow',
    title: 'Income Engine Flow',
    kicker: 'HONEST RECURRING REVENUE',
    story: 'Research demand, publish useful comparisons, bind the catalog, capture email, and audit every link.',
    steps: ['Research', 'Compare', 'Catalog', 'Capture', 'Audit'],
    homes: ['agenticincome', 'template', 'L4 repos'],
    accent: '#6ee7b7',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390e47a234819391be0dc38f04abc0.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Income Engine Flow backplate: an honest AI-tool income workflow represented as a clean operational pipeline from research signals to comparison evidence, curated catalog, email capture, and audit receipts.
Scene/backdrop: dark editorial workspace made of luminous data lanes and proof artifacts, no readable text.
Subject: five-stage pipeline with evidence panels, catalog blocks, capture gate, and audit ledger represented by abstract shapes only.
Style/medium: premium 3D technical illustration with product-storytelling clarity, not marketing fluff.
Composition/framing: left-to-right flow with five distinct stations, open top area and bottom caption area for deterministic overlay text later.
Lighting/mood: commercially sharp, credible, useful, calm confidence.
Color palette: graphite, cyan, teal, emerald, amber accents; restrained contrast, no beige/tan, no one-color theme.
Materials/textures: glass data trays, fine scan lines, precise routing, subtle paper-like proof surfaces without markings.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no coins, no dollar signs, no credit cards, no fake UI text, no humans.
Avoid: get-rich imagery, generic funnels, stock marketing charts, bokeh, decorative orbs, unreadable labels.`
  },
  {
    slug: 'website-growth-loop',
    title: 'Website Growth Loop',
    kicker: 'HUB, TEMPLATE, SPOKES, SKILLS',
    story: 'The flagship site, forkable template, passive spoke, awesome list, and skills library feed one loop.',
    steps: ['Hub', 'Template', 'Spoke', 'Awesome list', 'Skills'],
    homes: ['3 Next.js sites', 'L4 READMEs'],
    accent: '#14b8a6',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390e8bba608193875b5f77080c6ffe.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Website Growth Loop backplate: a hub-and-spoke growth network for AI income sites, showing flagship hub, forkable template, passive-income spoke, curated list, and skills library feeding each other in a clean circular operating loop.
Scene/backdrop: polished web systems command surface with browser-like panels as abstract blank glass slabs, no readable text.
Subject: central hub plane with four connected spokes, looped signal paths, content proof blocks, and conversion path represented abstractly.
Style/medium: premium product-storytelling 3D illustration, editorial website operations map.
Composition/framing: wide landscape, circular flow centered slightly right, left side has calm negative space for overlay headline, lower band clear for deterministic step labels.
Lighting/mood: sharp, credible, commercial, not hypey.
Color palette: graphite, cyan, teal, emerald, amber highlights, restrained white glints; avoid purple-blue dominance.
Materials/textures: blank glass browser panes, precise path lines, soft metal frames, crisp reflection control.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no fake UI text, no coins, no dollar signs, no humans, no bokeh.
Avoid: generic marketing funnel, dark abstract fog, social-media icons, unreadable interface marks.`
  },
  {
    slug: 'payments-safety-spine',
    title: 'Payments Safety Spine',
    kicker: 'FAIL-CLOSED BY DEFAULT',
    story: 'Mandate verification, spend caps, audit records, and human approval before settlement.',
    steps: ['Mandate', 'Spend cap', 'Audit', 'Human gate'],
    homes: ['payments MCP', 'payment protocol list'],
    accent: '#f59e0b',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390ed7681c8193b614e2ef374d506b.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Payments Safety Spine backplate: a fail-closed agent payments governance flow where a mandate, spend cap, audit ledger, and human approval gate protect any settlement path.
Scene/backdrop: secure dark technical operations table with four guarded checkpoints and a final locked human gate represented abstractly.
Subject: a clear left-to-right safety spine with cryptographic seal object, cap threshold gate, append-only ledger stack, and approval lock, all without readable symbols.
Style/medium: premium cybersecurity and payments-governance 3D illustration, precise, serious, no hype.
Composition/framing: wide landscape, strong horizontal spine through center, negative space above for deterministic headline, lower space for labels.
Lighting/mood: trustworthy, fail-closed, high-assurance, controlled.
Color palette: graphite, amber, cyan, emerald, small red guardrail alerts; no finance gold overload.
Materials/textures: dark metal rails, glass guard panels, etched verification paths, precise light gates.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no coins, no dollar signs, no credit card graphics, no bank icons, no fake UI text, no humans.
Avoid: casino/finance imagery, generic padlock clipart, fake code text, clutter, bokeh, decorative orbs.`
  },
  {
    slug: 'swarm-runtime',
    title: 'Swarm Runtime',
    kicker: 'QUEEN/WORKER ORCHESTRATION',
    story: 'Founder command, queen coordination, worker lanes, escalation, and receipts.',
    steps: ['Founder', 'Queen', 'Workers', 'Escalate', 'Receipts'],
    homes: ['starlight-swarm', 'ops hub'],
    accent: '#a78bfa',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390f1c06e881938f91307cfd4f455d.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Swarm Runtime backplate: a governed queen-worker orchestration runtime with founder command, queen coordinator, worker lanes, escalation ladder, and verification receipts.
Scene/backdrop: dark operational command floor with routed task lanes and elevated coordination nodes, no readable UI.
Subject: one high-level coordinator node directing several worker lanes, with a clear escalation path rising to a guarded decision point and receipt trail.
Style/medium: premium 3D systems illustration, calm operational intelligence, developer-grade precision.
Composition/framing: wide landscape, coordinator centered, workers arranged in ordered lanes, diagonal escalation path toward upper-right; clean areas for overlay text.
Lighting/mood: intelligent, decisive, controlled, collaborative without human figures.
Color palette: graphite, cyan, violet, emerald, amber, tiny red escalation signals; avoid all-purple wash.
Materials/textures: glass task lanes, metal docking points, light rails, subtle grid, receipt-like blank tiles with no marks.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no humans, no animals, no fake UI text, no coins, no bokeh or decorative orbs.
Avoid: sci-fi spaceship bridge, fantasy throne imagery, generic network cloud, clutter.`
  },
  {
    slug: 'red-blue-assurance',
    title: 'Red/Blue Assurance',
    kicker: 'EVALS BEFORE MONEY',
    story: 'Red probes, blue controls, scorecards, receipts, and release gates for income/payment flows.',
    steps: ['Probe', 'Exploit attempt', 'Guardrail', 'Scorecard', 'Release gate'],
    homes: ['starlight-evals', 'ops hub', 'payments'],
    accent: '#fb7185',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390f59d738819389f9901823abb48d.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Red/Blue Assurance backplate: a rigorous eval lane where red-team probes test an agentic income/payments stack, blue-team controls respond, scorecards collect receipts, and a release gate opens only after evidence passes.
Scene/backdrop: dark assurance lab table with two opposing signal lanes converging into an evidence board and guarded release gate.
Subject: red probe lane, blue defense lane, central receipt/scorecard matrix represented as blank tiles, and final release checkpoint.
Style/medium: premium technical assurance illustration, cybersecurity lab meets product QA, crisp and legible.
Composition/framing: wide landscape, split red/blue lanes left and right, central evidence grid, final gate toward right; room for text overlays above and below.
Lighting/mood: rigorous, skeptical, controlled, high-trust.
Color palette: graphite, cyan-blue defense, signal red probe, amber release, emerald pass accents; not neon chaos.
Materials/textures: matte dark lab surface, glass tiles, lit rails, precision frames, no written marks.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no fake code text, no skulls, no weapons, no humans, no bokeh, no decorative orbs.
Avoid: hacker cliche, fake terminal text, scary imagery, clutter, over-saturated red-blue gradients.`
  },
  {
    slug: 'build-deploy-verify',
    title: 'Build / Deploy / Verify',
    kicker: 'SHIPPING PATH',
    story: 'Branch, local gates, PR, CI, preview, main, and live verification as one disciplined path.',
    steps: ['Branch', 'Local gates', 'PR', 'CI', 'Preview', 'Main', 'Live check'],
    homes: ['ops docs', 'README contribution paths'],
    accent: '#10b981',
    source: `${generatedRoot}/ig_0f176f3eb23cee4f016a390fc49668819383d2eb7e46e4969d.png`,
    prompt: `Use case: stylized-concept
Asset type: Premium visual-suite backplate for GitHub README and website infographic, 16:9 landscape, no text
Primary request: Build Deploy Verify Path backplate: a disciplined software delivery path for agentic repos from branch, local gates, PR, CI, preview deploy, main merge, and live verification.
Scene/backdrop: dark engineering release runway with sequential checkpoints and evidence beacons, no readable UI.
Subject: a clear release pipeline path with seven clean stations, code branch fork, check gates, preview portal, merge spine, and live verification beacon represented abstractly.
Style/medium: premium developer-ops 3D illustration, Vercel/Linear-like clarity without copying any brand.
Composition/framing: wide landscape, left-to-right path with distinct checkpoints, clean upper band for deterministic title and lower band for labels.
Lighting/mood: precise, fast, careful, production-grade.
Color palette: graphite, cyan, white, emerald pass lights, amber preview, small red blocked state accents; avoid one-note blue/purple.
Materials/textures: matte rails, glass checkpoint tiles, subtle terminal-like surfaces without text, crisp routing lines.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no fake code text, no GitHub/Vercel logos, no humans, no bokeh, no decorative orbs.
Avoid: generic DevOps clipart, fake terminal windows, clutter, dark fog, illegible symbols.`
  }
]

const visuals = Object.fromEntries(visualList.map((visual) => [visual.slug, visual]))

const repos = [
  {
    repo: 'agentic-ops-hub',
    title: 'Agentic Ops Hub',
    layer: 'L2',
    subtitle: 'The control plane for the L0-L7 agentic income ecosystem.',
    headerVisual: 'ecosystem-north-star',
    mapVisual: 'repo-constellation',
    chips: ['ECOSYSTEM', 'MCP strategy', 'Protection layers', 'Red/blue charter'],
    role: 'Keeps agent rules, MCP strategy, protection layers, and the full estate map aligned.',
    primaryPath: 'Design the operating contract -> sync agents -> verify the release path.',
    proofGate: 'Every repo gets visual provenance, deterministic text, and build/deploy checks.',
    steps: ['Define the L0-L7 map', 'Sync repo rules', 'Route skills and MCPs', 'Gate releases with evidence'],
    outputs: ['README command surface', 'Premium suite source', 'Cross-repo manifest']
  },
  {
    repo: 'starlight-agent-skills',
    title: 'Starlight Agent Skills',
    layer: 'L1',
    subtitle: 'Portable substrate skills for Starlight work.',
    headerVisual: 'ecosystem-north-star',
    mapVisual: 'repo-constellation',
    chips: ['agentic-income', 'affiliate-audit', 'payments-mandate', 'swarm-queen'],
    role: 'Turns the income thesis, affiliate loop, payment mandate, and queen coordination into portable skills.',
    primaryPath: 'Package repeatable behavior -> document triggers -> ship skills into agents.',
    proofGate: 'Skills stay small, named, and backed by source repo workflows.',
    steps: ['Name the job', 'Write trigger rules', 'Encode the workflow', 'Use in coding agents'],
    outputs: ['Reusable skills', 'Agent behavior contracts', 'Income operating memory']
  },
  {
    repo: 'agenticincome',
    title: 'Agentic Income',
    layer: 'L4',
    subtitle: 'The flagship hub for honest AI-agent income systems.',
    headerVisual: 'income-engine-flow',
    mapVisual: 'website-growth-loop',
    chips: ['Hub site', 'Comparison posts', 'Affiliate catalog', 'Owned audience'],
    role: 'Ranks for high-intent searches, tells the truth, and routes only to tools that genuinely win.',
    primaryPath: 'Research demand -> publish comparisons -> bind affiliate catalog -> capture email.',
    proofGate: 'Affiliate links are audited, JSON-LD is hardened, and build output is static-safe.',
    steps: ['Find search demand', 'Test and compare tools', 'Bind the catalog', 'Capture email', 'Audit links'],
    outputs: ['Authority pages', 'Recurring revenue paths', 'Network traffic']
  },
  {
    repo: 'agentic-income-template',
    title: 'Agentic Income Template',
    layer: 'L4',
    subtitle: 'Clone-and-deploy starter for honest AI-tool comparison sites.',
    headerVisual: 'website-growth-loop',
    mapVisual: 'income-engine-flow',
    chips: ['Next.js 16', 'MDX', 'Affiliate binding', 'Forkable brand config'],
    role: 'Packages the hub method into a reusable site engine.',
    primaryPath: 'Fork the template -> swap site config -> write comparisons -> deploy.',
    proofGate: 'Portable affiliate audit and static OG surfaces ship with the template.',
    steps: ['Fork', 'Configure brand', 'Write MDX posts', 'Sync catalog', 'Deploy'],
    outputs: ['Reusable starter', 'Site visual assets', 'Affiliate-safe workflow']
  },
  {
    repo: 'agentic-income-skills',
    title: 'Agentic Income Skills',
    layer: 'L4',
    subtitle: 'Portable operating brain for income systems.',
    headerVisual: 'income-engine-flow',
    mapVisual: 'website-growth-loop',
    chips: ['agentic-income', 'affiliate-audit', 'Audit script', 'Five principles'],
    role: 'Extracts the income thesis and affiliate audit loop into standalone skills.',
    primaryPath: 'Explain the thesis -> choose programs honestly -> audit every recommendation.',
    proofGate: 'Skills encode the no-hype, best-tool-wins rule.',
    steps: ['Load thesis', 'Select use case', 'Compare honestly', 'Audit links', 'Publish receipts'],
    outputs: ['Income skill pack', 'Audit patterns', 'Reusable prompts']
  },
  {
    repo: 'awesome-agentic-income',
    title: 'Awesome Agentic Income',
    layer: 'L4',
    subtitle: 'Curated map of honest agentic income systems.',
    headerVisual: 'repo-constellation',
    mapVisual: 'income-engine-flow',
    chips: ['Method', 'Engines', 'Programs', 'Playbooks'],
    role: 'Separates useful recurring-income resources from generic affiliate noise.',
    primaryPath: 'Find source-grounded resources -> sort by usefulness -> keep the list current.',
    proofGate: 'Public curation favors proof, recency, and editorial selectivity.',
    steps: ['Source', 'Filter', 'Group', 'Link', 'Maintain'],
    outputs: ['Curated list', 'Learning map', 'Traffic bridge']
  },
  {
    repo: 'agenticpassiveincome',
    title: 'Agentic Passive Income',
    layer: 'L4',
    subtitle: 'Spoke site for set-and-review income loops.',
    headerVisual: 'website-growth-loop',
    mapVisual: 'income-engine-flow',
    chips: ['Spoke site', 'Passive loop', 'Shared catalog', 'Hub links'],
    role: 'Uses the shared engine with a passive-income angle for builders who want set-and-review systems.',
    primaryPath: 'Adapt the hub -> focus passive loops -> reuse catalog -> cross-link authority.',
    proofGate: 'The spoke keeps the same audit discipline as the flagship hub.',
    steps: ['Choose passive angle', 'Reuse engine', 'Publish comparison', 'Cross-link hub', 'Capture email'],
    outputs: ['Spoke authority', 'Passive loop pages', 'Shared revenue paths']
  },
  {
    repo: 'payment-intelligence-system',
    title: 'Payment Intelligence System',
    layer: 'L5',
    subtitle: 'Fail-closed payments governance MCP.',
    headerVisual: 'payments-safety-spine',
    mapVisual: 'red-blue-assurance',
    chips: ['Ed25519', 'AP2 mandate', 'Spend cap', 'Audit log'],
    role: 'Verifies mandates, checks caps, records audit entries, and requires humans without moving money.',
    primaryPath: 'Verify mandate -> check cap -> record audit -> require approval.',
    proofGate: 'The MCP exposes verify-only tools and fails closed under invalid input.',
    steps: ['Verify mandate', 'Check spend cap', 'Record audit', 'Require human approval'],
    outputs: ['Verify-only MCP', 'Audit receipts', 'Human approval objects']
  },
  {
    repo: 'awesome-payment-agent-skills',
    title: 'Awesome Payment Agent Skills',
    layer: 'L5',
    subtitle: 'Curated payment protocols and safety tooling.',
    headerVisual: 'payments-safety-spine',
    mapVisual: 'repo-constellation',
    chips: ['AP2', 'x402', 'ACP', 'Safety tooling'],
    role: 'Maps authorization, settlement, and audit tooling so agents can pay only under guardrails.',
    primaryPath: 'Collect protocols -> classify risk -> link safety patterns -> update the map.',
    proofGate: 'Curation favors protocols with clear authorization and audit semantics.',
    steps: ['Collect', 'Classify', 'Explain guardrails', 'Link source', 'Maintain'],
    outputs: ['Protocol list', 'Safety map', 'Implementation pointers']
  },
  {
    repo: 'starlight-swarm',
    title: 'Starlight Swarm',
    layer: 'L6',
    subtitle: 'Queen-worker runtime for governed income streams.',
    headerVisual: 'swarm-runtime',
    mapVisual: 'payments-safety-spine',
    chips: ['Founder', 'Queens', 'Workers', 'Escalation'],
    role: 'Models founder, queens, workers, and escalation with verify-only payments integration.',
    primaryPath: 'Founder intent -> queen plan -> worker tasks -> escalation when risk rises.',
    proofGate: 'Escalation spine and payments adapter are unit-tested.',
    steps: ['Receive intent', 'Coordinate queens', 'Dispatch workers', 'Escalate risk', 'Record receipts'],
    outputs: ['Runtime primitives', 'Escalation tests', 'Payments adapter']
  },
  {
    repo: 'starlight-evals',
    title: 'Starlight Evals',
    layer: 'L7',
    subtitle: 'Whole-system evals and income/payments red-blue lane.',
    headerVisual: 'red-blue-assurance',
    mapVisual: 'build-deploy-verify',
    chips: ['R1-R6 probes', 'Scorecards', 'Receipts', 'Named weaknesses'],
    role: 'Records receipts, named weaknesses, and red-blue probes before the stack touches real funds.',
    primaryPath: 'Run probes -> collect receipts -> score risk -> gate release.',
    proofGate: 'R4/R5/R6 lanes prove income and payments defenses before promotion.',
    steps: ['Probe', 'Attack the workflow', 'Apply guardrail', 'Score evidence', 'Gate release'],
    outputs: ['Runnable evals', 'Scorecards', 'Release evidence']
  }
]

const sites = [
  {
    repo: 'agenticincome',
    name: 'Agentic Income',
    layer: 'L4 hub',
    domain: 'agenticincome.ai',
    heroVisual: 'income-engine-flow',
    explainerVisual: 'website-growth-loop',
    ogVisual: 'income-engine-flow',
    headline: 'Build a system that earns.',
    deck: 'Research demand, compare honestly, bind the catalog, and audit every recommendation.'
  },
  {
    repo: 'agentic-income-template',
    name: 'Agentic Income Template',
    layer: 'L4 template',
    domain: 'example.com',
    heroVisual: 'website-growth-loop',
    explainerVisual: 'income-engine-flow',
    ogVisual: 'website-growth-loop',
    headline: 'Fork the engine, ship your niche.',
    deck: 'A cloneable site system for honest AI-tool comparisons and recurring affiliate paths.'
  },
  {
    repo: 'agenticpassiveincome',
    name: 'Agentic Passive Income',
    layer: 'L4 spoke',
    domain: 'agenticpassiveincome.ai',
    heroVisual: 'website-growth-loop',
    explainerVisual: 'income-engine-flow',
    ogVisual: 'website-growth-loop',
    headline: 'Set it once, review the loop.',
    deck: 'Passive-income positioning on the same audited hub-and-spoke engine.'
  }
]

const repoByName = Object.fromEntries(repos.map((repo) => [repo.repo, repo]))

function ensureDir(path) {
  mkdirSync(path, { recursive: true })
}

function cleanDir(path) {
  rmSync(path, { recursive: true, force: true })
  ensureDir(path)
}

function escapeXml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
}

function wrapWords(text, maxChars) {
  const words = text.split(/\s+/)
  const lines = []
  let line = ''
  for (const word of words) {
    const next = line ? `${line} ${word}` : word
    if (next.length > maxChars && line) {
      lines.push(line)
      line = word
    } else {
      line = next
    }
  }
  if (line) {
    lines.push(line)
  }
  return lines
}

function textBlock({ text, x, y, size, weight = 500, fill = '#e5eefb', maxChars = 48, lineHeight = 1.22, opacity = 1 }) {
  const lines = wrapWords(text, maxChars)
  return `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="${fill}" opacity="${opacity}">${lines
    .map((line, index) => `<tspan x="${x}" dy="${index === 0 ? 0 : size * lineHeight}">${escapeXml(line)}</tspan>`)
    .join('')}</text>`
}

function pill({ x, y, text, fill = 'rgba(255,255,255,0.07)', stroke = 'rgba(255,255,255,0.16)', color = '#dff7ff' }) {
  const width = Math.max(92, 18 + text.length * 8.1)
  return `<g>
    <rect x="${x}" y="${y}" width="${width}" height="34" rx="17" fill="${fill}" stroke="${stroke}"/>
    <text x="${x + 16}" y="${y + 22}" font-size="14" font-weight="700" fill="${color}">${escapeXml(text)}</text>
  </g>`
}

function stepCard({ x, y, w, h, n, title, body, accent }) {
  const titleMax = Math.max(12, Math.floor((w - 44) / 10.5))
  const bodyMax = Math.max(24, Math.floor((w - 44) / 7.2))
  const titleLines = wrapWords(title, titleMax)
  const bodyY = y + 60 + titleLines.length * 23
  return `<g>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="rgba(5,8,14,0.74)" stroke="rgba(255,255,255,0.18)"/>
    <rect x="${x}" y="${y}" width="5" height="${h}" rx="2.5" fill="${accent}"/>
    <text x="${x + 22}" y="${y + 31}" font-size="13" font-weight="900" fill="${accent}">${escapeXml(n)}</text>
    ${textBlock({ text: title, x: x + 22, y: y + 61, size: 21, weight: 850, fill: '#f8fafc', maxChars: titleMax, lineHeight: 1.05 })}
    ${textBlock({ text: body, x: x + 22, y: bodyY, size: 14, fill: '#b6c2d6', maxChars: bodyMax, lineHeight: 1.22 })}
  </g>`
}

function defs() {
  return `<defs>
    <linearGradient id="shade" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#02040a" stop-opacity="0.86"/>
      <stop offset="45%" stop-color="#02040a" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#02040a" stop-opacity="0.82"/>
    </linearGradient>
    <linearGradient id="topFade" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#02040a" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#02040a" stop-opacity="0"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#000000" flood-opacity="0.42"/>
    </filter>
  </defs>`
}

function baseImage(slug, hrefPrefix, w, h, opacity = 0.88) {
  return `<image href="${hrefPrefix}/${slug}.png" x="0" y="0" width="${w}" height="${h}" preserveAspectRatio="xMidYMid slice" opacity="${opacity}"/>`
}

function headerSvg(repo) {
  const visual = visuals[repo.headerVisual]
  const chips = repo.chips.slice(0, 4)
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640" role="img" aria-labelledby="title desc" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
  <title id="title">${escapeXml(repo.title)} premium GitHub header</title>
  <desc id="desc">${escapeXml(repo.subtitle)}</desc>
  ${defs()}
  <rect width="1280" height="640" fill="#05070d"/>
  ${baseImage(repo.headerVisual, 'visual-suite/backplates', 1280, 640)}
  <rect width="1280" height="640" fill="url(#shade)"/>
  <rect width="1280" height="220" fill="url(#topFade)"/>
  <rect x="24" y="24" width="1232" height="592" rx="30" fill="none" stroke="rgba(255,255,255,0.18)"/>
  <text x="56" y="78" font-size="15" font-weight="900" fill="${visual.accent}" letter-spacing="3">${escapeXml(repo.layer)} / ${escapeXml(visual.kicker)}</text>
  ${textBlock({ text: repo.title, x: 56, y: 154, size: 66, weight: 900, fill: '#f8fafc', maxChars: 28, lineHeight: 0.98 })}
  ${textBlock({ text: repo.subtitle, x: 58, y: 262, size: 25, weight: 650, fill: '#d7e2f3', maxChars: 58, lineHeight: 1.25 })}
  <g transform="translate(58 326)">
    ${chips.map((chip, index) => pill({ x: index * 178, y: 0, text: chip, color: index === 0 ? visual.accent : '#dff7ff' })).join('')}
  </g>
  <g filter="url(#softShadow)">
    <rect x="58" y="420" width="360" height="116" rx="22" fill="rgba(3,7,18,0.72)" stroke="rgba(255,255,255,0.18)"/>
    <rect x="448" y="420" width="360" height="116" rx="22" fill="rgba(3,7,18,0.72)" stroke="rgba(255,255,255,0.18)"/>
    <rect x="838" y="420" width="360" height="116" rx="22" fill="rgba(3,7,18,0.72)" stroke="rgba(255,255,255,0.18)"/>
    <text x="84" y="455" font-size="13" font-weight="900" fill="${visual.accent}" letter-spacing="2">ROLE</text>
    ${textBlock({ text: repo.role, x: 84, y: 485, size: 17, weight: 600, fill: '#e5eefb', maxChars: 34, lineHeight: 1.22 })}
    <text x="474" y="455" font-size="13" font-weight="900" fill="${visual.accent}" letter-spacing="2">PRIMARY PATH</text>
    ${textBlock({ text: repo.primaryPath, x: 474, y: 485, size: 17, weight: 600, fill: '#e5eefb', maxChars: 34, lineHeight: 1.22 })}
    <text x="864" y="455" font-size="13" font-weight="900" fill="${visual.accent}" letter-spacing="2">PROOF GATE</text>
    ${textBlock({ text: repo.proofGate, x: 864, y: 485, size: 17, weight: 600, fill: '#e5eefb', maxChars: 34, lineHeight: 1.22 })}
  </g>
  <text x="58" y="588" font-size="13" font-weight="800" fill="#8ea3bd">Premium visual suite ${version} / imagegen backplate + deterministic SVG text</text>
</svg>
`
}

function howSvg(repo) {
  const visual = visuals[repo.mapVisual]
  const stepCount = repo.steps.length
  const cardW = stepCount <= 4 ? 270 : 222
  const gap = stepCount <= 4 ? 28 : 18
  const startX = 54
  const cardBodies = ['Start from source truth.', 'Create the artifact.', 'Keep evidence attached.', 'Escalate risky actions.', 'Ship after checks pass.', 'Promote only with proof.', 'Verify the live surface.']
  const cards = repo.steps.map((step, index) =>
    stepCard({
      x: startX + index * (cardW + gap),
      y: 390,
      w: cardW,
      h: 178,
      n: String(index + 1).padStart(2, '0'),
      title: step,
      body: cardBodies[index] ?? 'Keep the path auditable.',
      accent: visual.accent
    })
  )
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
  <title id="title">${escapeXml(repo.title)} operating map</title>
  <desc id="desc">${escapeXml(repo.role)}</desc>
  ${defs()}
  <rect width="1280" height="720" fill="#05070d"/>
  ${baseImage(repo.mapVisual, 'visual-suite/backplates', 1280, 720)}
  <rect width="1280" height="720" fill="url(#shade)"/>
  <rect x="28" y="28" width="1224" height="664" rx="32" fill="none" stroke="rgba(255,255,255,0.18)"/>
  <text x="56" y="82" font-size="15" font-weight="900" fill="${visual.accent}" letter-spacing="3">${escapeXml(repo.layer)} / HOW THIS REPO WORKS</text>
  ${textBlock({ text: repo.title, x: 56, y: 152, size: 54, weight: 900, fill: '#f8fafc', maxChars: 34, lineHeight: 1.02 })}
  ${textBlock({ text: repo.role, x: 58, y: 236, size: 22, weight: 650, fill: '#d7e2f3', maxChars: 72, lineHeight: 1.25 })}
  <g>
    <rect x="856" y="76" width="340" height="220" rx="24" fill="rgba(3,7,18,0.72)" stroke="rgba(255,255,255,0.18)"/>
    <text x="884" y="116" font-size="13" font-weight="900" fill="${visual.accent}" letter-spacing="2">OUTPUTS</text>
    ${repo.outputs.map((out, index) => `<g>
      <circle cx="895" cy="${154 + index * 48}" r="6" fill="${visual.accent}"/>
      <text x="914" y="${161 + index * 48}" font-size="20" font-weight="750" fill="#f8fafc">${escapeXml(out)}</text>
    </g>`).join('')}
  </g>
  <line x1="70" y1="360" x2="1188" y2="360" stroke="${visual.accent}" stroke-width="2" opacity="0.65"/>
  ${cards.join('')}
  <text x="58" y="652" font-size="13" font-weight="800" fill="#8ea3bd">Backplate: ${escapeXml(visual.title)} / exact labels rendered in SVG</text>
</svg>
`
}

function masterSvg(visual, hrefPrefix = '../backplates') {
  const w = 1280
  const h = 720
  const cardW = visual.steps.length <= 4 ? 258 : visual.steps.length === 7 ? 154 : 204
  const gap = visual.steps.length === 7 ? 14 : 18
  const total = visual.steps.length * cardW + (visual.steps.length - 1) * gap
  const startX = (w - total) / 2
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="title desc" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
  <title id="title">${escapeXml(visual.title)}</title>
  <desc id="desc">${escapeXml(visual.story)}</desc>
  ${defs()}
  <rect width="${w}" height="${h}" fill="#05070d"/>
  ${baseImage(visual.slug, hrefPrefix, w, h)}
  <rect width="${w}" height="${h}" fill="url(#shade)"/>
  <rect x="28" y="28" width="1224" height="664" rx="32" fill="none" stroke="rgba(255,255,255,0.18)"/>
  <text x="56" y="82" font-size="15" font-weight="900" fill="${visual.accent}" letter-spacing="3">${escapeXml(visual.kicker)}</text>
  ${textBlock({ text: visual.title, x: 56, y: 156, size: 58, weight: 900, fill: '#f8fafc', maxChars: 34, lineHeight: 1.02 })}
  ${textBlock({ text: visual.story, x: 58, y: 244, size: 23, weight: 650, fill: '#d7e2f3', maxChars: 72, lineHeight: 1.24 })}
  <g transform="translate(58 316)">
    ${visual.homes.map((home, index) => pill({ x: index * 210, y: 0, text: home, color: index === 0 ? visual.accent : '#dff7ff' })).join('')}
  </g>
  <g>
    ${visual.steps.map((step, index) => `<g>
      <rect x="${startX + index * (cardW + gap)}" y="500" width="${cardW}" height="86" rx="17" fill="rgba(3,7,18,0.76)" stroke="rgba(255,255,255,0.18)"/>
      <text x="${startX + index * (cardW + gap) + 18}" y="533" font-size="12" font-weight="900" fill="${visual.accent}">${String(index + 1).padStart(2, '0')}</text>
      ${textBlock({ text: step, x: startX + index * (cardW + gap) + 18, y: 562, size: 18, weight: 800, fill: '#f8fafc', maxChars: cardW < 170 ? 11 : 18, lineHeight: 1.08 })}
    </g>`).join('')}
  </g>
  <text x="58" y="652" font-size="13" font-weight="800" fill="#8ea3bd">Imagegen backplate + deterministic SVG overlay / no generated text in final labels</text>
</svg>
`
}

function ogSvg(site) {
  const visual = visuals[site.ogVisual]
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
  <title id="title">${escapeXml(site.name)} open graph image</title>
  <desc id="desc">${escapeXml(site.deck)}</desc>
  ${defs()}
  <rect width="1200" height="630" fill="#05070d"/>
  ${baseImage(site.ogVisual, 'backplates', 1200, 630, 0.82)}
  <rect width="1200" height="630" fill="url(#shade)"/>
  <rect x="42" y="42" width="1116" height="546" rx="34" fill="none" stroke="rgba(255,255,255,0.18)"/>
  <text x="74" y="104" font-size="18" font-weight="900" fill="${visual.accent}" letter-spacing="3">${escapeXml(site.layer)} / ${escapeXml(site.domain)}</text>
  ${textBlock({ text: site.name, x: 74, y: 200, size: 76, weight: 900, fill: '#f8fafc', maxChars: 24, lineHeight: 0.98 })}
  ${textBlock({ text: site.headline, x: 78, y: 318, size: 34, weight: 800, fill: '#d7e2f3', maxChars: 44, lineHeight: 1.18 })}
  ${textBlock({ text: site.deck, x: 78, y: 398, size: 25, weight: 650, fill: '#b6c2d6', maxChars: 58, lineHeight: 1.26 })}
  <g transform="translate(78 510)">
    ${visual.steps.slice(0, 5).map((step, index) => pill({ x: index * 172, y: 0, text: step, color: index === 0 ? visual.accent : '#dff7ff' })).join('')}
  </g>
</svg>
`
}

function suiteManifest(repo) {
  return {
    version,
    generatedAt: today,
    repo: repo.repo,
    title: repo.title,
    layer: repo.layer,
    publicAssets: {
      header: 'assets/github/header.svg',
      howItWorks: 'assets/github/how-it-works.svg',
      buildDeployVerify: 'assets/github/build-deploy-verify.svg',
      visualSuite: 'assets/github/visual-suite.json'
    },
    mapping: {
      headerVisual: repo.headerVisual,
      howItWorksVisual: repo.mapVisual,
      buildDeployVerifyVisual: 'build-deploy-verify'
    },
    method: 'Built-in image_gen created text-free backplates. All labels, repo names, paths, and captions are deterministic SVG text.',
    sources: [
      'C:/Users/frank/.codex/skills/.system/imagegen/SKILL.md',
      'C:/Users/frank/starlight/repos/DESIGN_TASTE.md',
      'C:/Users/frank/starlight/repos/WEB_EXPERIENCE_STANDARD.md',
      'C:/Users/frank/starlight/repos/VISUAL_QA_GATE.md',
      'Motion Design Studio designer-thinking.md'
    ]
  }
}

function provenance(repo) {
  return {
    repo: repo.repo,
    title: repo.title,
    layer: repo.layer,
    visualSystemVersion: version,
    generatedAt: today,
    assetStrategy: 'Imagegen provides text-free backplates; deterministic SVG overlays provide exact GitHub and website infographic text.',
    headerVisual: repo.headerVisual,
    howItWorksVisual: repo.mapVisual,
    imagegen: {
      mode: 'built-in image_gen',
    backplates: [repo.headerVisual, repo.mapVisual, 'build-deploy-verify'].map((slug) => ({
        slug,
        title: visuals[slug].title,
        sourcePath: visuals[slug].source,
        promptFile: repo.repo === 'agentic-ops-hub' ? `assets/github/visual-suite/prompts/${slug}.txt` : null
      }))
    },
    deterministicText: {
      reason: 'Exact labels and workflow copy are not rendered by the image model.',
      files: ['assets/github/header.svg', 'assets/github/how-it-works.svg', 'assets/github/visual-suite.json']
    }
  }
}

function copyBackplates(repoRoot, slugs) {
  const backplateDir = join(repoRoot, 'assets', 'github', 'visual-suite', 'backplates')
  if (repoRoot === opsRoot) {
    return
  }
  cleanDir(backplateDir)
  for (const slug of [...new Set(slugs)]) {
    copyFileSync(join(opsRoot, 'assets', 'github', 'visual-suite', 'backplates', `${slug}.png`), join(backplateDir, `${slug}.png`))
  }
}

function buildDeploySvg(repo) {
  const visual = visuals['build-deploy-verify']
  const steps = ['Branch', 'Local gates', 'PR', 'CI', 'Preview', 'Main', 'Live check']
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
  <title id="title">${escapeXml(repo.title)} build deploy verify path</title>
  <desc id="desc">Branch, local gates, PR, CI, preview, main, and live verification for ${escapeXml(repo.title)}.</desc>
  ${defs()}
  <rect width="1280" height="720" fill="#05070d"/>
  ${baseImage('build-deploy-verify', 'visual-suite/backplates', 1280, 720)}
  <rect width="1280" height="720" fill="url(#shade)"/>
  <rect x="28" y="28" width="1224" height="664" rx="32" fill="none" stroke="rgba(255,255,255,0.18)"/>
  <text x="56" y="82" font-size="15" font-weight="900" fill="${visual.accent}" letter-spacing="3">${escapeXml(repo.layer)} / SHIPPING PATH</text>
  ${textBlock({ text: `${repo.title}: build, deploy, verify`, x: 56, y: 156, size: 52, weight: 900, fill: '#f8fafc', maxChars: 38, lineHeight: 1.02 })}
  ${textBlock({ text: 'Every visual and site change moves through a concrete evidence path before it is treated as live.', x: 58, y: 246, size: 23, weight: 650, fill: '#d7e2f3', maxChars: 76, lineHeight: 1.24 })}
  <line x1="70" y1="382" x2="1190" y2="382" stroke="${visual.accent}" stroke-width="2" opacity="0.66"/>
  ${steps.map((step, index) => {
    const w = 146
    const x = 58 + index * 171
    return `<g>
      <rect x="${x}" y="430" width="${w}" height="112" rx="18" fill="rgba(3,7,18,0.76)" stroke="rgba(255,255,255,0.18)"/>
      <text x="${x + 18}" y="464" font-size="12" font-weight="900" fill="${visual.accent}">${String(index + 1).padStart(2, '0')}</text>
      ${textBlock({ text: step, x: x + 18, y: 496, size: 18, weight: 850, fill: '#f8fafc', maxChars: 14, lineHeight: 1.1 })}
    </g>`
  }).join('')}
  <text x="58" y="652" font-size="13" font-weight="800" fill="#8ea3bd">Local fast gates -> PR evidence -> preview/live verification; no live claim without a verified URL.</text>
</svg>
`
}

function readmeVisualBlock(repo) {
  return `<!-- GITHUB_VISUALS_START -->
<p align="center">
  <img src="assets/github/header.svg" alt="${repo.title} - ${repo.subtitle}" width="100%">
</p>

<details open>
<summary><strong>How this repo works</strong></summary>
<p align="center">
  <img src="assets/github/how-it-works.svg" alt="${repo.title} operating map" width="100%">
</p>
</details>

<details>
<summary><strong>Build, deploy, verify path</strong></summary>
<p align="center">
  <img src="assets/github/build-deploy-verify.svg" alt="${repo.title} build deploy verify path" width="100%">
</p>
</details>

<!-- GITHUB_VISUALS_END -->`
}

function updateReadme(repo) {
  const readmePath = join(estateRoot, repo.repo, 'README.md')
  if (!existsSync(readmePath)) {
    return
  }
  const current = readFileSync(readmePath, 'utf8')
  const nextBlock = readmeVisualBlock(repo)
  const pattern = /<!-- GITHUB_VISUALS_START -->[\s\S]*?<!-- GITHUB_VISUALS_END -->/
  const next = pattern.test(current) ? current.replace(pattern, nextBlock) : `${nextBlock}\n\n${current}`
  writeFileSync(readmePath, next)
}

function writeRepoAssets(repo) {
  const repoRoot = join(estateRoot, repo.repo)
  const assetsDir = join(repoRoot, 'assets', 'github')
  ensureDir(assetsDir)
  copyBackplates(repoRoot, [repo.headerVisual, repo.mapVisual, 'build-deploy-verify'])
  writeFileSync(join(assetsDir, 'header.svg'), headerSvg(repo))
  writeFileSync(join(assetsDir, 'how-it-works.svg'), howSvg(repo))
  writeFileSync(join(assetsDir, 'build-deploy-verify.svg'), buildDeploySvg(repo))
  writeFileSync(join(assetsDir, 'visual-suite.json'), `${JSON.stringify(suiteManifest(repo), null, 2)}\n`)
  writeFileSync(join(assetsDir, 'provenance.json'), `${JSON.stringify(provenance(repo), null, 2)}\n`)
  updateReadme(repo)
}

function writeOpsSuite() {
  const suiteDir = join(opsRoot, 'assets', 'github', 'visual-suite')
  ensureDir(suiteDir)
  const exportsDir = join(suiteDir, 'exports')
  const promptsDir = join(suiteDir, 'prompts')
  const sourceDir = join(suiteDir, 'source')
  cleanDir(exportsDir)
  cleanDir(promptsDir)
  ensureDir(sourceDir)

  for (const visual of visualList) {
    writeFileSync(join(exportsDir, `${visual.slug}.svg`), masterSvg(visual))
    writeFileSync(join(promptsDir, `${visual.slug}.txt`), `${visual.prompt}\n`)
  }

  writeFileSync(
    join(sourceDir, 'visual-suite-data.json'),
    `${JSON.stringify(
      {
        version,
        generatedAt: today,
        visuals: visualList.map(({ prompt, ...visual }) => ({ ...visual, promptFile: `../prompts/${visual.slug}.txt` })),
        repos
      },
      null,
      2
    )}\n`
  )

  writeFileSync(
    join(suiteDir, 'README.md'),
    `# Premium Visual Suite

Generated: ${today}

This directory contains the second-wave GitHub and website infographic system.

- Backplates: text-free imagegen PNGs in \`backplates/\`.
- Master exports: deterministic SVG overlays in \`exports/\`.
- Prompts: exact imagegen prompts in \`prompts/\`.
- Source data: repo and visual mappings in \`source/visual-suite-data.json\`.

Final published repo assets keep the existing contract:

- \`assets/github/header.svg\`
- \`assets/github/how-it-works.svg\`
- \`assets/github/visual-suite.json\`
- \`assets/github/provenance.json\`

Text policy: imagegen never owns exact explanatory copy. All repo names, workflow labels, and captions are rendered in SVG.
`
  )

  writeFileSync(
    join(opsRoot, 'docs', 'PREMIUM_VISUAL_SUITE.md'),
    `# Premium GitHub And Website Infographic System

Date: ${today}

## What changed

The first visual wave gave each repo a clear README header and operating map. This second wave upgrades the estate into an eight-image visual storytelling suite:

${visualList.map((visual) => `- **${visual.title}**: ${visual.story}`).join('\n')}

## Design decisions

- Imagegen is used for premium text-free backplates.
- Deterministic SVG renders all text, labels, repo names, arrows, and workflow copy.
- Each repo keeps \`assets/github/header.svg\` and \`assets/github/how-it-works.svg\`.
- \`visual-suite.json\` records which master visuals each repo uses.
- The three Next.js sites receive deployable \`public/visuals/*\` assets, but live publishing still depends on Vercel project/domain linkage.

## Regeneration

Run from \`agentic-ops-hub\` inside the clean premium workspace:

\`\`\`bash
node scripts/generate-premium-visual-suite.mjs
\`\`\`

The script expects sibling checkouts for all 11 repos.
`
  )
}

function copySiteVisuals(site) {
  const siteRoot = join(estateRoot, site.repo)
  const publicVisuals = join(siteRoot, 'public', 'visuals')
  const publicBackplates = join(publicVisuals, 'backplates')
  ensureDir(publicVisuals)
  cleanDir(publicBackplates)

  const slugs = [...new Set([site.heroVisual, site.explainerVisual, site.ogVisual])]
  for (const slug of slugs) {
    copyFileSync(join(opsRoot, 'assets', 'github', 'visual-suite', 'backplates', `${slug}.png`), join(publicBackplates, `${slug}.png`))
    writeFileSync(join(publicVisuals, `${slug}.svg`), masterSvg(visuals[slug], 'backplates'))
  }
  writeFileSync(join(publicVisuals, 'opengraph.svg'), ogSvg(site))
  writeFileSync(
    join(publicVisuals, 'visuals.json'),
    `${JSON.stringify(
      {
        version,
        generatedAt: today,
        site: site.name,
        hero: `/visuals/${site.heroVisual}.svg`,
        explainer: `/visuals/${site.explainerVisual}.svg`,
        openGraph: '/visuals/opengraph.svg',
        backplates: slugs.map((slug) => `/visuals/backplates/${slug}.png`)
      },
      null,
      2
    )}\n`
  )
}

writeOpsSuite()
for (const repo of repos) {
  writeRepoAssets(repo)
}
for (const site of sites) {
  copySiteVisuals(site)
}

console.log(`Generated premium visual suite ${version}`)
console.log(`Ops root: ${opsRoot}`)
console.log(`Sibling repos: ${repos.map((repo) => repo.repo).join(', ')}`)
