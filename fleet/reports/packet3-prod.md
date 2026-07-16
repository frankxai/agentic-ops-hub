# Packet 3 — Production Targets P0/P1 Evidence Audit

**Date:** 2026-07-16  
**Machine:** c940 (DESKTOP-1B4ICID)  
**Scope:** Evidence only — **no deploy, no force push, no main/prod ship**  
**Sources:** `fleet/clone-manifest.json` `production_targets` P1–P6 · `ops/OPS-LEDGER.md` R1 · live git status · `hermes cron list` · repo content search · HTTP probes  
**Constraints honored:** REGISTER-BOUNDARIES (Professional FrankX voice) · no production push

---

## Executive summary

| ID | Target | Priority | Status | One-line |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | frankx.ai production | P0 | **RED** | Live site HTTP 200, but prod clone is heavily dirty + off-main; prod-sync behind origin |
| **P2** | R1 FrankX→GenCreator bridge | P0 | **YELLOW** | R1 still open in ledger, but **not zero links** — footer + 47 blog posts CTAs to gencreator.ai; primary nav still on-site `/gencreator` |
| **P3** | SIS memory substrate | P1 | **YELLOW** | Clone healthy-ish; main diverged (ahead 8 / behind 22); dirty 22; full `verify` not re-run this packet |
| **P4** | ACOS execution layer | P1 | **GREEN** | Clean tree on `feat/v12-open-core`; head hardened post-adversarial review; no health run this packet |
| **P5** | Arcanea product surface | P1 | **YELLOW** | Arcanea dirty 100 on integrate branch; arcanea-platform clean on staging |
| **P6** | Railway estate health | P1 | **YELLOW** | Manifest cron `railway-daily-health-check` **exists & active**; related weekly/monthly crons active; **Railway CLI missing** on host → estate metrics not CLI-verified |

**Overall P0 posture:** Content funnel is live and partially bridged; **shipping hygiene is the hard blocker** (dirty prod tree + branch state). Do not ship without content-integrity gate + clean worktree strategy.

---

## Dirty prod / tier-1 trees (evidence)

| Repo | Path | Branch | Dirty | Ahead/Behind | Head | Prod? |
| :--- | :--- | :--- | ---: | :--- | :--- | :--- |
| frankx.ai-vercel-website | `C:/Users/frank/frankx.ai-vercel-website` | `agent/claude/content-integrity-gate` | **427** | 0 / 0 | `aa8e2229` | **yes** |
| frankx-prod-sync | `C:/Users/frank/frankx-prod-sync` | `main` | **2** | 0 / **17** | `32cf00c9` | **yes** |
| gencreator.ai | `C:/Users/frank/gencreator.ai` | `main` | **1** | 0 / 0 | `1d19755` | **yes** |
| FrankX (authoring, **not** deploy) | `C:/Users/frank/FrankX` | `main` | **111** | **39 / 111** | `9ebb5330` | no |
| Starlight-Intelligence-System | `C:/Users/frank/Starlight-Intelligence-System` | `main` | **22** | 8 / 22 | `d0ed1ee` | no |
| agentic-creator-os | `C:/Users/frank/agentic-creator-os` | `feat/v12-open-core` | **0** | 0 / 0 | `7168d20` | no |
| Arcanea | `C:/Users/frank/Arcanea` | `integrate/agent-native-main-2026-06-12` | **100** | 8 / 31 | `3e1ec71b` | no |
| arcanea-platform | `C:/Users/frank/arcanea-platform` | `staging/madrid-2026-05-25` | **0** | 0 / 0 | `2d8cb93` | no |

Inventory cross-check: `fleet/last-inventory.json` generated 2026-07-16T03:40Z (disk ~86% used, 66 GB free). Matches live `git status` for the above.

**Deploy architecture reminder:** frankx.ai deploys from **`frankx.ai-vercel-website`**, not from `FrankX` (confirmed in FrankX `AGENTS.md`).

---

## P1 — frankx.ai production · **RED**

| Check | Result | Evidence |
| :--- | :--- | :--- |
| Live HTTP | **200** | `curl` → `https://www.frankx.ai/` HTTP 200; `/gencreator` HTTP 200 |
| Clone branch hygiene | **RED** | Working tree on `agent/claude/content-integrity-gate`, not `main`; **427 dirty** (mostly `public/reading/**` + data manifests) |
| Prod mirror | **YELLOW** | `frankx-prod-sync` on `main`, dirty 2 (untracked harness + lockfile), **behind origin 17** |
| Gate | Not re-run | Manifest expects `pnpm build` + merge:gate / predeploy via FrankX sync — **skipped** (audit only; dirty tree unsafe) |
| Ship readiness | **Blocked** | Do not push main/prod until dirty classified + gate green |

**Blockers:** Extreme dirty sprawl on production clone; feature branch checkout; prod-sync lag. Aligns with Packet 6 dirty-steward work.

---

## P2 — R1 FrankX → GenCreator bridge · **YELLOW** (ledger still P0)

### Ledger claim vs evidence

| Source | Claim | Audit finding |
| :--- | :--- | :--- |
| OPS-LEDGER R1 | “40k readers, **zero links** to gencreator.ai” · Linear ARC-204 P0 | **Partially stale.** External product links **do exist** in prod repo content + footer; live homepage HTML contains both `/gencreator` and `https://gencreator.ai` |
| clone-manifest P2 | Blocker: weak bridge links | **Still true for primary conversion path** — mega-nav and hub CTAs mostly **on-site** `/gencreator`, not product domain |

### Bridge signals found

**A. Production repo (`frankx.ai-vercel-website`) — product-domain CTAs**

| Signal | Location | Detail |
| :--- | :--- | :--- |
| Footer external CTA | `components/Footer.tsx:41` | `{ label: 'GenCreator.AI', href: 'https://gencreator.ai', external: true, accent: 'emerald' }` |
| Footer hub (on-site) | `components/Footer.tsx:36` | `GenCreator Hub` → `/gencreator` |
| Blog CTAs | `content/blog/*.mdx` | **47 files**, **126** matches of `https://gencreator.ai` (workflow pillars, best-of, AEO, model routing, etc.) |
| Live HTML | `https://frankx.ai` | Extracted tokens: `/gencreator`, `https://gencreator.ai` |

**B. On-site GenCreator framework (not the product domain)**

| Signal | Location | Detail |
| :--- | :--- | :--- |
| Hub + subroutes | `app/gencreator/**` | Hub, principles, handbook, blueprints, soul, manifesto — all `https://frankx.ai/gencreator…` |
| Nav mega | `components/NavigationMega.tsx` (FrankX; mirrored in prod patterns) | GenCreators section → **`/gencreator`**, not gencreator.ai |
| Command palette | `components/CommandPalette.tsx` | GenCreator Hub / Principles / Handbook → on-site paths |
| Creators product UI | `app/creators/page.tsx`, `components/creators/CreatorsShell.tsx` | “GenCreator OS” pricing/features — on-site funnel |

**C. FrankX authoring repo**

| Signal | Detail |
| :--- | :--- |
| On-site GenCreator system | Strong — full `app/gencreator/**` + nav |
| External `https://gencreator.ai` in UI components/app | **No Footer match** in FrankX `components/Footer.tsx` at audit time; external hits mostly observability snapshots / docs, not primary chrome |
| Implication | Authoring tree and prod tree **may be out of sync** on footer product CTA — sync path matters before treating FrankX main as bridge SoT |

**D. Live product domain**

| URL | HTTP |
| :--- | :--- |
| `https://gencreator.ai/` | **200** |

### R1 residual risk (why not GREEN)

1. Primary chrome (nav mega / hub) steers 40k readers into **on-site framework**, not necessarily the CoE product at gencreator.ai.  
2. Strongest external CTAs sit in **blog mid/end-of-post** blocks — good density, weak homepage/hero placement.  
3. Ledger + Linear still track R1/ARC-204 as open P0 — conversion measurement not evidenced here.  
4. FrankX vs vercel Footer parity gap risks future sync wiping or reintroducing drift.

**Next 3 actions (no ship without approval):**

1. Homepage + article-template **primary CTA** to `https://gencreator.ai` (Professional register).  
2. Align FrankX Footer with vercel Footer external GenCreator.AI link via controlled sync.  
3. Update OPS-LEDGER R1 wording from “zero links” → “weak primary conversion path; blog/footer present.”

---

## P3 — SIS memory substrate · **YELLOW**

| Check | Result |
| :--- | :--- |
| Clone | Present; `main` dirty **22**; **ahead 8 / behind 22** |
| Head | `d0ed1ee` chore(memory): dreaming consolidation |
| Health scripts | `pnpm test` / `npm run verify` exist (heavy full matrix) — **not executed** this packet (audit-only, disk/time) |
| Cron support | Hermes `sis-memory-maintenance` active; last run 2026-07-15 ok |

**Blockers:** Diverged main + dirty WIP (memory-provider, motion, pricing, etc.). Needs classify-then-verify, not blind pull.

---

## P4 — ACOS execution layer · **GREEN**

| Check | Result |
| :--- | :--- |
| Clone | Present; branch `feat/v12-open-core`; **dirty 0** |
| Head | `7168d20` fix: harden v12 after adversarial verification |
| Ledger | F3 🟢 v12 shipped & hardened |
| Health | Scripts present (`build:all`, `typecheck:all`, observatory tests) — **not re-run** this packet |

Cleanest production-adjacent tree in the set. Residual: still on feature branch name vs `main` (confirm whether origin default is this branch).

---

## P5 — Arcanea product surface · **YELLOW**

| Repo | Branch | Dirty | Note |
| :--- | :--- | ---: | :--- |
| Arcanea | `integrate/agent-native-main-2026-06-12` | **100** | Ahead 8 / behind 31 origin/main; large WIP (agent surface, brand, book) |
| arcanea-platform | `staging/madrid-2026-05-25` | **0** | Clean staging handoff commit |

Product surface active but not merge-clean. UI handoff eligible for Yoga Book; backend stay on c940. Mythic register only inside Arcanea trees.

---

## P6 — Railway estate health · **YELLOW**

### Hermes crons (confirmed via `hermes cron list`)

| Name | Schedule | Next run (local) | Status | Workdir |
| :--- | :--- | :--- | :--- | :--- |
| **`railway-daily-health-check`** | `0 7 * * *` | 2026-07-16T07:00:00+02:00 | **[active]** | `C:\Users\frank\FrankX` |
| `railway-queen-weekly-review` | `0 9 * * 1` | 2026-07-20T09:00:00+02:00 | **[active]** | `C:\Users\frank\FrankX` |
| `railway-monthly-rotation-audit` | `0 10 1 * *` | 2026-08-01T10:00:00+02:00 | **[active]** | `C:\Users\frank\FrankX` |

Manifest P6 cron field: **`railway-daily-health-check`** → **exists**.

### Gaps

| Gap | Detail |
| :--- | :--- |
| Railway CLI | Inventory: `railway` **MISSING** on c940 (`WinError 2`) — cannot CLI-confirm frankx-eth project health from this host without install/path fix |
| Last-run fields | Daily railway job listed active with next fire; **last-run success not shown** in the truncated railway block (unlike ops crons that show 2026-07-15 ok) |
| Surface | “Railway frankx-eth projects” — not HTTP-probed here |

**Rating rationale:** Cron **wiring GREEN**, observability **incomplete** without CLI/metrics → overall **YELLOW**.

---

## Cross-cutting risks

| Risk | Severity | Notes |
| :--- | :--- | :--- |
| Dirty prod clone (427) | **P0** | Blocks safe ship; Packet 6 territory |
| FrankX main diverged (39/111) + 111 dirty | High | Authoring drift; do not treat as prod SoT |
| R1 wording stale in OPS-LEDGER | Medium | Update after this packet |
| Disk 86% (was higher earlier) | Medium | R8 monitoring continues |
| Railway CLI missing | Medium | Install or document alternate health path |

---

## Next 3 actions (priority)

1. **Do not ship frankx.ai** until `frankx.ai-vercel-website` dirty work is classified (commit / worktree / discard-safe) and content-integrity gate is green on an intentional branch.  
2. **Close the R1 gap qualitatively:** homepage + nav primary CTA → `https://gencreator.ai`; refresh OPS-LEDGER R1 text; keep blog CTAs.  
3. **P6 hardening:** ensure `railway` CLI on c940 PATH or document job-internal tooling; confirm next `railway-daily-health-check` run leaves a success artifact.

---

## What was explicitly **not** done

- No deploys, merges, force pushes, or `main` production ships  
- No `git reset --hard` / dirty wipe  
- No full `pnpm build` / `npm run verify` / ACOS test matrix (expensive; deferred)  
- No Railway project mutation  

---

## Evidence commands (reproducible)

```bash
# Git dirty (Windows paths)
git -C "C:/Users/frank/frankx.ai-vercel-website" status -sb
git -C "C:/Users/frank/FrankX" status -sb
# …same for other P1–P6 repos

# Bridge search
rg -n "https://gencreator\.ai" "C:/Users/frank/frankx.ai-vercel-website/components/Footer.tsx"
rg -l "https://gencreator\.ai" "C:/Users/frank/frankx.ai-vercel-website/content/blog" --glob '*.mdx' | wc -l

# Live HTTP
curl -sS -o /dev/null -w "%{http_code}\n" -L --max-time 12 https://frankx.ai
curl -sS -o /dev/null -w "%{http_code}\n" -L --max-time 12 https://gencreator.ai

# Crons
hermes cron list
```

**Report path:** `C:/Users/frank/agentic-ops/fleet/reports/packet3-prod.md`  
**Packet complete.**
