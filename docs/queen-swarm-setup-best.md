# Best-in-the-World Starlight Queen Swarm Setup Process

**Status:** Production control-plane artifact (agentic-ops-hub)
**Validated:** 2026-08-10 via AGY Gemini 3.1 Pro (High) council + Hermes execution
**Source:** fleet/TASK-CONTRACTS.md + AGY audit report (sha256 recorded in receipt)

## Core Philosophy (Advanced & Smooth)
- Queen = strict **Contract Orchestrator**, never a free-form maker.
- Everything is leased, bounded, receipted, Git-synced.
- Human gates on Master Contract only.
- Sequential, evidence-first (no theater).
- One-command + progressive disclosure + dry-run.
- Memory/KG strictly isolated (no pollution of SIS).
- GitOps as the convergence layer.
- Model routing + finite councils for "dozens of specialists" without chaos.
- Admission gates fail-closed on capacity, expiry, budget, allowlist.

This process is the canonical, reusable way to stand up any Starlight Queen swarm.

## 8-Step Best Swarm Setup Process
1. **Define Intent (Human, concise)**  
   Human provides 3-bullet goal + priority + rough budget in DM or ticket.

2. **Draft Master Contract (Queen)**  
   Queen drafts `fleet/bus/contracts/master-xxx.json` (see example in this repo).  
   Includes: machine_owner(s), repo_path_allowlist, resource_budget, allowed_kg_mutations=false, explicit done_condition (and/or receipt_exists, test_pass, git_commit).

3. **Human Gate (Approval)**  
   Human reviews budget, allowlist, expiry, constraints.  
   Approves by commenting or touching a gate file. Queen does not proceed without it.

4. **Sub-Lease Generation (Queen)**  
   Queen decomposes into worker contracts (e.g., worker-frontend, worker-backend, worker-memory-boundary).  
   Assigns to specific machines (yogabook for frontend/UX, c940 for GitOps/backend).

5. **Dry-Run & Diagnostics (Automated)**  
   Command: `python scripts/fleet_swarm_init.py --dry-run --contract master-xxx.json`  
   - Verifies heartbeats in bus/.
   - Shows exact branches, models, AGY lanes, expected receipts.
   - Fails if capacity low or conflicts.

6. **Execution (Machines + AGY)**  
   - Machines claim leases (write claimed_by + heartbeat).
   - Spawn on dedicated branches: `agent/<harness>/<scope>`.
   - Use AGY with exact models (Gemini 3.5 Flash High for audits, 3.1 Pro High for architecture).
   - Sequential one-at-a-time for heavy lanes.
   - Every step produces hashed reports + receipts.

7. **Receipt & Audit (Queen)**  
   Workers write `fleet/bus/receipts/<task>-<machine>.json` with:
   - execution_status + outcome_status
   - done_condition_met
   - evidence_refs + artifacts (with sha256)
   - resource_used
   - next_actions
   Queen verifies all receipts against Master done_condition + Git SHAs.

8. **GitOps Promotion (Queen + Human)**  
   Queen stages merge/PR with all evidence attached.
   Human final approval for main.
   Post-merge: archive contracts, update ledger.

## Executable Admission Gates (Implemented in this elevation)
- Queen refuses without valid Master Contract.
- Validates expiry, budget, repo_path_allowlist, allowed_kg_mutations before any sub-work.
- Capacity check (RAM >=8GiB free, CPU <=80%, 0 active heavy agents) before AGY.
- Phone Link ban + explicit repo leaf only.

## Model & Subagent Assignment (Dozens of Specialists, Controlled)
- Architecture/Contracts/KG boundaries: Gemini 3.1 Pro (High) + strategist
- Audits, DX, GitOps, adversarial: Gemini 3.5 Flash (High) + integrity-guard / discussion-based-planning
- 28-seat council pattern: 14 paired lanes (Principal + Staff per domain).
- Finite sequential: one AGY at a time, receipts before next.

## Adversarial Tests (Must Fail Before, Pass After)
1. Rogue Historian: Worker tries KG mutation without `allowed_kg_mutations: true` → rejected.
2. Zombie Swarm: Expired contract claimed after expiry → refused.
3. Unfunded Queen: Launch without Master Contract → "No valid lease".

## Evidence & Validation
- All contracts/receipts in git (public refs only).
- Hashes + logs in fleet/reports/.
- This doc + TASK-CONTRACTS.md updated with council output.
- Local validation: JSON schema checks + git status narrow + receipt presence.

## Rollback & Non-Actions
- Rollback: git revert the contract/receipt files + re-issue with new task_id.
- Never: broad search, secrets, uncontrolled deploys, parallel heavy writers on same tree, claims without receipts.

This is the smoothest, most advanced, evidence-backed swarm setup process in the estate. Reusable across all domains.

**Delivered & Validated in this repo (control-plane prod):** 2026-08-10.