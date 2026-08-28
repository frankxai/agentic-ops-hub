# Fleet Task Contract & Receipt Schema v1

**Status:** candidate contract format; operational only after an owner-issued contract is committed and
its current lifecycle checks pass.
**Owner:** fleet control plane (agentic-ops)
**SSOT:** `fleet/bus/contracts/` + `fleet/bus/receipts/` + this file (git)
**Cross-machine:** committed JSON + MD only. No live sockets/telemetry/private state. See "Phone Link note" in WORKSPACE_MAP.

## Principles (from task t_b332aaec)
- Lease-based: task has explicit machine owner, expiry, budget, allowlist.
- SSOT via git: any machine can claim by writing receipt/heartbeat; conflict via git.
- No private telemetry: evidence is public refs only (paths, shas, report files in fleet/reports/).
- Done-condition explicit so machines can verify without central coordinator.
- Idempotent: task_id + machine_owner unique for claim.

## TaskContract (Lease) v1

JSON shape (written to `fleet/bus/contracts/<task_id>.json` ):

```json
{
  "schema_version": "1.0.0",
  "task_id": "string (slug or uuid, e.g. fleet-night-2026-07-17-n1)",
  "title": "string",
  "description": "string (full packet body or summary)",
  "issuer": "string (command-center | frank | c940 | ...)",
  "issued_at": "2026-07-17T12:00:00Z",
  "machine_owner": "string (c940 | yoga-book | future)",
  "repo_path_allowlist": [
    "agentic-ops",
    "FrankX:docs/ops/*",
    "frankx.ai-vercel-website"
  ],
  "resource_budget": {
    "max_tokens": 100000,
    "max_minutes": 45,
    "max_cost_usd": 2.0,
    "models_allowed": ["grok-4.5", "claude-3-5"]
  },
  "expiry": "2026-07-18T00:00:00Z",
  "done_condition": {
    "type": "or",
    "conditions": [
      { "type": "file_exists", "path": "fleet/reports/xxx.md" },
      { "type": "test_pass", "cmd": "python -m pytest tests/test_foo.py" },
      { "type": "git_commit", "pattern": "fix(fleet): ..." },
      { "type": "kanban_done", "local_id": "t_xxxx" }
    ]
  },
  "priority": "P0",
  "constraints": [
    "no force push",
    "no dirty wipe",
    "register-boundary:professional"
  ],
  "source": "fleet/TASK-PACKETS.md#PacketX | ops/OPS-LEDGER | ...",
  "execution_status": "issued",
  "outcome_status": null,
  "claimed_by": null,
  "claimed_at": null,
  "evidence_refs": []
}
```

Key fields per spec:
- task lease (the whole + expiry, done-condition)
- machine owner
- repo/path allowlist
- resource budget
- expiry
- done-condition
- execution_status
- outcome_status
- evidence refs

## TaskReceipt v1

Written to `fleet/bus/receipts/<task_id>-<machine>.json` on completion/update.

```json
{
  "schema_version": "1.0.0",
  "task_id": "string",
  "machine": "c940",
  "receipt_id": "string (e.g. receipt-uuid or timestamped)",
  "at": "2026-07-17T13:45:00Z",
  "execution_status": "completed",
  "outcome_status": "success",
  "summary": "1-3 sentence human readable + metrics. e.g. Night runner executed 4/4; 12k tokens used.",
  "done_condition_met": [
    "file_exists:fleet/reports/night/2026-07-17-n1-agentic-ops.md",
    "git_commit:92a874f"
  ],
  "evidence_refs": [
    "fleet/reports/night/2026-07-17-n1-agentic-ops.md",
    "commit:92a874f",
    "bus/heartbeats/c940.json",
    "kanban:t_b332aaec"
  ],
  "artifacts": [
    { "type": "file", "path": "fleet/reports/...", "sha256": "..." },
    { "type": "pr", "number": 17, "url": "https://github.com/frankxai/agentic-ops-hub/pull/17" }
  ],
  "resource_used": {
    "tokens": 12345,
    "minutes": 12,
    "cost_usd": 0.11
  },
  "next_actions": ["string list for follow up"],
  "errors": []
}
```

## Lifecycle / Status Machine

- `issued`: a proven local issuer writes a complete, validated contract.
- `claimed`: the named physical owner claims a still-current `issued` contract.
- `running`: the owner records in-progress work only after its claim.
- `completed` | `expired` | `cancelled`: terminal states. `completed` requires an owner-authored receipt,
  an existing claim by that owner, an unexpired contract, and at least one evidence reference.
- Readers on other machines only pull and inspect contracts/receipts. They never claim, heartbeat, or
  complete peer-owned work.

A contract is not live merely because its JSON exists. Unknown, malformed, unclaimed, expired, and
historical contracts are `HOLD` until their owner creates a fresh contract or returned receipt.

## Bus / Script Integration v1
Extend `scripts/fleet_bus.py` :
- `python scripts/fleet_bus.py task-lease --task-id <id> --machine <owner> --file contract.json`
- `python scripts/fleet_bus.py task-claim --task-id <id>`
- `python scripts/fleet_bus.py task-receipt --task-id <id> --outcome success --summary "..." --evidence "file1,commit:xxx"`
- `python scripts/fleet_bus.py task-status --task-id <id>`

Contracts and receipts also appear in queues as items with "task_id" ref.

## Usage in TASK-PACKETS.md and night manifests
Packets now reference or are backed by a contract lease.
E.g. night runner will use resource_budget, allowlist, done_condition.

## Verification (2026-08-28 hardening)

- Four Git facts and `verify-lane` were checked before this update in the verified
  `agentic-ops-hub` checkout.
- The command accepts only a full `--file` lease from the proven local issuer; it rejects unsafe task
  IDs, absolute/traversing allowlists, incomplete budgets/done conditions, foreign issuers, foreign
  claims/receipts, expired contracts, unclaimed receipts, and receipts without evidence.
- `tests/test_fleet_bus.py` runs against an auto-cleaned temporary bus root and proves those refusal
  paths; it does not write the live fleet bus.
- Existing historical C940-labelled local files are not reclassified or published by this document.
  Only a physical C940 process may create or refresh its identity, heartbeat, contract claim, or receipt.

`fleet/schemas/task-contract.v1.schema.json` defines the portable v1 contract shape. The
runtime validator enforces the same required ownership, allowance, budget, lifecycle, and evidence
fields; extension properties remain allowed for backward-compatible machine-specific metadata.

## Locations (SSOT only)
fleet/TASK-CONTRACTS.md
fleet/schemas/task-contract.v1.schema.json
fleet/bus/contracts/*.json
fleet/bus/receipts/*.json
Updated: fleet/FLEET-OPS.md , fleet/TASK-PACKETS.md (refs), scripts/fleet_bus.py , COMMAND-CENTER-DISPATCH.md (optional)
Reports: fleet/reports/
**Rule:** Owner machine ONLY writes to its contracts/receipts/heartbeats/identity. Git is the cross-machine sync. Use fleet_bus.py for all writes.

## Historical elevation note (2026-08-10)

The Queen/swarm elevation artifacts below are retained as design history. They do not authorize work,
prove a current AGY route, or convert an old contract/receipt into current execution evidence. Any new
Queen run must begin with the validated v1 lifecycle above and a fresh owner-issued contract.

See `docs/queen-swarm-setup-best.md` for the archived process discussion and require a new receipt for
any future implementation.
