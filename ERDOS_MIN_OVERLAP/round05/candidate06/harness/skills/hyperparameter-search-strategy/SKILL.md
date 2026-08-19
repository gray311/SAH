---
name: hyperparameter-search-strategy
description: Specialized playbook for hyperparameter-heavy continuous optimization. Focuses on probe-first evaluation and systematic hyperparameter exploration.
---

# Hyperparameter Search Strategy for Optimization Tasks

## Core Principle: Quality Over Quantity
You have exactly 30 full evaluations. Each must count. Use probes to filter out bad ideas early.

## Step-by-Step Method

### 1. Establish Baseline
- Check best_so_far score
- Note current hyperparameters
- If combined_score ≤ 1.0, you need substantive improvements

### 2. Single-Parameter Exploration
Change only ONE hyperparameter at a time:\n      - penalty_strength: Try [500, 1000, 2000, 5000] in sequence\n      - base_learning_rate: Try [0.001, 0.005, 0.01, 0.05]\n      - num_intervals: Try [400, 800, 1600, 3200]\n      - optimizer: Adam → AdamW → rmsprop\n      - num_restarts: Try [1, 5, 10]\n      
### 3. Probe-Based Ranking
After each edit:\n      - Call probe_solution IMMEDIATELY\n      - Compare probe score to best_so_far\n      - If probe is worse, abandon this direction (save an eval!)\n      - If probe is better, consider 1 more probe, then evaluate\n      
### 4. Full Evaluation Criteria\n      Call evaluate_solution only when:\n      - Probe shows consistent improvement\n      - You've tested at least 2 variants showing probe improvement\n      - You have ≥5 evals remaining\n      - You want to confirm a direction before committing

### 5. Convergence Detection\n      If probes show no improvement for 2 consecutive variants:\n      - Stop down this path\n      - Try a completely different hyperparameter direction\n      - Consider structural changes (different algorithm, not just params)\n      
## Red Flags (Stop and Reassess)\n      - validity = 0: Constraint violated (integral ≠ 1.0)\n      - probe scores consistently lower: Wrong direction\n      - evals_left < 5 with no improvement: May need bigger changes\n      
## Winning Patterns Observed
- Moderate penalty (1000-2000) with AdamW + LR scheduling\n      - Higher num_intervals (1600-3200) for finer function resolution\n      - Structured initializations that respect constraints by design
