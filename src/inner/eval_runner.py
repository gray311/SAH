"""Isolated evaluation of a candidate program against an EFT task.

Runs the task evaluator in a subprocess with a hard wall-clock timeout, so a
crashing / hanging / import-polluting candidate cannot take down the harness
(plan.md §6.1, §13.2). Returns a normalized :class:`EvalOutcome`.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

from inner.eft_task import EFTTask

_WORKER = Path(__file__).with_name("_eval_worker.py")


def _stop_process_group(pgid: int, *, grace_s: float = 1.0) -> None:
    """Stop every evaluator descendant, even after the worker has exited.

    Some third-party evaluators launch an additional candidate subprocess and
    return after their own timeout without reaping it. The worker is always a
    fresh session leader, so its process group is an exact cleanup boundary.
    """
    try:
        os.killpg(pgid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    deadline = time.monotonic() + grace_s
    while time.monotonic() < deadline:
        try:
            os.killpg(pgid, 0)
        except (ProcessLookupError, PermissionError):
            return
        time.sleep(0.05)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


@dataclass
class EvalOutcome:
    combined_score: float
    validity: float
    error: Optional[str]
    wall_s: float
    timed_out: bool = False
    metrics: Dict[str, float] = field(default_factory=dict)

    @property
    def valid(self) -> bool:
        return self.error is None and self.validity >= 1.0


def evaluate_program(
    task: EFTTask,
    program: str,
    *,
    timeout_s: Optional[float] = None,
    python_exe: str = sys.executable,
    workdir: Optional[Path] = None,
    subsample: Optional[int] = None,
) -> EvalOutcome:
    """Write ``program`` to a temp file and score it with ``task``'s evaluator."""
    timeout = timeout_s if timeout_s is not None else task.per_eval_timeout_s
    hard_timeout = timeout + 30.0  # margin over the evaluator's own internal timeout
    tmp = Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix="eft_eval_"))
    tmp.mkdir(parents=True, exist_ok=True)
    prog_path = tmp / "candidate.py"
    res_path = tmp / "result.json"
    req_path = tmp / "request.json"
    prog_path.write_text(program)
    req_path.write_text(json.dumps({
        "evaluator_path": str(task.evaluator_path),
        "program_path": str(prog_path),
        "shim_path": str(task.shim_path),
        "result_path": str(res_path),
        "subsample": subsample,
    }))

    env = dict(os.environ)
    # let the evaluator import its runtime shim + the candidate's deps
    extra = f"{task.shim_path}{os.pathsep}{task.task_dir}"
    env["PYTHONPATH"] = extra + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")

    t0 = time.time()
    timed_out = False
    worker = subprocess.Popen(
        [python_exe, str(_WORKER), str(req_path)],
        env=env,
        cwd=str(tmp),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        worker.wait(timeout=hard_timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
    finally:
        # Always close the isolated group. A worker may exit normally while a
        # buggy evaluator leaves its candidate subprocess running.
        _stop_process_group(worker.pid)
        if worker.poll() is None:
            try:
                worker.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                pass
    dt = time.time() - t0

    if timed_out:
        return EvalOutcome(0.0, 0.0, f"Timeout after {hard_timeout:.0f}s", dt, timed_out=True)
    if not res_path.exists():
        return EvalOutcome(0.0, 0.0, "worker produced no result (crash?)", dt)
    try:
        d = json.loads(res_path.read_text())
    except Exception as e:
        return EvalOutcome(0.0, 0.0, f"bad worker result: {e}", dt)
    return EvalOutcome(
        combined_score=float(d.get("combined_score", 0.0)),
        validity=float(d.get("validity", 0.0)),
        error=d.get("error"),
        wall_s=dt,
        metrics=d.get("metrics", {}),
    )
