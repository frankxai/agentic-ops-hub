# Arcanea migration: independent Crown audit

Date: 10 October 2026. Reviewer: Codex, independently reviewing Antigravity's documents. Verdict: hold bulk transfers. The organization split is reasonable; the claim that it is the best possible execution is unsupported.

## Evidence scope

Read the ecosystem handover, ARD, security framework and strategy artifact identified by Frank. Ecosystem source is `2ec0b74b61464f35430d55432316fea46c8d4056`; its handover is an untracked file, so that commit does not contain the handover. Instruction and document hashes are retained in the private review receipt. Also inspected Antigravity's separate hub worktree: its session, ledger and prompt updates exist there, but are absent from the primary hub checkout. Local worktree persistence does not establish integration into main.

Reviewed router `1851d7f`, Studio `096e127`, and Claw provenance `4040a066b98ca2048f6a190ada7c97b3b5c2aa27`. This review establishes the observations below, not production acceptance or completion of their existing implementation issues.

## Verified organization state

The authenticated GitHub CLI identity is `frankxai`. Both `Arcanea-Labs` and `Starlight-Intelligence` report plan `free` and active membership role `admin` for this identity. Both have organization-scoped budgets of $0 with `prevent_further_usage: true` for Actions, Packages, Codespaces and Git LFS. Those settings were read, not changed. This verifies these particular budget controls, not zero total estate spend.

Arcanea-Labs base repository permission is `none`; Starlight-Intelligence base permission is `read`. The latter grants ordinary members broad read access and should be considered before moving private control-plane repositories. No permissions were changed.

`Arcanea-Labs/Arcanea` already exists, with HEAD `8d7b446aad051fd4beb6397c760d3791a19163bd`. `frankxai/arcanea` has a different HEAD, `f4b598dd07adcdc8ab81ed33eff53f90985cfce0`. GitHub repository names are case insensitive; changing capitalization will not resolve the collision. Compare histories, accepted product ownership and deployments before selecting a destination. Do not overwrite, delete or archive either repository to clear the name.

`Arcanea-Labs/Starlight-Intelligence-System` also exists. The destination `Starlight-Intelligence/Starlight-Intelligence-System` returned 404 for this owner-authenticated request. Reconcile the existing Arcanea-Labs repository with the personal source before any transfer. Starlight-Intelligence's repository listing returned no entries at inspection.

The live personal router and Claw repositories are archived, while their local implementation branches remain available. The private `frankxai/arcanea-agent-skills` repository requires a private-feature review before transfer. Preserve all unfinished implementations.

## Corrections required

| Claim in source | Finding and correction |
|---|---|
| Free organizations permanently guarantee $0 total cost | Free is the current base plan. Metered products, hosting, model inference and object storage are separate. Future prices cannot be guaranteed. |
| Free organizations include native branch protection without qualification | Public repositories support it; transferring a private repository to Free loses protected branches and private Pages. Personal Pro does not confer its private-repository features on an organization. Inspect required-review/ruleset dependencies before transferring. |
| All harnesses inherit administrative access from local gh | Only this CLI identity and its two memberships were verified. Git Credential Manager, SSH keys, GH_TOKEN/GITHUB_TOKEN overrides, fine-grained PAT selections, MCP connectors, cloud agents and CI tokens can use different credentials. Verify each actual transport. Shared owner credentials also give compromised agent sessions an estate-wide blast radius. |
| GitHub redirects are permanent and cover every link | Git clone/fetch/push redirects normally work. Reusing an old repository path deletes its redirect. Pages URLs do not redirect; Packages links vary by registry. Review integrations and update canonical remotes after transfer. |
| gh repo rename OWNER/REPO transfers ownership | The installed CLI explicitly documents that rename accepts a repository name without its owner. The proposed commands do not implement transfers. Use the transfer endpoint or GitHub transfer UI after preflight and authorization. |
| Organization-wide secrets cover private repositories on Free | Organization-level Actions secrets and variables are inaccessible to private repositories on Free. Retain suitable repository-scoped credentials or use supported short-lived identity federation; do not duplicate all deployment secrets into a broad shared pool. |
| Copilot creates no duplication or policy friction | A personal IDE subscription is separate from the organization plan. Actual seat assignments, organization policies and metered AI credits still need inspection. Neither universal harness access nor a future fixed price was established. |
| R2 eliminates asset costs and is automatically safe | Direct R2 egress is free. Standard storage is $0.015/GB-month, Class A $4.50/million and Class B $0.36/million beyond included usage. Infrequent Access adds retrieval fees. Public access, retention, integrity, encryption, residency and restore proof remain separate. |
| KvK trade names are independently verified | The mapping reflects Frank's supplied names and the source documents. No current registration extract was inspected. A sole proprietorship may have several trade names, but GitHub organizations do not establish separate legal entities or change liability. |
| Sub-30ms TTFB, perfect Web Vitals, guaranteed ranking and margins | No live geographically distributed measurement, customer benchmark or cost reconciliation was supplied. These are targets or hypotheses. Google Search does not use llms.txt for its search/AI features; it cannot establish guaranteed citation or market leadership. |
| C2PA stamping proves AI Act and copyright compliance | Machine-readable marking and relevant deployer disclosures are different obligations. A signature does not certify rights ownership or complete regulatory compliance. Determine actual role, output type and applicable disclosure obligations. |

## Implementation verification

Router: reran all nine Node tests and syntax validation successfully. Source rejects missing consent, browser origins, unsupported streaming/tools, invalid authentication and unavailable metering. Explicit 429/5xx responses may fail over; ambiguous transport errors stop. Caching and payload logging are disabled. This differs from the strategy's automatic semantic caching claims. Polar ingestion is sandbox-only; production mode is rejected. Request-rate admission is not a funded balance or session spending reservation. Real provider adapters/catalog access, paid entitlements, retention/reconciliation, durable storage growth and end-to-end recovery remain open. No live provider call was made.

Studio: reran all four flow tests successfully. They cover portable DAG serialization, typed connections, unsafe sources, credentials, duplicate IDs and import limits. The inspected canvas is a custom React/localStorage prototype with import/export and undo, not a demonstrated React Flow/WebGPU implementation. Its UI explicitly says generation adapters are disconnected. Browser interaction, accessibility, large-graph behavior, real generation and export recovery remain unverified by these tests.

Claw: reran five provenance cases: four passed, one real-tool fixture case skipped because explicit fixture configuration is absent. Source requires external signing and trust paths, trusted signatures and asset hash binding, preserves the prompt sidecar and verifies upload snapshots. Mocked transport checks do not prove an operational production signer, complete audio/video coverage or legal compliance.

Existing ecosystem issue6 already records unpublished/unaccepted implementations and further platform/billing findings. Reuse it; do not replace these open records with architectural completion claims.

## Better execution

Use selective migration. Put suitable public brand repositories in Free organizations after identity and integration checks. Keep private repositories that depend on personal Pro protections where they are until Team benefits or an explicitly accepted alternative justify the change. Keeping current ownership while using organization profiles and links is the immediate alternative: it avoids transfer risk while creator acceptance is unfinished. Choose per repository from required capabilities and operating cost, not a blanket prohibition on Team.

Prioritize the existing creator workflow and its billing/recovery defects before organizational housekeeping. Reuse the accepted core application, local manuscript editor and portable workflow work. Compare the existing Vercel inference path with the Worker on the same consented task, output, cost and recovery criteria before committing to another inference hop. Keep separate deployment repositories only where runtime, release ownership or dependency isolation requires them.

For each eventual transfer, record source and destination repository IDs, visibility, histories, archive state, branch protections, open PRs/issues, Pages/Packages dependencies, app installations, deployment projects, Actions/OIDC trust references, webhooks and secret scopes. Destination name and fork-network checks must pass. Pause the affected writer lanes by agreement; preserve local commits and worktrees. Use a low-dependency public pilot, verify identity at the destination and actual fetch/push transport, then review CI and deployment health before further transfers. Do not use write probes in other agents' branches.

The supported API shape, provided for review only and not executed:

```powershell
gh api --method POST repos/frankxai/REPOSITORY/transfer -f new_owner=Arcanea-Labs
```

The endpoint returns 202 Accepted, which is not completion. Verify the destination repository's stable ID and owner after the asynchronous operation. Authorization must name the reconciled repository mapping and accepted private-feature consequences. Neither bulk transfer nor archival has been executed in this audit.

## Sources

- [GitHub transfer prerequisites, redirects and feature loss](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository)
- [GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
- [GitHub CLI rename](https://cli.github.com/manual/gh_repo_rename)
- [Transfer API](https://docs.github.com/en/rest/repos/repos#transfer-a-repository)
- [GitHub budgets and blocking behavior](https://docs.github.com/en/billing/how-tos/set-up-budgets)
- [Actions organization secret restrictions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
- [KvK sole proprietorship](https://www.kvk.nl/starten/de-eenmanszaak/)
- [Google AI optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [European Commission Article 50 guidance](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)

This is an independent review of Gemini's plan. It does not supply the missing different-provider review of the Codex implementation commits or their release gates. Original files and other harness lanes remain preserved.
