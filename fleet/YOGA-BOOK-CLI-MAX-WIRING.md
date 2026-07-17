# YogaBook CLI-Max Wiring Packet

**Owner:** YogaBook (`Starlight`, `yoga-book`, `@Hermesyogabookbot`)  
**Control plane:** C940 (`DESKTOP-1B4ICID`, `c940`, `@lenovostarlightbot`)  
**Work plane:** private DM topic per machine  
**Coordination plane:** Git (`agentic-ops/fleet`) + one-line Starlight Swarm notices

## First sync

Run on YogaBook:

```bash
cd C:/Users/frank/agentic-ops
git fetch --prune origin
git switch main
git pull --ff-only
python scripts/fleet_bus.py identity
python scripts/fleet_bus.py heartbeat --status live --notes "CLI-max wiring synced"
python scripts/fleet_bus.py status --fetch
```

Expected identity is `yoga-book` even though the hostname is `Starlight`. Never write C940's heartbeat.

## Prove subscription lanes

```bash
python scripts/cli_capacity.py \
  --machine yoga-book \
  --live \
  --codex-model gpt-5.6-terra \
  --output fleet/reports/cli-capacity/yoga-book.json
```

The report may say a lane is blocked. That is a valid result. Do not label a lane ready from version/login output alone. Do not commit credentials or raw tokens.

## Active outcome packet: BOOK-CLI-20260717

**Outcome:** independently harden the production `First €100 Weekend` experience from `frankx.ai-vercel-website` PR #326, with mobile/browser evidence and an integration decision. This is a revenue-surface outcome, not a generic audit.

1. Pull the active Book queue from `fleet/bus/queues/to-book.json`.
2. Create an isolated worktree and branch `agent/book/first-100-hardening` from current production main.
3. Review PR #326's diff and live/local experience.
4. If blockers exist, implement scoped fixes on the Book branch and open a follow-up PR; otherwise submit a verified accept/hold decision with evidence.
5. Run repo-local lint/typecheck/tests/build plus mobile browser checks.
6. Write:
   - human report: `fleet/reports/book/2026-07-17-first-100-hardening.md`
   - receipt: `fleet/receipts/BOOK-CLI-20260717.json`
7. Push the agentic-ops receipt update and post exactly one thin-bus line with PR/receipt URL.

**Done when:** receipt has commit, exact zero-exit checks, integration state, and completion timestamp; CI is green or an explicit blocker/owner is recorded. A heartbeat, analysis message, or cron configuration is not done.

## Ongoing connection

```bash
# Beginning of Book session
python scripts/fleet_bus.py status --fetch
python scripts/fleet_activity.py today

# End of Book session
python scripts/fleet_bus.py heartbeat --status live --notes "<delivered outcome or explicit hold>"
python scripts/fleet_activity.py log \
  --machine yoga-book --agent hermes-book \
  --did "<delivered outcome or explicit hold>" \
  --evidence "<receipt/PR path>" \
  --next "<single next owner/action>"
git add fleet/ && git commit -m "activity(book): <outcome>" && git push
```

The Starlight Swarm channel remains a bulletin board. Deep work and corrections happen in YogaBook DM topics.
