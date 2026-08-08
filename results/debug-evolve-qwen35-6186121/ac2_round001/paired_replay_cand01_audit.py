#!/usr/bin/env python3
"""Bind AC2 cand01 to its exact same-seed retrospective parent control."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TASK_ID = "eft__math__second_autocorr_ineq"


def resolve_one(root: Path, pattern: str) -> tuple[Path, dict]:
    paths = sorted(root.glob(pattern))
    if len(paths) != 1:
        raise RuntimeError(
            f"expected exactly one artifact below {root} for {pattern!r}, got {paths}"
        )
    return paths[0], json.loads(paths[0].read_text())


def program_sha(row: dict) -> str | None:
    program = row.get("best_program")
    return hashlib.sha256(program.encode()).hexdigest() if program else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--control-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    candidate_root = (
        args.run_dir / "rounds" / "round001" / "rollouts" / TASK_ID / "cand01"
    )
    candidate_path, candidate = resolve_one(
        candidate_root, f"*/results/{TASK_ID}.json"
    )
    control_path, control = resolve_one(
        args.control_dir, f"*/results/{TASK_ID}.json"
    )

    assertions = {
        "same_decode_seed": candidate.get("decode_seed") == control.get("decode_seed") == 200001,
        "same_seed_program_sha256": (
            (candidate.get("seed_program_provenance") or {}).get("program_sha256")
            == (control.get("seed_program_provenance") or {}).get("program_sha256")
        ),
        "same_seed_registry_sha256": (
            (candidate.get("seed_program_provenance") or {}).get("registry_sha256")
            == (control.get("seed_program_provenance") or {}).get("registry_sha256")
        ),
        "same_eval_budget": (
            (candidate.get("ledger") or {}).get("max_evaluator_calls")
            == (control.get("ledger") or {}).get("max_evaluator_calls")
            == 2
        ),
        "both_score_eligible": (
            candidate.get("score_eligible") is not False
            and control.get("score_eligible") is not False
        ),
    }
    if not all(assertions.values()):
        raise RuntimeError(f"paired-control contract failed: {assertions}")

    candidate_score = float(candidate["best_score"])
    control_score = float(control["best_score"])
    payload = {
        "schema": "paired-parent-control/1.0",
        "task_id": TASK_ID,
        "candidate": "cand01",
        "pairing": "same_task_program_budget_model_decode_seed",
        "assertions": assertions,
        "candidate_result": str(candidate_path),
        "control_result": str(control_path),
        "candidate_score": candidate_score,
        "control_score": control_score,
        "causal_delta": candidate_score - control_score,
        "candidate_program_sha256": program_sha(candidate),
        "control_program_sha256": program_sha(control),
        "candidate_stop_reason": candidate.get("stop_reason"),
        "control_stop_reason": control.get("stop_reason"),
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
