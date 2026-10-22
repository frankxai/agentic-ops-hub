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
- Free routing is opt-in: a class that does not require ZDR (scout, review, vision)
  lists opencode/*-free models, which run on OpenCode's endpoint and outside the
  Vercel gateway key. Unless the caller passes allow_free=True those classes are
  served by the cheapest ZDR gateway model with an explicit non-zero ceiling
  (the class's zdr_cost_ceiling_usd), so the gateway key covers the call and the
  ledger counts its cost. effective_route() is the one function that decides this;
  route(), the admission checks, record_receipt() and gen_omo_config all use it.
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
MAX_SANE_LATENCY_MS = 86_400_000  # one day; a longer single call is a corrupt receipt


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
    STARLIGHT_RECEIPTS_DIR is an absolute path or the schema root is absolute on
    this OS. A relative override means one ledger per working directory."""
    override = os.environ.get("STARLIGHT_RECEIPTS_DIR")
    if override:
        return Path(override).is_absolute()
    return _schema_root() is not None


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


POOL_TOKEN_PASS, POOL_FREE, POOL_OTHER = "token-pass", "free", "other"


def is_free_model(model: str, schema: dict) -> bool:
    """Explicitly free: listed under free_tier.models now, or named like a free model
    (so a retired free model is still recognised in old receipts)."""
    if not isinstance(model, str):
        return False
    listed = schema.get("free_tier", {}).get("models", {})
    return model in listed or model.endswith("-free")


def receipt_pool(used: str, cost_usd: float, schema: dict) -> str:
    """Which budget a call belongs to. Fail closed: only a zero-cost call on a free-marked
    model is "free"; a model outside the catalog that cost money is Token Pass spend."""
    if is_paid(used, schema) or cost_usd > 0:
        return POOL_TOKEN_PASS
    return POOL_FREE if is_free_model(used, schema) else POOL_OTHER


def counts_toward_token_pass(r: dict, schema: dict) -> bool:
    """Whether a stored receipt's cost belongs to the Token Pass month. Uses the receipt's own
    pool, so retiring a model from token_pass.models cannot erase what it already cost. A pool
    that is present but unreadable counts (conservative). A legacy receipt without a pool counts
    when it cost money and its model is not explicitly free."""
    if "pool" in r:
        pool = r["pool"]
        if pool in (POOL_FREE, POOL_OTHER):
            return False
        return True  # "token-pass", or anything malformed
    return is_paid(r.get("used", ""), schema) or not is_free_model(r.get("used", ""), schema)


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


def cheapest_zdr_model(schema: dict) -> str:
    """Cheapest model priced under token_pass.models (input + output per 1M), name breaks ties."""
    models = schema["token_pass"]["models"]
    return min(models, key=lambda m: (models[m]["input"] + models[m]["output"], m))


def effective_route(schema: dict, task_class: str, allow_non_zdr: bool = False,
                    allow_free: bool = False) -> dict:
    """The route a class actually gets: chain, primary and cost ceiling in one place.

    A class that does not require ZDR is served by the cheapest ZDR gateway model
    (ceiling zdr_cost_ceiling_usd, which must be positive) unless allow_free is set,
    in which case it keeps its own free chain and zero ceiling."""
    if task_class not in schema.get("task_classes", {}):
        raise ValueError(f"Unknown task class: {task_class}")
    route_def = schema["task_classes"][task_class]
    required = ("primary", "variant", "fallbacks", "cost_ceiling_usd", "zdr_required")
    for k in required:
        if k not in route_def:
            raise ValueError(f"task class '{task_class}' missing field: {k}")
    full = [route_def["primary"]] + list(route_def["fallbacks"])
    ceiling = route_def["cost_ceiling_usd"]
    replaced = not route_def["zdr_required"] and not allow_free
    if replaced:
        ceiling = route_def.get("zdr_cost_ceiling_usd")
        if not _finite_number(ceiling) or ceiling <= 0:
            raise ValueError(f"task class '{task_class}' needs a positive zdr_cost_ceiling_usd "
                             f"to be served without free models")
        chain = [cheapest_zdr_model(schema)]
    elif allow_non_zdr:
        chain = full
    else:
        chain = zdr_safe_chain(schema, task_class)
    if not chain:
        raise ValueError(f"task class '{task_class}' has no ZDR-safe model left in its chain; "
                         f"add a model to token_pass.models or pass allow_non_zdr")
    excluded = [m for m in full if m not in chain]
    primary = chain[0]  # never the raw schema primary: that model may have been filtered out
    return {
        "task_class": task_class,
        "primary": primary,
        "variant": route_def["variant"],
        "fallbacks": [m for m in chain if m != primary],
        "cost_ceiling_usd": ceiling,
        "zdr_required": route_def["zdr_required"],
        "chain": chain,
        "zdr_excluded": excluded,
        "allow_non_zdr": allow_non_zdr,
        "allow_free": allow_free,
        "free_replaced": replaced,
    }


def route(task_class: str, allow_non_zdr: bool = False, allow_free: bool = False) -> dict:
    return effective_route(load_schema(), task_class, allow_non_zdr, allow_free)


def pick_next(failed: list[str], task_class: str, allow_non_zdr: bool = False,
              allow_free: bool = False) -> str | None:
    """Walk the fallback chain, skipping already-failed models.

    Returns None when the entire chain is exhausted; callers MUST handle None
    (do not dereference the result without a guard).
    """
    r = route(task_class, allow_non_zdr, allow_free)
    for m in r["chain"]:
        if m not in failed:
            return m
    return None


def _read_receipts(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    # errors="replace": a torn multi-byte tail becomes one malformed line, not a crash
    for line in path.read_bytes().decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except (ValueError, RecursionError):  # JSONDecodeError, int-conversion limit
            continue
    return out


def _as_utc(ts: datetime) -> datetime:
    """Naive timestamps are UTC; aware ones are converted, so a month boundary never depends on the offset."""
    return ts.replace(tzinfo=timezone.utc) if ts.tzinfo is None else ts.astimezone(timezone.utc)


def month_paid_spend(now: datetime | None = None) -> float:
    """Token Pass spend recorded in the ledger for the current UTC month."""
    now = _as_utc(now or datetime.now(timezone.utc))
    schema = load_schema()
    total = 0.0
    for r in _read_receipts(receipts_dir() / "routing.jsonl"):
        try:
            ts = _as_utc(datetime.fromisoformat(r["ts"]))
            cost = float(r["cost_usd"])
        except (KeyError, ValueError, TypeError, OverflowError):
            continue
        if ts.year == now.year and ts.month == now.month and counts_toward_token_pass(r, schema) \
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
        if math.isfinite(est) and 0 <= est <= MAX_SANE_USD:
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


def _admit(task_class: str, model: str, est_cost_usd: float | None, allow_non_zdr: bool,
           allow_free: bool = False) -> dict:
    """Pure admission check; raises on anything that should not run."""
    r = route(task_class, allow_non_zdr, allow_free)
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
              allow_non_zdr: bool = False, allow_free: bool = False) -> dict:
    """Check a call BEFORE it is made, without holding any headroom."""
    return _admit(task_class, model, est_cost_usd, allow_non_zdr, allow_free)


def reserve(task_class: str, model: str, est_cost_usd: float | None = None,
            allow_non_zdr: bool = False, allow_free: bool = False) -> dict:
    """Admit a call and hold its estimate against the cap until record_receipt()
    settles it. Check and hold happen under one lock, so concurrent callers
    cannot be admitted into the same headroom."""
    ledger = receipts_dir() / "routing.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    try:
        with _locked(ledger):
            status = _admit(task_class, model, est_cost_usd, allow_non_zdr, allow_free)
            if is_paid(model, load_schema()):
                rid = uuid.uuid4().hex[:12]
                held = status["held_usd"]
                event = {"kind": "reserve", "id": rid, "ts": datetime.now(timezone.utc).isoformat(),
                         "model": model, "task_class": task_class, "est_cost_usd": held}
                holds = receipts_dir() / "reservations.jsonl"
                _append_unlocked(holds, json.dumps(event, allow_nan=False))
                if not _receipt_is_last_line(holds, rid):
                    raise OSError(f"hold {rid} could not be verified in {holds}; paid call not admitted")
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
    """One binary write, LF endings. The caller must hold _locked on the ledger.
    A file whose last byte is not a newline (a torn write) gets one first, so the
    new record never joins the torn fragment and disappears with it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (line + "\n").encode("utf-8")
    fd = os.open(path, os.O_RDWR | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0))
    try:
        size = os.fstat(fd).st_size
        if size:
            os.lseek(fd, size - 1, os.SEEK_SET)
            if os.read(fd, 1) != b"\n":
                data = b"\n" + data
        view = memoryview(data)
        while view:  # os.write may write fewer bytes than asked
            n = os.write(fd, view)
            if n <= 0:
                raise OSError(f"could not write to {path}")
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)


def _countable_receipt(r: dict) -> bool:
    """True when a stored receipt is complete and month_paid_spend() will count it:
    every field present and typed, a parseable timestamp, a finite cost in range."""
    try:
        _as_utc(datetime.fromisoformat(r["ts"]))  # the path month_paid_spend() takes; may overflow
        return (isinstance(r["id"], str) and isinstance(r["used"], str) and isinstance(r["task_class"], str)
                and _finite_number(r["cost_usd"]) and r["cost_usd"] >= 0
                and isinstance(r["latency_ms"], int) and not isinstance(r["latency_ms"], bool)
                and 0 <= r["latency_ms"] <= MAX_SANE_LATENCY_MS
                and isinstance(r["success"], bool) and isinstance(r["over_ceiling"], bool))
    except (KeyError, ValueError, TypeError, OverflowError):
        return False


def _sync_file(path: Path) -> None:
    """Flush a file to disk. Used before a retry closes a hold over a receipt that
    an earlier, interrupted attempt wrote."""
    fd = os.open(path, os.O_RDWR | getattr(os, "O_BINARY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _receipt_is_last_line(path: Path, record_id: str) -> bool:
    """True when the last line of the file parses and carries this record id.
    Called under the lock right after an append, so the last line is ours."""
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 8192))
            tail = f.read()
    except OSError:
        return False
    lines = [ln for ln in tail.splitlines() if ln.strip()]
    if not lines:
        return False
    try:
        rec = json.loads(lines[-1])
    except (ValueError, RecursionError):
        return False
    return isinstance(rec, dict) and rec.get("id") == record_id


def append_line(path: Path, line: str) -> None:
    """Append one line under the lock, LF endings, exactly one write call."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with _locked(path):
        _append_unlocked(path, line)


def record_receipt(task_class: str, used: str, fallback_used: bool,
                   cost_usd: float, latency_ms: int, success: bool,
                   provider: str = "", machine: str = "",
                   allow_non_zdr: bool = False, synthetic: bool = False,
                   reservation_id: str | None = None, allow_free: bool = False) -> dict:
    """Append a routing receipt (jsonl) and return it. A reservation_id from
    reserve() is settled in the same locked step.

    Spend that already happened is always recorded. A cost over the class
    ceiling is flagged over_ceiling rather than refused, so the ledger and the
    weekly review can see it.
    """
    # New admissions are checked against the CURRENT chain. A settlement of an existing hold is
    # checked against the hold's own (class, model) binding below, so a model that was retired
    # between reserve() and settle still records the money that was really spent.
    r = None
    try:
        r = route(task_class, allow_non_zdr, allow_free)
    except ValueError:
        if not reservation_id:
            raise
    if r is None or used not in r["chain"]:
        if not reservation_id:
            raise ValueError(f"used model '{used}' is not in the chain for '{task_class}': {r['chain']}")
        # the reservation lookup inside the lock refuses this unless the hold names the same class and model
        if r is None:
            r = {"primary": used, "chain": [used], "cost_ceiling_usd": float("inf"), "zdr_required": False}
    if not _finite_number(cost_usd) or cost_usd < 0:
        raise ValueError("cost_usd must be a finite non-negative number")
    if not isinstance(latency_ms, int) or isinstance(latency_ms, bool) or not 0 <= latency_ms <= MAX_SANE_LATENCY_MS:
        raise ValueError(f"latency_ms must be an integer from 0 to {MAX_SANE_LATENCY_MS}")
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
        "reservation_id": reservation_id or None,
        "allow_free": bool(allow_free),
        "pool": receipt_pool(used, cost_usd, load_schema()),
    }
    ledger = receipts_dir() / "routing.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with _locked(ledger):
        holds = receipts_dir() / "reservations.jsonl"
        if reservation_id:
            prior = next((r for r in _read_receipts(ledger)
                          if isinstance(r, dict) and r.get("reservation_id") == reservation_id), None)
            if prior is not None:
                # An earlier attempt already wrote this call's receipt. Never write a second
                # one: make both files durable, finish the settlement if it is missing, and
                # return the receipt that is already there, provided it can be counted.
                if not _countable_receipt(prior):
                    raise ValueError(
                        f"reservation '{reservation_id}' has a receipt that is incomplete or cannot be "
                        f"counted; the hold stays open until it is reconciled with --release")
                if prior.get("task_class") != task_class or prior.get("used") != used:
                    raise ValueError(
                        f"reservation '{reservation_id}' already settled for "
                        f"{prior.get('task_class')}/{prior.get('used')}, not {task_class}/{used}")
                _sync_file(ledger)
                if any(h["id"] == reservation_id for h in reservations()):
                    _append_unlocked(holds, json.dumps(
                        {"kind": "settle", "id": reservation_id, "ts": prior.get("ts", receipt["ts"])},
                        allow_nan=False))
                elif holds.exists():
                    _sync_file(holds)
                return prior
            hold = next((h for h in reservations() if h["id"] == reservation_id), None)
            if hold is None:
                raise ValueError(f"reservation '{reservation_id}' is unknown, already settled or released")
            if hold["task_class"] != task_class or hold["model"] != used:
                raise ValueError(
                    f"reservation '{reservation_id}' was made for {hold['task_class']}/{hold['model']}, "
                    f"not {task_class}/{used}; nothing was recorded")
        _append_unlocked(ledger, json.dumps(receipt, allow_nan=False))
        if reservation_id:
            if not _receipt_is_last_line(ledger, receipt["id"]):
                raise OSError(f"receipt {receipt['id']} could not be verified in {ledger}; "
                              f"reservation '{reservation_id}' stays open")
            settle = {"kind": "settle", "id": reservation_id, "ts": receipt["ts"]}
            _append_unlocked(holds, json.dumps(settle, allow_nan=False))
    return receipt


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Route a task class to a model chain.")
    ap.add_argument("task_class", help="Task class (scout/review/bulk/code/hard-reasoning/vision/ultrabrain)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-non-zdr", action="store_true",
                    help="Include non-ZDR fallbacks for ZDR-required classes (stamped on receipts)")
    ap.add_argument("--allow-free", action="store_true",
                    help="Keep opencode/*-free models for scout, review and vision (outside the ZDR gateway key)")
    args = ap.parse_args()
    try:
        r = route(args.task_class, args.allow_non_zdr, args.allow_free)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=__import__("sys").stderr)
        raise SystemExit(2)
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"class={args.task_class}  primary={r['primary']}  variant={r['variant']}  fallbacks={r['fallbacks']}")


if __name__ == "__main__":
    main()
