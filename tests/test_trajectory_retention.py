from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inner.harness_runner import InnerResult, _is_score_eligible  # noqa: E402
from inner.run_baseline import _agent_run, _has_executor_trajectory  # noqa: E402
from scripts.audit_trajectories import _has_assistant_turn  # noqa: E402


def test_executor_trajectory_requires_an_assistant_turn() -> None:
    cases = [
        (None, False),
        ([], False),
        ([{"role": "user", "content": "task"}], False),
        ([{"role": "assistant", "content": "answer"}], True),
        ([{"role": "MessageRole.ASSISTANT", "tool_calls": []}], True),
    ]
    for trajectory, expected in cases:
        assert _has_executor_trajectory(trajectory) is expected
        assert _has_assistant_turn(trajectory) is expected


def test_harness_error_is_never_score_eligible() -> None:
    assert not _is_score_eligible("harness_error", [])
    assert not _is_score_eligible("completed", ["generated middleware not invoked"])
    assert _is_score_eligible("completed", [])


def test_required_missing_trajectory_is_retained_but_not_published() -> None:
    result = InnerResult(
        task_id="task", source="test", best_score=2.0, seed_score=1.0,
        best_metrics={}, best_program="candidate", stop_reason="completed",
        ledger={"evaluator_calls": 1}, trajectory=None, score_eligible=True,
    )
    args = SimpleNamespace(
        model="model", base_url="http://unused", api_key="EMPTY",
        temperature=0.7, top_p=0.95, max_tokens=10, llm_timeout=1,
        thinking=False, seed=7, max_iters=1, harness_dir=None, max_evals=1,
        eval_timeout=1, eval_python="python3", no_trajectory=False,
        require_trajectory=True,
    )
    task = SimpleNamespace(
        task_id="task", source="test", initial_program="seed",
        _seed_program_provenance={"mode": "task_initial"},
    )
    with tempfile.TemporaryDirectory() as temp, patch(
        "inner.harness_runner.run_task", return_value=result,
    ):
        published = _agent_run(task, args, Path(temp))
    assert published["best_score"] is None
    assert published["delta"] is None
    assert published["_full"]["best_score"] == 2.0
    assert published["_full"]["score_eligible"] is False
    assert published["stop_reason"] == "trajectory_missing"


class TrajectoryRetentionTest(unittest.TestCase):
    # Keep the module-level functions usable by pytest while making the same
    # contract visible to the repository's canonical unittest invocation.
    def test_assistant_turn_contract(self) -> None:
        test_executor_trajectory_requires_an_assistant_turn()

    def test_harness_error_contract(self) -> None:
        test_harness_error_is_never_score_eligible()

    def test_missing_trajectory_contract(self) -> None:
        test_required_missing_trajectory_is_retained_but_not_published()


if __name__ == "__main__":
    unittest.main()
