# Estate Ops Governance — agent-driven PR & website management

> How every repo in the estate is kept excellent **without a human in the loop at each step** — and without an agent nagging one at every step either. Event-driven, tiered, multi-harness, batched. Agents prepare and fix; a human commits only genuine decisions.

Last updated: 2026-07-09. Composes [`PROTECTION-LAYERS.md`](PROTECTION-LAYERS.md) (L1–L7) and [`CODING_AGENTS_REGISTRY.md`](CODING_AGENTS_REGISTRY.md) (the harness fleet + failure modes).

---

## The problem this fixes

Two failure modes, both real, both observed:

1. **Human-in-every-loop.** Nothing ships unless Frank clicks. The estate doesn't scale past his attention.
2. **Agent-nags-every-step.** The naive fix — an agent that "watches" a PR from a chat session and polls it hourly — just moves the interruption from Git to the inbox. A draft PR that only a human can advance got re-checked 12× with "nothing changed." That is not automation; it is a louder wait.

The correct shape is neither. It is **event-driven CI that acts on real events, fixes what is safe, and surfaces one digest** — so a human touches only the decisions that are genuinely theirs.

---

## The three laws

1. **React to events, never poll.** Work is triggered by a PR event (opened, pushed, CI failed, review comment) or a schedule — never by an agent sitting in a loop asking "changed yet?". CI success, merges, and conflict transitions arrive as events; there is nothing to poll.
2. **Batch, don't nag.** Per-PR status is written **once** and updated **in place** (one sticky comment per PR). Cross-repo state is a **single scheduled digest**, not a message per repo per hour. If nothing is actionable, say nothing.
3. **Agents prepare; humans commit the irreversible.** Everything below auto-fixes, reviews, labels, and can auto-merge the TRIVIAL tier. The [L7 hard-stops](PROTECTION-LAYERS.md#l7--human-gate-last-line) are never delegated.

---

## Autonomy levels (per repo)

Every repo runs at exactly one level, set by the `ESTATE_AUTONOMY` repository variable. Unset behaves as `off` (fail closed); `assist` is the recommended working level. Production websites stay `assist` or `off`.

| Level | Agents may… | Never |
|---|---|---|
| `off` (and unset) | run the free risk-classify + post the sticky status | call any paid agent |
| `assist` (recommended) | review, comment, label, and **fix on request** (`@estate fix`, maintainers only) | merge; push unrequested commits |
| `auto` | additionally **auto-merge the TRIVIAL tier** (green, no sacred paths) | auto-merge STANDARD/HIGH_RISK/BLOCKED, sacred paths, or production-URL changes |

`auto` is opt-in per repo and only appropriate for low-blast-radius repos (skills packs, internal tools). The production site is `assist`.

---

## The tiers (risk-classified, free to compute)

Reuses the proven classifier from `arcanea-ai-app/guardian-pr-check.yml` — diff size + sacred-path touch:

| Tier | Trigger | What runs | Cost cap |
|---|---|---|---|
| 🟢 **TRIVIAL** | ≤5 files, ≤100 deletions, no sacred path (dependabot, typos, docs) | CI only + sticky status; `auto` may merge | $0 |
| 🟡 **STANDARD** | code, <50 files | one domain reviewer (Claude) → verdict; the verdict is advisory (not yet a machine-readable check), so the merge stays with a human even at `auto` | ≤ $0.15 |
| 🟠 **HIGH_RISK** | >50 files **or** a sacred path (`.github/workflows/`, `CLAUDE.md`, `AGENTS.md`, `.claude/`, prod `app/`, URLs) | full review + **escalate to human** (label `estate:needs-human`) | ≤ $1.00 |
| 🔴 **BLOCKED** | >500 files **or** >10k deletions | auto-reject unless a commit carries `BIG-CHANGE:` / `SACRED-DELETE:` | $0 |

Sacred paths always route to HIGH_RISK regardless of size — that is where reputation and irreversibility live.

---

## Multi-harness division of labor

The estate has more than one coding agent for a reason: each has a different strength **and a different failure mode** (from `CODING_AGENTS_REGISTRY.md`). Governance assigns each to the gate it is best at, and pairs it with the check that covers its weakness.

| Gate | Harness | Why it | Its failure mode → the mitigating check |
|---|---|---|---|
| **Correctness / code review** | **Claude Code** (`claude-code-action`) | strongest at deep repo traversal + TDD | context exhaustion, injection from logs → scope-limited to the diff; read-only in review mode |
| **Design / brand / big-context** | **Gemini / Antigravity** (opt-in) | 1–2M context, whole-site visual reasoning | style/output drift → strict rubric prompt + `brand-guidelines` gate; advisory only |
| **Second opinion / security** | **Codex** (opt-in) | fast, cheap divergent read | hallucinates new APIs → never authoritative; used to *dissent*, not approve |
| **Trivial mechanical** | **OpenCode / Codex** | sub-second, near-free | small-context, edge-case misses → confined to TRIVIAL tier only |

Rule: **no single agent both writes and approves.** The harness that fixes is never the harness that green-lights the merge — the reviewer is independent (the fail-closed spine from L5/L6). Second opinions can *block*; they cannot *approve*.

---

## The escalation ladder (what reaches a human)

```
event → classify (free) → [TRIVIAL] CI green? ──auto level──▶ auto-merge
                              │                └─assist level─▶ label estate:ready → digest
                              ├[STANDARD] review+fix → verdict (advisory) ──▶ human merges → digest
                              ├[HIGH_RISK] review → label estate:needs-human ──▶ digest (one line)
                              └[BLOCKED] fail with instructions
```

A human sees exactly one surface: the **estate digest** (below). Everything green and safe flows without them; everything that needs a decision lands as one line in one place. No per-PR pings.

---

## The digest (the one place a human looks)

A single scheduled workflow (`estate-digest.yml`, generalizing the existing `ecosystem-monitor`) sweeps **all** repos and emits one report:

- **Needs you** — PRs labeled `estate:needs-human`, red CI on `main`, merge conflicts. (If empty, the digest is one line: "estate green.")
- **Moving on its own** — auto-merged / auto-fixed since last digest (receipts, not asks).
- **Health** — open PR count, stale branches, oldest un-triaged PR per repo.

Delivered once (daily or weekly) to one channel. **This replaces every per-PR watch.** Nothing polls.

---

## What stays human (never delegated)

Inherited verbatim from [`PROTECTION-LAYERS.md` L7](PROTECTION-LAYERS.md#l7--human-gate-last-line):

- Force-push to `main` of a production repo; deleting/renaming live URLs.
- Editing `/papa/` (family memorial) or other declared-sacred content.
- Moving funds, rotating keys, sending external blasts (newsletter, social).
- Any irreversible action, any spend over cap, any new vendor/rail.

Agents draft and stage these; a human commits. The workflows here **cannot** perform them — the tools don't exist in their scope (L3 IAM).

---

## How it runs (the mechanism)

Two files, distributed to every repo by one script:

1. **`estate-pr-guardian.yml`** — the per-PR event handler: classify → review (Claude) → fix-on-request → one sticky status + labels → conditional auto-merge. Cost-capped, autonomy-gated.
2. **`estate-digest.yml`** — the scheduled cross-repo digest. One report, no nagging.

Rollout: `node scripts/rollout-ops-governance.mjs` (dry-run by default) copies the templates into each target repo's `.github/workflows/`, opening a PR per repo. Nothing activates until that PR is merged **and** `ANTHROPIC_API_KEY` + `ESTATE_AUTONOMY` are set on the repo. See [`ESTATE-OPS-ACTIVATION.md`](ESTATE-OPS-ACTIVATION.md).

---

## Why this is "gentle"

- A human is interrupted **only** by a decision that is genuinely theirs — never by a status.
- Every automated action is reversible, cost-capped, and leaves an audit line (L1).
- The blast radius is bounded per repo by the autonomy level; production is conservative by default.
- The system degrades safely: no key → classify-only; over budget → stop and label, never guess.

Agents run the estate. Humans set the standard and hold the last gate.
