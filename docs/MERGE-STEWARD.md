# Merge Steward

**Problem.** Agents open more PRs than one person can review. Green, low-risk PRs (a docs fix, a patch bump) wait days for Frank's click, while a PR that changes payouts gets the same one-line glance.

**Model.** Split the queue by risk, decided by rules, not by a model:

- **auto** — merge when checks are green and one steward review approves.
- **review** — merge only when checks are green and **two** reviews approve (a second, adversarial prompt on a different model or vendor).
- **human** — never merged by a machine. The steward writes a decision brief and lists the PR in the daily digest.

The AI reviewers can stop a merge; they can never lower a tier or merge on their own.

Rollout: [`MERGE-STEWARD-ROLLOUT.md`](MERGE-STEWARD-ROLLOUT.md). Related: [`ESTATE-OPS-GOVERNANCE.md`](ESTATE-OPS-GOVERNANCE.md), [`PROTECTION-LAYERS.md`](PROTECTION-LAYERS.md).

---

## 1. Architecture: one central steward, nothing in target repos

```
agentic-ops-hub (main)                          target repos (allow-listed)
┌──────────────────────────────────────┐        ┌───────────────────────────┐
│ .github/workflows/merge-steward.yml  │        │ no steward workflow        │
│   schedule */10 · workflow_dispatch  │  API   │ no steward policy          │
│   environment: merge-steward (main)  │───────▶│ no steward secrets         │
│ scripts/merge_steward.py             │ App    │ frankx-steward App         │
│ merge-steward/targets.yml            │ token  │   installed (selected repos)│
│ merge-steward/policies/<repo>.yml    │        └───────────────────────────┘
└──────────────────────────────────────┘
```

- **Only the hub runs the steward.** The scheduled job checks out the hub at `github.sha` (immutable for the run; recorded as `hub=<sha>` in every verdict comment), reads the allow-list and the policies from the hub, and walks open PRs through the API with a `frankx-steward` installation token scoped to the listed repos.
- **Target repos hold nothing the steward trusts.** No workflow, no policy, no secret. A PR that rewrites its own repo's workflows gets nowhere near the App key or the classifier; `.github/**` changes are human tier anyway.
- **Secrets live in the hub's `merge-steward` environment**, whose deployment branches are restricted to `main`. A branch that edits the workflow and dispatches it gets no secrets. The job additionally refuses to run outside `frankxai/agentic-ops-hub@main`, and the loader refuses to steward the hub itself.
- **Only current code acts.** A re-run (`GITHUB_RUN_ATTEMPT` > 1) does nothing — re-runs keep their original commit and could resurrect a removed target or a looser policy. A run whose commit is not an ancestor of `main`, or whose steward files (`scripts/merge_steward.py`, `merge-steward/**`, the workflow) differ from `main`, also does nothing; the next scheduled run uses the new code. Unrelated hub commits (bus heartbeats) do not stop a run.
- **App token scope:** every repo the App is installed on (Frank chooses those; the sweep below needs them all, evaluation only touches `targets.yml`), with `pull_requests: write`, `checks: read`, `statuses: read`, and `contents: read` — `contents: write` only when some target is live (merging needs it). Never `workflows`, `administration`, `secrets` or `actions`. The steward's own login is taken from the minted token (`<app-slug>[bot]`), so there is no name to misconfigure; a missing or malformed login stops the run.
- **Hub-side writes** (incident issues, digest, reading the kill switch) use the hub's own `GITHUB_TOKEN` with `issues: write`.

## 2. One PR, one snapshot, one SHA

For each open, non-draft PR (oldest first, bounded per run):

1. **Resolve once.** `GET /pulls/{n}` → head SHA `H`, base, author (login **and** API `type`), labels.
2. **Snapshot pinned to `H`.** `GET /compare/{base}...{H}` gives files, patches, statuses, rename sources and commits (with signature verification). Tree modes come from `git/trees` walked at `H` and at the merge base, one directory level at a time. No checkout.
3. **Classify** (pure, no AI) → tier + reasons.
4. **Checks** for `H`: every check run completed with success/neutral/skipped — and the enumeration must be complete (more than 1000 runs, or fewer listed than `total_count`, counts as failure) — and the **combined** commit-status state `success` (it covers every context, not just the first page). No CI reported = pending. Pending → `wait` (no review yet, re-checked next run).
5. **Review** (auto/review tiers, checks green): the reviewers get the snapshot's full diff as text; see §4.
6. **Decide** (pure): kill switch · tier · checks · strict verdicts · mode · open incidents · rolling-24h cap · per-run budget.
7. **Merge (live only)**, re-reading every guard live:
   - kill switch and incidents re-read from the hub; run freshness re-checked (a policy, target or code change merged to hub `main` during review stops the approval); cap recounted from the API;
   - `GET /pulls/{n}` again: head still `H`, still open, not draft, same base ref **and base SHA**; the PR is **re-classified with its current labels and author** (a `steward:human` label added during review stops it); no auto-merge armed by someone else;
   - checks for `H` re-read: still green;
   - the PR's review count re-read: more than 300 reviews → no approval (the steward's own approval must stay within reach of an oldest-first listing);
   - an **approval ledger** entry is opened in the hub (issue labelled `steward:ledger`, written by the hub workflow's own token, `state=pending`) — if that write fails, nothing is approved;
   - `POST /pulls/{n}/reviews` with `event: APPROVE, commit_id: H`; the ledger entry is updated with the returned review id;
   - kill switch re-read once more;
   - `PUT /pulls/{n}/merge` with `sha: H` (GitHub refuses if the head moved) and `merge_method: squash`.
   - On **every** path that does not end in the steward's own merge — expected refusal, kill switch, timeout, connection error, lost response, any exception — a `finally` block lists the steward's approvals on the PR and dismisses them (and disables any auto-merge riding on them). Expected refusals (moved head, not mergeable) → hold and re-queue; anything else is re-raised, the run fails, and a failure incident opens.
8. **Sticky comment** on the PR (the only write in shadow mode) with tier, reasons, verdicts, reviewed head, steward code SHA. Its first line is a machine marker (`head`, `mode`, `rules` = hash of the repo policy + steward code, `labels` hash, `checks`, `tries`, `final`). The steward trusts a marker only from a comment authored by its own App, and only to *skip* work — never to authorise anything. A PR is re-evaluated on a new push, a label change, a mode change, a policy or steward-code change, a checks change, or while its last decision was not final.

**The steward never leaves authority standing.** Every run, in every mode, it first works through every open ledger entry — whatever the PR's age or state: a merged PR closes the entry; otherwise the recorded review id is dismissed directly (an entry whose id never came back is resolved by a newest-first, author-filtered GraphQL scan of the App's own approvals plus the oldest-first listing), and only then is the entry closed. It then lists its own `APPROVED` reviews on all open PRs and on unmerged PRs closed in the last 30 days, in every repo the App is installed on (so a repo removed from `targets.yml` is still swept), and dismisses them — dismissal first, then disarming any auto-merge riding on them, each step attempted even if another fails; any failure fails the run and opens an incident. In normal operation there are none — approve and merge happen seconds apart in the same run.

**Residuals (accepted, documented).**
- *Review-tier code that CI executes.* Review tier merges ordinary application code by design (two independent model approvals + green checks). Any source file an existing CI job runs (tests, build steps) is therefore reachable by review tier. Target-repo CI holds no steward secret; entry points named like deploy/release/publish, all scripts, composite actions and build files are human; keep production-deploy secrets out of jobs that run on the default branch without a protected environment.
- *Interrupted cleanup.* If withdrawing an approval fails, the run fails and a `steward:incident` pauses the steward; the ledger entry stays open, so every later run retries that exact approval regardless of how old or how closed the PR is. Residual: only someone with write access to the hub repo can close a ledger entry by hand (and so drop it from the sweep); the listing-based sweep (open PRs, PRs closed in the last 30 days) still covers it in that window.
- *Review flooding.* A PR with more than 300 reviews is human tier and is never approved. Because creating reviews is rate-limited, the steward's approval therefore stays within the first few hundred reviews of GitHub's chronological list, which the 5,000-review oldest-first listing always reaches; ledger ids and the author-filtered newest-first scan do not depend on the listing at all.

**Residual window.** GitHub has no atomic approve-and-merge. Between the steward's approval and its merge call (about a second) a person with write access could arm auto-merge or merge `H` themselves. What lands is still exactly the reviewed, checked `H`; what escapes is the kill switch and the cap for that one PR. The approval is withdrawn right after.

## 3. Risk tiers

Policy file per repo: `merge-steward/policies/<repo>.yml` (template [`_template.yml`](../merge-steward/policies/_template.yml)), referenced from [`merge-steward/targets.yml`](../merge-steward/targets.yml).

**Built-in human, in every repo, not overridable** (case-insensitive, old and new path of renames, deletions included):
`.github/**` (all workflows, actions, CODEOWNERS, dependabot config) · `**/CODEOWNERS` · the steward's own paths (`**/merge_steward*`, `**/merge-steward*`, `**/merge-policy*`, and directories of those names) · agent instructions and config — matched against **every path segment**, so a directory covers all its descendants and nested copies count: `.claude/`, `.cursor/`, `.cursorrules`, `.clinerules` (file or directory), `.cline/`, `.windsurf/`, `.windsurfrules`, `.codex/`, `.gemini/`, `.continue/`, `.roo/`, `.roorules*`, `.kilocode/`, `.amazonq/`, `.junie/`, `.agent/`, `.agents/`, `.aider*`, `.augment/`, `.trae/`, `.qwen/`, `.kiro/`, `.opencode/`, `opencode.json*`, `.goose/`, `.goosehints`, `.zed/`, `.rules`, any `AGENTS*`, `CLAUDE*`, `GEMINI*` segment, any `*.mdc`, `.mcp.json`, `mcp.json`, `copilot-instructions.md`, `.github/{instructions,prompts,chatmodes,agents,copilot*}` at any depth; plus `.agent-harness.json` · package-manager and git config (`.npmrc`, `.yarnrc*`, `.pnpmfile.cjs`, `pip.conf`, `.gitattributes`, `.gitmodules`, `.husky/**`, `.pre-commit-config.yaml`, `.devcontainer/**`) · build, deploy and toolchain entry points (`setup.py`, `setup.cfg`, `wrangler.*`, `vercel.json`, `netlify.toml`, `renovate.json*`, `.renovaterc*`, `Makefile`, `*.mk`, `Justfile`, `Taskfile.y*ml`, `Dockerfile*`, `docker-compose*`, `compose.y*ml`, `Procfile`, `.nvmrc`, `.node-version`, `.python-version`, `.tool-versions`, `runtime.txt`, `constraints*.txt`, `CMakeLists.txt`, `*.cmake`, `meson.build`, Bazel `BUILD`/`WORKSPACE`, Gradle, `pom.xml`, Sphinx `conf.py`, composite actions anywhere (`**/action.y*ml`), and any path containing `deploy`, `release` or `publish`) · **every executable script** (`*.sh`, `*.bash`, `*.zsh`, `*.ps1`, `*.psm1`, `*.bat`, `*.cmd`: which of them CI or a deploy runs is repo-specific, so none is machine-merged) · `.env*`, `*.pem`, `*.key`.

**Only plain text can be `auto`.** A file whose extension is not `md`, `txt`, `rst`, `adoc` or `csv` is at least `review` even if an `auto` glob matches it — MDX (executable JSX), SVG/HTML (same-origin script), JSON config, tests, source code. (Build files that happen to end in `.txt` are in the protected list above.) The template also makes agent instructions (`SKILL.md`, `skills/**`, `prompts/**`, `agents/**`, `commands/**`, `.claude-plugin/**`) human.

**Also always human:**

| Condition | Why |
| --- | --- |
| path with a control character, non-NFC unicode, `..`, `\`, leading `/`, empty segment | cannot be matched safely |
| symlink (`120000`) or submodule (`160000`) on either side, or a tree mode the steward could not read | content is elsewhere |
| any file without a patch (binary, too large, pure rename) | reviewers could not see it |
| a file over `max_patch_lines`, or the whole diff over `max_diff_bytes` | reviewers must see all of it — nothing is ever truncated |
| ≥ 300 files (API limit), incomplete compare, or over `max_files` | incomplete list |
| fork PR, base other than the default branch, PR authored by the steward | out of scope |
| label `steward:human` / `steward:hold` (or a policy `human_labels` entry) | a person said so |
| unparseable policy, unknown key, wrong version, missing policy | fail closed |

**Dependencies.** A PR that touches manifests or lockfiles (either side of a rename) is auto/review only when **all** of these hold; otherwise it is human:

- **Identity.** PR author login `dependabot[bot]` or `renovate[bot]` with API user `type: Bot`; exactly one commit; that commit's author is the bot, its committer is `web-flow` (GitHub-signed) and its signature is verified; and every head-branch force-push / delete / restore event on the PR was performed by the bot. (A branch writer can create a `web-flow`-signed commit with a forged author through the contents API, but only by adding a commit or force-pushing — both fail these checks.)
- **Shape.** Only manifests/lockfiles, all modified in place (no renames, adds or deletes), none matching a policy `human` glob. The title names exactly one package (grouped updates → human).
- **Manifests are parsed, not pattern-matched.** `package.json` at the merge base and at `H` is fetched and parsed: the only difference allowed is that package's version in one dependency section, as a plain semver range (no URL, git, `file:`, `npm:` alias; no script, source or new dependency — so a version-shaped script value and JSON-escape tricks fail). `requirements*.txt` and `go.mod` must change exactly one line: that package's pinned version. Other manifest formats → human.
- **Lockfiles.** Only `package-lock.json` **v3** is verified (v2 also carries a legacy `dependencies` tree older npm clients install from → human). It is parsed: no package may appear or disappear, only the bumped package's own entries (`version`, `resolved`, `integrity`, engines/licence/its dependency map) and the root spec for it may change, `resolved` must be exactly `https://registry.npmjs.org/<name>/-/<name>-<version>.tgz`, and the locked version must equal the manifest's new version (and the title's). Every other lockfile (`pnpm-lock.yaml`, `yarn.lock`, `go.sum`, …) → human: a line-level check cannot bind every change to the named package.

Then patch/minor → the policy's `dependency_bumps` (default auto); major, `0.x` minor or unknown → at least review. `dependency_bumps` can only raise the tier (`human` keeps even majors human). A manifest or lockfile changed alongside other files is human: adding or moving a dependency is a human call.

**Policy globs.** Per file the strictest matching list wins (`human` > `review` > `auto`); unmatched → `default_tier`, which never drops below `review`. The PR's tier is its strictest file. Numeric limits are clamped to built-in ceilings. A policy can only make the steward stricter.

## 4. Reviewers and prompt injection

- Reviewers are **plain API calls** — Anthropic Messages (`claude-opus-5` primary, `claude-sonnet-5` adversarial) or, when `OPENAI_API_KEY` and `MERGE_STEWARD_OPENAI_MODEL` are set, OpenAI for the adversarial pass. **No tools, no workspace, no checkout**, so no PR-supplied `.claude/` settings, hooks, `CLAUDE.md` or skills can load. Raw HTTP on purpose: the job holding merge authority installs no packages.
- **Instructions come only from the hub** (`PRIMARY_PROMPT`, `ADVERSARIAL_PROMPT` in the script). The PR (title, file names, diff — including any instruction files, which are human tier anyway) arrives in the user turn between delimiters carrying a fresh random nonce, labelled as untrusted data.
- **Strict verdicts.** Output must be exactly `{verdict ∈ {approve, request_changes}, summary: str, brief: str, issues: [{severity ∈ {critical, high, medium, low}, file: str, detail: str}]}` — requested via JSON-schema output and re-validated. Missing/extra keys, wrong types, unknown enums, invalid or truncated JSON, a non-`end_turn` stop reason (e.g. `max_tokens`, `refusal`) → invalid → no approval. `approve` with a critical/high issue → `request_changes`.
- An invalid verdict is retried on later runs at most 3 times per head, then the hold is final until the author pushes.
- **Residual risk:** a successful injection can at worst turn an `auto`/`review`-tier PR whose checks are green into a merge. Everything that changes authority, CI, dependencies or agent config is human before any model sees it, and review-tier needs two models to be fooled.

## 5. Safety rails

| Rail | Mechanism |
| --- | --- |
| Kill switch | Any open hub issue labelled `steward:stop` — **live**: re-read at run start, immediately before approving, and again before merging. Hub variable `MERGE_STEWARD=off` works too but is read once when the job starts (the job token cannot re-read variables), so it stops the *next* run. Either way the run dismisses every standing steward approval, disables auto-merge riding on it, and does nothing else. For an immediate stop, open the issue. |
| Mode | Live only if hub variable `MERGE_STEWARD_MODE=live` **and** the target's `mode: live`. Otherwise shadow: sticky comments only — no labels, approvals, merges, reverts or branches in target repos. |
| Circuit breaker | Any open hub issue labelled `steward:incident` pauses all merges estate-wide. Opened automatically on a failed run or on a steward-caused red main; closing it resumes. |
| Daily cap | Rolling 24h count of PRs whose `mergedBy` is the steward App (GraphQL, type `Bot`) across all targets, against `min(policy daily_merge_cap, global_daily_cap)`. Recounted live right before each merge; runs are serialised (`concurrency: merge-steward`), so the count cannot race. No labels involved. |
| Per-run budgets | `max_merges_per_run`, `max_reviews_per_run`, `max_prs_per_run` in `targets.yml`. |
| Auto-revert (live) | Each run checks each live target's default-branch tip. If it is red, the steward walks back (up to 20 commits) to the last green commit; if any commit in that red stretch is the merge commit of a PR whose `mergedBy` is the steward App, it opens a hub incident (pausing all merges). When the red tip itself is the steward's merge and its parent is green, it also opens a revert PR built through the API (a commit whose tree is the parent's tree); otherwise the incident says to revert by hand. A human merges any revert. |
| Fail loudly | Unexpected API errors are raised, the run fails, and a `steward:incident` issue opens (deduplicated). Missing App secrets = the job skips with a notice (no authority, nothing to do). |
| One merge authority | Where a repo is live, keep `ESTATE_AUTONOMY` below `auto` so the Estate PR Guardian's TRIVIAL auto-merge does not run beside it. |

## 6. Daily digest

At 06:17 UTC (or `workflow_dispatch` with `digest: true`) the run posts to one hub issue identified by the hidden marker `<!-- merge-steward-digest -->` **and** author `github-actions[bot]` (never by title): merges by the steward (24h), open incidents, PRs seen, the human queue across all targets oldest first, and PRs not evaluated this run. Open PRs are paginated fully.

## 7. Files

| Path | Role |
| --- | --- |
| `.github/workflows/merge-steward.yml` | the only steward runtime |
| `scripts/merge_steward.py` | classify · verdicts · decide · API snapshot · merge · revert guard · digest (stdlib) |
| `merge-steward/targets.yml` | allow-list, modes, estate-wide limits |
| `merge-steward/policies/*.yml` | per-repo tiers (`_template.yml` documents the rules) |
| `tests/test_merge_steward.py` | tier floors and every audited bypass, strict verdicts, decisions, and the run against a fake GitHub (TOCTOU, revocation, shadow writes, cap, digest, revert attribution) |

Changing any of these is a hub PR that Frank merges; the hub is never stewarded.
