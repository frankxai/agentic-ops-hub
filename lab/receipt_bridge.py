#!/usr/bin/env python3
"""Map Routing Brain call records onto a starlight.run-receipt.v1 draft.

SIS run-receipt v1 is the envelope (decision recorded 2026-10-21). v1 forbids extra
properties, so routing detail travels in three places that v1 already allows:
stage fields (model, provider, tokens, cost, latency), a stage note (class, fallback,
ZDR flag, the USD cost and the FX rate), and hash-bound evidence entries that point
at the raw routing records. The result is an unsigned draft. Signing and verifying
belong to SIS (src/run-receipt.ts); this module never touches keys.

One receipt is one run: the routing calls made for a task attempt, then the checker.
"""
from __future__ import annotations

import datetime as dt
import math
import re
import uuid

SCHEMA = "starlight.run-receipt.v1"
SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ACCEPT_GATE = "accept"


def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _when(value) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value) if isinstance(value, str) else value
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.isoformat()


def _check_evidence(entries: list[dict]) -> None:
    for entry in entries:
        if not entry.get("kind") or not entry.get("ref") or not SHA_PATTERN.match(str(entry.get("sha256", ""))):
            raise ValueError(f"evidence entry needs kind, ref and a 64-hex sha256: {entry!r}")


def _call_stage(index: int, rec: dict, fx: float) -> tuple[dict, dt.datetime, dt.datetime]:
    if rec.get("synthetic") is True:
        raise ValueError("synthetic routing records never become receipts")
    usd, latency = rec["cost_usd"], rec["latency_ms"]
    if not _finite(usd) or usd < 0 or not _finite(latency) or latency < 0:
        raise ValueError(f"call {rec.get('id')}: cost_usd and latency_ms must be finite and non-negative")
    end = _when(rec["ts"])
    start = end - dt.timedelta(milliseconds=latency)
    note = (f"class={rec['task_class']};primary={rec['primary']};fallback={int(bool(rec.get('fallback_used')))};"
            f"zdr_override={int(bool(rec.get('zdr_override')))};usd={usd!r};fx={fx!r};call={rec.get('id')}")
    stage = {"name": f"call:{rec['task_class']}#{index}", "status": "ok" if rec.get("success") else "failed",
             "model": rec["used"], "provider": rec.get("provider", ""), "costEur": usd * fx,
             "latencyMs": latency, "note": note}
    for src, dst in (("input_tokens", "inputTokens"), ("output_tokens", "outputTokens")):
        if isinstance(rec.get(src), int) and not isinstance(rec.get(src), bool) and rec[src] >= 0:
            stage[dst] = rec[src]
    return stage, start, end


def _verdict(statuses: list[str]) -> str:
    if all(s == "ok" for s in statuses):
        return "PASS"
    return "FAIL" if all(s == "failed" for s in statuses) else "PARTIAL"


def build_receipt(calls: list[dict], *, run: dict, subject: dict, verifier: dict, fx_eur_per_usd,
                  evidence: list[dict], now=None, issuer_name: str = "starlight-router",
                  receipt_id: str | None = None) -> dict:
    if not calls:
        raise ValueError("a receipt needs at least one routing call")
    if not _finite(fx_eur_per_usd) or fx_eur_per_usd <= 0:
        raise ValueError("fx_eur_per_usd is required: say which EUR-per-USD rate was used")
    evidence = list(evidence)
    if verifier.get("evidence_ref"):
        evidence.append({"kind": "checker-output", "ref": verifier["evidence_ref"], "sha256": verifier.get("evidence_sha256", "")})
    _check_evidence(evidence)

    stages, starts, ends = [], [], []
    for i, rec in enumerate(calls):
        stage, start, end = _call_stage(i, rec, fx_eur_per_usd)
        stages.append(stage); starts.append(start); ends.append(end)
    verified_at = _when(verifier["at"])
    latency = verifier.get("latency_ms", 0)
    stages.append({"name": f"verify:{verifier['checker']}", "status": "ok" if verifier["passed"] else "failed",
                   "latencyMs": latency, "costEur": 0.0})
    started, ended = min(starts), max(ends + [verified_at])
    issued = max(_when(now) if now else dt.datetime.now(dt.timezone.utc), ended)

    verdict = _verdict([s["status"] for s in stages])
    if verdict == "PASS" and not evidence:
        raise ValueError("a PASS receipt needs at least one evidence entry")
    decided_by = verifier.get("decided_by", "agent")
    accept = {"gate": ACCEPT_GATE, "decidedBy": decided_by, "actorId": verifier["actor"],
              "outcome": "approved" if verifier["passed"] else "rejected", "at": _iso(verified_at),
              "note": f"checker={verifier['checker']}"}
    if decided_by == "human":
        if not verifier.get("approval_ref"):
            raise ValueError("a human accept decision needs approval_ref")
        accept["approvalRef"] = verifier["approval_ref"]
    zdr_breach = any(bool(c.get("zdr_override")) for c in calls)
    decisions = [
        {"gate": "route", "decidedBy": "policy", "actorId": "routing-brain", "outcome": "approved", "at": _iso(started),
         "note": "model chosen by routing.schema.json for the task class"},
        {"gate": "zdr", "decidedBy": "policy", "actorId": "routing-brain", "outcome": "rejected" if zdr_breach else "approved",
         "at": _iso(started), "note": "non-ZDR model used by explicit override" if zdr_breach else "ZDR rule held for every call"},
        accept,
    ]
    totals = {"costEur": sum(s.get("costEur", 0.0) for s in stages),
              "latencyMs": max((ended - started).total_seconds() * 1000, max(s.get("latencyMs", 0) for s in stages)),
              "tokens": {"input": sum(s.get("inputTokens", 0) for s in stages), "output": sum(s.get("outputTokens", 0) for s in stages)}}
    receipt_run = {"id": run["id"], "kind": run["kind"], "host": run["host"],
                   "startedAt": _iso(started), "endedAt": _iso(ended)}
    if run.get("correlation_id"):
        receipt_run["correlationId"] = run["correlation_id"]
    return {"schema": SCHEMA, "receiptId": receipt_id or f"rcpt_{uuid.uuid4().hex[:16]}", "issuedAt": _iso(issued),
            "issuer": {"name": issuer_name}, "run": receipt_run,
            "subject": {"name": subject["name"], "digest": {"sha256": subject["sha256"]}},
            "stages": stages, "totals": totals, "decisions": decisions, "evidence": evidence, "verdict": verdict}


def separation_problems(receipt: dict) -> list[str]:
    """Maker-checker rule: the actor that accepted the work is not the harness that made it."""
    accept = next((d for d in receipt["decisions"] if d["gate"] == ACCEPT_GATE), None)
    if accept is None:
        return ["no accept decision: nobody checked this work"]
    if accept["actorId"] == receipt["run"]["host"]:
        return [f"maker {receipt['run']['host']!r} accepted its own work"]
    return []


def accepted(receipt: dict) -> bool:
    """Accepted means a different actor approved it and the checker stage passed. Verdict can still be
    PARTIAL when a fallback call failed on the way; v1 verdicts describe stage health, not acceptance."""
    accept = next((d for d in receipt["decisions"] if d["gate"] == ACCEPT_GATE), None)
    check = next((s for s in receipt["stages"] if s["name"].startswith("verify:")), None)
    return bool(accept and accept["outcome"] == "approved" and check and check["status"] == "ok"
                and not separation_problems(receipt))
