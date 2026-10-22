---
id: opencode-docs-platform-20261022
what: Docs platform for the five estate brands — draft PR #1 open, waiting on Frank's merge/visibility/Vercel/DNS rulings
where: prompt below
owner: opencode
status: open-unverified
note: awaiting a cross-provider adversarial review before the draft PR can go ready; Vercel project and DNS are Frank-gated
updated: 2026-10-23
---

## Prompt

Continue the multi-brand docs platform in `frankxai/docs-platform` (draft PR
#1, branch `agent/opencode/docs-platform`, head `5c83bc2`). The build is done
and locally verified: one Next.js 16.4.2 deployment, five `docs.<brand>` hosts
via `proxy.ts` host routing, content as `content/<brand>/*.mdx` rendered by
Fumadocs v16, agent-native markdown on every page (`.md` suffix and
`Accept: text/markdown`, both rewrite to `/llms.mdx/<brand>/<path>/content.md`
with `Vary: Accept`).

Next session, in order:

1. Run the cross-provider adversarial review of PR #1 (maker ≠ checker —
   reviewer must be a different harness/provider than OpenCode). Read the diff,
   verify the curl sweep claims, probe negotiation edge cases, and record
   findings as review comments.
2. Fix open findings, then `gh pr ready` once review is signed off.
3. Do not merge: Frank rules on PR #1, repo visibility (public or private),
   the Vercel project, and `docs.*` DNS wiring.
4. If Frank approves deployment: create the Vercel project, wire the five
   `docs.*` domains, then re-run the 14-point curl sweep against the preview
   and production URLs from [the session file](../sessions/2026-10-22.md).
