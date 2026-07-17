#!/usr/bin/env python3
"""Probe flat-subscription CLI capacity without exposing credentials.

Default mode checks installation and declared auth only. --live performs one-turn
provider calls and is the only mode allowed to label a CLI ready.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if __package__ in {None, ""}:
    sys.path.insert(0, str(ROOT))

from scripts.fleet_bus import detect_machine


def run(command: list[str], *, cwd: str | None = None, timeout: int = 90) -> tuple[int, str]:
    try:
        executable = shutil.which(command[0]) or command[0]
        normalized: list[str] | str = [executable, *command[1:]]
        use_shell = False
        if os.name == "nt" and Path(executable).suffix.lower() in {".cmd", ".bat"}:
            normalized = subprocess.list2cmdline([executable, *command[1:]])
            use_shell = True
        result = subprocess.run(
            normalized,
            cwd=cwd,
            shell=use_shell,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.returncode, ((result.stdout or "") + (result.stderr or "")).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 124, str(exc)


def classify_probe(
    *, installed: bool, auth_declared: bool, live_checked: bool, live_ok: bool
) -> str:
    if not installed:
        return "missing-cli"
    if live_checked:
        return "ready" if live_ok else "blocked-live-auth"
    return "auth-declared-unverified" if auth_declared else "auth-missing"


def resource_gate(
    *, disk_free_gb: float, memory_percent: float, disk_floor_gb: float = 50, memory_ceiling: float = 85
) -> dict[str, Any]:
    blockers = []
    if disk_free_gb < disk_floor_gb:
        blockers.append("disk")
    if memory_percent > memory_ceiling:
        blockers.append("memory")
    return {
        "launch_allowed": not blockers,
        "blockers": blockers,
        "disk_free_gb": round(disk_free_gb, 1),
        "disk_floor_gb": disk_floor_gb,
        "memory_percent": round(memory_percent, 1),
        "memory_ceiling_percent": memory_ceiling,
    }


def memory_percent() -> float:
    try:
        import psutil  # type: ignore

        return float(psutil.virtual_memory().percent)
    except ImportError:
        if os.name == "nt":
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(status)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return float(status.dwMemoryLoad)
        pages = os.sysconf("SC_PHYS_PAGES")
        available = os.sysconf("SC_AVPHYS_PAGES")
        return 100.0 * (1.0 - available / pages)


def _version(binary: str) -> tuple[bool, str]:
    resolved = shutil.which(binary)
    if not resolved:
        return False, "missing"
    code, output = run([resolved, "--version"], timeout=30)
    line = next((line.strip() for line in output.splitlines() if line.strip()), "unknown")
    return code == 0, line[:200]


def claude_live_ok(exit_code: int, output: str) -> bool:
    if exit_code != 0:
        return False
    try:
        payload: Any = json.loads(output)
    except json.JSONDecodeError:
        try:
            payload = json.loads(output.splitlines()[0])
        except (json.JSONDecodeError, IndexError):
            return "PONG" in output.upper()
    if isinstance(payload, list):
        payload = next(
            (item for item in reversed(payload) if isinstance(item, dict) and item.get("type") == "result"),
            payload[-1] if payload else None,
        )
    if not isinstance(payload, dict):
        return False
    return not payload.get("is_error") and "PONG" in str(payload.get("result", "")).upper()


def _probe_claude(live: bool) -> dict[str, Any]:
    installed, version = _version("claude")
    auth_declared = False
    declared_detail = ""
    if installed:
        code, output = run(["claude", "auth", "status"], timeout=30)
        declared_detail = output[:500]
        try:
            payload = json.loads(output)
            auth_declared = code == 0 and bool(payload.get("loggedIn"))
        except json.JSONDecodeError:
            auth_declared = code == 0 and "logged" in output.lower()
    live_ok = False
    live_detail = "not run"
    if live and installed:
        code, output = run(
            [
                "claude",
                "-p",
                "Reply exactly PONG.",
                "--model",
                "sonnet",
                "--max-turns",
                "1",
                "--output-format",
                "json",
            ],
            timeout=90,
        )
        live_detail = output[:800]
        live_ok = claude_live_ok(code, output)
    return {
        "installed": installed,
        "version": version,
        "status": classify_probe(
            installed=installed,
            auth_declared=auth_declared,
            live_checked=live,
            live_ok=live_ok,
        ),
        "auth_declared": auth_declared,
        "declared_detail": "logged-in" if auth_declared else declared_detail[:200],
        "live_detail": live_detail[:300],
    }


def _probe_codex(live: bool, repo: str, model: str) -> dict[str, Any]:
    installed, version = _version("codex")
    auth_declared = False
    declared_detail = ""
    if installed:
        code, output = run(["codex", "login", "status"], timeout=30)
        declared_detail = output[:300]
        auth_declared = code == 0 and "logged in" in output.lower()
    live_ok = False
    live_detail = "not run"
    if live and installed:
        code, output = run(
            [
                "codex",
                "exec",
                "-C",
                repo,
                "--sandbox",
                "read-only",
                "-m",
                model,
                "-c",
                "model_reasoning_effort=low",
                "Reply exactly PONG. Do not inspect or modify files.",
            ],
            timeout=120,
        )
        live_ok = code == 0 and "PONG" in output.upper()
        live_detail = output[-800:]
    return {
        "installed": installed,
        "version": version,
        "model": model,
        "status": classify_probe(
            installed=installed,
            auth_declared=auth_declared,
            live_checked=live,
            live_ok=live_ok,
        ),
        "auth_declared": auth_declared,
        "declared_detail": declared_detail[:200],
        "live_detail": live_detail[:300],
    }


def _probe_gemini(live: bool, model: str = "gemini-3.5") -> dict[str, Any]:
    installed, version = _version("gemini")
    gemini_home = Path(os.environ.get("GEMINI_CLI_HOME", str(Path.home()))) / ".gemini"
    oauth_declared = any(
        (gemini_home / name).is_file() for name in ("oauth_creds.json", "google_accounts.json")
    )
    metered_key_present = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    auth_declared = oauth_declared
    live_ok = False
    live_detail = "not run"
    live_checked = live and installed and auth_declared
    if live_checked:
        code, output = run(
            ["gemini", "-m", model, "-p", "Reply exactly PONG.", "--output-format", "json"],
            timeout=120,
        )
        live_ok = code == 0 and "PONG" in output.upper()
        live_detail = output[-500:]
    return {
        "installed": installed,
        "version": version,
        "model": model,
        "status": classify_probe(
            installed=installed,
            auth_declared=auth_declared,
            live_checked=live_checked,
            live_ok=live_ok,
        ),
        "auth_declared": auth_declared,
        "auth_source": "oauth-subscription" if oauth_declared else ("metered-key-only" if metered_key_present else "none"),
        "declared_detail": (
            "Gemini OAuth credential source present"
            if oauth_declared
            else "metered API key present but not counted as Gemini Ultra subscription capacity"
            if metered_key_present
            else "no Gemini OAuth credential source found"
        ),
        "live_detail": live_detail[:300],
    }


def _probe_simple(binary: str, live: bool, live_command: list[str], auth_command: list[str]) -> dict[str, Any]:
    installed, version = _version(binary)
    auth_declared = False
    declared_detail = ""
    if installed:
        code, output = run(auth_command, timeout=30)
        declared_detail = output[:300]
        lowered = output.lower()
        auth_declared = code == 0 and "0 credentials" not in lowered and "not logged" not in lowered
    live_ok = False
    live_detail = "not run"
    live_checked = live and installed and auth_declared
    if live_checked:
        code, output = run(live_command, timeout=120)
        live_ok = code == 0 and "PONG" in output.upper()
        live_detail = output[-500:]
    return {
        "installed": installed,
        "version": version,
        "status": classify_probe(
            installed=installed,
            auth_declared=auth_declared,
            live_checked=live_checked,
            live_ok=live_ok,
        ),
        "auth_declared": auth_declared,
        "declared_detail": declared_detail[:200],
        "live_detail": live_detail[:300],
    }


def build_report(*, machine: str, live: bool, repo: str, codex_model: str) -> dict[str, Any]:
    usage = shutil.disk_usage(repo)
    gate = resource_gate(
        disk_free_gb=usage.free / (1024**3),
        memory_percent=memory_percent(),
    )
    effective_live = live and gate["launch_allowed"]
    probes = {
        "claude-max": _probe_claude(effective_live),
        "openai-codex-max": _probe_codex(effective_live, repo, codex_model),
        "gemini-ultra": _probe_gemini(effective_live),
        "opencode": _probe_simple(
            "opencode",
            effective_live,
            ["opencode", "run", "Reply exactly PONG."],
            ["opencode", "auth", "list"],
        ),
    }
    ready = [name for name, probe in probes.items() if probe["status"] == "ready"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "machine_id": machine,
        "hostname": platform.node(),
        "live_requested": live,
        "live_checked": effective_live,
        "resource_gate": gate,
        "subscription_clis": probes,
        "ready_lanes": ready if gate["launch_allowed"] else [],
        "launch_policy": (
            "bounded-outcome-only"
            if gate["launch_allowed"]
            else "blocked-until-resource-pressure-clears"
        ),
        "notes": [
            "Flat subscriptions should be maximized by verified outcomes, not synthetic token burn.",
            "Declared auth is never treated as ready without a one-turn live preflight.",
            "Across machines, parallelize owners; on a 16GB node, run coding CLIs sequentially.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe coding CLI capacity")
    parser.add_argument("--machine", default=None)
    parser.add_argument("--repo", default=str(ROOT))
    parser.add_argument("--codex-model", default="gpt-5.6-terra")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    machine = args.machine or detect_machine()
    report = build_report(machine=machine, live=args.live, repo=args.repo, codex_model=args.codex_model)
    output = Path(args.output) if args.output else ROOT / "fleet" / "reports" / "cli-capacity" / f"{machine}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"wrote {output}")
    return 0 if report["resource_gate"]["launch_allowed"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
