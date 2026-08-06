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
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from outer import proposer_io as pio, harness_spec as hs, propose as pp, rewards as rw  # noqa: E402
from outer.program_ratchet import suppress_task_training, update_program_ratchet  # noqa: E402
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


def _input_file_provenance(path_value: str | None) -> Dict[str, Any]:
    """Hash a mutable cross-round input at the moment this round consumes it."""
    if not path_value:
        return {"path": None, "exists": False, "sha256": None, "bytes": 0}
    path = Path(path_value)
    if not path.is_file():
        return {"path": str(path), "exists": False, "sha256": None, "bytes": 0}
    raw = path.read_bytes()
    return {
        "path": str(path),
        "exists": True,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def cmd_propose(args) -> None:
    from inner.eft_task import get_task  # tasks registry (spec + seed program)

    round_dir = Path(args.round_dir)
    round_dir.mkdir(parents=True, exist_ok=True)
    bases = _load_bases(args.bases_file, args.tasks)
    feedback_input = _input_file_provenance(
        getattr(args, "feedback_file", None)
    )
    program_input = _input_file_provenance(
        getattr(args, "seed_programs_file", None)
    )
    bases_input = _input_file_provenance(getattr(args, "bases_file", None))
    base_urls = [f"http://127.0.0.1:{8800 + g}/v1" for g in range(args.n_replicas)] \
        if args.n_replicas > 0 else [args.base_url]

    # per-task context: base spec (that task's current best harness) + user message
    inherited = {}
    logical_index = int(os.environ.get("LOGICAL_ROUND_INDEX", "0") or 0)
    if os.environ.get("SAH_FIXED_INFERENCE_SLOTS", "0") == "1" \
            and logical_index > 0 \
            and not getattr(args, "seed_programs_file", None):
        raise RuntimeError(
            "canonical post-cold round requires --seed-programs-file"
        )
    if getattr(args, "seed_programs_file", None):
        try:
            inherited = json.loads(Path(args.seed_programs_file).read_text())
            if not isinstance(inherited, dict):
                raise TypeError("seed-program registry must be a JSON object")
        except Exception as e:
            if os.environ.get("SAH_FIXED_INFERENCE_SLOTS", "0") == "1" \
                    and logical_index > 0:
                raise RuntimeError(
                    "canonical post-cold round requires its task-local "
                    "seed-program registry"
                ) from e
            print(f"[propose] WARNING: seed-programs-file unreadable ({e}); using task seeds")
            inherited = {}
    # Rollouts consume this immutable round-local copy, never the mutable
    # workspace registry that the collector will update after the batch.
    seed_snapshot = round_dir / "seed_programs_in.json"
    seed_snapshot.write_text(
        json.dumps(inherited, indent=2, ensure_ascii=False) + "\n"
    )
    snapshot_raw = seed_snapshot.read_bytes()
    program_input["snapshot_path"] = str(seed_snapshot.resolve())
    program_input["snapshot_sha256"] = hashlib.sha256(snapshot_raw).hexdigest()
    program_input["snapshot_bytes"] = len(snapshot_raw)

    # Anti-tampering: verify the task texts about to be served against the
    # pinned registry (fail-closed under SAH_TASK_TEXT_ENFORCE=1).
    from outer.task_text_registry import verify_task_texts
    _tasks_by_id = {tid: get_task(tid) for tid in args.tasks}
    task_text_provenance = verify_task_texts(_tasks_by_id)
    (round_dir / "task_text_provenance.json").write_text(
        json.dumps(task_text_provenance, indent=1)
    )
    for _tid, _row in task_text_provenance.get("tasks", {}).items():
        if _row.get("status") == "MISMATCH":
            print(f"[task-text] WARNING: {_tid} differs from the pinned registry")

    ctx: Dict[str, Dict[str, Any]] = {}
    for tid in args.tasks:
        task = _tasks_by_id[tid]
        base_spec = hs.read_base_spec(Path(bases[tid]["package"]))
        ent = inherited.get(tid)
        if ent:  # inheritance: rollouts start from the current best program
            seed_prog = ent["program"] if isinstance(ent, dict) else ent
            seed_sc = float(ent.get("score", bases[tid]["score"])) if isinstance(ent, dict) \
                else float(bases[tid]["score"])
        else:
            seed_prog, seed_sc = task.initial_program, float(bases[tid]["seed_score"])
        fb_text = ""
        fb = None
        analysis_enabled = os.environ.get("SAH_ANALYSIS", "0") == "1"
        analysis_required = os.environ.get("SAH_ANALYSIS_REQUIRED", "0") == "1"
        if analysis_required and not analysis_enabled:
            raise RuntimeError(
                "SAH_ANALYSIS_REQUIRED=1 requires SAH_ANALYSIS=1"
            )
        analysis_meta = {
            "enabled": analysis_enabled,
            "required_after_cold_round": analysis_required,
            "feedback_available": False,
            "brief_attached": False,
            "model_calls": 0,
            "specialists": [],
            "feedback_input": feedback_input,
        }
        if getattr(args, "feedback_file", None):
            try:
                fb = json.loads(Path(args.feedback_file).read_text()).get(tid)
                if fb:
                    fb_text = pio.render_feedback(fb)
                    analysis_meta["feedback_available"] = True
            except Exception as e:
                print(f"[propose] WARNING: feedback-file unreadable ({e})")
        # optional analysis brief (campaign_config: analysis.enabled). Two
        # read-only specialists on the SAME frozen M0 distill the feedback into a
        # bounded, leak-guarded brief appended to the proposer message. Legacy
        # runs fail open; the canonical context arm sets SAH_ANALYSIS_REQUIRED=1
        # and fails closed after the cold round.
        if analysis_enabled and fb:
            try:
                from outer import analysis as an
                # LEAK GUARD: analysis MUST run on the frozen M0, never the
                # trained proposer M_phi. Under split serving base_urls[0] is
                # M_phi; the worker exports SAH_ANALYSIS_BASE_URL pointing at a
                # frozen replica. Without split serving base_urls[0] is already
                # the frozen base, so that fallback is also frozen M0.
                an_url = os.environ.get("SAH_ANALYSIS_BASE_URL") or base_urls[0]
                chat = an.make_chat_fn(an_url, args.model)
                brief = an.run_analysis(
                    fb, chat=chat,
                    want_perf=os.environ.get("SAH_ANALYSIS_PERF", "1") == "1",
                    want_design=os.environ.get("SAH_ANALYSIS_DESIGN", "1") == "1")
                if brief:
                    fb_text += brief
                    analysis_meta.update({
                        "brief_attached": True,
                        "model_calls": 2,
                        "specialists": ["performance", "design"],
                    })
                    print(f"[propose] {tid}: analysis brief attached ({len(brief)} chars)")
                elif analysis_required:
                    raise RuntimeError(
                        f"{tid}: required post-cold analyzer produced no brief"
                    )
            except Exception as e:
                if analysis_required:
                    raise RuntimeError(
                        f"{tid}: required post-cold analyzer failed"
                    ) from e
                print(f"[propose] WARNING: analysis stage skipped ({e})")
        ctx[tid] = {
            "base_spec": base_spec,
            "analysis": analysis_meta,
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
    _FORCE_MSG = ("\n\n## REQUIRED FOR THIS CANDIDATE\nThis candidate MUST add "
                  "at least one generated tool that gives the executor a genuinely "
                  "new capability. Add its entry to agent.yaml, its schema under "
                  "tools/, its implementation under custom_tools/, and its exact "
                  "name plus usage guidance to prompt.md. A candidate with no new "
                  "mounted tool is not acceptable here.")

    def _msg_for(tid, k):
        msg = ctx[tid]["user_message"]
        return msg + _FORCE_MSG if k in force_ks else msg

    def run(idx_job):
        idx, (tid, k) = idx_job
        seed = (args.seed * 1000 + idx) if args.seed is not None else None
        return tid, pp.run_once(
            k, base_spec=ctx[tid]["base_spec"], user_message=_msg_for(tid, k),
            base_url=base_urls[idx % len(base_urls)], model=args.model,
            api_key="EMPTY", seed=seed, timeout=600.0)

    # -- optional sequential sampling (campaign_config: sampling.mode) -------- #
    # In parallel mode (default) the K samples of a task are independent. In
    # sequential mode, later samples see prior VALID actions from the same task
    # so they don't re-propose a paraphrase — Adaptive's within-batch diversity
    # policy. Tasks still run concurrently across the pool; only the K samples
    # WITHIN a task serialize. Zero change to the parallel path.
    seq = os.environ.get("SAH_SEQUENTIAL", "0") == "1"
    max_shared = int(os.environ.get("SAH_SEQ_MAX_SHARED", "6") or "6")

    def run_task_sequential(tid):
        recs, shared = [], []
        for k in range(args.k):
            seed = (args.seed * 1000 + k) if args.seed is not None else None
            msg = _msg_for(tid, k)
            if shared:
                msg = msg + pio.render_prior_actions(shared[-max_shared:])
            rec = pp.run_once(
                k, base_spec=ctx[tid]["base_spec"], user_message=msg,
                base_url=base_urls[k % len(base_urls)], model=args.model,
                api_key="EMPTY", seed=seed, timeout=600.0)
            recs.append((tid, rec))
            if rec.valid and rec.effective is not None:
                shared.append({"k": k, "changed_fields": rec.changed_fields,
                               "spec": rec.spec})
        return recs

    if seq:
        print(f"[propose] sequential sampling ON (share <= {max_shared} prior valid actions)")
        with ThreadPoolExecutor(max_workers=min(args.parallel, len(args.tasks))) as ex:
            results = [r for task_recs in ex.map(run_task_sequential, args.tasks)
                       for r in task_recs]
    else:
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
                component_lineage = hs.generated_component_lineage(
                    ctx[tid]["base_spec"], rec.effective
                )
                materialize(rec.effective, cdir, raw_spec_text=rec.raw_submission,
                            meta={"round": args.round, "task_id": tid, "k": rec.k,
                                  "spec_hash": rec.spec_hash,
                                  "changed_fields": rec.changed_fields,
                                  "base_package": bases[tid]["package"],
                                  "base_component_inventory":
                                      hs.generated_component_inventory(
                                          ctx[tid]["base_spec"]),
                                  "component_lineage": component_lineage,
                                  "effective": rec.effective})
                entry["dir"] = str(cdir)
                entry["component_lineage"] = component_lineage
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
                         "analysis": ctx[tid]["analysis"],
                         "candidates": cands}

    fixed_inference_slots = (
        os.environ.get("SAH_FIXED_INFERENCE_SLOTS", "0") == "1"
    )
    logical_round_raw = os.environ.get("LOGICAL_ROUND_INDEX", "")
    logical_round_index = (
        int(logical_round_raw) if logical_round_raw.strip() else None
    )
    if fixed_inference_slots and logical_round_index is None:
        raise RuntimeError(
            "fixed inference slots require LOGICAL_ROUND_INDEX for x-axis provenance"
        )
    nominal_total = 2 * int(args.k) if fixed_inference_slots else None
    (round_dir / "round.json").write_text(json.dumps({
        "round": args.round, "created": time.strftime("%Y%m%d-%H%M%S"),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "mode": "instance_wise",
        "h1_version": pio.H1_VERSION, "h1_package_hash": pio.h1_hash(),
        "proposer": {
            "base_urls": base_urls,
            "model": args.model,
            "seed": args.seed,
            "checkpoint": (
                os.environ.get("MPHI_PATH")
                or os.environ.get("MODEL_PATH")
                or None
            ),
            "executor_checkpoint": os.environ.get("MODEL_PATH") or None,
        },
        "tasks_order": args.tasks, "max_evals": args.max_evals, "k": args.k,
        "cross_round_inputs": {
            "bases": bases_input,
            "feedback": feedback_input,
            "seed_programs": program_input,
        },
        "inference_trajectory_budget": {
            "schema": 1,
            "axis_unit": "generated_agent_trajectory",
            "fixed_h1_plus_h2_slots": fixed_inference_slots,
            "logical_round_index": logical_round_index,
            "h1_slots_per_task": int(args.k),
            "h2_slots_per_task": (
                int(args.k) if fixed_inference_slots else None
            ),
            "nominal_total_slots_per_task": nominal_total,
            "shared_anchor_x": 1 if fixed_inference_slots else None,
            "axis_x_after_round": (
                1 + (logical_round_index + 1) * nominal_total
                if fixed_inference_slots else None
            ),
            "h2_decode_seed_base": int(os.environ.get("H2_SEED_BASE", "200000")),
            "h2_decode_seeds": [
                int(os.environ.get("H2_SEED_BASE", "200000"))
                + logical_round_index * 16 + k
                for k in range(int(args.k))
            ],
            "analyzer_calls_excluded_from_axis": True,
            "post_submit_reviewer_model_calls": 0,
        },
        "program_ratchet_mode": os.environ.get(
            "SAH_PROGRAM_RATCHET_MODE", "legacy_qd"
        ),
        "eval_timeout_s": int(float(os.environ.get("EVAL_TIMEOUT", "0") or 0)),
        "trajectory_wall_timeout_s": int(float(
            os.environ.get("ROLLOUT_WALL_TIMEOUT", "0") or 0
        )),
        "proposal_parallelism": {
            "requested_workers": int(args.parallel),
            "serving_replicas": len(base_urls),
        },
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
    prompts = json.loads((round_dir / "prompts.json").read_text())
    trajs = {(t["task_id"], t["k"]): t
             for t in json.loads((round_dir / "trajectories.json").read_text())}
    system_text = (pio.H1_PACKAGE / "system.md").read_text()

    adv_mode = os.environ.get("SAH_ADV", "v2")
    # v3 == v2 except on no_signal groups, so results alone can't tell you which
    # impl ran — log it so collect.log is proof the env survived sbatch/srun.
    print(f"[collect] advantage impl: SAH_ADV={adv_mode} "
          f"(hist_lambda={os.environ.get('SAH_HIST_LAMBDA', '-')})")
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
        elif adv_mode == "anchored":
            g = rw.compute_task_group_anchored(
                task_id=tid, candidates=pt["candidates"],
                rollout_root=round_dir / "rollouts", base_score=float(pt["base_score"]),
                ceiling=ceilings.get(tid))
            print(f"  [{tid}] advantages: {g['adv_mode']} ceiling={g.get('ceiling')}")
        elif adv_mode == "v3":
            g = rw.compute_task_group_v3(
                task_id=tid, candidates=pt["candidates"],
                rollout_root=round_dir / "rollouts", base_score=float(pt["base_score"]),
                ceiling=ceilings.get(tid), sharpen_alpha=float(os.environ.get("SAH_ALPHA", "0.3")),
                hist_lambda=float(os.environ.get("SAH_HIST_LAMBDA", "0.3")))
            print(f"  [{tid}] advantages: {g['adv_mode']} ceiling={g.get('ceiling')}")
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
            # anti-leak (campaign_config: leakage_guard): the analyst_note is the
            # only free-form text reaching the proposer; drop it if it carries a
            # leak marker, else neutralize unproven result-claim words so they
            # can't survive as facts. Default-on; a no-op on clean structured notes.
            if os.environ.get("SAH_LEAK_NEUTRALIZE", "1") == "1":
                from outer.leak_guard import code_signals, sanitize_note
                dropped_for = code_signals(prev_note)
                prev_note = sanitize_note(prev_note)
                if dropped_for:
                    print(f"[leak-guard] {tid}: analyst_note DROPPED "
                          f"(code-injection signals: {dropped_for})")
            if prev_note:
                feedback[tid]["analyst_note"] = prev_note
    fb_path.write_text(json.dumps(feedback, indent=1))
    (round_dir / "task_feedback_after.json").write_text(
        json.dumps(feedback, indent=1)
    )

    # Route-independent program inheritance.  Canonical comparison runs set
    # SAH_PROGRAM_RATCHET_MODE=strict_single; legacy exploratory campaigns keep
    # their historical QD/crossover memory behind an explicit mode.
    bp_path = round_dir.parent / "best_programs.json"
    ratchet_mode = os.environ.get("SAH_PROGRAM_RATCHET_MODE", "legacy_qd")
    ratchet_mode_source = (
        "env" if "SAH_PROGRAM_RATCHET_MODE" in os.environ else "default"
    )
    if (os.environ.get("SAH_REQUIRE_STRICT_RATCHET", "0") == "1"
            and ratchet_mode != "strict_single"):
        raise RuntimeError(
            "SAH_REQUIRE_STRICT_RATCHET=1 but program ratchet mode is "
            f"{ratchet_mode!r} ({ratchet_mode_source}); canonical campaigns "
            "must run strict_single"
        )
    logical_index = (
        meta.get("inference_trajectory_budget") or {}
    ).get("logical_round_index")
    try:
        best_programs = json.loads(bp_path.read_text()) if bp_path.exists() else {}
        if not isinstance(best_programs, dict):
            raise TypeError("program incumbent registry must be a JSON object")
    except Exception as exc:
        if ratchet_mode == "strict_single":
            raise RuntimeError(
                f"canonical program incumbent registry is unreadable: {bp_path}"
            ) from exc
        best_programs = {}
    if ratchet_mode == "strict_single" and logical_index not in (None, 0) \
            and not bp_path.is_file():
        raise RuntimeError(
            f"canonical post-cold round lacks program incumbent registry: {bp_path}"
        )
    best_programs, ratchet_audit = update_program_ratchet(
        mode=ratchet_mode,
        round_dir=round_dir,
        groups=groups,
        bases_in=meta.get("bases_in", {}),
        previous=best_programs,
        round_id=int(meta["round"]),
    )
    for tid, row in ratchet_audit["tasks"].items():
        groups[tid]["program_ratchet"] = row
        groups[tid]["accepted_improvement"] = bool(row.get("promoted"))
        if ratchet_mode == "strict_single" and groups[tid].get("improved") \
                and not row.get("promoted"):
            # A raw score cannot advance H2 when it cannot be bound to a newly
            # improved program from the same rollout.  This closes the legacy
            # step-0/inherited-program attribution hole.
            pt = meta["per_task"][tid]
            next_bases[tid] = {
                "package": pt["base_package"],
                "score": pt["base_score"],
                "seed_score": pt["seed_score"],
                "from": "unchanged_program_attribution_failed",
            }
            # Do not let an unbound step-0/noisy score update proposer weights
            # indirectly.  Keeping the diagnostic rewards while zeroing every
            # task-row advantage makes replay conversion skip this update.
            suppress_task_training(batch_rows, tid, row.get("reason"))
            groups[tid]["training_suppressed"] = True
            groups[tid]["training_suppression_reason"] = row.get("reason")
        if tid in feedback:
            feedback[tid]["accepted_improvement"] = bool(row.get("promoted"))
            feedback[tid]["program_ratchet_reason"] = row.get("reason")
            feedback[tid]["outgoing_base_score"] = next_bases[tid]["score"]
        print(
            f"  [program-ratchet:{ratchet_mode}] {tid}: "
            f"promoted={row.get('promoted')} reason={row.get('reason', 'legacy')}"
        )

    bp_path.write_text(json.dumps(best_programs, indent=1))
    (round_dir / "best_programs_after.json").write_text(
        json.dumps(best_programs, indent=1)
    )
    ratchet_audit["mode_source"] = ratchet_mode_source
    ratchet_audit["strict_required"] = (
        os.environ.get("SAH_REQUIRE_STRICT_RATCHET", "0") == "1"
    )
    (round_dir / "program_ratchet_audit.json").write_text(
        json.dumps(ratchet_audit, indent=2)
    )
    # Rewrite after the joint H2/program transition so the next context sees
    # the accepted state, not merely a noisy/raw candidate maximum.
    fb_path.write_text(json.dumps(feedback, indent=1))
    (round_dir / "task_feedback_after.json").write_text(
        json.dumps(feedback, indent=1)
    )

    with open(round_dir / "grpo_batch.jsonl", "w") as f:
        for row in batch_rows:
            f.write(json.dumps(row) + "\n")
    (round_dir / "round_summary.json").write_text(json.dumps({
        "round": meta["round"], "groups": groups,
        "inference_trajectory_budget": meta.get("inference_trajectory_budget"),
        "improved_tasks": [t for t, g in groups.items() if g["improved"]],
        "accepted_improved_tasks": [
            t for t, g in groups.items() if g.get("accepted_improvement")
        ],
    }, indent=2))
    (round_dir / "next_bases.json").write_text(json.dumps(next_bases, indent=2))
    n_imp = sum(bool(g.get("accepted_improvement")) for g in groups.values())
    print(f"[collect] {len(batch_rows)} GRPO rows | {n_imp}/{len(groups)} tasks accepted-improved "
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
    p.set_defaults(fn=cmd_propose)

    c = sub.add_parser("collect", help="per-task rewards + GRPO batch + next bases")
    c.add_argument("--round-dir", required=True)
    c.set_defaults(fn=cmd_collect)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
