# 2026-09-30 — applied AI lab

Grok. YogaBook. Production was rechecked and left as it is. The product record is on a placement-gate pull request, not on `starlight-agent-config` `main`.

## Which repo holds the record

| Role | Repo | What happened |
| :--- | :--- | :--- |
| Product source | `frankxai/starlight-agent-config` | Lab policies and the progress item are on [PR 72](https://github.com/frankxai/starlight-agent-config/pull/72), head `922d94e`, base `agent/grok/repo-placement-gate` at `6e723ea`. Six files. Not merged to `main`. |
| Open door | `frankxai/starlight-agent-config` #73 | https://github.com/frankxai/starlight-agent-config/issues/73 |
| Agentic progress | `frankxai/agentic-ops-hub` | This file. Branch `agent/grok/applied-ai-lab-2026-09-30` from `origin/main` `51c57ba`. |
| Railway note | `frankxai/agentic-ops` #20 | Stays open. Follow-up: https://github.com/frankxai/agentic-ops/issues/20#issuecomment-5911937332 |
| Separate plan | `frankxai/agentic-ops` #94 | C940 Podman LiteLLM and Langfuse. Not this Railway lab. Left open. |
| Control plane | `C:/Users/frank/starlight` (`frankxai/starlight-command`, branch `codex/rova`) | Dirty. The two Postiz files stayed untracked. |

`ops/sessions/2026-09-30.md` is already the placement handover on unmerged [PR 80](https://github.com/frankxai/agentic-ops-hub/pull/80). This slice uses this second file so the two same-day records do not share one path.

`origin/main` of `starlight-agent-config` is `99b1273`. It does not contain `core/tasks/global-progress-ledger.json` or the four lab policy files. The lab branch is 38 commits and about 1727 files ahead of that main. Retargeting PR 72 onto main would publish unrelated history. The ledger was not copied onto main.

The primary hub checkout `C:/Users/frank/starlight/repos/agentic-ops-hub` stays on `agent/hermes/fleet-task-contract-v1`. This file was written in `C:/Users/frank/starlight/worktrees/agentic-ops-hub-applied-ai-lab-20260930`.

## Production

Railway project perceptive-curiosity, rechecked 2026-09-30. No service was started, stopped, redeployed, or given a new variable.

- Langfuse `GET /api/public/health` returned 200, version 3.213.0. `GET /api/public/traces` returned 401.
- LiteLLM has no public domain. ClickHouse has no TCP proxy.
- Langfuse web, Langfuse worker, ClickHouse, Langfuse Postgres, LiteLLM, Redis, capital-P Postgres, and Infisical were SUCCESS and running. MinIO and ParadeDB were stopped. Postgres-B-gc had no deployment status and was left alone.
- Bill: $82.74 spent, $119.28 estimated, hard cap $130, soft cap $75, not over the limit.

## What was not verified

- No trace has been ingested. LiteLLM still has no Langfuse callback keys. The master key was not proven, because SSH on this machine rejects `C:\Users\frank\.ssh\config`.
- No Vercel project env was changed. The Vercel connector is signed out.
- No public LiteLLM URL was created.
- Sites still do not call the lab. That is the intended shape until the key and the publish decision exist.

## Still open

1. Sign in at https://langfuse-web-production-840d.up.railway.app and create a project API key. Do not paste it.
2. Sign the Vercel CLI back in.
3. Say when LiteLLM may be published. It stays private until anonymous model calls are rejected.
4. If the Railway estimate climbs through $125, say so. Do not change the $130 cap. If a crash loop would push the estimate through the cap, stop Langfuse and ClickHouse rather than taking Postiz, n8n, Infisical, and LiteLLM down with them.
