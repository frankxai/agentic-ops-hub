#!/usr/bin/env python3
"""Read-only evidence-gap report and held packets using the existing mission envelope.

This inspects supplied observations. It authenticates no provider evidence, starts
no workers, writes no queue and cannot authorize or attest a production release.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

if __package__ in (None, ""):
    from mission_envelope import assert_independent_evaluator, body_hash, envelope_template
else:
    from .mission_envelope import assert_independent_evaluator, body_hash, envelope_template


QUALITY_GATES = ("workflow", "recovery", "rights", "security", "accessibility", "design", "performance", "cost", "ci", "rollback", "independent_review")
ROOT = Path(__file__).resolve().parents[1]


def fresh(stamp: object, now: datetime, seconds: int = 86400) -> bool:
    if not isinstance(stamp, str):
        return False
    try:
        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and -60 <= (now - parsed).total_seconds() <= seconds
    except (ValueError, TypeError, OverflowError):
        return False


def safe_url(value: object) -> bool:
    if not isinstance(value, str) or len(value) > 2048 or any(ord(c) < 33 or 127 <= ord(c) <= 159 for c in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password and not parsed.query
    except ValueError:
        return False


def valid_receipt(value: object, revision: str, now: datetime) -> bool:
    return isinstance(value, dict) and bool(re.fullmatch(r"[a-f0-9]{40}", revision)) and value.get("result") == "pass" and value.get("revision") == revision and fresh(value.get("observed_at"), now) and safe_url(value.get("uri"))


def assess_site(site: dict, evidence: object, now: datetime) -> dict:
    data = evidence if isinstance(evidence, dict) else {}
    revision = data.get("source_revision", "")
    revision = revision if isinstance(revision, str) else ""
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    missing = [gate for gate in QUALITY_GATES if not valid_receipt(checks.get(gate), revision, now)]
    review = checks.get("independent_review") if isinstance(checks.get("independent_review"), dict) else {}
    builder = data.get("builder")
    try:
        if not isinstance(builder, str) or not builder.strip() or not isinstance(review.get("evaluator"), str):
            raise ValueError("missing builder")
        assert_independent_evaluator(review.get("evaluator"), worker=builder, queen="queen")
    except (ValueError, TypeError):
        missing.append("independent evaluator identity")
    provider = review.get("provider")
    builder_provider = data.get("builder_provider")
    placeholders = {"", "unknown", "none", "tbd", "unassigned"}
    if not isinstance(provider, str) or not isinstance(builder_provider, str) or provider.strip().lower() in placeholders or builder_provider.strip().lower() in placeholders or provider.strip().lower() == builder_provider.strip().lower():
        missing.append("independent provider identity")
    cost = checks.get("cost") if isinstance(checks.get("cost"), dict) else {}
    amount = cost.get("actual_cost_usd")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0:
        missing.append("measured cost")
    deployment = data.get("deployment") if isinstance(data.get("deployment"), dict) else {}
    deployment_ok = deployment.get("state") == "READY" and deployment.get("target") == "production" and deployment.get("revision") == revision and fresh(deployment.get("observed_at"), now) and safe_url(deployment.get("url"))
    if deployment_ok:
        deployment_ok = urlsplit(deployment["url"]).hostname in (site["domain"], "www." + site["domain"])
    if not deployment_ok:
        missing.append("production deployment")
    journey = data.get("production_journey")
    if not valid_receipt(journey, revision, now) or journey.get("domain", site["domain"]) != site["domain"]:
        missing.append("production customer journey")
    return {"domain": site["domain"], "repository": site["repository"], "team": site["team"], "customer_result": site["customer_result"],
            "source_revision": revision or None, "supplied_evidence_state": "incomplete" if missing else "complete", "missing_or_invalid": missing,
            "production_verification": "not_performed_by_this_tool", "dispatch_state": "not_dispatched"}


def assess_capacity(value: object, now: datetime) -> dict:
    data = value if isinstance(value, dict) else {}
    if not fresh(data.get("timestamp"), now, 900):
        return {"state": "unknown", "reason": "missing or expired capacity observation"}
    numbers = (data.get("disk_free_pct"), data.get("disk_free_gib"))
    if any(isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n < 0 for n in numbers):
        return {"state": "unknown", "reason": "disk observation incomplete"}
    if numbers[0] > 100:
        return {"state": "unknown", "reason": "disk percentage is invalid"}
    if numbers[0] < 8 or numbers[1] < 50 or data.get("decision") in ("hold", "bounded"):
        return {"state": "hold", "reason": "disk floor or supplied PP constraint"}
    if data.get("decision") != "allow":
        return {"state": "unknown", "reason": "PP decision unknown"}
    return {"state": "allow-reported", "reason": "revalidate actual host, owner, budget and action before execution"}


def make_packet(site: dict) -> dict:
    packet = envelope_template(site["customer_result"], queen="existing-starlight-coordinator", worker="unassigned", evaluator="required-independent", budget_usd=0, max_turns=20)
    packet["status"] = "held"
    packet["autonomy"]["effective"] = None
    packet["autonomy"]["notes"] = "No effective authority is assigned; the owning host must establish it."
    packet["budget"]["wall_time_minutes"] = 45
    packet["scope"]["repository_full_name"] = site["repository"]
    packet["non_goals"] = ["No new queue or scheduler", "No provider, deployment or paid infrastructure call", "No ownership or grant assertion"]
    packet["stop_conditions"] += ["no execution authority", "missing exact owned files", "missing fresh host and budget admission"]
    packet["acceptance"]["customer_result"] = site["customer_result"]
    packet["envelope_hash"] = body_hash(packet, "envelope_hash")
    return packet


def read_json(path: Path) -> object:
    with path.open("rb") as stream:
        content = stream.read(2_097_153)
    if len(content) > 2_097_152:
        raise ValueError("input exceeds 2 MiB")
    return json.loads(content.decode("utf-8-sig"), parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON number")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "ops/plans/software-factory-2026-10-16/sites.json")
    parser.add_argument("--evidence", type=Path, help="Supplied site receipts and capacity; no network verification is performed")
    parser.add_argument("--packet", help="Emit a held existing-format mission envelope for one domain, to stdout only")
    args = parser.parse_args(argv)
    try:
        catalog = read_json(args.catalog)
        if not isinstance(catalog, dict) or not isinstance(catalog.get("sites"), list) or not catalog["sites"]:
            raise ValueError("catalog needs a nonempty sites array")
        sites = catalog["sites"]
        domains = []
        for site in sites:
            if not isinstance(site, dict) or any(not isinstance(site.get(k), str) or not site[k].strip() for k in ("domain", "repository", "team", "customer_result")):
                raise ValueError("every site needs domain, repository, team and customer_result")
            domains.append(site["domain"])
        if len(set(domains)) != len(domains):
            raise ValueError("catalog has duplicate domains")
        evidence = read_json(args.evidence) if args.evidence else {}
        if not isinstance(evidence, dict) or not isinstance(evidence.get("sites", {}), dict):
            raise ValueError("evidence needs an object with site receipts keyed by domain")
        now = datetime.now(timezone.utc)
        if args.packet:
            site = next((s for s in sites if s["domain"] == args.packet), None)
            if site is None:
                raise ValueError("domain is not in the inspected catalog")
            result = make_packet(site)
        else:
            result = {"schema": "starlight.software-factory-evidence-gaps.v1", "observed_at": now.isoformat(), "registry_revision": catalog.get("registry_revision"),
                      "assurance": "supplied observations only; not live release attestation", "capacity": assess_capacity(evidence.get("capacity"), now),
                      "sites": [assess_site(s, evidence.get("sites", {}).get(s["domain"], {}), now) for s in sites]}
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc), "state": "unknown"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
