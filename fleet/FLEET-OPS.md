# Fleet Ops — Multi-Machine Operational Excellence

**SoT:** this file + `fleet/clone-manifest.json` + `ops/OPS-LEDGER.md`  
**Owner machine:** C940 (`DESKTOP-1B4ICID`) always-on control plane  
**Companion:** Yoga Book (frontend/innovation) → future machines via same manifest slot  

## Purpose

Bring private GitHub estate, local clones, agent CLIs, backups, and production targets into one managed loop that scales from **2 laptops → N machines**.

## Roles

| Machine ID | Role | Primary tools | Clone set |
| --- | --- | --- | --- |
| `c940` | Backend, content/GEO, ops, crons, backups | Hermes full + Claude Code + Codex | Full (priority ≤3) |
| `yoga-book` | Frontend, product UI, innovation | Codex + Antigravity + light Hermes | `yoga_book_core` |
| `node-a` | Background agent swarm, headless browser QA, builds, MCP singletons, monitoring | Claude Code, Codex, Grok CLI, Playwright | Role-based subset (see Daily cells) |
| `future` | Expandable | Assign on onboard | Role-based subset |
## Daily / Weekly Loops

### C940 (always-on)
| When | Job | How |
| --- | --- | --- |
| Boot / AM | Inventory | `python scripts/fleet_inventory.py --machine c940` |
| AM | Safe sync | `python scripts/fleet_sync.py --machine c940` |
| 07:00 | Railway health | existing cron |
| 09:00 | OPS sweep | existing `daily-ops-sweep` |
| 10–15 | Content/GEO/PR/image | existing crons |
| Weekly Mon | Railway Queen | existing cron |
| Weekly | Backup verify | `python scripts/fleet_backup_check.py` |
| Session end | Ledger | append OPS-LEDGER |

### Yoga Book
1. `gh auth status` must be frankxai  
2. Clone/pull control plane: `agentic-ops`  
3. Run inventory + sync for `yoga-book`  
4. Claim frontend lane in OPS-LEDGER  
5. Work on `agent/book/<scope>` branches only  
6. Push + ledger note before shutdown  

## Daily cells (proposal; every schedule stays Frank-gated)

Inventory of 2026-10-05 (probe again before citing): 27 registered properties, 24 live; 50 `Starlight*` tasks with 5 enabled; 34 loop contracts, runner disabled, last run 27 green, 6 red, 5 without a gate; 15 registered agents plus 12 steward domains that have no schedule; 9 properties with owner [OPEN]; 418 open PRs, 9 repos over the 10-PR budget. The swarm extends this system. It adds no second orchestrator.

| Cell | Lead (existing agent) | Daily output | Evidence |
| --- | --- | --- | --- |
| Reliability | corps-reliability, steward-infra | Tier 1 uptime and deploy verification, red CI triage | receipt per run, heartbeat |
| Backlog landing | corps-engineering | land or close PRs until each repo is at 8 or fewer open | `pr-budget.json` before and after |
| Design refinement | corps-design, plus a design steward to forge | one refinement lane per day on a Tier 1 site, mobile predicates, weekly excellence scan | craft receipt, device run |
| Product engineering | gencreator-product-lead, skill-foundry-lead | one slice per day on a `building` product, broken waitlist doors first | gate receipt, `products.graph.json` row |
| Content and distribution | steward-content | cadence per brand, Postiz queue; live posts stay human-gated | content-ops receipts |
| Verification | a different harness than the maker (Grok first while its quota is low) | sign-off on exact head through `pr-gate` | PR comment bound to head SHA |
| Weekly | steward-security, steward-release, steward-memory, steward-skills | sweep and report | receipt |

Proposed owners for the nine [OPEN] properties, for Frank to accept or change: starlight.technology, starlight.you, starlightintelligence.academy, starlight.domains and starlightintelligence.ai to steward-substrate (one Starlight brand lead); gencreator.community to steward-revenue (it already owns gencreator.ai); bluelifecommons.org to steward-partnerships; cecilia.chat to steward-content; the personal site stays unowned.

Enablement order, each step a Frank-run command with a metric before the next: (0) node installed, `pp` admitted, queen workers capped at 6; (1) backlog-landing sprint with two reviewer lanes, no schedule; (2) re-enable the property pulse; (3) fix the 6 red and 5 gate-less loops, then re-enable the loop fleet; (4) schedule steward passes one domain at a time; (5) forge the design steward with `agent-forge`, maker is not checker. A step counts as done when its metric has moved and receipts exist. Crons stay `alwaysOffUntilApproved`.
## Work distribution rules

1. **Git is coordination.** One agent = one branch = preferably one worktree.  
2. Branch: `agent/<machine>/<scope>`  
3. Never two writers in same working tree.  
4. Dirty trees: fetch only — no auto-reset.  
5. Handoff package: PR or pushed branch + 5 lines in `ops/OPS-LEDGER.md`.  
6. Register boundaries: FrankX professional / Arcanea mythic / SIS-ACOS neutral.

## Commands (both machines)

```bash
cd ~/agentic-ops   # or C:/Users/frank/agentic-ops

# What is installed + clone health
python scripts/fleet_inventory.py

# Clone missing + fetch; ff-pull only if clean
python scripts/fleet_sync.py --dry-run
python scripts/fleet_sync.py

# Backup posture check
python scripts/fleet_backup_check.py
```

## Production targets (priority order)

See `clone-manifest.json` → `production_targets`:

1. **P0** frankx.ai production ship path  
2. **P0** R1 FrankX → GenCreator bridge  
3. **P1** SIS memory substrate health  
4. **P1** ACOS execution layer  
5. **P1** Arcanea surfaces  
6. **P1** Railway estate  

## Agent task packets

See `fleet/TASK-PACKETS.md` — copy-paste goals for Hermes / Claude Code / Codex / Book machine.

## Adding machine N+1

1. Add entry under `machines` in clone-manifest.  
2. Define `on: [...]` for each repo.  
3. On new machine: install git, gh, node, pnpm, hermes (or lite), claude/codex as needed.  
4. `gh auth login` as frankxai.  
5. Clone `agentic-ops` first.  
6. Run inventory + sync.  
7. Announce in OPS-LEDGER with hostname + role.  

## Files

| Path | Role |
| --- | --- |
| `fleet/clone-manifest.json` | SoT for machines, repos, prod targets |
| `pulse/<machine>` branches | Live heartbeat (`heartbeat.json`, one force-pushed commit). Main is PR-only, so heartbeats never go there. Expected machines = `liveness` blocks in clone-manifest; `.github/workflows/fleet-watch.yml` alarms on a missing or stale pulse |
| `fleet/last-inventory.json` | Latest inventory snapshot |
| `fleet/last-sync.json` | Latest sync report |
| `fleet/BACKUP-MIGRATION.md` | Backup + migration plan |
| `fleet/TASK-PACKETS.md` | Distributed agent goals |
| `scripts/fleet_*.py` | Automation |

## Excellence bar

- Private stays private (no secrets in git; Business/c940-only).  
- Dirty work preserved.  
- Ledger updated when state changes.  
- Crons stay green on C940.  
- Disk free ≥ 80GB target on C940 (currently ~67GB — continue reclaim).  
