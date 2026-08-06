from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.collect_ttt_eval_manifest import harness_hash
from scripts.hash_h2_package import h2_sha256


REPO = Path(__file__).resolve().parents[1]


class H2HashContractTest(unittest.TestCase):
    def test_executor_manifest_uses_canonical_h2_hash(self) -> None:
        expected = h2_sha256(REPO / "src" / "inner" / "harness")
        self.assertEqual(harness_hash(), expected)
        worker = (REPO / "scripts" / "ttt_executor_eval.sbatch").read_text()
        self.assertIn("from inner.package_hash import h2_sha256", worker)

    def test_hash_is_path_independent_and_content_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            left, right = root / "left", root / "right"
            for package in (left, right):
                (package / "tools").mkdir(parents=True)
                (package / "agent.yaml").write_text("name: h2\n")
                (package / "tools" / "x.py").write_text("VALUE = 1\n")
            self.assertEqual(h2_sha256(left), h2_sha256(right))
            (right / "tools" / "x.py").write_text("VALUE = 2\n")
            self.assertNotEqual(h2_sha256(left), h2_sha256(right))


if __name__ == "__main__":
    unittest.main()
