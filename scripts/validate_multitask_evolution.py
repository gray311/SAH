#!/usr/bin/env python3
"""Validate the public multi-task evolution artifact layout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_task(task_root: Path) -> tuple[int, int, int]:
    evolution = load_json(task_root / "evolution.json")
    exported_rounds = 0
    candidates = 0
    executor_trajectories = 0
    for row in evolution["rounds"]:
        if row.get("status") != "exported":
            continue
        exported_rounds += 1
        local_round = int(row["local_round"])
        round_root = task_root / f"round{local_round:02d}"
        if not round_root.is_dir():
            raise AssertionError(f"missing round directory: {round_root}")
        candidate_dirs = sorted(round_root.glob("candidate*"))
        expected = len(row["candidates"])
        launched = int(row.get("launched_candidates", expected))
        if launched != expected:
            raise AssertionError(
                f"{round_root}: summary has {expected} candidates but launched {launched}"
            )
        if len(candidate_dirs) != expected:
            raise AssertionError(
                f"{round_root}: found {len(candidate_dirs)} candidates, expected {expected}"
            )
        round_summary = load_json(round_root / "round_summary.json")
        if round_summary != row:
            raise AssertionError(f"round summary mismatch: {round_root}")
        for candidate in candidate_dirs:
            summary = load_json(candidate / "candidate_summary.json")
            trajectory = candidate / "executor_trajectory.json"
            if trajectory.is_file() != bool(summary["executor_trajectory_available"]):
                raise AssertionError(f"trajectory availability mismatch: {candidate}")
            candidates += 1
            executor_trajectories += int(trajectory.is_file())
    return exported_rounds, candidates, executor_trajectories


def validate_full_trace(task_root: Path) -> tuple[int, int, int]:
    evolution = load_json(task_root / "evolution.json")
    rounds = evolution["rounds"]
    if len(rounds) != 1:
        raise AssertionError(f"expected one full-trace round: {task_root}")
    row = rounds[0]
    round_root = task_root / "round01"
    if load_json(round_root / "round_summary.json") != row:
        raise AssertionError(f"full-trace round summary mismatch: {task_root}")
    candidates = sorted(round_root.glob("candidate*"))
    if len(candidates) != int(row["candidate_count"]):
        raise AssertionError(f"full-trace candidate count mismatch: {task_root}")
    for candidate in candidates:
        for required in (
            "proposer_input.json",
            "proposer_trajectory.json",
            "proposer_submission.txt",
            "generated_harness.json",
            "executor_input.json",
            "executor_trajectory.json",
            "executor_result.json",
            "executor_program.py",
            "candidate_summary.json",
        ):
            if not (candidate / required).is_file():
                raise AssertionError(f"missing {required}: {candidate}")
        summary = load_json(candidate / "candidate_summary.json")
        if not summary["full_proposer_trajectory"] or not summary["full_executor_trajectory"]:
            raise AssertionError(f"trace incorrectly marked incomplete: {candidate}")
    return 1, len(candidates), len(candidates)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    # Parse every JSON document before checking cross-file invariants.
    json_count = 0
    for path in root.rglob("*.json"):
        load_json(path)
        json_count += 1

    rows = []
    for name in ("ERDOS_MIN_OVERLAP", "AC2", "AHC039", "EPLB"):
        rows.append((name, *validate_task(root / name)))
    rows.append(
        (
            "AC2_REPAIRED_FULL_TRACE",
            *validate_full_trace(root / "AC2_REPAIRED_FULL_TRACE"),
        )
    )
    for name, rounds, candidates, trajectories in rows:
        print(
            f"{name}: rounds={rounds} candidates={candidates} "
            f"executor_trajectories={trajectories}"
        )
    print(f"parsed_json_files={json_count}")


if __name__ == "__main__":
    main()
