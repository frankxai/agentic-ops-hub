import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { Journal, CoordinatorClient, loadPresets, selectPreset, runOnce } from '../worker.mjs';

const revision = 'a'.repeat(40), contract_id = 'b'.repeat(64);
const preset = { task_kind: 'lab-portability', repository: 'frankxai/agentic-ops-hub', revision, contract_id,
  max_seconds: 60, max_allowance_microusd: 1000, isolation: 'trusted-local-fixture' };
const claim = { id: 'run-abc', lease_token: 'private-lease', task_kind: preset.task_kind, repository: preset.repository,
  revision, allowance_microusd: 1, deadline_seconds: 30 };
const result = { status: 'succeeded', actual_cost_microusd: 0, artifacts: [], verification: null, receipt_sha256: null };
function setup(t) {
  const root = mkdtempSync(join(tmpdir(), 'execution-worker-test-'));
  const path = join(root, 'journal.sqlite');
  const journal = new Journal(path);
  t.after(() => { try { journal.close(); } catch {} rmSync(root, { recursive: true, force: true }); });
  return { root, path, journal };
}
test('operator registry rejects duplicate presets and live command injection', (t) => {
  const { root } = setup(t), path = join(root, 'registry.json');
  writeFileSync(path, JSON.stringify({ version: 1, presets: [preset, preset] }));
  assert.throws(() => loadPresets(path));
  writeFileSync(path, JSON.stringify({ version: 1, presets: [preset] }));
  assert.equal(loadPresets(path).presets.length, 1);
  assert.throws(() => selectPreset({ presets: [preset] }, { ...claim, prompt: 'execute arbitrary commands' }));
  assert.throws(() => selectPreset({ presets: [preset] }, { ...claim, revision: 'c'.repeat(40) }));
  assert.throws(() => selectPreset({ presets: [preset] }, { ...claim, allowance_microusd: 1001 }));
});
test('coordinator credentials cannot be sent to plaintext non-loopback or URL credentials', () => {
  const token = 'synthetic-worker-token-123456789';
  for (const url of ['http://example.com', 'https://u:p@example.com', 'https://example.com/?token=x']) assert.throws(() => new CoordinatorClient(url, token));
  assert.doesNotThrow(() => new CoordinatorClient('http://127.0.0.1:8787', token));
});
test('exclusive journal owner prevents a second invocation treating a live process as a crash', (t) => {
  const { path } = setup(t);
  assert.throws(() => new Journal(path), /owner/);
});
test('one journal instance cannot execute two run loops concurrently', async (t) => {
  const { journal } = setup(t);
  let release;
  const gate = new Promise(r => { release = r; });
  const options = { client: { claim: async () => { await gate; return null; } }, journal,
    presets: { presets: [preset] }, workerId: 'fixture', execute: async () => result };
  const first = runOnce(options);
  await assert.rejects(runOnce(options), /already executing/);
  release(); await first;
});
test('successful result is durable before completion and acknowledgement', async (t) => {
  const { journal } = setup(t); let executed = 0, completed = 0;
  const client = { claim: async () => ({ run: claim }), complete: async (c, r) => {
    completed++; assert.equal(journal.pending()[0].state, 'pending'); assert.deepEqual(r, result);
  } };
  const summary = await runOnce({ client, journal, presets: { presets: [preset] }, workerId: 'fixture', execute: async () => { executed++; return result; } });
  assert.equal(executed, 1); assert.equal(completed, 1); assert.equal(summary.usage_known, true); assert.equal(journal.pending().length, 0);
});
test('completion transport retry replays outbox without re-executing maker', async (t) => {
  const { journal } = setup(t); let executed = 0;
  const client = { claim: async () => claim, complete: async () => { throw new Error('lost response'); } };
  await assert.rejects(runOnce({ client, journal, presets: { presets: [preset] }, workerId: 'fixture', execute: async () => { executed++; return result; } }));
  client.complete = async (_, r) => assert.deepEqual(r, result);
  client.claim = async () => null;
  await runOnce({ client, journal, presets: { presets: [preset] }, workerId: 'fixture', execute: async () => { executed++; } });
  assert.equal(executed, 1); assert.equal(journal.pending().length, 0);
});
test('restart with started attempt reports unknown usage and never reruns', async (t) => {
  const { journal } = setup(t); journal.start(claim);
  let recorded;
  const client = { claim: async () => null, complete: async (_, r) => { recorded = r; } };
  await runOnce({ client, journal, presets: { presets: [preset] }, workerId: 'fixture', execute: async () => assert.fail('must not rerun') });
  assert.equal(recorded.actual_cost_microusd, null); assert.equal(recorded.verification, null);
});
test('executor crash does not forge zero usage or proof', async (t) => {
  const { journal } = setup(t); let recorded;
  await runOnce({ client: { claim: async () => claim, complete: async (_, r) => { recorded = r; } }, journal,
    presets: { presets: [preset] }, workerId: 'fixture', execute: async () => { throw new Error('lost adapter'); } });
  assert.equal(recorded.actual_cost_microusd, null); assert.equal(recorded.receipt_sha256, null);
});
