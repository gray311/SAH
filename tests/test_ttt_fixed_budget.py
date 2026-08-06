import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import ttt_discover_prepare as prepare


TASK = "eft__math__hadamard_maximal_det"


def write_rollout(root: Path, k: int, score: float) -> None:
    path = root / f"k{k}" / "run" / "summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([{
        "task_id": TASK,
        "best_score": score,
        "best_program": f"program-{k}",
        "evaluations": 20,
    }]))


class FixedBudgetPrepareTest(unittest.TestCase):
    def run_prepare(self, round_dir: Path, state_dir: Path) -> None:
        argv = [
            "ttt_discover_prepare.py",
            "--task", TASK,
            "--round-dir", str(round_dir),
            "--state-dir", str(state_dir),
            "--step", "0",
            "--launched", "16",
            "--checkpoint", "/base",
            "--parent-id", "root",
            "--max-train-rows", "16",
            "--min-train-rows", "8",
        ]
        with patch.object(sys, "argv", argv), redirect_stdout(StringIO()):
            prepare.main()

    def test_zero_usable_rows_still_records_charged_curve_point(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.run_prepare(root / "round", root / "state")
            curve = json.loads((root / "state" / "curve.jsonl").read_text())
            manifest = json.loads((root / "state" / "prepare_step00.json").read_text())
            self.assertEqual(curve["launched"], 16)
            self.assertEqual(curve["usable"], 0)
            self.assertFalse(manifest["update_eligible"])
            self.assertIsNone(manifest["replay"])
            self.assertFalse((root / "state" / "replay_step01.jsonl").exists())

    def test_four_usable_rows_are_retained_but_do_not_trigger_update(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            round_dir = root / "round"
            for k in range(4):
                write_rollout(round_dir, k, 0.2 + 0.01 * k)
            self.run_prepare(round_dir, root / "state")
            state = json.loads((root / "state" / "state.json").read_text())
            manifest = json.loads((root / "state" / "prepare_step00.json").read_text())
            self.assertEqual(state["batches"][0]["usable"], 4)
            self.assertEqual(state["batches"][0]["train_rows"], 0)
            self.assertFalse(manifest["update_eligible"])


if __name__ == "__main__":
    unittest.main()
