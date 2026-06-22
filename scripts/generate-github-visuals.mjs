import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const workspaceRoot = path.resolve(repoRoot, '..');

const generatedAt = '2026-06-22';
const visualSystemVersion = '2026.06';
const generatedBackplateSource =
  'C:/Users/frank/.codex/generated_images/019eee93-7525-7c43-bb1f-836e174dd5cb/ig_060220fbd7fa9f0f016a38fd05b6148191b3e3170d09599c13.png';

const imagegenPrompt = `Use case: stylized-concept
Asset type: GitHub README visual system backplate, no text
Primary request: A premium abstract technical backplate for an AI agent income ecosystem: layered constellation map, luminous operational grid, subtle nodes connected through capability, config, income, payments, swarm, and assurance layers.
Style/medium: high-end editorial 3D illustration, precise luminous systems design, glass-and-metal depth, dark but not murky.
Composition/framing: ultra-wide landscape composition with strong negative space in the center-left for deterministic SVG overlays later; no central text, no logos.
Lighting/mood: intelligent, trustworthy, operational, high-agency; luminous cyan, emerald, amber, and restrained violet accents on a charcoal base.
Color palette: charcoal black, deep graphite, cool cyan, emerald, amber, small violet accents; avoid one-note purple-blue gradient dominance.
Materials/textures: fine grid lines, subtle translucent planes, precise particle trails, clean glass highlights, no blur haze.
Text (verbatim): none.
Constraints: no words, no letters, no numbers, no logos, no watermarks, no UI screenshots, no humans, no finance symbols, no coins, no generic bokeh or decorative orbs.
Avoid: unreadable labels, fake text, stock-photo style, clutter, heavy gradients, dark cropped mystery.`;

const repos = [
  {
    repo: 'agentic-ops-hub',
    layer: 'L2',
    title: 'Agentic Ops Hub',
    subtitle: 'Configuration control plane for AI coding agents',
    audience: 'Developers running multi-agent coding fleets',
    status: 'Blueprint + control plane',
    accent: '#38bdf8',
    secondary: '#a78bfa',
    role: 'Keeps AGENTS.md, sync rules, MCP strategy, protection layers, and the L0-L7 map aligned.',
    chips: ['AGENTS.md', 'MCP strategy', 'Protection layers', 'Red/blue charter'],
    steps: [
      ['Source', 'One plain AGENTS.md contract'],
      ['Fan out', 'Claude, Cursor, Cline, Copilot, Codex'],
      ['Govern', 'MCP strategy and protection layers'],
      ['Map', 'L0-L7 income ecosystem blueprint'],
    ],
    risk: 'Prevents agent drift and config sprawl.',
  },
  {
    repo: 'starlight-agent-skills',
    layer: 'L1',
    title: 'Starlight Agent Skills',
    subtitle: 'Portable substrate skills for Starlight work',
    audience: 'Agents composing income, payments, and swarm behavior',
    status: '4 substrate skills',
    accent: '#22d3ee',
    secondary: '#34d399',
    role: 'Turns the income thesis, affiliate loop, payment mandate, and queen coordination into portable skills.',
    chips: ['agentic-income', 'affiliate-audit', 'payments-mandate', 'swarm-queen'],
    steps: [
      ['Trigger', 'Intent activates the matching skill'],
      ['Compose', 'Skills call each other by responsibility'],
      ['Constrain', 'Human gates and no-money invariants remain explicit'],
      ['Ingest', 'SIS and runtimes consume the same rules'],
    ],
    risk: 'Keeps capabilities substrate-level and reusable.',
  },
  {
    repo: 'agenticincome',
    layer: 'L4',
    title: 'Agentic Income',
    subtitle: 'Flagship hub for honest AI-agent income systems',
    audience: 'Creators and builders comparing AI tools that compound',
    status: 'Live content hub',
    accent: '#60a5fa',
    secondary: '#f59e0b',
    role: 'Ranks for high-intent AI tool searches, tells the truth, and routes to recurring-payer tools only when they win.',
    chips: ['Hub site', 'Comparison posts', 'Affiliate catalog', 'Owned audience'],
    steps: [
      ['Demand', 'Search queries people already ask'],
      ['Answer', 'Honest comparison shape'],
      ['Route', 'Affiliate link only when joined and true'],
      ['Compound', 'Recurring programs plus email capture'],
    ],
    risk: 'Trust stays upstream of monetization.',
    site: true,
  },
  {
    repo: 'agentic-income-template',
    layer: 'L4',
    title: 'Agentic Income Template',
    subtitle: 'Clone-and-deploy AI-tool comparison starter',
    audience: 'Builders forking a trust-first affiliate site',
    status: 'Reusable starter',
    accent: '#14b8a6',
    secondary: '#f97316',
    role: 'Packages the same honest comparison engine into a forkable Next.js template.',
    chips: ['Next.js 16', 'MDX', 'Affiliate binding', 'Forkable brand config'],
    steps: [
      ['Fork', 'Start from the template'],
      ['Brand', 'Change the site config'],
      ['Compare', 'Write source-grounded posts'],
      ['Deploy', 'Ship a spoke with the same engine'],
    ],
    risk: 'One engine, many honest sites.',
    site: true,
  },
  {
    repo: 'agentic-income-skills',
    layer: 'L4',
    title: 'Agentic Income Skills',
    subtitle: 'Portable operating brain for income systems',
    audience: 'Agents planning, auditing, and scaling income loops',
    status: '2 portable skills',
    accent: '#2dd4bf',
    secondary: '#fbbf24',
    role: 'Extracts the income thesis and affiliate audit loop into standalone skills for any coding agent.',
    chips: ['agentic-income', 'affiliate-audit', 'Audit script', 'Five principles'],
    steps: [
      ['Decide', 'What should be built next?'],
      ['Audit', 'Catalog times content times traffic'],
      ['Prioritize', 'Join programs and link gaps'],
      ['Repeat', 'Improve the money loop on cadence'],
    ],
    risk: 'Makes the money loop portable without hiding the ethics.',
  },
  {
    repo: 'awesome-agentic-income',
    layer: 'L4',
    title: 'Awesome Agentic Income',
    subtitle: 'Curated map of honest agentic income systems',
    audience: 'Builders looking for credible engines, programs, and playbooks',
    status: 'Curated resource list',
    accent: '#10b981',
    secondary: '#60a5fa',
    role: 'Separates useful recurring-income resources from generic affiliate noise.',
    chips: ['Method', 'Engines', 'Programs', 'Playbooks'],
    steps: [
      ['Curate', 'Only useful and source-grounded entries'],
      ['Explain', 'Why each resource earns attention'],
      ['Connect', 'Route to engines and templates'],
      ['Maintain', 'Keep links and terms current'],
    ],
    risk: 'Editorial usefulness beats exhaustive dumping.',
  },
  {
    repo: 'agenticpassiveincome',
    layer: 'L4',
    title: 'Agentic Passive Income',
    subtitle: 'Spoke site for set-and-review income loops',
    audience: 'Technical creators building compounding systems',
    status: 'Live spoke site',
    accent: '#48d3ac',
    secondary: '#60a5fa',
    role: 'Uses the same engine as the hub with a systems-builder passive-income angle.',
    chips: ['Spoke site', 'Passive loop', 'Shared catalog', 'Hub cross-links'],
    steps: [
      ['Choose', 'Recurring tools with real utility'],
      ['Publish', 'Search-shaped comparisons'],
      ['Route', 'Shared short-link plane'],
      ['Review', 'Update winners before pages decay'],
    ],
    risk: 'Passive does not mean unattended.',
    site: true,
  },
  {
    repo: 'payment-intelligence-system',
    layer: 'L5',
    title: 'Payment Intelligence System',
    subtitle: 'Fail-closed payments governance MCP',
    audience: 'Agents verifying payment authorization before settlement',
    status: 'v0.2 hardened scaffold',
    accent: '#f59e0b',
    secondary: '#38bdf8',
    role: 'Verifies mandates, checks caps, records audit entries, and requires humans without exposing a money-moving tool.',
    chips: ['Ed25519', 'AP2 mandate', 'Spend cap', 'Audit log'],
    steps: [
      ['Mandate', 'Was this purchase authorized?'],
      ['Cap', 'Is it under the allowed limit?'],
      ['Audit', 'Can we prove the decision?'],
      ['Human gate', 'Unknown or over-cap never auto-approves'],
    ],
    risk: 'There is no transfer tool by design.',
  },
  {
    repo: 'awesome-payment-agent-skills',
    layer: 'L5',
    title: 'Awesome Payment Agent Skills',
    subtitle: 'Curated payment protocols and safety tooling',
    audience: 'Builders giving agents spend authority safely',
    status: 'Curated protocol list',
    accent: '#fbbf24',
    secondary: '#22d3ee',
    role: 'Maps authorization, settlement, and audit tooling so agents can pay only under guardrails.',
    chips: ['AP2', 'x402', 'ACP', 'Safety tooling'],
    steps: [
      ['Authorize', 'Mandate proves human intent'],
      ['Settle', 'Rail moves value after the gate'],
      ['Audit', 'Append-only receipts'],
      ['Constrain', 'Fail closed and human-gate the unknown'],
    ],
    risk: 'Authorization and settlement stay separate.',
  },
  {
    repo: 'starlight-swarm',
    layer: 'L6',
    title: 'Starlight Swarm',
    subtitle: 'Queen-worker runtime for governed income streams',
    audience: 'Agents coordinating work without crossing money gates',
    status: 'Unit-tested safety spine',
    accent: '#8b5cf6',
    secondary: '#22d3ee',
    role: 'Models founder, queens, workers, and the escalation ladder with verify-only payments integration.',
    chips: ['Founder', 'Queens', 'Workers', 'Escalation'],
    steps: [
      ['Worker', 'Draft, audit, research, propose'],
      ['Queen', 'Coordinate one stream below caps'],
      ['Founder', 'Resolve cross-stream and structural calls'],
      ['Human', 'Approve money and irreversible actions'],
    ],
    risk: 'No autonomous money movement, ever.',
  },
  {
    repo: 'starlight-evals',
    layer: 'L7',
    title: 'Starlight Evals',
    subtitle: 'Whole-system evals and income/payments red-blue lane',
    audience: 'Operators proving the stack holds under attack',
    status: 'Runnable safety lane',
    accent: '#ef4444',
    secondary: '#38bdf8',
    role: 'Records receipts, named weaknesses, and red-blue probes before the stack touches real funds.',
    chips: ['R1-R6 probes', 'Scorecards', 'Receipts', 'Named weaknesses'],
    steps: [
      ['Attack', 'Forge, tamper, inject, bypass'],
      ['Defend', 'Reject and audit every malicious action'],
      ['Score', 'Record verdicts and weaknesses'],
      ['Harden', 'Fix the layer that failed'],
    ],
    risk: 'Green means rejected and audited, not silently lucky.',
  },
];

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function ensureDir(dir) {
  mkdirSync(dir, { recursive: true });
}

function write(file, contents) {
  ensureDir(path.dirname(file));
  writeFileSync(file, contents, 'utf8');
}

function wrapWords(text, max = 44) {
  const words = String(text).split(/\s+/);
  const lines = [];
  let line = '';
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > max && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function textBlock(lines, x, y, options = {}) {
  const {
    size = 26,
    weight = 500,
    fill = '#dbeafe',
    lineHeight = Math.round(size * 1.35),
    anchor = 'start',
    opacity = 1,
  } = options;
  return lines
    .map((line, index) => {
      return `<text x="${x}" y="${y + index * lineHeight}" text-anchor="${anchor}" font-size="${size}" font-weight="${weight}" fill="${fill}" opacity="${opacity}">${esc(line)}</text>`;
    })
    .join('\n');
}

function svgShell(width, height, accent, secondary, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#05070d"/>
      <stop offset="0.48" stop-color="#0b1220"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${accent}"/>
      <stop offset="1" stop-color="${secondary}"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="38%" r="56%">
      <stop offset="0" stop-color="${accent}" stop-opacity="0.28"/>
      <stop offset="0.5" stop-color="${secondary}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#05070d" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      text { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: 0; }
      .fine { stroke: rgba(219,234,254,0.16); stroke-width: 1; }
      .panel { fill: rgba(15,23,42,0.72); stroke: rgba(219,234,254,0.16); }
      .chip { fill: rgba(255,255,255,0.055); stroke: rgba(219,234,254,0.16); }
    </style>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#bg)"/>
  <rect width="${width}" height="${height}" fill="url(#glow)"/>
  <g opacity="0.38">
    ${Array.from({ length: 14 }, (_, i) => `<path class="fine" d="M ${-80 + i * 115} ${height} C ${160 + i * 60} ${height * 0.62}, ${420 + i * 32} ${height * 0.32}, ${width + 80} ${70 + i * 18}"/>`).join('\n')}
    ${Array.from({ length: 9 }, (_, i) => `<path class="fine" d="M ${width} ${60 + i * 74} C ${width * 0.72} ${height * 0.2 + i * 19}, ${width * 0.45} ${height * 0.78 - i * 22}, 0 ${height - 55 - i * 55}"/>`).join('\n')}
  </g>
  ${body}
</svg>
`;
}

function chip(label, x, y, width, accent) {
  return `<g>
    <rect x="${x}" y="${y}" width="${width}" height="38" rx="19" class="chip"/>
    <circle cx="${x + 20}" cy="${y + 19}" r="4" fill="${accent}" filter="url(#softGlow)"/>
    <text x="${x + 35}" y="${y + 25}" font-size="15" font-weight="650" fill="#dbeafe">${esc(label)}</text>
  </g>`;
}

function headerSvg(repo) {
  const chipWidth = [170, 178, 184, 196];
  const titleLines = wrapWords(repo.title, 23);
  const titleSize = titleLines.length > 1 ? 50 : 58;
  const titleLineHeight = titleLines.length > 1 ? 56 : 62;
  const subtitleY = 118 + titleLines.length * titleLineHeight;
  const roleY = subtitleY + 60;
  const audienceLabelY = roleY + 118;
  const audienceY = audienceLabelY + 33;
  const chipY = audienceY + 54;
  const body = `
  <title>${esc(repo.title)} GitHub header</title>
  <desc>${esc(repo.subtitle)}. ${esc(repo.role)}</desc>
  <g transform="translate(64 58)">
    <rect x="0" y="0" width="226" height="38" rx="19" fill="rgba(255,255,255,0.07)" stroke="rgba(219,234,254,0.18)"/>
    <text x="19" y="25" font-size="15" font-weight="760" fill="${repo.accent}">${repo.layer} / ${esc(repo.status)}</text>
    ${textBlock(titleLines, 0, 108, { size: titleSize, weight: 850, fill: '#f8fafc', lineHeight: titleLineHeight })}
    ${textBlock(wrapWords(repo.subtitle, 54), 2, subtitleY, { size: 26, weight: 650, fill: '#dbeafe' })}
    ${textBlock(wrapWords(repo.role, 66), 2, roleY, { size: 19, weight: 450, fill: '#94a3b8', lineHeight: 28 })}
    <text x="2" y="${audienceLabelY}" font-size="13" font-weight="760" fill="#64748b">PRIMARY AUDIENCE</text>
    ${textBlock(wrapWords(repo.audience, 58), 2, audienceY, { size: 21, weight: 650, fill: '#e2e8f0', lineHeight: 28 })}
    <g transform="translate(0 ${chipY})">
      ${repo.chips.map((label, index) => chip(label, index % 2 === 0 ? 0 : 220, Math.floor(index / 2) * 52, chipWidth[index] ?? 180, repo.accent)).join('\n')}
    </g>
  </g>
  <g transform="translate(790 80)">
    <rect x="0" y="0" width="382" height="420" rx="36" class="panel"/>
    <rect x="34" y="34" width="314" height="76" rx="22" fill="rgba(255,255,255,0.045)" stroke="rgba(219,234,254,0.14)"/>
    <text x="56" y="79" font-size="18" font-weight="780" fill="#e2e8f0">${esc(repo.layer)} operating layer</text>
    ${repo.steps.map((step, index) => {
      const y = 150 + index * 60;
      const next = index < repo.steps.length - 1 ? `<path d="M72 ${y + 30} L72 ${y + 54}" stroke="${repo.accent}" stroke-width="2" opacity="0.5"/>` : '';
      return `<g>
        <circle cx="72" cy="${y}" r="18" fill="url(#accent)" filter="url(#softGlow)"/>
        <text x="72" y="${y + 6}" text-anchor="middle" font-size="14" font-weight="800" fill="#06111f">${index + 1}</text>
        <text x="106" y="${y - 3}" font-size="17" font-weight="780" fill="#f8fafc">${esc(step[0])}</text>
        <text x="106" y="${y + 21}" font-size="13" font-weight="500" fill="#94a3b8">${esc(step[1])}</text>
        ${next}
      </g>`;
    }).join('\n')}
  </g>
  <path d="M 630 154 C 700 118, 742 128, 795 170" fill="none" stroke="${repo.accent}" stroke-width="2" opacity="0.34"/>
  <path d="M 612 396 C 690 462, 738 446, 792 396" fill="none" stroke="${repo.secondary}" stroke-width="2" opacity="0.28"/>
  <text x="64" y="594" font-size="14" font-weight="650" fill="#64748b">Visual system ${visualSystemVersion} / deterministic SVG for GitHub legibility / generated ${generatedAt}</text>`;
  return svgShell(1280, 640, repo.accent, repo.secondary, body);
}

function howSvg(repo) {
  const body = `
  <title>${esc(repo.title)} how it works map</title>
  <desc>${esc(repo.steps.map((s) => `${s[0]}: ${s[1]}`).join('. '))}</desc>
  <g transform="translate(66 58)">
    <text x="0" y="30" font-size="18" font-weight="800" fill="${repo.accent}">${repo.layer} SYSTEM MAP</text>
    <text x="0" y="86" font-size="46" font-weight="860" fill="#f8fafc">How ${esc(repo.title)} works</text>
    ${textBlock(wrapWords(repo.risk, 78), 0, 126, { size: 20, weight: 520, fill: '#94a3b8' })}
  </g>
  <g transform="translate(70 214)">
    ${repo.steps.map((step, index) => {
      const x = index * 286;
      const connector = index < repo.steps.length - 1 ? `<path d="M ${x + 222} 112 C ${x + 246} 112, ${x + 256} 112, ${x + 278} 112" stroke="${repo.accent}" stroke-width="3" opacity="0.45"/>` : '';
      return `<g>
        <rect x="${x}" y="0" width="240" height="230" rx="28" class="panel"/>
        <circle cx="${x + 58}" cy="62" r="28" fill="url(#accent)" filter="url(#softGlow)"/>
        <text x="${x + 58}" y="72" text-anchor="middle" font-size="22" font-weight="850" fill="#06111f">${index + 1}</text>
        <text x="${x + 34}" y="126" font-size="24" font-weight="820" fill="#f8fafc">${esc(step[0])}</text>
        ${textBlock(wrapWords(step[1], 22), x + 34, 162, { size: 16, weight: 520, fill: '#a8b3c7', lineHeight: 23 })}
        ${connector}
      </g>`;
    }).join('\n')}
  </g>
  <g transform="translate(90 504)">
    <rect x="0" y="0" width="1100" height="108" rx="26" fill="rgba(255,255,255,0.045)" stroke="rgba(219,234,254,0.14)"/>
    <text x="36" y="44" font-size="15" font-weight="800" fill="${repo.secondary}">OPERATING INVARIANT</text>
    ${textBlock(wrapWords(repo.risk, 96), 36, 76, { size: 20, weight: 680, fill: '#e2e8f0', lineHeight: 28 })}
  </g>`;
  return svgShell(1280, 720, repo.accent, repo.secondary, body);
}

function ecosystemSvg() {
  const layers = repos.filter((repo) => ['L1', 'L2', 'L4', 'L5', 'L6', 'L7'].includes(repo.layer));
  const groups = [
    ['L7', 'Assurance', 'starlight-evals'],
    ['L6', 'Swarm Runtime', 'starlight-swarm'],
    ['L5', 'Payments', 'payment-intelligence-system + awesome-payment-agent-skills'],
    ['L4', 'Income Engine', 'skills + hub + template + curated lists + spokes'],
    ['L2', 'Config', 'agentic-ops-hub'],
    ['L1', 'Capability', 'starlight-agent-skills'],
    ['L0', 'Substrate', 'SIS + second-brain-os'],
  ];
  const body = `
  <title>Agentic income ecosystem map</title>
  <desc>L0 through L7 operating map for capability, config, income, payments, swarm runtime, and assurance.</desc>
  <g transform="translate(60 52)">
    <text x="0" y="34" font-size="18" font-weight="820" fill="#38bdf8">CANONICAL OPERATING MAP</text>
    <text x="0" y="92" font-size="52" font-weight="880" fill="#f8fafc">Agentic income stack</text>
    <text x="0" y="132" font-size="20" font-weight="520" fill="#94a3b8">Capability -> config -> income -> payments -> swarm -> assurance, all grounded in substrate memory and human gates.</text>
  </g>
  <g transform="translate(82 188)">
    ${groups.map((group, index) => {
      const y = index * 64;
      const repo = layers.find((r) => r.layer === group[0]) ?? repos[0];
      return `<g>
        <rect x="0" y="${y}" width="1116" height="50" rx="18" fill="rgba(255,255,255,0.05)" stroke="rgba(219,234,254,0.13)"/>
        <rect x="0" y="${y}" width="96" height="50" rx="18" fill="${repo.accent}" opacity="0.22"/>
        <text x="34" y="${y + 32}" font-size="18" font-weight="850" fill="${repo.accent}">${group[0]}</text>
        <text x="124" y="${y + 32}" font-size="20" font-weight="780" fill="#f8fafc">${esc(group[1])}</text>
        <text x="370" y="${y + 32}" font-size="16" font-weight="520" fill="#94a3b8">${esc(group[2])}</text>
      </g>`;
    }).join('\n')}
  </g>
  <g transform="translate(82 654)">
    <rect x="0" y="0" width="1116" height="96" rx="24" fill="rgba(245,158,11,0.09)" stroke="rgba(245,158,11,0.32)"/>
    <text x="32" y="38" font-size="16" font-weight="850" fill="#fbbf24">MONEY SAFETY RULE</text>
    <text x="32" y="70" font-size="22" font-weight="760" fill="#f8fafc">Agents draft, verify, gate, and audit. Humans approve capital and irreversible actions.</text>
  </g>`;
  return svgShell(1280, 820, '#38bdf8', '#f59e0b', body);
}

function provenance(repo) {
  return {
    repo: repo.repo,
    title: repo.title,
    layer: repo.layer,
    visualSystemVersion,
    generatedAt,
    assetStrategy: 'Deterministic SVG for exact GitHub text and diagrams; imagegen used for a text-free style backplate only.',
    sources: [
      'C:/Users/frank/starlight/repos/DESIGN_TASTE.md',
      'C:/Users/frank/starlight/repos/WEB_EXPERIENCE_STANDARD.md',
      'C:/Users/frank/starlight/repos/VISUAL_QA_GATE.md',
      'C:/Users/frank/.codex/skills/.system/imagegen/SKILL.md',
      'Motion Design Studio designer-thinking rubric',
      'agentic-ops-hub/ECOSYSTEM.md',
    ],
    imagegen: {
      mode: 'built-in image_gen',
      sourcePath: generatedBackplateSource,
      prompt: imagegenPrompt,
      use: repo.repo === 'agentic-ops-hub' ? 'Stored as ecosystem-backplate.png and documented as a reusable style frame.' : 'Referenced by provenance; exact repo visuals are SVG.',
    },
  };
}

function visualReadme(repo) {
  return `# GitHub visual assets

Generated ${generatedAt} from the Agentic Income GitHub Visual System.

- \`header.svg\` is the README banner.
- \`how-it-works.svg\` is the repo-specific operating map.
- \`provenance.json\` records sources and imagegen usage.

The assets are deterministic SVG so labels stay crisp in GitHub READMEs. Raster image generation is reserved for text-free style frames and backgrounds.
`;
}

function readmeBlock(repo) {
  return `<!-- GITHUB_VISUALS_START -->
<p align="center">
  <img src="assets/github/header.svg" alt="${esc(repo.title)} - ${esc(repo.subtitle)}" width="100%">
</p>

<details open>
<summary><strong>How this repo works</strong></summary>
<p align="center">
  <img src="assets/github/how-it-works.svg" alt="${esc(repo.title)} operating map" width="100%">
</p>
</details>

<!-- GITHUB_VISUALS_END -->
`;
}

function stripLegacyHero(markdown) {
  let next = markdown.replace(/^\s*!\[[^\]]*\]\([^)]+\)\s*\r?\n\r?\n/, '');
  next = next.replace(/^\s*<p align="center">\s*\r?\n\s*<img[^>]+>\s*\r?\n\s*<\/p>\s*\r?\n\r?\n/i, '');
  return next;
}

function updateReadme(repo, repoDir) {
  const readmePath = path.join(repoDir, 'README.md');
  if (!existsSync(readmePath)) return;
  const start = '<!-- GITHUB_VISUALS_START -->';
  const end = '<!-- GITHUB_VISUALS_END -->';
  const block = readmeBlock(repo);
  const current = readFileSync(readmePath, 'utf8');
  const pattern = new RegExp(`${start}[\\s\\S]*?${end}\\s*`, 'm');
  const body = pattern.test(current) ? current.replace(pattern, '') : stripLegacyHero(current);
  write(readmePath, `${block}\n${body.replace(/^\s+/, '')}`);
}

function opengraphImage(repo) {
  return `import { ImageResponse } from 'next/og'
import { site } from '@/lib/site'

export const dynamic = 'force-static'
export const alt = \`${repo.title} - ${repo.subtitle}\`
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          background: 'linear-gradient(135deg, #05070d 0%, #0b1220 52%, #111827 100%)',
          color: '#f8fafc',
          fontFamily: 'Inter, Arial, sans-serif',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'radial-gradient(circle at 75% 25%, ${repo.accent}44, transparent 34%), radial-gradient(circle at 88% 70%, ${repo.secondary}33, transparent 30%)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            right: -20,
            top: 70,
            width: 430,
            height: 430,
            border: '1px solid rgba(219,234,254,0.18)',
            borderRadius: 48,
            transform: 'rotate(8deg)',
            background: 'rgba(255,255,255,0.045)',
          }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', padding: 76, width: 820, position: 'relative' }}>
          <div
            style={{
              display: 'flex',
              width: 360,
              padding: '10px 18px',
              borderRadius: 999,
              border: '1px solid rgba(219,234,254,0.18)',
              color: '${repo.accent}',
              fontSize: 24,
              fontWeight: 800,
            }}
          >
            ${repo.layer} / {site.domain}
          </div>
          <div style={{ marginTop: 42, fontSize: 78, fontWeight: 900, lineHeight: 0.95 }}>{site.name}</div>
          <div style={{ marginTop: 28, fontSize: 34, fontWeight: 700, color: '#dbeafe' }}>{site.tagline}</div>
          <div style={{ marginTop: 24, fontSize: 24, lineHeight: 1.35, color: '#94a3b8' }}>{site.description}</div>
        </div>
      </div>
    ),
    size
  )
}
`;
}

function visualSystemDoc() {
  return `# Agentic Income GitHub Visual System

Date: ${generatedAt}

This repo owns the repeatable visual system for the agentic-income GitHub estate.

## Design Thinking

- First read: each README banner must answer what the repo is, where it sits in L0-L7, and what safety or income job it performs.
- Specificity beats polish: diagrams show the actual operating contract, not abstract AI decoration.
- Text is deterministic SVG. Generated raster art may provide atmosphere, but never exact labels.
- GitHub readability wins over spectacle: high contrast, large type, no tiny baked text, no cards inside cards.

## Asset Contract

- \`assets/github/header.svg\`: 1280 x 640 README banner.
- \`assets/github/how-it-works.svg\`: 1280 x 720 repo operating map.
- \`assets/github/provenance.json\`: design sources, generated prompt, and visual-system version.
- \`assets/github/ecosystem-map.svg\`: only in \`agentic-ops-hub\`; the L0-L7 estate map.
- \`assets/github/ecosystem-backplate.png\`: only in \`agentic-ops-hub\`; text-free imagegen style frame.

## Palette Roles

- L1 capability: cyan and emerald.
- L2 config: cyan and violet.
- L4 income: blue, teal, emerald, amber.
- L5 payments: amber and cyan.
- L6 swarm: violet and cyan.
- L7 assurance: red and cyan.

## Regeneration

Run from \`agentic-ops-hub\`:

\`\`\`bash
node scripts/generate-github-visuals.mjs
\`\`\`

The generator expects sibling checkouts for the named repos in the same parent directory.
`;
}

function generateRepo(repo) {
  const repoDir = path.join(workspaceRoot, repo.repo);
  if (!existsSync(repoDir)) {
    throw new Error(`Missing sibling repo: ${repo.repo}`);
  }
  const assetDir = path.join(repoDir, 'assets', 'github');
  write(path.join(assetDir, 'header.svg'), headerSvg(repo));
  write(path.join(assetDir, 'how-it-works.svg'), howSvg(repo));
  write(path.join(assetDir, 'README.md'), visualReadme(repo));
  write(path.join(assetDir, 'provenance.json'), `${JSON.stringify(provenance(repo), null, 2)}\n`);
  updateReadme(repo, repoDir);
  if (repo.site) {
    write(path.join(repoDir, 'app', 'opengraph-image.tsx'), opengraphImage(repo));
  }
}

function main() {
  for (const repo of repos) {
    generateRepo(repo);
  }
  write(path.join(repoRoot, 'assets', 'github', 'ecosystem-map.svg'), ecosystemSvg());
  write(path.join(repoRoot, 'docs', 'GITHUB_VISUAL_SYSTEM.md'), visualSystemDoc());
  if (existsSync(generatedBackplateSource)) {
    const backplatePath = path.join(repoRoot, 'assets', 'github', 'ecosystem-backplate.png');
    ensureDir(path.dirname(backplatePath));
    copyFileSync(generatedBackplateSource, backplatePath);
  }
}

main();
