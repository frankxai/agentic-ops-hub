#!/usr/bin/env python3
"""Backup posture check for fleet machines.

Usage:
  python scripts/fleet_backup_check.py
  python scripts/fleet_backup_check.py --json
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

HOME = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or Path.home())
ROOT = Path(__file__).resolve().parents[1]


def which(name: str) -> bool:
    return shutil.which(name) is not None or shutil.which(name + ".exe") is not None


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()
    except Exception as e:
        return 1, str(e)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    usage = shutil.disk_usage(str(HOME))
    free_gb = usage.free / (1024**3)

    one_drive_candidates = [
        HOME / "OneDrive",
        HOME / "OneDrive - Personal",
    ]
    onedrive = next((str(p) for p in one_drive_candidates if p.exists()), None)

    code, gh = run(["gh", "auth", "status"])
    biz = HOME / "Business"
    biz_origin = None
    if (biz / ".git").exists():
        c, o = run(["git", "-C", str(biz), "remote", "get-url", "origin"])
        biz_origin = o if c == 0 else None

    control = ROOT
    control_dirty = 0
    if (control / ".git").exists():
        c, o = run(["git", "-C", str(control), "status", "--porcelain"])
        if c == 0 and o:
            control_dirty = len([ln for ln in o.splitlines() if ln.strip()])

    checks = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "disk_free_gb": round(free_gb, 1),
        "disk_free_ok": free_gb >= 80,
        "gh_auth_ok": code == 0 and "Logged in" in gh,
        "onedrive_path": onedrive,
        "onedrive_ok": bool(onedrive),
        "restic_installed": which("restic"),
        "rclone_installed": which("rclone"),
        "tar_installed": which("tar"),
        "business_exists": biz.exists(),
        "business_has_origin": bool(biz_origin),
        "business_origin": biz_origin,
        "control_plane_path": str(control),
        "control_plane_dirty": control_dirty,
        "gaps": [],
    }

    if not checks["gh_auth_ok"]:
        checks["gaps"].append("gh auth not OK — code cannot sync to GitHub")
    if not checks["onedrive_ok"]:
        checks["gaps"].append("OneDrive path not found — secondary backup weak")
    if not checks["rclone_installed"]:
        checks["gaps"].append("rclone MISSING — no encrypted offsite layer")
    if not checks["restic_installed"]:
        checks["gaps"].append("restic MISSING — no encrypted local snapshots tool")
    if free_gb < 80:
        checks["gaps"].append(f"disk free {free_gb:.1f}GB < 80GB target")
    if checks["business_exists"] and not checks["business_has_origin"]:
        checks["gaps"].append("Business has no git origin — local-only risk")
    if control_dirty:
        checks["gaps"].append(f"agentic-ops dirty={control_dirty} — commit fleet control plane")

    checks["status"] = "GREEN" if not checks["gaps"] else ("YELLOW" if len(checks["gaps"]) <= 3 else "RED")

    out = ROOT / "fleet" / "last-backup-check.json"
    out.write_text(json.dumps(checks, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        print(f"# Backup check — {checks['status']}")
        print(f"free_gb={checks['disk_free_gb']} onedrive={checks['onedrive_ok']} rclone={checks['rclone_installed']} restic={checks['restic_installed']}")
        for g in checks["gaps"]:
            print(f"- GAP: {g}")
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
