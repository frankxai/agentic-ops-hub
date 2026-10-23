#!/usr/bin/env node
// Explicit development smoke. Credentials stay in a private operator file, never child env.
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { Journal, CoordinatorClient, runOnce, executeKernel } from './worker.mjs';

const arg = (name) => { const index = process.argv.indexOf(`--${name}`); return index < 0 ? undefined : process.argv[index + 1]; };
for (const name of ['credentials', 'fixture-root', 'kernel', 'endpoint']) if (!arg(name)) throw new Error(`missing --${name}`);
const root = resolve(arg('fixture-root')), kernelRoot = resolve(arg('kernel'));
const auth = JSON.parse(readFileSync(arg('credentials'), 'utf8'));
const endpoint = arg('endpoint').replace(/\/$/, '');
// Reuse an operator-created immutable fixture contract from the local acceptance demo.
const prior = JSON.parse(readFileSync(join(root, 'report.json'), 'utf8'));
const oldRun = prior.run.run;
const receipt = JSON.parse(readFileSync(join(prior.artifact_directory, 'kernel-receipt.json'), 'utf8'));
const preset = { task_kind: oldRun.task_kind, repository: oldRun.repository, revision: oldRun.revision,
  contract_id: receipt.contractId, max_seconds: 300, max_allowance_microusd: 1, isolation: 'trusted-local-fixture' };
const require = createRequire(join(import.meta.dirname, 'cloudflare/package.json'));
const [{ Client }, { StreamableHTTPClientTransport }] = await Promise.all([
  import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/index.js'))),
  import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/streamableHttp.js'))),
]);
const worker = new CoordinatorClient(endpoint, auth.worker);
const transport = new StreamableHTTPClientTransport(new URL(endpoint + '/mcp'), {
  requestInit: { headers: { authorization: `Bearer ${auth.client}` } },
});
const client = new Client({ name: 'starlight-cloud-acceptance', version: '0.1.0' });
const journal = new Journal(join(root, 'live-worker.sqlite'));
const unwrap = (r) => { if (r.isError) throw new Error('MCP tool refused'); return r.structuredContent || JSON.parse(r.content[0].text); };
const tool = async (name, args) => unwrap(await client.callTool({ name, arguments: args }));
try {
  const anonymous = await fetch(endpoint + '/mcp', { method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list' }), signal: AbortSignal.timeout(15000) });
  assert.equal(anonymous.status, 401);
  await client.connect(transport);
  const tools = await client.listTools(); assert.equal(tools.tools.length, 5);
  const task = { idempotency_key: `cloud-estate-${Date.now()}`, repository: preset.repository, revision: preset.revision,
    task_kind: preset.task_kind, allowance_microusd: 1, deadline_seconds: 300 };
  const submitted = await tool('submit_task', task);
  assert.equal((await tool('submit_task', task)).run.id, submitted.run.id);
  const execution = await runOnce({ client: worker, journal, presets: { presets: [preset] }, workerId: 'development-fixture-worker',
    execute: (p, claim, cancelled) => executeKernel(p, claim, { kernelRoot, kernelHome: join(root, 'kernel-home'),
      kernelPolicy: join(root, 'policy.json'), artifactRoot: join(root, 'live-artifacts'), allowFixtures: true }, cancelled) });
  const run = await tool('get_run', { run_id: submitted.run.id });
  const evaluation = await tool('get_eval_report', { run_id: submitted.run.id });
  const artifacts = await tool('get_artifacts', { run_id: submitted.run.id });
  assert.equal(run.run.status, 'succeeded', JSON.stringify(run));
  assert.equal(artifacts.accepted, true);
  const report = { schema: 'starlight.cloud-execution-smoke.v1', endpoint, anonymous_mcp_status: anonymous.status,
    mcp_tools: tools.tools.map(t => t.name), duplicate_submission_same_run: true, execution, run, evaluation, artifacts,
    artifact_directory: join(root, 'live-artifacts', submitted.run.id), verification_kind: 'deterministic-estate-fixture',
    independent_model_review: false, model_calls: 0, measured_model_cost_microusd: 0, infrastructure_cost_microusd: null };
  writeFileSync(join(root, 'cloud-live-report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ status: 'PASS', endpoint, run_id: submitted.run.id, artifacts: artifacts.artifacts.length,
    report: join(root, 'cloud-live-report.json'), model_calls: 0 }));
} finally { journal.close(); await client.close(); }
