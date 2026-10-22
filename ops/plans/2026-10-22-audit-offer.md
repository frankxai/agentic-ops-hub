# Agent Setup Audit: the offer (draft, 2026-10-22)

Author: Claude Code. Status: **draft for Frank. Nothing here is sent, published, priced or sold.** Price, channel and wording are Frank's. Companion docs: `2026-10-22-audit-runbook.md` (how the audit is done) and `2026-10-22-strategy-map.md` (where this fits).

> **Sovereign delegation, proven by receipts.** (`lab/goals.json`, north star)

## Who it is for

A person or small team that runs **two or more coding agents** (Claude Code, OpenCode, OmO, Codex and similar) and pays for models through a gateway (one account that forwards your calls to many model providers) or through provider keys they control. This is persona P1 and P2 in the product plan (`2026-10-21-product-prd-ard-funnel.md` section 4.2). It is not yet for organisations that need tenant isolation or a compliance attestation (P3).

## The problem

Three questions the owner of such a setup usually cannot answer from their own data (paraphrased from product plan section 4.1, not from interviews; we have held none):

1. What did that task cost, and which key paid for it?
2. Could this task's data have left through a provider or model they did not choose?
3. Did anyone other than the agent that made the change check it?

## What you get

A written findings report on your configuration, produced by a **read-only** review:

- Where a prompt or credential can reach an endpoint or model you did not intend (provider endpoint overrides, ambient models, free-tier routes, launcher and shim behaviour).
- Whether keys sit in plaintext config, how many exist, what each one is capped at, and whether a leaked key has a bounded loss.
- Whether spend is checked **before** a call is made or only counted afterwards.
- Whether your run records are consistent, and, if you issue signed receipts, whether they verify and whether maker and checker are different parties.
- Each finding has a severity, the file and setting it refers to, a redacted piece of evidence, and the smallest fix.

Every check comes from a defect class we found in our own system during independent review (13 review rounds on our routing layer, 5 on our receipt verifier). The runbook cites each one. So far we have run only the configuration checks (C1 to C3) on our own setup; the rest are not yet run on anyone.

## What the audit does not claim

- It is not a security certification, a penetration test, or legal advice. It does not make you GDPR-compliant.
- It does not prove a provider's zero-data-retention (ZDR: the provider keeps no copy of your prompts) promise. It checks which route your calls take and whether your own controls would enforce the route you intended.
- It does not measure model quality, and it does not promise a saving. We have no cost-saving result yet; the experiment that would produce one (EXP-008) has not run (`lab/experiments/EXP-008-oms-vs-omo-vs-bare.json`, status `blocked`).
- A signed receipt shows who signed what, not that its contents are true (`docs/receipts.md` in the Starlight Intelligence System repo, "The rule").
- It reviews configuration and records you show us. It does not run your code or your agents.

## What we need from you

- Written confirmation that you own or are authorised to share the machine and accounts in scope.
- Either a screen-share where you run the read-only commands we give you, or redacted exports of config files. We never ask for key values.
- Your list of gateway keys with names, caps and last-use dates (from your own dashboard).
- An hour for the walkthrough. [Frank decides: any further time estimate; none has been measured.]

## Who does the work

Frank, or an AI agent following the runbook under his supervision. [Frank decides: which to say, and whether the checklist itself is published free so that the paid part is the walkthrough and fixes.]

## Honest limits

- **Demand is unproven.** No prospect has been asked. This offer exists to test whether the problem is felt strongly enough to pay for. The first step is a small number of conversations, not a billing system.
- **The audit is manual today.** The runbook is followed by a person or an agent. One helper script exists (`scripts/audit_inspect.py`, prints setting names and value classes, never values). Nothing is automated beyond that.
- **Some of our own fixes are not yet merged.** The router and launcher hardening (PR 377) and the receipt verifier (SIS PR 481) are open drafts. Until they merge, we describe the defect classes and our fixes as "in review", not as a shipped product.
- **Version-bound findings.** Checks that depend on OpenCode behaviour were verified on opencode 2.1.2 only. We record the version we see.
- **Public verifier does not exist yet.** Run receipts verify with a local command and the issuer's public key. The public site's verify page does not read run receipts (`docs/receipts.md`).

## Price and channel

Price: **[Frank decides]**. Payment rail: **[Frank decides]**. The product plan names Polar as the rail for products and says no checkout goes live before Polar approves (`2026-10-21-product-prd-ard-funnel.md` section 6.2). Whether a services invoice follows that rule is open.

Channel and voice: **[Frank decides]**. Public copy must follow the register boundaries (see the strategy map) and carry no income promises.

## Next step if Frank agrees

1. Run the audit on our own machine and write up the findings (internal; the runbook has a worked example).
2. Have a different harness review this offer and runbook.
3. Offer it to a few people Frank chooses, free, in exchange for feedback and permission to use the anonymised findings.
