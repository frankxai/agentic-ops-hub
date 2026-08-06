#!/usr/bin/env python3
"""Mission envelope + outcome receipt helpers (candidate vs verified).

Worker-authored reports are candidate only. Verified requires an independent
evaluator name that is not the worker/queen/self/placeholder.
Writes are restricted to allowlisted roots and .json only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FORBIDDEN_EVALUATORS = {
    "",
    "self",
    "worker",
    "queen",
    "required-independent",
    "me",
    "same",
    "n/a",
    "na",
    "none",
    "null",
    "tbd",
    "todo",
    "unknown",
    "local",
    "auto",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "hermes"
    return Path.home() / ".hermes"


def default_out_dir() -> Path:
    root = Path(os.environ.get("AGENTIC_OPS_ROOT", r"C:/Users/frank/agentic-ops"))
    return (root / "fleet" / "receipts").resolve()


def write_allow_roots() -> list[Path]:
    roots = [
        default_out_dir(),
        hermes_home() / "state",
        Path(r"C:/Users/frank/.worktrees/agentic-ops-night-loops-20260806/fleet/receipts"),
        Path(r"C:/Users/frank/agentic-ops/fleet/receipts"),
    ]
    # Also allow any agentic-ops* worktree receipts under .worktrees
    wt = Path(r"C:/Users/frank/.worktrees")
    if wt.is_dir():
        for child in wt.iterdir():
            if child.is_dir() and "agentic-ops" in child.name.lower():
                roots.append(child / "fleet" / "receipts")
    out: list[Path] = []
    for r in roots:
        try:
            out.append(r.resolve())
        except OSError:
            continue
    return out


def assert_safe_write_path(path: Path) -> Path:
    """Resolve and require path under allowlisted roots, .json only, no traversal tricks."""
    if path.suffix.lower() != ".json":
        raise ValueError("write path must end with .json")
    # Disallow obvious traversal tokens in the original string form
    raw = str(path)
    if ".." in Path(raw).parts:
        raise ValueError("path traversal rejected")
    try:
        resolved = path.expanduser().resolve()
    except OSError as e:
        raise ValueError(f"cannot resolve path: {e}") from e
    allowed = False
    for root in write_allow_roots():
        try:
            resolved.relative_to(root)
            allowed = True
            break
        except ValueError:
            continue
    if not allowed:
        raise ValueError(
            "write path outside allowlist (fleet/receipts or HERMES_HOME/state only)"
        )
    return resolved


def body_hash(body: dict[str, Any], hash_key: str) -> str:
    clone = {k: v for k, v in body.items() if k != hash_key}
    return sha256_text(json.dumps(clone, sort_keys=True, default=str))


def normalize_evaluator(name: str | None) -> str | None:
    if name is None:
        return None
    cleaned = re.sub(r"\s+", " ", str(name).strip().lower())
    return cleaned or None


def assert_independent_evaluator(evaluator: str | None, *, worker: str | None = None, queen: str | None = None) -> str:
    ev = normalize_evaluator(evaluator)
    if not ev:
        raise ValueError("verified requires named independent evaluator")
    if ev in FORBIDDEN_EVALUATORS:
        raise ValueError(f"evaluator '{evaluator}' is not independent")
    for role in (worker, queen):
        if role and normalize_evaluator(role) == ev:
            raise ValueError("evaluator must differ from worker/queen")
    # reject trivial self-ish patterns
    if ev.startswith("self") or ev.endswith("/self") or "worker" == ev:
        raise ValueError(f"evaluator '{evaluator}' is not independent")
    return ev


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
    body: dict[str, Any] = {
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
    body["envelope_hash"] = body_hash(body, "envelope_hash")
    return body


def receipt_template(
    envelope_id: str,
    *,
    status: str = "candidate",
    summary: str = "",
    evidence: list[str] | None = None,
    evaluator: str | None = None,
    worker: str | None = "self",
    queen: str | None = "hermes-default",
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
    ev_out: str | None = normalize_evaluator(evaluator)
    if status == "verified":
        ev_out = assert_independent_evaluator(evaluator, worker=worker, queen=queen)
    rid = new_id("rcpt")
    body: dict[str, Any] = {
        "schema": "outcome-receipt/v1",
        "receipt_id": rid,
        "envelope_id": envelope_id,
        "created_at": utc_now(),
        "machine": socket.gethostname(),
        "status": status,
        "summary": (summary or "")[:2000],
        "evidence_refs": list(evidence or [])[:50],
        "route": {"provider": provider, "model": model},
        "resources": {"tokens": tokens, "cost_usd": cost_usd},
        "evaluator": ev_out,
        "roles": {"worker": worker, "queen": queen},
        "security": {
            "red_team": "not_run",
            "supply_chain": "not_run",
        },
        "notes": "Worker reports cannot self-promote to verified",
    }
    body["receipt_hash"] = body_hash(body, "receipt_hash")
    return body


def write_json(path: Path, data: dict[str, Any]) -> Path:
    safe = assert_safe_write_path(path)
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return safe


def validate_receipt(raw: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if raw.get("schema") != "outcome-receipt/v1":
        errors.append("schema")
    status = raw.get("status")
    if status not in {
        "attempted",
        "blocked",
        "failed",
        "candidate",
        "verified",
        "quarantined",
    }:
        errors.append("bad_status")
    stored = raw.get("receipt_hash")
    if not stored:
        errors.append("missing_receipt_hash")
    else:
        expected = body_hash(raw, "receipt_hash")
        if stored != expected:
            errors.append("receipt_hash_mismatch")
    if status == "verified":
        roles = raw.get("roles") if isinstance(raw.get("roles"), dict) else {}
        try:
            assert_independent_evaluator(
                raw.get("evaluator"),
                worker=roles.get("worker") if roles else raw.get("worker"),
                queen=roles.get("queen") if roles else raw.get("queen"),
            )
        except ValueError:
            errors.append("verified_without_independent_evaluator")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Mission envelope / outcome receipt CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("envelope", help="create run envelope")
    e.add_argument("--objective", required=True)
    e.add_argument("--repo", default="")
    e.add_argument("--branch", default="")
    e.add_argument("--path", action="append", default=[])
    e.add_argument("--autonomy", default="A2")
    e.add_argument("--worker", default="self")
    e.add_argument("--queen", default="hermes-default")
    e.add_argument("--out", type=Path)

    r = sub.add_parser("receipt", help="create outcome receipt")
    r.add_argument("--envelope-id", required=True)
    r.add_argument("--status", default="candidate")
    r.add_argument("--summary", default="")
    r.add_argument("--evidence", action="append", default=[])
    r.add_argument("--evaluator", default=None)
    r.add_argument("--worker", default="self")
    r.add_argument("--queen", default="hermes-default")
    r.add_argument("--model", default=None)
    r.add_argument("--provider", default=None)
    r.add_argument("--out", type=Path)

    v = sub.add_parser("validate", help="validate receipt file")
    v.add_argument("path", type=Path)

    args = ap.parse_args()
    out_dir = default_out_dir()

    try:
        if args.cmd == "envelope":
            data = envelope_template(
                args.objective,
                repo=args.repo,
                branch=args.branch,
                path_scope=args.path,
                autonomy=args.autonomy,
                worker=args.worker,
                queen=args.queen,
            )
            path = args.out or (out_dir / f"{data['envelope_id']}.json")
            written = write_json(path, data)
            print(
                json.dumps(
                    {"ok": True, "path": str(written), "envelope_id": data["envelope_id"]},
                    indent=2,
                )
            )
            return 0

        if args.cmd == "receipt":
            data = receipt_template(
                args.envelope_id,
                status=args.status,
                summary=args.summary,
                evidence=args.evidence,
                evaluator=args.evaluator,
                worker=args.worker,
                queen=args.queen,
                model=args.model,
                provider=args.provider,
            )
            path = args.out or (out_dir / f"{data['receipt_id']}.json")
            written = write_json(path, data)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "path": str(written),
                        "receipt_id": data["receipt_id"],
                        "status": data["status"],
                    },
                    indent=2,
                )
            )
            return 0

        if args.cmd == "validate":
            raw = json.loads(args.path.read_text(encoding="utf-8"))
            errors = validate_receipt(raw)
            ok = not errors
            print(json.dumps({"ok": ok, "errors": errors, "status": raw.get("status")}, indent=2))
            return 0 if ok else 2
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
