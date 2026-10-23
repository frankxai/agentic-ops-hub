// Fixed deterministic replay of the independently identified estate bug; no inference.
import { readFileSync, writeFileSync } from 'node:fs';
const path = 'tests/test_receipt_bridge.py';
let source = readFileSync(path, 'utf8');
const guard = '@unittest.skipUnless((SIS / "protocol" / "run-receipt.v1.schema.json").exists(), "SIS checkout not present")\n';
if (!source.includes(guard + 'class SemanticInvariantTests') || source.includes(guard + 'class ConformanceTests')) process.exit(2);
source = source.replace(guard + 'class SemanticInvariantTests', 'class SemanticInvariantTests')
  .replace('class ConformanceTests', guard + 'class ConformanceTests');
writeFileSync(path, source);
console.log(JSON.stringify({ fixture: 'lab-portability', model_calls: 0 }));
