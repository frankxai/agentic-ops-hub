import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, appendFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { create, regenerate, lint, setStatus, parseHandover, paths } from '../scripts/handover.mjs';

function fixture() {
  const root = mkdtempSync(join(tmpdir(), 'handover-'));
  mkdirSync(join(root, 'ops'), { recursive: true });
  writeFileSync(join(root, 'ops', 'HANDOVER-INDEX.md'), '# Index\n\n<!-- handover-index:start -->\n<!-- handover-index:end -->\n\n## Rules\n');
  writeFileSync(join(root, 'ops', 'NEXT-PROMPTS.md'), '');
  create(root, { id: 'H-a', what: 'First', where: 'branch x', owner: 'claude', updated: '2026-10-17' }, '\n## Prompt\n\nDo the thing.\n');
  create(root, { id: 'H-b', what: 'Second | piped', where: 'branch y', owner: 'codex', updated: '2026-10-16' });
  regenerate(root);
  return root;
}

test('a freshly generated hub lints clean', () => {
  assert.deepEqual(lint(fixture()), []);
});

test('index lists every handover and escapes pipes; prompt list holds only live handovers with a prompt', () => {
  const root = fixture();
  const index = readFileSync(paths(root).index, 'utf8');
  assert.match(index, /\[H-a\]\(handovers\/H-a\.md\)/);
  assert.match(index, /Second \\\| piped/);
  const prompts = readFileSync(paths(root).prompts, 'utf8');
  assert.match(prompts, /H-a/);
  assert.doesNotMatch(prompts, /H-b/);
});

test('hand-editing NEXT-PROMPTS.md fails lint', () => {
  const root = fixture();
  appendFileSync(paths(root).prompts, '\n## Current npm prompt\n\nembedded again\n');
  assert.ok(lint(root).some((e) => e.includes('NEXT-PROMPTS.md is stale or hand-edited')));
});

test('a repeated heading and an oversized section are both reported', () => {
  const root = fixture();
  const long = Array.from({ length: 61 }, (_, i) => `line ${i}`).join('\n');
  appendFileSync(paths(root).prompts, `\n## Same\n${long}\n## Same\nx\n`);
  const errors = lint(root);
  assert.ok(errors.some((e) => /section "## Same" is 61 lines/.test(e)), errors.join('\n'));
  assert.ok(errors.some((e) => /repeats heading/.test(e)), errors.join('\n'));
});

test('processed without evidence fails lint, with evidence passes', () => {
  const root = fixture();
  setStatus(root, 'H-a', 'processed', { today: '2026-10-17' });
  regenerate(root);
  assert.ok(lint(root).some((e) => e.includes('H-a: processed without an evidence link')));
  setStatus(root, 'H-a', 'processed', { evidence: 'https://github.com/frankxai/agentic-ops-hub/pull/1', today: '2026-10-17' });
  regenerate(root);
  assert.deepEqual(lint(root), []);
});

test('superseded needs a target that exists', () => {
  const root = fixture();
  setStatus(root, 'H-b', 'superseded', { by: 'H-missing', today: '2026-10-17' });
  regenerate(root);
  assert.ok(lint(root).some((e) => e.includes('superseded_by H-missing has no file')));
});

test('a handover file added without regenerating makes the index stale', () => {
  const root = fixture();
  create(root, { id: 'H-c', what: 'Third', where: 'z', owner: 'grok' });
  assert.ok(lint(root).some((e) => e.includes('HANDOVER-INDEX.md table is stale')));
});

test('unknown status and mismatched id are rejected', () => {
  const root = fixture();
  writeFileSync(join(paths(root).dir, 'H-d.md'), '---\nid: H-other\nstatus: maybe\n---\n');
  regenerate(root);
  const errors = lint(root);
  assert.ok(errors.some((e) => e.includes('does not match file name')));
  assert.ok(errors.some((e) => e.includes('status "maybe"')));
  assert.throws(() => setStatus(root, 'H-a', 'maybe'), /unknown status/);
});

test('frontmatter round-trips and body is kept', () => {
  const root = fixture();
  setStatus(root, 'H-a', 'claimed', { owner: 'grok', today: '2026-10-18' });
  const h = parseHandover(readFileSync(join(paths(root).dir, 'H-a.md'), 'utf8'));
  assert.equal(h.meta.owner, 'grok');
  assert.equal(h.meta.updated, '2026-10-18');
  assert.match(h.body, /Do the thing\./);
});
