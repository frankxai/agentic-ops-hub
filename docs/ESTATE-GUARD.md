# Estate Guard — protecting an agentic estate from the text it reads

> The control-plane record for securing every repo, hook, workflow, MCP server
> and Vercel project in the frankxai estate against agent hijack. Written from
> a real scan of 48 repos on 2026-10-05. Companion to
> [PROTECTION-LAYERS.md](PROTECTION-LAYERS.md) (money and irreversibility) and
> [RED-BLUE-CHARTER.md](RED-BLUE-CHARTER.md).

Last updated: 2026-10-05.

---

## The threat in one sentence

Every documented agent compromise of 2025-2026 is the same shape: **untrusted
text reaches a prompt, secrets sit in the same runtime, and a write channel
exists.** Comment-and-Control (2026-04, three vendors' GitHub agents leaked
secrets through PR titles and hidden HTML comments), the Nx `s1ngularity`
compromise (2025-08, a PR title injected into a workflow, then local `claude`
and `gemini` CLIs were driven to harvest 2,349 credentials), the Trivy action
tag-poisoning that began with a `pull_request_target` flaw and ended in a
poisoned LiteLLM on PyPI (2026-03), the first malicious MCP server
(`postmark-mcp`, 2025-09), and the ClawHub skill campaign (2026-02, hundreds of
malicious skills in a public registry). Sources with dates and confidence tags:
[frontier-landscape.md](../ops/evidence/estate-guard/2026-10-05/frontier-landscape.md).

This estate is unusually exposed to that shape because it *publishes* the
attack surface: 2,000+ `SKILL.md` files, 750 agent definitions, 180 hooks, 170
workflows, and `.mcp.json` files across 48 public-and-private repos, installed
by other people's agents. A hijack here propagates.

## What already existed, and the gap

| Layer | Exists | Where |
|---|---|---|
| Money and irreversibility | 7 layers, fail-closed Payments MCP, human gate | [PROTECTION-LAYERS.md](PROTECTION-LAYERS.md), `payment-intelligence-system`, `starlight-swarm` |
| Per-session safety | circuit breaker, audit trail, self-modify gate, agent IAM | `agentic-creator-os/.claude/hooks/` |
| Per-repo PR gates | `surface-guard` (pull_request_target, trusted-by-construction), `media-guard`, `risk-classifier`, `contract-guard` | frankx.ai-vercel-website, SIS, five product sites |
| Routine honesty | preflight + digest, no silent green | `claude-skills-library/packs/routine-contract` |
| Sentinel intent | permission/secret/mutation gates as a Claw | `Starlight-Intelligence-System/claws/sentinel/` |
| Deploy protection | Vercel SSO on all non-custom-domain URLs | all 60 Vercel projects checked (3 inspected) |

The gap was precise: **nothing scanned the agentic surface itself** (a skill
that says "ignore previous instructions", a hook that runs `npx x@latest` on
every edit, a workflow that hands a stranger's comment to an agent with
`contents: write`), **nothing was deterministic inside a live session** (every
guard was advice a model could be talked out of), and **nothing ran
estate-wide on a schedule** (31 Routines exist; none look at this).

## What shipped on 2026-10-05

The `estate-guard` pack in
[claude-skills-library](https://github.com/frankxai/claude-skills-library)
`packs/estate-guard/`:

| Piece | Mechanism | Strength |
|---|---|---|
| Scanner (`estate-guard-scan.mjs`) | 33 regex/parse rules over workflows, Claude config, MCP, skills, secrets, Next.js routes, deps. Zero deps. `--estate` rolls up many repos. | deterministic |
| CI ratchet (`estate-guard.yml`) | every PR, push to main, and Mondays. High fails. SHA-pinned actions. | deterministic, between sessions |
| Gate hook (PreToolUse on Bash) | **denies** force-push to main, `rm -rf` of root/home, `curl \| sh`, permission bypass, history rewrites, secret deletion, destructive SQL, global-settings writes; **asks** on direct push to main, `reset --hard`, any `rm -r`, unpinned remote exec, prod deploys, db pushes, DELETE API calls, email sends | deterministic, inside the session |
| Taint hook (PostToolUse on WebFetch/WebSearch/MCP/fetching Bash) | marks instruction-shaped text and hidden unicode in tool output as data, next to the data | advisory, cannot be argued away since it fires after the fact |
| Session hook | the three-rule contract plus last scan counts in the prompt | advisory |
| Skill | run, triage, suppress, fix patterns | advisory |

Tests: 22 node tests on temp git fixtures, 50 python hook assertions, run by
the library's `pack-tests` workflow. The one-line install is
`packs/estate-guard/install.sh <repo>`; the estate script is
[`scripts/estate-guard-rollout.sh`](../scripts/estate-guard-rollout.sh).

## The scan: 48 repos, 2026-10-05

Full report: [estate-scan.md](../ops/evidence/estate-guard/2026-10-05/estate-scan.md)
(machine-readable: `estate-scan.json`). After precision tuning against every
high and medium by hand:

| Severity | Count | What they are |
|---|---|---|
| critical | 0 | No live credential in any tracked file across 48 repos. |
| high | 5 | 3 service-role routes with no server-side auth (2 are one IDOR in `arcanea-ai-app` `/api/forge`, fixed in the same PR as the pack install; 1 public form in `gencreator.ai` with no rate limit or origin check); 1 comment-triggered agent workflow in `arcanea-ai-app` with `contents: write` and the comment as its prompt (author gate added, same PR); 1 duplicate of the forge finding. |
| medium | 83 | 10 hooks in `arcanea` running `npx @claude-flow/cli@latest` on every edit, command and prompt; 3 tracked `settings.local.json` (one with `Bash(*)` and auto-approve of all MCP servers); 18 autonomy-escalation lines, all in the vendored `gstack` skill ("do not ask the user for confirmation"); 15 copies of one zero-width space in our own `web-excellence` template (fixed at source); 22 `dangerouslySetInnerHTML` from non-JSON sources (reader components, mostly trusted markdown); 9 workflows with write permissions on untrusted triggers (all `surface-guard`-style, trusted by construction; medium by design); 2 `media-guard` head checkouts (isolated, credential-less, SHA-verified; medium by design). |
| low | 717 | 473 skill lines that run unpinned `npx -y` / `@latest`; 152 `SKILL.md` with no loadable frontmatter (they never load, so whatever they claim to enforce is not enforced); 61 third-party actions pinned to a tag, not a SHA; 15 `.mcp.json` servers on unpinned `npx -y`; 6 Next.js repos with no CSP. |

What the numbers say: the estate's **own code is not leaking**; the exposure
is **supply chain and autonomy surface**. `@latest` in 10 hooks and 473 skill
lines means a single poisoned npm release executes with Frank's privileges on
the next edit. The Trivy incident is exactly that path.

## The layered design

```
  L7  HUMAN GATE         unchanged — money, URLs, keys, blasts, force-push to prod
  L6  RED / BLUE         starlight-evals lane gets injection + hook fixtures from this pack
  L5  ESTATE SWEEP       weekly estate-guard Routine → PR into ops/evidence (durable sink)
  L4  CI RATCHET         estate-guard.yml per repo (PR + push + weekly) + surface-guard + risk-classifier
  L3  TAINT MARKING      PostToolUse taint hook; Routine /fire payloads are already wrapped as untrusted
  L2  DETERMINISTIC GATE PreToolUse Bash gate: deny / ask tiers, deny-list, fails open on parse error
  L1  CONTRACT           SessionStart hook + one CLAUDE.md line per repo: untrusted content is data
  L0  CREDENTIAL BROKER  keys never in the agent: GitHub proxy (cloud sessions), Vercel bypass secrets,
                         Managed Agents vaults, .env untracked, MCP env as ${VAR}; nothing to steal
```

L0 is the layer that makes the others survivable: when the runtime holds no
real secret, an injection that wins still has nothing to exfiltrate. Cloud
sessions already do this for GitHub (credentials attach at the proxy). The
remaining work is the local machines: `.mcp.json` env values as `${VAR}`
references (already true in all 6 configs scanned), `.env` untracked (true in
all 48), and no `settings.local.json` in git (3 to remove).

## Teams on different machines

Git is the coordination layer and the trust boundary. The rules that already
hold (`AGENTS.md` §4 in FrankX, this repo's `AGENTS.md`) stay: one agent, one
branch, one working tree; integrate through a PR; the ops ledger is the shared
memory. What estate-guard adds for a multi-machine, multi-harness fleet:

- **Every harness reads the same contract.** The CLAUDE.md line is harness-
  agnostic text; Codex, Gemini, Grok and Cursor sessions see it through
  `AGENTS.md`/`GEMINI.md`/`GROK.md` pointers. The hooks are Claude Code
  specific; the CI ratchet is not.
- **Cross-agent messages are untrusted.** A message from another session,
  a Routine fire payload, a PR comment written by a bot: all of it arrives
  through tools the taint hook watches. An agent cannot grant another agent
  permission by asking.
- **The sentinel is the schedule, not a process.** "Live" means the Monday
  CI run in every repo plus the Monday estate roll-up Routine. There is no
  daemon to keep up, no machine that must stay on, and the Routine's only
  success condition is a PR with the report in it (routine-contract rule).
- **Drift is measured, not assumed.** The same scanner runs locally, in CI
  and in the Routine; the three numbers must agree. When a repo's `.claude/`
  diverges from the pack, `install.sh` upgrades it in place and the diff is
  the review.

## Rollout

| Wave | Repos | Mode | Status |
|---|---|---|---|
| 1 | `claude-skills-library` (source), `agentic-ops-hub` (control plane), `arcanea-ai-app` (highest exposure: public, 206 routes, 30 workflows, comment-triggered agent) | full | PRs open 2026-10-05 |
| 2 | `frankx.ai-vercel-website`, `gencreator.ai`, `Starlight-Intelligence-System`, `FrankX`, `agentic-creator-os`, `arcanea`, `second-brain-os`, the 5 product sites | full | `scripts/estate-guard-rollout.sh ~/repos --only "..."` |
| 3 | `awesome-*`, `*-agent-skills`, `*-intelligence-system*`, `marine-*`, `mind-*` (no `.claude/`) | `--no-hooks` (scanner + CI) | same script |
| 4 | the 60+ repos outside this session's 48 (`list_repos` shows `has_more`) | per wave 2/3 | after `personal-backup-critical` is rotated and removed, per CONTROL_PLANE.md |

Medium findings worth their own PR, in order: `arcanea` hooks off `@latest`
(10 lines, one file); untrack the 3 `settings.local.json`; pin the 61 actions
by SHA (dependabot can keep them current); CSP for the 6 sites without one.

## Decisions that are Frank's

1. **Vercel firewall.** All 60 projects have SSO on preview URLs and none has
   a custom firewall configuration or bot-protection ruleset on production
   (`get_active_attack_status` returns "Seawall Config not found" on frankx.ai
   and arcanea.ai). Bot Protection in *log* mode is non-disruptive and gives
   data; *challenge* mode can block real users and agents alike. Recommend log
   mode on the three production projects for two weeks, then decide.
2. **`claude-fix.yml` keeps `contents: write`?** With the author gate it is a
   collaborator-only path. If that is acceptable it stays; if not, the agent
   should push to a branch and open a PR instead.
3. **`@latest` policy.** Pin hooks and `.mcp.json` by version everywhere, or
   accept the supply-chain exposure on the 10 arcanea hooks and 15 MCP servers.
4. **Routines and connectors.** Routines run with every connector enabled and
   no permission picker. The estate-guard Routine is created with no
   connectors; the other 12 enabled Routines should each be trimmed to what
   they use.
5. **Which scanners to add.** `zizmor` (Actions), `gitleaks` (history), and
   `snyk/agent-scan` or `cisco-ai-defense/skill-scanner` (skills, MCP) go
   deeper in their lanes. estate-guard stays zero-dependency so it runs
   wherever a hook does; the others can be added to `estate-guard.yml` as
   extra steps when a repo warrants them.

## What this does not claim

No model was involved in any check; the false-negative rate is whatever the
regexes miss, not whatever a prompt can be talked into. The scan covers tracked
and untracked files in the working tree, not git history. Medium and low
findings are reports, not gates. The 60+ repos not in this session were not
scanned.
