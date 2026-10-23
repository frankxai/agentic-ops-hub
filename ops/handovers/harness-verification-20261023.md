---
id: harness-verification-20261023
what: Absorb lab portability fix and close paid-launch admission gap before activation
where: ops/sessions/2026-10-23-harness-verification.md
owner: unassigned
status: open
note: local tests verified; no merge, formal sign-off, live experiment or activation
evidence: https://github.com/frankxai/agentic-ops-hub/pull/379
updated: 2026-10-23
---

## Prompt

Read the verification session and current main AGENTS.md before acting. Recheck PR 377 and 379 heads. Absorb the two-line receipt-test decorator move from agent/codex/lab-conformance-portability into the lab owner branch after review; run the 99-test lab suites with jsonschema 4.26.0. Nine local semantic invariant tests must run without a SIS checkout; only two external conformance checks may skip. The routing wrapper still launches its injected process runner when an isolated ledger is at its monthly cap: close run admission and usage reconciliation before unattended paid activation. Keep the existing PRs as owners; no new runner, model spend or feature PR. Local test evidence is not a formal sign-off or a live harness experiment.
