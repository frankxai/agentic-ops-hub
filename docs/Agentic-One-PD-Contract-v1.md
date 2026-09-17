# Agentic One PD-OS Contract v1 (Federated)

**Home:** agentic-ops-hub (L2) as the integration contract layer.  
**Philosophy:** One canonical work identity. Federated ownership. Evidence flows (Product Packet → Outcome Pack → Income Asset → Evidence Receipt). No duplicate control planes.

## Core Mappings (inspired by delegation audit)

1. **Product Registry**  
   Base: awesome-product-development-agent-skills/schemas/product-registry.schema.json  
   Fields: identity, lifecycle, ICP, offer, owner, risk class, brand vertical.

2. **Product Packet** (the "thin slice" next verified decision)  
   Base: schemas/product-development-packet.schema.json (or equivalent in awesome-product-development-agent-skills)  
   Contains: decision, hypothesis/assumptions, delivery scope, metrics, owner, proof path, stop condition, taste/evidence gates.

3. **Outcome Pack Binding**  
   Base: agentic-income-skills IncomeSystem / Outcome Pack contract.  
   Links paid work, authority, budget, revocation, evaluation, economics.

4. **Income Asset Binding** (for passive)  
   Base: agenticpassiveincome schemas.  
   Links owned asset, stream, surface map, engine spec, maintenance loop.

5. **Evidence Receipt**  
   Tests, eval version, Git commit/PR, preview, claim review, human gate.

6. **Canonical Work ID**  
   Single ID mapped to: Hermes task / Kanban, GitHub issue/PR, Product Packet, future Paperclip if used, Starlight swarm receipt.

## G-Stack Integration (as adapter, not controller)
- Location found: Primarily in agentic-creator-os/.claude/skills/gstack (229+ files).
- Use: Optional QA / browser persistence / role-specific execution adapter.
- Emit: Evidence only into Product Packet / Evidence Receipt. Do not let it own task state or scheduling.
- Evolve: Project key specialists (office-hours, plan-*, design-*, qa, ship) into portable SKILL.md in this hub or creator-os.

## Paperclip / RooFlow
- Paperclip: No committed integration in primary repos. References in awesome-agent-operating-systems (untracked). Hold for bounded governance only after security gate + proof of lower overhead than current Hermes + Starlight + Git.
- RooFlow/Ruflo: Landscape benchmark only. Overlaps existing swarm fabric. No new plane.

## Delivery Sequence (from audit)
1. Reconcile (one canonical AIS; refresh ECOSYSTEM.md).
2. Schema convergence (adapters only; preserve compatibility).
3. One vertical-slice proof (e.g., agenticincome offer → scoring → packet → Outcome Pack → income asset).
4. Unified release gate (validators + evidence + human gate).
5. Governance after proof.

## Implementation Notes for this OS
- Store contracts/examples in this repo under docs/ or schemas/.
- Queen/swarm updates receipts with work ID.
- Dashboard (HTML prototype + future) visualizes the flow with one ID.
- Per-brand: Extend registry with vertical (Arcanea canon, Income flows, etc.).

This contract makes the PD-OS portable and federated while keeping agentic-ops-hub as the config anchor.
