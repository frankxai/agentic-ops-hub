#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

const requiredFiles = [
  'AGENTS.md',
  'templates/AGENTS.md',
  'docs/AGENT_LOOP_OS.md',
  'ops/agent-loop-contract.v1.json',
  '.cursor/rules/coding-guardrails.mdc',
  '.clinerules/coding-guardrails.md',
  '.github/copilot-instructions.md',
  '.claude/skills/coding-guardrails/SKILL.md'
];

const requiredPhrases = [
  '## Core Agent Execution Loop',
  'Orient:',
  'Bound:',
  'Discover:',
  'Execute:',
  'Verify:',
  'Red-team:',
  'Handoff:',
  'Do not create persona-only agents'
];

let failures = 0;

function fail(message) {
  failures += 1;
  console.error(`FAIL ${message}`);
}

for (const rel of requiredFiles) {
  if (!fs.existsSync(path.join(ROOT, rel))) {
    fail(`missing ${rel}`);
  }
}

for (const rel of [
  'AGENTS.md',
  'templates/AGENTS.md',
  '.cursor/rules/coding-guardrails.mdc',
  '.clinerules/coding-guardrails.md',
  '.github/copilot-instructions.md',
  '.claude/skills/coding-guardrails/SKILL.md'
]) {
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const phrase of requiredPhrases) {
    if (!text.includes(phrase)) fail(`${rel} lacks phrase: ${phrase}`);
  }
}

const contractPath = path.join(ROOT, 'ops/agent-loop-contract.v1.json');
if (fs.existsSync(contractPath)) {
  try {
    const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
    const steps = contract.defaultLoop?.map((step) => step.id) ?? [];
    for (const id of ['orient', 'bound', 'discover', 'execute', 'verify', 'red_team', 'handoff']) {
      if (!steps.includes(id)) fail(`contract lacks loop step: ${id}`);
    }
    if (!contract.routingRules?.singleAgentDefault) fail('contract lacks routingRules.singleAgentDefault');
    if (!Array.isArray(contract.approvalGates) || contract.approvalGates.length < 5) {
      fail('contract approval gates are too thin');
    }
  } catch (error) {
    fail(`invalid contract JSON: ${error.message}`);
  }
}

if (failures > 0) {
  console.error(`\n${failures} agent loop check(s) failed.`);
  process.exit(1);
}

console.log('Agent loop contract is present, projected, and internally consistent.');
