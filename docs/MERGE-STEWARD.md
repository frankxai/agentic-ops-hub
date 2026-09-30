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
- **App token scope:** `pull_requests: write`, `checks: read`, `statuses: read`, and `contents: read` — `contents: write` only when some target is live (merging needs it). Never `workflows`, `administration`, `secrets` or `actions`.
- **Hub-side writes** (incident issues, digest, reading the kill switch) use the hub's own `GITHUB_TOKEN` with `issues: write`.

## 2. One PR, one snapshot, one SHA

For each open, non-draft PR (oldest first, bounded per run):

1. **Resolve once.** `GET /pulls/{n}` → head SHA `H`, base, author (login **and** API `type`), labels.
2. **Snapshot pinned to `H`.** `GET /compare/{base}...{H}` gives files, patches, statuses, rename sources and commits (with signature verification). Tree modes come from `git/trees` walked at `H` and at the merge base, one directory level at a time. No checkout.
3. **Classify** (pure, no AI) → tier + reasons.
4. **Checks** for `H`: every check run completed with success/neutral/skipped and every commit status `success`. No CI reported = pending. Pending → `wait` (no review yet, re-checked next run).
5. **Review** (auto/review tiers, checks green): the reviewers get the snapshot's full diff as text; see §4.
6. **Decide** (pure): kill switch · tier · checks · strict verdicts · mode · open incidents · rolling-24h cap · per-run budget.
7. **Merge (live only)**, re-reading every guard live:
   - kill switch and incidents re-read from the hub; cap recounted from the API;
   - `GET /pulls/{n}` again: head must still be `H`, still open, same base, no auto-merge armed by someone else;
   - `POST /pulls/{n}/reviews` with `event: APPROVE, commit_id: H`;
   - kill switch re-read once more;
   - `PUT /pulls/{n}/merge` with `sha: H` (GitHub refuses if the head moved) and `merge_method: squash`.
   - If the merge does not complete, the steward **dismisses its own approval immediately**. Expected refusals (moved head, not mergeable) → hold and re-queue; anything else is raised, the run fails, and a failure incident opens.
8. **Sticky comment** on the PR (the only write in shadow mode) with tier, reasons, verdicts, reviewed head, steward code SHA. Its first line is a machine marker (`head`, `mode`, `labels` hash, `checks`, `tries`, `final`). The steward trusts a marker only from a comment authored by its own App, and only to *skip* work — never to authorise anything. A PR is re-evaluated on a new push, a label change, a mode change, a checks change, or while its last decision was not final.

**The steward never leaves authority standing.** Every run, in every mode, it lists its own `APPROVED` reviews on open PRs in each target and dismisses them (disabling any auto-merge riding on them). In normal operation there are none — approve and merge happen seconds apart in the same run.

## 3. Risk tiers

Policy file per repo: `merge-steward/policies/<repo>.yml` (template [`_template.yml`](../merge-steward/policies/_template.yml)), referenced from [`merge-steward/targets.yml`](../merge-steward/targets.yml).

**Built-in human, in every repo, not overridable** (case-insensitive, old and new path of renames, deletions included):
`.github/**` (all workflows, actions, CODEOWNERS, dependabot config) · `**/CODEOWNERS` · the steward's own paths (`**/merge_steward*`, `**/merge-steward*`, `**/merge-policy*`, and directories of those names) · agent instructions and config (`**/.claude/**`, `**/CLAUDE*.md`, `**/AGENTS.md`, `**/GEMINI.md`, `**/.cursor/**`, `.cursorrules`, `**/.codex/**`, `**/.gemini/**`, `.mcp.json`, `.agent-harness.json`) · package-manager and git config (`.npmrc`, `.yarnrc*`, `.pnpmfile.cjs`, `pip.conf`, `.gitattributes`, `.gitmodules`, `.husky/**`, `.pre-commit-config.yaml`, `.devcontainer/**`) · `.env*`, `*.pem`, `*.key`.

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

**Dependencies.** A manifest or lockfile change is auto/review only when **all** hold, else human:

- author login is `dependabot[bot]` or `renovate[bot]` **and** the API user `type` is `Bot`; every commit is authored by that bot and signature-verified;
- the PR touches only manifests and lockfiles, and the title names exactly one package (grouped updates → human);
- every changed manifest line is that package's version string (plain semver range; no URL, git, `file:`, `npm:` alias, script, new dependency or source change); versions agree with the title;
- lockfile lines reference only the public registries (`registry.npmjs.org`, `registry.yarnpkg.com`, PyPI, crates.io, the Go proxy) — no `git+`, `file:`, `link:`, `tarball:`, `http://`, other hosts, or registry settings.

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
| Kill switch | Hub variable `MERGE_STEWARD=off` **or** any open hub issue labelled `steward:stop`. The run then dismisses every standing steward approval, disables auto-merge riding on it, and does nothing else. Also re-read immediately before approving and again before merging. |
| Mode | Live only if hub variable `MERGE_STEWARD_MODE=live` **and** the target's `mode: live`. Otherwise shadow: sticky comments only — no labels, approvals, merges, reverts or branches in target repos. |
| Circuit breaker | Any open hub issue labelled `steward:incident` pauses all merges estate-wide. Opened automatically on a failed run or on a steward-caused red main; closing it resumes. |
| Daily cap | Rolling 24h count of PRs whose `mergedBy` is the steward App (GraphQL, type `Bot`) across all targets, against `min(policy daily_merge_cap, global_daily_cap)`. Recounted live right before each merge; runs are serialised (`concurrency: merge-steward`), so the count cannot race. No labels involved. |
| Per-run budgets | `max_merges_per_run`, `max_reviews_per_run`, `max_prs_per_run` in `targets.yml`. |
| Auto-revert (live) | Each run checks each live target's default-branch tip. If it is red, its parent green, and the tip is the merge commit of a PR whose `mergedBy` is the steward App, the steward opens a hub incident and a revert PR built through the API (a commit whose tree is the parent's tree). A human merges the revert. |
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
