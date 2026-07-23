"""Subprocess worker: evaluate one candidate program with a task's evaluator.

Invoked as ``python _eval_worker.py <request.json>``. Keeps the (potentially
crashy, import-polluting, slow) evaluator import + call out of the harness
process. Writes a single JSON result to the ``result_path`` in the request;
never writes the result to stdout (evaluators print freely to stdout/stderr).

request.json = {
  "evaluator_path": "...evaluator.py",
  "program_path":   "...candidate.py",
  "shim_path":      "...runtime/skydiscover_min",   # on sys.path so evaluator imports
  "result_path":    "...result.json"
}
"""
import importlib.util
import inspect
import json
import sys
import traceback
from pathlib import Path


def _normalize(result):
    """Return {combined_score, validity, error, metrics} from any evaluator return."""
    # skydiscover EvaluationResult -> flatten .metrics
    if hasattr(result, "metrics") and isinstance(getattr(result, "metrics"), dict):
        d = dict(result.metrics)
    elif hasattr(result, "to_dict"):
        d = dict(result.to_dict())
    elif isinstance(result, dict):
        d = dict(result)
    else:
        return {"combined_score": 0.0, "validity": 0.0,
                "error": f"unrecognized evaluator return type: {type(result)}", "metrics": {}}
    score = d.get("combined_score", d.get("score", 0.0))
    try:
        score = float(score)
    except Exception:
        score = 0.0
    return {
        "combined_score": score,
        "validity": float(d.get("validity", 1.0 if d.get("error") in (None, "") else 0.0)),
        "error": d.get("error"),
        "metrics": {k: v for k, v in d.items() if isinstance(v, (int, float))},
    }


def main() -> None:
    req = json.loads(Path(sys.argv[1]).read_text())
    out = {"combined_score": 0.0, "validity": 0.0, "error": None, "metrics": {}}
    try:
        ev_path = Path(req["evaluator_path"])
        # make the evaluator importable: its own dir, the runtime shim, and the task dir
        for p in (req.get("shim_path"), str(ev_path.parent), str(ev_path.parent.parent)):
            if p and p not in sys.path:
                sys.path.insert(0, p)
        spec = importlib.util.spec_from_file_location("_eft_evaluator", str(ev_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        evaluate = getattr(mod, "evaluate")
        # call with program_path only (all task evaluators accept this; extras have defaults)
        try:
            result = evaluate(req["program_path"])
        except TypeError:
            sig = inspect.signature(evaluate)
            if "config" in sig.parameters:
                result = evaluate(req["program_path"], None)
            else:
                raise
        out = _normalize(result)
    except Exception as e:  # never raise out of the worker
        out = {"combined_score": 0.0, "validity": 0.0,
               "error": f"{type(e).__name__}: {e}",
               "traceback": traceback.format_exc().splitlines()[-3:], "metrics": {}}
    Path(req["result_path"]).write_text(json.dumps(out))


if __name__ == "__main__":
    main()
