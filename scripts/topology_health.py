#!/usr/bin/env python3
"""Declared → installed → scheduled → running health receipt.

No-agent safe. Never prints secret file contents. Never mutates Hermes credentials.
Writes restricted to allowlisted roots (.json only).
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
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


def sanitize(value: Any, limit: int = 200) -> Any:
    """Strip control chars and cap length for stdout-safe fields."""
    if value is None or isinstance(value, (int, float, bool)):
        return value
    if isinstance(value, list):
        return [sanitize(v, limit=limit) for v in value[:40]]
    if isinstance(value, dict):
        return {str(k)[:64]: sanitize(v, limit=limit) for k, v in list(value.items())[:40]}
    text = str(value)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # drop obvious secret-ish assignments
    text = re.sub(r"(?i)(api[_-]?key|token|password|secret|authorization)\s*[:=]\s*\S+", r"\1=[redacted]", text)
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def run_cmd(args: list[str], timeout: int = 45) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except FileNotFoundError:
        return 127, "", "not found"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as e:
        return 1, "", str(e)


def which(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
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


def disk_free_gb(path: str | Path = "C:/") -> float | None:
    try:
        u = shutil.disk_usage(str(path))
        return round(u.free / (1024**3), 2)
    except OSError:
        return None


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def write_allow_roots(home: Path) -> list[Path]:
    roots = [
        home / "state",
        Path(r"C:/Users/frank/agentic-ops/fleet/reports"),
        Path(r"C:/Users/frank/agentic-ops/fleet/receipts"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-night-loops-20260806/fleet/reports"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-night-loops-20260806/fleet/receipts"),
    ]
    wt = Path(r"C:/Users/frank/.worktrees")
    if wt.is_dir():
        for child in wt.iterdir():
            if child.is_dir() and "agentic-ops" in child.name.lower():
                roots.append(child / "fleet" / "reports")
                roots.append(child / "fleet" / "receipts")
    out: list[Path] = []
    for r in roots:
        try:
            out.append(r.resolve())
        except OSError:
            continue
    return out


def assert_safe_write_path(path: Path, home: Path) -> Path:
    if path.suffix.lower() != ".json":
        raise ValueError("write path must end with .json")
    if ".." in Path(str(path)).parts:
        raise ValueError("path traversal rejected")
    resolved = path.expanduser().resolve()
    for root in write_allow_roots(home):
        try:
            resolved.relative_to(root)
            return resolved
        except ValueError:
            continue
    raise ValueError("write path outside allowlist (HERMES state or fleet reports/receipts)")


def list_jobs(home: Path) -> list[dict[str, Any]]:
    data = load_json(home / "cron" / "jobs.json")
    if data is None:
        return []
    if isinstance(data, list):
        return [j for j in data if isinstance(j, dict)]
    if isinstance(data, dict):
        if "jobs" in data and isinstance(data["jobs"], list):
            return [j for j in data["jobs"] if isinstance(j, dict)]
        out = []
        for k, v in data.items():
            if isinstance(v, dict):
                row = dict(v)
                row.setdefault("id", k)
                out.append(row)
        return out
    return []


def job_is_active(job: dict[str, Any]) -> bool:
    en = job.get("enabled")
    if en is None:
        return True  # Hermes default: present job is active unless explicitly false
    if en is True or en == "true" or en == 1 or en == "1":
        return True
    if en is False or en == "false" or en == 0 or en == "0":
        return False
    return bool(en)


def mcp_status(home: Path) -> tuple[list[dict[str, Any]], str | None]:
    """Return (servers, probe_error). probe_error set when MCP plane invisible."""
    code, out, _err = run_cmd(["hermes", "mcp", "list"], timeout=60)
    servers: list[dict[str, Any]] = []
    list_ok = code == 0 and bool(out)
    if list_ok:
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("Name") or line.startswith("─") or line.startswith("MCP"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                name = sanitize(parts[0], 64)
                status = "enabled" if "enabled" in line.lower() else "unknown"
                servers.append({"name": name, "status": status, "source": "hermes mcp list"})

    yaml_ok = False
    try:
        import yaml  # type: ignore

        raw = (home / "config.yaml").read_text(encoding="utf-8")
        y = yaml.safe_load(raw) or {}
        mcp = y.get("mcp_servers") or {}
        yaml_ok = True
        for name, conf in mcp.items():
            if not isinstance(conf, dict):
                continue
            existing = next((s for s in servers if s["name"] == name), None)
            row = existing or {"name": sanitize(name, 64)}
            row["enabled"] = conf.get("enabled", True)
            row["transport"] = "url" if conf.get("url") else "stdio"
            cmd = conf.get("command")
            if isinstance(cmd, str) and cmd:
                row["command_basename"] = sanitize(Path(cmd).name, 64)
            if not existing:
                servers.append(row)
            else:
                existing.update(row)
    except Exception:
        yaml_ok = False

    if not list_ok and not yaml_ok:
        return [], "mcp_plane_invisible"

    for s in servers:
        name = s.get("name")
        if not name:
            continue
        c, o, _e = run_cmd(["hermes", "mcp", "test", str(name)], timeout=90)
        # Prefer structured signals over unicode checkmarks alone
        ok = c == 0 and ("Tools discovered" in o or "Connected" in o)
        s["handshake_ok"] = ok
        if c == 0:
            for line in o.splitlines():
                if "Tools discovered:" in line:
                    try:
                        s["tools"] = int(line.split(":")[-1].strip())
                    except ValueError:
                        pass
    return servers, None


def profile_snapshot() -> tuple[list[dict[str, Any]], str | None]:
    code, out, err = run_cmd(["hermes", "profile", "list"], timeout=45)
    if code != 0:
        return [], sanitize(err or out or "profile list failed", 200)
    rows: list[dict[str, Any]] = []
    for line in out.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        if line.strip().startswith("Profile") or "────" in line or (line.strip().startswith("Model") and "Gateway" in line):
            continue
        if "◆" in line or line.strip():
            parts = line.replace("◆", " ").split()
            if len(parts) >= 2 and parts[0] not in {"Profile", "───────────────"}:
                gw = "unknown"
                low = line.lower()
                # word-boundary-ish tokens
                if re.search(r"\brunning\b", low):
                    gw = "running"
                elif re.search(r"\bstopped\b", low):
                    gw = "stopped"
                rows.append(
                    {
                        "name": sanitize(parts[0], 64),
                        "gateway": gw,
                        "summary": sanitize(" ".join(parts[1:5]), 120),
                    }
                )
    return rows, None


def tool_probe(names: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for n in names:
        path = which(n)
        if not path:
            out[n] = {"ok": False, "path": None}
            continue
        c, o, _e = run_cmd([path, "--version"], timeout=20)
        if c != 0 and path.lower().endswith(".cmd"):
            c, o, _e = run_cmd(["cmd.exe", "/c", path, "--version"], timeout=20)
        out[n] = {
            "ok": c == 0,
            "path": sanitize(path, 160),
            "version": sanitize((o.splitlines()[0] if o else ""), 120),
        }
    return out


def score_overall(findings: list[dict[str, Any]], free_gb: float | None, running_gateways: int | None) -> str:
    if free_gb is not None and free_gb < DISK_HARD_GB:
        return "RED"
    reds = [f for f in findings if f.get("severity") == "RED"]
    yellows = [f for f in findings if f.get("severity") == "YELLOW"]
    if reds:
        return "RED"
    if free_gb is not None and free_gb < DISK_RED_GB:
        return "YELLOW"
    if yellows:
        return "YELLOW"
    if running_gateways is None:
        return "RED"
    if running_gateways != 1:
        return "YELLOW" if running_gateways == 0 else "RED"
    return "GREEN"


def build_receipt(write_path: Path | None = None) -> dict[str, Any]:
    home = hermes_home()
    free_candidates = [disk_free_gb("C:/"), disk_free_gb(home)]
    free_vals = [f for f in free_candidates if f is not None]
    free = min(free_vals) if free_vals else None
    findings: list[dict[str, Any]] = []

    if free is not None and free < DISK_HARD_GB:
        findings.append(
            {
                "severity": "RED",
                "code": "disk_hard_floor",
                "detail": f"{free}GB free < {DISK_HARD_GB}GB hard floor; block heavyweight work",
            }
        )
    elif free is not None and free < DISK_RED_GB:
        findings.append(
            {
                "severity": "YELLOW",
                "code": "disk_ops_floor",
                "detail": f"{free}GB free < {DISK_RED_GB}GB ops floor",
            }
        )
    elif free is None:
        findings.append({"severity": "YELLOW", "code": "disk_probe_failed", "detail": "disk_usage unavailable"})

    tools = tool_probe(["git", "gh", "node", "npm", "pnpm", "python", "hermes", "claude", "codex", "opencode"])
    for name, info in tools.items():
        if name in {"git", "gh", "python", "hermes"} and not info.get("ok"):
            findings.append({"severity": "RED", "code": f"tool_missing_{name}", "detail": name})
        elif name in {"claude", "codex"} and not info.get("ok"):
            findings.append({"severity": "YELLOW", "code": f"tool_missing_{name}", "detail": name})

    jobs = list_jobs(home)
    active = [j for j in jobs if job_is_active(j)]
    paused = [j for j in jobs if not job_is_active(j)]
    unpinned_llm = []
    for j in active:
        if j.get("no_agent"):
            continue
        if not j.get("provider") or not j.get("model"):
            unpinned_llm.append(sanitize(j.get("name") or j.get("id"), 80))
    if unpinned_llm:
        findings.append(
            {
                "severity": "YELLOW",
                "code": "cron_unpinned_llm",
                "detail": unpinned_llm[:12],
            }
        )
    grok_pinned_paused = [
        sanitize(j.get("name"), 80)
        for j in paused
        if str(j.get("provider") or "").startswith("xai") or "grok" in str(j.get("model") or "").lower()
    ]

    profiles, profile_err = profile_snapshot()
    running_gws: list[dict[str, Any]] = []
    running_count: int | None
    if profile_err is not None:
        findings.append({"severity": "RED", "code": "profile_probe_failed", "detail": profile_err})
        running_count = None
    else:
        running_gws = [p for p in profiles if p.get("gateway") == "running"]
        running_count = len(running_gws)
        if running_count > 1:
            findings.append(
                {
                    "severity": "RED",
                    "code": "multi_gateway_running",
                    "detail": [p.get("name") for p in running_gws],
                }
            )
        elif running_count == 0:
            findings.append(
                {
                    "severity": "YELLOW",
                    "code": "no_gateway_running",
                    "detail": "default gateway not observed running",
                }
            )

    mcp, mcp_err = mcp_status(home)
    mcp_fail = [m.get("name") for m in mcp if m.get("handshake_ok") is False]
    if mcp_err:
        findings.append({"severity": "RED", "code": "mcp_probe_failed", "detail": mcp_err})
    elif not mcp:
        findings.append({"severity": "YELLOW", "code": "mcp_none_configured", "detail": "no mcp servers discovered"})
    if mcp_fail:
        findings.append({"severity": "RED", "code": "mcp_handshake_fail", "detail": sanitize(mcp_fail)})

    ops_candidates = [
        Path(r"C:/Users/frank/agentic-ops"),
        Path(r"C:/Users/frank/.worktrees/agentic-ops-control"),
        Path(__file__).resolve().parents[1],
    ]
    heartbeat = None
    claimed_c940 = "1B4ICID" in socket.gethostname().upper()
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
            heartbeat = {"path": sanitize(str(hb), 160), "fresh": age_ok, "age_minutes": age_m, "at": sanitize(at, 40)}
            if not age_ok:
                findings.append({"severity": "YELLOW", "code": "heartbeat_stale", "detail": heartbeat})
            break
    if heartbeat is None:
        findings.append(
            {
                "severity": "RED" if claimed_c940 else "YELLOW",
                "code": "heartbeat_missing",
                "detail": "c940 heartbeat file not found",
            }
        )

    ticker = home / "cron" / "ticker_heartbeat"
    ticker_age = None
    if ticker.is_file():
        ticker_age = int(time.time() - ticker.stat().st_mtime)

    overall = score_overall(findings, free, running_count)
    receipt: dict[str, Any] = {
        "schema": "topology-health/v1",
        "status": overall,
        "generated_at": utc_now(),
        "machine": {
            "hostname": sanitize(socket.gethostname(), 80),
            "node": sanitize(platform.node(), 80),
            "platform": sanitize(platform.platform(), 120),
            "claimed_role": "c940" if claimed_c940 else "unknown",
        },
        "planes": {
            "disk_free_gb": free,
            "disk_class": (
                "HARD_RED"
                if free is not None and free < DISK_HARD_GB
                else ("RED" if free is not None and free < DISK_RED_GB else ("OK" if free is not None else "UNKNOWN"))
            ),
            "hermes_home": sanitize(str(home), 160),
            "tools": tools,
            "profiles": profiles,
            "gateways_running": [p.get("name") for p in running_gws],
            "mcp": mcp,
            "cron": {
                "total": len(jobs),
                "active": len(active),
                "paused": len(paused),
                "active_names": [sanitize(j.get("name"), 80) for j in active][:40],
                "paused_names": [sanitize(j.get("name"), 80) for j in paused][:40],
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
            "running_gateways": running_count,
            "delivered_note": "delivery proof is per-job; this receipt is control-plane health only",
        },
        "findings": findings,
        "next_actions": [],
    }

    if free is not None and free < DISK_HARD_GB:
        receipt["next_actions"].append("Run safe reclaim of rebuildable caches; block new heavy clones/builds")
    if grok_pinned_paused:
        receipt["next_actions"].append(
            "Repin paused content/memory/PR crons to openai-codex live provider or keep HOLD explicit"
        )
    if unpinned_llm:
        receipt["next_actions"].append("Pin provider+model on active LLM crons")
    if mcp_fail or mcp_err:
        receipt["next_actions"].append("Repair MCP handshake/probe before trusting memory tools")
    if profile_err:
        receipt["next_actions"].append("Repair hermes profile list probe; dual-gateway risk unobserved")
    if not receipt["next_actions"] and overall == "GREEN":
        receipt["next_actions"].append("No control-plane action required")

    if write_path:
        safe = assert_safe_write_path(Path(write_path), home)
        safe.parent.mkdir(parents=True, exist_ok=True)
        safe.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        receipt["written_to"] = str(safe)
    return receipt


def main() -> int:
    ap = argparse.ArgumentParser(description="Topology health receipt (no-agent)")
    ap.add_argument("--json", action="store_true", help="force JSON stdout")
    ap.add_argument("--write", type=Path, help="write receipt JSON path")
    ap.add_argument("--quiet-ok", action="store_true", help="print nothing when GREEN")
    args = ap.parse_args()
    try:
        receipt = build_receipt(write_path=args.write)
    except ValueError as exc:
        print(json.dumps({"schema": "topology-health/v1", "status": "RED", "error": str(exc)}, indent=2))
        return 2
    if args.quiet_ok and receipt.get("status") == "GREEN":
        return 0
    print(json.dumps(receipt, indent=2))
    status = receipt.get("status")
    if status == "RED":
        return 2
    if status == "YELLOW":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
