#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { readdirSync } from 'node:fs';
import { join } from 'node:path';
const root = import.meta.dirname;
const run = (command, args, cwd = root) => {
  const r = spawnSync(command, args, { cwd, stdio: 'inherit', timeout: 180000, shell: false });
  if (r.error || r.status !== 0) process.exit(r.status || 1);
};
run(process.execPath, ['--test', ...readdirSync(join(root, 'tests')).filter(x => x.endsWith('.test.mjs')).map(x => join(root, 'tests', x))]);
run(process.execPath, ['--test', 'test/coordinator.test.mjs'], join(root, 'cloudflare'));
run(process.platform === 'win32' ? 'npm.cmd' : 'npm', ['run', 'build'], join(root, 'cloudflare'));
const index = process.argv.indexOf('--demo');
if (index >= 0) run(process.execPath, [join(root, 'demo.mjs'), ...process.argv.slice(index + 1)]);
console.log('Execution candidate verification PASS; paid-model and production gates remain separate.');
