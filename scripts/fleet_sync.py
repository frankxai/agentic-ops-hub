#!/usr/bin/env python3
"""Safe fleet sync from clone-manifest.json.

- Clones missing remotes (gh repo clone or git clone)
- git fetch --all --prune on existing
- ff-only pull ONLY when working tree clean
- NEVER resets or merges dirty trees

Usage:
  python scripts/fleet_sync.py --machine c940 --dry-run
  python scripts/fleet_sync.py --machine c940
  python scripts/fleet_sync.py --machine yoga-book --home C:/Users/frank
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fleet" / "clone-manifest.json"
HOME = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or Path.home())


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
        return r.returncode, out.strip()
    except Exception as e:
        return 1, f"ERR: {e}"


def detect_machine(manifest: dict) -> str:
    host = platform.node().upper()
    for mid, meta in manifest.get("machines", {}).items():
        for hint in meta.get("hostname_hints", []) or []:
            if hint and hint.upper() in host:
                return mid
    return "c940"


def is_dirty(path: Path) -> bool:
    c, o = run(["git", "status", "--porcelain"], cwd=path)
    return c == 0 and bool(o.strip())


def sync_one(home: Path, repo: dict, dry_run: bool) -> dict:
    name = repo["name"]
    path = home / repo["path"]
    remote = repo.get("remote")
    result = {"name": name, "path": str(path), "action": None, "ok": True, "detail": ""}

    if not path.exists():
        if not remote:
            result.update(action="skip_no_remote", ok=False, detail="path missing and no remote")
            return result
        url = remote if remote.startswith("http") else f"https://github.com/{remote}.git"
        cmd = ["gh", "repo", "clone", remote if "/" in remote else f"frankxai/{remote}", str(path)]
        result["action"] = "clone"
        if dry_run:
            result["detail"] = " ".join(cmd)
            return result
        # prefer gh; fallback git
        c, o = run(cmd, timeout=600)
        if c != 0:
            c, o = run(["git", "clone", url, str(path)], timeout=600)
        result["ok"] = c == 0
        result["detail"] = o[-500:]
        return result

    if not (path / ".git").exists():
        result.update(action="skip_not_git", ok=False, detail="path exists but not a git repo")
        return result

    dirty = is_dirty(path)
    if dry_run:
        result["action"] = "fetch" + ("+skip_pull_dirty" if dirty else "+ff_pull")
        result["detail"] = f"dirty={dirty}"
        return result

    c, o = run(["git", "fetch", "--all", "--prune"], cwd=path, timeout=300)
    if c != 0:
        result.update(action="fetch_fail", ok=False, detail=o[-500:])
        return result

    if dirty:
        result.update(action="fetch_only_dirty", ok=True, detail="working tree dirty — no pull")
        return result

    c2, o2 = run(["git", "pull", "--ff-only"], cwd=path, timeout=300)
    if c2 != 0:
        # still ok if no upstream
        result.update(action="fetch_ok_pull_skipped", ok=True, detail=o2[-400:])
        return result

    result.update(action="fetch_and_ff_pull", ok=True, detail=o2[-400:] or "up to date")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--machine", default=None)
    ap.add_argument("--home", default=str(HOME))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--priority-max", type=int, default=99, help="Only sync repos with priority <= N")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    machine = args.machine or detect_machine(manifest)
    home = Path(args.home)

    results = []
    for repo in sorted(manifest.get("repos", []), key=lambda r: r.get("priority", 50)):
        if machine not in (repo.get("on") or []):
            continue
        if int(repo.get("priority", 50)) > args.priority_max:
            continue
        results.append(sync_one(home, repo, args.dry_run))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "machine": machine,
        "hostname": platform.node(),
        "dry_run": args.dry_run,
        "results": results,
        "ok": sum(1 for r in results if r["ok"]),
        "fail": sum(1 for r in results if not r["ok"]),
    }
    out = ROOT / "fleet" / "last-sync.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"# Fleet sync — {machine} dry_run={args.dry_run}")
    for r in results:
        flag = "OK" if r["ok"] else "FAIL"
        print(f"- [{flag}] {r['name']}: {r['action']} — {r['detail'][:120]}")
    print(f"ok={report['ok']} fail={report['fail']} wrote {out}")
    return 0 if report["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
