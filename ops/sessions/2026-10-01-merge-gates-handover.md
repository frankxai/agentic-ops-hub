# Handover: merge gates, autonomous merge, agent-native rollout (2026-10-01)

Session: https://claude.ai/code/session_012UAPLSSS7uTwsAKKsmKcp7 · Owner: Frank (`frankxai`)

## Frank's intent (verbatim direction, condensed)

- Every product is agent-native: one core behind a CLI, MCP server, API and plugin. No separate "<Brand> Code" harnesses.
- Agents lead and merge autonomously, but must never rearchitect a homepage, landing page or offer page that already works because they misread him. Protected surfaces are evolved, not replaced.
- Every AI review finding is answered (fixed with a commit, or declined with a reason) before merge. Reviewer provider differs from maker.
- Best-in-class and proven: tests and live verification, not claims.

## What exists now

| Piece | Where | State |
|---|---|---|
| Autonomous merge policy | starlight estate `AGENTS.md` §5e, skill `skills/merge-steward` | in force |
| Protected-surface registry (estate view) | estate `graph/protected-surfaces.graph.json` | in force |
| Surface Guard + Review Gate (reference) | [frankx.ai-vercel-website](https://github.com/frankxai/frankx.ai-vercel-website) `scripts/governance/`, `.github/workflows/{surface-guard,review-gate}.yml`, `.github/protected-surfaces.json` | on main since #820; **required checks on main since 2026-09-30** |
| Gate hardening (10 review rounds) | [frankx#829](https://github.com/frankxai/frankx.ai-vercel-website/pull/829), head `ccb131f`, 41 tests | waits for Frank's `surface-approved` label (gate files are a locked surface), then merge |
| Rollout of the same gates | [gencreator.ai#110](https://github.com/frankxai/gencreator.ai/pull/110), [realityarchitect#42](https://github.com/frankxai/realityarchitect/pull/42), [agenticincome#42](https://github.com/frankxai/agenticincome/pull/42), [gencreator-community#10](https://github.com/frankxai/gencreator-community/pull/10) | synced to #829's code, 41/41 tests each, all threads answered; need a Codex review of the current head with no open P0/P1, then merge |
| agenticincome playbook truth pass | [agenticincome#46](https://github.com/frankxai/agenticincome/pull/46) | merged `ccf8555` |

## How the gates work (read before touching them)

- **Surface Guard** runs on `pull_request_target`: workflow, guard, self-test and registry come from the base branch; the PR head is fetched as a ref and only diffed. It posts commit status `Surface Guard` on the head. A PR touching a protected path needs a brief in its body (`Surface/Kind/Intent/Keeps/Changes/Evidence`, Keeps as `job: explanation;` per job). `rearchitect`, `locked` surfaces and the built-in governance surface also need the `surface-approved` label applied by an approver in the base registry (frankxai). Any new commit withdraws the label.
- **Review Gate** posts status `Review Gate`. Reviewers are exact Bot logins (Codex connector, Copilot, Claude, CodeRabbit). Each finding needs an answer from the PR author or a member; P0/P1 need a fix commit of this PR made after the finding, or `Declined: <30+ chars reason>`. Answers in multi-finding threads or review bodies must quote the finding's title or link it.
- **Threat model** (decided): cooperative agents under the shared `frankxai` identity. Declined as residual risk, concurred by a second provider: forged commit timestamps, fork-PR read-only tokens, status spoofing by PR workflows, races with cancelled runs, evaluator code controlled by the PR. The durable fix is a separate agent GitHub identity (Frank's decision). Do not keep re-litigating these when Codex raises them again; decline with that reason.
- To change gate code: change frankx.ai first (tests in `scripts/tests/governance-gates.test.mjs`), then copy `scripts/governance/*.mjs` and both workflows verbatim to the rollout repos; their test files keep their own registry tests after the marker `test('every protected path matches a tracked file`.

## Blocked on Frank (do not attempt; the harness refuses these as permission grants)

1. `gh pr edit 829 -R frankxai/frankx.ai-vercel-website --add-label surface-approved` (label now exists).
2. npm publishes. Logged in as `frankxai`. Verified ready: `@frankxai/prompt-engine@0.1.0` (6/6 tests, 24 files, 53.4 kB). Still need build + test on a machine with RAM headroom: `@frankxai/mcp-doctor@0.5.0` (registry has 0.4.1), `@frankxai/gencreator@0.1.0` (publish from `GenCreator-OS/cli`, MIT LICENSE present), `@arcanea/starlight-intelligence-system@8.3.0` (registry has 6.0.1). After first publishes, set up npm trusted publishing (OIDC) per repo.
3. Separate GitHub identity for agents.

## Open agent/claude PRs (82 on 2026-10-01)

Run this to get the live list instead of trusting a copy:

```
gh api graphql -f query='query{search(query:"is:pr is:open user:frankxai head:agent/claude",type:ISSUE,first:100){nodes{... on PullRequest{repository{name} number title headRefName isDraft mergeStateStatus updatedAt url}}}}'
```

Priorities, in order:
1. The 5 gate PRs above (land the safety net first).
2. Non-draft, CLEAN or BEHIND PRs with passing CI: arcanea-ai-app#468, #421; arcanea-onchain#4, #5, #6; agentic-ops#81; agentic-ops-hub#78, #81; gencreator.ai#115, #117; starlightintelligence.ai#66; frankx.ai-vercel-website#763; starlight-memory-vault#1.
3. arcanea-platform#33-#42 (seven CI fixes, all UNSTABLE: one shared root cause is likely).
4. Drafts older than 14 days: decide land or close; do not let them rot (estate PR budget is 10 per repo).

Ownership: `arcanea-ai-app` and `starlight-agent-config` are Codex-owned trees; flag findings there, do not push.

---

## Prompt for the next agent (GitHub cloud agent, frontier model)

```
You are the lead engineer continuing Frank's (github: frankxai) autonomous-merge and agent-native programme.
Read first, in order: frankxai/agentic-ops-hub ops/sessions/2026-10-01-merge-gates-handover.md, then
AGENTS.md and CLAUDE.md of every repo before you write in it.

Goal for this run: land the safety net, then drain the PR queue with excellence.

1. Gates. For frankx.ai-vercel-website#829 and the rollout PRs (gencreator.ai#110, realityarchitect#42,
   agenticincome#42, gencreator-community#10): read every unresolved AI review finding on the current head.
   Fix real defects in frankx.ai first with a test, then copy the gate files to the rollout repos and run
   `node --test scripts/tests/governance-gates.test.mjs` in each. Reply on each thread with the fix SHA or
   "Declined: <reason>" (threat-model items in the handover are declined, not reopened), resolve it, and
   request "@codex review". Merge a rollout PR (squash) when CI is green, the Review Gate status is success,
   and the reviewer's latest review of the head has no open P0/P1. Never apply surface-approved yourself.

2. Queue. Take the live list of open agent/claude PRs. For each in the priority order in the handover:
   update from main by merge (not rebase, so cited SHAs stay valid), make CI green, get a review from a
   different provider than the author, answer every finding, merge when the estate policy (AGENTS.md 5e)
   allows. Close a PR only when its change is superseded or wrong, with a comment saying which.

3. Standard. Best-in-class, measured: every change carries a test or a live check. No invented numbers,
   benchmarks or claims on public pages. Protected surfaces (homepage, offer pages, about, capture, brand)
   are evolved with a Surface change brief, never rearchitected. One branch per change: agent/<you>/<scope>.

Report at the end: a table of PRs merged, closed, and still open with the one blocker each, plus anything
that needs Frank (labels, publishes, money, secrets, identity).
```
