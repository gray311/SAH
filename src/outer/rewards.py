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
