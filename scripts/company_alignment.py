"""Read selected issue/source metadata; report gaps without changing task authority."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess


REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
ISSUE = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/issues/([1-9][0-9]*)")
SHA = re.compile(r"[0-9a-f]{40}")


def utc(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Observation timestamps need an explicit timezone")
    return result.astimezone(timezone.utc)


def validate(catalog):
    if catalog.get("schema_version") != "1.0":
        raise ValueError("Unsupported capability-map schema")
    if catalog.get("status") != "proposed-capability-projection":
        raise ValueError("This tool reads proposals, not canonical task authority")
    rows = catalog.get("capabilities", [])
    if not rows or len(rows) > 40:
        raise ValueError("Expected 1-40 selected capabilities")
    ids = [row["id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate capability ID")
    for row in rows:
        for key in ("name", "owner_status", "recommended_mode", "next_gate"):
            if not row.get(key):
                raise ValueError("Missing required capability field: " + key)
        issue = row.get("tracking_issue")
        if issue is not None and not ISSUE.fullmatch(issue):
            raise ValueError("Invalid tracking issue URL")
        owner = row.get("implementation_candidate")
        if owner is not None and not REPO.fullmatch(owner):
            raise ValueError("Invalid repository candidate")
        if any(dep not in ids for dep in row.get("dependencies", [])):
            raise ValueError("Unknown capability dependency")
    sources = catalog.get("source_snapshots", [])
    if len(sources) > 12:
        raise ValueError("Limit source reads to 12 selected repositories")
    if len({source["repository"] for source in sources}) != len(sources):
        raise ValueError("Duplicate source repository")
    for source in sources:
        if not REPO.fullmatch(source["repository"]) or not SHA.fullmatch(source["sha"]):
            raise ValueError("Invalid pinned source identity")
    visiting, visited = set(), set()
    dependencies = {row["id"]: row.get("dependencies", []) for row in rows}

    def visit(key):
        if key in visiting:
            raise ValueError("Capability dependency cycle")
        if key in visited:
            return
        visiting.add(key)
        for dep in dependencies[key]:
            visit(dep)
        visiting.remove(key)
        visited.add(key)

    for key in ids:
        visit(key)
    freshness = catalog.get("freshness_days", 7)
    if not isinstance(freshness, int) or not 1 <= freshness <= 30:
        raise ValueError("Expected a 1-30 day freshness window")


def gh_read(path):
    try:
        result = subprocess.run(
            ["gh", "api", path], capture_output=True, text=True,
            encoding="utf-8", timeout=15, check=False,
        )
        if result.returncode:
            return {"read_error": "GitHub read unavailable"}
        return json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return {"read_error": "GitHub read unavailable"}


def observe(catalog):
    snapshot = {"observed_at": datetime.now(timezone.utc).isoformat(),
                "issues": {}, "source_heads": {}}
    for url in sorted({row["tracking_issue"] for row in catalog["capabilities"]
                       if row.get("tracking_issue")}):
        match = ISSUE.fullmatch(url)
        response = gh_read("repos/" + match[1] + "/issues/" + match[2])
        if "read_error" in response:
            snapshot["issues"][url] = response
        elif "pull_request" in response or response.get("html_url") != url:
            snapshot["issues"][url] = {"read_error": "Unexpected issue identity"}
        else:
            # Keep bodies, comments, identities and credentials out of this projection.
            snapshot["issues"][url] = {
                "state": response.get("state"), "updated_at": response.get("updated_at"),
            }
    for source in catalog["source_snapshots"]:
        repository = source["repository"]
        response = gh_read("repos/" + repository + "/commits/" + source.get("branch", "main"))
        snapshot["source_heads"][repository] = (
            response if "read_error" in response else {"sha": response.get("sha")}
        )
    return snapshot


def report(catalog, snapshot, now=None):
    validate(catalog)
    now = now or datetime.now(timezone.utc)
    findings = []

    def finding(kind, target, action):
        findings.append({"kind": kind, "target": target, "action": action})

    try:
        age = (now - utc(snapshot["observed_at"])).total_seconds()
        if age < -300 or age > catalog.get("freshness_days", 7) * 86400:
            finding("snapshot-freshness", "selected-observations", "Refresh observations; do not infer current state")
    except (KeyError, TypeError, ValueError):
        finding("snapshot-freshness", "selected-observations", "Supply a dated, timezone-aware observation")
    issues = snapshot.get("issues", {})
    heads = snapshot.get("source_heads", {})
    for source in catalog["source_snapshots"]:
        current = heads.get(source["repository"], {})
        sha = current.get("sha")
        if current.get("read_error") or not isinstance(sha, str) or not SHA.fullmatch(sha):
            finding("source-unknown", source["repository"], "Resolve read coverage before relying on the pin")
        elif sha != source["sha"]:
            finding("source-changed", source["repository"], "Inspect the relevant diff and rebind applicable evidence")
    for row in catalog["capabilities"]:
        key = row["id"]
        if not row.get("implementation_candidate") or row["owner_status"] in (
            "unresolved-per-product", "issue-declared-pending-registry"
        ):
            finding("placement-unresolved", key, "Confirm receiving ownership before implementation")
        issue = row.get("tracking_issue")
        current = issues.get(issue, {})
        if not issue:
            finding("untracked-capability", key, "Search existing work; route a real admitted job before opening an issue")
        elif current.get("read_error") or current.get("state") not in ("open", "closed"):
            finding("issue-unknown", key, "Read the owning issue; current state is unknown")
        elif current["state"] == "closed":
            finding("closed-issue-review", key, "Inspect accepted evidence and refresh the next gate; closure alone proves no acceptance")
        if not row.get("acceptance_receipt"):
            finding("acceptance-unobserved", key, "Acceptance was not read by this tool; obtain relevant behavior/owner evidence")
    return {
        "schema_version": "1.0", "kind": "read-only-company-alignment-observation",
        "generated_at": now.isoformat(), "authority": "Observation only; no status or permission changes",
        "coverage": {"capabilities": len(catalog["capabilities"]),
                     "unique_issues": len({r["tracking_issue"] for r in catalog["capabilities"] if r.get("tracking_issue")}),
                     "source_repositories": len(catalog["source_snapshots"]),
                     "product_behavior_checked": False, "worker_liveness_checked": False,
                     "acceptance_artifacts_checked": False, "all_repositories_checked": False},
        "observations": snapshot, "findings": findings,
    }


def private_destination(value):
    path = Path(value).resolve()
    if any((parent / ".git").exists() for parent in [path.parent, *path.parents]):
        raise ValueError("Private observation destination must be outside Git checkouts")
    if not path.parent.is_dir():
        raise ValueError("Use an existing private dossier directory")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--snapshot")
    parser.add_argument("--private-report", required=True)
    args = parser.parse_args()
    try:
        destination = private_destination(args.private_report)
        catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8-sig"))
        validate(catalog)
        snapshot = observe(catalog) if args.live else json.loads(Path(args.snapshot).read_text(encoding="utf-8-sig"))
        result = report(catalog, snapshot)
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(2, "Alignment check failed: " + type(exc).__name__ + "\n")
    print(json.dumps({"report": str(destination), "coverage": result["coverage"],
                      "finding_count": len(result["findings"]), "writes_to_github": False}))


if __name__ == "__main__":
    main()
