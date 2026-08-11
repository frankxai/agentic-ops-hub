# 06 — Swarm delivery and client trust

## The productized delivery swarm

A client does not buy "a swarm." They buy a named business outcome, a clear accountable owner, and a safe delivery process.

```text
Client owner (decisions / approval)
        ↕
Engagement lead / Queen (scope, quality, delivery)
        ├─ Domain researcher: sources, workflow map
        ├─ Product designer: user journey, UI, personas
        ├─ Builder: implementation in isolated worktree
        ├─ QA / evaluator: primary path, security/truth review
        └─ Ops: deployment, monitoring, handoff receipts
```

## Boundary table

| Can be automated | Requires human approval | Never delegate to an unbounded agent |
|---|---|---|
| draft, classify, summarize, extract, propose, test, prepare | publish, send external communication, change business data, choose recommendation, grant access, change billing/config | payments, contracts, credentials, employee/customer termination, regulated final decisions, destructive operations |

## Client engagement phases

1. **Diagnostic** — inspect existing workflow and define a measurable job.  
2. **Proposal** — fixed scope, outcome, exclusions, customer responsibilities, data boundary.  
3. **Build / configure** — work in a controlled tenant/worktree; no production data by default.  
4. **Review** — client executes primary path, verifies outputs and approvals.  
5. **Launch** — enable the narrow approved workflow; create support/rollback path.  
6. **Handoff / learn** — delivery receipt, export, training, 30-day result review.

## Required client receipts

- signed/accepted scope (commercial terms handled appropriately)
- data source / processing authorization
- domain expert decisions and approval points
- test acceptance
- launch approval
- deployed/version receipt
- export/handoff location
- incident / rollback contact

## AaaS technical minimum

```text
Tenant ID on every request
RBAC and least privilege
Server-side credentials only
Tool allowlist + input validation
Confirmation token for high-impact action
Idempotency keys for writes
Append-only action receipts/audit record
Usage/budget cap
Error monitoring and kill switch
Export/exit path
```

## Delivery economics

A delivery swarm is profitable only when the client-facing time falls each cycle because shared modules, test suites, checklists and connectors improve.

Track:

- sales-to-start days
- human hours per delivery
- agent/model/infrastructure cost per delivery
- reuse percentage
- first-success time
- P0/P1 escapes
- 30-day outcome score
- expansion/referral rate

If human time increases on the second client, halt expansion and refactor the shared core.
