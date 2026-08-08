#!/usr/bin/env python3
"""Audit trusted skill enactment and post-budget edit refusal for cand03."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


TASK_ID = "eft__math__second_autocorr_ineq"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollout-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    paths = sorted(args.rollout_dir.glob(f"*/results/{TASK_ID}.json"))
    if len(paths) != 1:
        raise RuntimeError(f"expected exactly one cand03 result, got {paths}")
    result = json.loads(paths[0].read_text())
    skill = (result.get("skill_audit") or {}).get("c2-optimization") or {}
    ledger = result.get("ledger") or {}
    trajectory = result.get("trajectory") or []

    initial_text = "\n".join(
        str(block.get("text", ""))
        for message in trajectory
        if str(message.get("role", "")).lower() == "user"
        for block in (message.get("content") or [])
        if isinstance(block, dict) and block.get("type") == "text"
    )
    budget_refusals = 0
    tool_order = []
    for message in trajectory:
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                tool_order.append(block.get("name"))
            elif block.get("type") == "tool_result" and (
                "evaluation budget is exhausted" in str(block.get("content", ""))
            ):
                budget_refusals += 1

    assertions = {
        "score_eligible": result.get("score_eligible") is True,
        "candidate_completed": result.get("stop_reason") == "completed",
        "skill_required_for_credit": skill.get("required_for_credit") is True,
        "skill_mounted": int(skill.get("mounts", 0)) >= 1,
        "skill_runtime_injected": int(skill.get("runtime_injections", 0)) == 1,
        "skill_enacted_before_edit": int(skill.get("loads_before_first_edit", 0)) >= 1,
        "full_playbook_in_initial_input": (
            "Automatically enacted proposer-generated skills" in initial_text
            and "C₂ Optimization Skill" in initial_text
        ),
        "evaluation_budget_exact": (
            ledger.get("evaluator_calls") == ledger.get("max_evaluator_calls") == 2
        ),
        "no_dead_edit_staged": int(ledger.get("edit_calls", 0)) <= 2,
    }
    payload = {
        "schema": "skill-enactment-budget-guard/1.0",
        "passed": all(assertions.values()),
        "assertions": assertions,
        "result_path": str(paths[0]),
        "best_score": result.get("best_score"),
        "skill_audit": skill,
        "ledger": ledger,
        "tool_order": tool_order,
        "post_budget_refusals": budget_refusals,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
