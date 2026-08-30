# Fleet Task Packets — Distributed Agents

**Issued:** 2026-07-16 from C940 control plane (Starlight Swarm / Hermes)  
**Coordination SoT:** `ops/OPS-LEDGER.md`  
**Manifest:** `fleet/clone-manifest.json`

Use these as **self-contained goals** for Hermes profiles, `delegate_task`, Claude Code, Codex, or the Yoga Book machine. Each packet states: role, machine, goal, constraints, verify, report.

---

## Packet 0 — Fleet Orchestrator (this session / agentic-ops)

**Machine:** c940  
**Agent:** Hermes default / agentic-ops  
**Goal:** Maintain fleet control plane, dispatch lanes, update ledger, manage multi-machine expansion.  
**Do:**
1. Keep `fleet/*` and `scripts/fleet_*.py` accurate.  
2. Run inventory + sync; never wipe dirty trees.  
3. Dispatch Packets 1–4; collect summaries into OPS-LEDGER.  
4. Produce Book onboard packet and future-machine template.  
**Verify:** `fleet/last-inventory.json` + `last-sync.json` exist; ledger entry dated today.  
**Report:** Executive status table (machines, dirty, prod blockers).

---

## Packet 1 — C940 Install & Repo Health Auditor

**Machine:** c940  
**Agent:** Hermes (terminal/file/github)  
**Goal:** Verify all required tools and Tier-1/2 clones; safe fetch.  
**Do:**
1. Run `python scripts/fleet_inventory.py --machine c940 --json`.  
2. Run `python scripts/fleet_sync.py --machine c940` (no force).  
3. Flag: missing tools (rclone, docker optional), missing remotes (Business), dirty>50 repos.  
4. List open production risks from dirty prod trees (esp. frankx.ai-vercel-website).  
**Constraints:** No `git reset --hard`, no force push, no delete of dirty work.  
**Verify:** last-inventory + last-sync written; summary counts match reality.  
**Report:** tools OK/MISSING, dirty table, recommended commits (names only).

---

## Packet 2 — Backup & Migration Executor

**Machine:** c940  
**Agent:** Hermes + optional Claude Code  
**Goal:** Operationalize backup posture and Book migration readiness.  
**Do:**
1. Confirm OneDrive path; note free disk.  
2. Check restic/rclone; document install commands if missing.  
3. Ensure control plane changes are ready to commit (agentic-ops fleet/).  
4. Draft exact Book first-boot command list (from BACKUP-MIGRATION.md).  
5. Identify protect-list paths still only local (Business no origin).  
**Constraints:** Do not upload secrets; do not change Infisical without approval.  
**Verify:** BACKUP-MIGRATION checklist advanced; backup_check script runs.  
**Report:** 3-2-1 gaps + next install steps for operator.

---

## Packet 3 — Production Targets Driver (P0/P1)

**Machine:** c940 (content/backend) + handoff to Book for UI  
**Agent:** frankx-prod / github / claude-code  
**Goal:** Advance full production targets with evidence.  
**Priorities:**
1. **P0 R1** FrankX → GenCreator bridge (links, CTAs, hub copy).  
2. **P0** frankx.ai prod hygiene — inventory dirty on `frankx.ai-vercel-website` / prod-sync; do not ship without gate.  
3. **P1** SIS verify / ACOS test status (run health if cheap).  
4. **P1** Railway daily health cron already exists — confirm next fire.  
**Constraints:** REGISTER-BOUNDARIES; no main/prod push without explicit approval.  
**Verify:** Evidence paths, commands run, remaining blockers.  
**Report:** Target status table GREEN/YELLOW/RED + next 3 actions.

---

## Packet 4 — Yoga Book Agent (run ON Book)

**Machine:** yoga-book  
**Agent:** **Hermes default = Grok 4.6 primary** (Codex/Antigravity fallback only)  
**Connection:** **git-bus** is canonical (`fleet/bus/`). Hermes LAN peer optional. Bot `@Hermesyogabookbot`.  
**Goal:** Frontend node; sync + HB. Prefer **refresh** if Book already had agentic-ops (it did — dual ONLINE 2026-08-16).  
**Do (refresh path — preferred):** follow **`fleet/YOGA-BOOK-REFRESH.md`** (pull, inventory, sync, heartbeat, activity, push, Swarm one-liner).  
**Do (cold path — only if agentic-ops missing):**  
1. Install tools (git, gh, node, pnpm, python, hermes).  
2. `gh auth login` as frankxai.  
3. Clone `frankxai/agentic-ops-hub` → `agentic-ops`.  
4. Then same as refresh path + `fleet/YOGA-BOOK-TELEGRAM-ALIGN.md`.  
**Constraints:** No Business clone; no always-on heavy crons; no dual-write dirty C940 mains; never forge c940 HB.  
**Verify:** fresh `fleet/bus/heartbeats/yoga-book.json` age_minutes small on C940 after pull; inventory present.  
**Report:** Swarm `[book] ONLINE …` + OPS-LEDGER.

### Copy-paste Book kickoff prompt (refresh)
See full prompt in `fleet/YOGA-BOOK-REFRESH.md`. Short form:

```
You are Yoga Book frontend agent (yoga-book / Starlight). C940 is backend control plane.
Primary model: Grok 4.6. Codex fallback only. Git-bus is the fleet link (not LAN peer required).
REFRESH (you were already online 2026-08-16): cd agentic-ops && git pull && python scripts/fleet_inventory.py --machine yoga-book && python scripts/fleet_sync.py --machine yoga-book && python scripts/fleet_bus.py heartbeat --status live --notes "Book refresh" && python scripts/fleet_activity.py log --machine yoga-book --agent hermes-book --did "HB refresh" --evidence "fleet/bus/heartbeats/yoga-book.json" --next "FE claim" && git add fleet/ && git commit -m "activity(book): HB refresh" && git push. Swarm: [book] ONLINE …. Frontend lanes agent/book/<scope> only. No Business. No c940 forge. Execute now.
```

---

## Packet 5 — Future Machine Template

**Machine:** `<new-id>`  
**Agent:** assign  
**Goal:** Expand fleet without redesign.  
**Do:**
1. Add machine block to clone-manifest.  
2. Assign repo `on` arrays.  
3. Onboard = Book steps with new id.  
4. Hermes: orchestrator stays on C940; new machine is specialist.  
**Verify:** inventory detects hostname hint.  
**Report:** machine card in estate-registry + ledger.

---

## Packet 6 — Dirty-Tree Steward (parallel, careful)

**Machine:** c940  
**Agent:** github skill / human-in-loop  
**Goal:** Reduce dirty sprawl without data loss.  
**Hot trees (2026-07-16 inventory):**
- frankx.ai-vercel-website ~427 dirty (branch agent/claude/content-integrity-gate)  
- FrankX ~111 dirty  
- Arcanea ~100 dirty  
- agentic-ops fleet docs untracked  
- SIS ~22 dirty  
**Do:** classify commit / stash / worktree / discard-safe; propose PR branches; commit **agentic-ops fleet** first (this control plane).  
**Constraints:** enhance-never-erase; no mass clean of unknown files.  
**Verify:** dirty counts drop on classified trees only.  
**Report:** proposed commit groups.

---

## Dispatch matrix (who runs what)

| Packet | Runner now | Profile / CLI |
| --- | --- | --- |
| 0 Orchestrator | C940 Hermes (this chat) | default |
| 1 Health auditor | C940 subagent | terminal/file |
| 2 Backup/migration | C940 subagent | terminal/file |
| 3 Production | C940 subagent | github/file |
| 4 Yoga Book | **Human starts on Book** | Codex/Hermes |
| 5 Future | On demand | orchestrator |
| 6 Dirty steward | C940 follow-up | github |

---

## Reporting format (all packets)

```
## Packet N — <name>
Machine: ...
Status: GREEN|YELLOW|RED
Evidence: (commands/paths)
Findings: ...
Actions taken: ...
Blocked on: ...
Next: ...
```
