# Fleet pass — 2026-10-01

Grok session on the YogaBook. Source prompt: `ops/sessions/2026-10-01-fleet-control-plane.md` on [agentic-ops-hub #84](https://github.com/frankxai/agentic-ops-hub/pull/84), still an open draft. This file does not replace it. Hermes was not stopped. Nothing was force-pushed. Nothing was self-merged. `pr-gate.mjs` was the only legal merge path, and no PR cleared it this pass.

## Open PRs

- Before: REST search `is:pr is:open author:frankxai user:frankxai` returned **432**.
- After: the same search returned **385**.
- Closed here, with a one-line reason: [claude-code-config #17](https://github.com/frankxai/claude-code-config/pull/17) and [#20](https://github.com/frankxai/claude-code-config/pull/20). Both are superseded by draft [#26](https://github.com/frankxai/claude-code-config/pull/26), whose body says it re-lands them on current main.
- The rest of the drop was not this session. GraphQL `gh pr` is rate-limited, so closes went through REST. No mass close. The six stale agentic-ops PRs stay until Frank says close. Voice drafts, FrankX #239, website #724/#725, Dependabot majors, and hub #83 stayed open.

## agentic-ops #81

Head is `c9c1a766b893829e371dc1abdbed5694db8e0b75` on `agent/claude/claude-review-scope`. A later merge already covers the Codex findings on `8078e68`: `opened` is a trigger, drafts stay quiet, the job does not skip on a branch name, and an incomplete run fails instead of counting as a review. Later pushes re-run only when the PR carries the `claude-review` label. Codex replied that code-review usage is exhausted, so it was not pinged again. Copilot's comment is on `233dc62`, not this head. Not signed off. Not merged.

## arcanea-ai-app #466

Fast-forwarded `agent/claude/fix-waitlist-and-404` from `bd9e851419` to `3089cb7866883c4bc1efb97a2a0ca33b7b89c33c`. No force. `supabase/migrations/20260926000001_waitlists.sql` stayed. Product `/api/waitlist` stays on demand capture. Footer subscribe writes `public.subscribers` through `captureEmail`, and a failed insert stays a 503. `node --test apps/web/lib/waitlist/__tests__/capture-email.test.ts` passed (5/5). The PR stays a draft until a different harness signs `3089cb78`. Upstash and `WAITLIST_TOKEN_SECRET` stay with Frank. Comment: https://github.com/frankxai/arcanea-ai-app/pull/466#issuecomment-5923099018

## Production, measured 2026-10-01

- `https://www.arcanea.ai/this-path-should-404-fleet-check` — HTTP 200, body contains `NEXT_HTTP_ERROR_FALLBACK;404`.
- `https://www.arcanea.ai/waitlist` — HTTP 200, same app shell, canonical `/waitlist`.
- `POST https://www.arcanea.ai/api/waitlist` with a non-email — HTTP 400, `success: false`. No address was stored.
- `https://www.frankx.ai/this-path-should-404-fleet-check` — HTTP 404 (`X-Matched-Path: /404`) after the apex 307.
- `https://starlightintelligence.ai/this-path-should-404-fleet-check` — HTTP 404.
- `https://akamoto.io/this-path-should-404-fleet-check` — HTTP 404.
- `https://gencreator.ai/this-path-should-404-fleet-check` — HTTP 404. Linked routes `/pricing`, `/waitlist`, `/create`, `/products`, `/products/kit`, `/founding`, `/ask`, `/studio`, `/sign-in`, `/community` returned 200.

The two Arcanea failures are the body of draft #466. A second chain was not queued on top of that draft. A third production defect, separate from an open PR, was not proven this pass, so no chain file was added under `starlight/queen/chains/`.

## Not landed

- gencreator.ai #115 (`5593390`) and #117 (`212c03b`) are open, not draft, and `mergeable: behind`. Not signed and not merged.
- Hub #84 stays a draft. Its base moved.
- Jules was not given a new task. `jules remote list --session` still shows Awaiting User Feedback on `10254169434191635759` (starlightintelligence.ai) and `1814326469422839011` (starlight-intelligence-web). In progress was under the cap. The review-and-merge pass had not cleared a PR through the gate.

## Still with Frank

Estate push of `starlight`. Arcanea Upstash plus `WAITLIST_TOKEN_SECRET`. Unarchive or drop `arcanea-orchestrator`. Say "close stale" before the six stale agentic-ops PRs move. Revoke the pasted gbrain token. Pick localhost or 127.0.0.1 for the gbrain MCP. Hermes split brain and the `state.db` backups. Agents do not kill Hermes.
