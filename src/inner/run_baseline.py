"""Run the M0 + H2 baseline over the EFT held-out tasks.

Modes
-----
--seed-only : evaluate each task's seed program only (no model needed). Produces
              the H_simple baseline table + validates the eval pipeline.
default     : run the H2 NexAU agent (Qwen3.5-9B via a vLLM endpoint) per task.

Outputs a per-task result JSON + a summary.json/summary.csv under --out, with
run provenance (plan.md §21).

Examples
--------
  # pipeline check, no model:
  python run_baseline.py --seed-only --tiers tier0_cpu_nosetup tier1_cpu_lightsetup

  # real baseline against a served endpoint:
  python run_baseline.py --tiers tier0_cpu_nosetup tier1_cpu_lightsetup \\
      --base-url http://127.0.0.1:8800/v1 --model qwen3.5-9b \\
      --max-evals 10 --eval-python /path/to/env/bin/python --out runs/inner_baseline
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # put `src/` on path -> import inner.*

from inner.eft_task import load_tasks, get_task, EFTTask  # noqa: E402
from inner.eval_runner import evaluate_program  # noqa: E402


def _select(args) -> list:
    if args.ids:
        return [get_task(i) for i in args.ids]
    tiers = args.tiers or None
    tasks = load_tasks(include_simpletes_crossref=not args.no_simpletes, cost_tiers=tiers)
    if args.limit:
        tasks = tasks[: args.limit]
    return tasks


def _seed_only(task: EFTTask, args) -> dict:
    out = evaluate_program(task, task.initial_program,
                           timeout_s=args.eval_timeout, python_exe=args.eval_python)
    return {
        "task_id": task.task_id, "source": task.source, "cost_tier": task.cost_tier,
        "mode": "seed_only", "seed_score": out.combined_score, "best_score": out.combined_score,
        "delta": 0.0, "validity": out.validity, "error": out.error, "wall_s": out.wall_s,
        "evaluations": 1,
    }


def _agent_run(task: EFTTask, args, out_dir: Path) -> dict:
    from inner.harness_runner import LLMEndpoint, H2Config, run_task  # lazy (needs nexau)

    ep = LLMEndpoint(model=args.model, base_url=args.base_url, api_key=args.api_key,
                     temperature=args.temperature, top_p=args.top_p, max_tokens=args.max_tokens,
                     timeout=args.llm_timeout, enable_thinking=args.thinking)
    if args.max_iters > 0:
        max_iters = args.max_iters
    elif args.harness_dir:
        max_iters = None  # candidate package: respect its own agent.yaml max_iterations
    else:
        max_iters = 3 * args.max_evals + 8
    h2 = H2Config(max_evaluator_calls=args.max_evals, max_iterations=max_iters,
                  eval_timeout_s=args.eval_timeout, python_exe=args.eval_python)
    ckpt = str(out_dir / "checkpoints" / f"{task.task_id}.json")
    res = run_task(task, endpoint=ep, h2=h2, keep_trajectory=not args.no_trajectory,
                   checkpoint_path=ckpt,
                   harness_dir=Path(args.harness_dir) if args.harness_dir else None)
    return {**{k: v for k, v in asdict(res).items() if k != "trajectory"},
            "mode": "agent", "delta": res.best_score - res.seed_score,
            "evaluations": res.ledger.get("evaluator_calls", 0),
            "_full": asdict(res)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed-only", action="store_true", help="evaluate seeds only (no model)")
    ap.add_argument("--tiers", nargs="*", default=None,
                    help="cost tiers to include, e.g. tier0_cpu_nosetup tier1_cpu_lightsetup")
    ap.add_argument("--ids", nargs="*", default=None, help="explicit task_ids")
    ap.add_argument("--no-simpletes", action="store_true", help="exclude the 3 SimpleTES cross-ref tasks")
    ap.add_argument("--limit", type=int, default=0)
    # endpoint / sampling
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8800/v1"))
    ap.add_argument("--model", default=os.environ.get("INNER_MODEL", "qwen3.5-9b"))
    ap.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", "EMPTY"))
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--llm-timeout", type=float, default=600.0)
    ap.add_argument("--thinking", action="store_true", help="enable Qwen thinking (default off)")
    # budget / eval
    ap.add_argument("--max-evals", type=int, default=10, help="evaluator-call budget per task")
    ap.add_argument("--max-iters", type=int, default=0, help="agent-loop cap; 0 = auto (3*max_evals+8; candidate packages keep their agent.yaml value)")
    ap.add_argument("--harness-dir", default=None,
                    help="run a candidate H2 package (dir with agent.yaml) instead of the built-in inner/harness")
    ap.add_argument("--eval-timeout", type=float, default=None, help="override per-eval timeout (s)")
    ap.add_argument("--eval-python", default=os.environ.get("INNER_EVAL_PYTHON", sys.executable),
                    help="interpreter with the task deps (numpy/scipy/jax/...) for eval subprocess")
    ap.add_argument("--no-trajectory", action="store_true")
    ap.add_argument("--out", default=None, help="output dir (default runs/inner_baseline/<ts>)")
    args = ap.parse_args()

    ts = time.strftime("%Y%m%d-%H%M%S")
    default_root = Path(__file__).resolve().parents[2] / "runs" / "inner_baseline"
    out_dir = (Path(args.out) / ts) if args.out else (default_root / ts)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results").mkdir(exist_ok=True)

    tasks = _select(args)
    provenance = {
        "timestamp": ts, "mode": "seed_only" if args.seed_only else "agent",
        "n_tasks": len(tasks), "task_ids": [t.task_id for t in tasks],
        "base_url": args.base_url, "model": args.model, "temperature": args.temperature,
        "top_p": args.top_p, "max_tokens": args.max_tokens, "max_evals": args.max_evals,
        "eval_python": args.eval_python, "argv": sys.argv,
    }
    (out_dir / "provenance.json").write_text(json.dumps(provenance, indent=2))
    print(f"[run] {provenance['mode']} | {len(tasks)} tasks | out={out_dir}")

    rows = []
    for i, task in enumerate(tasks, 1):
        print(f"[{i}/{len(tasks)}] {task.task_id} ({task.cost_tier}) ...", flush=True)
        try:
            row = _seed_only(task, args) if args.seed_only else _agent_run(task, args, out_dir)
        except Exception as e:
            row = {"task_id": task.task_id, "source": task.source, "mode": "error",
                   "seed_score": None, "best_score": None, "delta": None,
                   "error": f"{type(e).__name__}: {e}"}
        full = row.pop("_full", None)
        (out_dir / "results" / f"{task.task_id}.json").write_text(
            json.dumps(full if full is not None else row, indent=2))
        rows.append(row)
        print(f"      best={row.get('best_score')} seed={row.get('seed_score')} "
              f"delta={row.get('delta')} evals={row.get('evaluations')} err={row.get('error')}")

    (out_dir / "summary.json").write_text(json.dumps(rows, indent=2))
    cols = ["task_id", "source", "cost_tier", "mode", "seed_score", "best_score",
            "delta", "validity", "evaluations", "error"]
    with open(out_dir / "summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    scored = [r for r in rows if r.get("best_score") is not None]
    if scored and not args.seed_only:
        improved = sum(1 for r in scored if (r.get("delta") or 0) > 1e-9)
        print(f"\n[done] {len(scored)} scored | improved over seed: {improved}/{len(scored)}")
    print(f"[done] summary -> {out_dir}/summary.csv")


if __name__ == "__main__":
    main()
