"""Per-task harness session: state the tools read/mutate, plus the budget ledger.

The inner harness runs a NexAU agent whose tools operate on a single
:class:`InnerSession` held in a contextvar (mirrors Weave's RuntimeBridge
pattern). The session owns the current candidate program, best-so-far tracking
(the reward), and the external budget ledger (plan.md §8.4: usage is reserved
and accounted here, never self-reported by the harness).
"""
from __future__ import annotations

import contextvars
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from inner import program_edit as pe
from inner.eft_task import EFTTask
from inner.eval_runner import EvalOutcome, evaluate_program


@dataclass
class BudgetLedger:
    """External accounting of every model/evaluator call (plan.md §8.4)."""

    max_evaluator_calls: int = 10
    evaluator_calls: int = 0
    max_probe_calls: int = 30
    probe_calls: int = 0
    edit_calls: int = 0
    llm_input_tokens: int = 0
    llm_output_tokens: int = 0
    llm_calls: int = 0
    sandbox_seconds: float = 0.0

    def evaluator_budget_left(self) -> int:
        return max(0, self.max_evaluator_calls - self.evaluator_calls)

    def evaluator_exhausted(self) -> bool:
        return self.evaluator_calls >= self.max_evaluator_calls


@dataclass
class StepRecord:
    step: int
    kind: str  # "seed" | "edit_eval"
    edit_mode: str
    edit_note: str
    combined_score: float
    validity: float
    error: Optional[str]
    wall_s: float
    is_new_best: bool


@dataclass
class InnerSession:
    task: EFTTask
    ledger: BudgetLedger
    eval_timeout_s: Optional[float] = None
    python_exe: Optional[str] = None
    checkpoint_path: Optional[str] = None  # if set, best-so-far is written here after each new best (wall-safe)

    current_program: str = ""
    best_score: float = float("-inf")
    best_program: str = ""
    best_metrics: Dict[str, float] = field(default_factory=dict)
    history: List[StepRecord] = field(default_factory=list)
    _pending_edit_note: str = "seed"
    _pending_edit_mode: str = "seed"

    def __post_init__(self) -> None:
        if not self.current_program:
            self.current_program = self.task.initial_program

    # -- tool-facing operations -------------------------------------------- #
    def apply_edit(self, code: str) -> str:
        """Apply an edit in either OpenEvolve format M0 knows:

        * SEARCH/REPLACE diff (``<<<<<<< SEARCH`` ... ``>>>>>>> REPLACE``) applied
          to the full current program — targeted changes, the OpenEvolve default;
        * otherwise a full rewrite of the EVOLVE-BLOCK body (fences optional).
        """
        self.ledger.edit_calls += 1
        if "<<<<<<< SEARCH" in code:
            new_prog, n = pe.apply_diff(self.current_program, code)
            if n > 0:
                self.current_program = new_prog
                self._pending_edit_mode, self._pending_edit_note = "diff", f"applied {n} diff block(s)"
                return f"edit staged (diff: {n} block(s) applied). Call evaluate_solution to score it."
            return (
                "No SEARCH section matched the current program verbatim, so nothing "
                "changed. Copy the exact lines to replace into the SEARCH block, or "
                "send the full EVOLVE-BLOCK code instead."
            )
        raw = code
        if "```" in raw:
            extracted = pe.parse_full_rewrite(raw, self.task.language)
            if extracted:
                raw = extracted
        if pe.BLOCK_START in raw and pe.BLOCK_END in raw:
            raw = pe.split_program(raw).block
        self.current_program = pe.split_program(self.current_program).assemble(raw)
        self._pending_edit_mode, self._pending_edit_note = "full_rewrite", "spliced new EVOLVE-BLOCK"
        return "edit staged (full EVOLVE-BLOCK replaced). Call evaluate_solution to score it."

    def evaluate(self) -> EvalOutcome:
        out = evaluate_program(
            self.task, self.current_program,
            timeout_s=self.eval_timeout_s,
            python_exe=self.python_exe or __import__("sys").executable,
        )
        self.ledger.evaluator_calls += 1
        self.ledger.sandbox_seconds += out.wall_s
        is_best = out.combined_score > self.best_score
        if is_best:
            self.best_score = out.combined_score
            self.best_program = self.current_program
            self.best_metrics = out.metrics
            self._write_checkpoint()
        self.history.append(StepRecord(
            step=len(self.history), kind=self._pending_edit_mode if self._pending_edit_mode != "seed" else "seed",
            edit_mode=self._pending_edit_mode, edit_note=self._pending_edit_note,
            combined_score=out.combined_score, validity=out.validity, error=out.error,
            wall_s=out.wall_s, is_new_best=is_best,
        ))
        self._pending_edit_mode, self._pending_edit_note = "edit_eval", ""
        return out

    def probe(self, subsample: int = 2000) -> EvalOutcome:
        """Cheap approximate evaluation on subsampled data (first N CSV rows).

        Guidance only: does NOT count against the evaluation budget and does
        NOT update best-so-far (probe scores are not comparable to full ones).
        """
        self.ledger.probe_calls += 1
        out = evaluate_program(
            self.task, self.current_program,
            timeout_s=min(self.eval_timeout_s or 120.0, 120.0),
            python_exe=self.python_exe or __import__("sys").executable,
            subsample=subsample,
        )
        self.history.append(StepRecord(
            step=len(self.history), kind="probe",
            edit_mode="probe", edit_note=f"subsample={subsample}",
            combined_score=out.combined_score, validity=out.validity,
            error=out.error, wall_s=out.wall_s, is_new_best=False,
        ))
        return out

    def seed_baseline(self) -> EvalOutcome:
        """Evaluate the seed once to initialise best-so-far (not charged to budget)."""
        self._pending_edit_mode, self._pending_edit_note = "seed", "seed program"
        out = self.evaluate()
        self.ledger.evaluator_calls -= 1  # seed eval is the harness baseline, not agent budget
        return out

    def _write_checkpoint(self) -> None:
        """Persist best-so-far after each new best, so a wall-kill never loses it."""
        if not self.checkpoint_path:
            return
        try:
            import json
            from pathlib import Path
            p = Path(self.checkpoint_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(p.suffix + ".tmp")
            tmp.write_text(json.dumps({
                "task_id": self.task.task_id, "source": self.task.source,
                "best_score": self.best_score, "best_metrics": self.best_metrics,
                "evaluations": self.ledger.evaluator_calls,
                "best_program": self.best_program,
            }))
            tmp.replace(p)  # atomic
        except Exception:
            pass  # checkpointing must never break a run

    # -- serialization ----------------------------------------------------- #
    def summary(self) -> Dict[str, Any]:
        return {
            "task_id": self.task.task_id,
            "source": self.task.source,
            "best_score": self.best_score,
            "best_metrics": self.best_metrics,
            "ledger": asdict(self.ledger),
            "steps": [asdict(s) for s in self.history],
        }


# --------------------------------------------------------------------------- #
# contextvar bridge so module-level NexAU tools reach the active session
# --------------------------------------------------------------------------- #
_CURRENT: "contextvars.ContextVar[Optional[InnerSession]]" = contextvars.ContextVar(
    "inner_session", default=None
)


def get_session() -> InnerSession:
    s = _CURRENT.get()
    if s is None:
        raise RuntimeError("no active InnerSession (tool called outside session_scope)")
    return s


@contextmanager
def session_scope(session: InnerSession):
    token = _CURRENT.set(session)
    try:
        yield session
    finally:
        _CURRENT.reset(token)
