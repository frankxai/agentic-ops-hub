#!/usr/bin/env node
// Roll the Estate Ops Governance workflows into target repos.
// Dry-run by default: prints exactly what it would do and changes nothing.
//
//   node scripts/rollout-ops-governance.mjs                # dry run, all targets
//   node scripts/rollout-ops-governance.mjs --repo arcanea # dry run, one repo
//   node scripts/rollout-ops-governance.mjs --apply        # actually open PRs (needs gh authed)
//
// Per-repo it: creates a branch, adds .github/workflows/estate-pr-guardian.yml, and opens a
// DRAFT PR. estate-digest.yml installs only into the hub repo (agentic-ops-hub). Nothing runs
// until that PR is merged AND the repo has ANTHROPIC_API_KEY + ESTATE_AUTONOMY set.
// See docs/ESTATE-OPS-ACTIVATION.md.

import { execSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const HUB = join(HERE, '..');
const OWNER = 'frankxai';

// Default recommended autonomy per repo. Production site stays conservative.
const TARGETS = [
  { repo: 'agentic-creator-os', autonomy: 'assist' },
  { repo: 'claude-skills-library', autonomy: 'auto' },
  { repo: 'agentic-ops-hub', autonomy: 'assist', hub: true },
  { repo: 'frankx.ai-vercel-website', autonomy: 'assist' }, // never auto — production
  { repo: 'FrankX', autonomy: 'assist' },
  { repo: 'vibe-os', autonomy: 'auto' },
];

const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const only = args.includes('--repo') ? args[args.indexOf('--repo') + 1] : null;
const targets = only ? TARGETS.filter((t) => t.repo === only) : TARGETS;

const guardian = readFileSync(join(HUB, 'templates/workflows/estate-pr-guardian.yml'), 'utf8');
const digest = readFileSync(join(HUB, 'templates/workflows/estate-digest.yml'), 'utf8');

function sh(cmd, opts = {}) {
  return execSync(cmd, { stdio: opts.capture ? 'pipe' : 'inherit', encoding: 'utf8', ...opts });
}

console.log(`Estate Ops rollout — ${APPLY ? 'APPLY' : 'DRY RUN'} — ${targets.length} repo(s)\n`);

for (const t of targets) {
  const slug = `${OWNER}/${t.repo}`;
  const files = ['.github/workflows/estate-pr-guardian.yml'];
  if (t.hub) files.push('.github/workflows/estate-digest.yml');
  console.log(`• ${slug}  (autonomy=${t.autonomy})`);
  console.log(`    would add: ${files.join(', ')}`);
  console.log(`    then set: gh variable set ESTATE_AUTONOMY -b ${t.autonomy} -R ${slug}`);
  console.log(`    then set: gh secret   set ANTHROPIC_API_KEY -R ${slug}   (your key)`);
  if (!APPLY) { console.log('    (dry run — nothing changed)\n'); continue; }

  // APPLY path: clone shallow into a temp dir, branch, add files, PR. Requires gh + git authed.
  const tmp = `/tmp/estate-rollout-${t.repo}`;
  sh(`rm -rf ${tmp} && gh repo clone ${slug} ${tmp} -- --depth=1`);
  const branch = 'ops/estate-governance';
  sh(`git -C ${tmp} checkout -B ${branch}`);
  sh(`mkdir -p ${tmp}/.github/workflows`);
  writeInto(`${tmp}/.github/workflows/estate-pr-guardian.yml`, guardian);
  if (t.hub) writeInto(`${tmp}/.github/workflows/estate-digest.yml`, digest);
  sh(`git -C ${tmp} add .github/workflows/ && git -C ${tmp} -c user.name=estate-ops -c user.email=ops@frankx.ai commit -m "ci: add Estate PR Guardian (off until ESTATE_AUTONOMY + key set)"`);
  sh(`git -C ${tmp} push -u origin ${branch} --force-with-lease`);
  sh(`gh pr create -R ${slug} --draft --base main --head ${branch} --title "ci: Estate Ops Governance" --body "Adds the estate-governed PR guardian. Off until ESTATE_AUTONOMY (${t.autonomy}) + ANTHROPIC_API_KEY are set. See agentic-ops-hub/docs/ESTATE-OPS-GOVERNANCE.md."`);
  console.log('    ✓ draft PR opened\n');
}

function writeInto(path, content) {
  execSync(`cat > ${path} <<'ESTATE_EOF'\n${content}\nESTATE_EOF`, { stdio: 'inherit', shell: '/bin/bash' });
}

if (!APPLY) console.log('Re-run with --apply to open the draft PRs (nothing merges automatically).');
