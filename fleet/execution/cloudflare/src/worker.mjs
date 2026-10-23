import { DurableObject } from 'cloudflare:workers';

const MAX_BODY = 65536;
const MAX_RUNS = 1000;
const MAX_MONEY = 1_000_000_000_000;
const PROTOCOL = '2025-03-26';
const SHA = /^[a-f0-9]{64}$/;
const IDENT = /^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$/;
const ident = value => typeof value === 'string' && IDENT.test(value);
const REPO = /^[a-zA-Z0-9][a-zA-Z0-9_.-]*\/[a-zA-Z0-9][a-zA-Z0-9_.-]*$/;

class Refusal extends Error {
  constructor(status, code) { super(code); this.status = status; this.code = code; }
}
const refuse = (status, code) => { throw new Refusal(status, code); };
const json = (value, status = 200) => new Response(JSON.stringify(value), {status, headers: {'content-type': 'application/json', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff'}});
const string = (v, min, max) => typeof v === 'string' && v.length >= min && v.length <= max;
const money = (v, positive = false) => Number.isSafeInteger(v) && v >= (positive ? 1 : 0) && v <= MAX_MONEY;
function shape(value, allowed, required = allowed) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) refuse(400, 'invalid_object');
  if (Object.keys(value).some(k => !allowed.includes(k)) || required.some(k => !Object.hasOwn(value, k))) refuse(400, 'invalid_fields');
}
function cleanText(v, max = 4000) {
  return string(v, 0, max) && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(v) && !/(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)/.test(v);
}
function parseList(raw, validator, allowEmpty = false) {
  let list;
  try { list = JSON.parse(raw); } catch { refuse(503, 'configuration_unavailable'); }
  if (!Array.isArray(list) || (!allowEmpty && list.length < 1) || list.length > 100 || !list.every(validator)) refuse(503, 'configuration_unavailable');
  return list;
}
function config(env) {
  if (!ident(env.TENANT_ID) || !string(env.EXECUTION_CLIENT_TOKEN, 32, 256) || !string(env.EXECUTION_WORKER_TOKEN, 32, 256) || env.EXECUTION_CLIENT_TOKEN === env.EXECUTION_WORKER_TOKEN) refuse(503, 'configuration_unavailable');
  if (!/^\d+$/.test(env.BUDGET_MICROUSD || '')) refuse(503, 'configuration_unavailable');
  const cap = Number(env.BUDGET_MICROUSD);
  if (!money(cap, true)) refuse(503, 'configuration_unavailable');
  return {tenant: env.TENANT_ID, cap, repos: parseList(env.ALLOWED_REPOSITORIES_JSON, v => string(v, 3, 160) && REPO.test(v)), kinds: parseList(env.ALLOWED_TASK_KINDS_JSON, v => ident(v))};
}
async function equalToken(actual, expected) {
  if (!string(actual, 1, 512)) return false;
  const encode = new TextEncoder();
  const [a, b] = await Promise.all([crypto.subtle.digest('SHA-256', encode.encode(actual)), crypto.subtle.digest('SHA-256', encode.encode(expected))]);
  const aa = new Uint8Array(a), bb = new Uint8Array(b); let diff = 0;
  for (let i = 0; i < aa.length; i++) diff |= aa[i] ^ bb[i];
  return diff === 0;
}
async function body(request) {
  if (!(request.headers.get('content-type') || '').toLowerCase().startsWith('application/json')) refuse(415, 'json_required');
  if (Number(request.headers.get('content-length')) > MAX_BODY) refuse(413, 'body_too_large');
  if (!request.body) refuse(400, 'json_required');
  const reader = request.body.getReader(); let size = 0; const chunks = [];
  while (true) { const {done, value} = await reader.read(); if (done) break; size += value.byteLength; if (size > MAX_BODY) { await reader.cancel(); refuse(413, 'body_too_large'); } chunks.push(value); }
  const bytes = new Uint8Array(size); let at = 0; for (const chunk of chunks) { bytes.set(chunk, at); at += chunk.length; }
  try { return JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes)); } catch { refuse(400, 'invalid_json'); }
}
function taskInput(input, cfg) {
  shape(input, ['idempotency_key', 'repository', 'revision', 'task_kind', 'prompt', 'allowance_microusd', 'deadline_seconds'], ['idempotency_key', 'repository', 'revision', 'task_kind', 'allowance_microusd', 'deadline_seconds']);
  if (!ident(input.idempotency_key) || !cfg.repos.includes(input.repository) || !/^[a-f0-9]{40}$/.test(input.revision || '') || !cfg.kinds.includes(input.task_kind) || !money(input.allowance_microusd, true) || !Number.isInteger(input.deadline_seconds) || input.deadline_seconds < 10 || input.deadline_seconds > 21600 || !cleanText(input.prompt ?? '')) refuse(400, 'invalid_task');
  return {idempotency_key: input.idempotency_key, repository: input.repository, revision: input.revision, task_kind: input.task_kind, prompt: input.prompt ?? '', allowance_microusd: input.allowance_microusd, deadline_seconds: input.deadline_seconds};
}
function artifact(value) {
  shape(value, ['name', 'sha256', 'ref']);
  if (!string(value.name, 1, 100) || !cleanText(value.name, 100) || !SHA.test(value.sha256 || '') || !string(value.ref, 1, 300) || !/^[A-Za-z0-9._/-]+$/.test(value.ref) || value.ref.startsWith('/') || value.ref.split('/').some(s => s === '..' || s === '.')) refuse(400, 'invalid_artifact');
}
function resultInput(result) {
  shape(result, ['status', 'actual_cost_microusd', 'artifacts', 'verification', 'receipt_sha256']);
  if (!['succeeded', 'failed'].includes(result.status) || !(result.actual_cost_microusd === null || money(result.actual_cost_microusd)) || !Array.isArray(result.artifacts) || result.artifacts.length > 20 || !(result.receipt_sha256 === null || SHA.test(result.receipt_sha256 || ''))) refuse(400, 'invalid_result');
  result.artifacts.forEach(artifact);
  const v = result.verification;
  if (result.status === 'failed' && v === null) return result;
  shape(v, ['passed', 'actor', 'maker', 'evidence_sha256']);
  if (typeof v.passed !== 'boolean' || !ident(v.actor) || !ident(v.maker) || !SHA.test(v.evidence_sha256 || '')) refuse(400, 'invalid_verification');
  if (result.status === 'succeeded' && (!v.passed || v.actor.toLowerCase() === v.maker.toLowerCase() || result.artifacts.length === 0 || !SHA.test(result.receipt_sha256 || ''))) refuse(400, 'verification_required');
  return result;
}
function canonical(value) { return Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(k => [k, canonical(value[k])])) : value; }
async function digest(value) { value = canonical(value); return [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(JSON.stringify(value))))].map(b => b.toString(16).padStart(2, '0')).join(''); }
function publicRun(run) { const {lease_token, completion_digest, ...view} = run; return view; }

export class ExecutionCoordinator extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.ctx = ctx; this.env = env;
    ctx.storage.sql.exec('CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, spent INTEGER NOT NULL, held INTEGER NOT NULL)');
    ctx.storage.sql.exec('INSERT OR IGNORE INTO ledger VALUES (1, 0, 0)');
    ctx.storage.sql.exec('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, idem TEXT UNIQUE NOT NULL, input_digest TEXT NOT NULL, data TEXT NOT NULL)');
  }
  ledger() { return this.ctx.storage.sql.exec('SELECT spent, held FROM ledger WHERE id=1').one(); }
  saveLedger(value) { this.ctx.storage.sql.exec('UPDATE ledger SET spent=?, held=? WHERE id=1', value.spent, value.held); }
  runs() { return this.ctx.storage.sql.exec('SELECT data FROM runs ORDER BY rowid').toArray().map(r => JSON.parse(r.data)); }
  get(id) { const row = this.ctx.storage.sql.exec('SELECT data FROM runs WHERE id=?', id).toArray()[0]; if (!row) refuse(404, 'run_not_found'); return JSON.parse(row.data); }
  save(run) { this.ctx.storage.sql.exec('UPDATE runs SET data=? WHERE id=?', JSON.stringify(run), run.id); }
  expire(now) {
    const ledger = this.ledger(); let changed = false;
    for (const run of this.runs()) {
      if (run.deadline_at > now || !['queued', 'running', 'cancel_requested'].includes(run.status)) continue;
      if (run.status === 'queued') { run.status = 'failed'; run.reason = 'deadline_before_execution'; ledger.held -= run.allowance_microusd; run.held_microusd = 0; }
      else { run.status = 'needs_reconciliation'; run.reason = 'execution_deadline'; }
      run.updated_at = now; this.save(run); changed = true;
    }
    if (changed) this.saveLedger(ledger);
  }
  async fetch(request) {
    try {
      const cfg = config(this.env); const input = await request.json();
      const {action, args} = input;
      const now = Date.now();
      let fingerprint;
      if (action === 'submit_task') fingerprint = await digest(taskInput(args, cfg));
      if (action === 'complete') { shape(args, ['run_id', 'lease_token', 'result']); resultInput(args.result); fingerprint = await digest(args.result); }
      const value = this.ctx.storage.transactionSync(() => {
        this.expire(now);
        if (action === 'submit_task') {
          const task = taskInput(args, cfg);
          const existing = this.ctx.storage.sql.exec('SELECT input_digest, data FROM runs WHERE idem=?', task.idempotency_key).toArray()[0];
          if (existing) { if (existing.input_digest !== fingerprint) refuse(409, 'idempotency_conflict'); return {run: publicRun(JSON.parse(existing.data)), replayed: true}; }
          if (this.ctx.storage.sql.exec('SELECT COUNT(*) AS n FROM runs').one().n >= MAX_RUNS) refuse(409, 'run_capacity');
          const ledger = this.ledger();
          if (ledger.spent + ledger.held + task.allowance_microusd > cfg.cap) refuse(409, 'budget_exhausted');
          const run = {...task, id: crypto.randomUUID(), tenant_id: cfg.tenant, status: 'queued', created_at: now, updated_at: now, deadline_at: now + task.deadline_seconds * 1000, held_microusd: task.allowance_microusd, actual_cost_microusd: null, artifacts: [], verification: null, provenance: 'worker-self-asserted'};
          this.ctx.storage.sql.exec('INSERT INTO runs VALUES (?, ?, ?, ?)', run.id, task.idempotency_key, fingerprint, JSON.stringify(run));
          ledger.held += task.allowance_microusd; this.saveLedger(ledger); return {run: publicRun(run), replayed: false};
        }
        if (action === 'claim') {
          shape(args, ['worker_id']); if (!ident(args.worker_id)) refuse(400, 'invalid_worker');
          const run = this.runs().find(r => r.status === 'queued');
          if (!run) return {run: null};
          run.status = 'running'; run.worker_id = args.worker_id; run.lease_token = crypto.randomUUID(); run.updated_at = now; this.save(run);
          return {run};
        }
        if (action === 'complete') {
          const run = this.get(args.run_id);
          if (typeof args.lease_token !== 'string' || run.lease_token !== args.lease_token) refuse(409, 'stale_lease');
          if (run.completion_digest) { if (run.completion_digest !== fingerprint) refuse(409, 'completion_conflict'); return {run: publicRun(run), replayed: true}; }
          if (!['running', 'cancel_requested', 'needs_reconciliation'].includes(run.status)) refuse(409, 'invalid_transition');
          const late = run.status !== 'running' || now >= run.deadline_at;
          const result = args.result;
          run.artifacts = result.artifacts; run.verification = result.verification; run.receipt_sha256 = result.receipt_sha256; run.actual_cost_microusd = result.actual_cost_microusd; run.completion_digest = fingerprint; run.completion_status = result.status; run.completion_was_late = late; run.updated_at = now;
          if (result.actual_cost_microusd === null) { run.status = 'needs_reconciliation'; run.reason = 'usage_unknown'; }
          else {
            const ledger = this.ledger();
            ledger.held -= run.held_microusd; ledger.spent += result.actual_cost_microusd;
            if (!Number.isSafeInteger(ledger.spent)) refuse(409, 'ledger_overflow');
            run.held_microusd = 0; run.over_allowance = result.actual_cost_microusd > run.allowance_microusd; run.over_budget = ledger.spent + ledger.held > cfg.cap;
            run.status = late ? 'cancelled' : result.status;
            if (late) run.reason = 'late_or_cancelled_completion';
            this.saveLedger(ledger);
          }
          this.save(run); return {run: publicRun(run), replayed: false};
        }
        if (action === 'reconcile') {
          shape(args, ['run_id', 'lease_token', 'actual_cost_microusd']);
          if (!money(args.actual_cost_microusd)) refuse(400, 'invalid_cost');
          const run = this.get(args.run_id);
          if (!run.lease_token || run.lease_token !== args.lease_token) refuse(409, 'stale_lease');
          if (run.actual_cost_microusd !== null) {
            if (run.actual_cost_microusd !== args.actual_cost_microusd) refuse(409, 'settlement_conflict');
            return {run: publicRun(run), replayed: true};
          }
          if (!run.completion_digest || run.status !== 'needs_reconciliation') refuse(409, 'invalid_transition');
          const ledger = this.ledger(); ledger.held -= run.held_microusd; ledger.spent += args.actual_cost_microusd;
          if (!Number.isSafeInteger(ledger.spent)) refuse(409, 'ledger_overflow');
          run.actual_cost_microusd = args.actual_cost_microusd; run.held_microusd = 0;
          run.over_allowance = args.actual_cost_microusd > run.allowance_microusd; run.over_budget = ledger.spent + ledger.held > cfg.cap;
          run.status = run.completion_was_late ? 'cancelled' : run.completion_status; run.updated_at = now;
          this.saveLedger(ledger); this.save(run); return {run: publicRun(run), replayed: false};
        }
        shape(args, ['run_id']); if (!string(args.run_id, 1, 80)) refuse(400, 'invalid_run_id');
        const run = this.get(args.run_id);
        if (action === 'get_run') return {run: publicRun(run)};
        if (action === 'get_artifacts') return {run_id: run.id, status: run.status, accepted: run.status === 'succeeded', artifacts: run.artifacts, provenance: run.provenance};
        if (action === 'get_eval_report') return {run_id: run.id, status: run.status, verification: run.verification, actual_cost_microusd: run.actual_cost_microusd, held_microusd: run.held_microusd, receipt_sha256: run.receipt_sha256 ?? null, provenance: run.provenance};
        if (action === 'cancel_run') {
          if (run.status === 'queued') { const ledger = this.ledger(); ledger.held -= run.held_microusd; run.held_microusd = 0; this.saveLedger(ledger); run.status = 'cancelled'; }
          else if (run.status === 'running') { run.status = 'cancel_requested'; run.completion_was_late = true; }
          else if (run.status === 'needs_reconciliation') { run.completion_was_late = true; run.reason = 'cancelled_pending_reconciliation'; }
          run.updated_at = now; this.save(run); return {run: publicRun(run)};
        }
        refuse(404, 'unknown_action');
      });
      return json(value);
    } catch (error) { return json({error: error instanceof Refusal ? error.code : 'coordinator_failure'}, error instanceof Refusal ? error.status : 500); }
  }
}

const RUN_ARGS = {type: 'object', properties: {run_id: {type: 'string', minLength: 1, maxLength: 80}}, required: ['run_id'], additionalProperties: false};
const TOOLS = [
  {name: 'submit_task', description: 'Reserve a bounded task in the operator-configured repository and task allowlist.', inputSchema: {type: 'object', properties: {idempotency_key: {type: 'string'}, repository: {type: 'string'}, revision: {type: 'string', pattern: '^[a-f0-9]{40}$'}, task_kind: {type: 'string'}, prompt: {type: 'string', maxLength: 4000}, allowance_microusd: {type: 'integer', minimum: 1}, deadline_seconds: {type: 'integer', minimum: 10, maximum: 21600}}, required: ['idempotency_key', 'repository', 'revision', 'task_kind', 'allowance_microusd', 'deadline_seconds'], additionalProperties: false}},
  ...['get_run', 'cancel_run', 'get_artifacts', 'get_eval_report'].map(name => ({name, description: `${name.replaceAll('_', ' ')} for a task in this tenant.`, inputSchema: RUN_ARGS}))
];
async function call(env, cfg, action, args) {
  const stub = env.EXECUTION.get(env.EXECUTION.idFromName(`execution-v1:${cfg.tenant}`));
  return stub.fetch(new Request('https://execution.internal', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({action, args})}));
}
export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      if (url.pathname === '/health' && request.method === 'GET') return json({service: 'starlight-execution', status: 'available'});
      const cfg = config(env);
      const origin = request.headers.get('origin');
      if (origin && !parseList(env.ALLOWED_ORIGINS_JSON || '[]', v => string(v, 1, 200), true).includes(origin)) refuse(403, 'origin_not_allowed');
      const internal = url.pathname.startsWith('/internal/');
      const expected = `Bearer ${internal ? env.EXECUTION_WORKER_TOKEN : env.EXECUTION_CLIENT_TOKEN}`;
      if (!(await equalToken(request.headers.get('authorization'), expected))) refuse(401, 'unauthorized');
      if (url.pathname === '/mcp') {
        if (request.method !== 'POST') refuse(405, 'post_required');
        const rpc = await body(request);
        if (!rpc || typeof rpc !== 'object' || Array.isArray(rpc) || rpc.jsonrpc !== '2.0' || typeof rpc.method !== 'string') return json({jsonrpc: '2.0', id: null, error: {code: -32600, message: 'Invalid Request'}}, 400);
        const id = rpc.id;
        if (id !== undefined && !(typeof id === 'string' || Number.isSafeInteger(id) || id === null)) return json({jsonrpc: '2.0', id: null, error: {code: -32600, message: 'Invalid Request'}}, 400);
        if (rpc.method.startsWith('notifications/')) return new Response(null, {status: 202});
        if (id === undefined) return json({jsonrpc: '2.0', id: null, error: {code: -32600, message: 'Request id required'}}, 400);
        let result;
        if (rpc.method === 'initialize') result = {protocolVersion: PROTOCOL, capabilities: {tools: {listChanged: false}}, serverInfo: {name: 'starlight-execution', version: '0.1.0'}};
        else if (rpc.method === 'ping') result = {};
        else if (rpc.method === 'tools/list') result = {tools: TOOLS};
        else if (rpc.method === 'tools/call') {
          try { shape(rpc.params, ['name', 'arguments']); } catch { return json({jsonrpc: '2.0', id, error: {code: -32602, message: 'Invalid tool parameters'}}); }
          if (!TOOLS.some(t => t.name === rpc.params.name)) return json({jsonrpc: '2.0', id, error: {code: -32602, message: 'Unknown tool'}});
          const response = await call(env, cfg, rpc.params.name, rpc.params.arguments);
          const data = await response.json();
          result = {content: [{type: 'text', text: JSON.stringify(data)}], isError: !response.ok};
        } else return json({jsonrpc: '2.0', id, error: {code: -32601, message: 'Method not found'}});
        return json({jsonrpc: '2.0', id, result});
      }
      let action, args;
      if (request.method === 'POST' && url.pathname === '/tasks') { action = 'submit_task'; args = await body(request); }
      else if (internal && request.method === 'POST' && ['/internal/claim', '/internal/complete', '/internal/reconcile'].includes(url.pathname)) { action = url.pathname.split('/').at(-1); args = await body(request); }
      else {
        const match = url.pathname.match(/^\/(?:internal\/)?runs\/([a-zA-Z0-9-]{1,80})(?:\/(cancel|artifacts|eval))?$/);
        if (!match) refuse(404, 'not_found');
        const suffix = match[2];
        if (request.method !== (suffix === 'cancel' ? 'POST' : 'GET')) refuse(405, 'method_not_allowed');
        action = suffix === 'cancel' ? 'cancel_run' : suffix === 'artifacts' ? 'get_artifacts' : suffix === 'eval' ? 'get_eval_report' : 'get_run'; args = {run_id: match[1]};
      }
      return call(env, cfg, action, args);
    } catch (error) { return json({error: error instanceof Refusal ? error.code : 'request_failed'}, error instanceof Refusal ? error.status : 500); }
  }
};
