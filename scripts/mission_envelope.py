#!/usr/bin/env python3
"""Mission envelope + outcome receipt helpers (candidate vs verified).

Worker-authored reports are candidate only. Verified requires independent evaluator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def default_out_dir() -> Path:
    root = Path(os.environ.get("AGENTIC_OPS_ROOT", r"C:/Users/frank/agentic-ops"))
    return root / "fleet" / "receipts"


def envelope_template(
    objective: str,
    *,
    repo: str = "",
    branch: str = "",
    path_scope: list[str] | None = None,
    autonomy: str = "A2",
    queen: str = "hermes-default",
    worker: str = "self",
    evaluator: str = "required-independent",
    budget_usd: float | None = None,
    max_turns: int | None = 90,
) -> dict[str, Any]:
    eid = new_id("env")
    body = {
        "schema": "run-envelope/v1",
        "envelope_id": eid,
        "created_at": utc_now(),
        "machine": socket.gethostname(),
        "objective": objective,
        "non_goals": [],
        "bindings": {
            "queen": queen,
            "worker": worker,
            "evaluator": evaluator,
        },
        "scope": {
            "repo": repo,
            "branch": branch,
            "path_scope": path_scope or [],
        },
        "autonomy": {
            "requested": autonomy,
            "effective": autonomy,
            "notes": "Effective autonomy is min(human, identity, policy, action gate, machine policy)",
        },
        "budget": {
            "metered_usd_cap": budget_usd,
            "max_turns": max_turns,
            "wall_time_minutes": None,
        },
        "stop_conditions": [
            "budget exhausted",
            "lease lost",
            "kill switch",
            "disk hard floor",
            "approval expiry",
        ],
        "acceptance": {
            "commands": [],
            "deterministic_required": True,
            "llm_judge_optional": True,
        },
        "status": "open",
    }
    body["envelope_hash"] = sha256_text(json.dumps(body, sort_keys=True))
    return body


def receipt_template(
    envelope_id: str,
    *,
    status: str = "candidate",
    summary: str = "",
    evidence: list[str] | None = None,
    evaluator: str | None = None,
    model: str | None = None,
    provider: str | None = None,
    tokens: int | None = None,
    cost_usd: float | None = None,
) -> dict[str, Any]:
    allowed = {
        "attempted",
        "blocked",
        "failed",
        "candidate",
        "verified",
        "quarantined",
    }
    if status not in allowed:
        raise ValueError(f"status must be one of {sorted(allowed)}")
    if status == "verified" and not evaluator:
        raise ValueError("verified requires named independent evaluator")
    rid = new_id("rcpt")
    body = {
        "schema": "outcome-receipt/v1",
        "receipt_id": rid,
        "envelope_id": envelope_id,
        "created_at": utc_now(),
        "machine": socket.gethostname(),
        "status": status,
        "summary": summary,
        "evidence_refs": evidence or [],
        "route": {"provider": provider, "model": model},
        "resources": {"tokens": tokens, "cost_usd": cost_usd},
        "evaluator": evaluator,
        "security": {
            "red_team": "not_run",
            "supply_chain": "not_run",
        },
        "notes": "Worker reports cannot self-promote to verified",
    }
    body["receipt_hash"] = sha256_text(json.dumps(body, sort_keys=True))
    return body


def write_json(path: Path, data: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Mission envelope / outcome receipt CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("envelope", help="create run envelope")
    e.add_argument("--objective", required=True)
    e.add_argument("--repo", default="")
    e.add_argument("--branch", default="")
    e.add_argument("--path", action="append", default=[])
    e.add_argument("--autonomy", default="A2")
    e.add_argument("--out", type=Path)

    r = sub.add_parser("receipt", help="create outcome receipt")
    r.add_argument("--envelope-id", required=True)
    r.add_argument("--status", default="candidate")
    r.add_argument("--summary", default="")
    r.add_argument("--evidence", action="append", default=[])
    r.add_argument("--evaluator", default=None)
    r.add_argument("--model", default=None)
    r.add_argument("--provider", default=None)
    r.add_argument("--out", type=Path)

    v = sub.add_parser("validate", help="validate receipt file")
    v.add_argument("path", type=Path)

    args = ap.parse_args()
    out_dir = default_out_dir()

    if args.cmd == "envelope":
        data = envelope_template(
            args.objective,
            repo=args.repo,
            branch=args.branch,
            path_scope=args.path,
            autonomy=args.autonomy,
        )
        path = args.out or (out_dir / f"{data['envelope_id']}.json")
        write_json(path, data)
        print(json.dumps({"ok": True, "path": str(path), "envelope_id": data["envelope_id"]}, indent=2))
        return 0

    if args.cmd == "receipt":
        data = receipt_template(
            args.envelope_id,
            status=args.status,
            summary=args.summary,
            evidence=args.evidence,
            evaluator=args.evaluator,
            model=args.model,
            provider=args.provider,
        )
        path = args.out or (out_dir / f"{data['receipt_id']}.json")
        write_json(path, data)
        print(json.dumps({"ok": True, "path": str(path), "receipt_id": data["receipt_id"], "status": data["status"]}, indent=2))
        return 0

    if args.cmd == "validate":
        raw = json.loads(args.path.read_text(encoding="utf-8"))
        errors = []
        if raw.get("schema") != "outcome-receipt/v1":
            errors.append("schema")
        if raw.get("status") == "verified" and not raw.get("evaluator"):
            errors.append("verified_without_evaluator")
        if raw.get("status") not in {
            "attempted",
            "blocked",
            "failed",
            "candidate",
            "verified",
            "quarantined",
        }:
            errors.append("bad_status")
        ok = not errors
        print(json.dumps({"ok": ok, "errors": errors, "status": raw.get("status")}, indent=2))
        return 0 if ok else 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
