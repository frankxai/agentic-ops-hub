from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_REQUIRED_GATES = (
    "source_provenance",
    "rights_and_reuse",
    "brand_voice",
    "accessibility",
    "platform_policy",
    "human_approval",
    "idempotency",
    "cost_or_quota",
)
_RECEIPT_FIELDS = {
    "event_id",
    "sequence",
    "event_type",
    "entity_type",
    "entity_id",
    "occurred_at",
    "payload_hash",
    "previous_event_hash",
    "event_hash",
}


class PolicyBlocked(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class MediaControlPlane:
    _in_process_lock = threading.RLock()

    def __init__(self, store: Path):
        self.store = store
        self.autonomy_stage = 0
        self.events_path = self.store / "events.jsonl"

    def preflight_publication(self, *, mode: str, evidence: dict[str, bool]) -> dict[str, Any]:
        with self._store_lock():
            self._require_healthy_event_chain()
            preflight_id = f"smis_preflight_{uuid.uuid4()}"
            if mode not in {"dry_run", "schedule", "publish"}:
                self._append_event("preflight.blocked", "preflight", preflight_id, {"mode": mode, "reason": "unsupported_mode"})
                raise PolicyBlocked("unsupported_mode")
            if self.autonomy_stage == 0 and mode in {"schedule", "publish"}:
                self._append_event(
                    "preflight.blocked",
                    "preflight",
                    preflight_id,
                    {"mode": mode, "reason": "autonomy_stage_0_draft_only"},
                )
                raise PolicyBlocked("autonomy_stage_0_draft_only")
            unexpected_gates = sorted(set(evidence) - set(_REQUIRED_GATES))
            if unexpected_gates:
                reason = f"unexpected_evidence:{','.join(unexpected_gates)}"
                self._append_event("preflight.blocked", "preflight", preflight_id, {"mode": mode, "reason": reason})
                raise PolicyBlocked(reason)
            for gate in _REQUIRED_GATES:
                if evidence.get(gate) is not True:
                    reason = f"missing_evidence:{gate}"
                    self._append_event("preflight.blocked", "preflight", preflight_id, {"mode": mode, "reason": reason})
                    raise PolicyBlocked(reason)
            decision = {"decision": "eligible_draft_only", "mode": mode, "autonomy_stage": self.autonomy_stage}
            self._append_event("preflight.eligible", "preflight", preflight_id, decision)
            return decision

    def create_experiment(
        self,
        *,
        experiment_id: str,
        hypothesis: str,
        brand_id: str,
        primary_metric: str,
        guardrails: list[str],
        decision_rule: str,
    ) -> dict[str, Any]:
        with self._store_lock():
            self._validate_identifier(experiment_id)
            self._require_healthy_event_chain()
            experiment = {
                "id": experiment_id,
                "hypothesis": hypothesis,
                "brand_id": brand_id,
                "primary_metric": primary_metric,
                "guardrails": guardrails,
                "decision_rule": decision_rule,
                "pre_registered_at": self._now(),
            }
            self._write_record("experiments", experiment_id, experiment)
            self._append_event("experiment.created", "experiment", experiment_id, experiment)
            return experiment

    def create_content_package(
        self,
        *,
        package_id: str,
        brand_id: str,
        thesis: str,
        source_packet_ids: list[str],
    ) -> dict[str, Any]:
        with self._store_lock():
            self._validate_identifier(package_id)
            self._require_healthy_event_chain()
            if not source_packet_ids:
                raise ValueError("content package requires at least one source packet")
            package = {
                "id": package_id,
                "brand_id": brand_id,
                "thesis": thesis,
                "source_packet_ids": source_packet_ids,
                "status": "draft",
                "created_at": self._now(),
            }
            self._write_record("content-packages", package_id, package)
            self._append_event("content_package.created", "content_package", package_id, package)
            return package

    def read_events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        return [json.loads(line) for line in self.events_path.read_text(encoding="utf-8").splitlines() if line]

    def verify_event_chain(self) -> bool:
        previous_event_hash = None
        expected_sequence = 1
        for event in self.read_events():
            stored_hash = event.get("event_hash")
            event_without_hash = {key: value for key, value in event.items() if key != "event_hash"}
            if set(event) != _RECEIPT_FIELDS or not isinstance(stored_hash, str):
                return False
            if not event["event_id"].startswith("smis_evt_"):
                return False
            if event["sequence"] != expected_sequence:
                return False
            if event["previous_event_hash"] != previous_event_hash:
                return False
            if self._hash(event_without_hash) != stored_hash:
                return False
            previous_event_hash = stored_hash
            expected_sequence += 1
        return True

    @contextmanager
    def _store_lock(self):
        with self._in_process_lock:
            lock_path = self.store / "events.lock"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            with lock_path.open("a+b") as lock_file:
                lock_file.seek(0, os.SEEK_END)
                if lock_file.tell() == 0:
                    lock_file.write(b"\0")
                    lock_file.flush()
                    os.fsync(lock_file.fileno())
                lock_file.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
                    try:
                        yield
                    finally:
                        lock_file.seek(0)
                        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                    try:
                        yield
                    finally:
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    def _append_event(
        self,
        event_type: str,
        entity_type: str,
        entity_id: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        previous_events = self.read_events()
        event = {
            "event_id": f"smis_evt_{uuid.uuid4()}",
            "sequence": len(previous_events) + 1,
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "occurred_at": self._now(),
            "payload_hash": self._hash(record),
            "previous_event_hash": previous_events[-1]["event_hash"] if previous_events else None,
        }
        event["event_hash"] = self._hash(event)
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        with self.events_path.open("a", encoding="utf-8", newline="\n") as events_file:
            events_file.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
            events_file.flush()
            os.fsync(events_file.fileno())
        return event

    def _write_record(self, category: str, record_id: str, record: dict[str, Any]) -> None:
        directory = self.store / "records" / category
        directory.mkdir(parents=True, exist_ok=True)
        destination = directory / f"{record_id}.json"
        if destination.exists():
            raise ValueError(f"record already exists: {record_id}")
        temporary = destination.with_suffix(".tmp")
        temporary.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(destination)

    def _require_healthy_event_chain(self) -> None:
        if not self.verify_event_chain():
            raise ValueError("event chain verification failed")

    @staticmethod
    def _hash(value: dict[str, Any]) -> str:
        canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _validate_identifier(value: str) -> None:
        if not _SAFE_IDENTIFIER.fullmatch(value):
            raise ValueError("identifier must contain only letters, numbers, dot, underscore, or hyphen")
