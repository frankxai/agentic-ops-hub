---
id: H-frankx-voice-layer-2026-10-24
what: FrankX voice layer is merged; finish the editorial pin and local skill pull
where: prompt below
owner: claude
status: open
note: 7 PRs merged through pr-gate with Codex sign-off on 2026-10-23/24
updated: 2026-10-24
---

## Prompt

FrankX voice now has three layers, all on main:

- Stance: Starlight-Intelligence/starlight-design-intelligence `brand-packs/frankx/POINT_OF_VIEW.md` (#56, approved by Frank 2026-10-23).
- Voice card: same pack `BRAND.md`, `COPY.md`, `NARRATIVE.md`.
- Reference lanes: frankxai/content-os `knowledge/voice-observatory/voices/frontier-lab-lane.md` and `founder-teacher-lane.md` (#8). Notion "AI Voices — Observatory" has matching rows.

Consumers point at them: frankx.ai-vercel-website #1094, FrankX-AI/FrankX #296, frankx-x-growth #1, claude-code-config #52 (brand-voice skill, content-polisher, social-content-generator). Website #1098 repinned the required design-contract check to Starlight-Intelligence@cbc5091; it had failed on every website PR since 2026-10-21. Any later change to the FrankX runtime brand pack needs the same repin of `kernel_commit_sha` and `brand.pack_sha256`.

Open:

1. The website editorial contract (`.starlight/editorial-contract.json`, its CI workflow and the STARLIGHT-EDITORIAL blocks) pins design-intelligence `50ae34c` from Codex PR #14, which was closed unmerged. Decide: revive #14 on the new namespace, or retire the projection. Codex owns that lane.
2. The local claude-code-config checkout (where `~/.claude/agents` and the brand-voice skill load from) is 11 commits behind main with 571 uncommitted entries; 15 overlap the incoming change, so it was not pulled. Whoever owns that tree pulls once it is clean.
3. Hyperagent: give it the read-order prompt from the 2026-10-23 session and grade its first six specimens against POINT_OF_VIEW.
