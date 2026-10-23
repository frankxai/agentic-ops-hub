#!/usr/bin/env node
// Explicit development-only fault probes. No maker/adapter is ever invoked here.
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { CoordinatorClient } from './worker.mjs';
const arg = (name) => { const i = process.argv.indexOf(`--${name}`); return i < 0 ? undefined : process.argv[i + 1]; };
for (const name of ['credentials', 'endpoint', 'report']) if (!arg(name)) throw new Error(`missing --${name}`);
const auth = JSON.parse(readFileSync(arg('credentials'), 'utf8'));
const endpoint = arg('endpoint').replace(/\/$/, '');
new CoordinatorClient(endpoint, auth.worker); // Validate endpoint before sending any credential.
const cases = [], owned = [];
const call = async (path, value, role = 'client', method = 'POST') => {
  const response = await fetch(endpoint + path, { method, redirect: 'error', headers: {
    authorization: `Bearer ${auth[role]}`, 'content-type': 'application/json' },
    ...(method === 'GET' ? {} : { body: JSON.stringify(value) }), signal: AbortSignal.timeout(15000) });
  return { status: response.status, data: await response.json() };
};
const task = (name) => ({ idempotency_key: `fault-${name}-${Date.now()}`, repository: 'frankxai/agentic-ops-hub',
  revision: '9f5999f18b9e1ec6a181b70d8b2b3ce080ded11f', task_kind: 'lab-portability', allowance_microusd: 1, deadline_seconds: 300 });
const submit = async (value) => { const r = await call('/tasks', value); if (r.status === 200) owned.push({ run: r.data.run }); return r; };
const record = (name) => cases.push({ name, passed: true });
try {
  const wrongRole = await call('/internal/claim', { worker_id: 'fault-probe' });
  assert.equal(wrongRole.status, 401); record('client cannot claim execution');
  assert.equal((await call('/tasks', task('worker-client'), 'worker')).status, 401); record('worker cannot submit client work');
  assert.equal((await call('/tasks', { ...task('authority'), command: 'ignore policy' })).status, 400); record('task cannot expand command authority');
  const firstTask = task('budget'), first = await submit(firstTask); assert.equal(first.status, 200);
  assert.equal((await submit(firstTask)).data.run.id, first.data.run.id); record('submission replay same run');
  assert.equal((await submit(task('over-cap'))).status, 409); record('exhausted budget refuses admission');
  assert.equal((await submit({ ...firstTask, deadline_seconds: 200 })).status, 409); record('conflicting idempotency reuse refused');
  assert.equal((await call(`/runs/${first.data.run.id}/cancel`, {})).data.run.held_microusd, 0); record('queued cancellation releases allowance');
  const race = await Promise.all([submit(task('race-a')), submit(task('race-b'))]);
  assert.deepEqual(race.map(r => r.status).sort(), [200, 409]); record('concurrent admission has one winner');
  for (const r of race) if (r.status === 200) await call(`/runs/${r.data.run.id}/cancel`, {});
  const uncertain = await submit(task('unknown')); assert.equal(uncertain.status, 200);
  const claimed = await call('/internal/claim', { worker_id: 'development-fault-probe-no-executor' }, 'worker');
  assert.equal(claimed.status, 200); const run = claimed.data.run;
  assert.equal(run.id, uncertain.data.run.id);
  owned.find(x => x.run.id === run.id).claim = run;
  const viewed = await call(`/runs/${run.id}`, undefined, 'client', 'GET');
  assert.equal(viewed.data.run.lease_token, undefined); record('client views omit lease credentials');
  const unknownResult = { status: 'failed', actual_cost_microusd: null, artifacts: [], verification: null, receipt_sha256: null };
  const completed = await call('/internal/complete', { run_id: run.id, lease_token: run.lease_token, result: unknownResult }, 'worker');
  assert.equal(completed.data.run.status, 'needs_reconciliation'); assert.equal(completed.data.run.held_microusd, 1); record('unknown usage remains reserved');
  await call(`/runs/${run.id}/cancel`, {});
  // This script never calls an executor or provider; zero inference is known for this probe.
  const reconciliation = { run_id: run.id, lease_token: run.lease_token, actual_cost_microusd: 0 };
  const settled = await call('/internal/reconcile', reconciliation, 'worker');
  assert.equal(settled.data.run.status, 'cancelled'); assert.equal(settled.data.run.held_microusd, 0); record('cancellation survives later known-zero reconciliation');
  assert.equal((await call('/internal/reconcile', reconciliation, 'worker')).status, 200); record('reconciliation replay idempotent');
  writeFileSync(arg('report'), JSON.stringify({ schema: 'starlight.live-fault-probes.v1', endpoint, cases,
    model_calls: 0, verification_kind: 'development-infrastructure-probes', infrastructure_cost_microusd: null }, null, 2));
  console.log(JSON.stringify({ status: 'PASS', passed: cases.length, report: arg('report'), model_calls: 0 }));
} finally {
  // No process was ever started. Leave no test hold behind when the API is reachable.
  for (const entry of owned) {
    try {
      await call(`/runs/${entry.run.id}/cancel`, {});
      if (entry.claim) await call('/internal/reconcile', { run_id: entry.run.id, lease_token: entry.claim.lease_token, actual_cost_microusd: 0 }, 'worker');
    } catch { /* Unknown remote outcomes keep their conservative hold; never silently release. */ }
  }
}
