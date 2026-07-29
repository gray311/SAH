"""Rewards + GRPO advantages, instance-wise (plan.md §2.2, §8.3).

Per task instance tau, K candidates were generated FOR tau and each rolled out
once on tau. Reward vs tau's current-best-harness score:

    r = clip((score - base_score) / (|base_score| + eps), -1, 1)

Failed/absent rollouts score 0 -> r = -1 after clipping; an INVALID candidate
(no submission / schema failure / duplicate) gets the fixed INVALID_REWARD.
The GRPO group = the K candidates of ONE task:

    A_k = (r_k - mean_group) / (std_group + eps)

Group-relative normalization within the task removes cross-task scale entirely.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

EPS = 1e-9
INVALID_REWARD = -1.0
# Asymmetric clip: relative gain is naturally bounded below by -1 (scores >= 0);
# the upper bound must NOT flatten winner ordering (step-3 lesson: 0.37/0.42/0.51
# on a 0.14 base all clipped to +1 and got identical advantages).
CLIP_LOW, CLIP_HIGH = -1.0, 5.0


def task_reward(score: Optional[float], base_score: float) -> float:
    if score is None:
        score = 0.0
    r = (score - base_score) / (abs(base_score) + EPS)
    return max(CLIP_LOW, min(CLIP_HIGH, r))


def load_rollout_score(rollout_dir: Path, task_id: str) -> Optional[float]:
    """Best score for ``task_id`` from a candidate's run_baseline output
    (final summary preferred; wall-safe checkpoint as fallback)."""
    best: Optional[float] = None
    for summ in rollout_dir.glob("*/summary.json"):
        try:
            for row in json.loads(summ.read_text()):
                if row.get("task_id") == task_id and row.get("best_score") is not None:
                    s = float(row["best_score"])
                    best = s if best is None else max(best, s)
        except Exception:
            pass
    if best is None:
        for ck in rollout_dir.glob(f"*/checkpoints/{task_id}.json"):
            try:
                s = float(json.loads(ck.read_text()).get("best_score", 0.0))
                best = s if best is None else max(best, s)
            except Exception:
                pass
    return best


def compute_task_group(
    *, task_id: str, candidates: List[Dict[str, Any]], rollout_root: Path,
    base_score: float,
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for cand in candidates:
        k = cand["k"]
        if not cand.get("valid"):
            score, reward = None, INVALID_REWARD
        else:
            score = load_rollout_score(rollout_root / task_id / f"cand{k:02d}", task_id)
            reward = task_reward(score, base_score)
        rows.append({"k": k, "valid": bool(cand.get("valid")), "score": score,
                     "reward": reward, "spec_hash": cand.get("spec_hash", ""),
                     "changed_fields": cand.get("changed_fields", [])})

    rewards = [r["reward"] for r in rows]
    mean = sum(rewards) / len(rewards)
    std = math.sqrt(sum((x - mean) ** 2 for x in rewards) / len(rewards))
    for r in rows:
        r["advantage"] = (r["reward"] - mean) / (std + EPS)

    valid = [r for r in rows if r["valid"] and r["score"] is not None]
    best = max(valid, key=lambda r: r["score"]) if valid else None
    return {"task_id": task_id, "base_score": base_score,
            "reward_mean": mean, "reward_std": std, "rows": rows,
            "best_k": best["k"] if best else None,
            "best_score": best["score"] if best else None,
            "improved": bool(best and best["score"] > base_score)}

# --------------------------------------------------------------------------- #
# v2 discovery-oriented rewards/advantages (2026-07-24 algorithm exploration)
#
# Motivations, each backed by campaign evidence:
#   1. GAP-NORMALIZED REWARD  — near saturation the relative-gain reward
#      vanishes (round019 AC1: +0.0001-level rewards) and GRPO's std division
#      inflates that noise into +/-2.6 advantages. Reward becomes "fraction of
#      the remaining gap to the task ceiling closed":  r = (s-b)/(ceil-b).
#   2. RLOO BASELINE, NO STD DIVISION — leave-one-out mean is unbiased at
#      small K and stops noise amplification.
#   3. MAX-WEIGHTED SHARPENING — discovery banks best-of-K, not the mean.
#      A = alpha*(softmax(r/tau) - 1/K) + (1-alpha)*A_rloo  approximates a
#      risk-seeking / E[max] gradient while retaining a stable mean term.
#   4. ZERO-SIGNAL FILTER — groups whose valid rewards are all identical
#      (round014 llm_sql: eight 0.0934s) carry only "submit anything valid"
#      pressure, which is drift fuel; their advantages are zeroed so the
#      training step skips them.
# --------------------------------------------------------------------------- #

def task_reward_v2(score: Optional[float], base_score: float,
                   ceiling: Optional[float]) -> float:
    if score is None:
        score = 0.0
    if ceiling is not None and ceiling > base_score + EPS:
        r = (score - base_score) / (ceiling - base_score)
        # soft cap: bounded ~3 but strictly monotonic, so two above-ceiling
        # candidates keep their ordering (hard clip made r020 cand0/cand4 tie)
        return 3.0 * math.tanh(r / 3.0) if r > 0 else max(-1.0, r)
    return task_reward(score, base_score)


def _rloo(rewards: List[float]) -> List[float]:
    n = len(rewards)
    if n < 2:
        return [0.0 for _ in rewards]
    tot = sum(rewards)
    return [r - (tot - r) / (n - 1) for r in rewards]


def _max_weights(rewards: List[float], tau: float) -> List[float]:
    m = max(rewards)
    exps = [math.exp((r - m) / max(tau, EPS)) for r in rewards]
    z = sum(exps)
    n = len(rewards)
    return [e / z - 1.0 / n for e in exps]


def compute_task_group_v2(
    *, task_id: str, candidates: List[Dict[str, Any]], rollout_root: Path,
    base_score: float, ceiling: Optional[float] = None,
    sharpen_alpha: float = 0.3, zero_range_eps: float = 1e-3,
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for cand in candidates:
        k = cand["k"]
        if not cand.get("valid"):
            score, reward = None, INVALID_REWARD
        else:
            score = load_rollout_score(rollout_root / task_id / f"cand{k:02d}", task_id)
            reward = task_reward_v2(score, base_score, ceiling)
        rows.append({"k": k, "valid": bool(cand.get("valid")), "score": score,
                     "reward": reward, "spec_hash": cand.get("spec_hash", ""),
                     "changed_fields": cand.get("changed_fields", [])})

    valid_rewards = [r["reward"] for r in rows if r["valid"]]
    rng = (max(valid_rewards) - min(valid_rewards)) if valid_rewards else 0.0
    all_valid = all(r["valid"] for r in rows)
    no_signal = all_valid and rng < zero_range_eps
    if valid_rewards and rng < zero_range_eps and not all_valid:
        # valids are effectively tied: collapse their micro-differences so the
        # only surviving signal is valid-vs-invalid (no fake ordering from 1e-6
        # score noise — the r014 llm_sql pathology)
        vm = sum(valid_rewards) / len(valid_rewards)
        for r in rows:
            if r["valid"]:
                r["reward"] = vm
    rewards = [r["reward"] for r in rows]

    if no_signal:
        for r in rows:
            r["advantage"] = 0.0
    else:
        base_adv = _rloo(rewards)
        tau = max(rng / 4.0, 1e-6)
        mw = _max_weights(rewards, tau)
        for r, a, w in zip(rows, base_adv, mw):
            r["advantage"] = (1.0 - sharpen_alpha) * a + sharpen_alpha * w

    mean = sum(rewards) / len(rewards)
    std = math.sqrt(sum((x - mean) ** 2 for x in rewards) / len(rewards))
    valid = [r for r in rows if r["valid"] and r["score"] is not None]
    best = max(valid, key=lambda r: r["score"]) if valid else None
    return {"task_id": task_id, "base_score": base_score, "ceiling": ceiling,
            "reward_mean": mean, "reward_std": std, "rows": rows,
            "adv_mode": "no_signal" if no_signal else f"rloo+max(a={sharpen_alpha})",
            "best_k": best["k"] if best else None,
            "best_score": best["score"] if best else None,
            "improved": bool(best and best["score"] > base_score)}


def compute_task_group_v3(
    *, task_id: str, candidates: List[Dict[str, Any]], rollout_root: Path,
    base_score: float, ceiling: Optional[float] = None,
    sharpen_alpha: float = 0.3, zero_range_eps: float = 1e-3,
    hist_lambda: float = 0.3,
) -> Dict[str, Any]:
    """v2 + HISTORICAL-FRONTIER RESCUE (the '历史 trajectory reward 对比' idea).

    v2 zeros a group whenever its K valid rewards are tied within
    ``zero_range_eps`` (no within-group signal). But ``base_score`` IS the
    historical frontier (the ratchet best), so a tied batch that sits UNIFORMLY
    above/below the frontier still carries a real cross-round signal that v2
    throws away. Empirically (AC1) that discards genuine gains — e.g. a round
    where all 8 candidates beat base by 20%% of the gap was zeroed.

    Rescue: for an off-frontier tied group, give a uniform directional advantage
    ``hist_lambda * softcap(vm)`` where ``vm`` is the shared gap-normalized
    reward vs base (>0 batch beat the frontier -> reinforce this phi; <0 ->
    discourage). A truly-plateaued group (vm ~ 0, batch reproduced the frontier
    program) still gets 0 — no signal can be manufactured from zero variance;
    that regime needs exploration (higher K/temperature), not a baseline.

    Only the previously-zeroed rounds change; groups with within-group signal are
    byte-identical to v2. Still fully on-policy: the historical frontier only
    sets the baseline/magnitude; we never backprop through past trajectories.
    """
    g = compute_task_group_v2(
        task_id=task_id, candidates=candidates, rollout_root=rollout_root,
        base_score=base_score, ceiling=ceiling, sharpen_alpha=sharpen_alpha,
        zero_range_eps=zero_range_eps)
    if g["adv_mode"] != "no_signal":
        return g  # within-group signal present -> identical to v2
    valid_rewards = [r["reward"] for r in g["rows"] if r["valid"]]
    vm = sum(valid_rewards) / len(valid_rewards) if valid_rewards else 0.0
    if abs(vm) < zero_range_eps:
        g["adv_mode"] = "no_signal(true-plateau)"        # genuinely nothing to learn
        return g
    nudge = hist_lambda * (3.0 * math.tanh(vm / 3.0))    # bounded, monotonic in vm
    for r in g["rows"]:
        r["advantage"] = nudge if r["valid"] else INVALID_REWARD
    g["adv_mode"] = f"hist_rescue(vm={vm:+.3f},lam={hist_lambda})"
    return g


def _rms_normalize(values: List[float]) -> List[float]:
    if not values:
        return values
    rms = math.sqrt(sum(v * v for v in values) / len(values))
    return [v / rms for v in values] if rms > EPS else list(values)


def compute_task_group_anchored(
    *, task_id: str, candidates: List[Dict[str, Any]], rollout_root: Path,
    base_score: float, ceiling: Optional[float] = None, **_ignored: Any,
) -> Dict[str, Any]:
    """Adaptive-ported anchored signed credit (reward.impl=anchored).

    Per candidate the raw advantage is a bounded blend
        0.70*tanh(delta/0.25) + 0.20*rank_term + 0.30*record_bonus
    where delta = gap-normalized gain vs base, rank_term is the within-group
    rank in [-1,1], and record_bonus fires only on a genuine new record. Signs
    are locked (valid positive delta >= +0.05, negative <= -0.05, invalid <=
    -1, behavior-equivalent = 0) so a high raw score that regressed against its
    matched parent can never read as a gain. Advantages are RMS-normalized
    across the group. Validity-gated best selection is inherited from the same
    load_rollout_score path the other impls use.
    """
    rows: List[Dict[str, Any]] = []
    for cand in candidates:
        k = cand["k"]
        valid = bool(cand.get("valid"))
        score = (load_rollout_score(rollout_root / task_id / f"cand{k:02d}", task_id)
                 if valid else None)
        rows.append({"k": k, "valid": valid, "score": score,
                     "spec_hash": cand.get("spec_hash", ""),
                     "changed_fields": cand.get("changed_fields", [])})

    denom = (ceiling - base_score) if (ceiling is not None and ceiling > base_score + EPS) \
        else (abs(base_score) + EPS)
    valid_scores = [r["score"] for r in rows if r["valid"] and r["score"] is not None]
    ranked = sorted(valid_scores)
    raw: List[float] = []
    for r in rows:
        if not r["valid"] or r["score"] is None:
            raw.append(-1.0)
            r["reward"] = INVALID_REWARD
            continue
        delta = (r["score"] - base_score) / denom
        hard_zero = abs(delta) <= EPS
        anchor = math.tanh(delta / 0.25)
        rank = (ranked.index(r["score"]) / max(1, len(ranked) - 1)) * 2 - 1 if len(ranked) > 1 else 0.0
        is_record = r["score"] > base_score + EPS and r["score"] >= max(valid_scores)
        record_bonus = math.tanh(max(0.0, delta) / 0.05) if is_record else 0.0
        value = 0.70 * anchor + 0.20 * rank + 0.30 * record_bonus
        if hard_zero:
            value = 0.0
        elif delta > 0.0:
            value = max(value, 0.05)
        elif delta < 0.0:
            value = min(value, -0.05)
        raw.append(value)
        r["reward"] = delta
    for r, adv in zip(rows, _rms_normalize(raw)):
        r["advantage"] = adv

    valid = [r for r in rows if r["valid"] and r["score"] is not None]
    best = max(valid, key=lambda r: r["score"]) if valid else None
    return {"task_id": task_id, "base_score": base_score, "ceiling": ceiling,
            "reward_mean": sum(r["reward"] for r in rows) / len(rows),
            "reward_std": 0.0, "rows": rows, "adv_mode": "anchored",
            "best_k": best["k"] if best else None,
            "best_score": best["score"] if best else None,
            "improved": bool(best and best["score"] > base_score)}
