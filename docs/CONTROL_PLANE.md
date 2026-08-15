# Control Plane — The Canonical Configuration Hub

> **LOCKED DECISION:** This repository (`frankxai/agentic-ops-hub`) is the canonical configuration control plane. One hub, one cockpit, no competing command centers.

Last updated: 2026-08-15.

---

## The lock

**Problem:** Multiple repos claimed to be "the cockpit" or "the hub," fragmenting configuration and creating confusion about where canonical rules, MCP strategy, ecosystem docs, and agent alignment live.

**Resolution:** The ecosystem now has ONE config plane and ONE desktop cockpit, with supporting repos playing defined roles.

### This is the control plane

**`frankxai/agentic-ops-hub`** (this repo) owns:
- Canonical rule source (`AGENTS.md`) and cross-agent sync
- Ecosystem map (`ECOSYSTEM.md`) — layers, repos, money path
- MCP own-vs-adopt strategy (`docs/MCP-STRATEGY.md`)
- Agent stack and protection layers
- Configuration alignment for the entire fleet
- Live fleet source-of-truth (`fleet/`, `bus/heartbeats`, ops ledger)

This is where all agents look for behavioral instruction, where the ecosystem's architecture is documented, and where fleet state is recorded.

**Naming trap:** The local folder historically named `agentic-ops` remotes to `frankxai/agentic-ops-hub` (this repo). The private remote `frankxai/agentic-ops` is a different sibling (ASPH/protocol spec). Do not treat the private remote as the config plane.

---

## The designated roles

| Repo | Role | What it owns |
|---|---|---|
| **`agentic-ops-hub`** | Config control plane | Rule source-of-truth, ecosystem map, MCP strategy, agent alignment |
| **`starlight-command-center`** | Desktop cockpit | Human-facing dashboard, topology view, stream health UI |
| `agentic-ops` | Supporting (protocol reference) | ASPH protocol spec, governance doc, reference implementation |
| `starlight-agent-config` | Supporting (fleet config) | Git-backed fleet config that feeds the hub |
| `claude-code-config` | Supporting (hooks companion) | Claude Code–specific config and hooks (still in hub clone-manifest) |

### Demoted cockpits

These repos are **no longer cockpits** and should not be used for new control-plane or dashboard work:

- **`hermes-cockpit`** — Hermes-only profile registry, not the fleet desktop
- **`jarvisops-desktop`** — competing native desktop control plane; keep as scanner, not promoted
- **`starlight-command`** — earlier "live cockpit" OS, cooling, name-collides with command-center
- **`starlight-agentic-os`** — public agent-pack "command center", not the operator cockpit
- **`StarlightOS`** — hosted productization shell, not an operator cockpit
- **`awesome-repo-control-plane`** — awesome-* catalog only, not fleet control
- **`frankx-starlight-command`** — portfolio map/catalog, not a running cockpit
- **`frankx-os`** — stale 1-commit public stub

If you're linking to a "command center" or "cockpit," link to **`starlight-command-center`**. Do not create new ones.

### Security note

**`personal-backup-critical`** — private, ~257 MB, description admits credentials/browser/OneNote, last write March 2026. Rotate and take off GitHub.

---

## Do-not list

To keep the control plane singular and the ecosystem aligned:

### ❌ Do NOT:
1. **Create a second hub** — no competing "control plane" or "ops hub" repos
2. **Build a swarm of command centers** — desktop UI goes in `starlight-command-center`, not new repos
3. **Put secrets in git** — no `.env`, API keys, or credentials in `agentic-ops-hub`, `starlight-agent-config`, or any config repo
4. **Fragment the ecosystem map** — `ECOSYSTEM.md` lives here; don't create competing maps in other repos
5. **Fork AGENTS.md without sync** — use the templates + sync engine; don't copy-paste the guardrails into untracked files

### ✅ Do:
1. Edit `AGENTS.md` here when you need to change agent behavior across the fleet
2. Run `node scripts/sync-agent-rules.mjs` to fan rules out to all agent formats
3. Link to this repo's docs when explaining ecosystem architecture
4. Open PRs here for MCP strategy updates, protection-layer changes, or agent-stack revisions
5. Use `starlight-command-center` for any human-facing dashboard or topology UI work

---

## Rationale

**Why one control plane?**
- Configuration drift is expensive: agents diverge, rules conflict, instructions go stale.
- The control plane is a **convergence point**, not a library. It must be singular to function.

**Why not multiple hubs?**
- Every competing hub fragments the truth. Agents read inconsistent rules. Engineers waste cycles reconciling conflicts.

**Why demote instead of delete?**
- History and git archaeology. The demoted repos stay readable, but all new work flows through the locked structure.

**Why no secrets in config repos?**
- Config repos are wired to agent fleets and may be logged, snapshotted, or checked into CI. Secrets belong in vaults, injected at runtime.

---

## If you're building something new

Ask:
- **Is it configuration or alignment for agents?** → Belongs in `agentic-ops-hub` (this repo).
- **Is it a human-facing dashboard or topology view?** → Belongs in `starlight-command-center`.
- **Is it fleet-specific git-backed config data?** → Belongs in `starlight-agent-config`.
- **Is it a new competing cockpit or hub?** → **STOP.** Use the existing one.

When in doubt, open an issue here. The lock is intentional and non-negotiable.
