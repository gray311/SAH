import json
import unittest
from pathlib import Path

from scripts.plot_reward_route_inference16 import FINAL_X, ROUNDS, expected_x
from scripts.audit_reward_route_inference16 import audit_static_configuration
from src.outer.trajectory_budget import build_h2_slot_plan


REPO = Path(__file__).resolve().parents[1]


class Inference16ProtocolTest(unittest.TestCase):
    def setUp(self):
        self.meta = {
            "k": 2,
            "tasks_order": ["task"],
            "per_task": {
                "task": {
                    "base_package": "/incumbent/h2",
                    "candidates": [
                        {"k": 0, "valid": True, "dir": "/candidate/h2-0"},
                        {"k": 1, "valid": False},
                    ],
                }
            },
        }

    def test_fixed_budget_has_one_real_h2_slot_per_h1_slot(self):
        plan = build_h2_slot_plan(self.meta, fixed_slots=True)
        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]["h2_slot_mode"], "candidate_harness")
        self.assertEqual(plan[0]["h2_harness_dir"], "/candidate/h2-0")
        self.assertTrue(plan[0]["eligible_for_h1_reward"])
        self.assertEqual(plan[1]["h2_slot_mode"], "incumbent_fallback")
        self.assertEqual(plan[1]["h2_harness_dir"], "/incumbent/h2")
        self.assertFalse(plan[1]["eligible_for_h1_reward"])

    def test_legacy_budget_still_skips_invalid_h1_candidates(self):
        plan = build_h2_slot_plan(self.meta, fixed_slots=False)
        self.assertEqual([row["k"] for row in plan], [0])

    def test_fixed_budget_rejects_missing_h1_slots(self):
        self.meta["k"] = 3
        with self.assertRaisesRegex(ValueError, "expected K=3"):
            build_h2_slot_plan(self.meta, fixed_slots=True)

    def test_curve_grid_is_shared_x_1_to_305(self):
        xs = [1] + [expected_x(index) for index in range(ROUNDS)]
        self.assertEqual(xs[:4], [1, 17, 33, 49])
        self.assertEqual(xs[-1], FINAL_X)
        self.assertEqual(FINAL_X, 305)

    def test_all_four_human_references_are_frozen(self):
        refs = json.loads(
            (REPO / "results" / "human_best_references.json").read_text()
        )["tasks"]
        selected = {
            "eft__math__erdos_min_overlap",
            "eft__math__second_autocorr_ineq",
            "eft__math__hadamard_maximal_det",
            "adrs__eplb",
        }
        self.assertTrue(selected.issubset(refs))

    def test_run_drivers_require_explicit_confirmation(self):
        for name in (
            "drive_reward_route_inference16_h1.sh",
            "drive_reward_route_inference16_executor.sh",
        ):
            source = (REPO / "scripts" / name).read_text()
            self.assertIn('RR_RUN_CONFIRMED:-NO', source)
            self.assertIn('= YES', source)

    def test_static_configuration_audit(self):
        audited = audit_static_configuration(REPO)
        self.assertEqual(audited["status"], "configured_not_run")
        self.assertEqual(audited["common_final_x"], 305)


if __name__ == "__main__":
    unittest.main()
