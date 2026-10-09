# 2026-10-05 Starlight Home (Claude, 65fd8e86)

Frank asked for one place that shows every session and piece of work, a home feed, saved next-action prompts he can copy into a new agent, and a prompt editor tuned to his goals and his users' interests.

## Shipped

- **Page:** https://claude.ai/artifact/Dw92kLEcn8ELG6bfeZauHy (private, opens on the phone). It has four parts:
  - **Waiting on you:** curated gates, checked live against GitHub, plus recent open PRs.
  - **Prompt deck:** cards with copy buttons and a ready, sent or done status that persists.
  - **Handover feed:** built from `ops/sessions`.
  - **Editor:** Sharpen and "Write a prompt" run on the viewer's Claude, against `ops/home-goals.v1.json`.
- **Code:** `frankxai/starlight-command-center`, branch `agent/claude/home-feed`.
  - `ops/home-feed.mjs` is the compiler, and `ops/home-feed.test.mjs` has 6 tests.
  - `ops/home-goals.v1.json` holds the north star, the quarter goal, eight doctrine rules with sources, the prompt contract and the curated gates.
  - The page source is `apps/starlight-home/starlight-home.html`.
- **Data:** the artifact database holds four feed documents (`feed/meta|prompts|sessions|decisions`). The page owns `state/<id>` and `drafts/<id>`, and the compiler never writes them.
  - Access rule: everyone may read; only editors and Frank may write.
  - Verified: a view-level read works, and an interact-level write is refused.

## Review

Codex reviewed the head as a skeptical buyer and returned REVISE, with 4 high and 6 medium findings. All were fixed at `45a2f65` except one I disputed with a trace ("Show more" does work); Codex's re-verification agreed it was a false positive. Codex re-verified the head and returned PASS WITH FIXES. Its two remaining fixes landed at `81db18d`: a failed status write now rolls back to the saved value, and decision titles are redacted. The original fixes were:
- **State writes:** rapid status clicks no longer lose an update.
- **Trust boundary:** agent text is quoted data inside the editor input.
- **Loud failures:** hub fetch failures stop the compile.
- **Stale gates:** gates whose PR has closed are dropped with a warning.
- **Drafts:** saved in a single write.
- **IDs:** collision-proof.
- **Redaction:** wider coverage.
- **Links:** limited to github.com and claude.ai.
- **Evidence:** the editor must name provable checks, or goal fit is capped at 2.

## How to refresh

`node ops/home-feed.mjs --ref <hub branch with the newest NEXT-PROMPTS> --ref main --days 6`, then in a Claude session read the four `feed` documents for their versions and apply `~/.starlight/home-feed/writes.json` as one ArtifactData batch with `if_version` on each entry. Codex, Grok and Gemini only need to keep `ops/NEXT-PROMPTS.md` and `ops/sessions` current. They have no ArtifactData tool.

## Not done

- **Untested in claude.ai:** Sharpen and "Write a prompt" have not been run there. The first use asks Frank to allow it, and it spends his own Claude usage.
- **Manual refresh:** the page updates only when someone runs the compiler. A scheduled refresh needs a Claude session with ArtifactData, so it cannot be a plain cron job.
- **PR budget:** `starlight/logs/digests/pr-budget.json` is missing, which the rule treats as over budget; the live count is 9 open PRs against a budget of 10.
