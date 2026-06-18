# Codex Automation And Social Approval Map

Created: 2026-06-17  
Timezone: Europe/Amsterdam  
Source repos inspected: `agentic-creator-os`, `agentic-creator-skills`, `claude-code-hooks`, `starlight-social`, `FrankX`, `frankx.ai-vercel-website`, `starlight-cosmos-engine`

This document defines the recommended automation layer for Codex, how it should relate to Claude Code automations, and how social media channels should work with human approval.

## What Claude Code Already Has

Claude has several automation surfaces. They are not one thing; they are a stack:

| Surface | Found in | What it does | Slack route |
| --- | --- | --- | --- |
| Hooks | `claude-code-hooks/hooks/*` | Lifecycle automation: session start/end, quality gate, audit trail, MCP health, compact handling, notification, circuit breaker. | `#ops`, `#repo-command`, `#mcp-integrations` |
| Claude settings hook wiring | `claude-code-hooks/settings-example.json` | Shows when hooks run: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, Stop, PreCompact, Notification. | `#ops` |
| ACOS agents | `agentic-creator-os/.claude/agents` | 147 Claude agents, including social/content/research/publishing agents. | `#agent-teams`, business channel, workflow channel |
| ACOS commands | `agentic-creator-os/.claude/commands` | 172 slash commands. Important folders: `automation`, `monitoring`, `github`, `gsd`, `hooks`. | `#repo-command`, `#ops` |
| ACOS workflows | `agentic-creator-os/workflows` | Content, social, X, LinkedIn, Instagram, YouTube Shorts, TikTok, Farcaster, Mirror, Web3 content flows. | `#social-command`, platform channels |
| GitHub Actions | `agentic-creator-skills/.github/workflows/plugin-validator.yml` | Weekly plugin validation. | `#repo-command`, `#creator-systems` |
| Social publishing MCP | `starlight-social` | MCP tools for channel discovery, local staging, Postiz/Blotato publishing, Playwright sessions, Bluesky/Farcaster direct posting. | `#social-command`, `#social-approvals` |

Important Claude Code hooks found:
- `session-start.js`
- `session-end-log.sh`
- `quality-gate.sh` / `quality-gate.js`
- `audit-trail.sh`
- `mcp-health-check.sh` / `mcp-health-check.js`
- `notification.sh`
- `pre-compact.sh` / `pre-compact.js`
- `circuit-breaker.sh`
- `self-modify-gate.sh`
- `skill-activation-prompt.sh`
- `stop-finalize.js`
- `gsd-context-monitor.*`
- `gsd-workflow-guard.*`

Important ACOS automation commands found:
- `automation/auto-agent.md`
- `automation/self-healing.md`
- `automation/session-memory.md`
- `automation/smart-agents.md`
- `automation/smart-spawn.md`
- `automation/workflow-select.md`
- `monitoring/agent-metrics.md`
- `monitoring/agents.md`
- `monitoring/real-time-view.md`
- `monitoring/status.md`
- `monitoring/swarm-monitor.md`
- `github/multi-repo-swarm.md`
- `github/issue-triage.md`
- `github/pr-manager.md`
- `github/release-manager.md`
- `github/project-board-sync.md`
- `github/workflow-automation.md`

## Best Approach

Use Claude Code hooks for in-session lifecycle enforcement. Use Codex automations for scheduled, detached operations that should wake up without an active Claude session.

Do not let Codex directly publish social content on a schedule. Codex should draft, stage, summarize, and request approval in Slack. Publishing should happen only after explicit approval.

Recommended trust model:

| Action | Agent may do automatically | Requires approval |
| --- | --- | --- |
| Read repo status | Yes | No |
| Summarize commits/PRs | Yes | No |
| Draft Slack updates | Yes | No, if draft only |
| Post internal Slack summaries | Yes, to approved ops channels | For broad announcements |
| Create social drafts | Yes | No |
| Stage social posts locally | Yes | No |
| Publish social posts | No | Yes |
| Schedule social posts | No | Yes |
| Edit website copy | Yes in branch/worktree | Merge/deploy needs approval |
| Create issues/tasks | Yes | No, unless customer-facing |
| Change secrets/env/auth | No | Yes |

## Recommended Codex Automations

These should be created as Codex cron automations after review.

| Automation | Cadence | Workspace | Output channel | Purpose |
| --- | --- | --- | --- | --- |
| Daily Fleet Brief | Weekdays 08:30 | `C:/Users/frank/starlight/repos/agentic-ops-hub` | `#ops` | Summarize repo/business priorities, blockers, stale branches, and top 3 moves. |
| Repo Command Sweep | Weekdays 09:00 | `C:/Users/frank/starlight/repos/agentic-ops-hub` | `#repo-command` | Check changed repos, open worktrees, uncommitted changes, stale branches, failed builds if discoverable. |
| Social Draft Queue | Weekdays 10:00 | `C:/Users/frank/starlight/repos/starlight-social` | `#social-approvals` | Draft platform-ready posts from approved source material; do not publish. |
| Content Repurposing Run | Tue/Thu 11:00 | `C:/Users/frank/starlight/repos/FrankX` | `#content-comms`, `#social-command` | Convert recent blog/video/research assets into social variants. |
| Weekly Agent Team Review | Friday 15:00 | `C:/Users/frank/starlight/repos/agentic-ops-hub` | `#agent-teams` | Review agent roles, stale ownership, workflow gaps, and suggested changes. |
| MCP Health Check | Weekdays 12:00 | `C:/Users/frank/starlight/repos/mcp-doctor` | `#mcp-integrations` | Check MCP/server health and integration drift. |
| Weekly Revenue Ops Review | Monday 13:00 | `C:/Users/frank/starlight/repos/agentic-ops-hub` | `#revenue-ops` | Review offers, checkout blockers, funnel assets, and next revenue experiments. |
| Weekly Social Analytics Review | Monday 16:00 | `C:/Users/frank/starlight/repos/starlight-social` | `#social-command` | Summarize content performance if analytics exports/API keys exist; otherwise list missing data connections. |

## Slack Channels For Automations

| Automation type | Primary Slack channel | Notes |
| --- | --- | --- |
| Cross-business decisions | `#ops` | Only high-level decisions and blockers. |
| Repo status and PR/build/deploy | `#repo-command` | Keep technical status out of business channels unless it blocks them. |
| Agent roster and delegation | `#agent-teams` | Use for who owns what and how agents should coordinate. |
| MCP/tooling health | `#mcp-integrations` | Use for tool auth, server health, adapter failures. |
| Content planning | `#content-comms` | Editorial calendar, launch comms, content briefs. |
| Social planning | `#social-command` | Weekly plan, platform priorities, source material. |
| Social approvals | `#social-approvals` | The only place where publish approval should happen. |
| Platform-specific drafting | `#social-x`, `#social-linkedin`, etc. | Use for variants, profile notes, platform experiments. |

## Social Profile Channels

Agents should use this channel map for profile management and approval.

| Platform/profile surface | Slack channel | Agent may manage | Approval rule |
| --- | --- | --- | --- |
| X/Twitter | `#social-x` | Threads, single posts, replies drafts, hooks. | Post final candidate to `#social-approvals`; publish only after approval. |
| LinkedIn | `#social-linkedin` | Professional posts, articles, carousels, executive authority content. | Approval required before publishing or scheduling. |
| Instagram | `#social-instagram` | Captions, carousel outlines, reel descriptions, hashtag sets. | Approval required before publishing or scheduling. |
| YouTube | `#social-youtube` | Shorts scripts, titles, descriptions, long-form metadata. | Approval required before upload/schedule. |
| TikTok | `#social-tiktok` | Short-form scripts, hooks, caption variants. | Approval required before publish/schedule. |
| Threads | `#social-threads` | Conversation posts and reply drafts. | Approval required before publish/schedule. |
| Bluesky | `#social-bluesky` | Bluesky posts; direct adapter can publish if credentials exist. | Approval required before direct publish. |
| Farcaster | `#social-farcaster` | Casts and Web3 community content. | Approval required before direct cast. |
| Medium / Dev.to / Mirror / Substack | `#social-syndication` | Syndicated long-form versions and canonical-link notes. | Approval required before publication. |
| Cross-platform campaign | `#social-command` | Campaign plan, source asset, platform matrix. | Final approval still happens in `#social-approvals`. |

Known profile references from repo scan:
- X handle correction in website docs: deprecated `@frankxai` should become `@frankxeth`.
- Suno handle correction in website docs: deprecated `suno.com/@frankxai` should become `suno.com/@frankx`.
- `starlight-social` local staging supports `local-x`, `local-linkedin`, `local-threads`.
- `starlight-social` browser adapter supports X, Threads, LinkedIn, Bluesky, and login helper also includes Instagram.
- `starlight-social` Web3 adapter supports Bluesky and Farcaster when env vars are present.

## Social Approval Protocol

All social draft approval messages should use this format in `#social-approvals`:

```md
**Approval request**
Platform:
Profile:
Business:
Source:
Proposed publish window:

**Post**
<final text>

**Media**
<path/link or none>

**Agent notes**
- Goal:
- Risk:
- Reuse:

Reply with one:
- APPROVE
- APPROVE WITH EDITS: <edit>
- REVISE: <reason>
- HOLD
```

Publishing rule:
- `APPROVE` means agent may publish or schedule exactly that post.
- `APPROVE WITH EDITS` means agent must apply only the requested edits, then publish/schedule.
- `REVISE` means return to the platform channel with a new draft.
- `HOLD` means no publish action.

## Recommended Social Agent Team

| Agent role | Source capability | Slack channels |
| --- | --- | --- |
| Content router | ACOS `aco-router` / content workflows | `#content-comms`, `#social-command` |
| Social generator | ACOS `social-content-generator` | Platform channels, `#social-approvals` |
| Publishing strategist | ACOS `publishing-strategist` | `#social-command`, `#social-syndication` |
| SEO specialist | ACOS `seo_specialist` | `#social-syndication`, `#frankx-growth` |
| Viral strategy agent | ACOS `viral-content-strategy` | Platform channels |
| Brand guard | FrankX brand/social skills | `#social-approvals`, `#content-comms` |
| Social publisher | `starlight-social` MCP | `#social-approvals` only after approval |

## Implementation Notes

`starlight-social` supports five engines:
- `local`: stages JSON files in `outputs/staging-social`; safest default.
- `postiz`: uses `POSTIZ_API_KEY`.
- `blotato`: uses `BLOTATO_API_KEY`.
- `playwright`: uses saved browser sessions for X, Threads, LinkedIn, Bluesky; login helper can launch X, Threads, LinkedIn, Bluesky, Instagram.
- `web3`: direct Bluesky and Farcaster publishing with `BLUESKY_USERNAME`, `BLUESKY_APP_PASSWORD`, `FARCASTER_NEYNAR_API_KEY`, `FARCASTER_SIGNER_UUID`.

Recommended default:
1. Use `local` for all automated Codex draft/stage runs.
2. Post approval requests to `#social-approvals`.
3. Only after approval, use Postiz/Blotato/browser/web3 adapter.
4. Store post receipts in `#social-command` and, if relevant, the business channel.

## Immediate Next Setup

1. Create Codex cron automations as reviewable proposals, not silent active jobs.
2. Add `starlight-social` README with engine setup, env vars, and approval protocol.
3. Add an approval-state file or small queue in `starlight-social/outputs/approval-queue`.
4. Add a no-publish default guard so `publish_post` refuses real adapters unless an approval token/id is supplied.
5. Create a weekly social calendar source of truth in `FrankX` or `agentic-ops-hub`.
