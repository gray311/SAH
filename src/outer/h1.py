"""H1 round-context builder + versioning (instance-wise).

The proposer harness H1 itself is the declarative NexAU package at
``src/outer/harness/`` — fixed forever (plan.md §0.3). This module builds the
round-varying USER message for ONE task instance (plan.md §2.2:
H_j ~ pi_phi(H | tau, H1)): the task's public spec, its seed program (excerpt),
the current best harness spec for this task, and its scores.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict

import yaml

H1_VERSION = "h1/0.3-instancewise"
H1_PACKAGE = Path(__file__).resolve().parent / "harness"

_SEED_PROGRAM_CAP = 5000  # chars of the seed program shown to the proposer

USER_TEMPLATE = """# Task instance: {task_id}

## Public task description
{task_spec}

## Seed program (the executor edits the EVOLVE-BLOCK region){seed_note}
```python
{seed_program}
```

## Scores on this task (combined_score, higher is better; budget {max_evals} evals)
- seed program alone: {seed_score:.6g}
- current harness best: {base_score:.6g}{stuck_tag}

# Current harness for this task (the spec you are mutating; omitted fields inherit from it)
```yaml
{base_spec_yaml}
```

# Task
Design ONE harness spec tailored to THIS task. Load the harness-design skill,
analyze why the current harness reaches only {base_score:.6g} here, draft your
spec, validate_spec it, then submit_spec it."""


def build_user_message(*, task_id: str, task_spec: str, seed_program: str,
                       seed_score: float, base_score: float,
                       base_spec: Dict[str, Any], max_evals: int = 20) -> str:
    prog = seed_program.strip()
    note = ""
    if len(prog) > _SEED_PROGRAM_CAP:
        prog = prog[:_SEED_PROGRAM_CAP]
        note = f" (truncated to {_SEED_PROGRAM_CAP} chars)"
    stuck = "  <-- STUCK AT SEED: the harness makes no progress here" \
        if abs(base_score - seed_score) < 1e-9 else ""
    return USER_TEMPLATE.format(
        task_id=task_id,
        task_spec=task_spec.strip() or "(no public description; rely on the seed program)",
        seed_note=note,
        seed_program=prog,
        seed_score=seed_score,
        base_score=base_score,
        stuck_tag=stuck,
        base_spec_yaml=yaml.safe_dump(base_spec, sort_keys=False, allow_unicode=True,
                                      width=100).strip(),
        max_evals=max_evals,
    )


def h1_hash() -> str:
    """Hash the whole H1 package (every file) for provenance."""
    h = hashlib.sha256()
    for f in sorted(H1_PACKAGE.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(str(f.relative_to(H1_PACKAGE)).encode())
            h.update(f.read_bytes())
    return "sha256:" + h.hexdigest()[:16]
