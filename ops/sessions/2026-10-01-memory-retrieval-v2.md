# 2026-10-01 — memory: Retrieval v2, truth reconciliation, MemPalace + paired protocol, referee lane

Harness: Claude (Opus 5.5) coordinating three Opus subagents and an R&D scout, each in its own
worktree. Every PR was reviewed by Codex (codex-rescue) in repeated rounds and signed through
`tools/pr-gate.mjs` (maker ≠ checker). Frank granted full authority for merges on 2026-09-30.

## Merged to `frankxai/starlight-memory` main

| PR | What | Evidence |
| --- | --- | --- |
| #16 | Consolidation reports stay out of the recall index; only authored memories load from `observations/` and `review/` | 3 Codex rounds, mutation-tested |
| #13 | MemPalace adapter, Mem0/MemPalace positioning, paired eval protocol (exact McNemar + seeded bootstrap), provider-id ledger: forget resolves real provider ids, single-flight per key, cancels unsent writes, tenant-filtered recall | 4 Codex rounds, 110 tests |
| #18 | Read-time truth reconciliation: `supersedes` / `superseded_by` / `valid_from` / `valid_to`; superseded or expired memories are demoted (never dropped) and annotated, replacements in force are pulled in (bounded), strict UTC ISO dates | 4 Codex rounds, 22/22 mutations caught; on the live vault it reorders nothing until memories carry the fields |
| #17 | Retrieval v2 with a paired eval: index down-weight on in `memory_recall`; cross-encoder rerank opt-in via `--rerank`; wikilink-graph spreading measured and removed (MRR 0.915 → 0.320) | 5 Codex rounds; see numbers below |

Retrieval v2 against v1 (production hybrid), paired per query, with a pool-size control:

- 38 real prompts: v2 MRR 0.694 → 0.749, +0.055, bootstrap 95% CI [0.014, 0.106]. No hit@k
  difference is significant under McNemar, and this set was not held out from development.
- 76 synthetic queries: +0.033 [0.002, 0.069]. The set is saturated (v1 hit@10 0.987).
- Rerank costs ~4 s p50 per query on this laptop's CPU, which is why it is opt-in.

## Production

`repos/starlight-memory` is on main `7a9c53f` with `dist` rebuilt. A live stdio smoke run on the
real vault served 13 tools, and hybrid recall plus reconcile returned the right memories.
`npm install` (lockfile unchanged) added `@hono/node-server` and the embedder; preflight allowed it
as an `interactive` workload with a 1.5 GB reserve while `build` was on HOLD. Suite: 138/138.

## In flight

- **#19 referee lane** (draft): official LongMemEval-S retrieval scorer port, streaming dataset
  reader, hash-pinned download, receipts. Codex found the reported 94.7% recall_any@5 inflated: the
  runner dropped no-target questions that upstream keeps as zeros. The agent is correcting the
  number plus 4 P2s (pinned numpy with UV_CACHE_DIR, exact cache-path check, output-path validation,
  dirty-run receipts). Do not cite 94.7%.
- **Security note:** before the hash pin existed, the referee agent executed the upstream
  `eval_utils.py` once, unverified. It was fetched from a commit-pinned URL in the MIT LongMemEval
  repo, and a classifier flagged the action. It is now refused unless its sha256 matches.

## R&D for the next agent

`docs/research/memory-rd-brief-2026-10-01.md` on main lists ranked experiments with dated sources:

- E1: grow a real-prompt held-out set to ~150 queries by pooled labelling. This gates everything.
- E2: Granite-embedding-small-r2 as the semantic leg. Fix the embedding cache key first: it carries
  no model id.
- E3: derived dates plus supersession proposals, now that #18 can consume them.
- E4: typo-tolerant lexical fallback.
- E5: EmbeddingGemma, parked behind a RAM/latency gate.

Rejected after measurement: clause splitting, RRF weight tuning, bge-small, arctic-embed-xs.

## Open

- Vault `review/queue.md`: 9 human items, unworked. The consolidation loop only improves memory
  once someone ratifies these.
- Rerank latency: next experiment is top-10 instead of top-30, or a q8 model, measured paired.
- The forget ledger lives in memory: ids are lost on restart until `flush` writes provider ids back
  into `provider_shadow_refs`.
- Tracking issue: frankxai/starlight-memory#8.
