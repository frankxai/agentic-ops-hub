from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .control_plane import MediaControlPlane, PolicyBlocked


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="smis")
    commands = parser.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser("init", help="initialize a local Stage 0 SMIS store")
    initialize.add_argument("--store", required=True, type=Path)

    experiment = commands.add_parser("experiment", help="pre-register a tool or workflow experiment")
    experiment.add_argument("--store", required=True, type=Path)
    experiment.add_argument("--id", required=True)
    experiment.add_argument("--hypothesis", required=True)
    experiment.add_argument("--brand", required=True)
    experiment.add_argument("--metric", required=True)
    experiment.add_argument("--guardrail", action="append", required=True)
    experiment.add_argument("--decision-rule", required=True)

    package = commands.add_parser("package", help="create a provenance-linked draft content package")
    package.add_argument("--store", required=True, type=Path)
    package.add_argument("--id", required=True)
    package.add_argument("--brand", required=True)
    package.add_argument("--thesis", required=True)
    package.add_argument("--source-packet", action="append", required=True)

    preflight = commands.add_parser("preflight", help="check a publication intent without publishing")
    preflight.add_argument("--store", required=True, type=Path)
    preflight.add_argument("--mode", required=True, choices=("dry_run", "schedule", "publish"))
    preflight.add_argument("--evidence-file", required=True, type=Path)
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    parsed = build_parser().parse_args(arguments)
    if parsed.command == "init":
        metadata = {
            "system_id": "starlight-media-intelligence",
            "schema_version": "1.0",
            "autonomy_stage": 0,
            "publication_mode": "draft_only",
        }
        parsed.store.mkdir(parents=True, exist_ok=True)
        destination = parsed.store / "control-plane.json"
        temporary = destination.with_suffix(".tmp")
        temporary.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(destination)
        print(json.dumps(metadata, sort_keys=True))
        return 0
    if parsed.command == "experiment":
        experiment = MediaControlPlane(parsed.store).create_experiment(
            experiment_id=parsed.id,
            hypothesis=parsed.hypothesis,
            brand_id=parsed.brand,
            primary_metric=parsed.metric,
            guardrails=parsed.guardrail,
            decision_rule=parsed.decision_rule,
        )
        print(json.dumps(experiment, sort_keys=True))
        return 0
    if parsed.command == "package":
        package = MediaControlPlane(parsed.store).create_content_package(
            package_id=parsed.id,
            brand_id=parsed.brand,
            thesis=parsed.thesis,
            source_packet_ids=parsed.source_packet,
        )
        print(json.dumps(package, sort_keys=True))
        return 0
    if parsed.command == "preflight":
        evidence = json.loads(parsed.evidence_file.read_text(encoding="utf-8"))
        try:
            decision = MediaControlPlane(parsed.store).preflight_publication(
                mode=parsed.mode,
                evidence=evidence,
            )
        except PolicyBlocked as blocked:
            print(json.dumps({"decision": "blocked", "reason": blocked.reason}, sort_keys=True))
            return 2
        print(json.dumps(decision, sort_keys=True))
        return 0
    raise RuntimeError(f"unsupported command: {parsed.command}")


if __name__ == "__main__":
    raise SystemExit(main())
