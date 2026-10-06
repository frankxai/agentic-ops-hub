# Reopen prompt: compute atlas, guide and design set (2026-10-06)

Paste everything below the line into a new Claude Code session started in `C:\Users\frank\starlight`.

---

You are the continuation lead for the compute-atlas slice. Judgment work runs on your strongest model; build and bulk work goes to Sonnet or Codex; adversarial review goes to a different provider than the maker. Binding contract: `C:\Users\frank\AGENTS.md` and `C:\Users\frank\starlight\AGENTS.md` (§0 routing, §1 lane claim, §5b craft and receipt, §5e merges). All repos below are public: no private business, family or financial detail in any file, issue or comment. Never merge your own work; never post socially; publishing the guide is Frank's call.

## State (verify every line with a command before acting)

| Thing | Where | Head |
|---|---|---|
| Atlas, planner, tests | `frankxai/starlight-technology`, branch `agent/claude/compute-fleet-intel`, draft PR 35 | `8f81da5`, CI green |
| Blog draft + 16-image design set | `frankxai/frankx.ai-vercel-website`, branch `agent/claude/blog-compute-guide-2026-10`, no PR (repo over PR budget) | `6e30d0621` |
| Handover | `frankxai/agentic-ops-hub`, branch `agent/claude/compute-fleet-handover`, draft PR 158 | `1882202` or later |
| Issues (each is a self-contained agent brief) | starlight-technology 36 and 37, frankx.ai 903, peak-performance 5 | open |
| Queen inbox | `C:\Users\frank\starlight\queen\inbox\2026-10-06-compute-*.json` and `2026-10-06-pp-workload-report.json` (priorities 3 to 6) | queued |

Facts to trust: 20 agent sessions need 49 to 59 GB; six businesses plus a local 30B MoE model need 106.2 to 128.2 GB (split 77.2 to 97.2 GB agent node plus 41 to 43 GB model node); 70B dense plus ERP needs 145.6 to 176.6 GB; largest queued GPU job is 26 GB VRAM. Most inputs are estimates from one laptop profile. Every price needs its own dated source on the merchant host.

## Mission

Move the four issues to done, in this order of value: (1) frankx.ai 903: cross-provider critique, number check, repo gates, publish-ready; (2) starlight-technology 37: planner widget on `/compute`, per-step CI timeouts, overlap with PRs 23 to 25, 390 px QA; (3) peak-performance 5: `pp report` so planner constants become measured; (4) starlight-technology 36: eight data gaps from primary sources. Done means: gates green on the exact commit, evidence file or craft receipt written, draft PR (or a comment explaining why not), handover updated.

## How to work, maximum capability

1. Orient in 5 minutes: `node tools/lane.mjs list`, read the four issue bodies and the queue envelopes, check `queen/running` so you do not duplicate a lane the Queen already dispatched, then `node tools/lane.mjs claim` your paths.
2. Fan out. One writer per worktree. Spawn the independent lanes in parallel in one message: a Codex build lane, a Claude verifier lane, a different-provider critic lane (Grok or Codex review profile). Give each agent the issue URL, the done-condition, the check command and the guardrails. Keep file dumps out of your own context; take back conclusions.
3. Codex that must write outside its launch directory runs directly: `codex exec -C <worktree> -s workspace-write -c sandbox_workspace_write.network_access=true --add-dir <notes-dir> - < brief.md`. A wrapper agent only gets the cwd it was launched in; that is why the first Codex design run wrote nothing.
4. Quality loop on anything visual or public: research three named current references, build, view every render at full size, fix, do a pass that only cuts and polishes, then a skeptical-buyer critique from another provider, then fix again. Check every number against `data/compute` and the post. If a number is not in the sources, it does not ship.
5. Evidence discipline: label vendor, observed, measured, estimate. Promo is not regular price. Unreadable pages are recorded as unreadable. A gate you have not seen fail is not a gate.

## Traps already hit (do not repeat)

- Machine is RAM-tight (about 1.4 GB free at times). Run `pp preflight --workload <type>` first; on HOLD do not start browsers, Next builds or local models. Rely on CI for heavy gates. Stop everything you start.
- PowerShell: a function named `R` collides with the `r` alias (Invoke-History); name helpers `Swap`. `=>` in shell one-liners creates zero-byte junk files; put JS and Python in script files and delete only untracked, zero-byte, junk-named files.
- Python on Windows rewrites files as CRLF; normalize to LF before checking frontmatter with regex.
- The Write and Edit tools refuse paths outside your own worktree; use scripts for other worktrees. Git in other worktrees works with `git -C`. Heredocs are not valid in PowerShell; write message files and use `git commit -F`.
- Cloud environment has a custom egress allowlist; on EGRESS_BLOCKED record the domain in your report.

## Output

Reply in Rundown style: TL;DR first, checklist with exact SHAs and URLs, one 🔴 line per blocker, a Your move block. End with `result:` and a one-line headline only when the ask is delivered, otherwise `needs input:` with exactly what you need.
