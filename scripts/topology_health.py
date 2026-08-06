#!/usr/bin/env python3
"""Declared → installed → scheduled → running → delivered health receipt.

No-agent safe. Prints JSON to stdout. Empty stdout only when --quiet-ok and GREEN.
Never prints secret file contents. Never mutates Hermes credentials.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DISK_RED_GB = 50.0
DISK_HARD_GB = 35.0
HEARTBEAT_MAX_AGE_S = 8 * 3600


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "hermes"
    return Path.home() / ".hermes"


def run_cmd(args: list[str], timeout: int = 45) -> tuple[int, str]:
    try:
        p = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        out = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else "")
        return p.returncode, out.strip()
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except OSError as e:
        return 1, str(e)


def which(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    # Windows npm-global shims often missing from the Python process PATH
    extras: list[Path] = []
    roaming = os.environ.get("APPDATA")
    local = os.environ.get("LOCALAPPDATA")
    home = Path.home()
    if roaming:
        npm = Path(roaming) / "npm"
        extras.extend(
            [
                npm / f"{name}.cmd",
                npm / f"{name}.exe",
                npm / f"{name}.ps1",
                npm / name,
            ]
        )
    if local:
        extras.append(Path(local) / "hermes" / "bin" / name)
    extras.append(home / ".local" / "bin" / name)
    extras.append(home / ".local" / "bin" / f"{name}.exe")
    for cand in extras:
        if cand.is_file():
            return str(cand)
    return None


def disk_free_gb(path: str = "C:/") -> float:
    u = shutil.disk_usage(path)
    return round(u.free / (1024**3), 2)


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def list_jobs(home: Path) -> list[dict[str, Any]]:
    data = load_json(home / "cron" / "jobs.json")
    if data is None:
        return []
    if isinstance(data, list):
        return [j for j in data if isinstance(j, dict)]
    if isinstance(data, dict):
        if "jobs" in data and isinstance(data["jobs"], list):
            return [j for j in data["jobs"] if isinstance(j, dict)]
        # id-keyed map
        vals = list(data.values())
        if vals and all(isinstance(v, dict) for v in vals):
            out = []
            for k, v in data.items():
                if isinstance(v, dict):
                    row = dict(v)
                    row.setdefault("id", k)
                    out.append(row)
            return out
    return []


def mcp_status(home: Path) -> list[dict[str, Any]]:
    cfg = load_json(home / "config.yaml")  # may be yaml
    # Prefer hermes mcp list text parse fallback via CLI
    code, out = run_cmd(["hermes", "mcp", "list"], timeout=60)
    servers: list[dict[str, Any]] = []
    if code == 0 and out:
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("Name") or line.startswith("─") or line.startswith("MCP"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                status = "enabled" if "enabled" in line.lower() or "✓" in line else "unknown"
                servers.append({"name": name, "status": status, "source": "hermes mcp list"})
    # Also read yaml if pyyaml available
    try:
        import yaml  # type: ignore

        raw = (home / "config.yaml").read_text(encoding="utf-8")
        y = yaml.safe_load(raw) or {}
        mcp = y.get("mcp_servers") or {}
        for name, conf in mcp.items():
            if not isinstance(conf, dict):
                continue
            existing = next((s for s in servers if s["name"] == name), None)
            row = existing or {"name": name}
            row["enabled"] = conf.get("enabled", True)
            row["transport"] = "url" if conf.get("url") else "stdio"
            row["command"] = conf.get("command")
            if not existing:
                servers.append(row)
            else:
                existing.update(row)
    except Exception:
        pass
    # handshake tests for known owned servers (names only)
    for s in servers:
        name = s.get("name")
        if not name:
            continue
        c, o = run_cmd(["hermes", "mcp", "test", str(name)], timeout=90)
        s["handshake_ok"] = c == 0 and ("Tools discovered" in o or "Connected" in o or "✓" in o)
        if c == 0:
            # extract tool count if present
            for line in o.splitlines():
                if "Tools discovered:" in line:
                    try:
                        s["tools"] = int(line.split(":")[-1].strip())
                    except ValueError:
                        pass
    return servers


def profile_snapshot() -> list[dict[str, Any]]:
    code, out = run_cmd(["hermes", "profile", "list"], timeout=45)
    rows: list[dict[str, Any]] = []
    if code != 0:
        return [{"error": out[:300]}]
    for line in out.splitlines():
        line = line.rstrip()
        if "◆" in line or (line.strip() and not line.strip().startswith("Profile") and "────" not in line and "Model" not in line):
            parts = line.replace("◆", " ").split()
            if len(parts) >= 2 and parts[0] not in {"Profile", "───────────────"}:
                rows.append(
                    {
                        "name": parts[0],
                        "gateway": "running" if "running" in line else ("stopped" if "stopped" in line else "unknown"),
                        "raw": " ".join(parts[1:6]),
                    }
                )
    return rows


def tool_probe(names: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for n in names:
        path = which(n)
        if not path:
            out[n] = {"ok": False, "path": None}
            continue
        # Always invoke the resolved path — bare names often miss npm-global PATH in Python.
        flag = "--version"
        c, o = run_cmd([path, flag], timeout=20)
        if c != 0 and path.lower().endswith(".cmd"):
            c, o = run_cmd(["cmd.exe", "/c", path, flag], timeout=20)
        out[n] = {
            "ok": c == 0,
            "path": path,
            "version": (o.splitlines()[0] if o else "")[:120],
        }
    return out


def score_overall(findings: list[dict[str, Any]], free_gb: float, running_gateways: int) -> str:
    if free_gb < DISK_HARD_GB:
        return "RED"
    reds = [f for f in findings if f.get("severity") == "RED"]
    yellows = [f for f in findings if f.get("severity") == "YELLOW"]
    if reds or free_gb < DISK_RED_GB:
        return "RED" if reds or free_gb < DISK_HARD_GB else "YELLOW"
    if yellows or running_gateways != 1:
        return "YELLOW"
    return "GREEN"


def build_receipt(write_path: Path | None = None) -> dict[str, Any]:
    home = hermes_home()
    free = disk_free_gb("C:/")
    findings: list[dict[str, Any]] = []

    if free < DISK_HARD_GB:
        findings.append(
            {
                "severity": "RED",
                "code": "disk_hard_floor",
                "detail": f"{free}GB free < {DISK_HARD_GB}GB hard floor; block heavyweight work",
            }
        )
    elif free < DISK_RED_GB:
        findings.append(
            {
                "severity": "YELLOW",
                "code": "disk_ops_floor",
                "detail": f"{free}GB free < {DISK_RED_GB}GB ops floor",
            }
        )

    tools = tool_probe(["git", "gh", "node", "npm", "pnpm", "python", "hermes", "claude", "codex", "opencode"])
    for name, info in tools.items():
        if name in {"git", "gh", "python", "hermes"} and not info.get("ok"):
            findings.append({"severity": "RED", "code": f"tool_missing_{name}", "detail": name})
        elif name in {"claude", "codex"} and not info.get("ok"):
            findings.append({"severity": "YELLOW", "code": f"tool_missing_{name}", "detail": name})

    jobs = list_jobs(home)
    active = [j for j in jobs if j.get("enabled") is True or j.get("enabled") == "true"]
    paused = [j for j in jobs if j.get("enabled") is False]
    unpinned_llm = []
    for j in active:
        if j.get("no_agent"):
            continue
        if not j.get("provider") or not j.get("model"):
            unpinned_llm.append(j.get("name") or j.get("id"))
    if unpinned_llm:
        findings.append(
            {
                "severity": "YELLOW",
                "code": "cron_unpinned_llm",
                "detail": unpinned_llm[:12],
            }
        )
    grok_pinned_paused = [
        j.get("name")
        for j in paused
        if str(j.get("provider") or "").startswith("xai") or "grok" in str(j.get("model") or "").lower()
    ]

    profiles = profile_snapshot()
    running_gws = [p for p in profiles if p.get("gateway") == "running"]
    if len(running_gws) > 1:
        findings.append(
            {
                "severity": "RED",
                "code": "multi_gateway_running",
                "detail": [p.get("name") for p in running_gws],
            }
        )
    elif len(running_gws) == 0:
        findings.append(
            {
                "severity": "YELLOW",
                "code": "no_gateway_running",
                "detail": "default gateway not observed running",
            }
        )

    mcp = mcp_status(home)
    mcp_fail = [m.get("name") for m in mcp if m.get("handshake_ok") is False]
    if mcp_fail:
        findings.append({"severity": "RED", "code": "mcp_handshake_fail", "detail": mcp_fail})

    # heartbeat self only
    ops_candidates = [
        Path(r"C:/Users/frank/agentic-ops"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-control"),
        Path(__file__).resolve().parents[1],
    ]
    heartbeat = None
    for root in ops_candidates:
        hb = root / "fleet" / "bus" / "heartbeats" / "c940.json"
        if hb.is_file():
            data = load_json(hb) or {}
            at = data.get("at")
            age_ok = False
            age_m = None
            if at:
                try:
                    stamp = datetime.fromisoformat(str(at).replace("Z", "+00:00"))
                    if stamp.tzinfo is None:
                        stamp = stamp.replace(tzinfo=timezone.utc)
                    age_s = int((datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds())
                    age_m = age_s // 60
                    age_ok = age_s <= HEARTBEAT_MAX_AGE_S
                except ValueError:
                    pass
            heartbeat = {"path": str(hb), "fresh": age_ok, "age_minutes": age_m, "at": at}
            if not age_ok:
                findings.append({"severity": "YELLOW", "code": "heartbeat_stale", "detail": heartbeat})
            break

    ticker = home / "cron" / "ticker_heartbeat"
    ticker_age = None
    if ticker.is_file():
        ticker_age = int(time.time() - ticker.stat().st_mtime)

    overall = score_overall(findings, free, len(running_gws))
    receipt = {
        "schema": "topology-health/v1",
        "status": overall,
        "generated_at": utc_now(),
        "machine": {
            "hostname": socket.gethostname(),
            "node": platform.node(),
            "platform": platform.platform(),
            "claimed_role": "c940" if "1B4ICID" in socket.gethostname().upper() else "unknown",
        },
        "planes": {
            "disk_free_gb": free,
            "disk_class": "HARD_RED" if free < DISK_HARD_GB else ("RED" if free < DISK_RED_GB else "OK"),
            "hermes_home": str(home),
            "tools": tools,
            "profiles": profiles,
            "gateways_running": [p.get("name") for p in running_gws],
            "mcp": mcp,
            "cron": {
                "total": len(jobs),
                "active": len(active),
                "paused": len(paused),
                "active_names": [j.get("name") for j in active][:40],
                "paused_names": [j.get("name") for j in paused][:40],
                "paused_grok_or_xai": grok_pinned_paused,
                "unpinned_active_llm": unpinned_llm,
            },
            "heartbeat": heartbeat,
            "cron_ticker_age_seconds": ticker_age,
        },
        "lifecycle": {
            "declared": ["profiles", "mcp_servers", "cron_jobs", "coding_clis"],
            "installed": {
                "hermes": tools.get("hermes", {}).get("ok"),
                "claude": tools.get("claude", {}).get("ok"),
                "codex": tools.get("codex", {}).get("ok"),
            },
            "scheduled_active": len(active),
            "running_gateways": len(running_gws),
            "delivered_note": "delivery proof is per-job; this receipt is control-plane health only",
        },
        "findings": findings,
        "next_actions": [],
    }

    if free < DISK_HARD_GB:
        receipt["next_actions"].append("Run safe reclaim of rebuildable caches; block new heavy clones/builds")
    if grok_pinned_paused:
        receipt["next_actions"].append(
            "Repin paused content/memory/PR crons to openai-codex live provider or keep HOLD explicit"
        )
    if unpinned_llm:
        receipt["next_actions"].append("Pin provider+model on active LLM crons")
    if mcp_fail:
        receipt["next_actions"].append("Repair MCP handshake failures before trusting memory tools")
    if not receipt["next_actions"] and overall == "GREEN":
        receipt["next_actions"].append("No control-plane action required")

    if write_path:
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        receipt["written_to"] = str(write_path)
    return receipt


def main() -> int:
    ap = argparse.ArgumentParser(description="Topology health receipt (no-agent)")
    ap.add_argument("--json", action="store_true", help="force JSON stdout")
    ap.add_argument("--write", type=Path, help="write receipt JSON path")
    ap.add_argument("--quiet-ok", action="store_true", help="print nothing when GREEN")
    args = ap.parse_args()
    receipt = build_receipt(write_path=args.write)
    if args.quiet_ok and receipt.get("status") == "GREEN":
        return 0
    print(json.dumps(receipt, indent=2))
    return 0 if receipt.get("status") != "RED" else 2


if __name__ == "__main__":
    sys.exit(main())
