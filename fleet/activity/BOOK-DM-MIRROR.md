# Book private-DM → fleet/activity mirror

**Why:** Private Telegram DMs with `@Hermesyogabookbot` never reach C940.  
**Rule:** Any **proposal**, plan, or next-step agreed in Book DM with Frank **must** be mirrored into shared git files so `@lenovostarlightbot` / Command Center can see them after `git pull`.

## Mandatory (Book agent)

After every meaningful private-DM turn that produces a proposal or handoff:

```bash
cd ~/agentic-ops   # or C:/Users/frank/agentic-ops

python scripts/fleet_activity.py propose \
  --machine yoga-book \
  --agent hermes-book \
  --title "one-line proposal" \
  --body "short detail, no secrets" \
  --evidence "branch/path/ticket" \
  --next "what C940 or Book should do next" \
  --source private-dm \
  --queue-to c940          # optional: also ticket into to-c940.json

git add fleet/activity fleet/bus/queues
git commit -m "activity(book): mirror DM proposal <id>"
git push origin main
```

Optional one-line Swarm bulletin (not a substitute for the log):

```bash
hermes send --to telegram:-1004300203404 "[book] mirrored proposal: <title> → ACTIVITY-LOG"
```

## What counts as a “proposal”

- “We should do X next”
- Lane claims (FE1, UI polish, R1 CTA, …)
- Blockers that need C940 / human
- Architecture / product decisions from the DM
- Explicit “tell c940 …” asks

**Do not** log secrets, tokens, wallet data, or full chat dumps.

## What C940 reads

| Path | Role |
| --- | --- |
| `fleet/activity/ACTIVITY-LOG.md` | Human + agent append-only log (`kind=proposal`) |
| `fleet/activity/calendar/YYYY-MM-DD.md` | Day glance |
| `fleet/activity/proposals.jsonl` | Machine-readable proposal stream |
| `fleet/bus/queues/to-c940.json` | If `--queue-to c940` was used |

```bash
# on C940 after pull
python scripts/fleet_activity.py proposals -n 10
python scripts/fleet_activity.py tail -n 40
python scripts/fleet_activity.py today
```

## Anti-patterns

- Only discussing next steps in Book DM with no git write  
- Assuming C940 “already knows” from Telegram  
- Using Swarm channel as the durable proposal store  
- Forging `c940` heartbeats or writing as the wrong machine  

## Related

- `fleet/activity/README.md` — full collab model  
- `fleet/YOGA-BOOK-TELEGRAM-ALIGN.md` — Telegram gates  
- `fleet/STARLIGHT-SWARM-DRIVER.md` — DM = work, channel = bulletin  
- `scripts/fleet_activity.py` — `propose` / `log` / `proposals` / `tail` / `today`  
