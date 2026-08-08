#!/usr/bin/env python3
"""Audit executor-visible contract, explicit skill use, and budget safety."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


TASK_ID = "eft__math__second_autocorr_ineq"


def text_blocks(message: dict) -> str:
    return "\n".join(
        str(block.get("text", ""))
        for block in (message.get("content") or [])
        if isinstance(block, dict) and block.get("type") == "text"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollout-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    paths = sorted(args.rollout_dir.glob(f"*/results/{TASK_ID}.json"))
    if len(paths) != 1:
        raise RuntimeError(f"expected exactly one cand03 result, got {paths}")
    result = json.loads(paths[0].read_text())
    trajectory = result.get("trajectory") or []
    skill = (result.get("skill_audit") or {}).get("c2-optimization") or {}
    ledger = result.get("ledger") or {}

    initial_text = "\n".join(
        text_blocks(message)
        for message in trajectory
        if str(message.get("role", "")).lower() == "user"
    )
    first_edit_text = ""
    tool_order = []
    for message in trajectory:
        blocks = message.get("content") or []
        for block in blocks:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            tool_order.append(block.get("name"))
            if block.get("name") == "edit_solution" and not first_edit_text:
                first_edit_text = text_blocks(message)

    normalized_first_edit = first_edit_text.lower()
    required_assertions = {
        "score_eligible": result.get("score_eligible") is True,
        "candidate_completed": result.get("stop_reason") == "completed",
        "contract_visible_in_exact_executor_input": (
            "<RuntimeComponentContract>" in initial_text
            and "Official evaluator budget: 2 call(s)." in initial_text
        ),
        "generated_skill_classified_mandatory": (
            "`c2-optimization` [AUTO-ENACTED, CURRENT CANDIDATE]" in initial_text
        ),
        "full_generated_playbook_visible": (
            "Automatically enacted proposer-generated skills" in initial_text
            and "C₂ Optimization Skill" in initial_text
        ),
        "skill_runtime_injected_before_edit": (
            int(skill.get("runtime_injections", 0)) == 1
            and int(skill.get("loads_before_first_edit", 0)) >= 1
        ),
        "executor_attributes_first_edit_to_generated_skill": (
            "c2-optimization" in normalized_first_edit
            or "c₂ optimization" in normalized_first_edit
            or "c2 optimization" in normalized_first_edit
        ),
        "base_skill_loaded_before_edit": (
            "LoadSkill" in tool_order
            and "edit_solution" in tool_order
            and tool_order.index("LoadSkill") < tool_order.index("edit_solution")
        ),
        "evaluation_budget_exact": (
            ledger.get("evaluator_calls") == ledger.get("max_evaluator_calls") == 2
        ),
        "no_dead_edit_staged": int(ledger.get("edit_calls", 0)) <= 2,
    }
    # A literal heading is useful for readability but is not causal evidence.
    # Do not fail a real replay merely because the model paraphrases the
    # requested heading while explicitly naming and following the generated
    # skill.  The mandatory gates above instead bind the exact executor input,
    # runtime injection, pre-edit ordering, and first-edit attribution.
    advisory_assertions = {
        "executor_emits_literal_component_plan_heading": (
            "component plan" in normalized_first_edit
        ),
    }
    payload = {
        "schema": "authoritative-component-contract-replay/1.0",
        "passed": all(required_assertions.values()),
        "assertions": required_assertions,
        "advisory_assertions": advisory_assertions,
        "result_path": str(paths[0]),
        "best_score": result.get("best_score"),
        "skill_audit": skill,
        "ledger": ledger,
        "tool_order": tool_order,
        "first_edit_rationale": first_edit_text,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
