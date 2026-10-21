#!/usr/bin/env python3
"""Validate the Starlight Lab registry and render the dashboard.

    python lab/build_lab.py --check                 # validate only, exit 1 on any problem
    python lab/build_lab.py                         # write lab/dist/index.html (standalone)
    python lab/build_lab.py --artifact --out F.html # page fragment for an Artifact publish

The registry in lab/*.json and lab/experiments/*.json is the only source. The page is
generated, never edited. Receipt numbers come from fleet/receipts/routing.jsonl (or
$STARLIGHT_RECEIPTS_DIR/routing.jsonl); with no receipts the page says so instead of
showing zeros.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
ROOT = LAB.parent

STATUSES = ("running", "ready", "blocked", "proposed", "concluded", "killed")
PLACES = {
    "local-c940": "Laptop c940",
    "railway": "Railway container",
    "vercel": "Vercel",
    "ci": "GitHub Actions",
}
PLACE_NOTES = {
    "local-c940": "Machine zone YELLOW. One process at a time; the preflight floor is 8,192 MiB free RAM.",
    "railway": "Isolated container with its own Token Pass key. Monthly cap is a proposal until Frank approves it.",
    "vercel": "Eve runs here. A Token Pass key can be used as an env var, but OIDC cannot spend it.",
    "ci": "Deterministic jobs only. No model calls.",
}
EXP_REQUIRED = (
    "id", "title", "pillar", "projects", "hypothesis", "status", "state", "owner", "owner_general",
    "verifier", "human_gate", "runs_on", "arms", "suite", "metric", "success_rule", "kill", "budget",
    "blocked_by", "clock", "next_gate", "decision_it_feeds",
)
GENERALS = ("ceo", "cfo", "coo", "cto", "cpo", "cmo", "caio", "chro", "cco", "frank")
BUDGET_KEYS = ("token_pass_usd_cap", "infra_usd_cap", "frank_hours")
ID_PATTERN = re.compile(r"^EXP-[0-9]{3}$")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load() -> dict:
    experiments = [read_json(p) for p in sorted((LAB / "experiments").glob("EXP-*.json"))]
    return {
        "goals": read_json(LAB / "goals.json"),
        "gates": read_json(LAB / "gates.json"),
        "budget": read_json(LAB / "budget.json"),
        "experiments": experiments,
    }


def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def blockers_of(exp: dict, data: dict) -> list[dict]:
    """Each blocker as {id, kind, title, resolved}."""
    gates = {g["id"]: g for g in data["gates"]["items"]}
    experiments = {e["id"]: e for e in data["experiments"]}
    out = []
    for ref in exp.get("blocked_by", []):
        if ref in gates:
            g = gates[ref]
            out.append({"id": ref, "kind": g["kind"], "title": g["title"], "resolved": g["status"] == "done"})
        elif ref in experiments:
            e = experiments[ref]
            out.append({"id": ref, "kind": "experiment", "title": e["title"], "resolved": e["status"] == "concluded"})
        else:
            out.append({"id": ref, "kind": "unknown", "title": ref, "resolved": False})
    return out


def validate(data: dict, today: dt.date | None = None) -> list[str]:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    problems: list[str] = []
    goals, gates, budget, experiments = data["goals"], data["gates"], data["budget"], data["experiments"]
    pillar_ids = {p["id"] for p in goals["pillars"]}
    project_ids = {p["id"] for p in goals["projects"]}
    gate_ids = [g["id"] for g in gates["items"]]
    exp_ids = [e.get("id") for e in experiments]

    if len(set(gate_ids)) != len(gate_ids):
        problems.append("gates: duplicate id")
    if len(set(exp_ids)) != len(exp_ids):
        problems.append("experiments: duplicate id")
    overlap = set(gate_ids) & set(exp_ids)
    if overlap:
        problems.append(f"ids used as both gate and experiment: {sorted(overlap)}")

    for exp in experiments:
        eid = exp.get("id", "?")
        missing = [k for k in EXP_REQUIRED if k not in exp]
        if missing:
            problems.append(f"{eid}: missing {missing}")
            continue
        if not ID_PATTERN.match(eid):
            problems.append(f"{eid}: id must look like EXP-001")
        if exp["status"] not in STATUSES:
            problems.append(f"{eid}: status {exp['status']!r} not in {STATUSES}")
        if exp["state"] != "S1":
            problems.append(f"{eid}: lab experiments live in lifecycle state S1")
        if exp["pillar"] not in pillar_ids:
            problems.append(f"{eid}: unknown pillar {exp['pillar']!r}")
        if not exp["projects"] or not set(exp["projects"]) <= project_ids:
            problems.append(f"{eid}: projects must be a non-empty subset of {sorted(project_ids)}")
        if exp["owner"] == exp["verifier"]:
            problems.append(f"{eid}: the verifier must be a different actor than the owner")
        if exp["owner_general"] not in GENERALS:
            problems.append(f"{eid}: owner_general {exp['owner_general']!r} unknown")
        for field in ("hypothesis", "success_rule", "kill", "human_gate", "decision_it_feeds"):
            if not str(exp[field]).strip():
                problems.append(f"{eid}: {field} is empty")
        if not exp["runs_on"] or any(r.get("where") not in PLACES for r in exp["runs_on"]):
            problems.append(f"{eid}: runs_on needs entries whose 'where' is one of {sorted(PLACES)}")
        if not exp["arms"]:
            problems.append(f"{eid}: needs at least one arm")
        if not all(is_number(exp["budget"].get(k)) for k in BUDGET_KEYS):
            problems.append(f"{eid}: budget needs non-negative numbers for {BUDGET_KEYS}")
        if not exp.get("metric", {}).get("primary"):
            problems.append(f"{eid}: metric.primary is required")
        if exp["clock"].get("ttl_days") != 30:
            problems.append(f"{eid}: S1 time to live is 30 days (registry/README.md)")

        blockers = blockers_of(exp, data)
        for b in blockers:
            if b["kind"] == "unknown":
                problems.append(f"{eid}: blocked_by {b['id']!r} is not a gate or experiment")
        unresolved = [b for b in blockers if not b["resolved"]]
        if exp["status"] == "blocked" and not unresolved:
            problems.append(f"{eid}: status blocked but nothing unresolved blocks it")
        if exp["status"] in ("running", "ready", "concluded") and unresolved:
            problems.append(f"{eid}: status {exp['status']} but blocked by {[b['id'] for b in unresolved]}")

        started = exp["clock"].get("started")
        if exp["status"] in ("running", "concluded", "killed") and not started:
            problems.append(f"{eid}: status {exp['status']} needs clock.started")
        if started and exp["status"] == "running":
            try:
                age = (today - dt.date.fromisoformat(started)).days
            except ValueError:
                problems.append(f"{eid}: clock.started {started!r} is not a date")
            else:
                if age > exp["clock"]["ttl_days"]:
                    problems.append(f"{eid}: past its {exp['clock']['ttl_days']}-day time to live; conclude or kill it")

    caps = {k: sum(e.get("budget", {}).get(k, 0) for e in experiments if e.get("status") not in ("concluded", "killed"))
            for k in ("token_pass_usd_cap", "infra_usd_cap")}
    if caps["token_pass_usd_cap"] > budget["token_pass"]["lab_allocation_usd"]:
        problems.append(f"experiment Token Pass caps {caps['token_pass_usd_cap']} exceed lab allocation {budget['token_pass']['lab_allocation_usd']}")
    if caps["infra_usd_cap"] > budget["railway_infra"]["monthly_cap_usd"]:
        problems.append(f"experiment infra caps {caps['infra_usd_cap']} exceed Railway cap {budget['railway_infra']['monthly_cap_usd']}")
    if budget["token_pass"]["lab_allocation_usd"] > budget["token_pass"]["monthly_usd"]:
        problems.append("lab allocation exceeds the Token Pass monthly credit")
    return problems


def receipts_path() -> Path:
    override = os.environ.get("STARLIGHT_RECEIPTS_DIR")
    return (Path(override) if override else ROOT / "fleet" / "receipts") / "routing.jsonl"


def summarize_receipts(path: Path | None = None, now: dt.datetime | None = None) -> dict:
    """Aggregate real receipts. Malformed lines and synthetic receipts are counted, not used."""
    path = path or receipts_path()
    now = now or dt.datetime.now(dt.timezone.utc)
    result = {"path": str(path), "exists": path.exists(), "used": 0, "skipped": 0, "synthetic": 0,
              "by_class_model": {}, "by_experiment": {}, "token_pass_month_usd": 0.0}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            if not isinstance(rec, dict):
                raise ValueError("not an object")
            if rec.get("synthetic") is True:
                result["synthetic"] += 1
                continue
            cls, model = rec["task_class"], rec["used"]
            cost = float(rec.get("cost_usd", 0.0))
            if not isinstance(cls, str) or not isinstance(model, str) or not math.isfinite(cost) or cost < 0:
                raise ValueError("bad field")
            ok = bool(rec.get("success"))
        except (ValueError, KeyError, TypeError):
            result["skipped"] += 1
            continue
        row = result["by_class_model"].setdefault((cls, model), {"n": 0, "ok": 0, "cost": 0.0})
        row["n"] += 1
        row["ok"] += 1 if ok else 0
        row["cost"] += cost
        result["used"] += 1
        exp = rec.get("experiment")
        if isinstance(exp, str):
            result["by_experiment"][exp] = result["by_experiment"].get(exp, 0.0) + cost
        stamp = str(rec.get("ts", ""))
        if rec.get("provider") == "token-pass" and stamp[:7] == now.strftime("%Y-%m"):
            result["token_pass_month_usd"] += cost
    return result


def git_sha() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def money(value: float) -> str:
    return f"${value:,.2f}" if value != int(value) else f"${int(value):,}"


STYLE = """
/* Layout concept: a lab notebook index. Direction first, then what needs Frank, then the experiments, then the evidence. */
:root {
  --bg: #f1f4f8; --surface: #ffffff; --ink: #161b24; --muted: #596377; --line: #d8dee8; --chip: #e6eaf2;
  --accent: #3947b8; --accent-ink: #ffffff;
  --ok: #1b7a4b; --warn: #9a5b06; --crit: #b3261e;
  --font-body: "Instrument Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-data: "JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0e1218; --surface: #171d27; --ink: #e5e9f1; --muted: #98a2b6; --line: #29313f; --chip: #212a38;
  --accent: #9aa6ff; --accent-ink: #0e1218; --ok: #4fc58a; --warn: #e3a64b; --crit: #ff7b72; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0e1218; --surface: #171d27; --ink: #e5e9f1; --muted: #98a2b6; --line: #29313f; --chip: #212a38;
  --accent: #9aa6ff; --accent-ink: #0e1218; --ok: #4fc58a; --warn: #e3a64b; --crit: #ff7b72; color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 15px/1.5 var(--font-body); padding-inline: 16px; padding-block: 24px 64px; }
.wrap { max-width: 1180px; margin-inline: auto; display: flex; flex-direction: column; gap: 36px; }
h1 { font-size: 1.9rem; line-height: 1.15; margin: 0; letter-spacing: -0.01em; text-wrap: balance; }
h2 { font-size: 1.05rem; margin: 0 0 12px; letter-spacing: 0.02em; }
h3 { font-size: 0.98rem; margin: 0; text-wrap: balance; }
p { margin: 0; }
a { color: var(--accent); }
.data, .mono { font-family: var(--font-data); font-variant-numeric: tabular-nums; }
.muted { color: var(--muted); }
.small { font-size: 0.84rem; }
.eyebrow { font-family: var(--font-data); font-size: 0.74rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
header { display: flex; flex-direction: column; gap: 10px; }
.north { font-size: 1.1rem; max-width: 70ch; }
.grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr)); }
.grid.wide { grid-template-columns: repeat(auto-fit, minmax(min(340px, 100%), 1fr)); }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 16px; min-width: 0; display: flex; flex-direction: column; gap: 10px; }
.pill { display: inline-block; font-family: var(--font-data); font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; background: var(--chip); color: var(--ink); white-space: nowrap; }
.pill.running { background: var(--ok); color: var(--accent-ink); }
.pill.ready { background: var(--accent); color: var(--accent-ink); }
.pill.blocked { background: var(--warn); color: var(--accent-ink); }
.pill.concluded { background: var(--ink); color: var(--bg); }
.pill.killed { background: var(--crit); color: var(--accent-ink); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.seg { display: flex; gap: 3px; height: 10px; }
.seg i { flex: 1; border-radius: 2px; background: var(--chip); }
.seg i.running { background: var(--ok); } .seg i.ready { background: var(--accent); } .seg i.blocked { background: var(--warn); }
.seg i.concluded { background: var(--ink); } .seg i.killed { background: var(--crit); }
.attention { display: flex; flex-direction: column; gap: 8px; }
.attention li { min-width: 0; overflow-wrap: anywhere; list-style: none; display: grid; grid-template-columns: auto 1fr; gap: 4px 12px; padding: 10px 12px; border-left: 3px solid var(--warn); background: var(--surface); border-radius: 0 6px 6px 0; }
.attention ul { margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.attention .unblocks { grid-column: 2; }
.attention .pill { align-self: start; justify-self: start; }
.card header { flex-direction: row; justify-content: space-between; align-items: baseline; gap: 8px; }
.kv { display: grid; grid-template-columns: 7.5rem 1fr; gap: 4px 10px; font-size: 0.88rem; }
.kv dt { color: var(--muted); } .kv dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
details { border-top: 1px solid var(--line); padding-top: 8px; font-size: 0.88rem; }
details summary { cursor: pointer; color: var(--accent); }
details summary:focus-visible, a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
details ul { margin: 8px 0 0; padding-left: 18px; }
.table-scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-family: var(--font-data); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); font-weight: 500; }
td.mark { text-align: center; font-family: var(--font-data); color: var(--accent); }
.bar { height: 12px; background: var(--chip); border-radius: 3px; position: relative; overflow: hidden; }
.bar > span { position: absolute; inset: 0 auto 0 0; background: var(--accent); }
.bar > span.spent { background: var(--ok); }
.source { font-family: var(--font-data); font-size: 0.72rem; color: var(--muted); overflow-wrap: anywhere; }
.empty { border: 1px dashed var(--line); border-radius: 6px; padding: 16px; color: var(--muted); }
footer { display: flex; flex-direction: column; gap: 4px; }
@media (max-width: 520px) { .kv { grid-template-columns: 1fr; } .kv dt { margin-top: 6px; } }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""


def pill(status: str) -> str:
    return f'<span class="pill {esc(status)}">{esc(status)}</span>'


def render_direction(data: dict) -> str:
    goals = data["goals"]
    cards = []
    for pillar in goals["pillars"]:
        mine = [e for e in data["experiments"] if e["pillar"] == pillar["id"]]
        segs = "".join(f'<i class="{esc(e["status"])}" title="{esc(e["id"])} {esc(e["status"])}"></i>' for e in mine)
        ids = ", ".join(e["id"] for e in mine) or "none yet"
        cards.append(
            f'<article class="panel"><h3>{esc(pillar["name"])}</h3>'
            f'<p class="small">{esc(pillar["moat"])}</p>'
            f'<div class="seg" role="img" aria-label="{len(mine)} experiments">{segs}</div>'
            f'<p class="small mono muted">{esc(ids)}</p>'
            f'<dl class="kv"><dt>Measured by</dt><dd>{esc(pillar["metric"])}</dd><dt>Now</dt><dd>{esc(pillar["state"])}</dd></dl>'
            f'<p class="source">source: {esc(pillar["source"])}</p></article>'
        )
    return (f'<section><h2>Direction</h2><div class="grid wide">{"".join(cards)}</div>'
            f'<p class="small muted" style="margin-top:10px">Test of the north star: {esc(goals["north_star"]["test"])}</p></section>')


def render_attention(data: dict) -> str:
    items = []
    for gate in data["gates"]["items"]:
        if gate["status"] == "done":
            continue
        unblocks = sorted(e["id"] for e in data["experiments"] if gate["id"] in e["blocked_by"] and e["status"] != "concluded")
        who = "Frank" if gate["owner"] == "frank" else gate["owner"].capitalize()
        tail = f'<span class="unblocks small muted">Unblocks {esc(", ".join(unblocks))}. {esc(gate["why"])}</span>' if unblocks else f'<span class="unblocks small muted">{esc(gate["why"])}</span>'
        items.append((0 if gate["owner"] == "frank" else 1, gate["id"],
                      f'<li><span class="pill">{esc(who)}</span><strong>{esc(gate["title"])}</strong>{tail}</li>'))
    body = "".join(html_ for _, _, html_ in sorted(items))
    return f'<section class="attention"><h2>Needs a decision or a task</h2><ul>{body}</ul></section>'


def render_card(exp: dict, data: dict) -> str:
    blockers = blockers_of(exp, data)
    chips = "".join(f'<span class="pill" title="{esc(b["title"])}">{"✓ " if b["resolved"] else ""}{esc(b["id"])}</span>' for b in blockers) or '<span class="muted">none</span>'
    projects = "".join(f'<span class="pill">{esc(p)}</span>' for p in exp["projects"])
    places = ", ".join(PLACES[r["where"]] for r in exp["runs_on"])
    arms = "".join(f'<li><span class="mono">{esc(a["harness"])}</span> on <span class="mono">{esc(a["model"])}</span> <span class="muted">({esc(a["role"])})</span></li>' for a in exp["arms"])
    why = "".join(f'<li>{esc(r["where"])}: {esc(r["why"])}</li>' for r in exp["runs_on"])
    evidence = "".join(f'<li>{esc(ev["claim"])} <span class="source">{esc(ev["source"])}</span><br><span class="muted">Caveat: {esc(ev["caveat"])}</span></li>' for ev in exp.get("prior_evidence", []))
    pre = "".join(f'<li>{esc(x)}</li>' for x in exp.get("preconditions", []))
    b = exp["budget"]
    clock = exp["clock"]["started"] or "starts when unblocked"
    extra = ""
    if pre:
        extra += f'<details><summary>Preconditions</summary><ul>{pre}</ul></details>'
    if evidence:
        extra += f'<details><summary>Prior evidence, not proof</summary><ul>{evidence}</ul></details>'
    return (
        f'<article class="panel card" id="{esc(exp["id"])}"><header><h3>{esc(exp["title"])}</h3>{pill(exp["status"])}</header>'
        f'<p class="small">{esc(exp["hypothesis"])}</p>'
        f'<dl class="kv"><dt>Id</dt><dd class="mono">{esc(exp["id"])} · {esc(exp["pillar"])}</dd>'
        f'<dt>Serves</dt><dd class="chips">{projects}</dd>'
        f'<dt>Runs on</dt><dd>{esc(places)}</dd>'
        f'<dt>Measures</dt><dd class="mono">{esc(exp["metric"]["primary"])}</dd>'
        f'<dt>Spend cap</dt><dd class="mono">{money(b["token_pass_usd_cap"])} Token Pass · {money(b["infra_usd_cap"])} infra · {b["frank_hours"]} h Frank</dd>'
        f'<dt>Waiting on</dt><dd class="chips">{chips}</dd>'
        f'<dt>Clock</dt><dd class="mono">{esc(clock)} · 30-day limit</dd>'
        f'<dt>Feeds</dt><dd>{esc(exp["decision_it_feeds"])}</dd>'
        f'<dt>Owner / verifier</dt><dd class="mono">{esc(exp["owner"])} / {esc(exp["verifier"])}</dd></dl>'
        f'<details><summary>Arms ({len(exp["arms"])})</summary><ul>{arms}</ul></details>'
        f'<details><summary>Pass rule and kill rule</summary><ul><li>Pass: {esc(exp["success_rule"])}</li><li>Kill: {esc(exp["kill"])}</li><li>Human gate: {esc(exp["human_gate"])}</li></ul></details>'
        f'<details><summary>Why these places</summary><ul>{why}</ul></details>{extra}</article>'
    )


def render_board(data: dict) -> str:
    groups = []
    for status in STATUSES:
        mine = [e for e in data["experiments"] if e["status"] == status]
        if mine:
            groups.append(f'<div><p class="eyebrow">{esc(status)} · {len(mine)}</p><div class="grid wide" style="margin-top:8px">{"".join(render_card(e, data) for e in mine)}</div></div>')
    return f'<section><h2>Experiments</h2><div style="display:flex;flex-direction:column;gap:22px">{"".join(groups)}</div></section>'


def render_where(data: dict) -> str:
    exps = data["experiments"]
    head = "".join(f'<th><a href="#{esc(e["id"])}">{esc(e["id"][4:])}</a></th>' for e in exps)
    rows = []
    for key, label in PLACES.items():
        cells = "".join(f'<td class="mark">{"●" if any(r["where"] == key for r in e["runs_on"]) else ""}</td>' for e in exps)
        rows.append(f'<tr><td><strong>{esc(label)}</strong><br><span class="small muted">{esc(PLACE_NOTES[key])}</span></td>{cells}</tr>')
    return (f'<section><h2>What runs where</h2><div class="panel table-scroll"><table><thead><tr><th>Place</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="small muted" style="margin-top:8px">Column headings are experiment numbers (EXP-001 is 001).</p></section>')


def render_projects(data: dict) -> str:
    exps = data["experiments"]
    head = "".join(f'<th><a href="#{esc(e["id"])}">{esc(e["id"][4:])}</a></th>' for e in exps)
    rows = []
    for proj in data["goals"]["projects"]:
        cells = "".join(f'<td class="mark">{"●" if proj["id"] in e["projects"] else ""}</td>' for e in exps)
        rows.append(f'<tr><td><strong>{esc(proj["name"])}</strong><br><span class="small muted">{esc(proj["gets"])}</span></td>{cells}</tr>')
    return (f'<section><h2>Which projects each experiment serves</h2><div class="panel table-scroll"><table><thead><tr><th>Project</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div></section>')


def render_budget(data: dict, summary: dict) -> str:
    b = data["budget"]
    live = [e for e in data["experiments"] if e["status"] not in ("concluded", "killed")]
    tp_caps = sum(e["budget"]["token_pass_usd_cap"] for e in live)
    infra_caps = sum(e["budget"]["infra_usd_cap"] for e in live)
    alloc, monthly = b["token_pass"]["lab_allocation_usd"], b["token_pass"]["monthly_usd"]
    infra_cap = b["railway_infra"]["monthly_cap_usd"]
    spent = f'{money(summary["token_pass_month_usd"])} this month' if summary["used"] else "not measured: no real receipts yet"
    keys = "".join(f'<tr><td>{esc(k["name"])}</td><td class="mono">{money(k["cap_usd"])}</td></tr>' for k in b["gateway_key_caps"]["keys"])
    return (
        '<section><h2>Budget</h2><div class="grid wide">'
        f'<article class="panel"><h3>Token Pass, lab share</h3>'
        f'<div class="bar" role="img" aria-label="Committed caps {tp_caps} of {alloc}"><span style="width:{min(100, 100*tp_caps/alloc if alloc else 0):.0f}%"></span></div>'
        f'<p class="mono">{money(tp_caps)} committed of {money(alloc)} lab allocation ({money(monthly)} shared monthly credit)</p>'
        f'<p class="small">Measured spend: {esc(spent)}</p><p class="small muted">{esc(b["token_pass"]["note"])}</p>'
        f'<p class="source">committed: sum of open experiment caps · allocation: lab/budget.json · measured: {esc(summary["path"])}</p></article>'
        f'<article class="panel"><h3>Railway infra (proposed)</h3>'
        f'<div class="bar"><span style="width:{min(100, 100*infra_caps/infra_cap if infra_cap else 0):.0f}%"></span></div>'
        f'<p class="mono">{money(infra_caps)} committed of {money(infra_cap)} per month</p>'
        f'<p class="small muted">{esc(b["railway_infra"]["note"])}</p><p class="source">lab/budget.json · status: {esc(b["railway_infra"]["status"])}</p></article>'
        f'<article class="panel"><h3>Gateway key caps</h3><div class="table-scroll"><table><thead><tr><th>Key</th><th>Cap</th></tr></thead><tbody>{keys}</tbody></table></div>'
        f'<p class="small muted">Team cap {money(b["gateway_key_caps"]["team_cap_usd"])}; default for new keys {money(b["gateway_key_caps"]["default_cap_usd"])}.</p>'
        f'<p class="source">{esc(b["gateway_key_caps"]["source"])}</p></article></div></section>'
    )


def render_receipts(summary: dict) -> str:
    if not summary["used"]:
        note = f' {summary["synthetic"]} synthetic test receipts ignored.' if summary["synthetic"] else ""
        return ('<section><h2>Measured so far</h2><div class="empty">No real routing receipts yet.' + esc(note) +
                ' This table fills from the first experiment run; until then the experiments above are plans, not results.</div>'
                f'<p class="source" style="margin-top:6px">source: {esc(summary["path"])}</p></section>')
    rows = []
    for (cls, model), r in sorted(summary["by_class_model"].items()):
        per = r["cost"] / r["ok"] if r["ok"] else None
        rows.append(f'<tr><td class="mono">{esc(cls)}</td><td class="mono">{esc(model)}</td><td class="mono">{r["n"]}</td>'
                    f'<td class="mono">{100*r["ok"]/r["n"]:.0f}%</td><td class="mono">{money(r["cost"])}</td>'
                    f'<td class="mono">{"n/a" if per is None else "$" + format(per, ".4f")}</td></tr>')
    return ('<section><h2>Measured so far</h2><div class="panel table-scroll"><table><thead><tr><th>Class</th><th>Model</th><th>Calls</th><th>Accepted</th><th>Cost</th><th>Per accepted</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="source" style="margin-top:6px">source: {esc(summary["path"])} · {summary["used"]} receipts used, {summary["skipped"]} malformed skipped, {summary["synthetic"]} synthetic ignored</p></section>')


def render(data: dict, summary: dict, fragment: bool = False) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    counts = {s: sum(1 for e in data["experiments"] if e["status"] == s) for s in STATUSES}
    tally = " · ".join(f"{n} {s}" for s, n in counts.items() if n)
    body = (
        '<div class="wrap"><header>'
        '<p class="eyebrow">Research lab · agentic-ops-hub</p><h1>Starlight Lab</h1>'
        f'<p class="north">{esc(data["goals"]["north_star"]["text"])}</p>'
        f'<p class="small muted mono">{esc(tally)}</p></header>'
        + render_direction(data) + render_attention(data) + render_board(data) + render_where(data)
        + render_projects(data) + render_budget(data, summary) + render_receipts(summary)
        + f'<footer class="small muted"><p>Generated {esc(now)} from commit {esc(git_sha())}. Edit lab/*.json, never this page.</p>'
        '<p>Lifecycle rules (S1 experiment: hypothesis, metric, token budget, 30-day limit) come from registry/README.md.</p></footer></div>'
    )
    if fragment:
        return f'<title>Starlight Lab</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap">\n<style>{STYLE}</style>\n{body}\n'
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Starlight Lab</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap">'
            f'<style>{STYLE}</style></head><body>{body}</body></html>\n')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate the registry and exit")
    parser.add_argument("--artifact", action="store_true", help="emit a page fragment for an Artifact publish")
    parser.add_argument("--out", help="output file (default lab/dist/index.html)")
    parser.add_argument("--receipts", help="routing.jsonl path override")
    args = parser.parse_args(argv)

    data = load()
    problems = validate(data)
    for p in problems:
        print(f"lab: {p}", file=sys.stderr)
    if problems:
        return 1
    if args.check:
        print(f"lab: ok, {len(data['experiments'])} experiments, {len(data['gates']['items'])} gates")
        return 0
    summary = summarize_receipts(Path(args.receipts) if args.receipts else None)
    out = Path(args.out) if args.out else LAB / "dist" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data, summary, fragment=args.artifact), encoding="utf-8", newline="\n")
    print(f"lab: wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
