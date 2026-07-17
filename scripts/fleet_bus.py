#!/usr/bin/env python3
"""Fleet bus helpers with local + remote Git truth reconciliation.

Only write heartbeats for THIS machine. Status reads local files and the latest
fetched origin/main tree so a dirty/diverged worktree cannot hide a live peer.
"""
from __future__ import annotations

import argparse
import json
import platform
import socket
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_OPS_ROOT = Path(__file__).resolve().parents[1]
BUS_ROOT = _OPS_ROOT / "fleet" / "bus"
LEGACY_BUS_ROOT = _OPS_ROOT / "bus"
MACHINE_MAP = {
    "DESKTOP-1B4ICID": "c940",
    "Starlight": "yoga-book",
}


def _mirror_legacy(rel: Path, content: str) -> None:
    try:
        dest = LEGACY_BUS_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    except OSError:
        pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_time(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def detect_machine() -> str:
    host = socket.gethostname()
    node = platform.node()
    for hint, mid in MACHINE_MAP.items():
        if hint.lower() in host.lower() or hint.lower() in node.lower():
            return mid
    combined = f"{host} {node}".lower()
    if "yoga" in combined or "book" in combined:
        return "yoga-book"
    return "unknown"


def _heartbeat_key(data: dict[str, Any], fallback: str = "") -> str:
    machine = str(data.get("machine_id", "")).lower()
    if machine == "yogabook":
        return "yoga-book"
    return machine or fallback.removesuffix(".json")


def _read_local_heartbeats(root: Path = BUS_ROOT) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    directory = root / "heartbeats"
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            result[_heartbeat_key(data, path.name)] = data
        except (OSError, json.JSONDecodeError) as exc:
            result[path.stem] = {"file": path.name, "error": str(exc)}
    return result


def _run_git(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(_OPS_ROOT), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _read_remote_heartbeats(ref: str = "origin/main") -> dict[str, dict[str, Any]]:
    tree = _run_git(["ls-tree", "-r", "--name-only", ref, "fleet/bus/heartbeats"])
    if tree.returncode:
        return {}
    result: dict[str, dict[str, Any]] = {}
    for relative in (line.strip() for line in tree.stdout.splitlines() if line.strip().endswith(".json")):
        shown = _run_git(["show", f"{ref}:{relative}"])
        if shown.returncode:
            continue
        try:
            data = json.loads(shown.stdout)
        except json.JSONDecodeError:
            continue
        result[_heartbeat_key(data, Path(relative).name)] = data
    return result


def reconcile_heartbeats(
    local: dict[str, dict[str, Any]], remote: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    reconciled: dict[str, dict[str, Any]] = {}
    for machine in sorted(set(local) | set(remote)):
        local_value = local.get(machine)
        remote_value = remote.get(machine)
        if remote_value and (
            not local_value
            or _parse_time(str(remote_value.get("at", "")))
            > _parse_time(str(local_value.get("at", "")))
        ):
            value = dict(remote_value)
            value["source"] = "remote"
        elif local_value:
            value = dict(local_value)
            value["source"] = "local"
        else:
            continue
        reconciled[machine] = value
    return reconciled


def peer_is_fresh(
    heartbeat: dict[str, Any], *, max_age_hours: float = 24, now: str | None = None
) -> bool:
    if heartbeat.get("status") != "live":
        return False
    observed = _parse_time(str(heartbeat.get("at", "")))
    current = _parse_time(now) if now else datetime.now(timezone.utc)
    return observed >= current - timedelta(hours=max_age_hours)


def reconciled_status(ref: str = "origin/main", max_age_hours: float = 24) -> dict[str, Any]:
    local = _read_local_heartbeats()
    remote = _read_remote_heartbeats(ref)
    heartbeats = reconcile_heartbeats(local, remote)
    book = heartbeats.get("yoga-book") or heartbeats.get("yogabook")
    return {
        "self": detect_machine(),
        "remote_ref": ref,
        "heartbeats": list(heartbeats.values()),
        "book_online": bool(book and peer_is_fresh(book, max_age_hours=max_age_hours)),
        "book_heartbeat": book,
    }


def cmd_identity(_: argparse.Namespace) -> int:
    mid = detect_machine()
    payload = {
        "machine_id": mid,
        "hostname": socket.gethostname(),
        "node": platform.node(),
        "platform": platform.platform(),
        "at": utc_now(),
    }
    path = BUS_ROOT / "identity" / f"{mid}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    _mirror_legacy(Path("identity") / f"{mid}.json", text)
    print(json.dumps(payload, indent=2))
    if mid == "unknown":
        print("WARN: hostname not mapped — update MACHINE_MAP / clone-manifest", file=sys.stderr)
        return 2
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    mid = args.machine or detect_machine()
    if mid == "unknown":
        print("REFUSE: unknown machine — will not write heartbeat", file=sys.stderr)
        return 2
    self_id = detect_machine()
    if mid != self_id:
        print(f"REFUSE: cannot write heartbeat for {mid} from host mapped as {self_id}", file=sys.stderr)
        return 3
    payload = {
        "machine_id": mid,
        "hostname": socket.gethostname(),
        "status": args.status,
        "role": "always-on-backend-content-ops" if mid == "c940" else "frontend-innovation",
        "telegram_bot": "@lenovostarlightbot" if mid == "c940" else "@Hermesyogabookbot",
        "notes": args.notes or "",
        "at": utc_now(),
    }
    path = BUS_ROOT / "heartbeats" / f"{mid}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    _mirror_legacy(Path("heartbeats") / f"{mid}.json", text)
    print(json.dumps(payload, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    if args.fetch:
        fetched = _run_git(["fetch", "--prune", "origin"], timeout=120)
        if fetched.returncode:
            print(f"WARN: fetch failed: {fetched.stderr.strip()}", file=sys.stderr)
    print(json.dumps(reconciled_status(args.remote_ref, args.max_age_hours), indent=2))
    return 0


def cmd_swarm_line(args: argparse.Namespace) -> int:
    out = reconciled_status(args.remote_ref, args.max_age_hours)
    mid = str(out["self"])
    own = next((beat for beat in out["heartbeats"] if beat.get("machine_id") == mid), {})
    peer = "book=ONLINE" if out["book_online"] else "book=STALE_OR_MISSING"
    source = (out.get("book_heartbeat") or {}).get("source", "none")
    print(
        f"[{mid}] host={socket.gethostname()} status={own.get('status', 'unknown')} "
        f"{peer} peer_source={source} at={utc_now()} · bus=fleet/bus"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Fleet bus (lightweight)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    identity = sub.add_parser("identity", help="Write identity file for this host")
    identity.set_defaults(func=cmd_identity)

    heartbeat = sub.add_parser("heartbeat", help="Write self heartbeat only")
    heartbeat.add_argument("--machine", default=None, help="Must match self; default=detect")
    heartbeat.add_argument("--status", default="live")
    heartbeat.add_argument("--notes", default="")
    heartbeat.set_defaults(func=cmd_heartbeat)

    status = sub.add_parser("status", help="Show reconciled local + remote heartbeats")
    status.add_argument("--remote-ref", default="origin/main")
    status.add_argument("--max-age-hours", type=float, default=24)
    status.add_argument("--fetch", action="store_true", help="Fetch origin before reading remote ref")
    status.set_defaults(func=cmd_status)

    swarm = sub.add_parser("swarm-line", help="One-line status for Telegram bus")
    swarm.add_argument("--remote-ref", default="origin/main")
    swarm.add_argument("--max-age-hours", type=float, default=24)
    swarm.set_defaults(func=cmd_swarm_line)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
