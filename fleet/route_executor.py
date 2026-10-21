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
- Budget: preflight() refuses a paid model when the month's paid spend, the live
  reservations and the estimate would pass token_pass.hard_cap_usd. reserve()
  does the same check and records the reservation in one locked step, so two
  callers cannot both be admitted into the same headroom; record_receipt()
  settles the reservation, and only a receipt for the same class and model can.
  A hold older than RESERVATION_TTL_S is reported as expired-unsettled but keeps
  counting against the cap (the call may still be running) until a late
  settlement replaces it or release_reservation() reconciles it.
- Shared budget: paid calls are refused when the schema's receipts root cannot
  be used on this OS, because each checkout would otherwise keep its own ledger.
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
from decimal import ROUND_CEILING, Decimal
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "routing.schema.json"
DEFAULT_RECEIPTS_DIR = Path(__file__).resolve().parent / "receipts"
LOCK_TIMEOUT_S = 10.0
RESERVATION_TTL_S = 1800


class BudgetError(ValueError):
    """Raised when a paid call would pass the Token Pass hard cap."""


class LedgerBusy(BudgetError):
    """The ledger lock could not be taken in time; the paid call is not admitted."""


MICRO = Decimal("0.000001")
MAX_SANE_USD = 1_000_000.0  # no single call or receipt is worth more; larger is corrupt input


def _finite_number(x) -> bool:
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    try:
        return math.isfinite(float(x)) and abs(float(x)) <= MAX_SANE_USD
    except OverflowError:
        return False


def _ceil6(x: float) -> float:
    """Round up to a whole micro-dollar, never below one."""
    return max(float(Decimal(repr(float(x))).quantize(MICRO, rounding=ROUND_CEILING)), 0.000001)


def _micros(x: float) -> int:
    return int(round(x * 1_000_000))


def receipts_dir() -> Path:
    """Ledger directory. Order: STARLIGHT_RECEIPTS_DIR (tests, dry runs), then the
    schema's receipts.root so every worktree shares one budget, then this checkout
    (only when the schema root is missing or not an absolute path on this OS)."""
    override = os.environ.get("STARLIGHT_RECEIPTS_DIR")
    if override:
        return Path(override)
    return _schema_root() or DEFAULT_RECEIPTS_DIR


def _schema_root() -> Path | None:
    try:
        root = load_schema().get("receipts", {}).get("root")
    except (FileNotFoundError, ValueError):
        return None
    if isinstance(root, str) and root:
        path = Path(os.path.expandvars(root)).expanduser()
        if path.is_absolute():
            return path
    return None


def shared_root_usable() -> bool:
    """True when every checkout on this machine resolves to one ledger: either
    STARLIGHT_RECEIPTS_DIR is set or the schema root is absolute on this OS."""
    return bool(os.environ.get("STARLIGHT_RECEIPTS_DIR")) or _schema_root() is not None


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
    return isinstance(model, str) and model in zdr_models(schema)


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
        except (ValueError, RecursionError):  # JSONDecodeError, int-conversion limit
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
        except (KeyError, ValueError, TypeError, OverflowError):
            continue
        if ts.year == now.year and ts.month == now.month and is_paid(r.get("used", ""), schema) \
                and math.isfinite(cost) and 0 <= cost <= MAX_SANE_USD:
            total += cost
    return total


def reservations(now: datetime | None = None) -> list[dict]:
    """Open holds: reserved and neither settled nor released. A hold past
    RESERVATION_TTL_S is "expired-unsettled": it still counts against the cap."""
    now = now or datetime.now(timezone.utc)
    reserves: dict[str, dict] = {}
    closed: set[str] = set()
    for e in _read_receipts(receipts_dir() / "reservations.jsonl"):
        try:
            if e["kind"] in ("settle", "release"):
                closed.add(str(e["id"]))
                continue
            ts = datetime.fromisoformat(e["ts"])
            est = float(e["est_cost_usd"])
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            rid = str(e["id"])
            hold = {"id": rid, "ts": ts, "est_cost_usd": est, "task_class": e.get("task_class"),
                    "model": e.get("model")}
        except (KeyError, ValueError, TypeError, AttributeError, OverflowError):
            continue
        if math.isfinite(est) and est >= 0:
            reserves[rid] = hold
    out = []
    for rid, h in reserves.items():
        if rid in closed:
            continue
        age = (now - h["ts"]).total_seconds()
        out.append({**h, "ts": h["ts"].isoformat(),
                    "status": "expired-unsettled" if age >= RESERVATION_TTL_S else "active"})
    return out


def reserved_usd(now: datetime | None = None) -> float:
    """Estimated spend held by open reservations, expired-unsettled ones included."""
    return sum(h["est_cost_usd"] for h in reservations(now))


def release_reservation(reservation_id: str, reason: str) -> dict:
    """Reconcile a hold whose call is known not to be running (or not to have spent)."""
    ledger = receipts_dir() / "routing.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with _locked(ledger):
        if not any(h["id"] == reservation_id for h in reservations()):
            raise ValueError(f"reservation '{reservation_id}' is unknown, already settled or released")
        event = {"kind": "release", "id": reservation_id, "ts": datetime.now(timezone.utc).isoformat(),
                 "reason": str(reason)[:200]}
        _append_unlocked(receipts_dir() / "reservations.jsonl", json.dumps(event, allow_nan=False))
    return event


def _admit(task_class: str, model: str, est_cost_usd: float | None, allow_non_zdr: bool) -> dict:
    """Pure admission check; raises on anything that should not run."""
    r = route(task_class, allow_non_zdr)
    if model not in r["chain"]:
        raise ValueError(f"model '{model}' is not allowed for '{task_class}': {r['chain']}")
    schema = load_schema()
    paid = is_paid(model, schema)
    if est_cost_usd is None:
        if paid:
            raise ValueError(f"'{model}' is a paid model: pass an explicit positive estimate")
        est_cost_usd = 0.0
    if not _finite_number(est_cost_usd) or est_cost_usd < 0:
        raise ValueError("est_cost_usd must be a finite non-negative number")
    if paid and est_cost_usd == 0:
        raise ValueError(f"'{model}' is a paid model: the estimate must be greater than zero")
    if paid:
        est_cost_usd = _ceil6(est_cost_usd)  # what is held is never less than what was checked
        if not shared_root_usable():
            raise BudgetError(
                "paid calls are refused: the schema receipts.root is not an absolute path on this OS and "
                "STARLIGHT_RECEIPTS_DIR is unset, so this checkout would keep its own budget instead of "
                "the shared one. Set STARLIGHT_RECEIPTS_DIR to the shared ledger directory.")
    if est_cost_usd > r["cost_ceiling_usd"]:
        raise BudgetError(
            f"estimate ${est_cost_usd} exceeds the ${r['cost_ceiling_usd']} ceiling for '{task_class}'")
    tp = schema.get("token_pass", {})
    status = {"model": model, "month_paid_spend_usd": 0.0, "reserved_usd": 0.0, "soft_alert": False,
              "reservation_id": None, "held_usd": est_cost_usd if paid else 0.0}
    if paid:
        spent, held = month_paid_spend(), reserved_usd()
        cap = tp.get("hard_cap_usd", float("inf"))
        status["month_paid_spend_usd"] = round(spent, 6)
        status["reserved_usd"] = round(held, 6)
        spent_m, held_m, est_m, cap_m = _micros(spent), _micros(held), _micros(est_cost_usd), _micros(cap)
        if spent_m + held_m >= cap_m or spent_m + held_m + est_m > cap_m:
            raise BudgetError(
                f"month spend ${spent:.4f} + reserved ${held:.4f} + ${est_cost_usd} would pass the "
                f"${cap} Token Pass hard cap")
        status["soft_alert"] = spent + held + est_cost_usd >= tp.get("soft_alert_usd", float("inf"))
    return status


def preflight(task_class: str, model: str, est_cost_usd: float | None = None,
              allow_non_zdr: bool = False) -> dict:
    """Check a call BEFORE it is made, without holding any headroom."""
    return _admit(task_class, model, est_cost_usd, allow_non_zdr)


def reserve(task_class: str, model: str, est_cost_usd: float | None = None,
            allow_non_zdr: bool = False) -> dict:
    """Admit a call and hold its estimate against the cap until record_receipt()
    settles it. Check and hold happen under one lock, so concurrent callers
    cannot be admitted into the same headroom."""
    ledger = receipts_dir() / "routing.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    try:
        with _locked(ledger):
            status = _admit(task_class, model, est_cost_usd, allow_non_zdr)
            if is_paid(model, load_schema()):
                rid = uuid.uuid4().hex[:12]
                held = status["held_usd"]
                event = {"kind": "reserve", "id": rid, "ts": datetime.now(timezone.utc).isoformat(),
                         "model": model, "task_class": task_class, "est_cost_usd": held}
                _append_unlocked(receipts_dir() / "reservations.jsonl", json.dumps(event, allow_nan=False))
                status["reservation_id"] = rid
                status["reserved_usd"] = round(status["reserved_usd"] + held, 6)
    except TimeoutError as e:
        raise LedgerBusy(f"ledger busy, paid call not admitted: {e}") from e
    return status


@contextlib.contextmanager
def _locked(path: Path):
    """Exclusive cross-process lock on a sidecar file (Windows and POSIX)."""
    lock_path = path.with_name(path.name + ".lock")
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT)
    try:
        timeout = float(os.environ.get("STARLIGHT_LOCK_TIMEOUT_S", LOCK_TIMEOUT_S))
    except ValueError:
        timeout = LOCK_TIMEOUT_S
    if not math.isfinite(timeout) or timeout <= 0:
        timeout = LOCK_TIMEOUT_S
    deadline = time.monotonic() + timeout
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


def _append_unlocked(path: Path, line: str) -> None:
    """One binary write, LF endings. The caller must hold _locked on the ledger."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (line + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0))
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)


def append_line(path: Path, line: str) -> None:
    """Append one line under the lock, LF endings, exactly one write call."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with _locked(path):
        _append_unlocked(path, line)


def record_receipt(task_class: str, used: str, fallback_used: bool,
                   cost_usd: float, latency_ms: int, success: bool,
                   provider: str = "", machine: str = "",
                   allow_non_zdr: bool = False, synthetic: bool = False,
                   reservation_id: str | None = None) -> dict:
    """Append a routing receipt (jsonl) and return it. A reservation_id from
    reserve() is settled in the same locked step.

    Spend that already happened is always recorded. A cost over the class
    ceiling is flagged over_ceiling rather than refused, so the ledger and the
    weekly review can see it.
    """
    r = route(task_class, allow_non_zdr)  # validates up front
    if used not in r["chain"]:
        raise ValueError(f"used model '{used}' is not in the chain for '{task_class}': {r['chain']}")
    if not _finite_number(cost_usd) or cost_usd < 0:
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
        "cost_usd": _ceil6(cost_usd) if cost_usd > 0 else 0.0,  # a real cost never rounds to zero
        "latency_ms": latency_ms,
        "success": bool(success),
        "provider": provider,
        "machine": machine,
        "over_ceiling": cost_usd > r["cost_ceiling_usd"],
        "zdr_override": bool(allow_non_zdr and r["zdr_required"] and not is_paid(used, load_schema())),
        "synthetic": bool(synthetic),
    }
    ledger = receipts_dir() / "routing.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with _locked(ledger):
        if reservation_id:
            hold = next((h for h in reservations() if h["id"] == reservation_id), None)
            if hold is None:
                raise ValueError(f"reservation '{reservation_id}' is unknown, already settled or released")
            if hold["task_class"] != task_class or hold["model"] != used:
                raise ValueError(
                    f"reservation '{reservation_id}' was made for {hold['task_class']}/{hold['model']}, "
                    f"not {task_class}/{used}; nothing was recorded")
        _append_unlocked(ledger, json.dumps(receipt, allow_nan=False))
        if reservation_id:
            settle = {"kind": "settle", "id": reservation_id, "ts": receipt["ts"]}
            _append_unlocked(receipts_dir() / "reservations.jsonl", json.dumps(settle, allow_nan=False))
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
