"""Outer-round orchestrator CLI (instance-wise).

Per round, for EACH task instance tau in the task list (plan.md §2.2):
K H1-agent runs conditioned on tau -> K candidate H2 packages for tau ->
each rolled out once on tau by the inner loop -> per-task GRPO group.

Stages (run inside the serving job; see scripts/outer_round.sbatch):

  propose  for every (task, k): run H1 against M_phi -> validate -> materialize
           <round_dir>/tasks/<task_id>/candNN/ + round.json/prompts/trajectories.
  collect  after rollouts: per-task rewards + group advantages ->
           grpo_batch.jsonl (K x n_tasks rows) + round_summary.json +
           next_bases.json (per-task best harness -> next round's bases).

Bases registry: {task_id: {"package": dir, "score": s}} — which H2 package is
the current best for each task and what it scored. Round 1 defaults to the
initial hand-written H2 + results/baseline_h2_20ev.json scores; later rounds
pass --bases-file <prev_round>/next_bases.json.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from outer import proposer_io as pio, harness_spec as hs, propose as pp, rewards as rw  # noqa: E402
from outer.materialize import materialize, INNER_HARNESS  # noqa: E402

REPO = _SRC.parent
BASELINE_JSON = REPO / "results" / "baseline_h2_20ev.json"

DEFAULT_TASKS = [
    "eft__math__circle_packing",
    "eft__math__hadamard_maximal_det",
    "eft__math__erdos_min_overlap",
    "adrs__prism",
    "adrs__txn_scheduling",
    "adrs__eplb",
    "eft__algotune__convolve2d_full_fill",
    "eft__algotune__psd_cone_projection",
]


def _load_bases(bases_file: str | None, tasks: list) -> Dict[str, Dict[str, Any]]:
    """task_id -> {package, score, seed_score}."""
    static = json.loads(BASELINE_JSON.read_text())["baseline"]
    if bases_file:
        bases = json.loads(Path(bases_file).read_text())
    else:
        bases = {t: {"package": str(INNER_HARNESS), "score": static[t]["h2_best"]}
                 for t in tasks}
    for t in tasks:
        if t not in bases:
            bases[t] = {"package": str(INNER_HARNESS), "score": static[t]["h2_best"]}
        bases[t].setdefault("seed_score", static.get(t, {}).get("seed", 0.0))
    return bases


def cmd_propose(args) -> None:
    if getattr(args, "protocol", "sah") == "adaptive_v1":
        from protocols import adaptive_v1

        adaptive_v1.cmd_propose(args, load_bases=_load_bases)
        return

    from inner.eft_task import get_task  # tasks registry (spec + seed program)

    round_dir = Path(args.round_dir)
    round_dir.mkdir(parents=True, exist_ok=True)
    bases = _load_bases(args.bases_file, args.tasks)
    base_urls = [f"http://127.0.0.1:{8800 + g}/v1" for g in range(args.n_replicas)] \
        if args.n_replicas > 0 else [args.base_url]

    # per-task context: base spec (that task's current best harness) + user message
    inherited = {}
    if getattr(args, "seed_programs_file", None):
        try:
            inherited = json.loads(Path(args.seed_programs_file).read_text())
        except Exception as e:
            print(f"[propose] WARNING: seed-programs-file unreadable ({e}); using task seeds")

    ctx: Dict[str, Dict[str, Any]] = {}
    for tid in args.tasks:
        task = get_task(tid)
        base_spec = hs.read_base_spec(Path(bases[tid]["package"]))
        ent = inherited.get(tid)
        if ent:  # inheritance: rollouts start from the current best program
            seed_prog = ent["program"] if isinstance(ent, dict) else ent
            seed_sc = float(ent.get("score", bases[tid]["score"])) if isinstance(ent, dict) \
                else float(bases[tid]["score"])
        else:
            seed_prog, seed_sc = task.initial_program, float(bases[tid]["seed_score"])
        fb_text = ""
        if getattr(args, "feedback_file", None):
            try:
                fb = json.loads(Path(args.feedback_file).read_text()).get(tid)
                if fb:
                    fb_text = pio.render_feedback(fb)
            except Exception as e:
                print(f"[propose] WARNING: feedback-file unreadable ({e})")
        ctx[tid] = {
            "base_spec": base_spec,
            "user_message": pio.build_user_message(
                task_id=tid, task_spec=task.spec,
                seed_program=seed_prog,
                seed_score=seed_sc,
                base_score=float(bases[tid]["score"]),
                base_spec=base_spec, max_evals=args.max_evals) + fb_text,
        }

    jobs = [(tid, k) for tid in args.tasks for k in range(args.k)]
    print(f"[propose] {len(args.tasks)} tasks x K={args.k} = {len(jobs)} H1 runs "
          f"across {len(base_urls)} replica(s)")

    # Structured exploration (opt-in via --force-tool-frac): a fraction of each
    # task's K candidates are told they MUST add a new tool. This breaks the
    # declarative-only prior of a phi trained before the generative genome
    # existed — like forcing an unexplored arm — without touching the fixed H1.
    force_frac = float(getattr(args, "force_tool_frac", 0.0) or 0.0)
    force_ks = set(range(min(args.k, max(0, round(args.k * force_frac)))))
    _FORCE_MSG = ("\n\n## REQUIRED FOR THIS CANDIDATE\nThis candidate MUST include "
                  "at least one entry under `new_tools` that gives the solver a "
                  "genuinely new capability (a task-specific probe, an input "
                  "analyzer, a custom mutation/scoring operator). Follow the worked "
                  "example exactly for the YAML block-scalar format. A candidate "
                  "with no new_tools is not acceptable here.")

    def run(idx_job):
        idx, (tid, k) = idx_job
        seed = (args.seed * 1000 + idx) if args.seed is not None else None
        msg = ctx[tid]["user_message"]
        if k in force_ks:
            msg = msg + _FORCE_MSG
        return tid, pp.run_once(
            k, base_spec=ctx[tid]["base_spec"], user_message=msg,
            base_url=base_urls[idx % len(base_urls)], model=args.model,
            api_key="EMPTY", seed=seed, timeout=600.0)

    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        results = list(ex.map(run, enumerate(jobs)))

    per_task: Dict[str, Any] = {}
    trajectories = []
    for tid in args.tasks:
        records = sorted((r for t, r in results if t == tid), key=lambda r: r.k)
        pp.dedup_group(records, ctx[tid]["base_spec"])
        cands = []
        for rec in records:
            entry = {"k": rec.k, "valid": rec.valid, "errors": rec.errors,
                     "spec_hash": rec.spec_hash, "changed_fields": rec.changed_fields,
                     "stop_reason": rec.stop_reason, "llm_calls": rec.llm_calls,
                     "review_log": getattr(rec, "review_log", [])}
            if rec.valid:
                cdir = round_dir / "tasks" / tid / f"cand{rec.k:02d}"
                materialize(rec.effective, cdir, raw_spec_text=rec.raw_submission,
                            meta={"round": args.round, "task_id": tid, "k": rec.k,
                                  "spec_hash": rec.spec_hash,
                                  "changed_fields": rec.changed_fields,
                                  "base_package": bases[tid]["package"],
                                  "effective": rec.effective})
                entry["dir"] = str(cdir)
            cands.append(entry)
            trajectories.append({"task_id": tid, "k": rec.k,
                                 "raw_submission": rec.raw_submission,
                                 "trajectory": rec.trajectory})
        n_ok = sum(c["valid"] for c in cands)
        print(f"  {tid}: {n_ok}/{len(cands)} valid | " + " ".join(
            f"c{c['k']:02d}{'+' if c['valid'] else '-'}" for c in cands))
        per_task[tid] = {"base_package": bases[tid]["package"],
                         "base_score": bases[tid]["score"],
                         "seed_score": bases[tid]["seed_score"],
                         "base_spec_hash": hs.spec_hash(ctx[tid]["base_spec"]),
                         "candidates": cands}

    (round_dir / "round.json").write_text(json.dumps({
        "round": args.round, "created": time.strftime("%Y%m%d-%H%M%S"),
        "mode": "instance_wise",
        "h1_version": pio.H1_VERSION, "h1_package_hash": pio.h1_hash(),
        "proposer": {"base_urls": base_urls, "model": args.model, "seed": args.seed},
        "tasks_order": args.tasks, "max_evals": args.max_evals, "k": args.k,
        "bases_in": bases,
        "per_task": per_task,
    }, indent=2))
    (round_dir / "prompts.json").write_text(json.dumps(
        {tid: ctx[tid]["user_message"] for tid in args.tasks}, indent=2))
    (round_dir / "trajectories.json").write_text(json.dumps(trajectories, indent=2))
    total_ok = sum(c["valid"] for t in per_task.values() for c in t["candidates"])
    print(f"[propose] {total_ok}/{len(jobs)} valid candidates -> {round_dir}")


def cmd_collect(args) -> None:
    round_dir = Path(args.round_dir)
    meta = json.loads((round_dir / "round.json").read_text())
    protocol = getattr(args, "protocol", None) or meta.get("protocol", "sah")
    if protocol == "adaptive_v1":
        from protocols import adaptive_v1

        adaptive_v1.cmd_collect(args)
        return

    prompts = json.loads((round_dir / "prompts.json").read_text())
    trajs = {(t["task_id"], t["k"]): t
             for t in json.loads((round_dir / "trajectories.json").read_text())}
    system_text = (pio.H1_PACKAGE / "system.md").read_text()

    import os
    adv_mode = os.environ.get("SAH_ADV", "v2")
    ceilings = {}
    try:
        ft = json.loads((Path(__file__).resolve().parents[2]
                         / "results" / "finch_targets.json").read_text())
        ceilings = {t: (v.get("sota_combined") or v.get("finch_combined"))
                    for t, v in ft.get("targets", {}).items()}
    except Exception:
        pass

    groups, batch_rows = {}, []
    next_bases = dict(meta.get("bases_in", {}))  # carry forward ALL tasks' bases
    for tid in meta["tasks_order"]:
        pt = meta["per_task"][tid]
        if adv_mode == "legacy":
            g = rw.compute_task_group(
                task_id=tid, candidates=pt["candidates"],
                rollout_root=round_dir / "rollouts", base_score=float(pt["base_score"]))
        else:
            g = rw.compute_task_group_v2(
                task_id=tid, candidates=pt["candidates"],
                rollout_root=round_dir / "rollouts", base_score=float(pt["base_score"]),
                ceiling=ceilings.get(tid), sharpen_alpha=float(os.environ.get("SAH_ALPHA", "0.3")))
            print(f"  [{tid}] advantages: {g['adv_mode']} ceiling={g.get('ceiling')}")
        groups[tid] = g
        for row in g["rows"]:
            t = trajs.get((tid, row["k"]), {})
            batch_rows.append({
                "round": meta["round"], "task_id": tid, "k": row["k"],
                "system": system_text, "user": prompts[tid],
                "response": t.get("raw_submission", ""),
                "trajectory": t.get("trajectory", []),
                "reward": row["reward"], "advantage": row["advantage"],
                "valid": row["valid"], "score": row["score"],
                "spec_hash": row["spec_hash"],
            })
        # next round's base for this task = best candidate iff it beat the base
        if g["improved"]:
            next_bases[tid] = {
                "package": str(round_dir / "tasks" / tid / f"cand{g['best_k']:02d}"),
                "score": g["best_score"], "seed_score": pt["seed_score"],
                "from": f"round{meta['round']:03d}/cand{g['best_k']:02d}"}
        else:
            next_bases[tid] = {"package": pt["base_package"],
                               "score": pt["base_score"],
                               "seed_score": pt["seed_score"], "from": "unchanged"}
        bs = f"{g['best_score']:.6g}" if g["best_score"] is not None else "n/a"
        print(f"  {tid}: base={g['base_score']:.6g} best={bs} "
              f"(cand{g['best_k']:02d})" if g["best_k"] is not None else
              f"  {tid}: base={g['base_score']:.6g} best=n/a",
              "IMPROVED" if g["improved"] else "")

    # inner-telemetry digest for the NEXT visit's H1 context (blind mutation ->
    # informed debugging): what each candidate's rollout actually did
    fb_path = round_dir.parent / "task_feedback.json"
    try:
        feedback = json.loads(fb_path.read_text()) if fb_path.exists() else {}
    except Exception:
        feedback = {}
    for tid, g in groups.items():
        cands = []
        for row in g["rows"]:
            ent = {"k": row["k"], "score": row["score"],
                   "changed": [c.split(".")[-1] for c in row.get("changed_fields", [])][:6]}
            rl = row.get("review_log") or []
            if rl:
                ent["tools"] = [f"{x['name']}:{'ok' if x['ok'] else 'dropped('+str(x.get('error',''))[:40]+')'}" for x in rl]
            for res in sorted((round_dir / "rollouts" / tid / f"cand{row['k']:02d}").glob("*/results/*.json")):
                try:
                    d = json.loads(res.read_text())
                    led = d.get("ledger") or {}
                    ent.update({"evals": led.get("evaluator_calls"),
                                "llm_calls": led.get("llm_calls"),
                                "stop": d.get("stop_reason"),
                                "err": (str(d.get("error"))[:120] if d.get("error") else None)})
                except Exception:
                    pass
            if not row["valid"]:
                ent["invalid"] = True
            cands.append(ent)
        n_stuck = sum(1 for c in cands if c.get("score") is not None
                      and abs((c["score"] or 0) - g["base_score"]) < 1e-9)
        prev_note = (feedback.get(tid) or {}).get("analyst_note")
        feedback[tid] = {"round": meta["round"], "base_score": g["base_score"],
                         "best_score": g["best_score"], "best_k": g["best_k"],
                         "n_stuck_at_base": n_stuck, "candidates": cands}
        if prev_note:  # analyst notes are curated externally — never wipe them
            feedback[tid]["analyst_note"] = prev_note
    fb_path.write_text(json.dumps(feedback, indent=1))

    # global best-program inheritance: merge this round's winners into
    # <outer_root>/best_programs.json (next steps' rollouts start there)
    bp_path = round_dir.parent / "best_programs.json"
    try:
        best_programs = json.loads(bp_path.read_text()) if bp_path.exists() else {}
    except Exception:
        best_programs = {}
    for tid, g in groups.items():
        if g["best_k"] is None or g["best_score"] is None:
            continue
        prev = best_programs.get(tid, {})
        if isinstance(prev, dict) and prev.get("score", float("-inf")) >= g["best_score"]:
            continue
        prog, prog_score = None, float("-inf")
        for res in sorted((round_dir / "rollouts" / tid / f"cand{g['best_k']:02d}").glob("*/results/*.json")):
            try:
                d = json.loads(res.read_text())
                # pick the program from the RUN that produced the best score —
                # under the cascade a screen run can beat the full run, and
                # taking "last file wins" banked a mismatched program (r25 txn)
                if d.get("best_program") and float(d.get("best_score", -1e18)) > prog_score:
                    prog, prog_score = d["best_program"], float(d["best_score"])
            except Exception:
                pass
        if prog:
            # lineage crossover parents: the displaced best becomes a parent
            # (diverse basin material for future hybridization), cap 2
            parents = list((prev or {}).get("parents") or [])
            if isinstance(prev, dict) and prev.get("program") and \
               prev["program"] != prog:
                parents = [{"score": prev["score"], "program": prev["program"]}] + parents
            best_programs[tid] = {"score": g["best_score"], "program": prog,
                                  "round": meta["round"], "k": g["best_k"],
                                  "parents": parents[:2]}
            print(f"  [inherit] {tid}: best_programs.json <- round{meta['round']:03d}/"
                  f"cand{g['best_k']:02d} ({g['best_score']:.6g}, "
                  f"{len(parents[:2])} parents)")
    bp_path.write_text(json.dumps(best_programs, indent=1))

    with open(round_dir / "grpo_batch.jsonl", "w") as f:
        for row in batch_rows:
            f.write(json.dumps(row) + "\n")
    (round_dir / "round_summary.json").write_text(json.dumps({
        "round": meta["round"], "groups": groups,
        "improved_tasks": [t for t, g in groups.items() if g["improved"]],
    }, indent=2))
    (round_dir / "next_bases.json").write_text(json.dumps(next_bases, indent=2))
    n_imp = sum(g["improved"] for g in groups.values())
    print(f"[collect] {len(batch_rows)} GRPO rows | {n_imp}/{len(groups)} tasks improved "
          f"-> grpo_batch.jsonl, round_summary.json, next_bases.json")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("propose", help="K H1 runs per task; validate; materialize")
    p.add_argument("--round-dir", required=True)
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--bases-file", default=None,
                   help="per-task bases registry (prev round's next_bases.json)")
    p.add_argument("--base-url", default="http://127.0.0.1:8800/v1")
    p.add_argument("--n-replicas", type=int, default=0,
                   help="if >0, fan H1 runs across ports 8800..8800+n-1")
    p.add_argument("--model", default="qwen3.5-9b")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--parallel", type=int, default=8)
    p.add_argument("--max-evals", type=int, default=20)
    p.add_argument("--tasks", nargs="*", default=DEFAULT_TASKS)
    p.add_argument("--force-tool-frac", type=float, default=0.0,
                   help="fraction of each task's K candidates required to add a new tool (0..1)")
    p.add_argument("--seed-programs-file", default=None,
                   help="global best_programs.json; H1 sees the inherited program as the rollout starting point")
    p.add_argument("--feedback-file", default=None,
                   help="global task_feedback.json; H1 sees a telemetry digest of the previous visit's rollouts")
    p.add_argument("--protocol", choices=("sah", "adaptive_v1"), default="sah",
                   help="outer-loop protocol; default preserves current SAH behavior")
    p.add_argument("--protocol-state", default=None,
                   help="Adaptive v1 controller/archive state JSON")
    p.add_argument("--protocol-round", type=int, default=None,
                   help="zero-based Adaptive campaign round (artifact round may differ)")
    p.add_argument("--total-rounds", type=int, default=None,
                   help="Adaptive v1 campaign length (prevents an unused final update)")
    p.set_defaults(fn=cmd_propose)

    c = sub.add_parser("collect", help="per-task rewards + GRPO batch + next bases")
    c.add_argument("--round-dir", required=True)
    c.add_argument("--protocol", choices=("sah", "adaptive_v1"), default=None,
                   help="normally inferred from round.json")
    c.add_argument("--protocol-state", default=None)
    c.add_argument("--confidence-z", type=float, default=0.0,
                   help="Adaptive confirmed-record/promotion confidence multiplier")
    c.add_argument("--plateau-rounds", type=int, default=3)
    c.set_defaults(fn=cmd_collect)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
