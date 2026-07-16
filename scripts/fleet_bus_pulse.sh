#!/usr/bin/env bash
# No-agent fleet pulse: write self heartbeat + optional swarm line to stdout.
# Used by Hermes cron no_agent script jobs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python scripts/fleet_bus.py heartbeat --status live --notes "cron pulse" >/dev/null
python scripts/fleet_bus.py swarm-line
