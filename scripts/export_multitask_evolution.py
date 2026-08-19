#!/usr/bin/env python3
"""Export legacy multi-task evolution artifacts in the public CP26 layout.

The historical production runner retained complete proposer trajectories and
materialized H2 packages, but usually stored ``trajectory: null`` for the
executor.  This exporter never synthesizes a missing executor trajectory.  It
copies the exact executor result and creates ``executor_trajectory.json`` only
when the source actually contains a non-null trajectory.

The per-round summary also separates an inherited seed jump from an improvement
made by the executor in that round.  That distinction is necessary for the
stitched legacy campaigns used by the paper curves.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any, Iterable


TASK_SLUGS = {
    "eft__math__erdos_min_overlap": "ERDOS_MIN_OVERLAP",
    "eft__math__second_autocorr_ineq": "AC2",
    "eft__math__hadamard_maximal_det": "HADAMARD_MAX_DET",
    "eft__ahc_simpletes__ahc039": "AHC039",
    "adrs__eplb": "EPLB",
}

EPS = 1e-12
PUBLIC_HARNESS_EXCLUDES = {
    "component_manifest.json",
    "smoke_test.json",
    "meta.json",
    "REFERENCE_CARD.md",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n")


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def copy_harness(source: Path, destination: Path) -> int:
    """Copy an as-run harness while omitting caches and duplicated meta.json."""
    if not source.is_dir():
        return 0
    copied = 0
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if path.name in PUBLIC_HARNESS_EXCLUDES:
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1
    return copied


def task_group(round_summary: dict[str, Any], task_id: str) -> dict[str, Any]:
    groups = round_summary.get("groups", [])
    if isinstance(groups, dict):
        group = groups.get(task_id)
        if isinstance(group, dict):
            return group
        raise KeyError(f"{task_id} is absent from round {round_summary.get('round')}")
    for group in groups:
        if group.get("task_id") == task_id:
            return group
    raise KeyError(f"{task_id} is absent from round {round_summary.get('round')}")


def proposer_entries(round_root: Path, task_id: str) -> dict[int, dict[str, Any]]:
    path = round_root / "trajectories.json"
    if not path.is_file():
        return {}
    entries: dict[int, dict[str, Any]] = {}
    for row in read_json(path):
        if row.get("task_id") == task_id and isinstance(row.get("k"), int):
            entries[int(row["k"])] = row
    return entries


def rollout_candidates(round_root: Path, task_id: str, k: int) -> list[Path]:
    root = round_root / "rollouts" / task_id / f"cand{k:02d}"
    if not root.is_dir():
        return []
    return sorted(root.glob("*/results/*.json"))


def select_rollout(paths: Iterable[Path], expected_score: float | None) -> Path | None:
    scored: list[tuple[float, str, Path]] = []
    for path in paths:
        try:
            result = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        score = finite_number(result.get("best_score"))
        distance = (
            abs(score - expected_score)
            if score is not None and expected_score is not None
            else float("inf")
        )
        scored.append((distance, str(path), path))
    if not scored:
        return None
    scored.sort(key=lambda item: (item[0], item[1]))
    return scored[0][2]


def relative_source(path: Path, outer_root: Path) -> str:
    try:
        return str(path.relative_to(outer_root))
    except ValueError:
        return path.name


def lineage_status(
    base_score: float | None,
    selected_seed: float | None,
    selected_best: float | None,
) -> str:
    if selected_best is None:
        return "no_executor_result"
    execution_gain = (
        selected_seed is not None and selected_best > selected_seed + EPS
    )
    inherited_gain = (
        base_score is not None
        and selected_seed is not None
        and selected_seed > base_score + EPS
    )
    if execution_gain and inherited_gain:
        return "inherited_stronger_seed_plus_executor_gain"
    if execution_gain:
        return "executor_gain_from_round_seed"
    if inherited_gain:
        return "inherited_seed_only_no_executor_gain"
    return "no_gain_over_round_seed"


def export_task(
    *,
    outer_root: Path,
    output_root: Path,
    task_id: str,
    title: str,
    source_rounds: list[int],
) -> dict[str, Any]:
    slug = TASK_SLUGS[task_id]
    destination = output_root / slug
    destination.mkdir(parents=True, exist_ok=False)
    exported_rounds: list[dict[str, Any]] = []

    for local_index, source_round in enumerate(source_rounds, start=1):
        round_root = outer_root / f"round{source_round}"
        summary_path = round_root / "round_summary.json"
        if not summary_path.is_file():
            exported_rounds.append(
                {
                    "local_round": local_index,
                    "source_round": source_round,
                    "status": "source_round_missing",
                }
            )
            continue

        summary = read_json(summary_path)
        group = task_group(summary, task_id)
        rows = sorted(group.get("rows", []), key=lambda row: int(row.get("k", 0)))
        entries = proposer_entries(round_root, task_id)
        round_destination = destination / f"round{local_index:02d}"
        round_destination.mkdir(parents=True)
        candidate_summaries: list[dict[str, Any]] = []

        for row in rows:
            k = int(row["k"])
            candidate_destination = round_destination / f"candidate{k + 1:02d}"
            candidate_destination.mkdir(parents=True)
            entry = entries.get(k)
            if entry is not None:
                trajectory = entry.get("trajectory")
                if isinstance(trajectory, list):
                    write_json(candidate_destination / "proposer_trajectory.json", trajectory)
                submission = entry.get("raw_submission")
                if isinstance(submission, str) and submission.strip():
                    write_text(candidate_destination / "proposer_submission.txt", submission)

            harness_source = round_root / "tasks" / task_id / f"cand{k:02d}"
            harness_files = copy_harness(
                harness_source, candidate_destination / "harness"
            )
            expected_score = finite_number(row.get("score"))
            rollout_paths = rollout_candidates(round_root, task_id, k)
            rollout_path = select_rollout(rollout_paths, expected_score)
            executor_trajectory_available = False
            executor_seed = None
            executor_best = None
            ledger: dict[str, Any] | None = None
            if rollout_path is not None:
                result = read_json(rollout_path)
                shutil.copy2(rollout_path, candidate_destination / "executor_result.json")
                executor_seed = finite_number(result.get("seed_score"))
                executor_best = finite_number(result.get("best_score"))
                ledger = result.get("ledger") if isinstance(result.get("ledger"), dict) else None
                program = result.get("best_program")
                if isinstance(program, str) and program.strip():
                    write_text(candidate_destination / "executor_program.py", program)
                executor_trajectory = result.get("trajectory")
                if isinstance(executor_trajectory, list):
                    write_json(
                        candidate_destination / "executor_trajectory.json",
                        executor_trajectory,
                    )
                    executor_trajectory_available = True

            candidate_summary = {
                "source_k": k,
                "valid": bool(row.get("valid", False)),
                "reported_score": expected_score,
                "reward": finite_number(row.get("reward")),
                "advantage": finite_number(row.get("advantage")),
                "changed_fields": row.get("changed_fields", []),
                "spec_hash": row.get("spec_hash", ""),
                "harness_files": harness_files,
                "executor_seed_score": executor_seed,
                "executor_best_score": executor_best,
                "executor_gain": (
                    executor_best - executor_seed
                    if executor_best is not None and executor_seed is not None
                    else None
                ),
                "executor_trajectory_available": executor_trajectory_available,
                "ledger": ledger,
                "selected_rollout_source": (
                    relative_source(rollout_path, outer_root)
                    if rollout_path is not None
                    else None
                ),
                "all_rollout_sources": [
                    relative_source(path, outer_root) for path in rollout_paths
                ],
            }
            write_json(candidate_destination / "candidate_summary.json", candidate_summary)
            candidate_summaries.append(candidate_summary)

        best_k = group.get("best_k")
        selected_by_k = {
            int(candidate["source_k"]): candidate for candidate in candidate_summaries
        }
        selected = selected_by_k.get(int(best_k)) if isinstance(best_k, int) else None
        base_score = finite_number(group.get("base_score"))
        selected_seed = selected.get("executor_seed_score") if selected else None
        selected_best = selected.get("executor_best_score") if selected else None
        round_record = {
            "local_round": local_index,
            "source_round": source_round,
            "status": "exported",
            "task_id": task_id,
            "base_score": base_score,
            "reported_best_k": best_k,
            "reported_best_score": finite_number(group.get("best_score")),
            "reported_improved": bool(group.get("improved", False)),
            "launched_candidates": len(rows),
            "selected_executor_seed_score": selected_seed,
            "selected_executor_best_score": selected_best,
            "selected_executor_gain": (
                selected_best - selected_seed
                if selected_best is not None and selected_seed is not None
                else None
            ),
            "lineage_status": lineage_status(base_score, selected_seed, selected_best),
            "executor_trajectories_retained": sum(
                int(row["executor_trajectory_available"])
                for row in candidate_summaries
            ),
            "source": {
                "round_summary": relative_source(summary_path, outer_root),
                "round_input": (
                    relative_source(round_root / "round.json", outer_root)
                    if (round_root / "round.json").is_file()
                    else None
                ),
                "proposer_trajectories": (
                    relative_source(round_root / "trajectories.json", outer_root)
                    if (round_root / "trajectories.json").is_file()
                    else None
                ),
            },
            "candidates": candidate_summaries,
        }
        write_json(round_destination / "round_summary.json", round_record)
        exported_rounds.append(round_record)

    evolution = {
        "schema": "sah-multitask-evolution/v1",
        "task_id": task_id,
        "title": title,
        "public_slug": slug,
        "source_kind": "legacy_production_rounds",
        "source_rounds": source_rounds,
        "evidence_boundary": {
            "proposer_trajectory": "exact when proposer_trajectory.json is present",
            "materialized_harness": "copied from the as-run candidate package",
            "executor_result": "exact selected result JSON",
            "executor_trajectory": (
                "present only when the source result retained a non-null trajectory; "
                "absence is missing evidence, not evidence of no tool call"
            ),
            "paired_control_program": "not retained by these legacy campaigns",
        },
        "rounds": exported_rounds,
    }
    write_json(destination / "evolution.json", evolution)

    table = [
        f"# {title}: proposer evolution process",
        "",
        "This directory mirrors the public `CP26/roundXX/candidateXX` layout.",
        "It contains exact proposer trajectories, proposer submissions, materialized",
        "harness packages, executor results, and best programs retained by the legacy",
        "production series. Source-round gaps can mark distinct campaign segments or",
        "proposer checkpoints; local round order follows the paper curve and must not be",
        "assumed to be a single uninterrupted program lineage.",
        "",
        "## Evidence boundary",
        "",
        "Historical production results usually saved `trajectory: null` for the executor.",
        "Accordingly, `executor_trajectory.json` is included only when the source really",
        "contains it. Its absence must not be interpreted as proof that a mounted tool was",
        "or was not called. `executor_result.json` remains the exact source artifact.",
        "",
        "A reported round gain is also separated from an inherited stronger seed. The",
        "`lineage_status` column prevents an imported program from being presented as a",
        "within-round executor discovery.",
        "",
        "## Round index",
        "",
        "| Local | Source | Candidates | Base | Selected seed | Selected best | Executor gain | Lineage status |",
        "|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in exported_rounds:
        if row.get("status") != "exported":
            table.append(
                f"| {row['local_round']} | {row['source_round']} | — | — | — | — | — | {row['status']} |"
            )
            continue

        def show(value: Any) -> str:
            number = finite_number(value)
            return f"{number:.9g}" if number is not None else "—"

        table.append(
            "| {local} | {source} | {count} | {base} | {seed} | {best} | {gain} | `{status}` |".format(
                local=row["local_round"],
                source=row["source_round"],
                count=row["launched_candidates"],
                base=show(row["base_score"]),
                seed=show(row["selected_executor_seed_score"]),
                best=show(row["selected_executor_best_score"]),
                gain=show(row["selected_executor_gain"]),
                status=row["lineage_status"],
            )
        )
    write_text(destination / "README.md", "\n".join(table))
    return evolution


def write_sha256sums(root: Path, destination: Path) -> None:
    lines: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == destination:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root)}")
    write_text(destination, "\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outer-root", type=Path, required=True)
    parser.add_argument("--curve-data", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--tasks",
        nargs="*",
        default=list(TASK_SLUGS),
        choices=sorted(TASK_SLUGS),
    )
    args = parser.parse_args()
    curve_data = read_json(args.curve_data)
    args.output_root.mkdir(parents=True, exist_ok=True)
    exported: list[dict[str, Any]] = []
    for task_id in args.tasks:
        task = curve_data["tasks"][task_id]
        source_rounds = [
            int(row["round"])
            for row in task["series"]["proposer_full"]
            if row.get("round") is not None
        ]
        exported.append(
            export_task(
                outer_root=args.outer_root,
                output_root=args.output_root,
                task_id=task_id,
                title=task["title"],
                source_rounds=source_rounds,
            )
        )

    overview = [
        "# Multi-task proposer evolution artifacts",
        "",
        "The task directories follow the same `roundXX/candidateXX` organization as",
        "the fully traced CP26 release. See each task README for the legacy evidence",
        "boundary and lineage audit.",
        "",
        "| Directory | Task | Source rounds | Candidate packages | Full executor trajectories |",
        "|---|---|---:|---:|---:|",
    ]
    for task in exported:
        rounds = [row for row in task["rounds"] if row.get("status") == "exported"]
        overview.append(
            "| [{slug}]({slug}/) | {title} | {rounds} | {candidates} | {trajectories} |".format(
                slug=task["public_slug"],
                title=task["title"],
                rounds=len(rounds),
                candidates=sum(row["launched_candidates"] for row in rounds),
                trajectories=sum(row["executor_trajectories_retained"] for row in rounds),
            )
        )
    overview.extend(
        [
            "",
            "The existing `CP26/` directory is a newer fully traced campaign and retains",
            "complete executor trajectories. The exported legacy tasks do not manufacture",
            "those missing conversations.",
        ]
    )
    write_text(args.output_root / "EVOLUTION_ARTIFACTS.md", "\n".join(overview))
    write_sha256sums(args.output_root, args.output_root / "EVOLUTION_SHA256SUMS")


if __name__ == "__main__":
    main()
