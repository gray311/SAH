#!/usr/bin/env python3
"""Build an auditable, compact digest of the eight AC2 H1/H2 trajectories."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
INSPECTION = HERE.parent
RUN = INSPECTION.parents[1]
ROUND = RUN / "rounds" / "round001"
TASK = "eft__math__second_autocorr_ineq"
BASE_PROMPT = RUN / "source_snapshot" / "src" / "inner" / "harness" / "system.md"


def load(path: Path) -> Any:
    return json.loads(path.read_text())


def block_text(block: dict[str, Any]) -> str:
    value = block.get("text", block.get("content", ""))
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def text_from_message(message: dict[str, Any]) -> str:
    content = message.get("content", [])
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(
        block_text(block)
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ).strip()


def action_digest(trajectory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for message in trajectory:
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            call_id = str(block.get("tool_use_id") or block.get("id") or "")
            results[call_id] = {
                "is_error": bool(block.get("is_error", False)),
                "text": block_text(block),
            }

    actions: list[dict[str, Any]] = []
    for message_index, message in enumerate(trajectory):
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        rationale = "\n".join(
            block_text(block)
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ).strip()
        for block_index, block in enumerate(content):
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            call_id = str(block.get("id") or block.get("tool_use_id") or "")
            arguments = block.get("input")
            if not isinstance(arguments, dict):
                arguments = {}
            action = {
                "ordinal": len(actions) + 1,
                "message_index": message_index,
                "block_index": block_index,
                "name": str(block.get("name", "")),
                "call_id": call_id,
                "rationale": rationale,
                "input": arguments,
                "result": results.get(call_id),
            }
            code = arguments.get("code")
            if isinstance(code, str):
                action["code_sha256"] = hashlib.sha256(code.encode()).hexdigest()
                action["edit_features"] = edit_features(code)
            actions.append(action)
    return actions


def edit_features(code: str) -> list[str]:
    lower = code.lower()
    features: list[str] = []
    patterns = {
        "hyperparameters": r"num_intervals|learning_rate|num_steps|warmup_steps",
        "step_or_plateau": r"step.function|piecewise|plateau|jnp\.where",
        "exponential_tail": r"jnp\.exp|exponential|decay",
        "gaussian": r"gaussian|normal\(",
        "triangular_or_ramp": r"triang|linspace|ramp",
        "symmetry": r"symmetr|\[::?-1\]|flip\(",
        "multi_start": r"multi.start|for seed|random restart|best_f",
        "positivity_change": r"softplus|relu|non.negative|jnp\.maximum",
        "objective_or_convolution": r"_objective_fn|convolution|fft_f|l2_norm",
        "optimizer_change": r"adamw|adafactor|rmsprop|clip_by_global_norm",
        "shape_change": r"concatenate|pad_size|num_intervals",
    }
    for name, pattern in patterns.items():
        if re.search(pattern, lower):
            features.append(name)
    return features


def eval_observations(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for action in actions:
        if action["name"] not in {"evaluate_solution", "probe_solution"}:
            continue
        result = (action.get("result") or {}).get("text", "")
        def capture(pattern: str) -> Any:
            match = re.search(pattern, result)
            return match.group(1) if match else None
        observations.append({
            "action_ordinal": action["ordinal"],
            "name": action["name"],
            "combined_score": capture(r"combined_score\s*=\s*([-+0-9.eE]+)"),
            "validity": capture(r"validity\s*=\s*([-+0-9.eE]+)"),
            "evaluations_left": capture(r"evaluations_left\s*=\s*([0-9]+)"),
            "is_error": bool((action.get("result") or {}).get("is_error", False)),
            "result": result,
        })
    return observations


def compact_action(action: dict[str, Any]) -> str:
    name = action["name"]
    if name == "LoadSkill":
        return f"LoadSkill({action['input']})"
    if name == "edit_solution":
        features = ",".join(action.get("edit_features", [])) or "unclassified"
        return f"edit_solution[{features}]"
    if name in {"evaluate_solution", "probe_solution"}:
        result = (action.get("result") or {}).get("text", "")
        score = re.search(r"combined_score\s*=\s*([-+0-9.eE]+)", result)
        valid = re.search(r"validity\s*=\s*([-+0-9.eE]+)", result)
        left = re.search(r"evaluations_left\s*=\s*([0-9]+)", result)
        return (
            f"{name}(score={score.group(1) if score else '?'},"
            f" valid={valid.group(1) if valid else '?'},"
            f" left={left.group(1) if left else '?'})"
        )
    return f"{name}({action['input']})"


def prompt_features(text: str) -> dict[str, Any]:
    lower = text.lower()
    keywords = {
        "step_or_piecewise": r"step|piecewise|plateau",
        "symmetry": r"symmetr|even function|f\(-x\)",
        "resolution_or_multiscale": r"resolution|multi.scale|coarse|refin|interval",
        "learning_rate": r"learning rate|\blr\b",
        "multi_start": r"multi.start|random restart|different seed",
        "optimizer_variant": r"adamw|rmsprop|adafactor|cma.es|cobyla",
        "positivity": r"non.negativ|softplus|\bexp\(",
        "gaussian_or_decay": r"gaussian|exponential|decay",
        "basis_change": r"spline|fourier|rational|mixture",
        "probe": r"probe_solution|\bprobe\b",
        "specific_hyperparameters": r"\b(?:n|num_intervals)\s*=|\blr\s*=|\b0\.00[0-9]|\b[12]00\b|\b20000\b",
        "wrong_36_eval_claim": r"36 evaluations|budget:\s*36",
        "correct_2_eval_claim": r"2 evaluations|only 2",
    }
    tokens = re.findall(r"[a-z0-9_]+", lower)
    return {
        "chars": len(text),
        "lines": len(text.splitlines()),
        "tokens": len(tokens),
        "keyword_flags": {
            name: bool(re.search(pattern, lower))
            for name, pattern in keywords.items()
        },
    }


def diversity_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    token_sets = {
        row["candidate"]: set(re.findall(r"[a-z0-9_]+", row["prompt_delta"].lower()))
        for row in rows
    }
    pairs: list[dict[str, Any]] = []
    names = sorted(token_sets)
    for left_index, left in enumerate(names):
        for right in names[left_index + 1:]:
            union = token_sets[left] | token_sets[right]
            intersection = token_sets[left] & token_sets[right]
            pairs.append({
                "left": left,
                "right": right,
                "word_set_jaccard": (
                    len(intersection) / len(union) if union else 1.0
                ),
            })
    return {
        "prompt_features": {
            row["candidate"]: prompt_features(row["prompt_delta"])
            for row in rows
        },
        "pairwise_word_set_jaccard": pairs,
        "mean_pairwise_word_set_jaccard": (
            sum(pair["word_set_jaccard"] for pair in pairs) / len(pairs)
            if pairs else None
        ),
    }


def main() -> None:
    base_prompt = BASE_PROMPT.read_text()
    rows: list[dict[str, Any]] = []
    markdown = [
        "# AC2 round001 mechanical trajectory digest",
        "",
        "This file is generated from the immutable inspection bundle. It records",
        "tool chronology and source fields; interpretation belongs in `REPORT.md`.",
        "",
    ]
    for k in range(8):
        name = f"cand{k:02d}"
        candidate_dir = INSPECTION / "candidates" / name
        materialized = ROUND / "tasks" / TASK / name
        meta = load(materialized / "meta.json")
        prompt = (materialized / "prompt.md").read_text()
        if prompt.startswith(base_prompt):
            prompt_delta = prompt[len(base_prompt):].strip()
        else:
            prompt_delta = prompt
        proposer_actions = action_digest(load(candidate_dir / "02_proposer_full_trajectory.json"))
        executor_actions = action_digest(load(candidate_dir / "06_executor_full_trajectory.json"))
        reward = load(candidate_dir / "07_executor_reward.json")
        train = load(candidate_dir / "09_proposer_grpo_training_row.json")
        row = {
            "candidate": name,
            "changed_fields": meta.get("changed_fields", []),
            "component_lineage": meta.get("component_lineage", {}),
            "prompt_delta": prompt_delta,
            "prompt_delta_sha256": hashlib.sha256(prompt_delta.encode()).hexdigest(),
            "proposer_actions": proposer_actions,
            "executor_actions": executor_actions,
            "evaluation_observations": eval_observations(executor_actions),
            "seed_score": reward.get("seed_score"),
            "best_score": reward.get("best_score"),
            "steps": reward.get("steps"),
            "ledger": reward.get("ledger"),
            "stop_reason": reward.get("stop_reason"),
            "score_eligible": reward.get("score_eligible"),
            "skill_audit": reward.get("skill_audit", {}),
            "training": {
                key: train.get(key)
                for key in (
                    "score", "reward", "advantage", "valid", "spec_hash",
                    "control_score", "causal_delta", "attribution_status",
                )
            },
        }
        rows.append(row)

        markdown.extend([
            f"## {name}",
            "",
            f"- changed fields: `{meta.get('changed_fields', [])}`",
            f"- score: seed `{reward.get('seed_score')}` -> best `{reward.get('best_score')}`",
            f"- old training reward/advantage: `{train.get('reward')}` / `{train.get('advantage')}`",
            f"- proposer calls: {' -> '.join(a['name'] for a in proposer_actions)}",
            f"- executor calls: {' -> '.join(compact_action(a) for a in executor_actions)}",
            "",
            "Prompt delta:",
            "",
            "```markdown",
            prompt_delta,
            "```",
            "",
        ])

    (HERE / "candidate_matrix.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    )
    (HERE / "prompt_diversity.json").write_text(
        json.dumps(diversity_summary(rows), ensure_ascii=False, indent=2) + "\n"
    )
    (HERE / "MECHANICAL_DIGEST.md").write_text("\n".join(markdown) + "\n")


if __name__ == "__main__":
    main()
