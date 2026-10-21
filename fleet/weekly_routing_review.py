#!/usr/bin/env python3
"""Weekly routing review: parse routing receipts, propose routing diffs.
Writes fleet/routing-proposals/YYYY-MM-DD.json for human approval.
Never auto-commits (money/merges stay on the human's button).

Receipts are read tolerantly: torn or malformed lines, unknown classes and
non-finite numbers are skipped and counted, never fatal. Synthetic (test)
receipts are ignored. A proposal must name a model that is already in the
class's ZDR-safe chain, and both models need a per-model sample floor.
"""
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from route_executor import receipts_dir, zdr_safe_chain

HERE = Path(__file__).resolve().parent
PROPOSALS = HERE / "routing-proposals"
SCHEMA = HERE / "routing.schema.json"
DEFAULT_MIN_SAMPLES = 20
MIN_MODEL_SAMPLES = 5
REQUIRED = ("ts", "task_class", "used", "success", "cost_usd", "latency_ms")


def load_receipts(path: Path | None = None, days: int = 7, now: datetime | None = None) -> tuple[list[dict], dict]:
    path = path or receipts_dir() / "routing.jsonl"
    skipped = {"malformed": 0, "incomplete": 0, "synthetic": 0, "non_finite": 0}
    if not path.exists():
        return [], skipped
    now = now or datetime.now(timezone.utc)
    cutoff = now.timestamp() - days * 86400
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            skipped["malformed"] += 1
            continue
        if not isinstance(r, dict) or any(k not in r for k in REQUIRED):
            skipped["incomplete"] += 1
            continue
        if r.get("synthetic"):
            skipped["synthetic"] += 1
            continue
        try:
            ts = datetime.fromisoformat(r["ts"])
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            cost, latency = float(r["cost_usd"]), float(r["latency_ms"])
        except (ValueError, TypeError):
            skipped["malformed"] += 1
            continue
        if not (math.isfinite(cost) and math.isfinite(latency)):
            skipped["non_finite"] += 1
            continue
        if ts.timestamp() >= cutoff:
            out.append({**r, "cost_usd": cost, "latency_ms": latency})
    return out, skipped


def analyze(receipts: list[dict], schema: dict) -> dict:
    min_samples = schema.get("feedback_loop", {}).get("min_samples_per_class", DEFAULT_MIN_SAMPLES)
    known = schema["task_classes"]
    by_class = defaultdict(lambda: {"n": 0, "success": 0, "cost": 0.0, "latency": 0.0, "over": 0,
                                    "models": defaultdict(lambda: {"n": 0, "success": 0, "cost": 0.0})})
    for r in receipts:
        if r["task_class"] not in known:
            continue
        c = by_class[r["task_class"]]
        c["n"] += 1
        c["success"] += int(bool(r["success"]))
        c["cost"] += r["cost_usd"]
        c["latency"] += r["latency_ms"]
        c["over"] += int(bool(r.get("over_ceiling")))
        m = c["models"][r["used"]]
        m["n"] += 1
        m["success"] += int(bool(r["success"]))
        m["cost"] += r["cost_usd"]

    result = {}
    for cls, d in by_class.items():
        models = {
            m: {
                "n": md["n"],
                "success_rate": round(md["success"] / md["n"], 3),
                "avg_cost_usd": round(md["cost"] / md["n"], 6),
            }
            for m, md in d["models"].items()
        }
        result[cls] = {
            "samples": d["n"],
            "success_rate": round(d["success"] / d["n"], 3),
            "avg_cost_usd": round(d["cost"] / d["n"], 6),
            "avg_latency_ms": round(d["latency"] / d["n"], 1),
            "over_ceiling": d["over"],
            "meets_min_samples": d["n"] >= min_samples,
            "models": models,
        }
    return result


def propose(analysis: dict, schema: dict) -> list[dict]:
    """Conservative: propose a new primary only when both it and the current
    primary have at least MIN_MODEL_SAMPLES, the target is already in the
    class's ZDR-safe chain, and it is clearly better."""
    proposals = []
    for cls, d in analysis.items():
        if not d["meets_min_samples"]:
            continue
        current = schema["task_classes"][cls]["primary"]
        allowed = set(zdr_safe_chain(schema, cls))
        cur = d["models"].get(current)
        if not cur or cur["n"] < MIN_MODEL_SAMPLES:
            continue
        candidates = [
            (m, s) for m, s in d["models"].items()
            if m != current and m in allowed and s["n"] >= MIN_MODEL_SAMPLES
        ]
        if not candidates:
            continue
        best, bs = sorted(candidates, key=lambda kv: (-kv[1]["success_rate"], kv[1]["avg_cost_usd"]))[0]
        if bs["success_rate"] > cur["success_rate"] + 0.02:
            reason = f"success_rate {bs['success_rate']} vs {cur['success_rate']} (n={bs['n']} vs {cur['n']})"
        elif (abs(bs["success_rate"] - cur["success_rate"]) < 0.02
              and bs["avg_cost_usd"] < cur["avg_cost_usd"] * 0.8):
            reason = f"equal success, lower cost ${bs['avg_cost_usd']} vs ${cur['avg_cost_usd']}"
        else:
            continue
        proposals.append({"class": cls, "action": "reroute_primary", "from": current, "to": best, "reason": reason})
    return proposals


def main():
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    receipts, skipped = load_receipts()
    analysis = analyze(receipts, schema)
    proposals = propose(analysis, schema)
    now = datetime.now(timezone.utc)

    report = {
        "generated": now.isoformat(),
        "window_days": 7,
        "receipt_count": len(receipts),
        "skipped": skipped,
        "analysis": analysis,
        "proposals": proposals,
        "note": "Proposals require human approval. Apply manually to routing.schema.json + regenerate OmO config. Never auto-commit.",
    }
    out_path = PROPOSALS / f"{now.date().isoformat()}.json"
    out_path.write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Receipts: {len(receipts)}  Skipped: {sum(skipped.values())}  Classes analyzed: {len(analysis)}  Proposals: {len(proposals)}")
    for p in proposals:
        print(f"  PROPOSE: {p['class']}: {p['from']} -> {p['to']} ({p['reason']})")
    if not proposals:
        print("  No proposals (insufficient samples or current routing optimal).")


if __name__ == "__main__":
    main()
