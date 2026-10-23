// Publication stays in a trusted service lane. The maker never receives GitHub credentials.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { assertShareable } from './artifacts.mjs';

export async function preparePublication({ kernelRoot, kernelHome, taskId, policy, repository, baseBranch }) {
  if (!/^[\w.-]+\/[\w.-]+$/.test(repository) || !/^[\w./-]+$/.test(baseBranch) || baseBranch.includes('..')) throw new Error('invalid publication target');
  const { context, operations } = await import(pathToFileURL(join(kernelRoot, 'src/cli.mjs')));
  const { readEvents, fold } = await import(pathToFileURL(join(kernelRoot, 'src/log.mjs')));
  const { loadContract } = await import(pathToFileURL(join(kernelRoot, 'src/contract.mjs')));
  const { git } = await import(pathToFileURL(join(kernelRoot, 'src/git.mjs')));
  const ctx = context({ home: kernelHome, policy });
  const [code] = operations.check({ ...ctx, taskId });
  if (code !== 0) throw new Error('unverified task cannot publish');
  const state = fold(readEvents(ctx.home, taskId)), contract = loadContract(ctx.home, state.contractId);
  const receipt = JSON.parse(readFileSync(join(ctx.home, 'receipts', `${state.last['receipt.issued'].data.receiptId}.json`)));
  if (git(contract.repo, ['remote', 'get-url', 'origin']) !== `https://github.com/${repository}.git`) throw new Error('wrong publication repository');
  const paths = git(contract.repo, ['diff', '--name-only', receipt.targetSha, receipt.artifactSha]).split('\n').filter(Boolean);
  if (!paths.length || paths.length > 30) throw new Error('empty or oversized publication');
  const files = paths.map((path) => {
    if (!/^[A-Za-z0-9_./-]+$/.test(path) || path.split('/').includes('..') || path.startsWith('.git')) throw new Error('unsafe publication path');
    const mode = git(contract.repo, ['ls-tree', receipt.artifactSha, '--', path]).split(' ')[0];
    if (!['100644', '100755'].includes(mode)) throw new Error('only regular UTF-8 file changes supported');
    const content = git(contract.repo, ['show', `${receipt.artifactSha}:${path}`]);
    // git() trims command output; recover exact trailing newlines through the object's byte length.
    // Publication must never silently alter a tested blob, so use execFileSync below instead.
    return { path, mode, type: 'blob', content };
  });
  const { execFileSync } = await import('node:child_process');
  for (const entry of files) {
    const bytes = execFileSync('git', ['-C', contract.repo, '-c', 'core.hooksPath=/dev/null', 'show', `${receipt.artifactSha}:${entry.path}`], { maxBuffer: 131072 });
    entry.content = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    assertShareable(entry.content);
  }
  return { schema: 'starlight.draft-publication.v1', repository, base_branch: baseBranch,
    base_sha: receipt.targetSha, base_tree_sha: git(contract.repo, ['rev-parse', `${receipt.targetSha}^{tree}`]),
    artifact_sha: receipt.artifactSha, artifact_tree_sha: git(contract.repo, ['rev-parse', `${receipt.artifactSha}^{tree}`]),
    branch: `agent/codex/execution-${taskId}`, files,
    title: 'fix(lab): run local receipt invariants without an external SIS checkout',
    body: 'Moves the external-checkout skip onto the two conformance tests. The nine local semantic checks now run on Linux.\n\nProduced by a fixed deterministic estate-repair fixture through authenticated local Cloudflare coordination and Starlight Kernel. Protected acceptance ran 99 tests: 97 pass, 2 external skips. This is integration evidence, not independent model review.\n\nThe kernel receipt binds the original local artifact commit. This PR must match its exact Git tree; a GitHub-created commit has different metadata and a different SHA. Do not present that SHA as the signed artifact.' };
}

export async function publishDraft(packet, api) {
  // api is a trusted connector or a narrowly-scoped REST client. No tokens in the packet.
  if (packet.schema !== 'starlight.draft-publication.v1') throw new Error('invalid publication packet');
  const root = `/repos/${packet.repository}`;
  const base = await api('GET', `${root}/git/ref/heads/${packet.base_branch}`);
  if (base.object.sha !== packet.base_sha) throw new Error('publication base moved; reverify first');
  const tree = await api('POST', `${root}/git/trees`, { base_tree: packet.base_tree_sha, tree: packet.files });
  if (tree.sha !== packet.artifact_tree_sha) throw new Error('published tree differs from verified artifact');
  let branch = await api('GET', `${root}/git/ref/heads/${packet.branch}`, undefined, { allow404: true });
  if (branch) {
    const commit = await api('GET', `${root}/git/commits/${branch.object.sha}`);
    if (commit.tree.sha !== tree.sha || commit.parents?.length !== 1 || commit.parents[0].sha !== packet.base_sha) {
      throw new Error('existing branch differs in tree or lineage; refusing overwrite');
    }
  } else {
    const commit = await api('POST', `${root}/git/commits`, { message: packet.title, tree: tree.sha, parents: [packet.base_sha] });
    branch = await api('POST', `${root}/git/refs`, { ref: `refs/heads/${packet.branch}`, sha: commit.sha });
  }
  const prs = await api('GET', `${root}/pulls?state=open&head=${encodeURIComponent(packet.repository.split('/')[0] + ':' + packet.branch)}`);
  const existing = prs.find((pr) => pr.head.sha === branch.object.sha && pr.base.ref === packet.base_branch);
  if (existing) {
    if (!existing.draft) throw new Error('existing PR is not a draft; manual review required');
    return { url: existing.html_url, replayed: true, commit_sha: branch.object.sha, artifact_sha: packet.artifact_sha, tree_sha: tree.sha };
  }
  const pr = await api('POST', `${root}/pulls`, { title: packet.title, body: packet.body, head: packet.branch, base: packet.base_branch, draft: true });
  return { url: pr.html_url, replayed: false, commit_sha: branch.object.sha, artifact_sha: packet.artifact_sha, tree_sha: tree.sha };
}
