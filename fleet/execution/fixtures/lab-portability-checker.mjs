// A deliberately narrow deterministic checker, not a cross-vendor model judge.
import { readFileSync } from 'node:fs';
const prompt = readFileSync(0, 'utf8');
const files = [...prompt.matchAll(/^\+\+\+ b\/(.+)$/gm)].map((m) => m[1]);
const ok = files.length === 1 && files[0] === 'tests/test_receipt_bridge.py' &&
  prompt.includes('-@unittest.skipUnless') && prompt.includes('+@unittest.skipUnless');
console.log(JSON.stringify({ verdict: ok ? 'accept' : 'reject', findings: [ok ? 'Only the expected test guard moved; protected suite is the behavioral judge' : 'Unexpected diff'] }));
