import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assertShareable } from '../artifacts.mjs';
import { publishDraft } from '../publication.mjs';

test('artifact release filter blocks planted provider keys and private keys', () => {
  const prefixes = ['sk-' + 'proj-', 'sk-' + 'ant-api03-', 'sk-', ...['p', 'o', 'u', 's', 'r'].map(x => 'gh' + x + '_'), 'github_' + 'pat_'];
  for (const prefix of prefixes) assert.throws(() => assertShareable(prefix + 'x'.repeat(36)));
  assert.throws(() => assertShareable('AK' + 'IA' + 'X'.repeat(16)));
  assert.throws(() => assertShareable('-----BEGIN ' + 'PRIVATE KEY-----'));
  assert.throws(() => assertShareable('€'.repeat(22000)));
  assert.doesNotThrow(() => assertShareable('Public key fingerprints and normal patch text.'));
});
const packet = { schema: 'starlight.draft-publication.v1', repository: 'frankxai/agentic-ops-hub', base_branch: 'main',
  base_sha: 'a'.repeat(40), base_tree_sha: 'b'.repeat(40), artifact_sha: 'c'.repeat(40), artifact_tree_sha: 'd'.repeat(40),
  branch: 'agent/codex/fixture', files: [], title: 'fixed title', body: 'fixed body' };
function apiMock({ baseMoved = false, wrongTree = false, branchExists = false, wrongBranchTree = false, wrongParent = false, existingPR = false } = {}) {
  const calls = [];
  const api = async (method, path, data) => {
    calls.push({ method, path, data });
    if (path.endsWith('/git/ref/heads/main')) return { object: { sha: baseMoved ? 'e'.repeat(40) : packet.base_sha } };
    if (path.endsWith('/git/trees')) return { sha: wrongTree ? 'e'.repeat(40) : packet.artifact_tree_sha };
    if (path.endsWith('/git/ref/heads/' + packet.branch)) return branchExists ? { object: { sha: 'f'.repeat(40) } } : null;
    if (path.includes('/git/commits/')) return { tree: { sha: wrongBranchTree ? 'e'.repeat(40) : packet.artifact_tree_sha }, parents: [{ sha: wrongParent ? 'e'.repeat(40) : packet.base_sha }] };
    if (path.endsWith('/git/commits')) return { sha: 'f'.repeat(40) };
    if (path.endsWith('/git/refs')) return { object: { sha: data.sha } };
    if (method === 'GET' && path.includes('/pulls?')) return existingPR ? [{ head: { sha: 'f'.repeat(40) }, base: { ref: 'main' }, draft: true, html_url: 'https://github.com/example/pr/1' }] : [];
    if (path.endsWith('/pulls')) return { html_url: 'https://github.com/example/pr/1' };
    throw new Error('unexpected API request');
  };
  return { api, calls };
}
test('publication refuses a moved base before writing anything', async () => {
  const { api, calls } = apiMock({ baseMoved: true });
  await assert.rejects(publishDraft(packet, api), /base moved/);
  assert.ok(calls.every(c => c.method === 'GET'));
});
test('publication refuses a different tree before creating a branch or PR', async () => {
  const { api, calls } = apiMock({ wrongTree: true });
  await assert.rejects(publishDraft(packet, api), /tree differs/);
  assert.equal(calls.filter(c => c.path.endsWith('/pulls')).length, 0);
});
test('publication creates only a draft and discloses distinct signed artifact SHA', async () => {
  const { api, calls } = apiMock(); const result = await publishDraft(packet, api);
  assert.equal(result.artifact_sha, packet.artifact_sha);
  assert.notEqual(result.commit_sha, result.artifact_sha);
  assert.equal(calls.find(c => c.path.endsWith('/pulls')).data.draft, true);
});
test('publication replay reuses matching branch and existing draft', async () => {
  const { api, calls } = apiMock({ branchExists: true, existingPR: true });
  assert.equal((await publishDraft(packet, api)).replayed, true);
  assert.equal(calls.filter(c => c.method === 'POST' && !c.path.endsWith('/git/trees')).length, 0);
});
test('publication never overwrites an existing different branch', async () => {
  const { api } = apiMock({ branchExists: true, wrongBranchTree: true });
  await assert.rejects(publishDraft(packet, api), /refusing overwrite/);
});
test('equal tree on unrelated commit cannot be reused as the draft branch', async () => {
  const { api } = apiMock({ branchExists: true, wrongParent: true });
  await assert.rejects(publishDraft(packet, api), /lineage/);
});
