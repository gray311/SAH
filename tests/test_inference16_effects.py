import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_reward_route_inference16_effects import (
    executor_batch,
    h1_batch,
)


TASK = "eft__math__hadamard_maximal_det"


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


class Inference16EffectLedgerTest(unittest.TestCase):
    def test_h1_batch_binds_exact_fixed_slot_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rd = (
                root / "runs" / "self_adapt_harness"
                / "outer-reward-route-inference16-v1-proposer-hadamard"
                / "round2200"
            )
            candidates = [{
                "k": k,
                "valid": True,
                "llm_calls": 2,
                "review_log": [],
            } for k in range(8)]
            dump(rd / "round.json", {
                "proposer": {"checkpoint": "/base", "executor_checkpoint": "/base"},
                "program_ratchet_mode": "strict_single",
                "inference_trajectory_budget": {
                    "axis_unit": "generated_agent_trajectory",
                    "fixed_h1_plus_h2_slots": True,
                    "logical_round_index": 0,
                    "h1_slots_per_task": 8,
                    "h2_slots_per_task": 8,
                    "axis_x_after_round": 17,
                },
                "per_task": {TASK: {
                    "analysis": {"enabled": False, "model_calls": 0},
                    "candidates": candidates,
                }},
            })
            dump(rd / "round_summary.json", {"groups": {TASK: {
                "best_score": 0.25, "improved": True,
                "accepted_improvement": True,
            }}})
            dump(rd / "next_bases.json", {TASK: {"score": 0.25}})
            dump(rd / "h2_slot_plan.json", {"slots": [{
                "h2_slot_mode": "candidate_harness",
            } for _ in range(8)]})
            dump(rd / "trajectories.json", [{"task_id": TASK, "k": k} for k in range(8)])
            dump(rd / "prompts.json", {TASK: "fixed prompt"})
            dump(rd / "seed_programs_in.json", {TASK: {
                "program": "initial", "score": 0.143,
            }})
            dump(rd / "program_ratchet_audit.json", {
                "schema": "program-ratchet/1.0",
                "mode": "strict_single",
                "tasks": {TASK: {
                    "promoted": True,
                    "reason": "strict_improvement",
                }},
            })
            for k in range(8):
                dump(rd / "rollouts" / TASK / f"cand{k:02d}" / "run" / "summary.json", [{
                    "task_id": TASK,
                    "best_score": 0.2 + 0.01 * k,
                    "best_program": f"program-{k}",
                    "evaluations": 20,
                    "seed_program_provenance": {
                        "mode": "task_initial", "program_sha256": "a" * 64,
                    },
                    "h2_package_provenance": {
                        "hash_scheme": "canonical-h2-v1", "sha256": "b" * 64,
                    },
                }])

            row = h1_batch(
                run_root=root / "runs",
                model_root=root / "models",
                method="proposer",
                tag="hadamard",
                task=TASK,
                round_base=2200,
                index=0,
                score_before=0.143,
            )
            self.assertIsNotNone(row)
            assert row is not None
            self.assertEqual((row["h1_trajectories"], row["h2_trajectories"]), (8, 8))
            self.assertEqual(row["x_after"], 17)
            self.assertEqual(row["rollout"]["terminal_summaries"], 8)
            self.assertEqual(row["rollout"]["evaluator_calls"], 160)
            self.assertIsNotNone(row["trajectory_bundle"]["sha256"])

    def test_executor_low_usable_batch_is_a_point_not_a_missing_batch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sd = root / "runs" / "self_adapt_harness" / "reward-route-inference16-v1" / "executor" / "hadamard"
            eval_dir = sd / "eval_rri16e_u0"
            dump(eval_dir / "eval_manifest.json", {
                "usable": 4, "evaluator_calls": 60, "batch_best": 0.2,
            })
            dump(sd / "prepare_step00.json", {
                "update_eligible": False,
                "update_skip_reason": "usable_rows_4_below_min_train_rows_8",
            })
            row = executor_batch(
                run_root=root / "runs",
                tag="hadamard",
                task=TASK,
                index=0,
                row={
                    "step": 0, "launched": 16, "usable": 4,
                    "best": 0.2, "batch_best": 0.2, "checkpoint": "/base",
                },
                next_row={
                    "step": 1, "launched": 16, "usable": 12,
                    "best": 0.21, "batch_best": 0.21, "checkpoint": "/base",
                },
            )
            self.assertEqual(row["h2_trajectories"], 16)
            self.assertFalse(row["outgoing_update"]["eligible"])
            self.assertFalse(row["outgoing_update"]["applied"])


if __name__ == "__main__":
    unittest.main()
