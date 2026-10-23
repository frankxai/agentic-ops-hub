#!/usr/bin/env node
// Operator-installed kernel adapter. The remote task may select a contract, never author one.
import { readFileSync, writeFileSync, realpathSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { writeArtifact } from './artifacts.mjs';
const digest = (text) => createHash('sha256').update(text).digest('hex');
const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
if (input.version !== 1 || !/^[a-z0-9][a-z0-9-]{2,63}$/.test(input.taskId) ||
    !/^[a-f0-9]{64}$/.test(input.contractId) || !/^[a-f0-9]{40}$/.test(input.revision)) throw new Error('bad dispatch');
const moduleAt = (name) => pathToFileURL(join(realpathSync(input.kernelRoot), 'src', name)).href;
const { context, operations } = await import(moduleAt('cli.mjs'));
const { loadContract } = await import(moduleAt('contract.mjs'));
const { readEvents, fold } = await import(moduleAt('log.mjs'));
const { git, revParse } = await import(moduleAt('git.mjs'));
const { exportPublicKey, verifyReceiptWithKey } = await import(moduleAt('receipt.mjs'));
const ctx = context({ home: input.home, policy: input.policy });
const contract = loadContract(ctx.home, input.contractId);
const source = revParse(contract.repo, contract.targetRef);
const origin = git(contract.repo, ['remote', 'get-url', 'origin']);
const slug = origin.match(/^https:\/\/github\.com\/([\w.-]+\/[\w.-]+?)(?:\.git)?$/)?.[1];
if (source !== input.revision || slug !== input.repository) throw new Error('contract source differs from admission');
const route = ctx.policy.classes[contract.taskClass];
// This release activates only the two operator fixture adapters below. A user-installed shell
// script is arbitrary same-user code, so the generic kernel shell adapter is not a remote capability.
const fixtureRoot = resolve(import.meta.dirname, 'fixtures');
if (route.maker !== `shell:${join(fixtureRoot, 'lab-portability-maker.mjs')}` ||
    route.grader !== `shell:${join(fixtureRoot, 'lab-portability-checker.mjs')}`) throw new Error('live maker isolation not activated');
operations.taskCreate({ ...ctx, taskId: input.taskId, contractId: input.contractId });
const [runCode, summary] = operations.run({ ...ctx, taskId: input.taskId });
const [checkCode, checked] = operations.check({ ...ctx, taskId: input.taskId });
const state = fold(readEvents(ctx.home, input.taskId));
const issued = state.last['receipt.issued'];
if (!issued) throw new Error('no kernel receipt');
const receiptBytes = readFileSync(join(ctx.home, 'receipts', `${issued.data.receiptId}.json`), 'utf8');
const receipt = JSON.parse(receiptBytes);
const publicKey = exportPublicKey(ctx.home);
const external = verifyReceiptWithKey(publicKey.publicKey, receipt, {
  artifactSha: state.last['attempt.result']?.data.artifactSha, targetSha: input.revision,
  contractId: input.contractId, policyVersion: ctx.policy.version,
});
const ok = runCode === 0 && checkCode === 0 && external.valid;
const artifactSha = state.last['attempt.result']?.data.artifactSha;
const patch = artifactSha ? git(contract.repo, ['diff', '--binary', '--no-ext-diff', '--no-textconv', input.revision, artifactSha]) : '';
const proof = JSON.stringify({ schema: 'starlight.execution-verification.v1', task_id: input.taskId,
  repository: input.repository, revision: input.revision, contract_id: input.contractId,
  kernel_summary: summary, kernel_check: checked, public_key_verification: external,
  verification_kind: 'deterministic-estate-fixture', independent_model_review: false,
  model_calls: 0, model_cost_microusd: 0, infrastructure_cost_microusd: null }, null, 2);
const files = { 'candidate.patch': patch, 'kernel-receipt.json': receiptBytes,
  'public-key.pem': publicKey.publicKey, 'verification.json': proof };
const artifacts = [];
for (const [name, text] of Object.entries(files)) {
  artifacts.push(writeArtifact(input.outputRoot, input.taskId, name, text));
}
console.log(JSON.stringify({ status: ok ? 'succeeded' : 'failed',
  // No inference is invoked by the two fixed fixtures. This is model usage only, not infra cost.
  actual_cost_microusd: 0, artifacts,
  verification: { passed: ok, actor: 'deterministic-protected-checks', maker: 'deterministic-estate-repair', evidence_sha256: digest(proof) },
  receipt_sha256: digest(receiptBytes) }));
