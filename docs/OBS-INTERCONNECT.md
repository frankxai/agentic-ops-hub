# Observability Interconnect — Queen Wave 1-C

**Date:** 2026-09-26 (Europe/Berlin)  
**Seat:** Fleet Steward (plan author)  
**Mission:** Unified Langfuse-class observability interconnect — **not** a new orchestration layer.  
**Control plane (locked):** `frankxai/agentic-ops-hub` (config) + `frankxai/starlight-command-center` (cockpit). No second control plane.  
**Stance:** Fail-closed. No live spend, secrets, deploy, or Cursor on-demand. Pause-new-swarms held — inventory via `gh` read-only only.

---

## Intent (one paragraph)

Wire existing pieces so local CLIs (`cl`, OmO, Codex, `gr`) and cloud agents emit / join the same cost · machine · git-contribution surface. Reuse Phoenix/Langfuse OTLP in `starlight-agentic-os`, Queen `outcome-receipt/v1` + ops ledger in `agentic-ops-hub`, eval receipts in `starlight-evals` / SIS, and the unwired usage-evidence boundary on `starlight-swarm` PR #26 — without inventing a parallel bus or orchestration runtime.

---

## A) Inventory table

| Piece | Exists? | Where | Emits / schema today | Gap |
|---|---|---|---|---|
| **Langfuse / OTel footprint** | **Yes (authored)** | `frankxai/starlight-agentic-os` → `observability/` | Phoenix default (`:6006`); optional Langfuse v3 compose (`docker-compose.langfuse.yml`); `otel.env.example`; `INSTRUMENTATION.md` — OpenLLMetry + native Claude Code OTel (`CLAUDE_CODE_ENABLE_TELEMETRY=1`); resource attrs `service.name=starlight.<cli>.<agent>`, `enduser.id`, pack tags | Runtime bring-up **not evidenced** in-repo (`registry.yaml`: “authored, runtime bring-up not evidenced”). No shared fleet field contract for harness/machine/PR/cost. Sink is swappable; interconnect missing. |
| **starlight-evals** | **Yes (public mirror)** | `frankxai/starlight-evals` | Scorecards with `runId`, lane metrics, latency, named weaknesses; harness scripts `harness/*.mjs`; `SPEC.md` scorecard contract; red/blue Lane 8 receipts PENDING | Origin is SIS `tools/proving-ground/`; mirror does not carry live OTLP. No join key to CLI sessions or swarm usage streams. |
| **llm-evals** | **Yes (private)** | `frankxai/llm-evals` | Description: “local-first multi-LLM evaluation control plane with sterile execution and verifiable receipts” | PAT could not read contents (`403 Resource not accessible`). Treat as **opaque sibling** until Foundations opens read; do not invent its schema here. Prefer `starlight-evals` + SIS schemas for interconnect stubs. |
| **Queen CI/PR receipts** | **Yes** | `frankxai/agentic-ops-hub` | `templates/outcome-receipt.json` → `outcome-receipt/v1` with `receipt_id`, `machine`, `route.{provider,model}`, `resources.{tokens,cost_usd}`, evidence refs, status; live sample `fleet/receipts/rcpt_night_loops_20260806_candidate.json` (`machine: DESKTOP-1B4ICID`, cost often **null**); `ops/OPS-LEDGER.md`; `fleet/CLI-MAX-SWARM.md` mission receipt JSON (`mission_id`, branch, commit, verification) | Cost/tokens often null. No `agent_id` / `harness` / `eval_run_id` / PR number as first-class fields. Ledger is narrative + receipts, not OTLP. |
| **Swarm provider-usage (#26)** | **Yes (OPEN, unwired)** | `frankxai/starlight-swarm` **PR #26** — *feat: authenticate runner lifecycle and provider usage evidence* (branch `codex/runner-start-observation-20260916`) | Fail-closed append-only usage-evidence + remote-stop acknowledgement; head `ac21a184` (CI #181: 398/398 PG17). Explicitly reports **`actual_usage_reconciled: false`**, `released_cost_usd: 0`, `budget_commitment_released: false`. Default provider attestor **denies** all evidence. OpenAI Costs API conformance refuses settlement (aggregate-only). | Queen claim confirmed: **unwired** — no deployed supervisor, no live dispatch, no budget settlement, no provider keys. Not a live cost bus. Hand pilot receipt schema exists (`hands/schema/starlight.hand.pilot-receipt.v1.schema.json`) with `model_cost_usd` but separate from #26. |
| **SIS / shared telemetry docs** | **Yes (partial)** | `frankxai/Starlight-Intelligence-System` | `core/telemetry/hearth/session.schema.json` — `harness` enum (`claude`,`codex`,`gemini`,`opencode`,`antigravity`), tokens, duration; `packages/core/schemas/cost-record.schema.json` — `agentRunId`, kind/amount; foundry evidence/platform-release receipts; cost-plane docs | Harness enum **missing OmO / Grok (`gr`)**; no unified `agent_id`+`machine`+`PR`+`eval_run_id` contract across OTel + receipts + evals. |
| **CLI alias map** | **Yes (docs)** | `agentic-ops-hub` `docs/CODING_AGENTS.md` + `CODING_AGENTS_REGISTRY.md` | Aliases: `cl`=Claude Code, Codex=`cd`/Codex CLI, `gr`=Grok CLI; OmO = writer-only harness per Wave board (HARNESS-MAP: OmO trailer count **0** across sampled repos) | OmO not in Hearth harness enum; attribution stamp gap (Cartographer W1-B). |
| **Control plane lock** | **Yes** | `agentic-ops-hub/docs/CONTROL_PLANE.md` | Hub = config SoT; `starlight-command-center` = cockpit; demotes competing cockpits | Interconnect docs must land **here** (or schema stub in evals) — never a new hub. |

**Verification method (this wave):** box `gh` read-only against frankxai repos (DESKTOP-1B4ICID was connected; inventory used authenticated box `gh`). Did **not** open `personal-backup-critical`. Did **not** launch CloudAgent.

---

## B) One interconnect plan — shared fields

All surfaces (OTLP resource/span attributes, Queen outcome receipts, eval scorecards, future swarm usage joins) MUST speak this **interconnect record** (logical; adapters map native names → these keys):

| Shared field | Type / convention | Source of truth when present | Notes |
|---|---|---|---|
| **`agent_id`** | string | Session/runner id, Hearth `sessionId`, swarm claim/runner id, or `receipt_id` | Stable per run; never a secret. |
| **`harness`** | enum string | CLI alias family | Canonical set for Wave 1-C: `cl` \| `omo` \| `codex` \| `gr` \| `cloud` \| `other`. Map Hearth `claude`→`cl`, `codex`→`codex`, etc. Extend enum only via hub docs PR. |
| **`model`** | string | Provider model id | From `route.model`, OTel gen_ai attrs, or scorecard lane — never invent prices here. |
| **`machine`** | string | Hostname / estate id | e.g. `DESKTOP-1B4ICID`, `c940`, `yoga-book`, `cloud:<provider>`. |
| **`repo`** | string | `owner/name` | GitHub full name; empty only for non-git work (must say so in notes). |
| **`PR`** | string \| null | `owner/name#N` or null | Git contribution join key; null until a PR exists. |
| **`cost`** | decimal string \| null | USD as **exact string** when known | Prefer string (swarm #26 v2 precision lesson). Null + `cost_status=unknown` if unreconciled. **Never** treat null as $0 spent. |
| **`latency`** | number \| null | milliseconds | Span duration, scorecard p95, or mission wall time — name unit in sibling `latency_unit` default `ms`. |
| **`eval_run_id`** | string \| null | starlight-evals / SIS `runId` | Join to scorecards; null when no eval attached. |

### Join graph (no new orchestrator)

```
  cl / OmO / Codex / gr / cloud agent
           │  OTLP resource attrs + optional outcome-receipt/v1
           ▼
  [optional local OTel Collector] ──► Phoenix (default) or Langfuse (heavy)
           │
           │  same field names as attributes / receipt JSON
           ▼
  agentic-ops-hub fleet/receipts + OPS-LEDGER  ←── human/CI attach PR + machine
           │
           ├── starlight-evals scorecards via eval_run_id
           └── starlight-swarm #26 usage stream (read-only join later;
               only when actual_usage_reconciled becomes true under Frank gate)
```

Cockpit (`starlight-command-center`) **reads** hub receipts + published eval mirrors + (later) Langfuse UI links. It does not become a second config plane.

---

## C) How CLIs + cloud agents map (no new orchestrator)

| Emitter | How it maps into shared fields | What it does **not** do |
|---|---|---|
| **`cl` (Claude Code)** | Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` + OTLP → Phoenix/Langfuse per `starlight-agentic-os/observability`. Resource: `harness=cl`, `service.name=starlight.cl.<agent_id>`, `machine`, `repo` from cwd/`git`. On mission end, write/extend `outcome-receipt/v1` with same keys; attach `PR` when opened. | No second launcher; no spend unlock. |
| **OmO** | Writer-only seat (board). Until native OTel exists: stamp git trailers + fill receipt fields `harness=omo`, `agent_id`, `machine`, `repo`, `PR`. Prefer receipt + git contribution over fake cost. | Not a ROUTE/Queen. No Cursor on-demand substitute. |
| **Codex** | Same OTLP pattern when available; else receipt + branch prefix `codex/…`. `harness=codex`, model from exec profile. Swarm #26 work already attributed via `codex/` branches — join by `PR` + `repo`. | Does not settle #26 budget. |
| **`gr` (Grok CLI)** | Alias grid already defined; map `harness=gr`. Emit receipt + optional OTLP when Hermes/xAI path supports it. | Orchestration stays Queen/Hermes — `gr` is craft/CLI, not control plane. |
| **Cloud agents** | `harness=cloud`, `machine=cloud:<provider>`, `agent_id`=provider run id, `PR`/`repo` from gh context. Cost null until provider attestation exists. | Pause-new-swarms: **do not** launch new CloudAgents for this interconnect. |
| **Evals** | Scorecard `runId` → `eval_run_id`; latency from lane metrics; cost only if scorecard records it. | Evals do not dispatch agents. |
| **Swarm #26** | Future: usage evidence rows join on runner/`agent_id` + `repo`. Until `actual_usage_reconciled=true` (Frank-gated), export **observability-only** with `cost=null` and flag `usage_reconciled=false`. | No merge/deploy/settlement in this wave. |

**Attribution glue (already in flight):** Empire Cartographer harness map (`HARNESS-MAP.csv`) supplies git contribution tallies; interconnect consumes those stamps — it does not replace them.

---

## D) Fail-closed rules

1. **No secrets in traces** — never put API keys, tokens, `.env`, webhook secrets, or raw Authorization headers in spans/receipts. Reference `${LANGFUSE_*}`, `${OTEL_*}` only. Redact provider payloads (swarm #26 conformance pattern).
2. **No spend without Frank** — `cost` may be estimated/observed; **budget release, settlement, live billing adapters, and `actual_usage_reconciled=true`** require explicit Frank approval. Null cost ≠ free.
3. **No second control plane** — docs/schema land in `agentic-ops-hub` (and optional eval schema stub). UI only in `starlight-command-center`. Do not promote agentic-os / starlight-command / hermes-cockpit to hub.
4. **No live deploy / Cursor on-demand** — interconnect is docs + optional schema stub + local OTLP pointing; no production Langfuse bring-up, no Railway mutate, no on-demand Cursor spend in this plan.
5. **Unwired stays unwired** — swarm #26 remains non-settling until a separate, reviewed pilot. Interconnect may *document* join keys only.
6. **Fail closed on unknown harness/machine** — prefer `harness=other` + explicit note over silent mis-attribution.
7. **personal-backup-critical** — do not open or reference for credentials.

---

## E) Single next reversible draft PR

| Item | Choice |
|---|---|
| **Owner seat** | **Fleet Steward** (observability interconnect); Foundations consulted for harness enum alignment with Cartographer stamps |
| **Exact repo** | **`frankxai/agentic-ops-hub`** (smallest reversible: docs-only on the locked config plane) |
| **Suggested branch** | `docs/obs-interconnect-shared-fields-20260926` |
| **Suggested title** | `docs: observability interconnect shared-field contract (Wave 1-C)` |
| **What lands** | Single markdown under `docs/OBS-INTERCONNECT.md` (or `docs/observability/SHARED-FIELDS.md`) copying the shared-field table + CLI mapping + fail-closed rules; link from `docs/CONTROL_PLANE.md` § Do list and `fleet/CLI-MAX-SWARM.md` receipt section. **Docs only** — no runtime, no secrets, no CI spend gates flipped. |
| **What it does NOT do** | Does not bring up Langfuse/Phoenix in CI; does not merge swarm #26; does not add provider keys; does not change settlement; does not create a cockpit or orchestrator; does not open llm-evals; does not touch personal-backup-critical; does not launch CloudAgents. |

**Why not starlight-evals first?** Evals already have `runId` scorecards; the missing piece is the **fleet-wide field contract** owned by the control plane. A later Foundations PR can add a JSON Schema stub under `starlight-evals` that `$ref`s the same field names — second step, not first.

**Optional follow-up (out of this draft PR):** Foundations schema stub `starlight-evals/schemas/interconnect-record.v0.json` mirroring the nine fields — still docs/schema-only.

---

## Evidence anchors (read-only)

- Langfuse/OTel: `starlight-agentic-os/observability/{README.md,INSTRUMENTATION.md,docker-compose.langfuse.yml,otel.env.example}`
- Receipts: `agentic-ops-hub/templates/outcome-receipt.json`, `fleet/receipts/rcpt_night_loops_20260806_candidate.json`
- Control plane lock: `agentic-ops-hub/docs/CONTROL_PLANE.md`
- Evals: `starlight-evals/SPEC.md`, scorecard `runId` contract
- Swarm: `frankxai/starlight-swarm` PR **#26** OPEN — quote: *“It remains **unwired**… explicitly reports `actual_usage_reconciled: false` and `released_cost_usd: 0`”* (PR body, checkpoint 2026-09-18, head `ac21a184`)
- Shared telemetry: SIS `core/telemetry/hearth/session.schema.json`, `packages/core/schemas/cost-record.schema.json`

---

Next draft PR: frankxai/agentic-ops-hub#draft docs: observability interconnect shared-field contract (Wave 1-C) — owner Fleet Steward
