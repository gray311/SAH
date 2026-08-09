#!/usr/bin/env python3
"""Render evidence-linked, self-contained reports for the copied CP rounds."""

from __future__ import annotations

import html
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parent
TASK = "eft__math__circle_packing"
METHODS = ("update_harness", "update_context", "update_executor")
ROUNDS = (3, 4)


CSS = r"""
:root {
  color-scheme: light dark;
  --bg: #f6f7fb; --panel: #ffffff; --panel2: #f0f3f8;
  --text: #172033; --muted: #5f6b7d; --line: #d9dfeb;
  --accent: #3157d5; --accent2: #0d8272; --good: #087a55;
  --warn: #9a5b00; --bad: #b52b39; --shadow: 0 10px 30px #1b264015;
}
html[data-theme="dark"] {
  --bg: #0f1420; --panel: #171e2d; --panel2: #20293a;
  --text: #edf2ff; --muted: #aab5c8; --line: #344057;
  --accent: #91a8ff; --accent2: #69d7c6; --good: #6ee7b7;
  --warn: #f6c76a; --bad: #ff8794; --shadow: 0 12px 30px #0007;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.62 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
}
a { color: var(--accent); }
.wrap { width: min(1180px, calc(100% - 36px)); margin: 0 auto; }
header { padding: 54px 0 30px; border-bottom: 1px solid var(--line); }
.eyebrow { color: var(--accent2); font-weight: 750; letter-spacing: .08em;
  text-transform: uppercase; font-size: 12px; }
h1 { font-size: clamp(31px, 5vw, 54px); line-height: 1.05; margin: 10px 0 14px; }
h2 { font-size: 24px; margin: 0 0 14px; }
h3 { font-size: 17px; margin: 0 0 8px; }
.lead { max-width: 900px; font-size: 18px; color: var(--muted); }
.toolbar { display:flex; gap:10px; flex-wrap:wrap; margin-top:22px; }
button, .navlink { border:1px solid var(--line); color:var(--text); background:var(--panel);
  padding:8px 12px; border-radius:10px; text-decoration:none; cursor:pointer; }
main { padding: 30px 0 70px; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(175px,1fr)); gap:14px; margin:20px 0 30px; }
.tile { background:var(--panel); border:1px solid var(--line); border-radius:16px;
  box-shadow:var(--shadow); padding:17px; min-height:112px; }
.tile .label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.06em; }
.tile .value { font-size:27px; font-weight:780; margin:6px 0 2px; font-variant-numeric:tabular-nums; }
.tile .source { font-size:12px; }
section { background:var(--panel); border:1px solid var(--line); border-radius:18px;
  box-shadow:var(--shadow); padding:24px; margin:18px 0; }
.claim { border-left:4px solid var(--accent); background:var(--panel2); border-radius:10px;
  padding:14px 16px; margin:12px 0; }
.claim.good { border-left-color:var(--good); }
.claim.warn { border-left-color:var(--warn); }
.claim.bad { border-left-color:var(--bad); }
.claim p { margin:5px 0; }
.ev { display:inline-flex; align-items:center; gap:5px; border:1px solid var(--line);
  background:var(--panel); border-radius:999px; padding:2px 8px; margin:2px 2px;
  font-size:12px; text-decoration:none; overflow-wrap:anywhere; }
.ev::before { content:"↗"; color:var(--accent2); font-weight:800; }
.ev.missing { border-style:dashed; color:var(--muted); }
.pill { display:inline-block; border:1px solid currentColor; border-radius:999px;
  padding:2px 8px; font-size:12px; font-weight:700; }
.pill.good { color:var(--good); }.pill.warn { color:var(--warn); }.pill.bad { color:var(--bad); }
.tablewrap { overflow:auto; border:1px solid var(--line); border-radius:12px; }
table { width:100%; border-collapse:collapse; min-width:850px; }
th, td { padding:10px 12px; text-align:left; vertical-align:top; border-bottom:1px solid var(--line); }
th { position:sticky; top:0; background:var(--panel2); color:var(--muted); font-size:12px;
  text-transform:uppercase; letter-spacing:.04em; }
tr:last-child td { border-bottom:0; }
td.num { font-variant-numeric:tabular-nums; white-space:nowrap; }
code { background:var(--panel2); border-radius:5px; padding:2px 5px; overflow-wrap:anywhere; }
pre { background:var(--panel2); border:1px solid var(--line); border-radius:10px;
  padding:13px; overflow:auto; white-space:pre-wrap; word-break:break-word; }
.muted { color:var(--muted); }.small { font-size:12px; }
.two { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:14px; }
details { border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin:8px 0; }
summary { cursor:pointer; font-weight:700; }
footer { color:var(--muted); border-top:1px solid var(--line); padding:24px 0 45px; }
@media print { button { display:none; } body { background:white; } section,.tile { box-shadow:none; } }
"""


JS = r"""
(function () {
  const key = "sah-artifact-report-theme";
  const root = document.documentElement;
  const saved = localStorage.getItem(key);
  if (saved) root.dataset.theme = saved;
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next; localStorage.setItem(key, next);
  });
})();
"""


def read_json(path: Path):
    return json.loads(path.read_text())


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def fmt(value, digits: int = 6) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def rel_href(path: Path, report_dir: Path) -> str:
    rel = Path(os.path.relpath(path, report_dir))
    return quote(rel.as_posix(), safe="/._-")


def ev(report_dir: Path, path: Path, field: str) -> str:
    if not path.exists():
        return f'<span class="ev missing">missing: {esc(path.name)} → {esc(field)}</span>'
    return f'<a class="ev" href="{rel_href(path, report_dir)}">{esc(path.name)} → {esc(field)}</a>'


def pill(text: str, kind: str) -> str:
    return f'<span class="pill {kind}">{esc(text)}</span>'


def tile(label: str, value: str, evidence: str, note: str = "") -> str:
    return (f'<div class="tile"><div class="label">{esc(label)}</div>'
            f'<div class="value">{esc(value)}</div><div class="source">{evidence}</div>'
            f'<div class="small muted">{esc(note)}</div></div>')


def marker_map(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def proposal_counts(propose_log: Path) -> tuple[int | None, int | None]:
    text = propose_log.read_text() if propose_log.exists() else ""
    matches = re.findall(r"(\d+)/(\d+) valid candidates", text)
    if not matches:
        matches = re.findall(r"(\d+)/(\d+) valid", text)
    return tuple(map(int, matches[-1])) if matches else (None, None)


def rollout_summary(round_dir: Path, candidate: str) -> tuple[Path | None, dict | None]:
    matches = sorted((round_dir / "rollouts" / TASK / candidate).glob("*/summary.json"))
    if not matches:
        return None, None
    path = matches[-1]
    data = read_json(path)
    return path, data[0] if isinstance(data, list) and data else data


def result_path_for(summary_path: Path | None) -> Path | None:
    if summary_path is None:
        return None
    target = summary_path.parent / "results" / f"{TASK}.json"
    return target if target.exists() else None


def harness_report(round_dir: Path, method: str, logical_round: int) -> str:
    summary_path = round_dir / "round_summary.json"
    summary = read_json(summary_path)
    group = summary["groups"][TASK]
    cost_path = round_dir / "round_cost.json"
    cost = read_json(cost_path)
    slot_path = round_dir / "h2_slot_plan.json"
    slot_plan = read_json(slot_path)
    slots = {row["k"]: row for row in slot_plan["slots"]}
    ratchet_path = round_dir / "program_ratchet_audit.json"
    ratchet = read_json(ratchet_path)["tasks"][TASK]
    gpu_path = round_dir / "runtime" / "gpu_utilization_summary.json"
    gpu = read_json(gpu_path)
    propose_path = round_dir / "propose.log"
    valid_count, proposed_count = proposal_counts(propose_path)
    marker_path = round_dir / "ROUND_COMPLETE"
    marker = marker_map(marker_path)
    trajectory_audit = round_dir / "candidate_trajectory_audit.log"
    training_marker = round_dir / "training" / "TRAIN_COMPLETE"
    training = marker_map(training_marker)
    rows = group["rows"]

    best_score = group.get("best_score")
    base_score = group.get("base_score")
    promoted = bool(ratchet.get("promoted"))
    method_title = "Update harness" if method == "update_harness" else "Update context"

    if method == "update_harness":
        failed_calls = propose_path.read_text().count("Invalid parameters for tool 'harness_shell'")
        lead = (
            f"The round completed and charged {cost['charged_agent_trajectories']} trajectories, "
            f"but the proposer materialized {valid_count}/{proposed_count} valid H2 candidates. "
            "All solution slots therefore used the incumbent fallback and none was eligible for "
            "H1 reward; the bundle records no scored program and no promotion."
        )
        if failed_calls:
            finding = (
                f"The proposer log records {failed_calls} invalid `harness_shell` calls whose "
                "required `command` parameter was missing. This co-occurs with 0/8 valid "
                "candidate submissions; the bundle does not isolate a single causal failure."
            )
        else:
            finding = (
                "The proposer log records an unavailable E2B SDK and 0/8 valid candidate "
                "submissions. It does not record enough evidence to attribute all failures to "
                "that warning alone."
            )
        claim_class = "bad"
    else:
        finding = (
            f"Candidate {ratchet.get('candidate_k')} was strictly promoted from "
            f"{fmt(base_score)} to {fmt(best_score)}. The valid-candidate count was "
            f"{valid_count}/{proposed_count}."
        )
        lead = (
            f"This round produced a valid strict promotion: {fmt(base_score)} → "
            f"{fmt(best_score)}. The candidate table below preserves the invalid proposals, "
            "unchanged valid candidates, and the promoted candidate rather than reporting only "
            "the winner."
        )
        claim_class = "good"

    tiles = [
        tile("Incoming score", fmt(base_score), ev(round_dir, summary_path, f"groups.{TASK}.base_score")),
        tile("Round best", fmt(best_score), ev(round_dir, summary_path, f"groups.{TASK}.best_score"),
             "Not recorded as zero when no scored candidate exists."),
        tile("Valid proposals", f"{fmt(valid_count, 0)} / {fmt(proposed_count, 0)}",
             ev(round_dir, propose_path, "valid candidates")),
        tile("Charged trajectories", fmt(cost["charged_agent_trajectories"], 0),
             ev(round_dir, cost_path, "charged_agent_trajectories"),
             f"{cost['trajectory_breakdown']['proposer']} proposer + "
             f"{cost['trajectory_breakdown']['solution_rollout']} solution"),
        tile("Promotion", "yes" if promoted else "no", ev(round_dir, ratchet_path, f"tasks.{TASK}.promoted"),
             ratchet.get("reason", "")),
        tile("Mean GPU util.", f"{gpu['mean_utilization_pct']:.2f}%",
             ev(round_dir, gpu_path, "mean_utilization_pct"),
             f"warning={str(gpu['underutilization_warning']).lower()}"),
    ]

    table_rows = []
    for row in rows:
        k = row["k"]
        slot = slots[k]
        candidate = f"cand{k:02d}"
        candidate_dir = round_dir / "tasks" / TASK / candidate
        summary_file, rollout = rollout_summary(round_dir, candidate)
        result_file = result_path_for(summary_file)
        links = [ev(round_dir, summary_path, f"groups.{TASK}.rows[k={k}]")]
        if candidate_dir.exists():
            links.append(ev(round_dir, candidate_dir / "agent.yaml", "materialized H2 mounts"))
            for skill_file in sorted((candidate_dir / "skills").glob("*/SKILL.md")):
                links.append(ev(round_dir, skill_file, "skill playbook"))
        if summary_file:
            links.append(ev(round_dir, summary_file, "best_score / audits"))
        if result_file:
            links.append(ev(round_dir, result_file, "executor trajectory"))
        outcome = "promoted" if ratchet.get("candidate_k") == k and promoted else (
            "valid, not promoted" if row["valid"] else "invalid proposal")
        changed = ", ".join(row.get("changed_fields") or []) or "—"
        table_rows.append(
            "<tr>"
            f'<td class="num">{k}</td>'
            f'<td>{pill("valid", "good") if row["valid"] else pill("invalid", "bad")}</td>'
            f'<td>{esc(slot["h2_slot_mode"])}</td>'
            f'<td>{esc(changed)}</td>'
            f'<td class="num">{fmt(row.get("score"))}</td>'
            f'<td class="num">{fmt(row.get("reward"))}</td>'
            f'<td>{esc(outcome)}</td>'
            f'<td>{" ".join(links)}</td>'
            "</tr>"
        )

    if method == "update_context" and promoted:
        best_k = ratchet["candidate_k"]
        best_summary_path, best_rollout = rollout_summary(round_dir, f"cand{best_k:02d}")
        skill_audit = (best_rollout or {}).get("skill_audit", {})
        skill_lines = []
        for name, audit in skill_audit.items():
            skill_lines.append(
                f"<li><code>{esc(name)}</code>: mounts={audit.get('mounts', '—')}, "
                f"loads_before_first_edit={audit.get('loads_before_first_edit', '—')}, "
                f"runtime_injections={audit.get('runtime_injections', '—')}, "
                f"required_for_credit={fmt(audit.get('required_for_credit'))}, "
                f"explicit loads={audit.get('loads', '—')} "
                f"{ev(round_dir, best_summary_path, f'skill_audit.{name}') if best_summary_path else ''}</li>"
            )
        mechanism = (
            '<div class="claim"><h3>Executor-visible mechanism</h3>'
            f'<p>The promoted H2 changed <code>{esc(", ".join(rows[best_k]["changed_fields"]))}</code>. '
            "The rollout's skill audit records the following delivery fields; they are reported "
            "verbatim because `loads` and `loads_before_first_edit` have distinct meanings in the artifact.</p>"
            f'<ul>{"".join(skill_lines) or "<li>No skill-audit entries were recorded.</li>"}</ul></div>'
        )
    else:
        mechanism = ""

    if training_marker.exists():
        training_html = (
            f'<p>Training updated: <strong>{esc(training.get("updated", "—"))}</strong>; '
            f'reason: <code>{esc(training.get("reason", "—"))}</code>. '
            f'{ev(round_dir, training_marker, "updated / reason")}</p>'
        )
    else:
        training_html = (
            '<p>This round directory has no <code>training/TRAIN_COMPLETE</code> marker. '
            'The report therefore does not infer a model update for this method.</p>'
        )

    paired = slot_plan["causal_attribution"]["enabled"]
    caveat = (
        "Paired causal attribution is disabled for this round. A score difference is therefore "
        "an observed candidate outcome, not an isolated estimate of the harness edit's causal effect."
        if not paired else "Paired causal attribution is enabled."
    )

    return page(
        title=f"CP · {method_title} · round {logical_round}",
        eyebrow=f"why-update-harness-11x3-fair16-v5 · logical round {logical_round}",
        lead=lead,
        toolbar=nav(round_dir, method, logical_round),
        body=(
            f'<div class="tiles">{"".join(tiles)}</div>'
            f'<section><h2>Finding</h2><div class="claim {claim_class}"><p>{esc(finding)}</p>'
            f'<p>{ev(round_dir, propose_path, "proposal outcome")} '
            f'{ev(round_dir, slot_path, "slots[*].h2_slot_mode / eligible_for_h1_reward")} '
            f'{ev(round_dir, ratchet_path, f"tasks.{TASK}.reason")}</p></div>{mechanism}</section>'
            '<section><h2>Candidate ledger</h2><p class="muted">A structurally valid proposer '
            'trajectory is not the same as a valid submitted H2. The trajectory audit and '
            'materialization outcome are both retained.</p>'
            f'<p>{ev(round_dir, trajectory_audit, "checked / valid / invalid")} '
            f'{ev(round_dir, propose_path, "valid candidates")}</p>'
            '<div class="tablewrap"><table><thead><tr><th>k</th><th>proposal</th><th>H2 slot</th>'
            '<th>changed fields</th><th>score</th><th>reward</th><th>outcome</th><th>evidence</th>'
            f'</tr></thead><tbody>{"".join(table_rows)}</tbody></table></div></section>'
            '<section><h2>Training and state transition</h2>' + training_html +
            f'<p>Round completion: <code>{esc(marker.get("completed_utc", "—"))}</code>, '
            f'job <code>{esc(marker.get("job_id", "—"))}</code>. '
            f'{ev(round_dir, marker_path, "full marker contents")}</p></section>'
            '<section><h2>Compute record</h2><div class="two"><div class="claim">'
            f'<p>Wall time: <strong>{cost["attempt_wall_seconds"]}</strong> seconds; allocated GPUs: '
            f'<strong>{cost["allocated_gpus"]}</strong>; CPUs: <strong>{cost["allocated_cpus"]}</strong>. '
            f'{ev(round_dir, cost_path, "attempt_wall_seconds / allocated resources")}</p></div>'
            '<div class="claim"><p>'
            f'Mean / median / p95 GPU utilization: {gpu["mean_utilization_pct"]:.2f}% / '
            f'{gpu["median_utilization_pct"]:.2f}% / {gpu["p95_utilization_pct"]:.2f}%. '
            f'{ev(round_dir, gpu_path, "mean / median / p95 utilization")}</p></div></div></section>'
            '<section><h2>Interpretation limits</h2><div class="claim warn"><p>'
            f'{esc(caveat)} {ev(round_dir, slot_path, "causal_attribution.enabled")}</p></div>'
            '<p>No missing score is rendered as zero. Absolute Lustre paths stored inside raw JSON '
            'are provenance strings; report links are relative and travel with this directory.</p></section>'
            + raw_guide(round_dir, method)
        ),
    )


def executor_report(round_dir: Path, logical_round: int) -> str:
    manifest_path = round_dir / "eval_manifest.json"
    manifest = read_json(manifest_path)
    cost_path = round_dir / "round_cost.json"
    cost = read_json(cost_path)
    gpu_path = round_dir / "runtime" / "gpu_utilization_summary.json"
    gpu = read_json(gpu_path)
    marker_path = round_dir / "ROUND_COMPLETE"
    marker = marker_map(marker_path)
    audit_path = round_dir / "trajectory_audit.log"
    train_path = round_dir / "training" / "TRAIN_COMPLETE"
    train = marker_map(train_path)
    bound_path = round_dir / "training" / "bound_replay_manifest.json"
    bound = read_json(bound_path)
    bound_log = round_dir / "training" / "bound_replay.log"
    prepare_path = round_dir / "ttt_prepare.log"
    prepare = read_json(prepare_path)

    candidates = []
    for summary_path in round_dir.glob("k*/*/summary.json"):
        match = re.fullmatch(r"k(\d+)", summary_path.parent.parent.name)
        if not match:
            continue
        k = int(match.group(1))
        raw = read_json(summary_path)
        row = raw[0] if isinstance(raw, list) else raw
        candidates.append((k, summary_path, row, result_path_for(summary_path)))
    candidates.sort(key=lambda item: item[0])
    best = max(candidates, key=lambda item: item[2]["best_score"])
    best_k, best_path, best_row, _ = best

    lead = (
        f"All {manifest['usable']}/{manifest['target']} fixed-H2 solution trajectories were usable, "
        f"and the batch best was {fmt(manifest['batch_best'])}. The post-round executor update did "
        f"not occur: all {bound['input_rows']} prepared rows were dropped by the bounded replay "
        "stage, and the completion marker records `updated=false`."
    )

    tiles = [
        tile("Batch best", fmt(manifest["batch_best"]), ev(round_dir, manifest_path, "batch_best")),
        tile("Usable trajectories", f"{manifest['usable']} / {manifest['target']}",
             ev(round_dir, manifest_path, "usable / target")),
        tile("Best trajectory", f"k{best_k}", ev(round_dir, best_path, "best_score"),
             f"{fmt(best_row['seed_score'])} → {fmt(best_row['best_score'])}"),
        tile("Evaluator calls", fmt(manifest["evaluator_calls"], 0),
             ev(round_dir, manifest_path, "evaluator_calls")),
        tile("Training update", train.get("updated", "—"), ev(round_dir, train_path, "updated / reason"),
             train.get("reason", "")),
        tile("Mean GPU util.", f"{gpu['mean_utilization_pct']:.2f}%",
             ev(round_dir, gpu_path, "mean_utilization_pct"),
             f"warning={str(gpu['underutilization_warning']).lower()}"),
    ]

    table_rows = []
    for k, summary_path, row, result_path in candidates:
        links = [ev(round_dir, summary_path, "best_score / seed_score / delta / audits")]
        if result_path:
            links.append(ev(round_dir, result_path, "full executor trajectory"))
        table_rows.append(
            "<tr>"
            f'<td class="num">{k}</td><td class="num">{fmt(row.get("seed_score"))}</td>'
            f'<td class="num">{fmt(row.get("best_score"))}</td>'
            f'<td class="num">{fmt(row.get("delta"))}</td>'
            f'<td class="num">{fmt(row.get("evaluations"), 0)}</td>'
            f'<td>{pill("eligible", "good") if row.get("score_eligible") else pill("ineligible", "bad")}</td>'
            f'<td>{esc(row.get("stop_reason", "—"))}</td><td>{" ".join(links)}</td></tr>'
        )

    return page(
        title=f"CP · Update executor · round {logical_round}",
        eyebrow=f"why-update-harness-11x3-fair16-v5 · logical round {logical_round}",
        lead=lead,
        toolbar=nav(round_dir, "update_executor", logical_round),
        body=(
            f'<div class="tiles">{"".join(tiles)}</div>'
            '<section><h2>Finding</h2><div class="claim warn"><p>'
            f'{esc(lead)} {ev(round_dir, manifest_path, "usable / batch_best")} '
            f'{ev(round_dir, bound_path, "input_rows / bounded_rows / dropped_rows")} '
            f'{ev(round_dir, train_path, "updated / reason")}</p></div>'
            '<div class="claim"><h3>What did advance</h3><p>The preparation artifact records '
            f'<code>update_eligible={fmt(prepare.get("update_eligible"))}</code>, a next parent program '
            f'<code>{esc(prepare.get("next_parent_id", "—"))}</code>, and {prepare.get("train_rows", "—")} '
            'prepared training rows. The later bounded replay stage dropped those rows, so program '
            'state advanced while executor-weight training did not. '
            f'{ev(round_dir, prepare_path, "update_eligible / next_parent_id / train_rows")} '
            f'{ev(round_dir, bound_path, "bounded_rows / dropped_rows")}</p></div></section>'
            '<section><h2>Solution-trajectory ledger</h2><p>The fixed H2 hash remained stable '
            'during all score-eligible rollouts. Each row links to its complete executor trajectory.</p>'
            f'<p>{ev(round_dir, manifest_path, "fixed_harness_sha256 / fixed harness hash scheme")} '
            f'{ev(round_dir, audit_path, "checked / valid / invalid")}</p>'
            '<div class="tablewrap"><table><thead><tr><th>k</th><th>seed</th><th>best</th><th>delta</th>'
            '<th>evals</th><th>credit</th><th>stop</th><th>evidence</th></tr></thead>'
            f'<tbody>{"".join(table_rows)}</tbody></table></div></section>'
            '<section><h2>Training boundary</h2><div class="claim bad"><p>'
            f'The bounded replay manifest records {bound["input_rows"]} input rows, '
            f'{bound["bounded_rows"]} retained rows, and {bound["dropped_rows"]} dropped rows. '
            f'The cleaner returned {bound["cleaner_returncode"]}; its log ends in an '
            '<code>IndexError</code> on an empty length list. The manifest explicitly labels this '
            f'as <code>recognized_zero_row_reporting_error={fmt(bound["recognized_zero_row_reporting_error"])}</code>. '
            f'{ev(round_dir, bound_path, "input_rows / bounded_rows / cleaner_returncode")} '
            f'{ev(round_dir, bound_log, "full traceback")}</p></div></section>'
            '<section><h2>Compute record</h2><div class="two"><div class="claim"><p>'
            f'Charged trajectories: {cost["charged_agent_trajectories"]} = '
            f'{cost["trajectory_breakdown"]["solution_rollout"]} solution + '
            f'{cost["trajectory_breakdown"]["proposer"]} proposer. Wall time: '
            f'{cost["attempt_wall_seconds"]} seconds. '
            f'{ev(round_dir, cost_path, "trajectory_breakdown / attempt_wall_seconds")}</p></div>'
            '<div class="claim"><p>'
            f'Mean / median / p95 GPU utilization: {gpu["mean_utilization_pct"]:.2f}% / '
            f'{gpu["median_utilization_pct"]:.2f}% / {gpu["p95_utilization_pct"]:.2f}%. '
            f'{ev(round_dir, gpu_path, "mean / median / p95 utilization")}</p></div></div>'
            f'<p>Round completion: <code>{esc(marker.get("completed_utc", "—"))}</code>, job '
            f'<code>{esc(marker.get("job_id", "—"))}</code>. '
            f'{ev(round_dir, marker_path, "full marker contents")}</p></section>'
            '<section><h2>Interpretation limits</h2><div class="claim warn"><p>The batch score '
            'demonstrates solution-search outcomes under a stable fixed H2. Because this round '
            'records no executor-weight update, it must not be described as evidence that newly '
            'trained executor weights caused the score change.</p></div><p>Missing values are shown '
            'as “—”, never zero.</p></section>'
            + raw_guide(round_dir, "update_executor")
        ),
    )


def nav(round_dir: Path, method: str, logical_round: int) -> str:
    sibling_round = 4 if logical_round == 3 else 3
    sibling = round_dir.parent / f"round{sibling_round:03d}" / "REPORT.html"
    index = ROOT / "INDEX.html"
    return (
        f'<a class="navlink" href="{rel_href(index, round_dir)}">Comparison index</a>'
        f'<a class="navlink" href="{rel_href(sibling, round_dir)}">Same method · round {sibling_round}</a>'
        '<button id="theme-toggle" type="button">Toggle theme</button>'
    )


def raw_guide(round_dir: Path, method: str) -> str:
    common = [
        (round_dir / "ROUND_COMPLETE", "completion marker"),
        (round_dir / "round_cost.json", "fair-compute and resource record"),
        (round_dir / "runtime" / "gpu_utilization_summary.json", "GPU summary"),
        (round_dir / "runtime" / "gpu_utilization.csv", "raw GPU samples"),
    ]
    if method == "update_executor":
        common += [
            (round_dir / "eval_manifest.json", "batch manifest"),
            (round_dir / "ttt_prepare.log", "training preparation"),
            (round_dir / "training" / "bound_replay_manifest.json", "training filter outcome"),
        ]
    else:
        common += [
            (round_dir / "prompts.json", "exact proposer inputs"),
            (round_dir / "trajectories.json", "all proposer trajectories"),
            (round_dir / "h2_slot_plan.json", "candidate/fallback slot mapping"),
            (round_dir / "round_summary.json", "candidate scores and rewards"),
            (round_dir / "program_ratchet_audit.json", "promotion decision"),
        ]
    items = "".join(f"<li>{ev(round_dir, path, description)}</li>" for path, description in common)
    return (
        '<section><h2>Guide to the raw bundle</h2><p>These are navigation links, not '
        'substitutes for the candidate-level evidence links above.</p>'
        f'<ul>{items}</ul></section>'
    )


def page(title: str, eyebrow: str, lead: str, toolbar: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><style>{CSS}</style></head>
<body><header><div class="wrap"><div class="eyebrow">{esc(eyebrow)}</div>
<h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p><div class="toolbar">{toolbar}</div>
</div></header><main class="wrap">{body}</main>
<footer><div class="wrap">Self-contained artifact report. Every numeric claim links to the file and
field it was read from; no network resources are loaded.</div></footer><script>{JS}</script></body></html>
"""


def index_page(records: list[dict]) -> str:
    rows = []
    for record in records:
        report_dir = record["dir"]
        report = report_dir / "REPORT.html"
        rows.append(
            "<tr>"
            f'<td>{esc(record["method_label"])}</td><td class="num">{record["round"]}</td>'
            f'<td class="num">{esc(record["start"])}</td><td class="num">{esc(record["end"])}</td>'
            f'<td>{esc(record["coverage"])}</td><td>{record["update"]}</td>'
            f'<td><a class="ev" href="{rel_href(report, ROOT)}">REPORT.html</a> '
            f'{record["primary_ev"]}</td></tr>'
        )
    body = (
        '<div class="tiles">'
        + tile("Per-round budget", "16", ev(ROOT, ROOT / "update_context/circle/rounds/round003/round_cost.json", "charged_agent_trajectories"))
        + tile("Task", "CP", ev(ROOT, ROOT / "update_context/circle/rounds/round003/round_cost.json", "task"))
        + '</div><section><h2>Cross-method finding</h2>'
        '<div class="claim bad"><p><strong>Update harness rounds 3–4 are not clean negative '
        'evidence:</strong> both materialized 0/8 valid proposals, used incumbent fallback slots, '
        'and produced no scored H1 candidate. '
        f'{ev(ROOT, ROOT / "update_harness/circle/rounds/round003/propose.log", "0/8 valid candidates")} '
        f'{ev(ROOT, ROOT / "update_harness/circle/rounds/round004/propose.log", "invalid harness_shell parameters / 0/8 valid")}</p></div>'
        '<div class="claim good"><p><strong>Update context produced strict promotions in both '
        'rounds.</strong> Round 4 cand07 added <code>circle-packing-advanced</code>; its rollout '
        'records one mount, one pre-edit delivery, one runtime injection, and '
        '<code>required_for_credit=true</code>. Paired controls were disabled, so this is '
        'executor-visible association, not an isolated causal estimate. '
        f'{ev(ROOT, ROOT / "update_context/circle/rounds/round004/round_summary.json", f"groups.{TASK}.rows[k=7]")} '
        f'{ev(ROOT, next((ROOT / "update_context/circle/rounds/round004/rollouts" / TASK / "cand07").glob("*/summary.json")), "skill_audit.circle-packing-advanced")} '
        f'{ev(ROOT, ROOT / "update_context/circle/rounds/round004/h2_slot_plan.json", "causal_attribution.enabled")}</p></div>'
        '<div class="claim warn"><p><strong>Update executor found stronger programs but did not '
        'update executor weights in either round.</strong> Each bounded replay stage dropped all '
        '16 input rows and the training marker records <code>updated=false</code>. '
        f'{ev(ROOT, ROOT / "update_executor/circle/rounds/round003/training/bound_replay_manifest.json", "input_rows / dropped_rows")} '
        f'{ev(ROOT, ROOT / "update_executor/circle/rounds/round004/training/TRAIN_COMPLETE", "updated / reason")}</p></div></section>'
        '<section><h2>Round comparison</h2><div class="tablewrap"><table><thead><tr>'
        '<th>method</th><th>round</th><th>incoming / seed</th><th>round best</th>'
        '<th>coverage</th><th>update outcome</th><th>report & evidence</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></section>'
        '<section><h2>What this subset can and cannot answer</h2><div class="claim warn"><p>'
        'The six bundles establish what was proposed, materialized, rolled out, scored, promoted, '
        'and trained in these two logical rounds. They do not provide paired candidate-vs-parent '
        'controls for the context promotions, and the two nominal update baselines each have a '
        'round-specific update failure. Any method-level causal conclusion must preserve those '
        'limitations.</p></div></section>'
    )
    return page(
        title="CP rounds 3–4 · artifact report index",
        eyebrow="why-update-harness-11x3-fair16-v5",
        lead="Evidence-linked reports covering update harness, update context, and update executor.",
        toolbar='<button id="theme-toggle" type="button">Toggle theme</button>',
        body=body,
    )


def build() -> None:
    records = []
    for method in METHODS:
        for logical_round in ROUNDS:
            round_dir = ROOT / method / "circle" / "rounds" / f"round{logical_round:03d}"
            if method == "update_executor":
                rendered = executor_report(round_dir, logical_round)
                manifest = read_json(round_dir / "eval_manifest.json")
                first_summary = min(
                    (read_json(path)[0] for path in round_dir.glob("k*/*/summary.json")),
                    key=lambda row: row["seed_score"],
                )
                start, end = fmt(first_summary["seed_score"]), fmt(manifest["batch_best"])
                coverage = f"{manifest['usable']}/{manifest['target']} usable"
                train = marker_map(round_dir / "training" / "TRAIN_COMPLETE")
                update = pill(f"weights updated={train.get('updated', '—')}", "bad")
                primary_ev = ev(ROOT, round_dir / "eval_manifest.json", "batch_best / usable")
                label = "Update executor"
            else:
                rendered = harness_report(round_dir, method, logical_round)
                summary_path = round_dir / "round_summary.json"
                group = read_json(summary_path)["groups"][TASK]
                start, end = fmt(group["base_score"]), fmt(group.get("best_score"))
                valid, total = proposal_counts(round_dir / "propose.log")
                coverage = f"{valid}/{total} valid H2"
                promoted = group["program_ratchet"]["promoted"]
                update = pill(f"promoted={fmt(promoted)}", "good" if promoted else "bad")
                primary_ev = ev(ROOT, summary_path, f"groups.{TASK}.base_score / best_score")
                label = "Update harness" if method == "update_harness" else "Update context"
            (round_dir / "REPORT.html").write_text(rendered)
            records.append({
                "dir": round_dir, "method_label": label, "round": logical_round,
                "start": start, "end": end, "coverage": coverage,
                "update": update, "primary_ev": primary_ev,
            })
    (ROOT / "INDEX.html").write_text(index_page(records))
    verify_links([ROOT / "INDEX.html"] + [record["dir"] / "REPORT.html" for record in records])


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.hrefs.append(value)


def verify_links(reports: list[Path]) -> None:
    failures = []
    for report in reports:
        parser = LinkCollector()
        parser.feed(report.read_text())
        for href in parser.hrefs:
            if href.startswith(("#", "http://", "https://")):
                continue
            target = (report.parent / unquote(href.split("#", 1)[0])).resolve()
            if not target.exists():
                failures.append(f"{report}: {href}")
    if failures:
        raise SystemExit("dead report links:\n" + "\n".join(failures))


if __name__ == "__main__":
    build()
