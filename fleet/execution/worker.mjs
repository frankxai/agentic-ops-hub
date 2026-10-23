#!/usr/bin/env node
// A pull worker for operator-installed kernel contracts. No commands arrive over HTTP.
import { spawn } from 'node:child_process';
import { createHash, randomUUID } from 'node:crypto';
import { hostname } from 'node:os';
import { DatabaseSync } from 'node:sqlite';
import { chmodSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const hash = (value) => createHash('sha256').update(value).digest('hex');
const sha = (value) => typeof value === 'string' && /^[a-f0-9]{40}$/.test(value);
const positive = (value) => Number.isSafeInteger(value) && value > 0;
export class WorkerError extends Error {}

export function loadPresets(path) {
  const config = JSON.parse(readFileSync(path, 'utf8'));
  if (!config || config.version !== 1 || !Array.isArray(config.presets)) throw new WorkerError('invalid preset registry');
  const ids = new Set();
  for (const p of config.presets) {
    if (!p || typeof p.task_kind !== 'string' || ids.has(p.task_kind) ||
        !/^[\w.-]{1,80}$/.test(p.task_kind) || !/^[\w.-]+\/[\w.-]+$/.test(p.repository) ||
        !sha(p.revision) || typeof p.contract_id !== 'string' || !/^[a-f0-9]{64}$/.test(p.contract_id) ||
        !positive(p.max_seconds) || p.max_seconds > 3600 || !positive(p.max_allowance_microusd) ||
        !['trusted-local-fixture', 'container'].includes(p.isolation)) throw new WorkerError('invalid preset');
    ids.add(p.task_kind);
  }
  return config;
}

export function selectPreset(config, run) {
  const p = config.presets.find((x) => x.task_kind === run.task_kind);
  if (!p || p.repository !== run.repository || p.revision !== run.revision ||
      !positive(run.deadline_seconds) || run.deadline_seconds > p.max_seconds ||
      !positive(run.allowance_microusd) || run.allowance_microusd > p.max_allowance_microusd ||
      (run.prompt !== undefined && run.prompt !== '')) throw new WorkerError('task does not match an installed contract');
  return p;
}

export class Journal {
  constructor(path) {
    mkdirSync(dirname(resolve(path)), { recursive: true });
    this.db = new DatabaseSync(path);
    chmodSync(path, 0o600);
    this.db.exec('PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; CREATE TABLE IF NOT EXISTS attempts (run_id TEXT PRIMARY KEY, claim TEXT NOT NULL, state TEXT NOT NULL, result TEXT)');
    this.db.exec('CREATE TABLE IF NOT EXISTS owner (id INTEGER PRIMARY KEY CHECK(id=1), token TEXT NOT NULL, pid INTEGER NOT NULL, host TEXT NOT NULL)');
    this.owner = randomUUID();
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const prior = this.db.prepare('SELECT * FROM owner WHERE id=1').get();
      if (prior) {
        let alive = true;
        if (prior.host === hostname()) {
          try { process.kill(prior.pid, 0); } catch (error) { if (error.code === 'ESRCH') alive = false; }
        }
        if (alive) throw new WorkerError('journal has a live or foreign owner; recovery refused');
      }
      this.db.prepare('INSERT OR REPLACE INTO owner VALUES (1, ?, ?, ?)').run(this.owner, process.pid, hostname());
      this.db.exec('COMMIT');
    } catch (error) { this.db.exec('ROLLBACK'); this.db.close(); throw error; }
  }
  start(claim) {
    this.db.prepare('INSERT INTO attempts VALUES (?, ?, ?, NULL)').run(claim.id, JSON.stringify(claim), 'started');
  }
  finish(id, result) {
    this.db.prepare("UPDATE attempts SET state='pending', result=? WHERE run_id=? AND state='started'").run(JSON.stringify(result), id);
  }
  acknowledged(id) { this.db.prepare("UPDATE attempts SET state='acknowledged' WHERE run_id=?").run(id); }
  pending() { return this.db.prepare("SELECT * FROM attempts WHERE state!='acknowledged'").all(); }
  close() {
    this.db.prepare('DELETE FROM owner WHERE id=1 AND token=?').run(this.owner);
    this.db.close();
  }
}

export class CoordinatorClient {
  constructor(endpoint, token) {
    const url = new URL(endpoint);
    if (url.username || url.password || url.search || url.hash ||
        (url.protocol !== 'https:' && !(url.protocol === 'http:' && ['127.0.0.1', '[::1]', 'localhost'].includes(url.hostname)))) {
      throw new WorkerError('coordinator must use HTTPS or loopback HTTP');
    }
    if (typeof token !== 'string' || token.length < 24) throw new WorkerError('worker token missing or too short');
    this.endpoint = endpoint.replace(/\/$/, ''); this.token = token;
  }
  async request(path, body) {
    const response = await fetch(this.endpoint + path, {
      method: body === undefined ? 'GET' : 'POST', redirect: 'error',
      headers: { authorization: `Bearer ${this.token}`, 'content-type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(15000),
    });
    const text = await response.text();
    if (text.length > 131072) throw new WorkerError('coordinator response too large');
    if (!response.ok) throw new WorkerError(`coordinator refused request (${response.status})`);
    return JSON.parse(text);
  }
  async claim(worker_id) { return this.request('/internal/claim', { worker_id }); }
  async state(id) { return this.request(`/internal/runs/${encodeURIComponent(id)}`); }
  async complete(claim, result) {
    return this.request('/internal/complete', { run_id: claim.id, lease_token: claim.lease_token, result });
  }
}

function childEnvironment(allowedNames) {
  // Coordinator, publication and cloud credentials never reach the maker.
  const blocked = /EXECUTION_|GITHUB|GH_TOKEN|CLOUDFLARE|AWS_|GOOGLE|AZURE|CLIENT_TOKEN|WORKER_TOKEN/i;
  const result = { PATH: process.env.PATH || '', LANG: 'C.UTF-8' };
  for (const name of allowedNames || []) {
    if (blocked.test(name) || !/^[A-Z][A-Z0-9_]*$/.test(name)) throw new WorkerError('forbidden child credential');
    if (process.env[name]) result[name] = process.env[name];
  }
  return result;
}

export async function executeKernel(preset, claim, options, isCancelled) {
  // Host execution is deliberately limited to the checked-in deterministic fixture.
  if (preset.isolation !== 'trusted-local-fixture') throw new WorkerError('container maker execution is not activated');
  if (!options.allowFixtures) throw new WorkerError('fixture execution requires an explicit worker flag');
  const kernelRoot = realpathSync(options.kernelRoot);
  const outputRoot = resolve(options.artifactRoot, claim.id);
  mkdirSync(outputRoot, { recursive: true, mode: 0o700 });
  const input = { version: 1, kernelRoot, home: resolve(options.kernelHome), policy: realpathSync(options.kernelPolicy), contractId: preset.contract_id,
    taskId: claim.id, repository: preset.repository, revision: preset.revision, outputRoot };
  const inputPath = join(outputRoot, 'dispatch.json');
  writeFileSync(inputPath, JSON.stringify(input), { mode: 0o600 });
  const env = childEnvironment([]);
  let stdout = '', overflow = false, cancelled = false;
  const child = spawn(process.execPath, [join(HERE, 'kernel-adapter.mjs'), inputPath], {
    env, stdio: ['ignore', 'pipe', 'pipe'], detached: process.platform !== 'win32', shell: false,
  });
  const stop = () => {
    try { if (process.platform !== 'win32') process.kill(-child.pid, 'SIGKILL'); else child.kill('SIGKILL'); } catch {}
  };
  const timeout = setTimeout(stop, Math.min(preset.max_seconds, claim.deadline_seconds) * 1000);
  let checking = false;
  const poll = setInterval(async () => {
    if (checking) return;
    checking = true;
    try { if (await isCancelled()) { cancelled = true; stop(); } } catch { stop(); } finally { checking = false; }
  }, options.pollMs || 1000);
  child.stdout.on('data', (data) => { stdout += data; if (stdout.length > 65536) { overflow = true; stop(); } });
  // Do not copy model stderr into public artifacts: it may contain credentials or prompts.
  child.stderr.on('data', () => {});
  try {
    const code = await new Promise((res, rej) => { child.on('error', rej); child.on('close', res); });
    if (cancelled) throw new WorkerError('execution cancelled');
    if (code !== 0 || overflow) throw new WorkerError('kernel adapter failed or exceeded output limit');
    const result = JSON.parse(stdout);
    if (!result || !['succeeded', 'failed'].includes(result.status)) throw new WorkerError('invalid adapter result');
    return result;
  } finally { clearTimeout(timeout); clearInterval(poll); stop(); }
}

export async function runOnce({ client, journal, presets, workerId, execute }) {
  if (journal.running) throw new WorkerError('journal already executing');
  journal.running = true;
  try { return await runLocked({ client, journal, presets, workerId, execute }); }
  finally { journal.running = false; }
}

async function runLocked({ client, journal, presets, workerId, execute }) {
  // A claim is never replayed after a process may have started. Only its durable result is replayed.
  for (const entry of journal.pending()) {
    const claim = JSON.parse(entry.claim);
    const result = entry.result ? JSON.parse(entry.result) : {
      status: 'failed', actual_cost_microusd: null, artifacts: [], verification: null, receipt_sha256: null,
    };
    await client.complete(claim, result);
    journal.acknowledged(claim.id);
  }
  const claimed = await client.claim(workerId);
  const claim = claimed?.run ?? claimed;
  if (!claim || !claim.id) return { claimed: false };
  journal.start(claim);
  let result;
  try {
    const preset = selectPreset(presets, claim);
    result = await execute(preset, claim, async () => {
      const state = await client.state(claim.id);
      return !['running'].includes((state?.run ?? state)?.status);
    });
  } catch {
    // Without a measured provider report, absence of output never means zero spend.
    result = { status: 'failed', actual_cost_microusd: null, artifacts: [], verification: null, receipt_sha256: null };
  }
  journal.finish(claim.id, result);
  await client.complete(claim, result);
  journal.acknowledged(claim.id);
  return { claimed: true, run_id: claim.id, status: result.status, usage_known: result.actual_cost_microusd !== null };
}

async function main() {
  const configPath = process.argv[2];
  if (!configPath) throw new WorkerError('usage: node worker.mjs <operator-config.json>');
  const config = JSON.parse(readFileSync(configPath, 'utf8'));
  const presets = loadPresets(config.presets);
  const journal = new Journal(config.journal);
  try {
    const client = new CoordinatorClient(config.endpoint, process.env.EXECUTION_WORKER_TOKEN);
    const result = await runOnce({ client, journal, presets, workerId: config.worker_id,
      execute: (preset, claim, cancelled) => executeKernel(preset, claim, config, cancelled) });
    console.log(JSON.stringify(result));
  } finally { journal.close(); }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(() => { console.error('execution worker refused or failed; inspect private journal and server state'); process.exitCode = 1; });
}
