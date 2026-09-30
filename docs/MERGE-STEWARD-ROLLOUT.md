# Merge Steward — rollout

Design: [`MERGE-STEWARD.md`](MERGE-STEWARD.md). Each phase has an exit test; nothing advances on a calendar alone.

## Phase 0 — Frank's setup (~15 min, once)

Agents cannot do these steps: they create credentials, grant permissions, or change settings. **Nothing is added to the target repos** — no workflow, no policy, no secret.

1. **Create the `frankx-steward` GitHub App** (https://github.com/settings/apps/new, account `frankxai`):
   - name `frankx-steward` (if taken, any name works — the workflow reads the App's identity from its token); homepage `https://github.com/frankxai/agentic-ops-hub`; **Webhook: Active off**;
   - **Repository permissions**: Contents *Read & write*, Pull requests *Read & write*, Checks *Read*, Commit statuses *Read*, Metadata *Read*. Everything else *No access* — in particular **no Workflows, Administration, Secrets, Actions, Environments**. No organisation/account permissions;
   - *Only on this account* → Create. Copy the **Client ID** (`Iv23…`); **Generate a private key** (a `.pem` downloads).
2. **Install the App on the pilot repos only**: App page → Install App → `frankxai` → *Only select repositories* → `affiliate-agent-skills`, `arcanea-ai-app`, `frankx.ai-vercel-website`. **Do not install it on `agentic-ops-hub`.**
3. **Create the `merge-steward` environment in agentic-ops-hub**: Settings → Environments → New environment `merge-steward` → Deployment branches and tags → *Selected branches* → add `main`. (Required reviewers: optional; they would gate every 10-minute run, so leave off.)
4. **Environment secrets** (in `merge-steward`, not repository secrets):
   ```sh
   gh secret set STEWARD_APP_ID      -R frankxai/agentic-ops-hub --env merge-steward --body "Iv23..."
   gh secret set STEWARD_PRIVATE_KEY -R frankxai/agentic-ops-hub --env merge-steward < frankx-steward.<date>.private-key.pem
   gh secret set ANTHROPIC_API_KEY   -R frankxai/agentic-ops-hub --env merge-steward
   # optional cross-vendor adversarial review:
   gh secret set OPENAI_API_KEY      -R frankxai/agentic-ops-hub --env merge-steward
   gh variable set MERGE_STEWARD_OPENAI_MODEL -R frankxai/agentic-ops-hub --body "<model>"
   ```
   Delete the local `.pem` afterwards (keep it only in the password manager). Dependabot secrets are not needed: Dependabot PRs never run steward code.
5. **Branch protection on `main` of each pilot repo**: require a PR, **1 approval**, **dismiss stale approvals on new commits**, **require approval of the most recent reviewable push**, required status checks = the repo's CI. Do **not** put `frankx-steward` on any bypass list. Leave "Allow auto-merge" as is — the steward merges directly and refuses to approve a PR someone else armed for auto-merge.
6. **Hub `main` protection** stays as is (Frank merges hub PRs): the steward's code, allow-list and policies can change only through it.
7. Leave `MERGE_STEWARD_MODE` unset (= shadow). Kill switch at any time: `gh variable set MERGE_STEWARD -R frankxai/agentic-ops-hub --body off`, or open a hub issue labelled `steward:stop`.

Until step 4 is done the workflow skips with a notice every run; it has no authority.

## Phase 1 — shadow on 3 repos (1 week)

The steward comments on every PR in the pilots (`👀 … shadow would: merge|hold`, `⏳` waiting for checks, `🧑‍⚖️` human) and posts the daily digest in the hub. It writes nothing else to the target repos.

**Measure agreement** at the end of the week. For each PR closed or merged during the week with a steward comment:

| Steward said | Frank did | Counts as |
| --- | --- | --- |
| would `merge` | merged without further commits | agree |
| would `merge` | requested changes, pushed fixes, or closed | **false approve** |
| would `hold` | requested changes / closed | agree |
| would `hold` | merged as-is | false hold |
| `human` | — | not scored (never automatic) |

```sh
for r in affiliate-agent-skills arcanea-ai-app frankx.ai-vercel-website; do
  gh pr list -R frankxai/$r --state all --search "updated:>=$(date -u -d '7 days ago' +%F) commenter:app/frankx-steward" \
    --json number,state,mergedAt,comments \
    --jq '.[] | {n:.number, state, merged:(.mergedAt!=null), steward:([.comments[].body|select(startswith("<!-- merge-steward"))|split("\n")[1]][0])}'
done
```

**Exit test:** ≥ 20 scored PRs, agreement ≥ 90 %, and **zero false approves on anything that later needed a correctness or security fix**. One false approve of that kind → tighten the policy or prompt and repeat the week.

## Phase 2 — `auto` tier live

In each pilot's hub policy, move the `review` globs under `human`, then set that target's `mode: live` in `merge-steward/targets.yml` (hub PR, Frank merges), then `gh variable set MERGE_STEWARD_MODE -R frankxai/agentic-ops-hub --body live`.

Run two weeks. **Exit test:** revert rate < 2 %, no red-main hour attributable to a steward merge left open > 4 h, human queue not growing.

Then add the remaining repos from the tier map (install the App on each, add a policy + target in shadow, one week each, same exit test).

## Phase 3 — `review` tier live

Restore the `review` globs in the pilot policies. Review-tier PRs now merge when checks are green and both reviews approve.

**Exit test after four weeks:** revert rate still < 2 %, and the review-tier false-approve rate from spot checks (Frank reads 5 steward-merged review-tier PRs a week) is zero for correctness/security defects.

## Metrics (daily digest)

| Metric | Target | Source |
| --- | --- | --- |
| Steward merges | ≤ cap | GraphQL `mergedBy` = steward App, rolling 24h |
| Incidents | 0 open > 4 h | hub issues labelled `steward:incident` |
| Human queue | stable or falling | human-tier PRs across targets |
| Not evaluated | 0 | PRs past `max_prs_per_run` or with a moving head |

**Stop conditions** (kill switch, no discussion needed): two steward incidents in 7 days; any merge of a file that should have been `human` (fix the policy, add a test, resume); a reviewer approving a diff that contained an instruction aimed at the reviewer.

## Proposed tier map

Every policy starts from [`_template.yml`](../merge-steward/policies/_template.yml); built-in protected paths apply everywhere, and only plain-text files (`md`, `txt`, `rst`, `adoc`, `csv`) can ever be `auto`. Per-repo additions:

| Repo | Visibility | `human` additions | `review` | `auto` | Start |
| --- | --- | --- | --- | --- | --- |
| `affiliate-agent-skills` | public | `data/**/affiliate*.json` (skills are already human via the template) | `src/**`, `scripts/**` | `docs/**`, `examples/**`, `**/*.md` | Phase 1 pilot |
| `arcanea-ai-app` | public | `supabase/**`, `apps/web/app/api/**`, `renovate.json` | `apps/**`, `packages/**`, `scripts/**` | `book/**`, `wiki/**`, `docs/**` (plain text only) | Phase 1 pilot |
| `frankx.ai-vercel-website` | public | `app/api/**`, `.vercelignore`, `next.config.*`, `.env*.example` | `app/**`, `components/**`, `lib/**`, `scripts/**` | `content/**`, `docs/**`, `public/images/**`, `**/*.md(x)` | Phase 1 pilot |
| `Starlight-Intelligence-System` | public | `packages/**/receipts/**`, `**/attestation*/**`, `ATTESTATIONS.md`, `site/vercel.json` | `packages/**`, `site/**`, `src/**` | `docs/**`, `vault/**` public notes | after pilot |
| `gencreator.ai` | private | `proxy.ts`, `instrumentation.ts`, `app/api/**`, `sentry.*` | `app/**`, `lib/**`, `packages/**` | `content/**`, `docs/**`, `brand/**`, `design/**` | after Actions billing fixed |
| `agenticincome` | private | `products/**`, `packs/**/license*` | `app/**`, `components/**`, `lib/**` (agents/commands human via template) | `knowledge/**`, `docs/**`, `design/**` | after billing |
| `go-agenticincome` | private | `app/api/**`, `data/**/links*` | `app/**`, `lib/**`, `scripts/**` | `docs/**`, `reports/**`, `design/**` | after billing |
| `agenticpassiveincome` | private | `products/**`, `schemas/**`, pricing experiments | `app/**`, `components/**`, `lib/**` | `knowledge/**`, `docs/**`, `design/**` | after billing |
| `arcanea-onchain` | public | `packages/**/deploy*/**`, `**/Anchor.toml`, `**/programs/**` (contracts already human) | `packages/**` | `docs/**`, `assets/**`, `**/*.md` | after pilot; contracts never leave human |
