# 2026-10-01 — Langfuse stack stopped

Grok. YogaBook. ClickHouse and the self-hosted Langfuse stack were stopped. Disks stayed. LiteLLM stayed up.

## Which repo holds the record

| Role | Repo | What happened |
| :--- | :--- | :--- |
| Product source | `frankxai/starlight-agent-config` | Stop record is commit `c2154ba` on `agent/grok/repo-placement-gate`. Not on `origin/main`. The follow-up handover clarification is on `agent/grok/infisical-host-2026-09-29`. |
| Open door | `frankxai/starlight-agent-config` #73 | https://github.com/frankxai/starlight-agent-config/issues/73#issuecomment-5922212634 |
| Agentic progress | `frankxai/agentic-ops-hub` | This file. Branch `agent/grok/lab-stop-2026-10-01` from `origin/main` `977d04a`. |
| Railway note | `frankxai/agentic-ops` #20 | Stays open. The 2026-09-30 correction remains https://github.com/frankxai/agentic-ops/issues/20#issuecomment-5911672732. |
| Separate plan | `frankxai/agentic-ops` #94 | C940 Podman LiteLLM and Langfuse. Not this Railway lab. Left open. |

`ops/sessions/2026-09-30.md` is the placement handover. `ops/sessions/2026-09-30-applied-ai-lab.md` is the pre-stop lab note. This file does not rewrite either one.

The primary hub checkout `C:/Users/frank/starlight/repos/agentic-ops-hub` stays on `agent/hermes/fleet-task-contract-v1`. This file was written in the existing worktree `C:/Users/frank/starlight/worktrees/agentic-ops-hub-applied-ai-lab-20260930`. No new worktree was added. C: was about 101 GiB free.

## Production

Railway project perceptive-curiosity, 2026-10-01. Frank named the stop.

- Restart policy NEVER was set on Langfuse web, Langfuse worker, the Langfuse Postgres, and ClickHouse. Their deployments were then removed.
- Two-minute memory after the stop was 0 for those four. A later status read still showed web and worker stopped, and ClickHouse and the Langfuse Postgres with no deployment. LiteLLM, Infisical, Redis, and capital-P Postgres were SUCCESS.
- `GET /api/public/health` on the old public Langfuse host returned 404.
- Volumes stayed attached. MinIO and ParadeDB stayed stopped. Elasticsearch, Temporal, Postiz, n8n, and launchpad were not touched.
- The bill just before the stop was $84.58 spent and $119.17 estimated, hard cap $130, not over the limit. The estimate was not re-read after the stop. It will not drop in the same hour.

## What was not done

- No Langfuse Cloud project key exists here. LiteLLM callbacks were not set. Do not paste a key into chat.
- No Vercel project env was changed. The Vercel connector is signed out.
- No public LiteLLM URL was created. The master key is still unproven because SSH rejects `C:\Users\frank\.ssh\config`.
- Sites still do not call LiteLLM. That stays true until the key and the publish decision exist.
- `origin/main` of `starlight-agent-config` was not moved. It still does not contain the lab policy files.

## Still open

1. Create a Langfuse Cloud project API key. Do not paste it. Do not sign in at the stopped Railway Langfuse URL.
2. Sign the Vercel CLI back in.
3. Say when LiteLLM may be published. It stays private until anonymous model calls are rejected.
4. Elasticsearch is the next cost cut only if Frank names it. Postiz v2.11.3 does not need it. Postiz v2.12 does.
