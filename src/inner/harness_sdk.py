"""Capability surface for M_phi-generated custom tools (h2spec/1.0).

A generated tool is a function ``run(ctx, args)``. ``ctx`` is the ONLY door to
the outside world: it exposes a small, audited set of operations bridged to the
inner session. Generated code passes static gates that forbid imports beyond a
whitelist and any direct I/O, so this context IS the tool's capability set —
the evaluator internals, benchmark answers, network, and the filesystem outside
the sandbox scratch dir are all unreachable by construction.

Anti-reward-hacking invariants:
  * no access to evaluator source or task answer files;
  * ``probe``/``evaluate`` go through the session's official pipeline and
    budgets (probes capped, evaluations debit the real budget);
  * ``read_input_sample`` serves at most SAMPLE_CAP rows of declared task
    input files, read-only.
"""
from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

SAMPLE_CAP = 5000
SCRATCH_CAP_BYTES = 8 * 1024 * 1024


class ToolContext:
    """Capability object handed to generated tools."""

    def __init__(self, session, scratch_dir: Path):
        self._s = session
        self._scratch = Path(scratch_dir)
        self._scratch.mkdir(parents=True, exist_ok=True)

    # ---- program access ---------------------------------------------------
    def get_program(self) -> str:
        """Current working program text."""
        return self._s.current_program

    def get_best_program(self) -> str:
        return self._s.best_program or self._s.current_program

    def best_score(self) -> float:
        return float(self._s.best_score)

    def stage_edit(self, code: str) -> str:
        """Stage a SEARCH/REPLACE diff or full EVOLVE-BLOCK replacement
        (identical semantics to the edit_solution tool)."""
        return self._s.apply_edit(code)

    # ---- evaluation -------------------------------------------------------
    def probe(self, subsample: int = 2000) -> Dict[str, Any]:
        """Cheap approximate evaluation (separate probe budget)."""
        if self._s.ledger.probe_calls >= self._s.ledger.max_probe_calls:
            return {"error": "probe budget exhausted"}
        out = self._s.probe(subsample=subsample)
        return {"combined_score": out.combined_score, "validity": out.validity,
                "error": out.error}

    def evaluate(self) -> Dict[str, Any]:
        """Full official evaluation — debits the REAL evaluation budget."""
        if self._s.ledger.exhausted():
            return {"error": "evaluation budget exhausted"}
        out = self._s.evaluate()
        return {"combined_score": out.combined_score, "validity": out.validity,
                "error": out.error}

    def budget_left(self) -> Dict[str, int]:
        return {"evaluations": self._s.ledger.evaluator_budget_left(),
                "probes": self._s.ledger.max_probe_calls - self._s.ledger.probe_calls}

    # ---- task data (read-only, capped) ------------------------------------
    def list_task_inputs(self) -> List[str]:
        """Names of data files in the task directory (read-only view)."""
        td = Path(self._s.task.task_dir)
        out = []
        for p in sorted(td.rglob("*")):
            if p.is_file() and p.suffix in (".csv", ".txt", ".json") \
                    and "evaluator" not in str(p.relative_to(td)):
                out.append(str(p.relative_to(td)))
        return out[:50]

    def read_input_sample(self, name: str, nrows: int = 1000) -> str:
        """First ``nrows`` lines of a task input file (never evaluator code)."""
        td = Path(self._s.task.task_dir).resolve()
        p = (td / name).resolve()
        if not str(p).startswith(str(td)) or "evaluator" in name:
            return "ERROR: path not allowed"
        if not p.exists():
            return "ERROR: no such file"
        nrows = min(int(nrows), SAMPLE_CAP)
        buf = io.StringIO()
        with open(p, "r", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= nrows:
                    break
                buf.write(line)
        return buf.getvalue()

    # ---- scratch ----------------------------------------------------------
    def scratch_write(self, name: str, text: str) -> str:
        p = (self._scratch / os.path.basename(name)).resolve()
        if len(text) > SCRATCH_CAP_BYTES:
            return "ERROR: too large"
        p.write_text(text)
        return str(p)

    def scratch_read(self, name: str) -> str:
        p = (self._scratch / os.path.basename(name)).resolve()
        return p.read_text() if p.exists() else "ERROR: no such file"

    def log(self, message: str) -> None:
        self._s.history_note(f"[custom-tool] {str(message)[:400]}")


class MockContext(ToolContext):
    """Self-test double: no session needed; canned responses."""

    def __init__(self, scratch_dir: Path, program: str = "# EVOLVE-BLOCK-START\npass\n# EVOLVE-BLOCK-END",
                 sample: str = "a,b\n1,2\n3,4\n"):
        self._scratch = Path(scratch_dir)
        self._scratch.mkdir(parents=True, exist_ok=True)
        self._program = program
        self._sample = sample
        self.calls: List[str] = []

    def get_program(self): self.calls.append("get_program"); return self._program
    def get_best_program(self): self.calls.append("get_best_program"); return self._program
    def best_score(self): self.calls.append("best_score"); return 0.5
    def stage_edit(self, code):
        self.calls.append("stage_edit")
        return "edit staged"
    def probe(self, subsample=2000):
        self.calls.append("probe")
        return {"combined_score": 0.5, "validity": 1.0, "error": None}
    def evaluate(self):
        self.calls.append("evaluate")
        return {"combined_score": 0.5, "validity": 1.0, "error": None}
    def budget_left(self): return {"evaluations": 10, "probes": 10}
    def list_task_inputs(self): return ["input.csv"]
    def read_input_sample(self, name, nrows=1000): return self._sample
