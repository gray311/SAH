"""Adaptive v1 rollout assessment, dual frontiers, and training controller."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

from protocols.adaptive_v1_proposal import (
    EPS,
    PROTOCOL,
    PROPOSER_SYSTEM_PROMPT,
    _atomic_write_json,
    _digest,
    _json_clone,
    _operator_statistics,
    _task_state,
    load_state,
    resolve_state_path,
)

CONTROLLER_VERSION = "adaptive-controller/1.4-bounded-evaluator"


def controller_package_hash() -> str:
    """Hash the Adaptive-only assessment/state-transition runtime."""
    source = Path(__file__).resolve()
    return "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()[:16]


def _adapter_safetensors_hash(adapter: Path) -> str:
    files = sorted(Path(adapter).glob("*.safetensors"))
    if not files:
        raise ValueError(
            f"Adaptive adapter path has no local safetensors: {adapter}"
        )
    hasher = hashlib.sha256()
    for path in files:
        hasher.update(path.name.encode())
        with path.open("rb") as handle:
            while chunk := handle.read(8 * 1024 * 1024):
                hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def build_rollout_plan(
    round_dir: Path,
    *,
    outcome_repeats: int,
    promotion_repeats: int,
    seed_base: int,
    eval_timeout_seconds: int = 120,
) -> Dict[str, Any]:
    """Create the exact matched outcome/promotion run matrix.

    This is Adaptive-only so the shared SAH worker contains only a small
    protocol dispatch instead of an embedded second controller.
    """
    if outcome_repeats < 1 or promotion_repeats < 1:
        raise ValueError("Adaptive rollout repeat counts must both be positive")
    if seed_base < 0:
        raise ValueError("Adaptive rollout seed base must be nonnegative")
    if eval_timeout_seconds != 120:
        raise ValueError(
            "Adaptive rollout plan requires eval_timeout_seconds=120"
        )
    round_dir = Path(round_dir)
    meta = json.loads((round_dir / "round.json").read_text())
    if meta.get("protocol") != PROTOCOL:
        raise ValueError("rollout plan requires an Adaptive v1 round")
    if int(meta.get("max_evals", 0)) != 30:
        raise ValueError("Adaptive rollout plan requires max_evals=30")

    runs: List[Dict[str, Any]] = []

    def add(
        task_id: str,
        label: str,
        package: str,
        output_dir: Path,
        request_seed: int,
        channel: str,
        repeat: int,
        candidate: Optional[int] = None,
    ) -> None:
        runs.append(
            {
                "task_id": task_id,
                "label": label,
                "package": str(package),
                "output_dir": str(output_dir),
                "request_seed": request_seed,
                "channel": channel,
                "repeat": repeat,
                "candidate": candidate,
            }
        )

    for task_index, task_id in enumerate(meta["tasks_order"]):
        task = meta["per_task"][task_id]
        task_root = round_dir / "rollouts" / task_id
        for repeat in range(outcome_repeats):
            request_seed = seed_base + task_index * 100000 + repeat
            add(
                task_id,
                f"base-outcome-r{repeat:02d}",
                task["base_package"],
                task_root / "base" / "outcome" / f"repeat{repeat:02d}",
                request_seed,
                "outcome_base",
                repeat,
            )
        for repeat in range(promotion_repeats):
            request_seed = (
                seed_base + task_index * 100000 + 50000 + repeat
            )
            add(
                task_id,
                f"champion-promotion-r{repeat:02d}",
                task["champion_package"],
                task_root
                / "champion"
                / "promotion"
                / f"repeat{repeat:02d}",
                request_seed,
                "promotion_champion",
                repeat,
            )
        for candidate in task["candidates"]:
            if not candidate["valid"]:
                continue
            k = int(candidate["k"])
            for repeat in range(outcome_repeats):
                request_seed = seed_base + task_index * 100000 + repeat
                add(
                    task_id,
                    f"cand{k:02d}-outcome-r{repeat:02d}",
                    candidate["dir"],
                    task_root
                    / f"cand{k:02d}"
                    / "outcome"
                    / f"repeat{repeat:02d}",
                    request_seed,
                    "outcome_candidate",
                    repeat,
                    k,
                )
            for repeat in range(promotion_repeats):
                request_seed = (
                    seed_base + task_index * 100000 + 50000 + repeat
                )
                add(
                    task_id,
                    f"cand{k:02d}-promotion-r{repeat:02d}",
                    candidate["dir"],
                    task_root
                    / f"cand{k:02d}"
                    / "promotion"
                    / f"repeat{repeat:02d}",
                    request_seed,
                    "promotion_candidate",
                    repeat,
                    k,
                )
    output_dirs = [item["output_dir"] for item in runs]
    if len(output_dirs) != len(set(output_dirs)):
        raise ValueError("Adaptive rollout plan contains duplicate output dirs")
    return {
        "schema": "sah.adaptive-v1-rollout-plan/1",
        "seed_base": seed_base,
        "outcome_repeats": outcome_repeats,
        "promotion_repeats": promotion_repeats,
        "eval_timeout_seconds": eval_timeout_seconds,
        "runs": runs,
    }


def write_rollout_plan(
    round_dir: Path,
    *,
    outcome_repeats: int,
    promotion_repeats: int,
    seed_base: int,
    eval_timeout_seconds: int = 120,
) -> Dict[str, Any]:
    plan = build_rollout_plan(
        round_dir,
        outcome_repeats=outcome_repeats,
        promotion_repeats=promotion_repeats,
        seed_base=seed_base,
        eval_timeout_seconds=eval_timeout_seconds,
    )
    _atomic_write_json(Path(round_dir) / "adaptive_rollout_plan.json", plan)
    return plan


def rollout_plan_shell_rows(plan: Mapping[str, Any]) -> List[str]:
    """Render validated worker records; controlled paths may not contain `|`."""
    rows = []
    for item in plan["runs"]:
        fields = (
            item["task_id"],
            item["label"],
            item["package"],
            item["output_dir"],
            str(item["request_seed"]),
        )
        if any("|" in str(field) or "\n" in str(field) for field in fields):
            raise ValueError("Adaptive rollout path contains a shell delimiter")
        rows.append("|".join(str(field) for field in fields))
    return rows


@dataclass(frozen=True)
class RolloutSamples:
    scores: tuple[float, ...]
    program_digests: tuple[str, ...]
    error_counts: tuple[tuple[str, int], ...] = ()
    invalid_steps: int = 0
    evaluated_steps: int = 0
    edit_mode_counts: tuple[tuple[str, int], ...] = ()
    custom_tool_call_counts: tuple[tuple[str, int], ...] = ()

    @property
    def mean(self) -> Optional[float]:
        return sum(self.scores) / len(self.scores) if self.scores else None

    @property
    def sem(self) -> Optional[float]:
        if len(self.scores) < 2:
            return 0.0 if self.scores else None
        return statistics.stdev(self.scores) / math.sqrt(len(self.scores))


def load_rollout_samples(
    root: Path,
    task_id: str,
    *,
    require_completed: bool = False,
    expected_max_evals: Optional[int] = None,
) -> RolloutSamples:
    rows: List[tuple[str, float, str]] = []
    error_counts: Counter[str] = Counter()
    edit_mode_counts: Counter[str] = Counter()
    custom_tool_call_counts: Counter[str] = Counter()
    invalid_steps = 0
    evaluated_steps = 0
    root = Path(root)
    for summary in sorted(root.rglob("summary.json")) if root.exists() else []:
        try:
            for row in json.loads(summary.read_text()):
                if row.get("task_id") != task_id or row.get("best_score") is None:
                    continue
                if require_completed and (
                    row.get("stop_reason") != "completed" or row.get("error")
                ):
                    continue
                for step in row.get("steps") or []:
                    if not isinstance(step, Mapping):
                        continue
                    if step.get("kind") not in {"seed", "note"}:
                        evaluated_steps += 1
                    mode = step.get("edit_mode")
                    if mode and mode != "seed":
                        edit_mode_counts[str(mode)] += 1
                    error = str(step.get("error") or "")
                    if error:
                        invalid_steps += 1
                        lower = error.lower()
                        if "overlap" in lower:
                            error_counts["circle_overlap"] += 1
                        elif "out of bounds" in lower:
                            error_counts["index_out_of_bounds"] += 1
                        elif "syntaxerror" in lower:
                            error_counts["syntax_error"] += 1
                        elif "timeout" in lower:
                            error_counts["timeout"] += 1
                        else:
                            error_counts["program_execution_error"] += 1
                result_file = summary.parent / "results" / f"{task_id}.json"
                digest = ""
                result: Optional[Mapping[str, Any]] = None
                if require_completed and not result_file.exists():
                    continue
                if result_file.exists():
                    loaded_result = json.loads(result_file.read_text())
                    if not isinstance(loaded_result, Mapping):
                        continue
                    result = loaded_result
                    if require_completed:
                        result_score = result.get("best_score")
                        summary_score = row.get("best_score")
                        program = result.get("best_program")
                        ledger = result.get("ledger")
                        ledger = ledger if isinstance(ledger, Mapping) else {}
                        maximum_calls = ledger.get("max_evaluator_calls")
                        evaluator_calls = ledger.get("evaluator_calls")
                        budget_valid = (
                            expected_max_evals is None
                            or (
                                isinstance(maximum_calls, int)
                                and not isinstance(maximum_calls, bool)
                                and maximum_calls == expected_max_evals
                                and isinstance(evaluator_calls, int)
                                and not isinstance(evaluator_calls, bool)
                                and 0 <= evaluator_calls <= expected_max_evals
                            )
                        )
                        if (
                            result.get("stop_reason") != "completed"
                            or result.get("error")
                            or not result.get("trajectory")
                            or not isinstance(result_score, (int, float))
                            or isinstance(result_score, bool)
                            or not math.isfinite(float(result_score))
                            or not isinstance(summary_score, (int, float))
                            or isinstance(summary_score, bool)
                            or not math.isfinite(float(summary_score))
                            or not isinstance(program, str)
                            or not program
                            or not math.isclose(
                                float(result_score),
                                float(summary_score),
                                rel_tol=0.0,
                                abs_tol=1e-12,
                            )
                            or not budget_valid
                        ):
                            continue
                    program = result.get("best_program")
                    if isinstance(program, str):
                        digest = hashlib.sha256(program.encode()).hexdigest()
                    builtins = {
                        "LoadSkill",
                        "edit_solution",
                        "evaluate_solution",
                        "probe_solution",
                        "finish",
                    }
                    for message in result.get("trajectory") or []:
                        if not isinstance(message, Mapping):
                            continue
                        for block in message.get("content") or []:
                            if (
                                isinstance(block, Mapping)
                                and block.get("type") == "tool_use"
                                and block.get("name") not in builtins
                            ):
                                custom_tool_call_counts[
                                    str(block.get("name"))
                                ] += 1
                rows.append((str(summary), float(row["best_score"]), digest))
        except Exception:
            continue
    if not rows and root.exists() and not require_completed:
        for checkpoint in sorted(root.rglob(f"checkpoints/{task_id}.json")):
            try:
                payload = json.loads(checkpoint.read_text())
                rows.append(
                    (
                        str(checkpoint),
                        float(payload["best_score"]),
                        hashlib.sha256(
                            str(payload.get("best_program", "")).encode()
                        ).hexdigest(),
                    )
                )
            except Exception:
                continue
    return RolloutSamples(
        scores=tuple(row[1] for row in rows),
        program_digests=tuple(row[2] for row in rows if row[2]),
        error_counts=tuple(error_counts.most_common(4)),
        invalid_steps=invalid_steps,
        evaluated_steps=evaluated_steps,
        edit_mode_counts=tuple(edit_mode_counts.most_common(4)),
        custom_tool_call_counts=tuple(
            custom_tool_call_counts.most_common(4)
        ),
    )


def _rollout_repeat_contract(
    round_dir: Path, round_meta: Mapping[str, Any]
) -> Optional[tuple[int, int]]:
    """Return strict repeat counts when the production rollout plan exists."""
    path = round_dir / "adaptive_rollout_plan.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    if payload.get("schema") != "sah.adaptive-v1-rollout-plan/1":
        raise ValueError(f"invalid Adaptive rollout plan schema: {path}")
    outcome = int(payload.get("outcome_repeats", 0))
    promotion = int(payload.get("promotion_repeats", 0))
    if outcome < 1 or promotion < 1:
        raise ValueError(
            "Adaptive rollout plan requires positive outcome/promotion repeats"
        )
    expected: Counter[tuple[str, str, Optional[int]]] = Counter()
    for task_id in round_meta.get("tasks_order") or []:
        expected[(task_id, "outcome_base", None)] = outcome
        expected[(task_id, "promotion_champion", None)] = promotion
        candidates = (
            (round_meta.get("per_task") or {}).get(task_id, {}).get("candidates")
            or []
        )
        for candidate in candidates:
            if not candidate.get("valid"):
                continue
            index = int(candidate["k"])
            expected[(task_id, "outcome_candidate", index)] = outcome
            expected[(task_id, "promotion_candidate", index)] = promotion
    observed: Counter[tuple[str, str, Optional[int]]] = Counter()
    for item in payload.get("runs") or []:
        candidate = item.get("candidate")
        observed[
            (
                str(item.get("task_id", "")),
                str(item.get("channel", "")),
                int(candidate) if candidate is not None else None,
            )
        ] += 1
    if observed != expected:
        missing = list((expected - observed).elements())
        extra = list((observed - expected).elements())
        raise ValueError(
            "Adaptive rollout plan channel cardinality mismatch: "
            f"missing={missing[:6]} extra={extra[:6]}"
        )
    return outcome, promotion


def _require_repeat_count(
    samples: RolloutSamples, *, expected: int, label: str
) -> None:
    if len(samples.scores) != expected:
        raise ValueError(
            f"incomplete Adaptive rollout channel {label}: "
            f"expected {expected} completed summaries, got {len(samples.scores)}"
        )


def _samples_telemetry(samples: RolloutSamples) -> Dict[str, Any]:
    """Render bounded execution telemetry for one isolated score channel."""
    return {
        "error_counts": dict(samples.error_counts),
        "invalid_steps": samples.invalid_steps,
        "evaluated_steps": samples.evaluated_steps,
        "edit_mode_counts": dict(samples.edit_mode_counts),
        "custom_tool_call_counts": dict(samples.custom_tool_call_counts),
    }


def _validated_program_result(
    result_file: Path,
    *,
    expected_max_evals: Optional[int],
) -> Optional[tuple[str, float]]:
    result = json.loads(result_file.read_text())
    program = result.get("best_program")
    score = result.get("best_score")
    if (
        not isinstance(program, str)
        or not program
        or not isinstance(score, (int, float))
        or isinstance(score, bool)
        or not math.isfinite(float(score))
        or result.get("stop_reason") != "completed"
        or result.get("error")
        or not (result.get("trajectory") or [])
    ):
        return None
    if expected_max_evals is not None:
        ledger = result.get("ledger") or {}
        maximum = ledger.get("max_evaluator_calls")
        calls = ledger.get("evaluator_calls")
        if (
            maximum != expected_max_evals
            or not isinstance(calls, int)
            or isinstance(calls, bool)
            or calls < 0
            or calls > expected_max_evals
        ):
            return None
    return program, float(score)


def load_best_program(
    root: Path,
    task_id: str,
    *,
    expected_repeats: Optional[int] = None,
    expected_max_evals: Optional[int] = None,
) -> tuple[Optional[str], Optional[float]]:
    best_program: Optional[str] = None
    best_score: Optional[float] = None
    root = Path(root)
    if expected_repeats is None:
        result_files = sorted(root.rglob(f"results/{task_id}.json"))
    else:
        result_files = []
        for repeat in range(expected_repeats):
            hits = sorted(
                (root / f"repeat{repeat:02d}").rglob(
                    f"results/{task_id}.json"
                )
            )
            if len(hits) != 1:
                raise ValueError(
                    "strict Adaptive result lookup expected exactly one result "
                    f"for repeat{repeat:02d}, got {len(hits)}"
                )
            result_files.append(hits[0])
    for result_file in result_files:
        try:
            validated = _validated_program_result(
                result_file,
                expected_max_evals=expected_max_evals,
            )
            if validated is not None:
                program, score = validated
                if best_score is None or score > best_score:
                    best_program = program
                    best_score = score
        except Exception:
            if expected_repeats is not None:
                raise
            continue
    return best_program, best_score


def _paired_delta_sem(
    candidate: RolloutSamples, baseline: RolloutSamples
) -> Optional[float]:
    if not candidate.scores or not baseline.scores:
        return None
    if len(candidate.scores) == len(baseline.scores) and len(candidate.scores) > 1:
        deltas = [
            candidate_score - baseline_score
            for candidate_score, baseline_score in zip(
                candidate.scores, baseline.scores
            )
        ]
        return statistics.stdev(deltas) / math.sqrt(len(deltas))
    csem = float(candidate.sem or 0.0)
    bsem = float(baseline.sem or 0.0)
    return math.sqrt(csem * csem + bsem * bsem)


def _zscore(values: Sequence[float]) -> List[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((item - mean) ** 2 for item in values) / len(values)
    std = math.sqrt(variance)
    return [0.0 for _ in values] if std <= EPS else [
        (item - mean) / std for item in values
    ]


def _rms_normalize(values: Sequence[float]) -> List[float]:
    if not values:
        return []
    rms = math.sqrt(sum(item * item for item in values) / len(values))
    if rms <= EPS:
        return list(values)
    return [max(-2.0, min(2.0, item / rms)) for item in values]


def _behavior_equivalent(
    candidate: RolloutSamples, baseline: RolloutSamples
) -> bool:
    return bool(
        candidate.program_digests
        and baseline.program_digests
        and set(candidate.program_digests) == set(baseline.program_digests)
    )


def _training_rows(
    *,
    task_id: str,
    round_index: int,
    candidate_rows: Sequence[Mapping[str, Any]],
    historical_record: Optional[float],
    confidence_z: float,
) -> tuple[List[Dict[str, Any]], bool, Optional[float]]:
    relative = [float(row["relative_delta"]) for row in candidate_rows]
    ranks = _zscore(relative)
    raw_advantages: List[float] = []
    components: List[Dict[str, float]] = []
    confirmed_record = historical_record
    for row, delta, rank in zip(candidate_rows, relative, ranks):
        valid = bool(row["valid"])
        hard_zero = valid and (
            bool(row["behavior_equivalent"]) or abs(delta) <= EPS
        )
        anchor = math.tanh(delta / 0.25)
        rank_term = max(-1.0, min(1.0, rank / 2.0))
        score = row.get("score")
        confirmed_parent = bool(row.get("confirmed_parent_progress"))
        is_record = bool(
            valid
            and not hard_zero
            and confirmed_parent
            and score is not None
            and (historical_record is None or float(score) > historical_record)
        )
        record_gain = (
            max(
                0.0,
                (float(score) - float(historical_record))
                / (abs(float(historical_record)) + EPS),
            )
            if is_record and historical_record is not None
            else 1.0 if is_record else 0.0
        )
        record_bonus = math.tanh(record_gain / 0.05)
        value = 0.70 * anchor + 0.20 * rank_term + 0.30 * record_bonus
        if not valid:
            value = min(value, -1.0)
        elif hard_zero:
            value = 0.0
        elif delta > 0.0:
            value = max(value, 0.05)
        elif delta < 0.0:
            value = min(value, -0.05)
        if delta > 0.0 and not hard_zero:
            value = max(value, 0.05)
        if hard_zero:
            value = 0.0
        raw_advantages.append(value)
        components.append(
            {
                "relative_delta": delta,
                "terminal_anchor": anchor,
                "group_rank_term": rank_term,
                "record_bonus": record_bonus,
                "confirmed_record": float(is_record),
                "hard_zero_terminal": float(hard_zero),
            }
        )
        if is_record:
            confirmed_record = max(
                float(score),
                confirmed_record if confirmed_record is not None else float("-inf"),
            )
    normalized = _rms_normalize(raw_advantages)
    output: List[Dict[str, Any]] = []
    for row, advantage, reward_components in zip(
        candidate_rows, normalized, components
    ):
        if not row.get("action"):
            continue
        output.append(
            {
                "schema": "evogate.proposer-training-row/v1",
                "round": round_index,
                "task_id": task_id,
                "k": row["k"],
                "proposal_id": row["proposal_id"],
                "system": row["system"],
                "user": row["user"],
                "response": row["response"],
                "response_format": row.get("response_format", "plain_text"),
                "trajectory": [],
                "tools": _json_clone(row.get("tools") or []),
                "advantage": advantage,
                "reward": reward_components["relative_delta"],
                "reward_components": reward_components,
                "valid": bool(row["valid"]),
                "score": row["score"],
                "spec_hash": row["spec_hash"],
                "policy_source_model": row.get("policy_source_model"),
            }
        )
    new_record = bool(
        confirmed_record is not None
        and (historical_record is None or confirmed_record > historical_record)
    )
    return output, new_record, confirmed_record


def _balanced_replay(
    pending: Sequence[Mapping[str, Any]],
    replay: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    output = [_json_clone(row) for row in pending]
    positive = sorted(
        (row for row in replay if float(row.get("advantage", 0.0)) > 0.0),
        key=lambda row: float(row["advantage"]),
        reverse=True,
    )
    negative = sorted(
        (row for row in replay if float(row.get("advantage", 0.0)) < 0.0),
        key=lambda row: float(row["advantage"]),
    )
    for original in [*positive[:1], *negative[:1]]:
        row = _json_clone(original)
        row["unscaled_advantage"] = float(row["advantage"])
        row["advantage"] = float(row["advantage"]) * 0.25
        row["policy_batch_source"] = "balanced_replay"
        output.append(row)
    return output


def _append_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    with open(path, "w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def cmd_collect(args) -> None:
    """Adaptive reward/frontier/controller implementation of collect."""
    round_dir = Path(args.round_dir)
    meta = json.loads((round_dir / "round.json").read_text())
    if meta.get("protocol") != PROTOCOL:
        raise ValueError("Adaptive collector received a non-Adaptive round")
    if int(meta.get("max_evals", 0)) != 30:
        raise ValueError(
            "Adaptive V1 collector requires a max_evals=30 round"
        )
    state_path = resolve_state_path(
        round_dir, getattr(args, "protocol_state", None) or meta.get("protocol_state")
    )
    state = load_state(state_path)
    pending_training = state.get("pending_training")
    if isinstance(pending_training, Mapping):
        raise ValueError(
            "Adaptive state has an uncommitted training batch at "
            f"{pending_training.get('manifest_path')}; commit or resolve it "
            "before collecting another round"
        )
    trajectories = {
        (item["task_id"], item["k"]): item
        for item in json.loads((round_dir / "trajectories.json").read_text())
    }
    total_rounds = meta.get("total_rounds")
    protocol_round = int(meta.get("protocol_round", meta["round"]))
    has_future_round = (
        total_rounds is None or protocol_round + 1 < int(total_rounds)
    )
    confidence_z = float(getattr(args, "confidence_z", 0.0) or 0.0)
    plateau_rounds = int(getattr(args, "plateau_rounds", 3) or 3)
    repeat_contract = _rollout_repeat_contract(round_dir, meta)
    strict_rollouts = repeat_contract is not None
    expected_outcome, expected_promotion = repeat_contract or (0, 0)
    expected_max_evals = int(meta.get("max_evals", 0))
    if strict_rollouts and expected_max_evals < 1:
        raise ValueError("Adaptive production round has no positive max_evals")

    groups: Dict[str, Any] = {}
    next_bases = dict(meta.get("bases_in") or {})
    current_round_rows: List[Dict[str, Any]] = []
    triggered_tasks: List[str] = []
    tasks_state = dict(state.get("tasks") or {})
    best_programs_path = round_dir.parent / "best_programs.json"
    try:
        best_programs = (
            json.loads(best_programs_path.read_text())
            if best_programs_path.exists() else {}
        )
    except Exception:
        best_programs = {}

    for tid in meta["tasks_order"]:
        pt = meta["per_task"][tid]
        task_state = _task_state(
            state,
            tid,
            base_package=pt["base_package"],
            base_score=float(pt["base_score"]),
            seed_score=float(pt["seed_score"]),
        )
        if protocol_round in task_state["collected_rounds"]:
            raise ValueError(
                f"Adaptive protocol round {protocol_round} already collected for {tid}"
            )
        controller = task_state["controller"]
        archive = task_state["archive"]
        historical_record = controller.get("confirmed_record")

        outcome_base = load_rollout_samples(
            round_dir / "rollouts" / tid / "base" / "outcome",
            tid,
            require_completed=strict_rollouts,
            expected_max_evals=(
                expected_max_evals if strict_rollouts else None
            ),
        )
        if strict_rollouts:
            _require_repeat_count(
                outcome_base,
                expected=expected_outcome,
                label=f"{tid}/base/outcome",
            )
        if not outcome_base.scores:
            raise ValueError(
                f"missing matched base outcome rollout for {tid}; "
                "Adaptive collection fails closed"
            )
        champion_baseline = load_rollout_samples(
            round_dir / "rollouts" / tid / "champion" / "promotion",
            tid,
            require_completed=strict_rollouts,
            expected_max_evals=(
                expected_max_evals if strict_rollouts else None
            ),
        )
        if strict_rollouts:
            _require_repeat_count(
                champion_baseline,
                expected=expected_promotion,
                label=f"{tid}/champion/promotion",
            )
        champion_reference_available = bool(champion_baseline.scores)

        rows: List[Dict[str, Any]] = []
        for candidate in pt["candidates"]:
            k = int(candidate["k"])
            trajectory = trajectories.get((tid, k), {})
            outcome_root = (
                round_dir / "rollouts" / tid / f"cand{k:02d}" / "outcome"
            )
            if not outcome_root.exists():
                outcome_root = round_dir / "rollouts" / tid / f"cand{k:02d}"
            outcome = (
                load_rollout_samples(
                    outcome_root,
                    tid,
                    require_completed=strict_rollouts,
                    expected_max_evals=(
                        expected_max_evals if strict_rollouts else None
                    ),
                )
                if candidate.get("valid")
                else RolloutSamples((), ())
            )
            promotion = load_rollout_samples(
                round_dir / "rollouts" / tid / f"cand{k:02d}" / "promotion",
                tid,
                require_completed=strict_rollouts,
                expected_max_evals=(
                    expected_max_evals if strict_rollouts else None
                ),
            )
            if strict_rollouts and candidate.get("valid"):
                _require_repeat_count(
                    outcome,
                    expected=expected_outcome,
                    label=f"{tid}/cand{k:02d}/outcome",
                )
                _require_repeat_count(
                    promotion,
                    expected=expected_promotion,
                    label=f"{tid}/cand{k:02d}/promotion",
                )
            score = outcome.mean
            valid = bool(candidate.get("valid") and score is not None)
            directional = (
                float(score) - float(outcome_base.mean)
                if valid and outcome_base.mean is not None
                else -abs(float(outcome_base.mean or pt["base_score"]))
            )
            relative = directional / (abs(float(outcome_base.mean or 0.0)) + EPS)
            delta_sem = _paired_delta_sem(outcome, outcome_base) if valid else None
            behavior_equivalent = (
                _behavior_equivalent(outcome, outcome_base) if valid else False
            )
            uncertainty_available = confidence_z <= 0.0 or delta_sem is not None
            confirmed_parent = bool(
                valid
                and not behavior_equivalent
                and directional > 0.0
                and uncertainty_available
                and directional > confidence_z * float(delta_sem or 0.0)
            )
            rows.append(
                {
                    "k": k,
                    "proposal_id": candidate.get(
                        "proposal_id", f"hopt-r{protocol_round:03d}-s{k:02d}"
                    ),
                    "valid": valid,
                    "score": score,
                    "score_samples": list(outcome.scores),
                    "score_sem": outcome.sem,
                    "delta": directional,
                    "relative_delta": relative,
                    "delta_sem": delta_sem,
                    "behavior_equivalent": behavior_equivalent,
                    # Only outcome telemetry reaches the proposer archive.
                    # Promotion remains an isolated champion-selection channel.
                    "rollout_telemetry": _samples_telemetry(outcome),
                    # Still retain promotion execution evidence in the round
                    # summary for artifact audit and human diagnosis.
                    "promotion_telemetry": _samples_telemetry(promotion),
                    "confirmed_parent_progress": confirmed_parent,
                    "promotion_score": promotion.mean,
                    "promotion_samples": list(promotion.scores),
                    "promotion_sem": promotion.sem,
                    "promotion_delta_sem": (
                        _paired_delta_sem(promotion, champion_baseline)
                        if promotion.scores and champion_baseline.scores
                        else None
                    ),
                    "spec_hash": candidate.get("spec_hash", ""),
                    "changed_fields": candidate.get("changed_fields", []),
                    "action": candidate.get("action"),
                    "system": trajectory.get("system", PROPOSER_SYSTEM_PROMPT),
                    "user": trajectory.get("user", ""),
                    "response": trajectory.get(
                        "training_response", trajectory.get("raw_submission", "")
                    ),
                    "response_format": (
                        "qwen3_xml_tool_call"
                        if trajectory.get("training_tools")
                        else "plain_text"
                    ),
                    "tools": trajectory.get("training_tools", []),
                    "policy_source_model": (meta.get("proposer") or {}).get("model"),
                    "failure_reason": (
                        None if valid else "; ".join(candidate.get("errors") or ["rollout_missing"])
                    ),
                }
            )

        transition_rows = [row for row in rows if row.get("action")]
        training_rows, new_record, confirmed_record = _training_rows(
            task_id=tid,
            round_index=protocol_round,
            candidate_rows=transition_rows,
            historical_record=(
                float(historical_record) if historical_record is not None else None
            ),
            confidence_z=confidence_z,
        )
        by_k = {row["k"]: row for row in training_rows}
        for row in rows:
            train = by_k.get(row["k"])
            row["advantage"] = train["advantage"] if train else 0.0
            row["reward"] = train["reward"] if train else -1.0

        # Working frontier: best admissible non-equivalent candidate, allowing
        # at most 10% regression for exploration, and never advancing after the
        # last usable round.
        regression_floor = -0.10 * max(abs(float(outcome_base.mean or 0.0)), EPS)
        working_eligible = [
            row for row in rows
            if row["valid"]
            and not row["behavior_equivalent"]
            and row["delta"] >= regression_floor
        ]
        working = (
            max(working_eligible, key=lambda row: float(row["score"]))
            if working_eligible and has_future_round else None
        )

        # Champion uses only promotion feedback and never leaks that signal
        # into the proposer archive or training reward.
        champion_base_score = (
            float(champion_baseline.mean)
            if champion_baseline.mean is not None
            else None
        )
        champion_eligible = []
        if champion_reference_available and champion_base_score is not None:
            for row in rows:
                if not row["valid"] or row["promotion_score"] is None:
                    continue
                gain = float(row["promotion_score"]) - champion_base_score
                delta_sem = row["promotion_delta_sem"]
                if confidence_z > 0.0 and delta_sem is None:
                    continue
                margin = confidence_z * float(delta_sem or 0.0)
                if gain > 0.0 and gain > margin:
                    champion_eligible.append(row)
        champion = (
            max(champion_eligible, key=lambda row: float(row["promotion_score"]))
            if champion_eligible else None
        )

        if working is not None:
            next_bases[tid] = {
                "package": str(
                    round_dir / "tasks" / tid / f"cand{working['k']:02d}"
                ),
                "score": working["score"],
                "seed_score": pt["seed_score"],
                "from": f"round{meta['round']:03d}/cand{working['k']:02d}:working",
            }
        else:
            # The matched base repeats are a newer estimate of the same
            # working harness than the score carried into this round. Keep
            # behavior-equivalent candidates reward-neutral, but do not feed a
            # stale frontier score into the next proposal context.
            next_bases[tid] = {
                "package": pt["base_package"],
                "score": float(outcome_base.mean),
                "seed_score": pt["seed_score"],
                "from": f"round{meta['round']:03d}:working_reestimate",
            }
        task_state["working"] = dict(next_bases[tid])
        if champion is not None:
            task_state["champion"] = {
                "package": str(
                    round_dir / "tasks" / tid / f"cand{champion['k']:02d}"
                ),
                "score": champion["promotion_score"],
                "from": f"round{meta['round']:03d}/cand{champion['k']:02d}:champion",
            }
        elif champion_reference_available and champion_baseline.mean is not None:
            # Promotion-baseline repeats similarly refresh the protected
            # champion estimate without counting as a promotion event.
            task_state["champion"] = {
                **task_state["champion"],
                "score": float(champion_baseline.mean),
                "from": f"round{meta['round']:03d}:champion_reestimate",
            }

        attempts = list(archive.get("attempts") or [])
        successful = list(archive.get("successful_actions") or [])
        invalid_signatures = list(archive.get("invalid_signatures") or [])
        for row in rows:
            if not row["action"]:
                continue
            confidence_margin = (
                confidence_z * float(row["delta_sem"])
                if row["delta_sem"] is not None else None
            )
            if confidence_z > 0.0 and confidence_margin is None:
                learning_reward = 0.0
            elif confidence_margin is not None:
                learning_reward = math.copysign(
                    max(0.0, abs(float(row["delta"])) - confidence_margin),
                    float(row["delta"]),
                )
            else:
                learning_reward = float(row["delta"])
            if row["behavior_equivalent"] or abs(float(row["delta"])) <= EPS:
                learning_reward = 0.0
            evidence_id = (
                f"adaptive-v1:{tid}:r{protocol_round:03d}:s{int(row['k']):02d}"
            )
            attempt = {
                "round_index": protocol_round,
                "proposal_id": row["proposal_id"],
                "evidence_id": evidence_id,
                "signature": row.get("spec_hash") or _digest(row["action"]),
                "action": row["action"],
                "valid": row["valid"],
                "reward": row["delta"],
                "learning_reward": learning_reward,
                "reward_components": {
                    "relative_delta": row["relative_delta"],
                    "terminal_anchor": math.tanh(row["relative_delta"] / 0.25),
                },
                "outcome_score": row["score"],
                "outcome_score_sem": row["score_sem"],
                "outcome_delta_sem": row["delta_sem"],
                "confidence_z": confidence_z,
                "confidence_margin": confidence_margin,
                "statistically_positive": learning_reward > 0.0,
                "outcome_behavior_equivalent": row["behavior_equivalent"],
                "rollout_telemetry": row["rollout_telemetry"],
                "failure_reason": row["failure_reason"],
            }
            attempts.append(attempt)
            if row["valid"] and learning_reward > 0.0:
                successful.append(attempt)
            elif not row["valid"]:
                invalid_signatures.append(attempt)
        attempts = attempts[-256:]
        successful = sorted(
            successful[-256:],
            key=lambda item: (
                float(item.get("learning_reward", 0.0)),
                str(item.get("proposal_id", "")),
            ),
        )
        invalid_by_signature: Dict[str, Mapping[str, Any]] = {}
        for item in invalid_signatures:
            if not isinstance(item, Mapping):
                continue
            signature = str(item.get("signature") or _digest(item))
            invalid_by_signature.pop(signature, None)
            invalid_by_signature[signature] = item
        task_state["archive"] = {
            **archive,
            "attempts": attempts,
            "successful_actions": successful,
            "invalid_signatures": list(invalid_by_signature.values())[-128:],
            "operator_statistics": _operator_statistics(attempts),
        }

        pending = [
            _json_clone(row)
            for row in controller.get("pending_examples", [])
            if isinstance(row, Mapping)
        ]
        pending.extend(training_rows)
        pending = pending[-128:]
        replay = [
            _json_clone(row)
            for row in controller.get("replay_examples", [])
            if isinstance(row, Mapping)
        ][-256:]
        streak = (
            0 if new_record
            else int(controller.get("rounds_since_confirmed_record", 0)) + 1
        )
        contrast = (
            any(float(row.get("advantage", 0.0)) > 0.0 for row in pending)
            and any(float(row.get("advantage", 0.0)) < 0.0 for row in pending)
        )
        trigger = streak >= plateau_rounds
        train_required = trigger and contrast and has_future_round
        decision = (
            "waiting_for_plateau"
            if not trigger
            else "skipped_no_future_round"
            if not has_future_round
            else "skipped_no_signed_contrast"
            if not contrast
            else "train_required"
        )
        history = list(controller.get("training_history") or [])
        history.append(
            {
                "round": protocol_round,
                "decision": decision,
                "new_confirmed_record": new_record,
                "confirmed_record": confirmed_record,
                "streak_before_reset": streak,
                "pending_examples": len(pending),
                "signed_contrast": contrast,
            }
        )
        task_state["controller"] = {
            **controller,
            "rounds_seen": int(controller.get("rounds_seen", 0)) + 1,
            "rounds_since_confirmed_record": streak,
            "confirmed_record": confirmed_record,
            "pending_examples": pending,
            "replay_examples": replay,
            "last_training_decision": decision,
            "training_history": history,
        }
        task_state["collected_rounds"].append(protocol_round)
        tasks_state[tid] = task_state
        current_round_rows.extend(training_rows)
        if train_required:
            triggered_tasks.append(tid)
        groups[tid] = {
            "task_id": tid,
            "base_score_prior": pt["base_score"],
            "base_score": outcome_base.mean,
            "base_score_samples": list(outcome_base.scores),
            "rows": rows,
            "working_k": working["k"] if working else None,
            "working_score": task_state["working"]["score"],
            "working_advanced": working is not None,
            "champion_k": champion["k"] if champion else None,
            "champion_score": task_state["champion"]["score"],
            "champion_advanced": champion is not None,
            "champion_reference_available": champion_reference_available,
            "champion_reference_score": champion_baseline.mean,
            "champion_reference_samples": list(champion_baseline.scores),
            "new_confirmed_record": new_record,
            "confirmed_record": confirmed_record,
            "plateau_streak": streak,
            "signed_contrast": contrast,
            "training_decision": decision,
        }
        scored_rows = [
            row for row in rows if row["valid"] and row["score"] is not None
        ]
        if scored_rows:
            best_observed = max(scored_rows, key=lambda row: float(row["score"]))
            program, program_score = load_best_program(
                round_dir
                / "rollouts"
                / tid
                / f"cand{int(best_observed['k']):02d}"
                / "outcome",
                tid,
                expected_repeats=(
                    expected_outcome if strict_rollouts else None
                ),
                expected_max_evals=(
                    expected_max_evals if strict_rollouts else None
                ),
            )
            previous = dict(best_programs.get(tid) or {})
            if (
                program
                and program_score is not None
                and float(previous.get("score", float("-inf"))) < program_score
            ):
                parents = list(previous.get("parents") or [])
                if previous.get("program") and previous["program"] != program:
                    parents = [
                        {
                            "score": previous.get("score"),
                            "program": previous["program"],
                        },
                        *parents,
                    ]
                best_programs[tid] = {
                    "score": program_score,
                    "program": program,
                    "round": meta["round"],
                    "protocol_round": protocol_round,
                    "k": best_observed["k"],
                    "parents": parents[:2],
                }
        print(
            f"  {tid}: base={outcome_base.mean} working="
            f"{working['score'] if working else None} champion="
            f"{champion['promotion_score'] if champion else None} "
            f"plateau={streak} decision={decision}"
        )

    state["tasks"] = tasks_state
    _atomic_write_json(best_programs_path, best_programs)
    _append_jsonl(round_dir / "grpo_batch.jsonl", current_round_rows)
    (round_dir / "next_bases.json").write_text(json.dumps(next_bases, indent=2))
    summary = {
        "round": meta["round"],
        "protocol_round": protocol_round,
        "protocol": PROTOCOL,
        "groups": groups,
        "working_advanced_tasks": [
            tid for tid, group in groups.items() if group["working_k"] is not None
        ],
        "champion_advanced_tasks": [
            tid for tid, group in groups.items() if group["champion_k"] is not None
        ],
        "training_required_tasks": triggered_tasks,
    }
    (round_dir / "round_summary.json").write_text(json.dumps(summary, indent=2))

    if triggered_tasks:
        policy_batch: List[Dict[str, Any]] = []
        pending_counts: Dict[str, int] = {}
        for tid in triggered_tasks:
            controller = tasks_state[tid]["controller"]
            pending = list(controller["pending_examples"])
            replay = list(controller["replay_examples"])
            pending_counts[tid] = len(pending)
            policy_batch.extend(_balanced_replay(pending, replay))
        batch_path = round_dir / "adaptive_train_batch.jsonl"
        _append_jsonl(batch_path, policy_batch)
        batch_digest = hashlib.sha256(batch_path.read_bytes()).hexdigest()
        manifest = {
            "schema": "sah.adaptive-v1-training-manifest/1",
            "round": int(meta["round"]),
            "protocol_round": protocol_round,
            "state_path": str(state_path),
            "batch_path": str(batch_path),
            "batch_sha256": batch_digest,
            "tasks": triggered_tasks,
            "pending_counts": pending_counts,
            "status": "pending_training",
        }
        (round_dir / "adaptive_train_manifest.json").write_text(
            json.dumps(manifest, indent=2)
        )
        state["pending_training"] = {
            "manifest_path": str(round_dir / "adaptive_train_manifest.json"),
            "batch_sha256": batch_digest,
            "round": int(meta["round"]),
            "protocol_round": protocol_round,
            "tasks": triggered_tasks,
        }
    _atomic_write_json(state_path, state)
    print(
        f"[adaptive_v1:collect] {len(current_round_rows)} current rows | "
        f"training_required={triggered_tasks} -> {round_dir}"
    )


def commit_update(
    *,
    state_path: Path,
    manifest_path: Path,
    adapter_path: str,
    checkpoint_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Atomically mark a successfully trained proposer update.

    Collection never claims an update before the external SAH trainer and merge
    succeed.  This explicit commit makes interrupted campaigns resumable.
    """
    state = load_state(state_path)
    manifest = json.loads(Path(manifest_path).read_text())
    if manifest.get("schema") != "sah.adaptive-v1-training-manifest/1":
        raise ValueError("unsupported Adaptive training manifest schema")
    batch_path = Path(manifest["batch_path"])
    actual = hashlib.sha256(batch_path.read_bytes()).hexdigest()
    if actual != manifest["batch_sha256"]:
        raise ValueError("Adaptive training batch digest mismatch")
    committed = list(state.get("committed_batches") or [])
    if actual in committed:
        pending = state.get("pending_training")
        if (
            isinstance(pending, Mapping)
            and pending.get("batch_sha256") != actual
        ):
            raise ValueError(
                "Adaptive stale commit cannot clear a different pending "
                "training update"
            )
        active = dict(state.get("active_adapter") or {})
        if (
            not active.get("path")
            or active.get("batch_sha256") != actual
        ):
            raise ValueError(
                "Adaptive committed batch no longer matches the active "
                "adapter; refusing to rewrite stale manifest provenance"
            )
        active_path = Path(str(active["path"]))
        active_digest = _adapter_safetensors_hash(active_path)
        if (
            active.get("safetensors_sha256")
            and active["safetensors_sha256"] != active_digest
        ):
            raise ValueError(
                "Adaptive committed adapter safetensors digest mismatch"
            )
        state_changed = False
        if not active.get("safetensors_sha256"):
            active["safetensors_sha256"] = active_digest
            state["active_adapter"] = active
            state_changed = True
        if isinstance(pending, Mapping):
            state["pending_training"] = None
            state_changed = True
        if state_changed:
            _atomic_write_json(Path(state_path), state)
        if (
            manifest.get("status") != "committed"
            or not manifest.get("adapter_safetensors_sha256")
        ):
            manifest["status"] = "committed"
            manifest["adapter_path"] = active.get("path", adapter_path)
            manifest["adapter_safetensors_sha256"] = active_digest
            manifest["checkpoint_path"] = active.get(
                "checkpoint_path", checkpoint_path
            )
            _atomic_write_json(Path(manifest_path), manifest)
        return state
    pending = state.get("pending_training")
    if not isinstance(pending, Mapping):
        raise ValueError("Adaptive state has no pending training update")
    if pending.get("batch_sha256") != actual:
        raise ValueError("Adaptive pending-training digest mismatch")
    if Path(str(pending.get("manifest_path", ""))).resolve() != Path(
        manifest_path
    ).resolve():
        raise ValueError("Adaptive pending-training manifest mismatch")
    adapter = Path(adapter_path)
    if not adapter.is_dir():
        raise ValueError(
            f"Adaptive adapter path has no local safetensors: {adapter}"
        )
    adapter_digest = _adapter_safetensors_hash(adapter)
    if checkpoint_path is not None and not Path(checkpoint_path).exists():
        raise ValueError(
            f"Adaptive checkpoint path does not exist: {checkpoint_path}"
        )
    if Path(manifest["state_path"]).resolve() != Path(state_path).resolve():
        raise ValueError("Adaptive training manifest targets a different state file")
    tasks = dict(state.get("tasks") or {})
    for tid in manifest["tasks"]:
        task_state = dict(tasks[tid])
        controller = dict(task_state["controller"])
        pending = list(controller.get("pending_examples") or [])
        expected_pending = int((manifest.get("pending_counts") or {}).get(tid, -1))
        if expected_pending != len(pending):
            raise ValueError(
                f"Adaptive pending batch is stale for {tid}: "
                f"expected {expected_pending}, found {len(pending)}"
            )
        replay = list(controller.get("replay_examples") or [])
        replay.extend(pending)
        history = list(controller.get("training_history") or [])
        if history:
            history[-1] = {
                **dict(history[-1]),
                "decision": "trained",
                "training_batch": actual,
                "adapter_path": adapter_path,
                "pending_examples_before_training": len(pending),
                "pending_examples_after_training": 0,
            }
        task_state["controller"] = {
            **controller,
            "pending_examples": [],
            "replay_examples": replay[-256:],
            "policy_updates": int(controller.get("policy_updates", 0)) + 1,
            "rounds_since_confirmed_record": 0,
            "last_training_decision": "trained",
            "training_history": history,
        }
        tasks[tid] = task_state
    state["tasks"] = tasks
    state["active_adapter"] = {
        "path": adapter_path,
        "checkpoint_path": checkpoint_path,
        "safetensors_sha256": adapter_digest,
        "batch_sha256": actual,
        "round": manifest["round"],
    }
    state["pending_training"] = None
    state["committed_batches"] = [*committed, actual]
    _atomic_write_json(Path(state_path), state)
    manifest["status"] = "committed"
    manifest["adapter_path"] = adapter_path
    manifest["adapter_safetensors_sha256"] = adapter_digest
    manifest["checkpoint_path"] = checkpoint_path
    _atomic_write_json(Path(manifest_path), manifest)
    return state


def campaign_status(*, state_path: Path, task_id: str) -> Dict[str, Any]:
    """Return the authoritative resume inputs for one Adaptive campaign."""
    state = load_state(state_path)
    task = dict((state.get("tasks") or {}).get(task_id) or {})
    collected = sorted({int(item) for item in task.get("collected_rounds", [])})
    if collected and collected != list(range(collected[-1] + 1)):
        raise ValueError(
            f"non-contiguous collected rounds for {task_id}: {collected}"
        )
    working = dict(task.get("working") or {})
    champion = dict(task.get("champion") or {})
    active = dict(state.get("active_adapter") or {})
    if active:
        active_path = Path(str(active.get("path") or ""))
        active_digest = _adapter_safetensors_hash(active_path)
        recorded_digest = active.get("safetensors_sha256")
        if recorded_digest and recorded_digest != active_digest:
            raise ValueError(
                "Adaptive active adapter safetensors digest mismatch"
            )
        active["safetensors_sha256"] = active_digest
    controller = dict(task.get("controller") or {})
    return {
        "schema": "sah.adaptive-v1-campaign-status/1",
        "state_path": str(Path(state_path)),
        "task_id": task_id,
        "next_protocol_round": collected[-1] + 1 if collected else 0,
        "collected_rounds": collected,
        "working": working or None,
        "champion": champion or None,
        "controller": {
            "rounds_seen": int(controller.get("rounds_seen", 0)),
            "rounds_since_confirmed_record": int(
                controller.get("rounds_since_confirmed_record", 0)
            ),
            "confirmed_record": controller.get("confirmed_record"),
            "last_training_decision": controller.get(
                "last_training_decision"
            ),
        },
        "active_adapter": active or None,
        "pending_training": state.get("pending_training"),
        "policy_updates": int(controller.get("policy_updates", 0)),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    commit = sub.add_parser("commit-update")
    commit.add_argument("--state", required=True)
    commit.add_argument("--manifest", required=True)
    commit.add_argument("--adapter", required=True)
    commit.add_argument("--checkpoint", default=None)
    status = sub.add_parser("campaign-status")
    status.add_argument("--state", required=True)
    status.add_argument("--task", required=True)
    plan = sub.add_parser("rollout-plan")
    plan.add_argument("--round-dir", required=True)
    plan.add_argument("--outcome-repeats", required=True, type=int)
    plan.add_argument("--promotion-repeats", required=True, type=int)
    plan.add_argument("--seed-base", required=True, type=int)
    plan.add_argument("--eval-timeout-seconds", required=True, type=int)
    args = parser.parse_args()
    if args.command == "commit-update":
        state = commit_update(
            state_path=Path(args.state),
            manifest_path=Path(args.manifest),
            adapter_path=args.adapter,
            checkpoint_path=args.checkpoint,
        )
        print(
            json.dumps(
                {
                    "status": "committed",
                    "active_adapter": state.get("active_adapter"),
                }
            )
        )
    elif args.command == "campaign-status":
        print(
            json.dumps(
                campaign_status(
                    state_path=Path(args.state),
                    task_id=args.task,
                )
            )
        )
    elif args.command == "rollout-plan":
        payload = write_rollout_plan(
            Path(args.round_dir),
            outcome_repeats=args.outcome_repeats,
            promotion_repeats=args.promotion_repeats,
            seed_base=args.seed_base,
            eval_timeout_seconds=args.eval_timeout_seconds,
        )
        print("\n".join(rollout_plan_shell_rows(payload)))


if __name__ == "__main__":
    main()
