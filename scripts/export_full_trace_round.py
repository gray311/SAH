#!/usr/bin/env python3
"""Export a fully traced proposer/executor round in the public CP26 layout.

The input is an inspection bundle whose candidates retain files 01--08.  The
export keeps those lossless records, adds the familiar concise aliases, and
materializes the generated harness package so readers can inspect what the
executor actually received.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path, PurePosixPath


ALIASES = {
    "01_proposer_exact_input.json": "proposer_input.json",
    "02_proposer_full_trajectory.json": "proposer_trajectory.json",
    "03_proposer_raw_submission.txt": "proposer_submission.txt",
    "05_executor_exact_input.json": "executor_input.json",
    "06_executor_full_trajectory.json": "executor_trajectory.json",
    "07_executor_reward.json": "executor_result.json",
    "08_executor_output_program.py": "executor_program.py",
}
PUBLIC_HARNESS_EXCLUDES = {
    "component_manifest.json",
    "smoke_test.json",
    "meta.json",
    "REFERENCE_CARD.md",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def safe_harness_path(raw: str) -> Path:
    posix = PurePosixPath(raw)
    if posix.is_absolute() or ".." in posix.parts or not posix.parts:
        raise ValueError(f"unsafe generated harness path: {raw!r}")
    return Path(*posix.parts)


def materialize_harness(source: Path, destination: Path) -> list[dict]:
    payload = load_json(source)
    manifest: list[dict] = []
    for row in payload.get("files", []):
        relative = safe_harness_path(str(row["path"]))
        if relative.name in PUBLIC_HARNESS_EXCLUDES:
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        content = row.get("content", "")
        if row.get("encoding", "utf-8") != "utf-8":
            raise ValueError(f"unsupported generated harness encoding: {row}")
        target.write_text(content, encoding="utf-8")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        expected = row.get("sha256")
        if expected and digest != expected:
            raise ValueError(f"content hash mismatch for {relative}")
        manifest.append(
            {"path": relative.as_posix(), "bytes": target.stat().st_size, "sha256": digest}
        )
    return manifest


def export(source: Path, destination: Path, source_label: str) -> None:
    candidates_root = source / "candidates"
    source_candidates = sorted(path for path in candidates_root.glob("cand*") if path.is_dir())
    if not source_candidates:
        raise FileNotFoundError(f"no candidates beneath {candidates_root}")

    destination.mkdir(parents=True, exist_ok=False)
    round_dir = destination / "round01"
    round_dir.mkdir()
    outcomes: list[dict] = []

    for index, candidate in enumerate(source_candidates, start=1):
        target = round_dir / f"candidate{index:02d}"
        target.mkdir()
        for source_name, alias in ALIASES.items():
            source_file = candidate / source_name
            if not source_file.is_file():
                raise FileNotFoundError(source_file)
            shutil.copy2(source_file, target / alias)

        generated_harness = candidate / "04_generated_harness.json"
        shutil.copy2(generated_harness, target / "generated_harness.json")
        harness_manifest = materialize_harness(generated_harness, target / "harness")

        reward = load_json(candidate / "07_executor_reward.json")
        summary = {
            "candidate": index,
            "source_candidate": candidate.name,
            "task_id": reward.get("task_id"),
            "seed_score": reward.get("seed_score"),
            "best_score": reward.get("best_score"),
            "score_eligible": reward.get("score_eligible"),
            "stop_reason": reward.get("stop_reason"),
            "error": reward.get("error"),
            "ledger": reward.get("ledger"),
            "middleware_audit": reward.get("middleware_audit"),
            "tool_audit": reward.get("tool_audit"),
            "skill_audit": reward.get("skill_audit"),
            "harness_files": harness_manifest,
            "full_proposer_trajectory": True,
            "full_executor_trajectory": True,
        }
        dump_json(target / "candidate_summary.json", summary)
        outcomes.append(summary)

    selected = max(
        outcomes,
        key=lambda row: float("-inf") if row["best_score"] is None else float(row["best_score"]),
    )
    round_summary = {
        "schema_version": 1,
        "source_bundle": source_label,
        "task_id": selected["task_id"],
        "candidate_count": len(outcomes),
        "selected_candidate": selected["candidate"],
        "selected_best_score": selected["best_score"],
        "full_proposer_trajectories": len(outcomes),
        "full_executor_trajectories": len(outcomes),
        "candidates": outcomes,
    }
    dump_json(round_dir / "round_summary.json", round_summary)
    dump_json(destination / "evolution.json", {"schema_version": 1, "rounds": [round_summary]})

    destination.joinpath("README.md").write_text(
        "# Autocorrelation II: repaired fully traced round\n\n"
        "This is a post-fix AC2 round exported in the same "
        "`roundXX/candidateXX` organization as CP26. It is separate from the "
        "historical multi-round curve in `../AC2/`: every candidate here retains "
        "the complete proposer and executor message trajectories.\n\n"
        "Each candidate contains exact proposer/executor inputs, trajectories, "
        "the proposer submission, the generated harness JSON, a materialized "
        "`harness/` package, the exact executor result, and its output program. "
        "Runtime component audits in `executor_result.json` are the source of "
        "truth for enactment; component names alone are not evidence of use.\n\n"
        f"- Candidates: {len(outcomes)}\n"
        f"- Selected candidate: candidate{selected['candidate']:02d}\n"
        f"- Selected best score: {selected['best_score']:.12g}\n"
        "- Full proposer trajectories: 8/8\n"
        "- Full executor trajectories: 8/8\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--source-label",
        default="results/debug-evolve-qwen35-6186121/ac2_round001",
    )
    args = parser.parse_args()
    export(args.source.resolve(), args.output.resolve(), args.source_label)


if __name__ == "__main__":
    main()
