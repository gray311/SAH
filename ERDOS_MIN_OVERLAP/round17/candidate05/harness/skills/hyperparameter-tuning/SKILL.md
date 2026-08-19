---
name: hyperparameter-tuning
description: Use search_hyperparams to tune optimizer hyperparameters with analytical screening.
---

# Hyperparameter Tuning for Erdos Problem

## Workflow

1. CALL search_hyperparams (no args)

2. EXAMINE the 5 returned configs:
   - Each has precomputed c5_estimate
   - Configs vary: intervals (400-1200), learning_rate (0.001-0.02), penalty (10-200)

3. FILTER configs:
   - KEEP if c5_estimate < 0.385 (training can improve further)
   - Prioritize lower c5_estimate

4. CALL evaluate_solution on ALL kept configs

5. If no improvement after 2-3 evals, MODIFY ONE hyperparameter:
   - Increase penalty_strength by 50%
   - Decrease learning_rate by 50%
   - Increase num_intervals by 50%

## Why This Works

- Grid search: covers key hyperparameter space
- Analytical screening: cheap c5 estimates
- Training can improve: c5_estimate is just initialization score
- Focused search: 5 configs, 2-5 evals max

## Example

Config 1: penalty=120, c5=0.378 -> EVALUATE (promising)
Config 2: intervals=400, c5=0.379 -> EVALUATE (promising)
Config 3: penalty=30, c5=0.381 -> SKIP (close to seed)
