from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.capture_shared_anchor import main


class SharedAnchorCaptureTest(unittest.TestCase):
    def test_resume_is_idempotent_but_score_or_program_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task, program = "task", "print('anchor')"
            source = root / "summary.json"
            source.write_text(json.dumps([{
                "task_id": task, "best_program": program, "best_score": 1.0,
            }]))
            index = root / "index.json"

            def write_index(score: float) -> None:
                index.write_text(json.dumps({"tasks": {task: {
                    "source_summary": str(source), "score": score,
                    "program_sha256": hashlib.sha256(program.encode()).hexdigest(),
                }}}))

            def capture() -> None:
                argv = [
                    "capture_shared_anchor.py", "--index", str(index),
                    "--task", task, "--out-dir", str(root / "capture"),
                ]
                with patch.object(sys, "argv", argv), redirect_stdout(StringIO()):
                    main()

            write_index(1.0)
            capture()
            capture()
            manifest = json.loads((root / "capture" / "manifest.json").read_text())
            self.assertEqual(manifest["tasks"][task]["score"], 1.0)

            source.write_text(json.dumps([{
                "task_id": task, "best_program": program, "best_score": 2.0,
            }]))
            write_index(2.0)
            with self.assertRaisesRegex(SystemExit, "refusing to mutate"):
                capture()


if __name__ == "__main__":
    unittest.main()
