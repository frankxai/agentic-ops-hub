# Arcanea Weekly Proof - 2026-06-26

Status: internal proof packet, read-only against `arcanea-ai-app`

Channel route:

- Decision room: `#brand-arcanea`
- Technical truth room: `#repo-command`
- Executive summary: `#daily-report`
- Receipt room: `#execution-room`

## Executive Signal

Arcanea has visible public life and active product momentum, but it is not yet
clean enough for another public push without a deliberate split decision.

Top signal:

1. `arcanea.ai` and `www.arcanea.ai` both respond with HTTP 200 and title
   `Arcanea(TM) - Creative Intelligence Platform`.
2. Vercel project metadata does not prove that the active `arcanea-ai-app`
   project owns the root custom domain. `arcanea-lobechat-labs` owns
   `lobe.arcanea.ai`; `arcanea-ai-app` lists only Vercel default domains.
3. The latest three `arcanea-ai-app` Vercel deployments are `ERROR` after
   several earlier `READY` deploys. The latest build fails because Vercel
   cannot detect a Next.js dependency from the configured build/root context.
4. The local repo has a large active dirty state across 14 top-level groups.
   Planning files now show at least two meaningful product slices:
   Genesis activation and Creature Atlas.

## Decision Needed

Recommended decision: **SPLIT**.

Treat the current Arcanea work as three lanes, each with its own proof:

- Product launch lane: homepage, creator flows, visual polish, current public
  `arcanea.ai` behavior.
- Genesis lane: `/genesis`, proof ledger, onboarding doctrine, first-session
  experience.
- Creature Atlas lane: `/atlas/creatures`, `/bestiary` redirect, world-engine
  contracts, generated media QA, persistence.

Do not merge these into one launch story until Vercel project/domain ownership
and the dirty-state split are clear.

## Evidence

### Domain

- `https://arcanea.ai` returned HTTP 200.
- `https://www.arcanea.ai` returned HTTP 200.
- Observed title: `Arcanea(TM) - Creative Intelligence Platform`.
- DNS A record observed for root and www: `216.150.1.1`.
- `vercel domains inspect arcanea.ai --scope starlight-intelligence` found the
  domain, but current nameservers do not match Vercel intended nameservers.
- Vercel intended nameservers: `ns1.vercel-dns.com`, `ns2.vercel-dns.com`.
- Current nameservers are IONOS-style `ui-dns` nameservers.

### Vercel

- `arcanea-lobechat-labs` project domains include `lobe.arcanea.ai`.
- `arcanea-ai-app` project domains include:
  - `arcanea-ai-app.vercel.app`
  - `arcanea-ai-app-starlight-intelligence.vercel.app`
  - `arcanea-ai-app-frankx-eth-starlight-intelligence.vercel.app`
- `arcanea-ai-app` latest deployment at 2026-06-26 04:51:47 +02:00 is `ERROR`.
- Two preceding deployments at 2026-06-26 04:50:14 +02:00 and
  2026-06-26 04:46:51 +02:00 are also `ERROR`.
- Last observed `READY` preview in this sample: 2026-06-26 02:17:45 +02:00.
- Latest build log ends with:
  `No Next.js version detected. Make sure your package.json has "next"...`

Likely fix path: inspect Vercel root directory/build settings for
`arcanea-ai-app`, then align Vercel with the actual Next app package before
another deploy attempt.

### Repo

- Repo: `C:\Users\frank\starlight\repos\arcanea-ai-app`
- Branch observed: `codex/arcanea-homepage-world-engine`
- HEAD observed: `eaf954c3` / `Polish Arcanea homepage and production build`
- Dirty-state group count observed:
  - `.agent-harness.json`: 1
  - `.arcanea`: 30
  - `.claude`: 14
  - `.grok`: 4
  - `.visual-qa`: 18
  - `AGENTS.md`: 1
  - `apps`: 24
  - `DESIGN.md`: 1
  - `docs`: 15
  - `packages`: 9
  - `planning-with-files`: 4
  - `scripts`: 1
  - `supabase`: 1
  - `TASTE.md`: 1

Planning files show Genesis Activation and Creature Atlas backlog/changelog
entries. This is more than a simple homepage polish lane.

## Slack Workflow Test

This packet tests the weekly brand-room cadence:

- `#brand-arcanea` gets the decision: split, hold, or ship as one campaign.
- `#repo-command` gets the exact domain/Vercel/repo evidence.
- `#daily-report` gets the concise executive signal.
- `#execution-room` gets the receipt that the proof loop ran.

No public action was taken. No merge, deploy, gateway start, schedule, spend, or
external message was performed.

## Next Safe Actions

1. Confirm whether `arcanea.ai` root should resolve to `arcanea-ai-app`,
   another Vercel project, or a non-Vercel deployment.
2. Fix Vercel root/build settings for `arcanea-ai-app` before another deploy.
3. Split the dirty state into lane-specific PRs or worktrees:
   Genesis, Creature Atlas, homepage/product polish, agent harness/tooling.
4. Keep public/social Arcanea activation gated until there is one current green
   preview or production proof link.

## Slack Receipts

- `#brand-arcanea` decision post:
  `https://frankxintelli-cu22555.slack.com/archives/C0BBUAKTGSD/p1782442973433779`
- `#repo-command` technical proof:
  `https://frankxintelli-cu22555.slack.com/archives/C0BA49F2BRP/p1782442988266099`
- `#daily-report` executive addendum:
  `https://frankxintelli-cu22555.slack.com/archives/C0BBHBAQZMH/p1782442998695569`
- `#execution-room` proof-loop receipt:
  `https://frankxintelli-cu22555.slack.com/archives/C0BB87M571V/p1782443006077779`
