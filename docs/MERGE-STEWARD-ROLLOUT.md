# Merge Steward — rollout

Design: [`MERGE-STEWARD.md`](MERGE-STEWARD.md). Each phase has an exit test; nothing advances on a calendar alone.

## Phase 0 — Frank's setup (~15 min, once)

Agents cannot do these steps: they create credentials, grant permissions, or change branch protection.

1. **Create and install `frankx-steward`** — follow *Creating the Apps* in [`MERGE-STEWARD.md`](MERGE-STEWARD.md#creating-the-apps-frank-10-min-once) (steps 1–10). Install it on the three pilot repos: `affiliate-agent-skills`, `arcanea-ai-app`, `frankx.ai-vercel-website`. (~8 min)
2. **Secrets per pilot repo** (Actions *and* Dependabot tabs): `STEWARD_APP_ID` (the Client ID), `STEWARD_PRIVATE_KEY`, `ANTHROPIC_API_KEY`. Optional `OPENAI_API_KEY` plus the caller input `second_opinion_openai_model` for a cross-vendor adversarial review. (~4 min)
3. **Branch protection on `main`** of each pilot repo (Settings → Branches → edit rule, or Rulesets):
   - Require a pull request before merging → **Require approvals: 1** → **Dismiss stale pull request approvals when new commits are pushed** → **Require approval of the most recent reviewable push**.
   - **Require status checks to pass** → select the repo's CI checks.
   - Do **not** add `frankx-steward` to any bypass list.
   (~3 min)
4. **Allow auto-merge** is already on for all nine target repos (checked 2026-09-30).
5. **Merge the caller + policy PR** that an agent opens in each pilot repo (`.github/workflows/merge-steward.yml` from the caller template, `.github/merge-policy.yml` from the tier map below). These PRs are human tier by construction.
6. Leave `MERGE_STEWARD_MODE` unset (= shadow).

Prerequisite: private repos need working Actions billing — the 2026-09 estate audit found private-repo CI blocked. The three pilots are public, so the pilot does not wait on it.

## Phase 1 — shadow on 3 repos (1 week)

The steward comments on every PR (`👀 … shadow would: merge|hold`, or `🧑‍⚖️` for human tier) and files the daily digest. It approves and merges nothing.

**Measure agreement** at the end of the week. For each PR closed or merged during the week that has a steward comment:

| Steward said | Frank did | Counts as |
| --- | --- | --- |
| would `merge` | merged without further commits | agree |
| would `merge` | requested changes, pushed fixes, or closed | **false approve** |
| would `hold` | requested changes / closed | agree |
| would `hold` | merged as-is | false hold |
| `human` | — | not scored (never automatic) |

```sh
# PRs the steward commented on this week, with its verdict line and the outcome
for r in affiliate-agent-skills arcanea-ai-app frankx.ai-vercel-website; do
  gh pr list -R frankxai/$r --state all --search "updated:>=$(date -u -d '7 days ago' +%F) commenter:app/github-actions" \
    --json number,state,mergedAt,comments \
    --jq '.[] | {n:.number, state, merged:(.mergedAt!=null), steward:([.comments[].body|select(startswith("<!-- merge-steward -->"))|split("\n")[1]][0])}'
done
```

**Exit test:** ≥ 20 scored PRs, agreement ≥ 90 %, and **zero false approves on anything that later needed a fix for correctness or security**. One false approve of that kind → tighten the policy or prompt and repeat the week.

## Phase 2 — `auto` tier live

First merge a policy change in each pilot repo that moves the `review` globs under `human` and sets `default_tier: human`, so only `auto`-tier PRs are eligible. Then set `MERGE_STEWARD_MODE=live`.

Run two weeks. **Exit test:** revert rate < 2 %, no red-main hour attributable to a steward merge left open > 4 h, human-queue size not growing.

Then roll the caller + policy to the remaining repos in the tier map (shadow first, one week each, same exit test).

## Phase 3 — `review` tier live

Restore the `review` globs and `default_tier: review` in the pilot policies. Review-tier PRs now merge when checks are green, the primary review approves, and the adversarial review (different model, or OpenAI) approves.

**Exit test after four weeks:** revert rate still < 2 %, and the review-tier false-approve rate from spot checks (Frank reads 5 steward-merged review-tier PRs a week) is zero for correctness/security defects.

## Metrics (in every daily digest)

| Metric | Target | Source |
| --- | --- | --- |
| Revert rate | < 2 % of steward merges | `steward:revert` PRs ÷ `steward:merged` PRs |
| Red-main hours | 0 attributable to the steward; any incident closed < 4 h | age of open `steward:incident` issues; estate-wide red mains stay with `estate-ci-watch` |
| Median open-PR age | falling week over week | open PRs' `createdAt` |
| Human-queue size | stable or falling | open PRs labelled `steward:needs-human` |

**Stop conditions** (set `MERGE_STEWARD=off`, no discussion needed): two steward incidents in one repo within 7 days; any merge of a file that should have been `human` (fix the policy, add a test, then resume); a reviewer approving a PR whose diff contained an instruction aimed at the reviewer.

## Proposed tier map

Every repo starts from [`templates/merge-policy.yml`](../templates/merge-policy.yml) (payments, auth, secrets, infra, licences, agent config, workflows-with-permissions and the steward itself are already `human`). Per-repo additions:

| Repo | Visibility | `human` additions | `review` | `auto` | Start |
| --- | --- | --- | --- | --- | --- |
| `affiliate-agent-skills` | public | `data/**/affiliate*.json` (payout/link data) | `src/**`, `scripts/**`, `skills/**` | `docs/**`, `examples/**`, `tests/**`, `**/*.md` | Phase 1 pilot |
| `arcanea-ai-app` | public | `supabase/**`, `apps/web/app/api/**`, `apps/*/middleware.ts`, `vercel.json`, `renovate.json` | `apps/**`, `packages/**`, `scripts/**` | `book/**`, `wiki/**`, `docs/**`, `prompts/**`, `data/**/*.json`, tests | Phase 1 pilot |
| `frankx.ai-vercel-website` | public | `app/api/**`, `middleware.ts`, `vercel.json`, `.vercelignore`, `next.config.*`, `.env*.example` | `app/**`, `components/**`, `lib/**`, `scripts/**` | `content/**`, `docs/**`, `public/images/**`, `**/*.md`, `**/*.mdx`, tests | Phase 1 pilot (production site: stays review-heavy) |
| `Starlight-Intelligence-System` | public | `packages/**/receipts/**`, `**/attestation*/**`, `ATTESTATIONS.md`, `LICENSING.md`, `site/vercel.json` | `packages/**`, `site/**`, `scripts/**`, `src/**` | `docs/**`, root `*.md` except licences, `vault/**` public notes, tests | after pilot |
| `gencreator.ai` | private | `proxy.ts`, `instrumentation.ts`, `app/api/**`, `sentry.*`, payments/auth dirs | `app/**`, `lib/**`, `packages/**` | `content/**`, `docs/**`, `brand/**`, `design/**`, tests | after Actions billing fixed |
| `agenticincome` | private | `products/**` (pricing), `vercel.json`, `packs/**/license*` | `app/**`, `components/**`, `lib/**`, `agents/**`, `commands/**` | `knowledge/**`, `docs/**`, `design/**`, `data/**/*.json`, tests | after billing |
| `go-agenticincome` | private | `app/api/**`, redirect/affiliate link maps in `data/**/links*` | `app/**`, `lib/**`, `scripts/**` | `docs/**`, `reports/**`, `design/**` | after billing |
| `agenticpassiveincome` | private | `products/**`, `schemas/**` (contract with partners), `experiments/**` touching pricing | `app/**`, `components/**`, `lib/**` | `knowledge/**`, `docs/**`, `design/**`, tests | after billing |
| `arcanea-onchain` | public | **`contracts/**`**, `packages/**/deploy*/**`, `**/*.sol`, `**/Anchor.toml`, `**/programs/**` | `packages/**` (off-chain TS) | `docs/**`, `assets/**`, `**/*.md` | after pilot; contracts never leave human |

A repo's policy PR is itself human tier; Frank merges each one.
