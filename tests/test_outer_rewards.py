import json
import tempfile
import unittest
from pathlib import Path

from outer.rewards import load_rollout_score


TASK = "example__task"


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


class LoadRolloutScoreTest(unittest.TestCase):
    def test_terminal_failure_does_not_inherit_seed_checkpoint(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run = root / "run0"
            write_json(run / "checkpoints" / f"{TASK}.json", {
                "task_id": TASK,
                "best_score": 7.5,
            })
            write_json(run / "summary.json", [{
                "task_id": TASK,
                "best_score": None,
                "best_program": None,
                "error": "ConfigError: invalid candidate harness",
            }])

            self.assertIsNone(load_rollout_score(root, TASK))

    def test_checkpoint_is_allowed_when_terminal_row_never_materialized(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_json(root / "run0" / "checkpoints" / f"{TASK}.json", {
                "task_id": TASK,
                "best_score": 7.5,
            })

            self.assertEqual(load_rollout_score(root, TASK), 7.5)

    def test_terminal_scores_remain_best_across_multiple_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_json(root / "run0" / "summary.json", {
                "task_id": TASK,
                "best_score": 6.0,
            })
            write_json(root / "run1" / "summary.json", [{
                "task_id": TASK,
                "best_score": 8.0,
            }])

            self.assertEqual(load_rollout_score(root, TASK), 8.0)

    def test_middleware_ineligible_score_is_never_rewarded(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_json(root / "run0" / "summary.json", [{
                "task_id": TASK,
                "best_score": 9.0,
                "score_eligible": False,
                "error": "MiddlewareParticipationError: hook not mounted",
            }])
            write_json(root / "run0" / "checkpoints" / f"{TASK}.json", {
                "task_id": TASK,
                "best_score": 9.0,
            })

            self.assertIsNone(load_rollout_score(root, TASK))


if __name__ == "__main__":
    unittest.main()
