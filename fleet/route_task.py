#!/usr/bin/env python3
"""Starlight one-shot router: task description -> routing decision.

Combines route_classifier + route_executor. Prints the chosen model + fallback
chain. Flow around a call:

  1. route_task.py "<task>" --preflight --est-cost 0.02   (before the call)
  2. make the call with the chosen model
  3. route_task.py "<task>" --record success --used <model> --cost <usd> --latency <ms>

Exit codes: 0 ok, 2 rejected input, 3 receipt recorded but cost passed the
class ceiling (the spend is in the ledger; treat the route as needing review).
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from route_classifier import classify
from route_executor import BudgetError, preflight, record_receipt, route


def _fail(msg: str, code: int = 2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description="Route a task to a model.")
    ap.add_argument("task", nargs="+", help="Task description")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-non-zdr", action="store_true",
                    help="Let ZDR-required classes fall back to non-ZDR (free) models; stamped on the receipt")
    ap.add_argument("--preflight", action="store_true", help="Check a planned call against ceiling and budget")
    ap.add_argument("--est-cost", type=float, default=0.0, help="Estimated cost USD for --preflight")
    ap.add_argument("--record", choices=["success", "fail"], help="Record a receipt")
    ap.add_argument("--used", help="Model actually used (required with --record/--preflight)")
    ap.add_argument("--cost", type=float, default=None, help="Cost USD (required with --record)")
    ap.add_argument("--latency", type=int, default=None, help="Latency ms (required with --record)")
    ap.add_argument("--provider", default="", help="Resolved provider")
    ap.add_argument("--synthetic", action="store_true", help="Mark the receipt as a test; reviews skip it")
    args = ap.parse_args()

    task = " ".join(args.task)

    try:
        c = classify(task)
        r = route(c["class"], args.allow_non_zdr)
    except (FileNotFoundError, ValueError, KeyError) as e:
        _fail(str(e))

    if args.preflight:
        model = args.used or r["primary"]
        try:
            status = preflight(c["class"], model, args.est_cost, args.allow_non_zdr)
        except BudgetError as e:
            _fail(str(e))
        except ValueError as e:
            _fail(str(e))
        print(json.dumps({"class": c["class"], **status}))
        return

    if args.record:
        if not args.used:
            _fail("--record requires --used")
        if args.cost is None or args.latency is None:
            _fail("--record requires --cost and --latency")
        if args.used not in r["chain"]:
            _fail(f"--used '{args.used}' not in chain {r['chain']}")
        try:
            receipt = record_receipt(c["class"], args.used, args.used != r["primary"], args.cost,
                                     args.latency, args.record == "success", args.provider,
                                     allow_non_zdr=args.allow_non_zdr, synthetic=args.synthetic)
        except (ValueError, FileNotFoundError, TimeoutError) as e:
            _fail(str(e))
        print(f"receipt recorded: class={c['class']} used={args.used} success={args.record == 'success'}")
        if receipt["over_ceiling"]:
            print(f"warning: cost ${receipt['cost_usd']} passed the ${r['cost_ceiling_usd']} ceiling for "
                  f"'{c['class']}'; recorded as over_ceiling", file=sys.stderr)
            sys.exit(3)
        return

    out = {
        "task": task,
        "class": c["class"],
        "source": c["source"],
        "primary": r["primary"],
        "variant": r["variant"],
        "fallbacks": r["fallbacks"],
        "chain": r["chain"],
        "zdr_excluded": r["zdr_excluded"],
        "cost_ceiling_usd": r["cost_ceiling_usd"],
        "zdr_required": r["zdr_required"],
    }
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"class={out['class']} ({out['source']})")
        print(f"primary={out['primary']}  variant={out['variant']}")
        print(f"fallbacks={out['fallbacks']}")
        if out["zdr_excluded"]:
            print(f"excluded (not ZDR): {out['zdr_excluded']}  (use --allow-non-zdr to include)")
        print(f"cost_ceiling=${out['cost_ceiling_usd']}  zdr={out['zdr_required']}")


if __name__ == "__main__":
    main()
