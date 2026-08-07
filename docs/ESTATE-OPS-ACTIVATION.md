# Estate Ops — Activation

The governance in [`ESTATE-OPS-GOVERNANCE.md`](ESTATE-OPS-GOVERNANCE.md) is **off until you turn it on, once, per repo.** That one-time gate is deliberate — it's cost (paid API calls) and security (write access), which are correctly yours. After it, the estate runs itself and only surfaces the digest.

## The one-time setup (per repo)

1. **Merge the rollout PR** (`ci: Estate Ops Governance`) — this only *adds* the workflow file; it does nothing yet.
2. **Set the API key:** `gh secret set ANTHROPIC_API_KEY -R frankxai/<repo>` — without it, only the free risk-classifier runs.
3. **Set the autonomy level:** `gh variable set ESTATE_AUTONOMY -b assist -R frankxai/<repo>`
   - `off` (and unset) — classify + status only, zero cost.
   - `assist` — review, label, fix on `@estate fix` (maintainer comments only). **Recommended default.**
   - `auto` — additionally auto-merges the TRIVIAL tier (green, no sacred paths). Only for low-blast-radius repos. STANDARD still needs a human merge — the review verdict is advisory, not a machine-enforced check.
4. **(Hub only)** In `agentic-ops-hub`, the digest also installs. Optionally set `ESTATE_GH_TOKEN` (org read scope) so it can sweep every repo, and adjust the schedule in `estate-digest.yml`.

## Recommended levels

| Repo class | Level | Why |
|---|---|---|
| Production site (`frankx.ai-vercel-website`) | `assist` | never auto-merge live URLs/pages — L7 |
| Skills / templates / internal packs | `auto` | low blast radius, high volume |
| Core dev repos (`agentic-creator-os`, `FrankX`) | `assist` | reviewed, human merges |

## Roll it out

```bash
# from agentic-ops-hub
node scripts/rollout-ops-governance.mjs            # dry run — shows exactly what it will do
node scripts/rollout-ops-governance.mjs --apply    # opens a DRAFT PR per repo (nothing merges)
```

## Turning it off

`gh variable set ESTATE_AUTONOMY -b off -R frankxai/<repo>` — instant, no redeploy. Or delete the workflow file. Nothing is sticky.

## What you'll actually experience after activation

- PRs get a single sticky status comment and a tier label. Safe ones flow (or wait for your merge on `assist`).
- Real decisions arrive as one line in the **Estate Digest** issue, refreshed on schedule.
- No per-PR pings. No polling. If everything's green, you hear nothing.
