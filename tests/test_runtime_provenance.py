from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.runtime_provenance import RUNTIME_SCRIPTS, snapshot, verify


REPO = Path(__file__).resolve().parents[1]


class RuntimeProvenanceTest(unittest.TestCase):
    def test_snapshot_verifies_live_and_immutable_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "runtime.json"
            frozen = root / "snapshot"
            payload = snapshot(REPO, manifest, frozen)
            self.assertGreater(payload["file_count"], 0)
            self.assertEqual(verify(manifest)["status"], "verified")

            copied = frozen / "scripts" / "runtime_provenance.py"
            copied.write_text(copied.read_text() + "\n# tampered\n")
            with self.assertRaisesRegex(SystemExit, "immutable snapshot bytes changed"):
                verify(manifest)

    def test_plotting_scripts_are_not_runtime_inputs(self) -> None:
        self.assertNotIn("plot_reward_route_inference16.py", RUNTIME_SCRIPTS)
        self.assertNotIn("build_reward_route_inference16_effects.py", RUNTIME_SCRIPTS)


if __name__ == "__main__":
    unittest.main()
