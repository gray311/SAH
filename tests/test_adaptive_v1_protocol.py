from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from outer.materialize import materialize  # noqa: E402
from outer import outer_round  # noqa: E402
from protocols import adaptive_v1 as adaptive  # noqa: E402
from training.grpo_to_replay import convert_row  # noqa: E402


class AdaptiveProposalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base, self.view = adaptive.read_adaptive_base(
            REPO / "src" / "inner" / "harness"
        )

    def test_frozen_system_prompt_matches_adaptive_v1(self) -> None:
        self.assertEqual(
            hashlib.sha256(adaptive.PROPOSER_SYSTEM_PROMPT.encode()).hexdigest(),
            "02ef7c5aff2eba3d5e522ee96c48e9e7e1b1b855d5c0091455c7d2855f5f4013",
        )
        self.assertIn("Produce exactly one sparse", adaptive.PROPOSER_SYSTEM_PROMPT)
        self.assertIn("mean_learning_reward", adaptive.PROPOSER_SYSTEM_PROMPT)

    def test_sequential_samples_see_prior_valid_actions(self) -> None:
        responses = iter(
            [
                json.dumps(
                    {
                        "axis": "prompt",
                        "hypothesis": "restore the best valid program after regression",
                        "edit_atoms": [
                            {
                                "kind": "prompt_upsert_section",
                                "field": "best-valid-recovery",
                                "value": (
                                    "After any regression, restore the best "
                                    "verifier-valid program before continuing."
                                ),
                            }
                        ],
                    }
                ),
                json.dumps(
                    {
                        "axis": "search",
                        "hypothesis": "reduce sampling noise independently",
                        "edit_atoms": [
                            {
                                "kind": "set",
                                "field": "/llm/temperature",
                                "value": 0.2,
                            }
                        ],
                    }
                ),
            ]
        )
        calls = []

        def generate(system, user, generation):
            calls.append((system, user, dict(generation)))
            return next(responses), {"total_tokens": 10}

        records = adaptive.propose_group(
            count=2,
            round_index=2,
            base_seed=23,
            base_spec=self.base,
            base_view=self.view,
            base_user_context='{"round_index": 2}',
            known_evidence_ids=[],
            generate=generate,
        )
        self.assertTrue(all(record.valid for record in records))
        self.assertIn('"prior_valid_actions": []', calls[0][1])
        self.assertIn("restore the best valid program", calls[1][1])
        self.assertIn("best-valid-recovery", calls[1][1])
        self.assertEqual([call[2]["seed"] for call in calls], [2023, 2024])
        self.assertNotIn("proposal_id", json.loads(records[0].training_response))
        self.assertEqual(
            json.loads(records[0].training_response)["axis"], "prompt"
        )

    def test_compiler_rejection_keeps_action_and_trace_for_negative_credit(
        self,
    ) -> None:
        response = json.dumps(
            {
                "axis": "context",
                "hypothesis": "try an invalid compaction threshold",
                "expected_effect": "exercise fail-closed compilation",
                "evidence_ids": [],
                "edit_atoms": [
                    {
                        "kind": "set",
                        "field": "/context_compaction/threshold",
                        "value": 0.1,
                    }
                ],
                "preserve": [],
            }
        )
        records = adaptive.propose_group(
            count=1,
            round_index=0,
            base_seed=1,
            base_spec=self.base,
            base_view=self.view,
            base_user_context="{}",
            known_evidence_ids=[],
            generate=lambda *_args: (response, {}),
        )
        record = records[0]
        self.assertFalse(record.valid)
        self.assertIsNotNone(record.action)
        self.assertTrue(record.training_response)
        self.assertEqual(
            [message["role"] for message in record.trajectory],
            ["system", "user", "assistant"],
        )
        self.assertIn("expected number in [0.5, 0.9]", record.errors[0])

    def test_compiler_preserves_sah_genome_and_adds_only_overlay(self) -> None:
        base = json.loads(json.dumps(self.base))
        base["new_skills"] = [
            {"name": "kept-skill", "description": "kept", "body": "Keep this."}
        ]
        base_before = json.loads(json.dumps(base))
        action = adaptive.HarnessAction.from_dict(
            {
                "proposal_id": "candidate",
                "axis": "context",
                "hypothesis": "compact earlier while retaining four iterations",
                "edit_atoms": [
                    {
                        "kind": "set",
                        "field": "compaction.threshold",
                        "value": 0.7,
                    }
                ],
            }
        )
        effective, changed = adaptive.compile_action(
            action, base_spec=base, base_view=self.view
        )
        self.assertEqual(changed, ["/context_compaction/threshold"])
        self.assertEqual(effective["new_skills"], base["new_skills"])
        self.assertEqual(
            effective["adaptive_runtime"]["context_compaction"]["threshold"], 0.7
        )
        self.assertTrue(
            effective["adaptive_runtime"]["context_compaction"]["enabled"]
        )
        self.assertEqual(base, base_before)

    def test_adaptive_overlay_does_not_change_plain_sah_materialization(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            plain = Path(temp) / "plain"
            materialize(self.base, plain)
            plain_agent = yaml.safe_load((plain / "agent.yaml").read_text())
            self.assertFalse(
                any(
                    "context_compaction" in item["import"]
                    for item in plain_agent["middlewares"]
                )
            )

            adaptive_dir = Path(temp) / "adaptive"
            action = adaptive.HarnessAction.from_dict(
                {
                    "proposal_id": "candidate",
                    "axis": "prompt",
                    "hypothesis": "add deterministic best-valid recovery",
                    "edit_atoms": [
                        {
                            "kind": "prompt_upsert_section",
                            "field": "recovery",
                            "value": "Restore the best verifier-valid candidate.",
                        }
                    ],
                }
            )
            effective, _ = adaptive.compile_action(
                action, base_spec=self.base, base_view=self.view
            )
            materialize(effective, adaptive_dir)
            adaptive.patch_materialized_package(adaptive_dir, effective)
            adaptive_agent = yaml.safe_load(
                (adaptive_dir / "agent.yaml").read_text()
            )
            self.assertFalse(
                any(
                    "context_compaction" in item["import"]
                    for item in adaptive_agent["middlewares"]
                )
            )
            self.assertIn(
                "<!-- HARNESSOPT:recovery -->",
                (adaptive_dir / "prompt.md").read_text(),
            )

            compaction_dir = Path(temp) / "adaptive-compaction"
            compaction_action = adaptive.HarnessAction.from_dict(
                {
                    "proposal_id": "compaction",
                    "axis": "context",
                    "hypothesis": "compact tool results earlier",
                    "edit_atoms": [
                        {
                            "kind": "set",
                            "field": "compaction.threshold",
                            "value": 0.7,
                        }
                    ],
                }
            )
            compaction_effective, _ = adaptive.compile_action(
                compaction_action, base_spec=self.base, base_view=self.view
            )
            materialize(compaction_effective, compaction_dir)
            adaptive.patch_materialized_package(
                compaction_dir, compaction_effective
            )
            compaction_agent = yaml.safe_load(
                (compaction_dir / "agent.yaml").read_text()
            )
            self.assertIn(
                "context_compaction", compaction_agent["middlewares"][0]["import"]
            )

    def test_context_fallback_matches_v1_shape(self) -> None:
        task_state = {
            "archive": {
                "attempts": [{"payload": "x" * 1000} for _ in range(20)],
                "operator_statistics": {},
            },
            "controller": {},
        }
        rendered, payload = adaptive.build_user_context(
            task_id="task",
            round_index=3,
            task_spec="spec",
            seed_program="pass",
            seed_score=0.0,
            base_score=1.0,
            max_evals=20,
            current_harness=self.view,
            task_state=task_state,
            max_prompt_chars=100,
        )
        self.assertIn("optimizer_memory", payload)
        self.assertNotIn("objective", payload)
        self.assertNotIn("mutable_set_fields", payload)
        self.assertIn('"truncated": true', rendered)


def _write_rollouts(root: Path, task_id: str, scores, program_prefix: str) -> None:
    for index, score in enumerate(scores):
        run = root / f"repeat{index:02d}" / "run"
        (run / "results").mkdir(parents=True, exist_ok=True)
        (run / "summary.json").write_text(
            json.dumps([{"task_id": task_id, "best_score": score}])
        )
        (run / "results" / f"{task_id}.json").write_text(
            json.dumps(
                {
                    "task_id": task_id,
                    "best_score": score,
                    "best_program": f"{program_prefix}-{index}",
                }
            )
        )


def _make_round(
    root: Path,
    *,
    round_index: int,
    task_id: str,
    state_path: Path,
    base_score: float,
    champion_score: float,
    positive_score: float,
    negative_score: float,
    total_rounds: int = 5,
) -> Path:
    round_dir = root / f"round{round_index:03d}"
    round_dir.mkdir()
    action0 = {
        "proposal_id": f"hopt-r{round_index:03d}-s00",
        "axis": "prompt",
        "hypothesis": "candidate positive mechanism",
        "expected_effect": "higher score",
        "evidence_ids": [],
        "edit_atoms": [
            {
                "kind": "prompt_upsert_section",
                "field": f"positive-{round_index}",
                "value": "Keep the best verifier-valid program.",
            }
        ],
        "preserve": [],
        "metadata": {},
    }
    action1 = {
        **action0,
        "proposal_id": f"hopt-r{round_index:03d}-s01",
        "hypothesis": "candidate negative mechanism",
        "edit_atoms": [
            {
                "kind": "set",
                "field": "/llm/temperature",
                "value": 0.1,
            }
        ],
    }
    candidates = [
        {
            "k": 0,
            "proposal_id": action0["proposal_id"],
            "valid": True,
            "errors": [],
            "spec_hash": f"hash-{round_index}-0",
            "changed_fields": ["/system_prompt"],
            "action": action0,
        },
        {
            "k": 1,
            "proposal_id": action1["proposal_id"],
            "valid": True,
            "errors": [],
            "spec_hash": f"hash-{round_index}-1",
            "changed_fields": ["/llm/temperature"],
            "action": action1,
        },
    ]
    metadata = {
        "round": round_index,
        "protocol": adaptive.PROTOCOL,
        "protocol_state": str(state_path),
        "total_rounds": total_rounds,
        "tasks_order": [task_id],
        "bases_in": {
            task_id: {
                "package": f"/base/{round_index}",
                "score": base_score,
                "seed_score": 0.0,
            }
        },
        "proposer": {"model": "fixture"},
        "per_task": {
            task_id: {
                "base_package": f"/base/{round_index}",
                "base_score": base_score,
                "seed_score": 0.0,
                "champion_package": f"/champion/{round_index}",
                "champion_score": champion_score,
                "candidates": candidates,
            }
        },
    }
    (round_dir / "round.json").write_text(json.dumps(metadata))
    (round_dir / "prompts.json").write_text(json.dumps({task_id: "{}"}))
    (round_dir / "trajectories.json").write_text(
        json.dumps(
            [
                {
                    "task_id": task_id,
                    "k": k,
                    "system": adaptive.PROPOSER_SYSTEM_PROMPT,
                    "user": f"context-{round_index}-{k}",
                    "raw_submission": json.dumps(
                        {key: value for key, value in action.items() if key != "proposal_id"}
                    ),
                    "trajectory": [],
                }
                for k, action in enumerate((action0, action1))
            ]
        )
    )
    _write_rollouts(
        round_dir / "rollouts" / task_id / "base" / "outcome",
        task_id,
        [base_score] * 3,
        f"base-{round_index}",
    )
    _write_rollouts(
        round_dir / "rollouts" / task_id / "champion" / "promotion",
        task_id,
        [champion_score] * 3,
        f"champion-{round_index}",
    )
    for k, score in ((0, positive_score), (1, negative_score)):
        _write_rollouts(
            round_dir / "rollouts" / task_id / f"cand{k:02d}" / "outcome",
            task_id,
            [score] * 3,
            f"cand-{round_index}-{k}-outcome",
        )
        _write_rollouts(
            round_dir / "rollouts" / task_id / f"cand{k:02d}" / "promotion",
            task_id,
            [score] * 3,
            f"cand-{round_index}-{k}-promotion",
        )
    return round_dir


class AdaptiveControllerTests(unittest.TestCase):
    def test_dual_frontier_plateau_batch_and_explicit_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state_path = root / "adaptive_state.json"
            task_id = "fixture_task"
            scores = [
                (100.0, 100.0, 110.0, 90.0),
                (110.0, 110.0, 105.0, 90.0),
                (105.0, 110.0, 104.0, 90.0),
                (104.0, 110.0, 103.0, 90.0),
            ]
            rounds = []
            for index, (base, champion, positive, negative) in enumerate(scores):
                round_dir = _make_round(
                    root,
                    round_index=index,
                    task_id=task_id,
                    state_path=state_path,
                    base_score=base,
                    champion_score=champion,
                    positive_score=positive,
                    negative_score=negative,
                )
                adaptive.cmd_collect(
                    SimpleNamespace(
                        round_dir=str(round_dir),
                        protocol_state=str(state_path),
                        confidence_z=0.0,
                        plateau_rounds=3,
                    )
                )
                rounds.append(round_dir)

            first = json.loads((rounds[0] / "round_summary.json").read_text())
            self.assertEqual(first["groups"][task_id]["working_k"], 0)
            self.assertEqual(first["groups"][task_id]["champion_k"], 0)
            self.assertEqual(first["groups"][task_id]["plateau_streak"], 0)

            final = json.loads((rounds[3] / "round_summary.json").read_text())
            self.assertEqual(
                final["groups"][task_id]["training_decision"], "train_required"
            )
            self.assertTrue((rounds[3] / "adaptive_train_batch.jsonl").exists())
            state = json.loads(state_path.read_text())
            controller = state["tasks"][task_id]["controller"]
            self.assertGreater(len(controller["pending_examples"]), 0)
            self.assertEqual(controller["policy_updates"], 0)

            adaptive.commit_update(
                state_path=state_path,
                manifest_path=rounds[3] / "adaptive_train_manifest.json",
                adapter_path="/merged/mphi_u000",
                checkpoint_path="/checkpoints/mphi_u000",
            )
            committed = json.loads(state_path.read_text())
            controller = committed["tasks"][task_id]["controller"]
            self.assertEqual(controller["pending_examples"], [])
            self.assertGreater(len(controller["replay_examples"]), 0)
            self.assertEqual(controller["policy_updates"], 1)
            self.assertEqual(controller["rounds_since_confirmed_record"], 0)
            self.assertEqual(controller["last_training_decision"], "trained")

    def test_final_round_never_requests_unused_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state_path = root / "adaptive_state.json"
            task_id = "fixture_task"
            round_dir = _make_round(
                root,
                round_index=0,
                task_id=task_id,
                state_path=state_path,
                base_score=100.0,
                champion_score=100.0,
                positive_score=90.0,
                negative_score=80.0,
                total_rounds=1,
            )
            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=0.0,
                    plateau_rounds=1,
                )
            )
            summary = json.loads((round_dir / "round_summary.json").read_text())
            self.assertEqual(
                summary["groups"][task_id]["training_decision"],
                "skipped_no_future_round",
            )
            self.assertFalse((round_dir / "adaptive_train_manifest.json").exists())


class ReplayCompatibilityTests(unittest.TestCase):
    def test_adaptive_plain_text_row_has_no_sah_h1_tools(self) -> None:
        row = {
            "round": 1,
            "task_id": "task",
            "k": 0,
            "system": "system",
            "user": "user",
            "response": "{}",
            "trajectory": [],
            "tools": [],
            "advantage": 1.0,
            "reward": 0.1,
            "valid": True,
            "spec_hash": "hash",
        }
        converted = convert_row(row, [{"type": "function"}], normalize=None)
        self.assertEqual(converted["tools"], [])
        self.assertEqual(converted["metadata"]["tools"], [])

    def test_replay_cli_accepts_both_adaptive_batch_and_sah_round(self) -> None:
        base_row = {
            "round": 1,
            "task_id": "task",
            "k": 0,
            "system": "system",
            "user": "user",
            "response": "{}",
            "trajectory": [],
            "advantage": 1.0,
            "reward": 0.1,
            "valid": True,
            "spec_hash": "hash",
        }
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            adaptive_batch = temp_path / "adaptive.jsonl"
            adaptive_batch.write_text(
                json.dumps({**base_row, "tools": []}) + "\n"
            )
            adaptive_out = temp_path / "adaptive_replay.jsonl"
            env = {**os.environ, "WEAVE_ROOT": str(temp_path / "missing-weave")}
            subprocess.run(
                [
                    sys.executable,
                    str(REPO / "src" / "training" / "grpo_to_replay.py"),
                    "--batch-files",
                    str(adaptive_batch),
                    "--out",
                    str(adaptive_out),
                ],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                json.loads(adaptive_out.read_text())["tools"], []
            )

            sah_round = temp_path / "round001"
            sah_round.mkdir()
            (sah_round / "grpo_batch.jsonl").write_text(
                json.dumps(base_row) + "\n"
            )
            sah_out = temp_path / "sah_replay.jsonl"
            subprocess.run(
                [
                    sys.executable,
                    str(REPO / "src" / "training" / "grpo_to_replay.py"),
                    "--rounds",
                    str(sah_round),
                    "--out",
                    str(sah_out),
                ],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertGreater(len(json.loads(sah_out.read_text())["tools"]), 0)


class SahDefaultCompatibilityTests(unittest.TestCase):
    def test_original_sah_collect_remains_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            round_dir = Path(temp) / "round001"
            round_dir.mkdir()
            task_id = "fixture_task"
            candidates = [
                {
                    "k": 0,
                    "valid": True,
                    "spec_hash": "sah-0",
                    "changed_fields": ["sampling.temperature"],
                },
                {
                    "k": 1,
                    "valid": True,
                    "spec_hash": "sah-1",
                    "changed_fields": ["agent.max_iterations"],
                },
            ]
            (round_dir / "round.json").write_text(
                json.dumps(
                    {
                        "round": 1,
                        "tasks_order": [task_id],
                        "bases_in": {
                            task_id: {
                                "package": "/base",
                                "score": 1.0,
                                "seed_score": 0.0,
                            }
                        },
                        "per_task": {
                            task_id: {
                                "base_package": "/base",
                                "base_score": 1.0,
                                "seed_score": 0.0,
                                "candidates": candidates,
                            }
                        },
                    }
                )
            )
            (round_dir / "prompts.json").write_text(
                json.dumps({task_id: "SAH H1 user prompt"})
            )
            (round_dir / "trajectories.json").write_text(
                json.dumps(
                    [
                        {
                            "task_id": task_id,
                            "k": k,
                            "raw_submission": f"schema: h2spec/1.0 # {k}",
                            "trajectory": [],
                        }
                        for k in range(2)
                    ]
                )
            )
            for k, score in ((0, 1.2), (1, 0.8)):
                run = (
                    round_dir
                    / "rollouts"
                    / task_id
                    / f"cand{k:02d}"
                    / "run"
                )
                run.mkdir(parents=True)
                (run / "summary.json").write_text(
                    json.dumps([{"task_id": task_id, "best_score": score}])
                )

            outer_round.cmd_collect(
                SimpleNamespace(round_dir=str(round_dir), protocol=None)
            )
            next_bases = json.loads(
                (round_dir / "next_bases.json").read_text()
            )
            self.assertEqual(next_bases[task_id]["score"], 1.2)
            self.assertNotIn(
                "protocol",
                json.loads((round_dir / "round_summary.json").read_text()),
            )
            rows = [
                json.loads(line)
                for line in (round_dir / "grpo_batch.jsonl").read_text().splitlines()
            ]
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["user"], "SAH H1 user prompt")


if __name__ == "__main__":
    unittest.main()
