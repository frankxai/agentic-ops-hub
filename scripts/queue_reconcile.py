#!/usr/bin/env python3
"""Deterministic fleet-queue reconciliation helpers.

Rejects active queue items whose source PR is already merged/closed, and
blocks remote YogaBook dispatch when the peer heartbeat is stale.
Does not forge heartbeats or invent new mission IDs.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


TERMINAL_STATUSES = frozenset(
    {
        "delivered",
        "integrated",
        "closed-unmerged",
        "cancelled",
        "superseded",
        "expired",
        "hold",
        "partial-manual",
    }
)
ACTIVE_STATUSES = frozenset({"queued", "in-progress", "claimed", "active"})


def _parse_time(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def heartbeat_is_fresh(
    heartbeat: dict[str, Any] | None,
    *,
    max_age_hours: float = 24,
    now: datetime | None = None,
) -> bool:
    if not heartbeat:
        return False
    if str(heartbeat.get("status", "")).lower() not in {"live", "online"}:
        return False
    observed = _parse_time(str(heartbeat.get("at", "")))
    current = now or datetime.now(timezone.utc)
    return observed >= current - timedelta(hours=max_age_hours)


def item_is_expired(item: dict[str, Any], *, now: datetime | None = None) -> bool:
    """True when an active item's declared TTL has elapsed.

    Fails closed: an unparseable expires_at/ttl_hours, or a ttl_hours with no
    issued_at/updated_at anchor, counts as expired. Items that declare no TTL
    at all return False here — require_ttl in validate_queue_document decides
    whether that absence is itself an error.
    """
    current = now or datetime.now(timezone.utc)
    expires = item.get("expires_at")
    if expires is not None:
        return _parse_time(str(expires)) < current
    ttl = item.get("ttl_hours")
    if ttl is None:
        return False
    try:
        ttl_hours = float(ttl)
    except (TypeError, ValueError):
        return True
    anchor = _parse_time(str(item.get("updated_at") or item.get("issued_at") or ""))
    return anchor + timedelta(hours=ttl_hours) < current


def source_pr_blocks_active(item: dict[str, Any], pr_state: str | None) -> bool:
    """True when an active item still points at a finished GitHub PR."""
    if "source_pr" not in item:
        return False
    status = str(item.get("status", "")).lower()
    if status not in ACTIVE_STATUSES:
        return False
    if not pr_state:
        return False
    return pr_state.lower() in {"merged", "closed"}


def validate_queue_document(
    doc: dict[str, Any],
    *,
    pr_states: dict[int, str] | None = None,
    peer_heartbeat: dict[str, Any] | None = None,
    require_fresh_peer_for_remote: bool = False,
    require_ttl: bool = False,
    now: datetime | None = None,
    max_age_hours: float = 24,
) -> list[str]:
    """Return human-readable validation errors (empty list == pass)."""
    errors: list[str] = []
    pr_states = pr_states or {}
    active = list(doc.get("active") or [])
    historical = list(doc.get("historical") or [])

    seen_ids: set[str] = set()
    for item in active + historical:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            errors.append("queue item missing id")
            continue
        if item_id in seen_ids:
            errors.append(f"duplicate queue_item_id: {item_id}")
        seen_ids.add(item_id)

    for item in active:
        status = str(item.get("status", "")).lower()
        item_id = str(item.get("id", "?"))
        if status in TERMINAL_STATUSES:
            errors.append(f"active item {item_id} has terminal status {status}")
        if status not in ACTIVE_STATUSES:
            errors.append(f"active item {item_id} has non-active status {status!r}")
        has_ttl = "expires_at" in item or "ttl_hours" in item
        if require_ttl and not has_ttl:
            errors.append(
                f"active item {item_id} missing ttl (expires_at or ttl_hours) "
                "required by the coordination contract"
            )
        if has_ttl and item_is_expired(item, now=now):
            errors.append(
                f"active item {item_id} ttl expired; move to historical or renew"
            )
        source_pr = item.get("source_pr")
        if source_pr is not None:
            try:
                pr_number = int(source_pr)
            except (TypeError, ValueError):
                errors.append(f"active item {item_id} has invalid source_pr {source_pr!r}")
                continue
            pr_state = pr_states.get(pr_number)
            if source_pr_blocks_active(item, pr_state):
                errors.append(
                    f"active item {item_id} source_pr #{pr_number} is {pr_state}; must be terminal"
                )

    if require_fresh_peer_for_remote and active:
        if not heartbeat_is_fresh(peer_heartbeat, max_age_hours=max_age_hours, now=now):
            errors.append(
                "remote dispatch blocked: peer heartbeat missing/stale/not-live "
                f"(max_age_hours={max_age_hours})"
            )

    return errors


def move_active_to_historical(
    doc: dict[str, Any],
    item_id: str,
    *,
    terminal_status: str,
    evidence: str,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Return a new queue document with item_id moved from active → historical."""
    if terminal_status not in TERMINAL_STATUSES:
        raise ValueError(f"terminal_status must be one of {sorted(TERMINAL_STATUSES)}")
    active = list(doc.get("active") or [])
    historical = list(doc.get("historical") or [])
    remaining: list[dict[str, Any]] = []
    moved: dict[str, Any] | None = None
    for item in active:
        if str(item.get("id")) == item_id:
            moved = dict(item)
        else:
            remaining.append(item)
    if moved is None:
        raise KeyError(item_id)
    hist_entry = {
        "id": item_id,
        "status": terminal_status,
        "evidence": evidence,
    }
    # keep useful provenance without carrying live-mission fields as active work
    for key in ("source_pr", "branch", "repo", "outcome"):
        if key in moved:
            hist_entry[key] = moved[key]
    historical = [h for h in historical if str(h.get("id")) != item_id]
    historical.append(hist_entry)
    out = dict(doc)
    out["active"] = remaining
    out["historical"] = historical
    out["updated_at"] = updated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return out
