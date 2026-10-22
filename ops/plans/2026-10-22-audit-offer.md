# Agent Setup Audit: the offer spec (draft, 2026-10-22)

Author: Claude Code. Status: **draft for Frank. Nothing here is sent, published, priced or sold.** This repository is public: the file is a working spec, not private. Price, channel and wording are Frank's, and public copy belongs in the FrankX Professional register on its own site, not in this repo (the neutral register here forbids brand calls to action and pricing; see the strategy map). Companions: `2026-10-22-audit-runbook.md` (how the audit is done) and `2026-10-22-strategy-map.md` (where this fits).

## Plain version (the only part a stranger should see; about 120 words)

> You run coding agents (OpenCode and tools built on it) and pay for models through a gateway or your own keys. Three questions are hard to answer from your own setup: what did a task cost and which key paid; could its data have gone to a provider you did not choose; did anyone besides the agent check the change. We have a read-only checklist, and one small script you can read first, that shows whether your **configuration** could answer each question and where it cannot. You apply any fixes yourself. We have run only part of it, on our own setup. We do not promise savings, security certification or compliance. Tested on OpenCode 2.1.2 configuration only.

Everything below is the internal spec behind that paragraph.

## Who it is for

A person or small team that runs **two or more coding agents, at least one of them OpenCode** (oh-my-opencode, "OmO", included), and pays for models through a gateway (one account that forwards your calls to many model providers) or through provider keys they control. This is persona P1 and P2 in the product plan (`2026-10-21-product-prd-ard-funnel.md` section 4.2). It is not yet for organisations that need tenant isolation or a compliance attestation (P3).

**Coverage today.** The checks are built and tested against OpenCode 2.1.2 JSON/JSONC configuration only. For Claude Code and Codex we can look at keys, caps and spend (C1, C7, C8) and, for Claude Code, an `ANTHROPIC_BASE_URL` override in a settings file the inspector can read; routing checks on Codex (TOML) and any other tool are done by hand. We do not claim more.

## The problem

Three questions we could not answer from our own data until we built checks for them (we have not asked anyone else yet; the wording is paraphrased from product plan section 4.1, not from interviews):

1. What did that task cost, and which key paid for it?
2. Could this task's data have left through a provider or model the owner did not choose?
3. Did anyone other than the agent that made the change check it?

**The audit does not answer these for you.** It shows whether your setup could answer each one, and where it cannot.

## What you get

A written findings report on your configuration, produced by a **read-only** review. You apply every fix yourself; we do not change your files or accounts.

- Which routes your configuration allows to endpoints or models you may not have intended (provider endpoint overrides, ambient models, free-tier routes), and whether your launch path actually uses that configuration (on opencode 2.1.2 it did not without `--standalone`). It reads configuration; it does not watch live traffic.
- Whether keys sit in plaintext config, how many exist, what each is capped at, and whether a leaked key has a bounded loss (check C7, from the owner's own dashboard).
- Whether spend is checked **before** a call or only counted afterwards (check C8, by questions; not yet run on anyone).
- Whether your run logs could tell you afterwards which model ran a task and what it cost, and whether "tests passed" was recorded by something other than the agent that did the work.
- Each finding has a severity, the file and setting it refers to, a redacted piece of evidence, and the smallest fix.

An appendix check (C10, verifying signed run receipts) applies only to setups that issue SIS run receipts; today that is only ours, and the verifier is a draft pull request.

**Provenance of the checks.** Each check is a defect class we met in our own system. Most were found by a second AI model from another vendor (OpenAI Codex) reviewing our code: 14 rounds on the routing layer, 5 passes on the receipt verifier. C1 and C7 come from our own registry and use, not from those rounds. The runbook cites each source. We have run only the configuration checks C1 to C3, by script, on our own setup; the rest are not yet run on anyone.

## The disclosure you owe the owner

You run one read-only script of ours (`scripts/audit_inspect.py`, about 100 lines; read it first). It prints setting names, hostnames and provider names. For fields whose names look like secrets it prints only whether the value is written literally or read from an environment variable. It is name-based and can miss a secret stored under an innocent field name. It reads JSON and JSONC; for TOML or YAML it reports the file as unreadable and prints nothing from it.

## What the audit does not claim

- It is not a security certification, a penetration test, or legal advice. It does not make you GDPR-compliant.
- It does not prove a provider's zero-data-retention (ZDR: the provider keeps no copy of your prompts) promise.
- It does not measure model quality, and it does not promise a saving. We have no cost-saving result yet; the experiment that would produce one (EXP-008) has not run (`lab/experiments/EXP-008-oms-vs-omo-vs-bare.json`, status `blocked`).
- A signed receipt shows who signed what, not that its contents are true (`docs/receipts.md` in the Starlight Intelligence System repo, "The rule").
- It reviews configuration and records you show us. It does not run your code or your agents.

## What we need from you

- Written confirmation that you own or are authorised to share the machine and accounts in scope.
- Either a screen-share where you run the read-only commands we give you, or redacted exports of config files. We never ask for key values. Screen-shares are not recorded and no screenshots are taken.
- Your list of gateway keys with names, caps and last-use dates (from your own dashboard).
- Your time for a walkthrough: **unmeasured.** We will time the first three pilots and state the result here.

## Who does the work, and what shape it takes

Frank, or an AI agent following the runbook under his supervision. The product-shaped option is a **self-audit kit** (checklist, inspector, findings template) the owner runs alone. A paid, hourly walkthrough would be consulting and breaks the audit's read-only promise if it grows into "fixes"; we do not offer it. [Frank decides: whether the kit is free and what, if anything, is paid; whether the audit is the first step of using Starlight Receipts.]

## Honest limits

- **Demand is unproven.** No prospect has been asked. This offer exists to test whether the problem is felt strongly enough to pay for.
- **The audit is manual today.** One helper script exists; nothing else is automated.
- **Some of our own fixes are not yet merged.** The router and launcher hardening (PR 377, 14 review rounds, round 14 still CHANGES REQUESTED) and the receipt verifier (SIS PR 481) are open drafts. Until they merge, we describe the defect classes and our fixes as "in review", not as a shipped product.
- **Version-bound findings.** Checks that depend on OpenCode behaviour were verified on opencode 2.1.2 only. We record the version we see.
- **Public verifier does not exist yet.** Run receipts verify with a local command and the issuer's public key. The public site's verify page does not read run receipts (`docs/receipts.md`).
- **A free alternative exists and must be beaten.** People already discuss this on OpenCode's public issue tracker (for example the thread "OpenCode is not private by default?", 83 reactions, measured 2026-10-22 by a reviewer through the GitHub search API, not re-measured here) and can set `small_model` and `enabled_providers` themselves. The audit has to be worth more than that thread plus the docs.

## Price and channel

Price, payment rail and channel are **[Frank decides]** and are deliberately not written in this repository. The product plan names Polar as the merchant of record for products and says no checkout goes live before Polar approves (`2026-10-21-product-prd-ard-funnel.md` section 6.2); whether a service invoice follows that rule is open. Public copy must follow the register boundaries and carry no income promises. Lead with mistakes we found in our own setup, never "your data is leaking".

## Next step: test demand before building anything

1. **Read, no contact.** An agent reads the 20 most-reacted OpenCode issues in two themes (models called without the owner choosing them or privacy; spend surprises) and records only counts: pain, workaround, any money mentioned.
2. **Five private messages.** An agent drafts them; **Frank sends them**, to people he already knows who run OpenCode with a gateway. Nothing is sent by an agent. Ask about past behaviour: when did an agent bill or model choice last surprise you and what did you do; show me which model ran your last task and what it cost; where do your keys live (locations only); what have you already spent in money or hours; what would you expect a written report of this to cost (no anchor from us). The commitment ask: "book 60 minutes this week for a free run; may we use the findings anonymised?" A booked slot is evidence; "sounds useful" is not.
3. **Decide the rule before sending.** *Proposed threshold, not data:* continue only if at least 3 of 5 book within 7 days and at least 2 name a non-zero price without prompting. Otherwise publish the checklist as free content and drop the paid path. Keep counts only; no names or addresses in git.
4. Use the same five as the product plan's "3 design partners by 20 Nov" intake (`2026-10-21-product-prd-ard-funnel.md` section 9), so one ask serves both.
5. A different harness reviews this spec and the runbook before any of it leaves the machine.
