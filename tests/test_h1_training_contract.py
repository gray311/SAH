from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from training.grpo_to_replay import _h1_tool_schemas  # noqa: E402


class H1TrainingContractTest(unittest.TestCase):
    def test_training_tools_are_exactly_the_inference_mounts(self) -> None:
        names = [row["function"]["name"] for row in _h1_tool_schemas()]
        self.assertEqual(names, [
            "harness_shell", "write_harness_file", "edit_harness_file",
            "delete_harness_file", "validate_harness", "submit_harness",
        ])
        self.assertNotIn("submit_spec", names)
        self.assertNotIn("validate_spec", names)


if __name__ == "__main__":
    unittest.main()
