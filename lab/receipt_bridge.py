#!/usr/bin/env python3
"""Map Routing Brain call records onto a starlight.run-receipt.v1 draft.

SIS run-receipt v1 is the envelope (decision recorded 2026-10-21). v1 forbids extra
properties, so routing detail travels in three places that v1 already allows:
stage fields (model, provider, tokens, cost, latency), a stage note (class, fallback,
ZDR flag, the USD cost and the FX rate), and hash-bound evidence entries that point
at the raw routing records. The result is an unsigned draft. Signing and verifying
belong to SIS (src/run-receipt.ts); this module never touches keys.

One receipt is one run: the routing calls made for a task attempt, then the checker.

Trust level: everything about WHO checked the work is self-asserted by the caller.
The bridge refuses malformed input, normalises actor ids before comparing them, and
binds the accept decision to the single checker stage, but it cannot prove that the
named checker really ran or that a human really approved. That proof arrives with the
standalone verifier (lab gate `receipt-verifier`). Until then `accepted()` means "the
receipt is internally consistent and claims an independent checker passed", not
"independently verified".
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import uuid
from pathlib import Path

SCHEMA = "starlight.run-receipt.v1"
SCHEMA_FILE = Path(__file__).resolve().parent / "vendor" / "run-receipt.v1.schema.json"
SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")
HTTPS_REF = re.compile(r"^https://[^\s/]+/\S+$")
GH_REF = re.compile(r"^(?:gh:)?([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(#[0-9]+|@[0-9a-f]{7,40})$")
ACCEPT_GATE = "accept"
VERIFY_PREFIX = "verify:"
EVIDENCE_KEYS = {"kind", "ref", "sha256"}
PROVENANCE = "provenance=self-asserted"
DATE_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$")


def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _non_negative(value, name: str):
    if not _finite(value) or value < 0:
        raise ValueError(f"{name} must be a finite non-negative number, got {value!r}")
    return value


def _flag(value, name: str, default: bool = False) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a real boolean, got {value!r}")
    return value


def _text(value, name: str) -> str:
    """A non-empty single-line string that cannot break the `key=value;` note encoding."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string, got {value!r}")
    value = value.strip()
    if ";" in value or "=" in value or CONTROL_CHARS.search(value):
        raise ValueError(f"{name} may not contain ';', '=' or control characters: {value!r}")
    return value


def _actor(value, name: str) -> str:
    return _text(value, name)


def _same_actor(a: str, b: str) -> bool:
    return a.strip().casefold() == b.strip().casefold()


def _when(value) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value) if isinstance(value, str) else value
        if not isinstance(parsed, dt.datetime):
            raise TypeError
    except (TypeError, ValueError):
        raise ValueError(f"not a timestamp: {value!r}") from None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.isoformat()


def _date(value) -> dt.datetime | None:
    """An RFC 3339 date-time with a zone designator, as SIS requires; anything else is None."""
    if not isinstance(value, str) or not DATE_TIME.match(value):
        return None
    try:
        return dt.datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    except ValueError:
        return None


def _cost_tolerance(priced_stages: int) -> float:
    """Mirror of SIS eurTolerance: half a 4-decimal rounding unit per priced stage, plus one."""
    return 0.00005 * (priced_stages + 1)


def semantic_problems(receipt: dict) -> list[str]:
    """The SIS receiptProblems() checks that JSON Schema cannot express: real dates, time order,
    finite numbers, and totals that are not below the stage sums. Mirrors src/run-receipt.ts."""
    problems: list[str] = []
    run = receipt.get("run") if isinstance(receipt.get("run"), dict) else {}
    issued = _date(receipt.get("issuedAt"))
    started, ended = _date(run.get("startedAt")), _date(run.get("endedAt"))
    for label, parsed in (("issuedAt", issued), ("run.startedAt", started), ("run.endedAt", ended)):
        if parsed is None:
            problems.append(f"{label} is not an RFC 3339 date-time with a zone")
    if started and ended and ended < started:
        problems.append("run.endedAt is before run.startedAt")
    if issued and ended and issued < ended:
        problems.append("issuedAt is before run.endedAt")

    cost_sum, latency_max, in_sum, out_sum, priced = 0.0, 0.0, 0, 0, 0
    for i, stage in enumerate(receipt.get("stages") or []):
        for key in ("costEur", "latencyMs"):
            if key in stage and not (_finite(stage[key]) and stage[key] >= 0):
                problems.append(f"stages[{i}].{key} is not a finite non-negative number")
        if _finite(stage.get("costEur")) and stage["costEur"] >= 0:
            cost_sum += stage["costEur"]
            priced += 1
        if _finite(stage.get("latencyMs")) and stage["latencyMs"] >= 0:
            latency_max = max(latency_max, stage["latencyMs"])
        in_sum += stage["inputTokens"] if isinstance(stage.get("inputTokens"), int) else 0
        out_sum += stage["outputTokens"] if isinstance(stage.get("outputTokens"), int) else 0
    if not math.isfinite(cost_sum):
        problems.append("the stage costs sum to a non-finite number")

    totals = receipt.get("totals") if isinstance(receipt.get("totals"), dict) else {}
    for key in ("costEur", "latencyMs"):
        if not (_finite(totals.get(key)) and totals[key] >= 0):
            problems.append(f"totals.{key} is not a finite non-negative number")
    if _finite(totals.get("costEur")) and priced and totals["costEur"] + _cost_tolerance(priced) < cost_sum:
        problems.append(f"totals.costEur {totals['costEur']} is below the stage sum {cost_sum:.4f}")
    if _finite(totals.get("latencyMs")) and totals["latencyMs"] < latency_max:
        problems.append(f"totals.latencyMs {totals['latencyMs']} is below the longest stage {latency_max}")
    tokens = totals.get("tokens") if isinstance(totals.get("tokens"), dict) else {}
    if isinstance(tokens.get("input"), int) and tokens["input"] < in_sum:
        problems.append(f"totals.tokens.input {tokens['input']} is below the stage sum {in_sum}")
    if isinstance(tokens.get("output"), int) and tokens["output"] < out_sum:
        problems.append(f"totals.tokens.output {tokens['output']} is below the stage sum {out_sum}")

    for i, decision in enumerate(receipt.get("decisions") or []):
        at = _date(decision.get("at"))
        if at is None:
            problems.append(f"decisions[{i}].at is not an RFC 3339 date-time with a zone")
        elif issued and at > issued:
            problems.append(f"decisions[{i}].at is after issuedAt")
    return problems


def _check_evidence(entries: list[dict]) -> list[dict]:
    clean = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != EVIDENCE_KEYS:
            raise ValueError(f"evidence entries have exactly kind, ref and sha256: {entry!r}")
        if not all(isinstance(entry[k], str) and entry[k] for k in EVIDENCE_KEYS) or not SHA_PATTERN.match(entry["sha256"]):
            raise ValueError(f"evidence entry needs kind, ref and a 64-hex sha256: {entry!r}")
        clean.append({k: entry[k] for k in ("kind", "ref", "sha256")})
    return clean


def _approval_ref(value) -> str:
    if isinstance(value, str) and HTTPS_REF.match(value.strip()):
        return value.strip()
    match = GH_REF.match(value.strip()) if isinstance(value, str) else None
    if match:
        return f"gh:{match.group(1)}{match.group(2)}"
    raise ValueError(f"a human approval_ref must be an https URL or a GitHub PR/commit reference, got {value!r}")


def _call_stage(index: int, rec: dict, fx: float) -> tuple[dict, dt.datetime, dt.datetime]:
    if not isinstance(rec, dict):
        raise ValueError("routing call must be an object")
    synthetic = rec.get("synthetic")
    if synthetic is not None and not isinstance(synthetic, bool):
        raise ValueError(f"synthetic must be a real boolean, got {synthetic!r}")
    if synthetic:
        raise ValueError("synthetic routing records never become receipts")
    usd = _non_negative(rec.get("cost_usd"), "cost_usd")
    latency = _non_negative(rec.get("latency_ms"), "latency_ms")
    ok = rec.get("success")
    if not isinstance(ok, bool):
        raise ValueError(f"success must be a real boolean, got {ok!r}")
    end = _when(rec.get("ts"))
    start = end - dt.timedelta(milliseconds=latency)
    task_class, primary, used = (_text(rec.get(k), k) for k in ("task_class", "primary", "used"))
    call_id = _text(rec.get("id", f"c{index}"), "id")
    note = (f"class={task_class};primary={primary};fallback={int(_flag(rec.get('fallback_used'), 'fallback_used'))};"
            f"zdr_override={int(_flag(rec.get('zdr_override'), 'zdr_override'))};usd={usd!r};fx={fx!r};call={call_id}")
    provider = rec.get("provider", "")
    if not isinstance(provider, str):
        raise ValueError(f"provider must be a string, got {provider!r}")
    cost_eur = usd * fx
    if not math.isfinite(cost_eur):
        raise ValueError(f"cost_usd {usd!r} at fx {fx!r} converts to a non-finite EUR cost")
    stage = {"name": f"call:{task_class}#{index}", "status": "ok" if ok else "failed",
             "model": used, "provider": provider, "costEur": cost_eur, "latencyMs": latency, "note": note}
    for src, dst in (("input_tokens", "inputTokens"), ("output_tokens", "outputTokens")):
        if rec.get(src) is None:
            continue
        value = rec[src]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{src} must be a non-negative integer, got {value!r}")
        stage[dst] = value
    return stage, start, end


def _verdict(statuses: list[str]) -> str:
    if all(s == "ok" for s in statuses):
        return "PASS"
    return "FAIL" if all(s == "failed" for s in statuses) else "PARTIAL"


def _schema_problems(receipt: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError as exc:  # the bridge never returns an unchecked receipt
        raise RuntimeError("jsonschema is required to validate receipts (pip install jsonschema)") from exc
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in validator.iter_errors(receipt)]


def build_receipt(calls: list[dict], *, run: dict, subject: dict, verifier: dict, fx_eur_per_usd,
                  evidence: list[dict], now=None, issuer_name: str = "starlight-router",
                  receipt_id: str | None = None) -> dict:
    if not isinstance(calls, list) or not calls:
        raise ValueError("a receipt needs at least one routing call")
    if not _finite(fx_eur_per_usd) or fx_eur_per_usd <= 0:
        raise ValueError("fx_eur_per_usd is required: say which EUR-per-USD rate was used")
    if not isinstance(subject, dict) or not isinstance(subject.get("name"), str) or not subject["name"].strip():
        raise ValueError("subject needs a name")
    if not isinstance(subject.get("sha256"), str) or not SHA_PATTERN.match(subject["sha256"]):
        raise ValueError("subject needs a 64-hex sha256 digest")
    evidence = _check_evidence(list(evidence))
    actor, checker = _actor(verifier.get("actor"), "verifier.actor"), _text(verifier.get("checker"), "verifier.checker")
    passed = verifier.get("passed")
    if not isinstance(passed, bool):
        raise ValueError(f"verifier.passed must be a real boolean, got {passed!r}")
    verified_at = _when(verifier.get("at"))
    verifier_latency = _non_negative(verifier.get("latency_ms", 0), "verifier.latency_ms")
    decided_by = verifier.get("decided_by", "agent")
    if decided_by not in ("agent", "human"):
        raise ValueError(f"decided_by must be 'agent' or 'human', got {decided_by!r}")
    if verifier.get("evidence_ref"):
        evidence = _check_evidence(evidence + [{"kind": "checker-output", "ref": verifier["evidence_ref"],
                                                "sha256": verifier.get("evidence_sha256", "")}])
    host = _actor(run.get("host"), "run.host")

    stages, starts, ends = [], [], []
    for i, rec in enumerate(calls):
        stage, start, end = _call_stage(i, rec, fx_eur_per_usd)
        stages.append(stage); starts.append(start); ends.append(end)
    stages.append({"name": f"{VERIFY_PREFIX}{checker}", "status": "ok" if passed else "failed",
                   "latencyMs": verifier_latency, "costEur": 0.0})
    started, ended = min(starts), max(ends + [verified_at])
    issued = max(_when(now) if now else dt.datetime.now(dt.timezone.utc), ended)

    verdict = _verdict([s["status"] for s in stages])
    if verdict == "PASS" and not evidence:
        raise ValueError("a PASS receipt needs at least one evidence entry")
    accept = {"gate": ACCEPT_GATE, "decidedBy": decided_by, "actorId": actor,
              "outcome": "approved" if passed else "rejected", "at": _iso(verified_at),
              "note": f"checker={checker};{PROVENANCE}"}
    if decided_by == "human":
        accept["approvalRef"] = _approval_ref(verifier.get("approval_ref"))
    zdr_breach = any(_flag(c.get("zdr_override"), "zdr_override") for c in calls)
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
    receipt_run = {"id": _text(run.get("id"), "run.id"), "kind": _text(run.get("kind"), "run.kind"), "host": host,
                   "startedAt": _iso(started), "endedAt": _iso(ended)}
    if run.get("correlation_id"):
        receipt_run["correlationId"] = _text(run["correlation_id"], "run.correlation_id")
    receipt = {"schema": SCHEMA, "receiptId": receipt_id or f"rcpt_{uuid.uuid4().hex[:16]}", "issuedAt": _iso(issued),
               "issuer": {"name": issuer_name}, "run": receipt_run,
               "subject": {"name": subject["name"].strip(), "digest": {"sha256": subject["sha256"]}},
               "stages": stages, "totals": totals, "decisions": decisions, "evidence": evidence, "verdict": verdict}
    problems = _schema_problems(receipt) + semantic_problems(receipt)
    if problems:
        raise ValueError("draft is not a valid run-receipt v1: " + "; ".join(problems[:5]))
    return receipt


def _checker_of(accept: dict) -> str | None:
    for part in str(accept.get("note", "")).split(";"):
        if part.startswith("checker="):
            return part[len("checker="):]
    return None


def separation_problems(receipt: dict) -> list[str]:
    """Maker-checker rule, self-asserted: the actor that accepted the work is not the harness that made it,
    and the accept decision names exactly the one checker stage in the receipt."""
    accepts = [d for d in receipt.get("decisions", []) if d.get("gate") == ACCEPT_GATE]
    if len(accepts) != 1:
        return ["no accept decision: nobody checked this work" if not accepts else "more than one accept decision"]
    accept = accepts[0]
    checks = [s for s in receipt.get("stages", []) if str(s.get("name", "")).startswith(VERIFY_PREFIX)]
    if len(checks) != 1:
        return [f"expected exactly one checker stage, found {len(checks)}"]
    problems = []
    if checks[0]["name"] != f"{VERIFY_PREFIX}{_checker_of(accept)}":
        problems.append("the accept decision does not name the checker stage")
    actor, host = str(accept.get("actorId", "")), str(receipt.get("run", {}).get("host", ""))
    if not actor.strip():
        problems.append("accept decision has no actor")
    elif _same_actor(actor, host):
        problems.append(f"maker {host!r} accepted its own work")
    if accept.get("decidedBy") == "human" and not accept.get("approvalRef"):
        problems.append("a human accept decision needs an approvalRef")
    return problems


def accepted(receipt: dict) -> bool:
    """True when the receipt is a valid v1 receipt (schema and the SIS semantic checks), one different actor approved it, and its single checker
    stage passed. Self-asserted: it does not prove the checker ran. Verdict can still be PARTIAL when a
    fallback call failed on the way; v1 verdicts describe stage health, not acceptance."""
    try:
        if _schema_problems(receipt) or semantic_problems(receipt):
            return False
        accept = next(d for d in receipt["decisions"] if d["gate"] == ACCEPT_GATE)
        check = next(s for s in receipt["stages"] if s["name"].startswith(VERIFY_PREFIX))
    except (StopIteration, KeyError, TypeError, AttributeError):
        return False
    return bool(accept["outcome"] == "approved" and check["status"] == "ok" and not separation_problems(receipt))
