# Yoga Book — Telegram + multi-agent alignment (Packet 4 companion)

Run **on the Yoga Book** after `YOGA-BOOK-FIRST-BOOT.md`.

## Goal

Book is **frontend/innovation**, not a second always-on control plane.  
Align Telegram so Lenovo + Book **do not interrupt each other**.

## Hermes Telegram settings (Book)

In Book’s Hermes home (`~/.hermes` / `%LOCALAPPDATA%\hermes`):

### `.env`

```bash
TELEGRAM_ALLOWED_USERS=<Frank user id 8582160385>
TELEGRAM_HOME_CHANNEL=<Frank DM id — usually same>
# Shared bus (one-way status)
TELEGRAM_GROUP_ALLOWED_CHATS=-1004300203404
TELEGRAM_REQUIRE_MENTION=true
TELEGRAM_EXCLUSIVE_BOT_MENTIONS=true
```

### `config.yaml`

```yaml
display:
  busy_input_mode: queue   # never interrupt

telegram:
  require_mention: true
  extra:
    require_mention: true
    exclusive_bot_mentions: true
    free_response_chats: ''
```

Then reload gateway from a **normal terminal** on Book:

```bash
hermes gateway restart
```

## Channel patch (if thrash returns)

If Book still self-interrupts in Starlight Swarm, copy C940’s channel echo filter from:

`%LOCALAPPDATA%\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`

Search for `_CHANNEL_ECHO_PREFIXES` / `_is_channel_system_echo` on C940 and mirror, then restart gateway.

## Usage rules

| Do | Don’t |
| --- | --- |
| Work in **DM** with `@Hermesyogabookbot` | Use Swarm as coding floor |
| Status: `hermes send --to telegram:-1004300203404 "[book] …"` | Dual-@ both bots same task |
| Branches `agent/book/<scope>` | Full C940 cron fleet |
| Frontend lanes only | Clone Business / wallets |

## After boot — paste once to Swarm

```text
Yoga Book online
hostname: …
disk free: …
repos: …
role: frontend-innovation
bot: @Hermesyogabookbot
```

## Read

- `fleet/STARLIGHT-SWARM-DRIVER.md` — full operating model  
- `fleet/FLEET-OPS.md` — daily loops  
- `fleet/YOGA-BOOK-FIRST-BOOT.md` — install/sync  
