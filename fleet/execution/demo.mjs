#!/usr/bin/env node
// Real estate source + deterministic maker, transported through actual workerd/DO storage.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { createHash, randomBytes } from 'node:crypto';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { Journal, CoordinatorClient, runOnce, executeKernel } from './worker.mjs';
import { preparePublication } from './publication.mjs';

const here = import.meta.dirname;
const arg = (name) => { const i = process.argv.indexOf(`--${name}`); return i < 0 ? undefined : process.argv[i + 1]; };
const kernelRoot = resolve(arg('kernel') || process.env.STARLIGHT_KERNEL_ROOT || '');
const sourceRepo = resolve(arg('source') || join(here, '../..', '..'));
const python = arg('python') || process.env.REVIEW_PYTHON;
if (!python) throw new Error('pass --python <absolute interpreter with jsonschema==4.26.0>');
const base = '9f5999f18b9e1ec6a181b70d8b2b3ce080ded11f';
const root = mkdtempSync(join(tmpdir(), 'starlight-execution-demo-'));
const repo = join(root, 'estate-source'), home = join(root, 'kernel-home');
execFileSync('git', ['clone', '--quiet', '--no-hardlinks', '--no-checkout', sourceRepo, repo]);
execFileSync('git', ['-C', repo, 'checkout', '--quiet', '--detach', base]);
execFileSync('git', ['-C', repo, 'remote', 'set-url', 'origin', 'https://github.com/frankxai/agentic-ops-hub.git']);
const { context, operations } = await import(pathToFileURL(join(kernelRoot, 'src/cli.mjs')));
const policyPath = join(root, 'policy.json');
writeFileSync(policyPath, JSON.stringify({ classes: { bugfix: {
  maker: `shell:${join(here, 'fixtures/lab-portability-maker.mjs')}`,
  grader: `shell:${join(here, 'fixtures/lab-portability-checker.mjs')}`,
} } }));
const ctx = context({ home, policy: policyPath });
const check = `import { spawnSync } from 'node:child_process';
const nonce=process.env.STARLIGHT_ACCEPTANCE_NONCE; delete process.env.STARLIGHT_ACCEPTANCE_NONCE;
const r=spawnSync(${JSON.stringify(python)},['-B','-m','unittest','tests.test_lab_registry','tests.test_receipt_bridge','-v'],{encoding:'utf8'});
if(r.status!==0 || !r.stderr.includes('Ran 99 tests') || !/test_understated_total_cost_is_not_accepted[^\\n]* \\.\\.\\. ok/.test(r.stderr) || !r.stderr.includes('OK (skipped=2)')) { console.error(r.stderr); process.exit(1); }
console.log('STARLIGHT-ACCEPTANCE-COMPLETE',nonce);
`;
const [, contract] = operations.contractCreate({ ...ctx, spec: {
  goal: 'Move the external SIS checkout skip decorator from SemanticInvariantTests onto ConformanceTests in tests/test_receipt_bridge.py. Change only that file.',
  repo, targetRef: base, taskClass: 'bugfix',
  acceptance: { commands: ['node service-acceptance.mjs'], files: { 'service-acceptance.mjs': check }, completionMarker: 'STARLIGHT-ACCEPTANCE-COMPLETE', isolation: 'process' },
  budget: { maxAttempts: 1, makerTimeoutMs: 30000, graderTimeoutMs: 30000, maxTotalMs: 120000 },
} });
const preset = { task_kind: 'lab-portability', repository: 'frankxai/agentic-ops-hub', revision: base,
  contract_id: contract.contractId, max_seconds: 300, max_allowance_microusd: 1, isolation: 'trusted-local-fixture' };
const require = createRequire(join(here, 'cloudflare/package.json'));
const { Miniflare, convertV4MiniflareOptions } = require('miniflare');
const clientToken = randomBytes(32).toString('hex'), workerToken = randomBytes(32).toString('hex');
const persist = join(root, 'cloudflare-state');
const start = () => {
  const config = convertV4MiniflareOptions({ name: 'starlight-service-demo', modules: true,
    scriptPath: join(here, 'cloudflare/src/worker.mjs'), compatibilityDate: '2026-10-23', compatibilityFlags: ['nodejs_compat'],
    durableObjects: { EXECUTION: { className: 'ExecutionCoordinator', useSQLite: true } },
    bindings: { TENANT_ID: 'starlight-demo', EXECUTION_CLIENT_TOKEN: clientToken, EXECUTION_WORKER_TOKEN: workerToken,
      BUDGET_MICROUSD: '1', ALLOWED_REPOSITORIES_JSON: JSON.stringify([preset.repository]), ALLOWED_TASK_KINDS_JSON: JSON.stringify([preset.task_kind]) },
    telemetry: { enabled: false } });
  config.resourcePersistencePath = persist;
  return new Miniflare(config);
};
let mf = start();
const journal = new Journal(join(root, 'worker.sqlite'));
const task = { idempotency_key: 'estate-lab-portability-v1', repository: preset.repository, revision: base,
  task_kind: preset.task_kind, allowance_microusd: 1, deadline_seconds: 300 };
const rpc = async (method, params) => {
  const response = await mf.dispatchFetch('http://localhost/mcp', { method: 'POST', headers: { authorization: `Bearer ${clientToken}`, 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }) });
  const json = await response.json();
  assert.equal(response.status, 200, JSON.stringify(json));
  assert.ok(!json.error, JSON.stringify(json));
  return json.result;
};
const tool = async (name, args) => {
  const result = await rpc('tools/call', { name, arguments: args });
  assert.ok(!result.isError, JSON.stringify(result));
  return result.structuredContent || JSON.parse(result.content[0].text);
};
try {
  const initialized = await rpc('initialize', { protocolVersion: '2025-03-26', capabilities: {}, clientInfo: { name: 'starlight-acceptance', version: '1' } });
  const listed = await rpc('tools/list', {});
  const submitted = await tool('submit_task', task);
  const id = submitted.run.id;
  assert.equal((await tool('submit_task', task)).run.id, id);
  // Restart the real runtime before dispatch: the queued task and budget must survive.
  await mf.dispose(); mf = start();
  const transport = {
    async request(path, body) {
      const response = await mf.dispatchFetch(`http://localhost${path}`, { method: body === undefined ? 'GET' : 'POST',
        headers: { authorization: `Bearer ${workerToken}`, 'content-type': 'application/json' }, ...(body === undefined ? {} : { body: JSON.stringify(body) }) });
      const data = await response.json(); if (!response.ok) throw new Error(JSON.stringify(data)); return data;
    },
    claim(worker_id) { return this.request('/internal/claim', { worker_id }); },
    state(run_id) { return this.request(`/internal/runs/${run_id}`); },
    complete(claim, result) { return this.request('/internal/complete', { run_id: claim.id, lease_token: claim.lease_token, result }); },
  };
  const execution = await runOnce({ client: transport, journal, presets: { presets: [preset] }, workerId: 'local-estate-fixture',
    execute: (p, claim, cancelled) => executeKernel(p, claim, { kernelRoot, kernelHome: home, kernelPolicy: policyPath,
      artifactRoot: join(root, 'artifacts'), allowFixtures: true }, cancelled) });
  const run = await tool('get_run', { run_id: id });
  const artifacts = await tool('get_artifacts', { run_id: id });
  const evaluation = await tool('get_eval_report', { run_id: id });
  const report = { schema: 'starlight.execution-demo.v1', task: 'actual estate lab portability repair', source_revision: base,
    kernel_revision: 'c69e582f61b25cbb92791aa8acedef0dfcf29b21', protocol: initialized.protocolVersion,
    mcp_tools: listed.tools.map(t => t.name), execution, run, artifacts, evaluation,
    runtime_restart_before_execution: true, duplicate_submission_same_run: true,
    verification_kind: 'deterministic-estate-fixture', independent_model_review: false, model_calls: 0,
    measured_model_cost_microusd: 0, infrastructure_cost_microusd: null, artifact_directory: join(root, 'artifacts', id) };
  writeFileSync(join(root, 'report.json'), JSON.stringify(report, null, 2));
  if ((run.run ?? run).status !== 'succeeded') throw new Error(`demo did not succeed; evidence at ${root}`);
  const publication = await preparePublication({ kernelRoot, kernelHome: home, taskId: id, policy: policyPath,
    repository: preset.repository, baseBranch: 'agent/claude/research-lab' });
  writeFileSync(join(root, 'publication.json'), JSON.stringify(publication, null, 2));
  console.log(JSON.stringify({ status: 'PASS', report: join(root, 'report.json'), run_id: id,
    verification_kind: report.verification_kind, artifacts: artifacts.artifacts?.length, model_calls: 0 }));
} finally { journal.close(); await mf.dispose(); }
