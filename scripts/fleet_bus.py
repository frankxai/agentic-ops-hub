#!/usr/bin/env python3
"""Lightweight fleet bus helpers for multi-machine coordination.

SSOT dirs: agentic-ops/fleet/bus/{identity,heartbeats,inbox,queues}
Only write heartbeats for THIS machine (never forge peer heartbeats).
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

# Canonical bus (shared via git). Optional legacy mirror under agentic-ops/bus/.
_OPS_ROOT = Path(__file__).resolve().parents[1]
BUS_ROOT = _OPS_ROOT / "fleet" / "bus"
LEGACY_BUS_ROOT = _OPS_ROOT / "bus"
MACHINE_MAP = {
    "DESKTOP-1B4ICID": "c940",
    "Starlight": "yoga-book",
}


def _mirror_legacy(rel: Path, content: str) -> None:
    """Keep legacy agentic-ops/bus/ in sync for older docs/scripts."""
    try:
        dest = LEGACY_BUS_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    except OSError:
        pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def detect_machine() -> str:
    host = socket.gethostname()
    node = platform.node()
    for hint, mid in MACHINE_MAP.items():
        if hint.lower() in host.lower() or hint.lower() in node.lower():
            return mid
    h = f"{host} {node}".lower()
    if "yoga" in h or "book" in h:
        return "yoga-book"
    return "unknown"


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
        print(
            f"REFUSE: cannot write heartbeat for {mid} from host mapped as {self_id}",
            file=sys.stderr,
        )
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


def cmd_status(_: argparse.Namespace) -> int:
    mid = detect_machine()
    beats = (
        sorted((BUS_ROOT / "heartbeats").glob("*.json"))
        if (BUS_ROOT / "heartbeats").exists()
        else []
    )
    out = {"self": mid, "heartbeats": [], "book_online": False}
    for p in beats:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out["heartbeats"].append(data)
            if data.get("machine_id") in ("yoga-book", "yogabook") or p.name.startswith("yoga"):
                out["book_online"] = True
        except Exception as e:
            out["heartbeats"].append({"file": p.name, "error": str(e)})
    print(json.dumps(out, indent=2))
    return 0


def cmd_swarm_line(_: argparse.Namespace) -> int:
    mid = detect_machine()
    host = socket.gethostname()
    beat_path = BUS_ROOT / "heartbeats" / f"{mid}.json"
    status = "unknown"
    if beat_path.exists():
        try:
            status = json.loads(beat_path.read_text(encoding="utf-8")).get("status", "unknown")
        except Exception:
            pass
    book = BUS_ROOT / "heartbeats" / "yoga-book.json"
    peer = "book=ONLINE" if book.exists() else "book=MISSING"
    print(
        f"[{mid}] host={host} status={status} {peer} at={utc_now()} · bus=fleet/bus"
    )
    return 0


# --- Task Contract / Receipt v1 support (per fleet/TASK-CONTRACTS.md) ---

TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
TASK_STATUSES = {"issued", "claimed", "running", "completed", "expired", "cancelled"}


def _parse_utc(value: object, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _require_relative_allowlist(paths: object) -> None:
    if not isinstance(paths, list) or not paths or not all(isinstance(path, str) and path for path in paths):
        raise ValueError("repo_path_allowlist must be a non-empty list of paths")
    for path in paths:
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("repo_path_allowlist must contain only relative non-traversing paths")


def validate_task_contract(contract: object) -> dict:
    if not isinstance(contract, dict):
        raise ValueError("task contract must be a JSON object")
    task_id = contract.get("task_id")
    if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
        raise ValueError("task_id must use only letters, numbers, dots, underscores, and hyphens")
    if contract.get("schema_version") != "1.0.0":
        raise ValueError("unsupported or missing schema_version")
    for field in ("title", "description", "issuer", "machine_owner", "priority", "source"):
        if not isinstance(contract.get(field), str) or not contract[field]:
            raise ValueError(f"{field} is required")
    for field in ("issuer", "machine_owner"):
        if not TASK_ID_RE.fullmatch(contract[field]):
            raise ValueError(f"{field} must use only letters, numbers, dots, underscores, and hyphens")
    if not re.fullmatch(r"P[0-9]+", contract["priority"]):
        raise ValueError("priority must use P followed by digits")
    _require_relative_allowlist(contract.get("repo_path_allowlist"))
    _parse_utc(contract.get("issued_at"), "issued_at")
    _parse_utc(contract.get("expiry"), "expiry")
    budget = contract.get("resource_budget")
    if not isinstance(budget, dict) or any(
        not isinstance(budget.get(field), (int, float)) or isinstance(budget.get(field), bool) or budget[field] < 0
        for field in ("max_tokens", "max_minutes", "max_cost_usd")
    ):
        raise ValueError("resource_budget requires non-negative max_tokens, max_minutes, and max_cost_usd")
    if not isinstance(budget.get("models_allowed"), list) or not budget["models_allowed"] or not all(
        isinstance(model, str) and model for model in budget["models_allowed"]
    ):
        raise ValueError("resource_budget.models_allowed must be a non-empty list of model names")
    done = contract.get("done_condition")
    if (
        not isinstance(done, dict)
        or done.get("type") not in {"and", "or"}
        or not isinstance(done.get("conditions"), list)
        or not done["conditions"]
    ):
        raise ValueError("done_condition requires type 'and' or 'or' and at least one condition")
    if not all(isinstance(condition, dict) and condition for condition in done["conditions"]):
        raise ValueError("done_condition.conditions must contain non-empty objects")
    for field in ("constraints", "evidence_refs"):
        value = contract.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"{field} must be a list of non-empty strings")
    if contract.get("execution_status") not in TASK_STATUSES:
        raise ValueError("execution_status is invalid")
    return contract


def _validate_task_id(task_id: object) -> str:
    if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
        raise ValueError("task_id must use only letters, numbers, dots, underscores, and hyphens")
    return task_id


def _task_contract_path(task_id: str) -> Path:
    return BUS_ROOT / "contracts" / f"{_validate_task_id(task_id)}.json"


def _task_receipt_path(task_id: str, machine: str) -> Path:
    if not isinstance(machine, str) or not TASK_ID_RE.fullmatch(machine):
        raise ValueError("machine must use only letters, numbers, dots, underscores, and hyphens")
    return BUS_ROOT / "receipts" / f"{_validate_task_id(task_id)}-{machine}.json"


def load_task_contract(task_id: str) -> dict | None:
    try:
        p = _task_contract_path(task_id)
    except ValueError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return None
    if p.exists():
        try:
            return validate_task_contract(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"WARN: invalid task contract {p.name}: {exc}", file=sys.stderr)
    return None


def write_task_contract(contract: dict) -> None:
    validated = validate_task_contract(contract)
    p = _task_contract_path(validated["task_id"])
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(validated, indent=2, sort_keys=True) + "\n"
    p.write_text(text, encoding="utf-8")
    _mirror_legacy(Path("contracts") / f"{validated['task_id']}.json", text)
    print(f"Wrote contract: {p}")


def write_task_receipt(receipt: dict) -> None:
    if not receipt.get("task_id") or not receipt.get("machine"):
        raise ValueError("receipt requires task_id and machine")
    p = _task_receipt_path(receipt["task_id"], receipt["machine"])
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    p.write_text(text, encoding="utf-8")
    _mirror_legacy(Path("receipts") / f"{receipt['task_id']}-{receipt['machine']}.json", text)
    print(f"Wrote receipt: {p}")


def cmd_task_lease(args: argparse.Namespace) -> int:
    if not args.file:
        print("REFUSE: task-lease requires --file with a complete validated contract", file=sys.stderr)
        return 2
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            contract = json.load(f)
        validated = validate_task_contract(contract)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERR loading --file: {exc}", file=sys.stderr)
        return 1
    if validated["task_id"] != args.task_id:
        print("REFUSE: --task-id must match contract task_id", file=sys.stderr)
        return 2
    if validated["issuer"] != detect_machine():
        print("REFUSE: only the local machine may issue its lease", file=sys.stderr)
        return 2
    try:
        write_task_contract(validated)
    except ValueError as exc:
        print(f"ERR validating contract: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_task_claim(args: argparse.Namespace) -> int:
    mid = detect_machine()
    contract = load_task_contract(args.task_id)
    if not contract:
        print(f"ERR: no valid contract for {args.task_id}", file=sys.stderr)
        return 1
    owner = contract["machine_owner"]
    if owner != mid:
        print(f"REFUSE: {mid} is not owner {owner} of task {args.task_id}", file=sys.stderr)
        return 2
    if contract["execution_status"] != "issued":
        print(f"REFUSE: task is {contract['execution_status']}, not issued", file=sys.stderr)
        return 2
    if utc_now() > contract["expiry"]:
        print(f"REFUSE: task expired at {contract['expiry']}", file=sys.stderr)
        return 3
    contract["execution_status"] = "claimed"
    contract["claimed_by"] = mid
    contract["claimed_at"] = utc_now()
    write_task_contract(contract)
    print(f"Claimed {args.task_id} as {mid}")
    return 0


def cmd_task_receipt(args: argparse.Namespace) -> int:
    mid = detect_machine()
    contract = load_task_contract(args.task_id)
    if not contract:
        print(f"REFUSE: no valid contract for {args.task_id}", file=sys.stderr)
        return 3
    if contract["machine_owner"] != mid:
        print(f"REFUSE: {mid} not owner {contract['machine_owner']}", file=sys.stderr)
        return 3
    if contract["execution_status"] not in {"claimed", "running"} or contract.get("claimed_by") != mid:
        print("REFUSE: receipt requires a current claim by this machine", file=sys.stderr)
        return 3
    if utc_now() > contract["expiry"]:
        print(f"REFUSE: task expired at {contract['expiry']}", file=sys.stderr)
        return 3
    evidence_list = [e.strip() for e in (args.evidence or "").split(",") if e.strip()]
    if not evidence_list:
        print("REFUSE: receipt requires at least one evidence reference", file=sys.stderr)
        return 3
    now = utc_now()
    receipt = {
        "schema_version": "1.0.0",
        "task_id": args.task_id,
        "machine": mid,
        "receipt_id": f"receipt-{now.replace(':', '-').replace('+', '')}",
        "at": now,
        "execution_status": "completed",
        "outcome_status": args.outcome,
        "summary": args.summary or "",
        "done_condition_met": evidence_list,
        "evidence_refs": evidence_list + [f"bus/heartbeats/{mid}.json", f"kanban:{args.task_id}"],
        "artifacts": [],
        "resource_used": {"tokens": 0, "minutes": 0, "cost_usd": 0.0},
        "next_actions": [],
        "errors": [],
    }
    write_task_receipt(receipt)
    contract["execution_status"] = "completed"
    contract["outcome_status"] = args.outcome
    contract["evidence_refs"] = receipt["evidence_refs"]
    write_task_contract(contract)
    print(f"Receipt for {args.task_id}: {args.outcome}")
    return 0


def cmd_task_status(args: argparse.Namespace) -> int:
    contract = load_task_contract(args.task_id)
    print("=== CONTRACT ===")
    if contract:
        print(json.dumps(contract, indent=2))
    else:
        print("(none)")
    print("\n=== RECEIPTS ===")
    rec_dir = BUS_ROOT / "receipts"
    if rec_dir.exists():
        for p in sorted(rec_dir.glob(f"{args.task_id}-*.json")):
            try:
                print(json.dumps(json.loads(p.read_text(encoding="utf-8")), indent=2))
            except Exception as e:
                print(f"{p.name}: {e}")
    else:
        print("(no receipts dir)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Fleet bus (lightweight)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("identity", help="Write identity file for this host")
    s.set_defaults(func=cmd_identity)

    s = sub.add_parser("heartbeat", help="Write self heartbeat only")
    s.add_argument("--machine", default=None, help="Must match self; default=detect")
    s.add_argument("--status", default="live")
    s.add_argument("--notes", default="")
    s.set_defaults(func=cmd_heartbeat)

    s = sub.add_parser("status", help="Show self + all heartbeats")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("swarm-line", help="One-line status for Telegram bus")
    s.set_defaults(func=cmd_swarm_line)

    # Task contract/lease/receipt commands (v1)
    s = sub.add_parser("task-lease", help="Create an issuer-owned validated lease from --file")
    s.add_argument("--task-id", required=True)
    s.add_argument("--file", required=True, help="path to a complete contract JSON")
    s.set_defaults(func=cmd_task_lease)

    s = sub.add_parser("task-claim", help="Claim as machine_owner (updates contract status)")
    s.add_argument("--task-id", required=True)
    s.set_defaults(func=cmd_task_claim)

    s = sub.add_parser("task-receipt", help="Record completion receipt + update contract")
    s.add_argument("--task-id", required=True)
    s.add_argument("--outcome", default="success", choices=["success", "failure", "cancelled", "expired"])
    s.add_argument("--summary", default="")
    s.add_argument("--evidence", default="", help="comma-separated evidence strings")
    s.set_defaults(func=cmd_task_receipt)

    s = sub.add_parser("task-status", help="Show contract + any receipts for a task_id")
    s.add_argument("--task-id", required=True)
    s.set_defaults(func=cmd_task_status)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
