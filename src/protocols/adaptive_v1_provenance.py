"""Source provenance for the Adaptive-only orchestration/runtime boundary."""
from __future__ import annotations

import hashlib
from pathlib import Path

RUNTIME_VERSION = "adaptive-runtime/1.2-process-group-cleanup"


def runtime_package_hash() -> str:
    """Hash every opt-in integration file that executes an Adaptive round."""
    repo = Path(__file__).resolve().parents[2]
    relative_paths = (
        "scripts/_outer_round_worker.sh",
        "scripts/train_mphi_step.sh",
        "scripts/unified_campaign.sh",
        "src/inner/eft_task.py",
        "src/inner/eval_runner.py",
        "src/inner/_eval_worker.py",
        "src/inner/harness_runner.py",
        "src/inner/harness_sdk.py",
        "src/inner/program_edit.py",
        "src/inner/run_baseline.py",
        "src/inner/session.py",
        "src/outer/materialize.py",
        "src/outer/outer_round.py",
        "src/protocols/adaptive_v1.py",
        "src/protocols/adaptive_v1_provenance.py",
        "src/training/grpo_to_replay.py",
    )
    hasher = hashlib.sha256()
    for relative in relative_paths:
        path = repo / relative
        hasher.update(relative.encode())
        hasher.update(path.read_bytes())
    for root_relative in ("src/inner/harness",):
        root = repo / root_relative
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = str(path.relative_to(repo))
            hasher.update(relative.encode())
            hasher.update(path.read_bytes())
    return "sha256:" + hasher.hexdigest()[:16]
