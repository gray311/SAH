---
name: discovery-optimization
description: "External search optimization for Erdos C5 via high num_restarts.\nStrategy: Set num_restarts >= 10 to explore diverse initializations (matching seed's 15 patterns).\nUse probe for cheap screening before full evals. Focus on num_restarts variation (5,10,15,20)."
---

# Erdos C5 - External Search via High Restarts

## Core Strategy

The seed optimizer has a powerful built-in feature: _get_best_initialization tries 15 pattern
variations analytically and picks the best one BEFORE training starts. The seed uses num_restarts=3.

## Why Previous Harnesses Failed

- They set num_restarts=1, which is WORSE than the seed's 3
- 6/7 harnesses made zero progress
- They wasted evals on incremental hyperparameter tuning instead of leveraging diverse restarts

## Correct Approach

1. SET num_restarts=10 (or higher: 15, 20) to explore MORE diverse initializations
2. Keep num_intervals=800 (seed default works well)
3. Keep penalty_strength=60.0 (strong integral constraint)
4. Keep num_steps=59000 (full training budget)
5. Use probe_solution for cheap c5_bound screening

## Tool Usage

- probe_solution: Call AFTER each edit to get approximate c5_bound. Only proceed if < 0.382.
- evaluate_solution: Only call when probe shows promise (combined_score potential > 1.0)
- edit_solution: Change ONE parameter at a time. Primary target: num_restarts

## Search Sequence

1. Start: num_restarts=10, all other seed defaults
2. If no improvement: try num_restarts=15, 20
3. If still no improvement: vary num_intervals (400, 1600)
4. Finally: vary base_learning_rate (0.005, 0.01)

## Success Criteria

Find c5_bound < 0.38092303510845016 (combined_score > 1.0) using high-num_restarts search.
Key: Diverse restarts > incremental tuning for this problem.
