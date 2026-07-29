from __future__ import annotations

import json
import os
import signal
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml
from nexau import AgentConfig

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from outer import harness_spec as hs  # noqa: E402
from outer import propose as sah_propose  # noqa: E402
from outer.materialize import materialize  # noqa: E402
from outer import outer_round  # noqa: E402
from inner.eft_task import EFTTask  # noqa: E402
from inner.eval_runner import evaluate_program  # noqa: E402
from inner.harness_runner import LLMEndpoint, _override_llm  # noqa: E402
from protocols import adaptive_v1 as adaptive  # noqa: E402
from protocols import adaptive_v1_controller as adaptive_controller  # noqa: E402
from protocols.adaptive_v1_proposal import (  # noqa: E402
    AdaptiveProposeSession,
    _review_rejection_errors,
    _reviewed_training_submission,
    _submitted_effective_capabilities,
    _adaptive_tool_capability_errors,
)
from training.grpo_to_replay import convert_row  # noqa: E402


class NativeAdaptiveProposalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = hs.read_base_spec(REPO / "src" / "inner" / "harness")

    def _native_record(self, k: int, partial: dict) -> sah_propose.CandidateRecord:
        validation = hs.parse_and_validate(yaml.safe_dump(partial, sort_keys=False))
        self.assertTrue(validation.valid, validation.errors)
        effective = hs.merge_with_base(validation.spec, self.base)
        differs, changed = hs.differs_from_base(effective, self.base)
        self.assertTrue(differs)
        raw = yaml.safe_dump(partial, sort_keys=False)
        return sah_propose.CandidateRecord(
            k=k,
            valid=True,
            raw_submission=raw,
            spec=validation.spec,
            effective=effective,
            changed_fields=changed,
            spec_hash=hs.spec_hash(effective),
            trajectory=[
                {"role": "assistant", "content": f"Test native fields {changed}."}
            ],
            llm_calls=2,
            stop_reason="submitted",
        )

    def test_adaptive_has_separate_nexau_h1_and_shared_sah_surface(self) -> None:
        config = yaml.safe_load((adaptive.ADAPTIVE_H1_PACKAGE / "agent.yaml").read_text())
        self.assertEqual(config["name"], "adaptive_v1_h1_proposer")
        self.assertNotEqual(adaptive.ADAPTIVE_H1_PACKAGE, outer_round.pio.H1_PACKAGE)
        self.assertEqual(
            [tool["name"] for tool in config["tools"]],
            ["validate_spec", "submit_spec"],
        )
        self.assertTrue(
            all("../../outer/harness/tools/" in tool["yaml_path"]
                for tool in config["tools"])
        )
        self.assertEqual(config["stop_tools"], ["submit_spec"])
        self.assertEqual(config["max_iterations"], 8)
        self.assertEqual(config["llm_config"]["max_tokens"], 4096)
        AgentConfig.from_yaml(adaptive.ADAPTIVE_H1_PACKAGE / "agent.yaml")
        AgentConfig.from_yaml(
            REPO
            / "src"
            / "protocols"
            / "adaptive_v1_context_harness"
            / "agent.yaml"
        )
        self.assertIn("new_tools", adaptive.PROPOSER_SYSTEM_PROMPT)
        self.assertIn("self-contained module", adaptive.PROPOSER_SYSTEM_PROMPT)
        self.assertIn("ctx.stage_edit(program)", adaptive.PROPOSER_SYSTEM_PROMPT)
        self.assertIn("whole-field replacement", adaptive.PROPOSER_SYSTEM_PROMPT)
        self.assertIn(
            "Imports,\n  constants, and helper functions that appear between",
            adaptive.PROPOSER_SYSTEM_PROMPT,
        )
        self.assertIn(
            "full-block rewrite restore all imports",
            adaptive.PROPOSER_SYSTEM_PROMPT,
        )
        self.assertEqual(
            adaptive.H1_VERSION,
            "adaptive-h1/3.4-diverse-native-contracts",
        )
        self.assertRegex(adaptive.h1_package_hash(), r"^sha256:[0-9a-f]{16}$")
        self.assertRegex(
            adaptive.controller_package_hash(), r"^sha256:[0-9a-f]{16}$"
        )
        self.assertNotEqual(adaptive.h1_package_hash(), outer_round.pio.h1_hash())

    def test_complete_native_action_surface_is_exposed(self) -> None:
        for pointer in (
            "/system_prompt",
            "/skill_body",
            "/tool_descriptions/*",
            "/sampling/top_p",
            "/sampling/top_k",
            "/new_tools/*",
            "/new_skills/*",
            "/new_middlewares/*",
        ):
            self.assertIn(pointer, adaptive.MUTABLE_POINTERS)
        rendered, payload = adaptive.build_user_context(
            task_id="fixture",
            round_index=1,
            task_spec="fixture task",
            seed_program="pass",
            seed_score=0.0,
            base_score=1.0,
            max_evals=2,
            current_harness=self.base,
            task_state={"archive": {}, "controller": {}},
        )
        contract = payload["capability_contract"]
        self.assertEqual(contract["schema"], "h2spec/1.0")
        self.assertIn("new_tools", contract["generated_capabilities"])
        self.assertNotIn("tools", contract["always_protected"])
        self.assertIn('"new_middlewares"', rendered)

    def test_adaptive_proposal_rejects_non_30_eval_budget(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_evals=30"):
            adaptive.cmd_propose(
                SimpleNamespace(max_evals=20),
                load_bases=lambda *_args, **_kwargs: self.fail(
                    "budget gate must run before loading task state"
                ),
            )

    def test_adaptive_context_deduplicates_full_specs_and_native_inputs(self) -> None:
        attempts = []
        for index in range(12):
            attempts.append(
                {
                    "round_index": index // 4,
                    "proposal_id": f"proposal-{index}",
                    "evidence_id": f"evidence-{index}",
                    "signature": f"sha256:{index:016x}",
                    "valid": index % 3 != 0,
                    "learning_reward": float(index) / 10,
                    "outcome_score": 1.0 + index / 100,
                    "outcome_score_sem": 0.01,
                    "statistically_positive": index > 8,
                    "outcome_behavior_equivalent": False,
                    "failure_reason": None if index % 3 else "schema failure",
                    "reward_components": {"relative_delta": index / 100},
                    "action": {
                        "hypothesis": "try a distinct capability",
                        "changed_fields": [
                            "system_prompt",
                            "new_tools.large_generated_tool",
                        ],
                        "native_partial_spec": {
                            "system_prompt": (
                                "FULL_SPEC_SENTINEL-" + "x" * 20_000
                            )
                        },
                    },
                }
            )
        task_state = {
            "archive": {
                "attempts": attempts,
                "successful_actions": attempts[-4:],
                "invalid_signatures": [],
                "operator_statistics": {
                    "field:new_tools": {
                        "count": 12,
                        "mean_learning_reward": 0.2,
                        "valid_count": 8,
                        "invalid_count": 4,
                        "statistically_positive_count": 3,
                    }
                },
            },
            "controller": {
                "rounds_since_confirmed_record": 2,
                "confirmed_record": 1.25,
                "policy_updates": 1,
                "last_training_decision": "waiting_for_plateau",
            },
        }
        rendered, payload = adaptive.build_user_context(
            task_id="fixture",
            round_index=3,
            task_spec="TASK_SPEC_SENTINEL",
            seed_program="SEED_PROGRAM_SENTINEL",
            seed_score=0.0,
            base_score=1.0,
            max_evals=2,
            current_harness=self.base,
            task_state=task_state,
        )
        self.assertLessEqual(len(rendered), adaptive.ADAPTIVE_CONTEXT_MAX_CHARS)
        self.assertEqual(
            payload["context_budget"]["rendered_chars"], len(rendered)
        )
        self.assertEqual(
            payload["schema"], "sah.adaptive-v1-proposer-context/2"
        )
        self.assertNotIn("current_harness", payload)
        self.assertNotIn("recent_attempts", payload["optimizer_memory"])
        self.assertNotIn("FULL_SPEC_SENTINEL", rendered)
        self.assertNotIn("TASK_SPEC_SENTINEL", rendered)
        self.assertNotIn("SEED_PROGRAM_SENTINEL", rendered)
        self.assertLessEqual(len(payload["evidence"]), 8)
        self.assertFalse(
            payload["context_budget"]["full_historical_specs_included"]
        )
        self.assertFalse(
            payload["context_budget"]["duplicate_task_seed_harness_included"]
        )
        self.assertEqual(json.loads(rendered)["schema"], payload["schema"])

    def test_adaptive_context_has_a_parseable_hard_fallback(self) -> None:
        task_state = {
            "archive": {
                "attempts": [
                    {
                        "proposal_id": f"proposal-{index}",
                        "evidence_id": f"evidence-{index}",
                        "signature": f"signature-{index}",
                        "valid": False,
                        "failure_reason": "z" * 10_000,
                        "action": {
                            "hypothesis": "h" * 10_000,
                            "changed_fields": [
                                f"new_tools.generated_{field}"
                                for field in range(100)
                            ],
                            "native_partial_spec": {"skill_body": "x" * 50_000},
                        },
                    }
                    for index in range(20)
                ],
                "operator_statistics": {},
            },
            "controller": {},
        }
        rendered, payload = adaptive.build_user_context(
            task_id="fixture",
            round_index=5,
            task_spec="fixture",
            seed_program="pass",
            seed_score=0.0,
            base_score=0.0,
            max_evals=1,
            current_harness=self.base,
            task_state=task_state,
            max_prompt_chars=4_000,
        )
        self.assertLessEqual(len(rendered), 4_000)
        self.assertEqual(
            payload["context_budget"]["rendered_chars"], len(rendered)
        )
        self.assertGreaterEqual(payload["context_budget"]["fallback_level"], 1)
        self.assertEqual(json.loads(rendered)["schema"], payload["schema"])

    def test_sequential_native_sampling_and_qwen_tool_training_rows(self) -> None:
        calls = []

        def runner(k, **kwargs):
            calls.append((k, kwargs))
            if k == 0:
                partial = {
                    "schema": "h2spec/1.0",
                    "new_tools": [
                        {
                            "name": "score_shape",
                            "description": "Inspect current score and budget.",
                            "input_schema": {"type": "object", "properties": {}},
                            "implementation_py": (
                                "def run(ctx, args):\n"
                                "    return {'score': ctx.best_score(), "
                                "'budget': ctx.budget_left()}\n"
                            ),
                        }
                    ],
                }
            else:
                partial = {
                    "schema": "h2spec/1.0",
                    "new_skills": [
                        {
                            "name": "recovery-playbook",
                            "description": "Recover after a regression.",
                            "body": "Restore the best valid program before another edit.",
                        }
                    ],
                }
            return self._native_record(k, partial)

        records = adaptive.propose_group(
            count=2,
            round_index=2,
            base_seed=23,
            base_spec=self.base,
            base_user_context="native task context",
            known_evidence_ids=[],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            force_tool_frac=0.5,
            run_candidate=runner,
        )
        self.assertTrue(all(record.valid for record in records))
        self.assertEqual([call[1]["seed"] for call in calls], [2023, 2024])
        self.assertIn("required_capability", calls[0][1]["user_message"])
        self.assertIn(
            '"preferred_distinct_domain": "generated_tool_capability"',
            calls[0][1]["user_message"],
        )
        self.assertIn(
            '"preferred_distinct_domain": "system_prompt_or_solver_skills"',
            calls[1][1]["user_message"],
        )
        self.assertIn("new_tools.score_shape", calls[1][1]["user_message"])
        self.assertEqual(records[0].action["axis"], "tools")
        self.assertIn("<function=submit_spec>", records[0].training_response)
        self.assertIn("new_tools:", records[0].training_response)
        self.assertEqual(
            [tool["function"]["name"] for tool in adaptive.H1_TRAINING_TOOLS],
            ["validate_spec", "submit_spec"],
        )

    def test_batch_rejects_semantic_prompt_paraphrases(self) -> None:
        calls = []

        def runner(k, **kwargs):
            calls.append(kwargs["user_message"])
            return self._native_record(
                k,
                {
                    "schema": "h2spec/1.0",
                    "system_prompt": f"Distinct wording {k}, same prompt-only family.",
                },
            )

        records = adaptive.propose_group(
            count=2,
            round_index=0,
            base_seed=23,
            base_spec=self.base,
            base_user_context="native task context",
            known_evidence_ids=[],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            run_candidate=runner,
        )
        self.assertTrue(records[0].valid)
        self.assertEqual(records[0].intervention_family, "system_prompt")
        self.assertFalse(records[1].valid)
        self.assertIn("semantic duplicate", records[1].errors[0])
        self.assertIn(
            '"intervention_family": "system_prompt"', calls[1]
        )

    def test_required_tool_fraction_is_enforced_after_review(self) -> None:
        def runner(k, **_kwargs):
            return self._native_record(
                k,
                {
                    "schema": "h2spec/1.0",
                    "system_prompt": (
                        "A prompt-only candidate ignored the requirement."
                    ),
                },
            )

        records = adaptive.propose_group(
            count=1,
            round_index=0,
            base_seed=23,
            base_spec=self.base,
            base_user_context="native task context",
            known_evidence_ids=[],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            force_tool_frac=1.0,
            run_candidate=runner,
        )

        self.assertFalse(records[0].valid)
        self.assertEqual(records[0].stop_reason, "constraint_rejected")
        self.assertIn("required generated-tool", records[0].errors[0])

    def test_inherited_tool_does_not_satisfy_current_required_tool_sample(
        self,
    ) -> None:
        inherited_tool = {
            "name": "existing_helper",
            "description": "Return the current best score.",
            "input_schema": {"type": "object", "properties": {}},
            "implementation_py": (
                "def run(ctx, args):\n"
                "    return {'score': ctx.best_score()}\n"
            ),
        }
        base_with_tool = json.loads(json.dumps(self.base))
        base_with_tool["new_tools"] = [inherited_tool]
        partial = {
            "schema": "h2spec/1.0",
            "system_prompt": "A prompt-only candidate with an inherited tool.",
        }
        validation = hs.parse_and_validate(
            yaml.safe_dump(partial, sort_keys=False)
        )
        self.assertTrue(validation.valid, validation.errors)
        effective = hs.merge_with_base(validation.spec, base_with_tool)
        native = sah_propose.CandidateRecord(
            k=0,
            valid=True,
            raw_submission=yaml.safe_dump(partial, sort_keys=False),
            spec=validation.spec,
            effective=effective,
            changed_fields=["system_prompt"],
            spec_hash=hs.spec_hash(effective),
            trajectory=[],
            llm_calls=1,
            stop_reason="submitted",
        )

        records = adaptive.propose_group(
            count=1,
            round_index=0,
            base_seed=23,
            base_spec=base_with_tool,
            base_user_context="native task context",
            known_evidence_ids=[],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            force_tool_frac=0.01,
            run_candidate=lambda *_args, **_kwargs: native,
        )

        self.assertFalse(records[0].valid)
        self.assertEqual(records[0].stop_reason, "constraint_rejected")
        self.assertIn("required generated-tool", records[0].errors[0])

    def test_exact_historical_harness_is_rejected(self) -> None:
        native = self._native_record(
            0,
            {
                "schema": "h2spec/1.0",
                "sampling": {"temperature": 0.73},
            },
        )
        records = adaptive.propose_group(
            count=1,
            round_index=3,
            base_seed=23,
            base_spec=self.base,
            base_user_context="native task context",
            known_evidence_ids=[],
            historical_spec_hashes=[native.spec_hash],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            run_candidate=lambda *_args, **_kwargs: native,
        )
        self.assertFalse(records[0].valid)
        self.assertIn("duplicate", records[0].errors[0])

    def test_invalid_native_submission_keeps_transition_for_negative_credit(self) -> None:
        native = sah_propose.CandidateRecord(
            k=0,
            valid=False,
            errors=["unknown top-level keys: ['model']"],
            raw_submission="schema: h2spec/1.0\nmodel: stronger-model\n",
            trajectory=[{"role": "assistant", "content": "Try changing the model."}],
            llm_calls=1,
            stop_reason="submitted",
        )
        records = adaptive.propose_group(
            count=1,
            round_index=0,
            base_seed=1,
            base_spec=self.base,
            base_user_context="context",
            known_evidence_ids=[],
            base_url="http://127.0.0.1:9999/v1",
            model="fixture",
            run_candidate=lambda *_args, **_kwargs: native,
        )
        self.assertFalse(records[0].valid)
        self.assertEqual(records[0].stop_reason, "validation_rejected")
        self.assertIsNotNone(records[0].action)
        self.assertIn("model: stronger-model", records[0].training_response)
        self.assertIn("unknown top-level", records[0].errors[0])

    def test_generated_tool_skill_and_middleware_survive_materialization(self) -> None:
        partial = {
            "schema": "h2spec/1.0",
            "system_prompt": "Use inspect_state before editing, then preserve the best score.",
            "sampling": {"top_p": 0.8, "top_k": 12},
            "new_tools": [
                {
                    "name": "inspect_state",
                    "description": "Return current best score and remaining budget.",
                    "input_schema": {"type": "object", "properties": {}},
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    return {'score': ctx.best_score(), "
                        "'budget': ctx.budget_left()}\n"
                    ),
                }
            ],
            "new_skills": [
                {
                    "name": "state-inspection",
                    "description": "Inspect before spending an evaluation.",
                    "body": "Call inspect_state before the first edit.",
                }
            ],
            "new_middlewares": [
                {
                    "name": "inspect_reminder",
                    "hook": "before_model",
                    "description": "Remind the solver to inspect state.",
                    "implementation_py": (
                        "def before_model(hook_input):\n"
                        "    return 'Inspect state before editing.'\n"
                    ),
                }
            ],
        }
        native = self._native_record(0, partial)
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "candidate"
            materialize(
                native.effective,
                package,
                raw_spec_text=native.raw_submission,
            )
            agent = yaml.safe_load((package / "agent.yaml").read_text())
            self.assertIn("inspect_state", [tool["name"] for tool in agent["tools"]])
            self.assertIn("./skills/state-inspection", agent["skills"])
            self.assertTrue(
                any("inspect_reminder" in row["import"] for row in agent["middlewares"])
            )
            self.assertEqual(agent["llm_config"]["top_p"], 0.8)
            reconstructed = hs.read_base_spec(package)
            self.assertEqual(reconstructed["new_tools"][0]["name"], "inspect_state")
            self.assertEqual(
                reconstructed["new_skills"][0]["name"], "state-inspection"
            )
            self.assertEqual(
                reconstructed["new_middlewares"][0]["name"], "inspect_reminder"
            )

            # Generated capabilities are inherited state, not fresh causal
            # edits. Adaptive must attribute a later prompt-only proposal only
            # to the prompt and must reject an exact inherited capability list
            # as a no-op. SAH's historical diff behavior remains untouched.
            prompt_session = AdaptiveProposeSession(reconstructed)
            accepted = prompt_session.submit(
                yaml.safe_dump(
                    {
                        "schema": "h2spec/1.0",
                        "system_prompt": "Use a different prompt-only strategy.",
                    },
                    sort_keys=False,
                )
            )
            self.assertIn("SUBMITTED. Candidate spec accepted", accepted)
            self.assertEqual(prompt_session.changed_fields, ["system_prompt"])
            self.assertEqual(
                prompt_session.effective["new_tools"],
                reconstructed["new_tools"],
            )
            self.assertEqual(
                _submitted_effective_capabilities(
                    prompt_session, "new_tools"
                ),
                [],
            )
            self.assertEqual(
                _submitted_effective_capabilities(
                    prompt_session, "new_middlewares"
                ),
                [],
            )
            inherited_session = AdaptiveProposeSession(reconstructed)
            rejected = inherited_session.submit(
                yaml.safe_dump(
                    {
                        "schema": "h2spec/1.0",
                        "new_tools": reconstructed["new_tools"],
                    },
                    sort_keys=False,
                )
            )
            self.assertIn("identical to the current harness", rejected)

    def test_generated_tool_json_schema_fails_before_materialization(self) -> None:
        malformed = {
            "schema": "h2spec/1.0",
            "new_tools": [
                {
                    "name": "generate_variants",
                    "description": "Generate parameter variants.",
                    "input_schema": {
                        "type": "object",
                        "properties": {"params": "object"},
                    },
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    return {'params': args.get('params')}\n"
                    ),
                }
            ],
        }
        validation = AdaptiveProposeSession(self.base).validate(
            yaml.safe_dump(malformed, sort_keys=False)
        )
        self.assertTrue(
            "invalid JSON Schema" in validation,
            validation,
        )

        non_object_root = {
            **malformed,
            "new_tools": [
                {
                    **malformed["new_tools"][0],
                    "input_schema": {"type": "array", "items": {"type": "number"}},
                }
            ],
        }
        validation = AdaptiveProposeSession(self.base).validate(
            yaml.safe_dump(non_object_root, sort_keys=False)
        )
        self.assertTrue(
            "root type must be 'object'" in validation,
            validation,
        )

    def test_adaptive_generated_tool_cannot_bypass_context_capabilities(
        self,
    ) -> None:
        safe = {
            "new_tools": [
                {
                    "name": "safe_helper",
                    "implementation_py": (
                        "def helper(value):\n"
                        "    return value\n\n"
                        "def run(ctx, args):\n"
                        "    ctx.log('checking')\n"
                        "    return helper(ctx.budget_left())\n"
                    ),
                }
            ]
        }
        self.assertEqual(_adaptive_tool_capability_errors(safe), [])

        private_escape = {
            "new_tools": [
                {
                    "name": "unsafe_helper",
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    return ctx._s.task.evaluator_path\n"
                    ),
                }
            ]
        }
        errors = _adaptive_tool_capability_errors(private_escape)
        self.assertTrue(any("private attribute" in item for item in errors))
        rejected = AdaptiveProposeSession(self.base).validate(
            yaml.safe_dump(
                {
                    "schema": "h2spec/1.0",
                    "new_tools": [
                        {
                            **private_escape["new_tools"][0],
                            "description": "Attempt a private escape.",
                            "input_schema": {
                                "type": "object",
                                "properties": {},
                            },
                        }
                    ],
                },
                sort_keys=False,
            )
        )
        self.assertIn("private attribute access is forbidden", rejected)

        dynamic_escape = {
            "new_tools": [
                {
                    "name": "unsafe_dynamic",
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    return getattr(ctx, '_s')\n"
                    ),
                }
            ]
        }
        errors = _adaptive_tool_capability_errors(dynamic_escape)
        self.assertTrue(any("dynamic attribute" in item for item in errors))

        alias_escape = {
            "new_tools": [
                {
                    "name": "unsafe_alias",
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    hidden = ctx\n"
                        "    return hidden.evaluator\n"
                    ),
                }
            ]
        }
        errors = _adaptive_tool_capability_errors(alias_escape)
        self.assertTrue(
            any("direct receiver" in item for item in errors),
            errors,
        )

    def test_failed_generated_capability_rejects_whole_candidate(self) -> None:
        errors = _review_rejection_errors(
            [
                {
                    "name": "explore_arrangements",
                    "ok": False,
                    "error": (
                        "NameError: construct_and_score is not defined"
                    ),
                },
                {
                    "name": "safe_helper",
                    "ok": True,
                    "error": None,
                },
            ]
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("explore_arrangements", errors[0])
        self.assertIn("construct_and_score", errors[0])

    def test_training_target_uses_reviewer_repaired_tool_code(self) -> None:
        partial = {
            "schema": "h2spec/1.0",
            "system_prompt": "Call the generated helper.",
            "new_tools": [
                {
                    "name": "helper",
                    "description": "Inspect state.",
                    "input_schema": {
                        "type": "object",
                        "properties": {},
                    },
                    "implementation_py": (
                        "def run(ctx, args):\n    return missing_name\n"
                    ),
                }
            ],
        }
        effective = {
            **partial,
            "new_tools": [
                {
                    **partial["new_tools"][0],
                    "implementation_py": (
                        "def run(ctx, args):\n"
                        "    return {'score': ctx.best_score()}\n"
                    ),
                }
            ],
        }

        rendered = _reviewed_training_submission(partial, effective)
        parsed = yaml.safe_load(rendered)

        self.assertIn("ctx.best_score()", rendered)
        self.assertNotIn("missing_name", rendered)
        self.assertEqual(
            parsed["system_prompt"], "Call the generated helper."
        )

    def test_small_long_tool_output_cap_materializes_valid_nexau_config(self) -> None:
        partial = {
            "schema": "h2spec/1.0",
            "middleware": {"long_tool_output_max_chars": 2000},
        }
        validation = hs.parse_and_validate(
            yaml.safe_dump(partial, sort_keys=False)
        )
        self.assertTrue(validation.valid, validation.errors)
        effective = hs.merge_with_base(validation.spec, self.base)
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "candidate"
            materialize(
                effective,
                package,
                raw_spec_text=yaml.safe_dump(partial, sort_keys=False),
                meta={"protocol": "adaptive_v1"},
            )
            agent = yaml.safe_load((package / "agent.yaml").read_text())
            self.assertNotIn("retry_backoff_max_seconds", agent)
            config = next(
                middleware
                for middleware in agent["middlewares"]
                if "long_tool_output" in middleware["import"]
            )
            params = config["params"]
            self.assertEqual(params["max_output_chars"], 2000)
            self.assertLessEqual(
                params["head_chars"] + params["tail_chars"],
                params["max_output_chars"],
            )
            sys.path.insert(0, str(package))
            try:
                AgentConfig.from_yaml(package / "agent.yaml")
            finally:
                sys.path.pop(0)


def _write_rollouts(root: Path, task_id: str, scores, program_prefix: str) -> None:
    for index, score in enumerate(scores):
        run = root / f"repeat{index:02d}" / "run"
        (run / "results").mkdir(parents=True, exist_ok=True)
        (run / "summary.json").write_text(
            json.dumps(
                [
                    {
                        "task_id": task_id,
                        "best_score": score,
                        "stop_reason": "completed",
                    }
                ]
            )
        )
        (run / "results" / f"{task_id}.json").write_text(
            json.dumps(
                {
                    "task_id": task_id,
                    "best_score": score,
                    "best_program": f"{program_prefix}-{index}",
                    "stop_reason": "completed",
                    "error": None,
                    "trajectory": [
                        {
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "tool_use",
                                    "name": "evaluate_solution",
                                }
                            ],
                        }
                    ],
                    "ledger": {
                        "max_evaluator_calls": 30,
                        "evaluator_calls": 1,
                    },
                }
            )
        )


class AdaptiveRolloutPlanTests(unittest.TestCase):
    def test_plan_is_exact_matched_seed_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            round_dir = Path(temp)
            (round_dir / "round.json").write_text(
                json.dumps(
                    {
                        "protocol": "adaptive_v1",
                        "max_evals": 30,
                        "tasks_order": ["task_a", "task_b"],
                        "per_task": {
                            "task_a": {
                                "base_package": "/packages/a-base",
                                "champion_package": "/packages/a-champion",
                                "candidates": [
                                    {
                                        "k": 0,
                                        "valid": True,
                                        "dir": "/packages/a-cand0",
                                    },
                                    {
                                        "k": 1,
                                        "valid": False,
                                        "dir": "/packages/a-cand1",
                                    },
                                ],
                            },
                            "task_b": {
                                "base_package": "/packages/b-base",
                                "champion_package": "/packages/b-champion",
                                "candidates": [],
                            },
                        },
                    }
                )
            )
            plan = adaptive.build_rollout_plan(
                round_dir,
                outcome_repeats=2,
                promotion_repeats=3,
                seed_base=17,
            )
            self.assertEqual(len(plan["runs"]), 15)
            self.assertEqual(
                len({item["output_dir"] for item in plan["runs"]}), 15
            )
            a_base = [
                item
                for item in plan["runs"]
                if item["task_id"] == "task_a"
                and item["channel"] == "outcome_base"
            ]
            a_candidate = [
                item
                for item in plan["runs"]
                if item["task_id"] == "task_a"
                and item["channel"] == "outcome_candidate"
            ]
            self.assertEqual(
                [item["request_seed"] for item in a_base], [17, 18]
            )
            self.assertEqual(
                [item["request_seed"] for item in a_candidate], [17, 18]
            )
            b_promotion = [
                item
                for item in plan["runs"]
                if item["task_id"] == "task_b"
                and item["channel"] == "promotion_champion"
            ]
            self.assertEqual(
                [item["request_seed"] for item in b_promotion],
                [150017, 150018, 150019],
            )
            self.assertEqual(plan["eval_timeout_seconds"], 120)
            rows = adaptive.rollout_plan_shell_rows(plan)
            self.assertEqual(len(rows), 15)
            self.assertTrue(all(row.count("|") == 4 for row in rows))

    def test_plan_rejects_noncanonical_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            round_dir = Path(temp)
            (round_dir / "round.json").write_text(
                json.dumps(
                    {
                        "protocol": "adaptive_v1",
                        "max_evals": 20,
                        "tasks_order": [],
                        "per_task": {},
                    }
                )
            )
            with self.assertRaisesRegex(ValueError, "max_evals=30"):
                adaptive.build_rollout_plan(
                    round_dir,
                    outcome_repeats=2,
                    promotion_repeats=2,
                    seed_base=17,
                )

    def test_plan_rejects_noncanonical_eval_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            round_dir = Path(temp)
            (round_dir / "round.json").write_text(
                json.dumps(
                    {
                        "protocol": "adaptive_v1",
                        "max_evals": 30,
                        "tasks_order": [],
                        "per_task": {},
                    }
                )
            )
            with self.assertRaisesRegex(ValueError, "eval_timeout_seconds=120"):
                adaptive.build_rollout_plan(
                    round_dir,
                    outcome_repeats=2,
                    promotion_repeats=2,
                    seed_base=17,
                    eval_timeout_seconds=390,
                )


class EvaluatorCleanupTests(unittest.TestCase):
    def test_evaluator_descendant_is_reaped_after_worker_returns(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "child.pid"
            evaluator = root / "evaluator.py"
            initial = root / "initial.py"
            initial.write_text("def run_code():\n    return 1\n")
            evaluator.write_text(
                "import os, subprocess, sys\n"
                "from pathlib import Path\n"
                "def evaluate(_program_path):\n"
                "    child = subprocess.Popen([\n"
                "        sys.executable, '-c', 'import time; time.sleep(120)'\n"
                "    ])\n"
                "    Path(os.environ['SAH_TEST_CHILD_PID']).write_text(\n"
                "        str(child.pid)\n"
                "    )\n"
                "    return {'combined_score': 1.0, 'validity': 1.0}\n"
            )
            task = EFTTask(
                task_id="cleanup_fixture",
                source="eft",
                cost_tier="fixture",
                plan_family="fixture",
                domain="fixture",
                task_dir=root,
                initial_program_path=initial,
                evaluator_path=evaluator,
                spec="fixture",
                diff_based=False,
                per_eval_timeout_s=2.0,
                max_iterations_hint=1,
                shim_path=root,
            )
            previous = os.environ.get("SAH_TEST_CHILD_PID")
            os.environ["SAH_TEST_CHILD_PID"] = str(marker)
            child_pid = None
            try:
                outcome = evaluate_program(
                    task,
                    initial.read_text(),
                    timeout_s=2.0,
                    python_exe=sys.executable,
                )
                self.assertTrue(outcome.valid, outcome)
                child_pid = int(marker.read_text())
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
            finally:
                if previous is None:
                    os.environ.pop("SAH_TEST_CHILD_PID", None)
                else:
                    os.environ["SAH_TEST_CHILD_PID"] = previous
                if child_pid is not None:
                    try:
                        os.kill(child_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass


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
                "field": "/sampling/temperature",
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
            "changed_fields": ["/sampling/temperature"],
            "action": action1,
        },
    ]
    metadata = {
        "round": round_index,
        "protocol": adaptive.PROTOCOL,
        "protocol_state": str(state_path),
        "total_rounds": total_rounds,
        "max_evals": 30,
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
            self.assertEqual(
                state["pending_training"]["manifest_path"],
                str(rounds[3] / "adaptive_train_manifest.json"),
            )
            pending_status = adaptive.campaign_status(
                state_path=state_path, task_id=task_id
            )
            self.assertEqual(
                pending_status["pending_training"]["protocol_round"], 3
            )
            controller = state["tasks"][task_id]["controller"]
            self.assertGreater(len(controller["pending_examples"]), 0)
            self.assertEqual(controller["policy_updates"], 0)

            blocked_round = _make_round(
                root,
                round_index=4,
                task_id=task_id,
                state_path=state_path,
                base_score=103.0,
                champion_score=110.0,
                positive_score=102.0,
                negative_score=90.0,
                total_rounds=6,
            )
            with self.assertRaisesRegex(
                ValueError, "uncommitted training batch"
            ):
                adaptive.cmd_collect(
                    SimpleNamespace(
                        round_dir=str(blocked_round),
                        protocol_state=str(state_path),
                        confidence_z=0.0,
                        plateau_rounds=3,
                    )
                )

            with self.assertRaisesRegex(
                ValueError, "has no local safetensors"
            ):
                adaptive.commit_update(
                    state_path=state_path,
                    manifest_path=rounds[3]
                    / "adaptive_train_manifest.json",
                    adapter_path=str(root / "missing-adapter"),
                    checkpoint_path=None,
                )
            self.assertIsNotNone(
                json.loads(state_path.read_text())["pending_training"]
            )

            adapter_path = root / "merged" / "mphi_u000"
            adapter_path.mkdir(parents=True)
            (adapter_path / "adapter_model.safetensors").write_bytes(b"fixture")
            checkpoint_path = root / "checkpoints" / "mphi_u000"
            checkpoint_path.mkdir(parents=True)
            adaptive.commit_update(
                state_path=state_path,
                manifest_path=rounds[3] / "adaptive_train_manifest.json",
                adapter_path=str(adapter_path),
                checkpoint_path=str(checkpoint_path),
            )
            committed = json.loads(state_path.read_text())
            controller = committed["tasks"][task_id]["controller"]
            self.assertEqual(controller["pending_examples"], [])
            self.assertGreater(len(controller["replay_examples"]), 0)
            self.assertEqual(controller["policy_updates"], 1)
            self.assertEqual(controller["rounds_since_confirmed_record"], 0)
            self.assertEqual(controller["last_training_decision"], "trained")
            self.assertIsNone(committed["pending_training"])
            status = adaptive.campaign_status(
                state_path=state_path, task_id=task_id
            )
            self.assertEqual(status["next_protocol_round"], 4)
            self.assertEqual(
                status["active_adapter"]["path"], str(adapter_path)
            )
            self.assertTrue(
                status["active_adapter"]["safetensors_sha256"].startswith(
                    "sha256:"
                )
            )
            committed_manifest = json.loads(
                (
                    rounds[3] / "adaptive_train_manifest.json"
                ).read_text()
            )
            self.assertEqual(
                committed_manifest["adapter_safetensors_sha256"],
                status["active_adapter"]["safetensors_sha256"],
            )
            self.assertEqual(status["working"]["seed_score"], 0.0)
            self.assertEqual(status["champion"]["score"], 110.0)
            self.assertEqual(status["controller"]["rounds_seen"], 4)
            self.assertEqual(
                status["controller"]["last_training_decision"], "trained"
            )
            stale_state = json.loads(state_path.read_text())
            stale_state["pending_training"] = {
                "batch_sha256": "different-new-batch",
                "manifest_path": str(root / "new-manifest.json"),
            }
            state_path.write_text(json.dumps(stale_state))
            with self.assertRaisesRegex(
                ValueError, "cannot clear a different pending"
            ):
                adaptive.commit_update(
                    state_path=state_path,
                    manifest_path=rounds[3]
                    / "adaptive_train_manifest.json",
                    adapter_path=str(adapter_path),
                    checkpoint_path=str(checkpoint_path),
                )
            preserved = json.loads(state_path.read_text())
            self.assertEqual(
                preserved["pending_training"]["batch_sha256"],
                "different-new-batch",
            )
            (adapter_path / "adapter_model.safetensors").write_bytes(
                b"corrupted-after-commit"
            )
            with self.assertRaisesRegex(
                ValueError, "active adapter safetensors digest mismatch"
            ):
                adaptive.campaign_status(
                    state_path=state_path,
                    task_id=task_id,
                )

    def test_missing_matched_base_fails_closed(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            shutil.rmtree(
                round_dir / "rollouts" / task_id / "base" / "outcome"
            )
            with self.assertRaisesRegex(
                ValueError, "missing matched base outcome"
            ):
                adaptive.cmd_collect(
                    SimpleNamespace(
                        round_dir=str(round_dir),
                        protocol_state=str(state_path),
                        confidence_z=0.0,
                        plateau_rounds=3,
                    )
                )
            self.assertFalse(state_path.exists())

    def test_invalid_transition_is_retained_in_long_term_memory(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            meta = json.loads((round_dir / "round.json").read_text())
            rejected = meta["per_task"][task_id]["candidates"][1]
            rejected["valid"] = False
            rejected["errors"] = ["generated tool failed static review"]
            (round_dir / "round.json").write_text(json.dumps(meta))

            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=1.96,
                    plateau_rounds=3,
                )
            )

            state = json.loads(state_path.read_text())
            invalid = state["tasks"][task_id]["archive"][
                "invalid_signatures"
            ]
            self.assertEqual(len(invalid), 1)
            self.assertEqual(invalid[0]["proposal_id"], rejected["proposal_id"])
            self.assertIn("static review", invalid[0]["failure_reason"])

    def test_missing_promotion_never_falls_back_to_outcome(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            shutil.rmtree(
                round_dir
                / "rollouts"
                / task_id
                / "cand00"
                / "promotion"
            )
            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=0.0,
                    plateau_rounds=3,
                )
            )
            summary = json.loads((round_dir / "round_summary.json").read_text())
            group = summary["groups"][task_id]
            self.assertEqual(group["working_k"], 0)
            self.assertIsNone(group["champion_k"])
            self.assertIsNone(group["rows"][0]["promotion_score"])

    def test_missing_champion_reference_disables_promotion(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            shutil.rmtree(
                round_dir
                / "rollouts"
                / task_id
                / "champion"
                / "promotion"
            )
            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=0.0,
                    plateau_rounds=3,
                )
            )
            group = json.loads(
                (round_dir / "round_summary.json").read_text()
            )["groups"][task_id]
            self.assertFalse(group["champion_reference_available"])
            self.assertIsNone(group["champion_k"])

    def test_unchanged_frontiers_use_latest_matched_repeat_estimates(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state_path = root / "adaptive_state.json"
            task_id = "fixture_task"
            round_dir = _make_round(
                root,
                round_index=0,
                task_id=task_id,
                state_path=state_path,
                base_score=90.0,
                champion_score=95.0,
                positive_score=80.0,
                negative_score=70.0,
            )
            _write_rollouts(
                round_dir / "rollouts" / task_id / "base" / "outcome",
                task_id,
                [105.0] * 3,
                "remeasured-base",
            )
            _write_rollouts(
                round_dir
                / "rollouts"
                / task_id
                / "champion"
                / "promotion",
                task_id,
                [107.0] * 3,
                "remeasured-champion",
            )

            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=1.96,
                    plateau_rounds=3,
                )
            )

            group = json.loads(
                (round_dir / "round_summary.json").read_text()
            )["groups"][task_id]
            self.assertIsNone(group["working_k"])
            self.assertFalse(group["working_advanced"])
            self.assertEqual(group["base_score_prior"], 90.0)
            self.assertEqual(group["base_score"], 105.0)
            self.assertEqual(group["working_score"], 105.0)
            self.assertIsNone(group["champion_k"])
            self.assertFalse(group["champion_advanced"])
            self.assertEqual(group["champion_reference_score"], 107.0)
            self.assertEqual(group["champion_score"], 107.0)

            next_bases = json.loads(
                (round_dir / "next_bases.json").read_text()
            )
            self.assertEqual(next_bases[task_id]["score"], 105.0)
            state = json.loads(state_path.read_text())["tasks"][task_id]
            self.assertEqual(state["working"]["score"], 105.0)
            self.assertEqual(state["champion"]["score"], 107.0)

    def test_production_plan_rejects_incomplete_rollout_channels(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            runs = []
            for repeat in range(4):
                runs.append(
                    {
                        "task_id": task_id,
                        "channel": "outcome_base",
                        "candidate": None,
                        "repeat": repeat,
                    }
                )
                for candidate in (0, 1):
                    runs.append(
                        {
                            "task_id": task_id,
                            "channel": "outcome_candidate",
                            "candidate": candidate,
                            "repeat": repeat,
                        }
                    )
            for repeat in range(3):
                runs.append(
                    {
                        "task_id": task_id,
                        "channel": "promotion_champion",
                        "candidate": None,
                        "repeat": repeat,
                    }
                )
                for candidate in (0, 1):
                    runs.append(
                        {
                            "task_id": task_id,
                            "channel": "promotion_candidate",
                            "candidate": candidate,
                            "repeat": repeat,
                        }
                    )
            (round_dir / "adaptive_rollout_plan.json").write_text(
                json.dumps(
                    {
                        "schema": "sah.adaptive-v1-rollout-plan/1",
                        "outcome_repeats": 4,
                        "promotion_repeats": 3,
                        "runs": runs,
                    }
                )
            )
            with self.assertRaisesRegex(
                ValueError, "expected 4 completed summaries, got 3"
            ):
                adaptive.cmd_collect(
                    SimpleNamespace(
                        round_dir=str(round_dir),
                        protocol_state=str(state_path),
                        confidence_z=1.96,
                        plateau_rounds=3,
                    )
                )
            self.assertFalse(state_path.exists())
            self.assertFalse((round_dir / "round_summary.json").exists())

    def test_strict_samples_exclude_harness_error_seed_scores(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task_id = "fixture_task"
            _write_rollouts(root, task_id, [1.0, 2.0], "fixture")
            completed_summary = (
                root / "repeat00" / "run" / "summary.json"
            )
            completed_payload = json.loads(completed_summary.read_text())
            completed_payload[0]["steps"] = [
                {"kind": "seed", "edit_mode": "seed", "error": None},
                {
                    "kind": "full_rewrite",
                    "edit_mode": "full_rewrite",
                    "error": "Circles 2 and 3 overlap: dist=0",
                },
                {
                    "kind": "full_rewrite",
                    "edit_mode": "full_rewrite",
                    "error": "IndexError: index 26 is out of bounds",
                },
            ]
            completed_summary.write_text(json.dumps(completed_payload))
            completed_result = (
                root
                / "repeat00"
                / "run"
                / "results"
                / f"{task_id}.json"
            )
            result_payload = json.loads(completed_result.read_text())
            result_payload["trajectory"] = [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "custom_optimizer",
                        },
                        {
                            "type": "tool_use",
                            "name": "evaluate_solution",
                        },
                    ],
                }
            ]
            completed_result.write_text(json.dumps(result_payload))
            summary = root / "repeat01" / "run" / "summary.json"
            payload = json.loads(summary.read_text())
            payload[0]["stop_reason"] = "harness_error"
            summary.write_text(json.dumps(payload))
            permissive = adaptive.load_rollout_samples(root, task_id)
            strict = adaptive.load_rollout_samples(
                root, task_id, require_completed=True
            )
            self.assertEqual(permissive.scores, (1.0, 2.0))
            self.assertEqual(strict.scores, (1.0,))
            self.assertEqual(
                dict(strict.error_counts),
                {"circle_overlap": 1, "index_out_of_bounds": 1},
            )
            self.assertEqual(strict.invalid_steps, 2)
            self.assertEqual(strict.evaluated_steps, 2)
            self.assertEqual(
                dict(strict.edit_mode_counts), {"full_rewrite": 2}
            )
            self.assertEqual(
                dict(strict.custom_tool_call_counts),
                {"custom_optimizer": 1},
            )

    def test_strict_samples_require_full_result_and_inner_trace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task_id = "fixture_task"
            _write_rollouts(root, task_id, [1.0], "fixture")
            result = (
                root
                / "repeat00"
                / "run"
                / "results"
                / f"{task_id}.json"
            )
            result.unlink()
            self.assertEqual(
                adaptive.load_rollout_samples(root, task_id).scores,
                (1.0,),
            )
            self.assertEqual(
                adaptive.load_rollout_samples(
                    root, task_id, require_completed=True
                ).scores,
                (),
            )
            _write_rollouts(root, task_id, [1.0], "fixture")
            payload = json.loads(result.read_text())
            payload["ledger"]["max_evaluator_calls"] = 20
            result.write_text(json.dumps(payload))
            self.assertEqual(
                adaptive.load_rollout_samples(
                    root,
                    task_id,
                    require_completed=True,
                    expected_max_evals=30,
                ).scores,
                (),
            )
            _write_rollouts(root, task_id, [1.0], "fixture")
            payload = json.loads(result.read_text())
            payload["best_program"] = ""
            result.write_text(json.dumps(payload))
            self.assertEqual(
                adaptive.load_rollout_samples(
                    root,
                    task_id,
                    require_completed=True,
                    expected_max_evals=30,
                ).scores,
                (),
            )

    def test_strict_best_program_uses_only_planned_valid_repeats(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task_id = "fixture_task"
            _write_rollouts(root, task_id, [1.0, 2.0], "planned")
            extra = root / "repeat99" / "run"
            (extra / "results").mkdir(parents=True)
            (extra / "results" / f"{task_id}.json").write_text(
                json.dumps(
                    {
                        "best_score": 999.0,
                        "best_program": "unplanned",
                        "stop_reason": "completed",
                        "error": None,
                        "trajectory": [{"role": "assistant", "content": []}],
                        "ledger": {
                            "max_evaluator_calls": 30,
                            "evaluator_calls": 1,
                        },
                    }
                )
            )
            program, score = adaptive.load_best_program(
                root,
                task_id,
                expected_repeats=2,
                expected_max_evals=30,
            )
            self.assertEqual(program, "planned-1")
            self.assertEqual(score, 2.0)

            planned = (
                root
                / "repeat01"
                / "run"
                / "results"
                / f"{task_id}.json"
            )
            payload = json.loads(planned.read_text())
            payload["ledger"]["max_evaluator_calls"] = 20
            planned.write_text(json.dumps(payload))
            program, score = adaptive.load_best_program(
                root,
                task_id,
                expected_repeats=2,
                expected_max_evals=30,
            )
            self.assertEqual(program, "planned-0")
            self.assertEqual(score, 1.0)

    def test_rollout_telemetry_keeps_outcome_and_promotion_isolated(
        self,
    ) -> None:
        outcome = adaptive.RolloutSamples(
            scores=(1.0, 1.1),
            program_digests=("a", "b"),
            error_counts=(("circle_overlap", 2),),
            invalid_steps=2,
            evaluated_steps=7,
            edit_mode_counts=(("diff", 5),),
            custom_tool_call_counts=(),
        )
        promotion = adaptive.RolloutSamples(
            scores=(1.2,),
            program_digests=("c",),
            error_counts=(("circle_overlap", 1), ("timeout", 1)),
            invalid_steps=2,
            evaluated_steps=4,
            edit_mode_counts=(("diff", 2), ("full_rewrite", 1)),
            custom_tool_call_counts=(("search_hexagonal", 1),),
        )

        telemetry = adaptive_controller._samples_telemetry(outcome)
        promotion_telemetry = adaptive_controller._samples_telemetry(
            promotion
        )
        self.assertEqual(
            telemetry["error_counts"],
            {"circle_overlap": 2},
        )
        self.assertEqual(telemetry["invalid_steps"], 2)
        self.assertEqual(telemetry["evaluated_steps"], 7)
        self.assertEqual(
            telemetry["edit_mode_counts"],
            {"diff": 5},
        )
        self.assertEqual(telemetry["custom_tool_call_counts"], {})
        self.assertEqual(
            promotion_telemetry["error_counts"],
            {"circle_overlap": 1, "timeout": 1},
        )
        self.assertEqual(promotion_telemetry["invalid_steps"], 2)
        self.assertEqual(promotion_telemetry["evaluated_steps"], 4)
        self.assertEqual(
            promotion_telemetry["edit_mode_counts"],
            {"diff": 2, "full_rewrite": 1},
        )
        self.assertEqual(
            promotion_telemetry["custom_tool_call_counts"],
            {"search_hexagonal": 1},
        )

    def test_paired_confidence_gate_rejects_lucky_champion_sample(self) -> None:
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
                positive_score=110.0,
                negative_score=90.0,
            )
            _write_rollouts(
                round_dir
                / "rollouts"
                / task_id
                / "cand00"
                / "promotion",
                task_id,
                [100.0, 100.0, 103.0],
                "lucky-promotion",
            )
            promotion_result = (
                round_dir
                / "rollouts"
                / task_id
                / "cand00"
                / "promotion"
                / "repeat00"
                / "run"
                / "results"
                / f"{task_id}.json"
            )
            promotion_payload = json.loads(promotion_result.read_text())
            promotion_payload["trajectory"] = [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "search_hexagonal",
                        }
                    ],
                }
            ]
            promotion_result.write_text(json.dumps(promotion_payload))
            adaptive.cmd_collect(
                SimpleNamespace(
                    round_dir=str(round_dir),
                    protocol_state=str(state_path),
                    confidence_z=1.96,
                    plateau_rounds=3,
                )
            )
            group = json.loads(
                (round_dir / "round_summary.json").read_text()
            )["groups"][task_id]
            self.assertIsNone(group["champion_k"])
            self.assertAlmostEqual(
                group["rows"][0]["promotion_delta_sem"], 1.0
            )
            self.assertEqual(
                group["rows"][0]["promotion_telemetry"][
                    "custom_tool_call_counts"
                ],
                {"search_hexagonal": 1},
            )
            state = json.loads(state_path.read_text())
            archived = state["tasks"][task_id]["archive"]["attempts"][0]
            self.assertEqual(
                archived["rollout_telemetry"]["custom_tool_call_counts"],
                {},
            )
            self.assertNotIn("promotion_telemetry", archived)

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
        converted = convert_row(
            row,
            [{"type": "function"}],
            normalize=None,
            use_row_tools=True,
        )
        self.assertEqual(converted["tools"], [])
        self.assertEqual(converted["metadata"]["tools"], [])

    def test_sah_replay_ignores_adaptive_row_tool_override_by_default(self) -> None:
        shared_tools = [{"type": "function", "function": {"name": "shared"}}]
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
        converted = convert_row(row, shared_tools, normalize=None)
        self.assertEqual(converted["tools"], shared_tools)
        self.assertEqual(converted["metadata"]["tools"], shared_tools)

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
    def test_dataset_override_is_adaptive_namespaced_and_opt_in(self) -> None:
        env = {
            **os.environ,
            "PYTHONPATH": str(REPO / "src"),
            "SAH_DATASET_ROOT": "/tmp/must-not-affect-default-sah",
        }
        env.pop("ADAPTIVE_V1_DATASET_ROOT", None)
        command = [
            sys.executable,
            "-c",
            "from inner.eft_task import DATASET_ROOT; print(DATASET_ROOT)",
        ]
        default_root = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(
            default_root,
            "/lustre/fsw/portfolios/av/users/yingzim/datasets/"
            "self_adapt_harness",
        )

        env["ADAPTIVE_V1_DATASET_ROOT"] = "/tmp/adaptive-dataset"
        namespaced_but_unselected_root = subprocess.run(
            command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(namespaced_but_unselected_root, default_root)

        explicit_command = [
            sys.executable,
            "-c",
            (
                "from inner import eft_task; "
                "eft_task.configure_dataset_root('/tmp/adaptive-dataset'); "
                "print(eft_task.DATASET_ROOT)"
            ),
        ]
        adaptive_root = subprocess.run(
            explicit_command,
            check=True,
            env=env,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(adaptive_root, "/tmp/adaptive-dataset")

    def test_request_seed_is_absent_from_default_sah_llm_body(self) -> None:
        default_config = SimpleNamespace(
            llm_config=SimpleNamespace(extra_params={})
        )
        _override_llm(default_config, LLMEndpoint(seed=None))
        default_body = default_config.llm_config.extra_params["extra_body"]
        self.assertNotIn("seed", default_body)

        adaptive_config = SimpleNamespace(
            llm_config=SimpleNamespace(extra_params={})
        )
        _override_llm(adaptive_config, LLMEndpoint(seed=104729))
        adaptive_body = adaptive_config.llm_config.extra_params["extra_body"]
        self.assertEqual(adaptive_body["seed"], 104729)

    def test_default_sah_materializer_keeps_legacy_long_output_shape(
        self,
    ) -> None:
        base = hs.read_base_spec(REPO / "src" / "inner" / "harness")
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "default-sah"
            materialize(base, package)
            agent = yaml.safe_load((package / "agent.yaml").read_text())
            self.assertEqual(agent["retry_backoff_max_seconds"], 30)
            config = next(
                middleware
                for middleware in agent["middlewares"]
                if "long_tool_output" in middleware["import"]
            )
            self.assertEqual(
                config["params"],
                {
                    "max_output_chars": 8000,
                    "head_lines": 40,
                    "tail_lines": 20,
                    "head_chars": 4000,
                    "tail_chars": 4000,
                    "bypass_tool_names": ["finish", "LoadSkill"],
                },
            )

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
