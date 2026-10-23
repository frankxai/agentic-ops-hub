import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

export function assertShareable(text) {
  // A conservative release filter, not comprehensive DLP. Public artifact hosting stays off.
  if (typeof text !== 'string' || Buffer.byteLength(text) > 65536 ||
      /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-(?:ant-|proj-)?|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{15,}|\bAKIA[A-Z0-9]{16}\b/.test(text)) {
    throw new Error('artifact refused by size or secret scan');
  }
}
export function writeArtifact(root, taskId, name, text) {
  if (!/^[a-z0-9][a-z0-9-]{2,63}$/.test(taskId) || !/^[a-z0-9][a-z0-9.-]{0,79}$/.test(name)) throw new Error('unsafe artifact name');
  assertShareable(text);
  writeFileSync(join(root, name), text, { mode: 0o600 });
  return { name, sha256: createHash('sha256').update(text).digest('hex'), ref: `artifacts/${taskId}/${name}` };
}
