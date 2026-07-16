#!/usr/bin/env python3
"""Fleet inventory: tools + clone-manifest repo status for this machine.

Usage:
  python scripts/fleet_inventory.py
  python scripts/fleet_inventory.py --machine c940
  python scripts/fleet_inventory.py --json > fleet/last-inventory.json
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

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fleet" / "clone-manifest.json"
HOME = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or Path.home())


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 45) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
        return r.returncode, out.strip()
    except Exception as e:
        return 1, f"ERR: {e}"


def tool_version(cmd: str) -> str:
    if shutil.which(cmd) is None and shutil.which(cmd + ".exe") is None:
        return "MISSING"
    code, out = run([cmd, "--version"])
    if code != 0:
        code, out = run([cmd, "version"])
    line = (out.splitlines() or [out])[0] if out else "UNKNOWN"
    return line[:120]


def detect_machine(manifest: dict) -> str:
    host = platform.node().upper()
    for mid, meta in manifest.get("machines", {}).items():
        for hint in meta.get("hostname_hints", []) or []:
            if hint and hint.upper() in host:
                return mid
    # default primary backend if unknown Windows frank workstation
    if host:
        return "c940"
    return "unknown"


def repo_status(home: Path, repo: dict) -> dict:
    path = home / repo["path"]
    item = {
        "name": repo["name"],
        "path": str(path),
        "remote": repo.get("remote"),
        "exists": path.exists(),
        "is_git": (path / ".git").exists(),
        "priority": repo.get("priority"),
        "prod": bool(repo.get("prod")),
        "lane": repo.get("lane"),
    }
    if not item["is_git"]:
        return item
    def g(*args: str) -> str:
        c, o = run(["git", *args], cwd=path)
        return o if c == 0 else o

    item["branch"] = g("branch", "--show-current")
    st = g("status", "--porcelain")
    item["dirty"] = 0 if not st else len([ln for ln in st.splitlines() if ln.strip()])
    item["head"] = g("rev-parse", "--short", "HEAD")
    item["origin"] = g("remote", "get-url", "origin")
    ab = g("rev-list", "--left-right", "--count", "@{u}...HEAD")
    if ab and "ERR" not in ab and "\t" in ab.replace(" ", "\t"):
        parts = ab.replace("\t", " ").split()
        if len(parts) >= 2:
            item["behind"], item["ahead"] = parts[0], parts[1]
    return item


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--machine", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--home", default=str(HOME))
    args = ap.parse_args()

    if not MANIFEST.exists():
        print(f"Missing manifest: {MANIFEST}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    machine = args.machine or detect_machine(manifest)
    home = Path(args.home)

    tools = {
        "git": tool_version("git"),
        "gh": tool_version("gh"),
        "node": tool_version("node"),
        "npm": tool_version("npm"),
        "pnpm": tool_version("pnpm"),
        "python": tool_version("python"),
        "uv": tool_version("uv"),
        "hermes": tool_version("hermes"),
        "claude": tool_version("claude"),
        "codex": tool_version("codex"),
        "opencode": tool_version("opencode"),
        "railway": tool_version("railway"),
        "docker": tool_version("docker"),
        "rclone": tool_version("rclone"),
    }

    code, gh = run(["gh", "auth", "status"])
    repos = []
    for repo in manifest.get("repos", []):
        on = repo.get("on") or []
        if machine in on or machine == "all":
            repos.append(repo_status(home, repo))

    # disk
    disk = {}
    try:
        usage = shutil.disk_usage(str(home))
        disk = {
            "total_gb": round(usage.total / (1024**3), 1),
            "used_gb": round(usage.used / (1024**3), 1),
            "free_gb": round(usage.free / (1024**3), 1),
            "used_pct": round(100 * usage.used / usage.total, 1),
        }
    except Exception as e:
        disk = {"error": str(e)}

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "machine_id": machine,
        "os": platform.platform(),
        "home": str(home),
        "disk": disk,
        "tools": tools,
        "gh_auth_ok": code == 0 and "Logged in" in gh,
        "gh_auth_snippet": "\n".join(gh.splitlines()[:6]),
        "repos": repos,
        "production_targets": manifest.get("production_targets", []),
        "summary": {
            "repo_count": len(repos),
            "missing": sum(1 for r in repos if not r.get("exists")),
            "dirty": sum(1 for r in repos if r.get("dirty", 0) > 0),
            "clean": sum(1 for r in repos if r.get("is_git") and r.get("dirty", 0) == 0),
        },
    }

    out_path = ROOT / "fleet" / "last-inventory.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"# Fleet inventory — {machine} ({platform.node()})")
    print(f"Generated: {report['generated_at']}")
    print(f"Disk free: {disk.get('free_gb')} GB ({disk.get('used_pct')}% used)")
    print(f"gh auth: {'OK' if report['gh_auth_ok'] else 'FAIL'}")
    print("\n## Tools")
    for k, v in tools.items():
        print(f"- {k}: {v}")
    print("\n## Repos (this machine set)")
    print(f"total={report['summary']['repo_count']} missing={report['summary']['missing']} dirty={report['summary']['dirty']} clean={report['summary']['clean']}")
    for r in repos:
        if not r.get("exists"):
            print(f"- MISSING {r['name']} @ {r['path']}")
        elif not r.get("is_git"):
            print(f"- NOT_GIT {r['name']}")
        else:
            print(
                f"- {r['name']}: branch={r.get('branch')} dirty={r.get('dirty')} head={r.get('head')} origin={r.get('origin')}"
            )
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
