#!/usr/bin/env node
/**
 * init-harness.mjs — Initialize any repository with the standard Agentic Harness files.
 *
 * Usage:
 *   node scripts/init-harness.mjs --dir <target-dir> --type <classification> [--health <command>]
 *
 * Classifications:
 *   - substrate  (agent-substrate)
 *   - product    (product-or-production)
 *   - content    (content-or-program)
 *   - library    (library-or-tooling)
 *   - study      (study-or-template)
 *
 * Example:
 *   node scripts/init-harness.mjs --dir C:/Users/frank/AnimeLegends.ai --type product --health "pnpm build"
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const args = process.argv.slice(2);
let targetDir = process.cwd();
let repoType = 'library';
let healthCmd = 'git status';

// Parse arguments
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--dir' && args[i + 1]) {
    targetDir = path.resolve(args[i + 1]);
  } else if (args[i] === '--type' && args[i + 1]) {
    repoType = args[i + 1];
  } else if (args[i] === '--health' && args[i + 1]) {
    healthCmd = args[i + 1];
  }
}

const OPS_HOME = 'C:/Users/frank/agentic-ops';
const TEMPLATE_AGENTS = path.join(OPS_HOME, 'templates/AGENTS.md');
const TEMPLATE_CLAUDE = path.join(OPS_HOME, 'templates/CLAUDE.md');

// Map command-line shorthand to canonical classifications
const TYPE_MAP = {
  substrate: 'agent-substrate',
  product: 'product-or-production',
  content: 'content-or-program',
  library: 'library-or-tooling',
  study: 'study-or-template',
};

const canonicalType = TYPE_MAP[repoType] || repoType;

function run() {
  console.log(`🚀 Initializing Agentic Harness in: ${targetDir}`);
  
  if (!fs.existsSync(targetDir)) {
    console.error(`❌ Target directory does not exist: ${targetDir}`);
    process.exit(1);
  }

  // 1. Write AGENTS.md if missing
  const destAgents = path.join(targetDir, 'AGENTS.md');
  if (!fs.existsSync(destAgents)) {
    console.log('📝 Copying AGENTS.md template...');
    fs.copyFileSync(TEMPLATE_AGENTS, destAgents);
  } else {
    console.log('✓ AGENTS.md already exists');
  }

  // 2. Write CLAUDE.md if missing
  const destClaude = path.join(targetDir, 'CLAUDE.md');
  if (!fs.existsSync(destClaude)) {
    console.log('📝 Copying CLAUDE.md template...');
    fs.copyFileSync(TEMPLATE_CLAUDE, destClaude);
  } else {
    console.log('✓ CLAUDE.md already exists');
  }

  // 3. Construct .agent-harness.json
  const deployPolicy = (canonicalType === 'product-or-production') ? 'protected' : 
                       (canonicalType === 'agent-substrate') ? 'restricted' : 'none';
                       
  const globalHooks = (canonicalType === 'agent-substrate');

  const harnessConfig = {
    risk: canonicalType,
    health: healthCmd,
    agentFiles: ['AGENTS.md', 'CLAUDE.md'],
    deployPolicy: deployPolicy,
    globalHooksAllowed: globalHooks
  };

  const destHarness = path.join(targetDir, '.agent-harness.json');
  console.log('⚙️ Generating .agent-harness.json...');
  fs.writeFileSync(destHarness, JSON.stringify(harnessConfig, null, 2) + '\n');

  // 4. Run rule compilation in target directory context
  console.log('⚡ Compiling behavioral rule fanning...');
  try {
    execSync(`node "${path.join(OPS_HOME, 'scripts/sync-agent-rules.mjs')}"`, {
      cwd: targetDir,
      stdio: 'inherit'
    });
  } catch (e) {
    console.error('⚠️  Failed to compile fanned rules:', e.message);
  }

  console.log('\n🎉 Repository harness initialized successfully!');
}

run();
