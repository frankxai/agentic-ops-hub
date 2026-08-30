#!/usr/bin/env python3
"""Validate the cron inventory and render its human-readable projection."""

from __future__ import annotations

import argparse
import difflib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "fleet" / "cron-classification.json"
DOCUMENT_PATH = ROOT / "fleet" / "CRON-CLASSIFICATION.md"
ACTIVE_CLASSES = ("watchdog", "specialist", "queen")
WRITE_DIMENSIONS = ("llm_state", "heartbeat_control_plane", "filesystem")


def fail(message: str) -> None:
    raise SystemExit(message)


def load_inventory() -> dict[str, Any]:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def validate_inventory(data: dict[str, Any]) -> tuple[Counter[str], dict[str, int]]:
    if data.get("schema") != "cron-classification/v2":
        fail("schema must be cron-classification/v2")
    if data.get("source_of_truth") != "fleet/cron-classification.json":
        fail("the JSON inventory must be the sole repository source of truth")

    jobs = data.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        fail("jobs must be a non-empty list")

    ids = [job.get("id") for job in jobs]
    names = [job.get("name") for job in jobs]
    if len(set(ids)) != len(ids):
        fail("job ids must be unique")
    if len(set(names)) != len(names):
        fail("job names must be unique")

    class_counts: Counter[str] = Counter()
    dimension_counts = {dimension: 0 for dimension in WRITE_DIMENSIONS}

    for job in jobs:
        job_class = job.get("class")
        if job_class not in ACTIVE_CLASSES:
            fail(f"{job.get('name')}: unsupported active class {job_class!r}")
        class_counts[job_class] += 1

        writes = job.get("writes")
        if not isinstance(writes, dict) or set(writes) != set(WRITE_DIMENSIONS):
            fail(
                f"{job.get('name')}: writes must declare exactly "
                + ", ".join(WRITE_DIMENSIONS)
            )
        for dimension in WRITE_DIMENSIONS:
            if not isinstance(writes[dimension], bool):
                fail(f"{job.get('name')}: writes.{dimension} must be boolean")
            dimension_counts[dimension] += int(writes[dimension])

    summary = data.get("summary") or {}
    expected_summary = {
        "active": len(jobs),
        "paused": 0,
        **{job_class: class_counts[job_class] for job_class in ACTIVE_CLASSES},
        "unclassified": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            fail(f"summary.{key}={summary.get(key)!r}; expected {expected}")

    if summary.get("write_dimensions") != dimension_counts:
        fail(
            "summary.write_dimensions does not match jobs: "
            f"{summary.get('write_dimensions')!r} != {dimension_counts!r}"
        )

    policy = data.get("write_policy") or {}
    derived_lists = {
        "llm_state_writer_jobs": [
            job["name"] for job in jobs if job["writes"]["llm_state"]
        ],
        "read_only_queen_jobs": [
            job["name"]
            for job in jobs
            if job["class"] == "queen" and not any(job["writes"].values())
        ],
        "heartbeat_control_plane_writer_jobs": [
            job["name"]
            for job in jobs
            if job["writes"]["heartbeat_control_plane"]
        ],
        "filesystem_writer_jobs": [
            job["name"] for job in jobs if job["writes"]["filesystem"]
        ],
    }
    for key, expected in derived_lists.items():
        if policy.get(key) != expected:
            fail(f"write_policy.{key} does not match jobs")

    llm_limit = policy.get("max_concurrent_llm_state_writers")
    if not isinstance(llm_limit, int) or llm_limit < 0:
        fail("write_policy.max_concurrent_llm_state_writers must be non-negative")
    if dimension_counts["llm_state"] > llm_limit:
        fail("scheduled LLM-state writers exceed the declared policy limit")

    return class_counts, dimension_counts


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_document(
    data: dict[str, Any],
    class_counts: Counter[str],
    dimension_counts: dict[str, int],
) -> str:
    jobs = data["jobs"]
    generated_date = str(data["generated"]).split("T", 1)[0]
    lines = [
        f"# Cron Classification — C940 Fleet ({generated_date})",
        "",
        "**Repository source of truth:** `fleet/cron-classification.json` only.",
        f"**Live source:** `{data['live_source']}`.",
        "**Projection:** this file is generated from the JSON `jobs` array; edit the JSON, then run `python scripts/render_cron_classification.py`.",
        "",
        f"## Class distribution (active = {len(jobs)}, paused = {data['summary']['paused']})",
        "",
        "| Class | Count | Rule |",
        "| --- | ---: | --- |",
    ]

    for job_class in ACTIVE_CLASSES:
        lines.append(
            f"| `{job_class}` | {class_counts[job_class]} | "
            f"{cell(data['class_legend'][job_class])} |"
        )
    lines.append("| `oneshot` / `retired` | 0 | none left active or dangling |")

    lines.extend(
        [
            "",
            "## Write dimensions",
            "",
            "| Dimension | Writers | Meaning |",
            "| --- | ---: | --- |",
        ]
    )
    for dimension in WRITE_DIMENSIONS:
        lines.append(
            f"| `{dimension}` | {dimension_counts[dimension]} | "
            f"{cell(data['write_dimension_legend'][dimension])} |"
        )

    policy = data["write_policy"]
    lines.extend(
        [
            "",
            "## Scheduled-write policy",
            "",
            f"- LLM-state writer limit: **{policy['max_concurrent_llm_state_writers']}**.",
            "- LLM-state writers: "
            + ", ".join(f"`{name}`" for name in policy["llm_state_writer_jobs"])
            + ".",
            "- Read-only queen lanes: "
            + ", ".join(f"`{name}`" for name in policy["read_only_queen_jobs"])
            + ".",
            "- Heartbeat/control-plane writers: "
            + ", ".join(
                f"`{name}`"
                for name in policy["heartbeat_control_plane_writer_jobs"]
            )
            + ".",
            "- Filesystem writers: "
            + ", ".join(f"`{name}`" for name in policy["filesystem_writer_jobs"])
            + ".",
            "",
            "## Jobs",
            "",
            "| Cron | Class | Write dimensions | Domain | Cadence | Delivers |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )

    for job in jobs:
        writes = [
            dimension
            for dimension in WRITE_DIMENSIONS
            if job["writes"][dimension]
        ]
        write_label = ", ".join(f"`{dimension}`" for dimension in writes) or "none"
        lines.append(
            f"| `{cell(job['name'])}` | `{job['class']}` | {write_label} | "
            f"{cell(job['domain'])} | {cell(job['schedule'])} | "
            f"{cell(job['deliver'])} |"
        )

    lines.extend(["", "## Open gaps", ""])
    for index, gap in enumerate(data.get("gaps") or [], start=1):
        lines.append(
            f"{index}. **{cell(gap['severity'])} — {cell(gap['id'])}.** "
            f"{cell(gap['detail'])}"
        )

    pulse = next(job for job in jobs if job["name"] == "fleet-swarm-pulse")
    lines.extend(
        [
            "",
            "## Heartbeat writes are explicit",
            "",
            "`fleet-swarm-pulse` declares both `heartbeat_control_plane` and "
            f"`filesystem` writes: {cell(pulse.get('notes', ''))}. "
            "Each machine still writes only its own heartbeat.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when the generated Markdown projection is stale",
    )
    args = parser.parse_args()

    data = load_inventory()
    class_counts, dimension_counts = validate_inventory(data)
    rendered = render_document(data, class_counts, dimension_counts)

    if args.check:
        current = DOCUMENT_PATH.read_text(encoding="utf-8")
        if current != rendered:
            diff = "".join(
                difflib.unified_diff(
                    current.splitlines(keepends=True),
                    rendered.splitlines(keepends=True),
                    fromfile=str(DOCUMENT_PATH),
                    tofile="generated",
                )
            )
            fail("cron projection is stale:\n" + diff)
        print(
            "cron inventory valid: "
            f"active={len(data['jobs'])} "
            + " ".join(
                f"{job_class}={class_counts[job_class]}"
                for job_class in ACTIVE_CLASSES
            )
        )
        return

    DOCUMENT_PATH.write_text(rendered, encoding="utf-8")
    print(f"wrote {DOCUMENT_PATH}")


if __name__ == "__main__":
    main()
