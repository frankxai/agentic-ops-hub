import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Miniflare, convertV4MiniflareOptions } from 'miniflare';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const CLIENT = 'test-client-token-'.padEnd(48, 'c');
const WORKER = 'test-worker-token-'.padEnd(48, 'w');
const BINDINGS = {TENANT_ID: 'test-tenant', EXECUTION_CLIENT_TOKEN: CLIENT, EXECUTION_WORKER_TOKEN: WORKER, BUDGET_MICROUSD: '100', ALLOWED_REPOSITORIES_JSON: '["frankxai/agentic-ops-hub"]', ALLOWED_TASK_KINDS_JSON: '["kernel-contract"]'};
const TASK = {idempotency_key: 'task1', repository: 'frankxai/agentic-ops-hub', revision: 'a'.repeat(40), task_kind: 'kernel-contract', prompt: 'Fix the fixture', allowance_microusd: 60, deadline_seconds: 300};
const SHA = 'b'.repeat(64);
const RESULT = {status: 'succeeded', actual_cost_microusd: 20, artifacts: [{name: 'patch.diff', sha256: SHA, ref: 'artifacts/patch.diff'}], verification: {passed: true, actor: 'checker', maker: 'maker', evidence_sha256: SHA}, receipt_sha256: SHA};
function start(extra = {}, persist) {
  const options = convertV4MiniflareOptions({name: 'execution-test', modules: true, scriptPath: fileURLToPath(new URL('../src/worker.mjs', import.meta.url)), compatibilityDate: '2026-10-23', compatibilityFlags: ['nodejs_compat'], durableObjects: {EXECUTION: {className: 'ExecutionCoordinator', useSQLite: true}}, durableObjectsPersist: persist, bindings: {...BINDINGS, ...extra}, log: undefined, telemetry: {enabled: false}});
  if (persist) options.resourcePersistencePath = persist;
  return new Miniflare(options);
}
async function fixture(t, extra) { const mf = start(extra); t.after(() => mf.dispose()); return mf; }
async function request(mf, path, payload, token = CLIENT, method = payload === undefined ? 'GET' : 'POST', headers = {}) {
  const r = await mf.dispatchFetch(`https://coordinator.test${path}`, {method, headers: {authorization: `Bearer ${token}`, 'content-type': 'application/json', ...headers}, ...(payload === undefined ? {} : {body: JSON.stringify(payload)})});
  const text = await r.text(); return {status: r.status, data: text ? JSON.parse(text) : null};
}
async function submit(mf, fields = {}) { const r = await request(mf, '/tasks', {...TASK, ...fields}); assert.equal(r.status, 200, JSON.stringify(r)); return r.data.run; }
async function claim(mf) { const r = await request(mf, '/internal/claim', {worker_id: 'worker1'}, WORKER); assert.equal(r.status, 200); return r.data.run; }
async function complete(mf, run, result = RESULT) { return request(mf, '/internal/complete', {run_id: run.id, lease_token: run.lease_token, result}, WORKER); }

test('auth separates client and worker surfaces and health leaks no state', async t => {
  const mf = await fixture(t);
  assert.equal((await request(mf, '/tasks', TASK, 'wrong')).status, 401);
  assert.equal((await request(mf, '/internal/claim', {worker_id: 'worker1'}, CLIENT)).status, 401);
  assert.equal((await request(mf, '/tasks', TASK, WORKER)).status, 401);
  assert.deepEqual((await request(mf, '/health', undefined, 'wrong')).data, {service: 'starlight-execution', status: 'available'});
});
test('missing or identical credentials fail closed', async t => {
  const mf = await fixture(t, {EXECUTION_WORKER_TOKEN: CLIENT});
  assert.equal((await request(mf, '/tasks', TASK)).status, 503);
});
test('browser origins are rejected by default', async t => {
  const mf = await fixture(t);
  assert.equal((await request(mf, '/tasks', TASK, CLIENT, 'POST', {origin: 'https://evil.test'})).status, 403);
});
test('task schema rejects expanded authority, hostile repositories and credentials', async t => {
  const mf = await fixture(t);
  for (const fields of [{idempotency_key: null}, {idempotency_key: 123}, {tenant_id: 'other'}, {command: 'curl evil'}, {repository: 'https://evil.test/repo'}, {revision: 'main'}, {task_kind: 'shell'}, {allowance_microusd: 0}, {allowance_microusd: 1.1}, {deadline_seconds: 0}, {prompt: 'sk-proj-' + 'x'.repeat(40)}]) {
    assert.equal((await request(mf, '/tasks', {...TASK, ...fields})).status, 400, JSON.stringify(fields));
  }
});
test('actual UTF-8 body size is bounded regardless of header', async t => {
  const mf = await fixture(t);
  const r = await request(mf, '/tasks', {...TASK, prompt: '€'.repeat(24000)});
  assert.equal(r.status, 413);
});
test('idempotent replay returns same run; changed request conflicts', async t => {
  const mf = await fixture(t); const a = await submit(mf); const b = await submit(mf);
  assert.equal(a.id, b.id);
  assert.equal((await request(mf, '/tasks', {...TASK, prompt: 'different'})).status, 409);
  assert.equal((await request(mf, `/runs/${a.id}`)).data.run.lease_token, undefined);
});
test('concurrent admission cannot share budget headroom', async t => {
  const mf = await fixture(t);
  const results = await Promise.all(['one', 'two', 'three'].map(idempotency_key => request(mf, '/tasks', {...TASK, idempotency_key})));
  assert.deepEqual(results.map(r => r.status).sort(), [200, 409, 409]);
});
test('duplicate concurrent claims do not execute one task twice', async t => {
  const mf = await fixture(t); await submit(mf);
  const runs = await Promise.all([claim(mf), claim(mf)]);
  assert.equal(runs.filter(Boolean).length, 1);
});
test('queued cancellation releases allowance for the next task', async t => {
  const mf = await fixture(t); const run = await submit(mf);
  const cancelled = await request(mf, `/runs/${run.id}/cancel`, {}, CLIENT);
  assert.equal(cancelled.data.run.status, 'cancelled');
  assert.equal(cancelled.data.run.held_microusd, 0);
  await submit(mf, {idempotency_key: 'next'});
});
test('running cancellation retains hold and worker can poll state', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  await request(mf, `/runs/${run.id}/cancel`, {});
  const state = await request(mf, `/internal/runs/${run.id}`, undefined, WORKER);
  assert.equal(state.data.run.status, 'cancel_requested'); assert.equal(state.data.run.held_microusd, 60); assert.equal(state.data.run.lease_token, undefined);
  const done = await complete(mf, run);
  assert.equal(done.data.run.status, 'cancelled');
});
test('successful completion settles usage; replay is idempotent and changed usage conflicts', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  const a = await complete(mf, run); assert.equal(a.status, 200); assert.equal(a.data.run.status, 'succeeded'); assert.equal(a.data.run.held_microusd, 0);
  const b = await complete(mf, run); assert.equal(b.data.replayed, true);
  assert.equal((await complete(mf, run, {...RESULT, actual_cost_microusd: 30})).status, 409);
  const report = await request(mf, `/runs/${run.id}/eval`); assert.equal(report.data.actual_cost_microusd, 20); assert.equal(report.data.provenance, 'worker-self-asserted');
  const artifact = await request(mf, `/runs/${run.id}/artifacts`); assert.deepEqual(artifact.data.artifacts, RESULT.artifacts);
});
test('stale lease cannot settle another worker task', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  assert.equal((await complete(mf, {...run, lease_token: 'wrong'})).status, 409);
});
test('unknown usage remains held then reconciles exactly once', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  const a = await complete(mf, run, {...RESULT, actual_cost_microusd: null});
  assert.equal(a.data.run.status, 'needs_reconciliation'); assert.equal(a.data.run.held_microusd, 60); assert.equal(a.data.run.actual_cost_microusd, null);
  const payload = {run_id: run.id, lease_token: run.lease_token, actual_cost_microusd: 25};
  const b = await request(mf, '/internal/reconcile', payload, WORKER); assert.equal(b.data.run.status, 'succeeded'); assert.equal(b.data.run.held_microusd, 0);
  assert.equal((await request(mf, '/internal/reconcile', payload, WORKER)).data.replayed, true);
  assert.equal((await request(mf, '/internal/reconcile', {...payload, actual_cost_microusd: 26}, WORKER)).status, 409);
});
test('failed unknown run stores absence of proof without inventing it', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  const done = await complete(mf, run, {status: 'failed', actual_cost_microusd: null, artifacts: [], verification: null, receipt_sha256: null});
  assert.equal(done.status, 200); assert.equal(done.data.run.status, 'needs_reconciliation'); assert.equal(done.data.run.verification, null);
});
test('failed checks, same checker, unsafe refs and missing receipt cannot claim success', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  for (const result of [{...RESULT, verification: {...RESULT.verification, passed: false}}, {...RESULT, verification: {...RESULT.verification, actor: 'MAKER'}}, {...RESULT, receipt_sha256: null}, {...RESULT, artifacts: [{...RESULT.artifacts[0], ref: '../secret'}]}]) assert.equal((await complete(mf, run, result)).status, 400);
});
test('overrun is recorded and prevents further admission', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  const done = await complete(mf, run, {...RESULT, actual_cost_microusd: 120});
  assert.equal(done.data.run.over_allowance, true); assert.equal(done.data.run.over_budget, true);
  assert.equal((await request(mf, '/tasks', {...TASK, idempotency_key: 'next', allowance_microusd: 1})).status, 409);
});
test('MCP initialize, tools, notification, submission and query use real HTTP transport', async t => {
  const mf = await fixture(t);
  const init = await request(mf, '/mcp', {jsonrpc: '2.0', id: 1, method: 'initialize', params: {protocolVersion: '2025-03-26', capabilities: {}, clientInfo: {name: 'test', version: '1'}}});
  assert.equal(init.data.result.protocolVersion, '2025-03-26');
  assert.equal((await request(mf, '/mcp', {jsonrpc: '2.0', method: 'notifications/initialized'})).status, 202);
  const listing = await request(mf, '/mcp', {jsonrpc: '2.0', id: 2, method: 'tools/list'});
  assert.deepEqual(listing.data.result.tools.map(x => x.name), ['submit_task', 'get_run', 'cancel_run', 'get_artifacts', 'get_eval_report']);
  const submitted = await request(mf, '/mcp', {jsonrpc: '2.0', id: 3, method: 'tools/call', params: {name: 'submit_task', arguments: TASK}});
  const run = JSON.parse(submitted.data.result.content[0].text).run;
  const queried = await request(mf, '/mcp', {jsonrpc: '2.0', id: 4, method: 'tools/call', params: {name: 'get_run', arguments: {run_id: run.id}}});
  assert.equal(JSON.parse(queried.data.result.content[0].text).run.id, run.id);
});
test('durable storage survives workerd restart with a claimed run and no duplicate claim', async t => {
  const persist = await mkdtemp(join(tmpdir(), 'starlight-do-')); t.after(() => rm(persist, {recursive: true, force: true}));
  let mf = start({}, persist); await submit(mf); const run = await claim(mf); await mf.dispose();
  mf = start({}, persist); t.after(() => mf.dispose());
  const queried = await request(mf, `/runs/${run.id}`); assert.equal(queried.data.run.status, 'running');
  assert.equal(await claim(mf), null);
  assert.equal((await complete(mf, run)).data.run.status, 'succeeded');
});

test('cancelling an unknown completion prevents later reconciliation from restoring success', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  await complete(mf, run, {...RESULT, actual_cost_microusd: null});
  const cancelled = await request(mf, `/runs/${run.id}/cancel`, {});
  assert.equal(cancelled.data.run.held_microusd, 60);
  const settled = await request(mf, '/internal/reconcile', {run_id: run.id, lease_token: run.lease_token, actual_cost_microusd: 20}, WORKER);
  assert.equal(settled.data.run.status, 'cancelled'); assert.equal(settled.data.run.held_microusd, 0);
});

test('deadline expiry releases never-started work but retains an uncertain execution and never reclaims it', async t => {
  const mf = await fixture(t);
  const first = await submit(mf, {idempotency_key: 'started', allowance_microusd: 40, deadline_seconds: 10});
  const run = await claim(mf);
  const second = await submit(mf, {idempotency_key: 'queued', allowance_microusd: 40, deadline_seconds: 10});
  await new Promise(resolve => setTimeout(resolve, 10_100));
  const running = await request(mf, `/runs/${first.id}`);
  assert.equal(running.data.run.status, 'needs_reconciliation'); assert.equal(running.data.run.held_microusd, 40);
  const queued = await request(mf, `/runs/${second.id}`);
  assert.equal(queued.data.run.status, 'failed'); assert.equal(queued.data.run.held_microusd, 0);
  assert.equal(await claim(mf), null);
  const late = await complete(mf, run);
  assert.equal(late.data.run.status, 'cancelled'); assert.equal(late.data.run.actual_cost_microusd, 20);
});

test('MCP invalid tool parameters retain the JSON-RPC error envelope', async t => {
  const mf = await fixture(t);
  const response = await request(mf, '/mcp', {jsonrpc: '2.0', id: 'bad', method: 'tools/call', params: {name: 'get_run'}});
  assert.equal(response.data.jsonrpc, '2.0'); assert.equal(response.data.id, 'bad'); assert.equal(response.data.error.code, -32602);
});

test('unknown-usage artifacts remain explicitly unaccepted', async t => {
  const mf = await fixture(t); await submit(mf); const run = await claim(mf);
  await complete(mf, run, {...RESULT, actual_cost_microusd: null});
  const response = await request(mf, `/runs/${run.id}/artifacts`);
  assert.equal(response.data.accepted, false); assert.equal(response.data.status, 'needs_reconciliation');
});

test('worker and verifier identifiers must be actual strings', async t => {
  const mf = await fixture(t); await submit(mf);
  assert.equal((await request(mf, '/internal/claim', {worker_id: 123}, WORKER)).status, 400);
  const run = await claim(mf);
  assert.equal((await complete(mf, run, {...RESULT, verification: {...RESULT.verification, actor: 123}})).status, 400);
});

test('official MCP SDK client connects and calls the five-tool HTTP server', async t => {
  const [{Client}, {StreamableHTTPClientTransport}] = await Promise.all([
    import('@modelcontextprotocol/sdk/client/index.js'),
    import('@modelcontextprotocol/sdk/client/streamableHttp.js')
  ]);
  const mf = await fixture(t);
  const transport = new StreamableHTTPClientTransport(new URL('https://coordinator.test/mcp'), {
    requestInit: {headers: {authorization: `Bearer ${CLIENT}`}},
    fetch: async (url, init) => mf.dispatchFetch(url.toString(), init)
  });
  const client = new Client({name: 'starlight-acceptance', version: '0.1.0'});
  t.after(() => client.close());
  await client.connect(transport);
  const listing = await client.listTools();
  assert.equal(listing.tools.length, 5);
  const result = await client.callTool({name: 'submit_task', arguments: TASK});
  assert.equal(result.isError, false);
  const run = JSON.parse(result.content[0].text).run;
  const query = await client.callTool({name: 'get_run', arguments: {run_id: run.id}});
  assert.equal(JSON.parse(query.content[0].text).run.status, 'queued');
});
