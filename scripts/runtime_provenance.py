#!/usr/bin/env python3
"""Snapshot and fail-closed verify the source used by long-running campaigns."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Iterable


SRC_SUFFIXES = {".py", ".yaml", ".yml"}
# Root-level prose is deliberately excluded.  It can explain a frozen run but
# cannot change its execution, and editing paper/protocol text while a campaign
# is live must not invalidate the byte-level runtime lineage.
ROOT_FILES: set[str] = set()

# Only code that can change search, evaluation, credit, or training belongs in
# the runtime bundle.  Plot/case-study/report scripts are deliberately absent:
# editing a figure while a two-week campaign is running must not invalidate an
# otherwise byte-identical scientific lineage.
RUNTIME_SCRIPTS = {
    "_outer_round_worker.sh",
    "audit_trajectories.py",
    "capture_shared_anchor.py",
    "collect_ttt_eval_manifest.py",
    "context_ablation.sh",
    "drive_reward_route_inference16_executor.sh",
    "drive_reward_route_inference16_h1.sh",
    "drive_ttt_executor_12h.sh",
    "fresh_campaign.sh",
    "hash_h2_package.py",
    "outer_round.sbatch",
    "reward_route_inference16_config.sh",
    "runtime_provenance.py",
    "sanitize_grpo_batch.py",
    "submit_ttt_executor_update.sh",
    "train_mphi_step.sh",
    "ttt_discover_prepare.py",
    "ttt_executor_eval.sbatch",
}


def _selected(repo: Path) -> Iterable[Path]:
    src = repo / "src"
    for path in sorted(src.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        # Markdown is executable configuration only inside an H1/H2 harness
        # (system prompts and skills), not in src-level documentation.
        is_harness_markdown = path.suffix == ".md" and "harness" in path.parts
        if path.suffix in SRC_SUFFIXES or is_harness_markdown:
            yield path
    for name in sorted(RUNTIME_SCRIPTS):
        path = repo / "scripts" / name
        if not path.is_file():
            raise FileNotFoundError(f"runtime source is missing: {path}")
        yield path
    for name in sorted(ROOT_FILES):
        path = repo / name
        if path.is_file():
            yield path
    for rel in (
        "results/baseline_h2_20ev.json",
        "results/baseline_h2_20ev_program_index.json",
        "results/human_best_references.json",
    ):
        path = repo / rel
        if path.is_file():
            yield path


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory(repo: Path) -> list[dict]:
    rows = []
    for path in _selected(repo):
        rel = path.relative_to(repo).as_posix()
        rows.append({"path": rel, "sha256": _sha(path), "bytes": path.stat().st_size})
    return rows


def _bundle(rows: list[dict]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(row["path"].encode() + b"\0" + row["sha256"].encode() + b"\n")
    return digest.hexdigest()


def snapshot(repo: Path, manifest: Path, snapshot_dir: Path) -> dict:
    repo = repo.resolve()
    rows = _inventory(repo)
    snapshot_dir = snapshot_dir.resolve()
    snapshot_dir.parent.mkdir(parents=True, exist_ok=True)
    if snapshot_dir.exists():
        # Crash recovery: the directory rename may have completed just before
        # the manifest write.  Reuse it only when every byte is identical.
        copied = _inventory(snapshot_dir)
        if copied != rows:
            raise FileExistsError(
                f"different immutable source snapshot already exists: {snapshot_dir}"
            )
    else:
        staging_parent = Path(tempfile.mkdtemp(
            prefix=f".{snapshot_dir.name}.staging-", dir=snapshot_dir.parent
        ))
        staging = staging_parent / "snapshot"
        try:
            for row in rows:
                source = repo / row["path"]
                target = staging / row["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            copied = _inventory(staging)
            if copied != rows:
                raise RuntimeError("source snapshot copy failed content verification")
            os.replace(staging, snapshot_dir)
        finally:
            shutil.rmtree(staging_parent, ignore_errors=True)
    payload = {
        "schema": "runtime-source/1.0",
        "repo": str(repo),
        "bundle_sha256": _bundle(rows),
        "file_count": len(rows),
        "files": rows,
        "snapshot_dir": str(snapshot_dir.resolve()),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    tmp = manifest.with_suffix(manifest.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    os.replace(tmp, manifest)
    return payload


def verify(manifest: Path) -> dict:
    payload = json.loads(manifest.read_text())
    repo = Path(payload["repo"]).resolve()
    expected = payload["files"]
    actual = _inventory(repo)
    errors = []
    expected_paths = [row["path"] for row in expected]
    actual_paths = [row["path"] for row in actual]
    if actual_paths != expected_paths:
        errors.append("selected source-file set changed")
    expected_by_path = {row["path"]: row for row in expected}
    for row in actual:
        old = expected_by_path.get(row["path"])
        if old is not None and row["sha256"] != old["sha256"]:
            errors.append(f"changed: {row['path']}")
    if _bundle(actual) != payload.get("bundle_sha256"):
        errors.append("bundle digest changed")
    snapshot_dir = Path(payload["snapshot_dir"]).resolve()
    if not snapshot_dir.is_dir():
        errors.append("immutable snapshot directory is missing")
    else:
        snap = _inventory(snapshot_dir)
        if snap != expected or _bundle(snap) != payload.get("bundle_sha256"):
            errors.append("immutable snapshot bytes changed")
    if errors:
        raise SystemExit(
            "runtime source verification failed for " + str(manifest) + ": "
            + "; ".join(errors[:20])
        )
    return {
        "status": "verified",
        "manifest": str(manifest.resolve()),
        "bundle_sha256": payload["bundle_sha256"],
        "file_count": len(actual),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("snapshot")
    create.add_argument("--repo", type=Path, required=True)
    create.add_argument("--manifest", type=Path, required=True)
    create.add_argument("--snapshot-dir", type=Path, required=True)
    check = sub.add_parser("verify")
    check.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    result = (
        snapshot(args.repo, args.manifest, args.snapshot_dir)
        if args.command == "snapshot" else verify(args.manifest)
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
