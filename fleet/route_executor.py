#!/usr/bin/env python3
"""Starlight route executor: given a task class, return the model to use and
walk the fallback chain. Emits a routing receipt (jsonl) per execution.

This module is the *decision* layer. Actual LLM calls happen elsewhere (OpenCode
subagent tool / OmO). The executor returns the chosen model + fallbacks so the
caller can invoke and report back success/failure via record_receipt().

Policy enforced here (not just documented):
- ZDR: a class with zdr_required only walks models listed under token_pass
  (zero data retention). Free/non-ZDR fallbacks are excluded unless the caller
  passes allow_non_zdr=True, which is stamped on the receipt.
- Budget: preflight() refuses a paid model when the month's paid spend plus the
  estimate would pass token_pass.hard_cap_usd.
- Ledger: an over-ceiling cost is still recorded (flagged over_ceiling) so the
  ledger sees the events the ceiling exists to catch.
"""
import contextlib
import json
import math
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "routing.schema.json"
DEFAULT_RECEIPTS_DIR = Path(__file__).resolve().parent / "receipts"
LOCK_TIMEOUT_S = 10.0


class BudgetError(ValueError):
    """Raised when a paid call would pass the Token Pass hard cap."""


def receipts_dir() -> Path:
    override = os.environ.get("STARLIGHT_RECEIPTS_DIR")
    return Path(override) if override else DEFAULT_RECEIPTS_DIR


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"routing schema not found: {SCHEMA_PATH}")
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"malformed routing schema: {e}") from e


def zdr_models(schema: dict) -> set[str]:
    """Models that retain no data: everything priced under token_pass."""
    return set(schema.get("token_pass", {}).get("models", {}))


def is_paid(model: str, schema: dict) -> bool:
    return model in zdr_models(schema)


def zdr_safe_chain(schema: dict, task_class: str) -> list[str]:
    """Full chain for a class, restricted to ZDR models when the class needs it."""
    d = schema["task_classes"][task_class]
    chain = [d["primary"]] + list(d["fallbacks"])
    if d["zdr_required"]:
        safe = zdr_models(schema)
        chain = [m for m in chain if m in safe]
    seen, out = set(), []
    for m in chain:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def route(task_class: str, allow_non_zdr: bool = False) -> dict:
    schema = load_schema()
    if task_class not in schema.get("task_classes", {}):
        raise ValueError(f"Unknown task class: {task_class}")
    route_def = schema["task_classes"][task_class]
    required = ("primary", "variant", "fallbacks", "cost_ceiling_usd", "zdr_required")
    for k in required:
        if k not in route_def:
            raise ValueError(f"task class '{task_class}' missing field: {k}")
    full = [route_def["primary"]] + list(route_def["fallbacks"])
    chain = full if allow_non_zdr else zdr_safe_chain(schema, task_class)
    excluded = [m for m in full if m not in chain]
    return {
        "task_class": task_class,
        "primary": route_def["primary"],
        "variant": route_def["variant"],
        "fallbacks": [m for m in chain if m != route_def["primary"]],
        "cost_ceiling_usd": route_def["cost_ceiling_usd"],
        "zdr_required": route_def["zdr_required"],
        "chain": chain,
        "zdr_excluded": excluded,
        "allow_non_zdr": allow_non_zdr,
    }


def pick_next(failed: list[str], task_class: str, allow_non_zdr: bool = False) -> str | None:
    """Walk the fallback chain, skipping already-failed models.

    Returns None when the entire chain is exhausted; callers MUST handle None
    (do not dereference the result without a guard).
    """
    r = route(task_class, allow_non_zdr)
    for m in r["chain"]:
        if m not in failed:
            return m
    return None


def _read_receipts(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def month_paid_spend(now: datetime | None = None) -> float:
    """Token Pass spend recorded in the ledger for the current UTC month."""
    now = now or datetime.now(timezone.utc)
    schema = load_schema()
    total = 0.0
    for r in _read_receipts(receipts_dir() / "routing.jsonl"):
        try:
            ts = datetime.fromisoformat(r["ts"])
            cost = float(r["cost_usd"])
        except (KeyError, ValueError, TypeError):
            continue
        if ts.year == now.year and ts.month == now.month and is_paid(r.get("used", ""), schema) \
                and math.isfinite(cost):
            total += cost
    return total


def preflight(task_class: str, model: str, est_cost_usd: float,
              allow_non_zdr: bool = False) -> dict:
    """Check a call BEFORE it is made. Raises on anything that should not run."""
    if not math.isfinite(est_cost_usd) or est_cost_usd < 0:
        raise ValueError("est_cost_usd must be a finite non-negative number")
    r = route(task_class, allow_non_zdr)
    if model not in r["chain"]:
        raise ValueError(f"model '{model}' is not allowed for '{task_class}': {r['chain']}")
    if est_cost_usd > r["cost_ceiling_usd"]:
        raise BudgetError(
            f"estimate ${est_cost_usd} exceeds the ${r['cost_ceiling_usd']} ceiling for '{task_class}'")
    schema = load_schema()
    tp = schema.get("token_pass", {})
    status = {"model": model, "month_paid_spend_usd": 0.0, "soft_alert": False}
    if is_paid(model, schema):
        spent = month_paid_spend()
        status["month_paid_spend_usd"] = round(spent, 6)
        if spent + est_cost_usd > tp.get("hard_cap_usd", float("inf")):
            raise BudgetError(
                f"month spend ${spent:.4f} + ${est_cost_usd} would pass the "
                f"${tp['hard_cap_usd']} Token Pass hard cap")
        status["soft_alert"] = spent + est_cost_usd >= tp.get("soft_alert_usd", float("inf"))
    return status


@contextlib.contextmanager
def _locked(path: Path):
    """Exclusive cross-process lock on a sidecar file (Windows and POSIX)."""
    lock_path = path.with_name(path.name + ".lock")
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT)
    deadline = time.monotonic() + LOCK_TIMEOUT_S
    try:
        if os.name == "nt":
            import msvcrt
            while True:
                try:
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise TimeoutError(f"could not lock {lock_path}")
                    time.sleep(0.005)
        else:
            import fcntl
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise TimeoutError(f"could not lock {lock_path}")
                    time.sleep(0.005)
        yield
    finally:
        try:
            if os.name == "nt":
                import msvcrt
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        os.close(fd)


def append_line(path: Path, line: str) -> None:
    """Append one line under the lock, LF endings, exactly one write call."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (line + "\n").encode("utf-8")
    with _locked(path):
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0))
        try:
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)


def record_receipt(task_class: str, used: str, fallback_used: bool,
                   cost_usd: float, latency_ms: int, success: bool,
                   provider: str = "", machine: str = "",
                   allow_non_zdr: bool = False, synthetic: bool = False) -> dict:
    """Append a routing receipt (jsonl) and return it.

    Spend that already happened is always recorded. A cost over the class
    ceiling is flagged over_ceiling rather than refused, so the ledger and the
    weekly review can see it.
    """
    r = route(task_class, allow_non_zdr)  # validates up front
    if used not in r["chain"]:
        raise ValueError(f"used model '{used}' is not in the chain for '{task_class}': {r['chain']}")
    if not isinstance(cost_usd, (int, float)) or not math.isfinite(cost_usd) or cost_usd < 0:
        raise ValueError("cost_usd must be a finite non-negative number")
    if not isinstance(latency_ms, int) or isinstance(latency_ms, bool) or latency_ms < 0:
        raise ValueError("latency_ms must be a non-negative integer")
    machine = machine or os.environ.get("STARLIGHT_MACHINE", "unknown")
    receipt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "id": uuid.uuid4().hex[:12],
        "task_class": task_class,
        "primary": r["primary"],
        "used": used,
        "fallback_used": fallback_used,
        "cost_usd": round(cost_usd, 6),
        "latency_ms": latency_ms,
        "success": bool(success),
        "provider": provider,
        "machine": machine,
        "over_ceiling": cost_usd > r["cost_ceiling_usd"],
        "zdr_override": bool(allow_non_zdr and r["zdr_required"] and not is_paid(used, load_schema())),
        "synthetic": bool(synthetic),
    }
    append_line(receipts_dir() / "routing.jsonl", json.dumps(receipt, allow_nan=False))
    return receipt


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Route a task class to a model chain.")
    ap.add_argument("task_class", help="Task class (scout/review/bulk/code/hard-reasoning/vision/ultrabrain)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-non-zdr", action="store_true",
                    help="Include non-ZDR fallbacks for ZDR-required classes (stamped on receipts)")
    args = ap.parse_args()
    try:
        r = route(args.task_class, args.allow_non_zdr)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=__import__("sys").stderr)
        raise SystemExit(2)
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"class={args.task_class}  primary={r['primary']}  variant={r['variant']}  fallbacks={r['fallbacks']}")


if __name__ == "__main__":
    main()
