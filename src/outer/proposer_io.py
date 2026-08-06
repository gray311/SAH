"""Proposer I/O — round-context builder + versioning (NOT the H1 harness).

The H1 harness itself (system prompt, tools, skill, sampling) is the declarative
NexAU package at ``src/outer/harness/`` — fixed forever (plan.md §0.3). This
module is only the surrounding glue: it builds the round-varying USER message
fed to that harness, renders feedback, and hashes the package for provenance.
Renamed from ``h1.py`` (that name wrongly implied it *was* H1).

It builds the round-varying USER message for ONE task instance (plan.md §2.2:
H_j ~ pi_phi(H | tau, H1)): the task's public spec, its seed program (excerpt),
the current best harness spec for this task, and its scores.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict

H1_VERSION = "h1/2.0-file-native"
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

# Current H2 harness
A complete private filesystem copy of the current H2 is available through the
harness file tools. Do not assume its contents from prior rounds. Your FIRST
action must be `harness_shell(command="cat agent.yaml")`. Follow mounts only as
needed. Next read `prompt.md`. For example, if you may change tools, run
`ls tools/`, then `cat` the specific schema and implementation before editing.

# Task
Design ONE H2 tailored to THIS task by inspecting and editing that filesystem.
Diagnose why the current H2 reaches only {base_score:.6g}, make one coherent
file-level change, call validate_harness, then submit_harness."""


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


def render_feedback(fb: dict) -> str:
    """Compact previous-visit telemetry section appended to the H1 user message."""
    lines = [
        "\n\n## Telemetry from the previous visit (round %s)" % fb.get("round"),
    ]
    if fb.get("analyst_note"):
        lines.append("ANALYST NOTE: " + fb["analyst_note"])
    best = fb.get("best_score") or fb.get("base_score", 0.0)
    accepted = fb.get("accepted_improvement")
    accepted_score = fb.get("outgoing_base_score", fb.get("base_score", 0.0))
    if accepted is False and best > fb.get("base_score", 0.0):
        score_line = (
            "The raw candidate maximum was %.6g, but it was not accepted "
            "(%s); the incumbent remains %.6g."
            % (best, fb.get("program_ratchet_reason", "attribution failed"), accepted_score)
        )
    else:
        score_line = (
            "The starting score was %.6g; the best of 8 candidate harnesses reached %.6g."
            % (fb.get("base_score", 0.0), best)
        )
    lines += [
        score_line,
        "%s of the candidates made NO progress past the starting program." % fb.get("n_stuck_at_base", "?"),
        "Per-candidate outcomes (k: score, evals used, stop reason, changed fields):",
    ]
    for c in fb.get("candidates", []):
        if c.get("invalid"):
            lines.append("  k%s: INVALID SPEC (never rolled out)" % c["k"])
            continue
        if c.get("tools"):
            lines.append("  k%s: tools=%s" % (c["k"], ", ".join(c["tools"])))
        lines.append("  k%s: score=%s evals=%s stop=%s changed=%s%s" % (
            c["k"],
            ("%.6g" % c["score"]) if c.get("score") is not None else "?",
            c.get("evals"), c.get("stop"), ",".join(c.get("changed", [])),
            (" err=" + c["err"]) if c.get("err") else ""))
    lines.append(
        "Diagnose WHY those harnesses failed to progress (e.g. the strategy they pushed "
        "saturated, edits kept failing, budget was wasted on timeouts) and design a harness "
        "that overcomes that specific failure mode. Do not resubmit a near-copy of a design "
        "that already stalled.")
    return "\n".join(lines)


def render_prior_actions(actions: list) -> str:
    """Sequential-sampling context: the VALID actions already proposed for THIS
    task in THIS batch, so this sample proposes something genuinely different
    (Adaptive within-batch diversity). Only the changed axes + a compact spec
    outline are shown — no scores, no rollout outcomes (those aren't available
    yet mid-batch, and withholding them keeps the channel leak-free)."""
    if not actions:
        return ""
    lines = ["\n\n## Already proposed this batch (do NOT paraphrase these)"]
    for a in actions:
        fields = ", ".join(a.get("changed_fields") or []) or "(no changes)"
        spec = a.get("spec") or {}
        tools = [t.get("name") for t in (spec.get("new_tools") or []) if isinstance(t, dict)]
        skills = [s.get("name") for s in (spec.get("new_skills") or []) if isinstance(s, dict)]
        extra = ""
        if tools:
            extra += " new_tools=[%s]" % ", ".join(filter(None, tools))
        if skills:
            extra += " new_skills=[%s]" % ", ".join(filter(None, skills))
        lines.append("  - k%s changed: %s%s" % (a.get("k"), fields, extra))
    lines.append("Propose a design that explores a DIFFERENT axis or strategy "
                 "than every entry above.")
    return "\n".join(lines)
