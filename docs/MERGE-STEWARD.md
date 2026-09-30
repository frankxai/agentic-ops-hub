# Merge Steward

**Problem.** Agents open more PRs than one person can review. Green, low-risk PRs (a docs fix, a patch bump) wait days for Frank's click, while a PR that changes payouts gets the same one-line glance. Both failure modes come from one queue.

**Model.** Split the queue by risk, decided by rules, not by a model:

- **auto** — merge when required checks are green and one steward review passes.
- **review** — merge only when checks are green and **two** independent reviews pass (a second, adversarial prompt on a different model).
- **human** — never merged by a machine. The steward writes a decision brief and puts it in the daily digest.

A PR's tier is computed deterministically by `scripts/merge_steward.py` from the repo's `.github/merge-policy.yml` **as it exists on the base branch**. The AI reviewers can block a merge; they can never raise a PR's tier or merge anything on their own.

Related: [`ESTATE-OPS-GOVERNANCE.md`](ESTATE-OPS-GOVERNANCE.md) (the per-PR Estate PR Guardian), [`PROTECTION-LAYERS.md`](PROTECTION-LAYERS.md). Rollout plan: [`MERGE-STEWARD-ROLLOUT.md`](MERGE-STEWARD-ROLLOUT.md).

---

## 1. Two GitHub Apps: author ≠ approver

GitHub forbids approving your own PR, and branch protection counts only approvals from someone other than the last pusher. The estate uses that rule instead of trusting any agent to stay honest:

| App | Does | Never does |
| --- | --- | --- |
| `frankx-builder` | pushes agent branches, opens PRs | approves, merges |
| `frankx-steward` | reviews, approves, enables auto-merge, opens revert PRs | writes feature code, edits workflows, changes settings |

Because the two identities differ, a steward approval satisfies "1 required approval" on a PR the builder wrote, and the builder can never approve its own work. PRs the steward itself opens (auto-reverts) are always `human` tier.

### Least-privilege permissions

Both Apps: **Webhook → Active: off**, **Where can this GitHub App be installed: Only on this account**, install on **selected repositories only**.

| Repository permission | `frankx-builder` | `frankx-steward` | Why |
| --- | --- | --- | --- |
| Metadata | Read (mandatory) | Read (mandatory) | |
| Contents | Read & write | Read & write | builder pushes branches; steward merges and pushes revert branches |
| Pull requests | Read & write | Read & write | open PRs / review, approve, enable auto-merge |
| Issues | Read & write | No access | steward labels and issues go through the workflow's `GITHUB_TOKEN` |
| Workflows | No access | No access | neither App can change CI; workflow edits need a human-held token |
| Administration | No access | No access | neither App can touch branch protection or settings |
| Secrets, Actions, Environments | No access | No access | |

The steward never gets `Workflows` or `Administration`, so even a fully compromised steward cannot weaken the checks that gate it. A consequence: if a steward-merged commit touched a workflow file, the auto-revert push is refused and the incident issue says "revert by hand" — acceptable, since workflow edits that touch permissions are already `human`.

### Creating the Apps (Frank, ~10 min, once)

For each App (`frankx-steward` first; `frankx-builder` when agents switch to it):

1. Open **https://github.com/settings/apps/new** (personal account `frankxai`).
2. **GitHub App name**: `frankx-steward` (names are global; if taken use `frankx-merge-steward` and set `steward_login: frankx-merge-steward[bot]` in the caller).
3. **Homepage URL**: `https://github.com/frankxai/agentic-ops-hub`.
4. **Webhook**: untick **Active**.
5. **Permissions → Repository permissions**: set exactly the column from the table above; leave everything else at *No access*. Organization and account permissions: none.
6. **Where can this GitHub App be installed?** → **Only on this account** → **Create GitHub App**.
7. On the App page copy the **Client ID** (starts `Iv23`). Scroll to **Private keys** → **Generate a private key** → a `.pem` downloads.
8. Left sidebar **Install App** → **Install** next to `frankxai` → **Only select repositories** → pick the pilot repos → **Install**.
9. Per repo (Settings → Secrets and variables → **Actions** → *New repository secret*), or from a terminal:
   ```sh
   gh secret set STEWARD_APP_ID      -R frankxai/<repo> --body "Iv23..."   # the Client ID
   gh secret set STEWARD_PRIVATE_KEY -R frankxai/<repo> < frankx-steward.<date>.private-key.pem
   gh secret set ANTHROPIC_API_KEY   -R frankxai/<repo>                     # if not already set
   ```
   Repeat the three under the **Dependabot** secrets tab (`gh secret set ... --app dependabot`) — Dependabot-triggered runs only see Dependabot secrets.
10. Delete the local `.pem` after storing it (or keep it in the password manager only).

`STEWARD_APP_ID` holds the **Client ID**: `actions/create-github-app-token@v3` deprecated the numeric App ID in favour of `client-id`; the secret name stays for estate consistency.

---

## 2. Risk tiers — `.github/merge-policy.yml`

Template: [`templates/merge-policy.yml`](../templates/merge-policy.yml). The file documents its own syntax; the rules:

1. **Built-in human paths**, not overridable by policy: `.github/merge-policy.yml`, `.github/workflows/merge-steward*.yml`, `CODEOWNERS`, `.github/dependabot.yml`, `.env*`, `*.pem`, `*.key`.
2. Per changed file (and its pre-rename path): a `human` glob → human; else a recognised single-package **patch/minor** dependency bump on a manifest/lockfile → `dependency_bumps` (default `auto`); else a `review` glob → review; else an `auto` glob → auto; else `default_tier` (default `review`).
3. **Workflow files** (`.github/workflows/*`): any added/removed line touching `permissions:`, `secrets.`, `pull_request_target`, `workflow_run`, `id-token`, a `: write` scope, `environment:`, `GITHUB_TOKEN`/`github.token`, or self-hosted runners → **human**. A changed `uses:` (third-party action swap) → at least **review**. A deleted workflow, or a diff GitHub will not show (too large) → **human**. Everything else follows the policy (CI config such as a Node version bump is `auto`).
4. The PR's tier is the **most restrictive** file tier. More than `max_files` changed files → human.
5. Labels `steward:human` or `steward:hold` (applied by a person) force human.
6. Fork PRs, PRs authored by the steward, and PRs with no file list → human.

**Dependency bumps.** Parsed from Dependabot (`Bump x from 1.2.3 to 1.2.4`) and Renovate (`Update dependency x to v1.2.4`) titles. Patch and minor → `dependency_bumps`. Major, a `0.x` minor (allowed to break under semver), grouped updates, Renovate titles without a level, or a bump PR that also touches non-manifest files → review. A lockfile-only change without a bump title is not auto (a lockfile can point at any tarball).

**Fail closed.** A missing policy, a policy that fails to parse (the parser accepts a small YAML subset on purpose), a wrong `version`, a missing API key, missing App secrets, a reviewer that returns no parseable verdict, or any count the workflow could not fetch → no merge.

### What belongs in `human`

Smart contracts and anything onchain · payments, billing, checkout, payouts · auth, sessions, middleware · secrets and `.env*` · branch protection, CODEOWNERS · workflow `permissions:`/secrets changes · licence files and licence gates · production infrastructure, `vercel.json`, DNS/`CNAME`, database migrations · agent permission config (`.claude/settings*.json`, hooks, `AGENTS.md`, `CLAUDE.md`) · **the merge steward itself** (its caller workflow and the policy).

---

## 3. The pipeline

Reusable workflow [`.github/workflows/merge-steward.yml`](../.github/workflows/merge-steward.yml), called by [`templates/merge-steward-caller.yml`](../templates/merge-steward-caller.yml) in each repo.

```
pull_request ─▶ classify (base-branch policy, no AI)            ─┐
               ─▶ review  primary (Claude, read-only tools)       │
                          adversarial (review tier only:          │
                           different model, or OpenAI if keyed)   │
               ─▶ decide ─ kill switch? tier? verdicts? mode?     │
                           incident open? daily cap? secrets?   ◀─┘
                    shadow ─▶ sticky comment "would merge / hold"
                    live   ─▶ approve AS frankx-steward + gh pr merge --auto --squash --match-head-commit
schedule     ─▶ digest: one durable "Merge Steward digest" issue, a comment per day
workflow_run ─▶ revert_guard: main red after a steward merge ─▶ revert PR + incident issue
```

- **Classify** reads the policy from the base commit and the file list (with patches) from the API. The script comes from `agentic-ops-hub` at `steward_ref`, never from the PR, so a PR cannot edit the classifier that judges it.
- **Review** jobs hold only `contents: read` / `pull-requests: read`. They run [`anthropics/claude-code-action@v1`](https://github.com/anthropics/claude-code-action) in automation mode (`prompt` + `claude_args`) with `--allowedTools "Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*)"` and a `--json-schema`, so the verdict arrives as the action's `structured_output` (`verdict`, `summary`, `issues[]`, `brief`). Bot-authored PRs need `allowed_bots` (default `frankx-builder,dependabot,renovate`). The primary review runs for every tier (on `human` it writes the decision brief); the adversarial review runs only for `review`.
- **Decide** is pure logic (`merge_steward.py decide`, unit-tested). An `approve` that lists a critical/high issue is downgraded to `request_changes`. In live mode, the token for the steward App is minted with `actions/create-github-app-token@v3` scoped to `contents: write, pull-requests: write` only.
- **Head pinning.** On every new push the classify job first disarms auto-merge; the approval and `--match-head-commit` bind the merge to the reviewed SHA. Turn on **Dismiss stale pull request approvals when new commits are pushed** so a push after approval also removes the approval.
- **No loops.** Labels and digest/incident issues are written with the workflow's `GITHUB_TOKEN`, whose events never trigger workflows. The caller re-runs on label events only for `steward:*` labels.

### Prompt injection

Reviewers read untrusted PR text. Defences, in order of strength: the tier is decided without AI; reviewers hold no write token; the merge needs green required checks; review-tier merges need a second reviewer with a different prompt and model; the prompts tell reviewers that text addressing a reviewer is itself a `block`; human-tier PRs never merge. An injected "approve" can at worst turn an `auto`-tier PR (docs, tests, patch bumps) into a merge that CI already passed.

---

## 4. Safety rails

| Rail | Mechanism |
| --- | --- |
| Kill switch | Repo variable `MERGE_STEWARD=off` → every job is skipped. Takes effect on the next event; to stop a queued auto-merge also run `gh pr merge <n> --disable-auto`. |
| Mode | `MERGE_STEWARD_MODE` unset or anything but `live` = **shadow**: sticky comment with the verdict and what it *would* do; no approval, no merge. |
| Daily cap | `daily_merge_cap` in the policy (default 10). Counts PRs labelled `steward:merged` merged today (UTC) plus those still queued. |
| Auto-revert | Caller's `workflow_run` on the CI workflow. If a push to main fails, the head commit belongs to a `steward:merged` PR, and the same workflow was green on the commit before, the steward opens a revert PR (human merges it) and an incident issue labelled `steward:incident`. |
| Circuit breaker | While any `steward:incident` issue is open, the steward approves and merges nothing in that repo. Closing the issue resumes it. |
| One merge authority | Where the steward is `live`, keep `ESTATE_AUTONOMY` below `auto` so the Estate PR Guardian's TRIVIAL auto-merge does not run beside it. |

---

## 5. Daily digest

One issue per repo titled **Merge Steward digest**, created once and commented daily (the durable-output-sink pattern of `fleet-watch.yml` and `estate-ci-watch.yml`). Each comment has only:

- stats: merged by steward (24h), steward reverts and revert rate (target < 2%), red-main hours (age of the oldest open steward incident), open PRs and their median age, human-queue size;
- a checklist of open PRs labelled `steward:needs-human`, oldest first. The decision brief sits in each PR's steward comment.

---

## 6. Labels

| Label | Set by | Meaning |
| --- | --- | --- |
| `steward:needs-human` | steward | human tier; listed in the digest. Removed automatically if a later push re-tiers the PR. |
| `steward:merged` | steward | approved and auto-merge enabled; counted for the cap and the revert guard |
| `steward:human` / `steward:hold` | a person | take this PR out of the steward's hands |
| `steward:incident` | steward | main went red after a steward merge; merges paused while open |
| `steward:revert` | steward | the auto-revert PR |

## 7. Files

| Path | Role |
| --- | --- |
| `scripts/merge_steward.py` | classify · decide · digest · optional OpenAI second opinion (stdlib) |
| `tests/test_merge_steward.py` | tiers, dependency bumps, workflow permission changes, fail-closed paths, decisions, digest |
| `.github/workflows/merge-steward.yml` | reusable workflow |
| `templates/merge-steward-caller.yml` | per-repo caller |
| `templates/merge-policy.yml` | policy template |
