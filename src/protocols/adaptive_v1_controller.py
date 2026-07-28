"""Adaptive v1 rollout assessment, dual frontiers, and training controller."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
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


@dataclass(frozen=True)
class RolloutSamples:
    scores: tuple[float, ...]
    program_digests: tuple[str, ...]

    @property
    def mean(self) -> Optional[float]:
        return sum(self.scores) / len(self.scores) if self.scores else None

    @property
    def sem(self) -> Optional[float]:
        if len(self.scores) < 2:
            return 0.0 if self.scores else None
        return statistics.stdev(self.scores) / math.sqrt(len(self.scores))


def load_rollout_samples(root: Path, task_id: str) -> RolloutSamples:
    rows: List[tuple[str, float, str]] = []
    root = Path(root)
    for summary in sorted(root.rglob("summary.json")) if root.exists() else []:
        try:
            for row in json.loads(summary.read_text()):
                if row.get("task_id") != task_id or row.get("best_score") is None:
                    continue
                result_file = summary.parent / "results" / f"{task_id}.json"
                digest = ""
                if result_file.exists():
                    result = json.loads(result_file.read_text())
                    program = result.get("best_program")
                    if isinstance(program, str):
                        digest = hashlib.sha256(program.encode()).hexdigest()
                rows.append((str(summary), float(row["best_score"]), digest))
        except Exception:
            continue
    if not rows and root.exists():
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
    )


def load_best_program(root: Path, task_id: str) -> tuple[Optional[str], Optional[float]]:
    best_program: Optional[str] = None
    best_score: Optional[float] = None
    for result_file in sorted(Path(root).rglob(f"results/{task_id}.json")):
        try:
            result = json.loads(result_file.read_text())
            program = result.get("best_program")
            score = result.get("best_score")
            if (
                isinstance(program, str)
                and isinstance(score, (int, float))
                and (best_score is None or float(score) > best_score)
            ):
                best_program = program
                best_score = float(score)
        except Exception:
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
        repairs = int(row.get("unknown_repairs", 0))
        repair_penalty = min(0.10, 0.02 * repairs) if repairs and not hard_zero else 0.0
        value -= repair_penalty
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
                "schema_repair_penalty": repair_penalty,
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
                "response_format": "plain_text",
                "trajectory": [],
                "tools": [],
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
            round_dir / "rollouts" / tid / "base" / "outcome", tid
        )
        if not outcome_base.scores:
            raise ValueError(
                f"missing matched base outcome rollout for {tid}; "
                "Adaptive collection fails closed"
            )
        champion_baseline = load_rollout_samples(
            round_dir / "rollouts" / tid / "champion" / "promotion", tid
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
                load_rollout_samples(outcome_root, tid)
                if candidate.get("valid")
                else RolloutSamples((), ())
            )
            promotion = load_rollout_samples(
                round_dir / "rollouts" / tid / f"cand{k:02d}" / "promotion", tid
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
            unknown_repairs = len(candidate.get("dropped_unknown_action_fields") or [])
            unknown_repairs += sum(
                len(items)
                for items in (
                    candidate.get("dropped_unknown_edit_atom_fields") or {}
                ).values()
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
                    "confirmed_parent_progress": confirmed_parent,
                    "promotion_score": promotion.mean,
                    "promotion_samples": list(promotion.scores),
                    "promotion_sem": promotion.sem,
                    "spec_hash": candidate.get("spec_hash", ""),
                    "changed_fields": candidate.get("changed_fields", []),
                    "action": candidate.get("action"),
                    "unknown_repairs": unknown_repairs,
                    "system": trajectory.get("system", PROPOSER_SYSTEM_PROMPT),
                    "user": trajectory.get("user", ""),
                    "response": trajectory.get(
                        "training_response", trajectory.get("raw_submission", "")
                    ),
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
                margin = confidence_z * math.sqrt(
                    float(row["promotion_sem"] or 0.0) ** 2
                    + float(champion_baseline.sem or 0.0) ** 2
                )
                if gain > 0.0 and gain >= margin:
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
            task_state["working"] = dict(next_bases[tid])
        else:
            next_bases[tid] = {
                "package": pt["base_package"],
                "score": pt["base_score"],
                "seed_score": pt["seed_score"],
                "from": "unchanged",
            }
        if champion is not None:
            task_state["champion"] = {
                "package": str(
                    round_dir / "tasks" / tid / f"cand{champion['k']:02d}"
                ),
                "score": champion["promotion_score"],
                "from": f"round{meta['round']:03d}/cand{champion['k']:02d}:champion",
            }

        attempts = list(archive.get("attempts") or [])
        successful = list(archive.get("successful_actions") or [])
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
                "signature": _digest(row["action"]),
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
                "failure_reason": row["failure_reason"],
            }
            attempts.append(attempt)
            if row["valid"] and learning_reward > 0.0:
                successful.append(attempt)
        attempts = attempts[-256:]
        successful = sorted(
            successful[-256:],
            key=lambda item: (
                float(item.get("learning_reward", 0.0)),
                str(item.get("proposal_id", "")),
            ),
        )
        task_state["archive"] = {
            **archive,
            "attempts": attempts,
            "successful_actions": successful,
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
            "base_score": outcome_base.mean,
            "base_score_samples": list(outcome_base.scores),
            "rows": rows,
            "working_k": working["k"] if working else None,
            "working_score": working["score"] if working else None,
            "champion_k": champion["k"] if champion else None,
            "champion_score": champion["promotion_score"] if champion else None,
            "champion_reference_available": champion_reference_available,
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
    batch_path = Path(manifest["batch_path"])
    actual = hashlib.sha256(batch_path.read_bytes()).hexdigest()
    if actual != manifest["batch_sha256"]:
        raise ValueError("Adaptive training batch digest mismatch")
    committed = list(state.get("committed_batches") or [])
    if actual in committed:
        state["pending_training"] = None
        _atomic_write_json(Path(state_path), state)
        if manifest.get("status") != "committed":
            manifest["status"] = "committed"
            manifest["adapter_path"] = (state.get("active_adapter") or {}).get(
                "path", adapter_path
            )
            manifest["checkpoint_path"] = (
                state.get("active_adapter") or {}
            ).get("checkpoint_path", checkpoint_path)
            _atomic_write_json(Path(manifest_path), manifest)
        return state
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
        "batch_sha256": actual,
        "round": manifest["round"],
    }
    state["pending_training"] = None
    state["committed_batches"] = [*committed, actual]
    _atomic_write_json(Path(state_path), state)
    manifest["status"] = "committed"
    manifest["adapter_path"] = adapter_path
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
    active = dict(state.get("active_adapter") or {})
    controller = dict(task.get("controller") or {})
    return {
        "schema": "sah.adaptive-v1-campaign-status/1",
        "state_path": str(Path(state_path)),
        "task_id": task_id,
        "next_protocol_round": collected[-1] + 1 if collected else 0,
        "collected_rounds": collected,
        "working": working or None,
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


if __name__ == "__main__":
    main()
