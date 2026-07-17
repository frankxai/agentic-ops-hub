# Repo lanes — who works where (C940 vs Book, private vs public)

**SoT:** this file + `fleet/clone-manifest.json` + `REPO-REGISTRY.md` + `docs/DEVICE-STRATEGY.md`  
**Machine:** C940 = `@lenovostarlightbot` · Book = `@Hermesyogabookbot`  
**Updated:** 2026-07-17

Enhance-never-erase. Parallel lanes — no “you first” deadlock (`fleet/ALIGNMENT.md`).

---

## 1. Machines (default ownership)

| Machine | Role | Engineering focus |
| --- | --- | --- |
| **C940 / Lenovo** | Always-on control plane | Backend, content/GEO, ops, memory, Railway, gates, crons |
| **Yoga Book** | Frontend / innovation | UI/UX, product surfaces, polish, frontend ship assist |

Shared repos are allowed only with **lane splits** (content vs UI, backend vs frontend).

---

## 2. Critical deploy architecture (FrankX)

| Surface | Repo | Visibility | Who | Notes |
| --- | --- | --- | --- | --- |
| **Authoring** | `FrankX` | **Private** | C940 content/GEO · Book UI polish | **Does not deploy** frankx.ai |
| **Production site** | `frankx.ai-vercel-website` | **Public** | C940 gates/policy · Book frontend-ship | Deploys **https://frankx.ai** |
| **Prod mirror** | `frankx-prod-sync` | Public (same remote) | **C940 only** | Sync/mirror worktree |

**Rule:** Public updates to frankx.ai = changes in **prod repo** (or approved sync), not “push FrankX main.”

---

## 3. Control plane & ops (C940 lead)

| Repo / surface | Remote | Visibility | C940 | Book | Engineering |
| --- | --- | --- | --- | --- | --- |
| **agentic-ops (local control plane)** | origin → `frankxai/agentic-ops-hub` (**Public**) · sibling `frankxai/agentic-ops` (**Private**) | dual | **ops-lead** | ops-read | Fleet bus, ALIGNMENT, activity log, OPS-LEDGER, packets. Never publish secrets/private reports to the public hub. |
| **claude-code-config** | `frankxai/claude-code-config` | (check) | **hooks-lead** | consume | Global agent harness / hooks |

---

## 4. Product & content map

| Product | Repo(s) | Visibility | C940 maintains | Book maintains | Public updates land |
| --- | --- | --- | --- | --- | --- |
| **frankx.ai** | FrankX + vercel-website + prod-sync | Private + **Public** | Content, GEO, integrity gate, prod policy | UI components, ship assist | **vercel-website** → frankx.ai |
| **GenCreator / R1** | `gencreator.ai` + FrankX bridge | **Private** product | Backend/content bridge, GEO | Product UI | Product deploy when go-live; CTAs from frankx public site |
| **SIS / Starlight** | `Starlight-Intelligence-System` | **Public** | **memory-lead**, pipelines | light-read | Public GitHub engineering |
| **ACOS** | `agentic-creator-os` | **Public** | **skills-lead**, execution layer | consume | Public GitHub / npm story |
| **Arcanea** | `Arcanea` (`arcanea-ai-app`) | **Private** | mythic-backend, lore ops | platform-ui | Arcanea surfaces when assigned; voice = mythic |
| **arcanea-platform** | `arcanea-platform` | (private-ish) | platform-backend | ui-when-assigned | Platform engineering |
| **AnimeLegends** | `AnimeLegends.ai` | — | backend/content/GEO (satellite) | frontend when claimed | Brand site |
| **VibeClubs** | `vibeclubs.ai` | — | backend/content (satellite) | frontend when claimed | Brand site |
| **library-os** | `library-os` | **Public** OSS | maintain/low-touch | optional | Public OSS |
| **starlight-memory** | `starlight-memory` | **Public** package seed | C940 | optional | Public package |
| **agentic-life-os** | `agentic-life-os` | — | C940 interconnect | rare | Engineering monorepo |
| **Business** | local `Business` | **Local-only / no origin** | **c940 only** sensitive | **never clone** | **No public** |

---

## 5. What *I* (C940 Hermes) default to work on

### Primary (lead & maintain)

1. **agentic-ops-hub** — fleet, bus, activity, alignment, ledger  
2. **FrankX** — content strategy, GEO, bridge copy (private authoring)  
3. **frankx.ai-vercel-website** — prod policy, gates, content integrity (public site)  
4. **SIS** — memory substrate, health  
5. **ACOS** — skills / creator OS  
6. **Railway estate** — health crons (not a single git repo)  
7. **gencreator.ai** — backend/content bridge (private)  
8. **Arcanea** — backend/mythic lane (private)  

### Secondary / when assigned

- arcanea-platform, AnimeLegends, VibeClubs, library-os, starlight-memory, agentic-life-os  
- frankx-prod-sync mirrors  

### Never by default

- Book-only pixel UI without handoff  
- Business on Book  
- Dual-write same dirty tree as Book  

---

## 6. What Book should default to

- UI/UX on **frankx prod**, **GenCreator**, **Arcanea**  
- Branches `agent/book/<scope>`  
- Read agentic-ops; don’t own ops crons  
- No Business  

---

## 7. Private vs public (engineering hygiene)

| Kind | Examples | Rule |
| --- | --- | --- |
| **Private engineering** | FrankX, gencreator.ai, Arcanea app, Business | Secrets, unfinished product, BV — no public dumps |
| **Public product/site** | frankx.ai-vercel-website, SIS, ACOS, library-os | Ship-ready docs/code; no secrets; register boundaries |
| **Private ops control plane** | agentic-ops / agentic-ops-hub mirrors | Fleet queues, activity, budgets — keep private; no secrets in Swarm posts |
| **Public brand updates** | Live sites via Vercel | Only through **prod** repos + gates |
| **Coordination** | OPS-LEDGER, fleet/activity, Swarm | Status OK public-ish; no secrets |

---

## 8. Suggested default work split (this week)

| Priority | C940 | Book |
| --- | --- | --- |
| P0 | frankx prod hygiene + R1 evidence/content | R1/nav UI on `agent/book/*` after pull |
| P0 | agentic-ops bus/activity/alignment | Pull hub; optional yoga-book heartbeat (signal only) |
| P1 | SIS/ACOS health | UI polish claimed surfaces |
| P1 | Railway crons | — |
| P1 | Disk reclaim C940 | Thin Hermes only |

---

## 9. Branch convention

```text
agent/c940/<scope>   # this machine
agent/book/<scope>   # Yoga Book
```

One writer per working tree. Handoff = push + 5 lines OPS-LEDGER or activity log.

---

## 10. Quick answers

| Question | Answer |
| --- | --- |
| Where do I maintain fleet coordination? | **agentic-ops-hub** (public) |
| Where is frankx.ai public engineering? | **frankx.ai-vercel-website** |
| Where is private content authoring? | **FrankX** |
| Where is sensitive BV? | **Business** (C940 only, no origin yet) |
| Where does Book engineer UI? | Prod site / GenCreator / Arcanea UI lanes |
| Do both touch same repo? | Yes, **split lanes** — never same dirty tree |

**Related:** `ALIGNMENT.md`, `STARLIGHT-SWARM-DRIVER.md`, `clone-manifest.json`, `DEVICE-STRATEGY.md`
