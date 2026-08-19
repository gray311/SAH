---
name: discovery-optimization
description: "Hyperparameter tuning: test configs with search_hyperparams tool, filter by c5_estimate < 0.385, then evaluate."
---

# Hyperparameter Tuning Strategy
## Problem The seed optimizer trains for 59000 steps. Small hyperparameter changes can lead to large improvements.
## Solution: search_hyperparams Tool
This tool generates 5 configs with varied hyperparameters: - num_intervals: 400-1200 (coarser to finer) - learning_rate: 0.001-0.02 (slower to faster) - penalty_strength: 10-200 (sharper to smoother)
Each has precomputed c5_estimate.
## Workflow
1. CALL search_hyperparams
2. FILTER configs: - Keep if c5_estimate < 0.385 - Prioritize lower c5_estimate
3. CALL evaluate_solution on all kept configs
4. If no improvement, MODIFY ONE hyperparameter in failed configs: - Increase penalty_strength by 50% - Decrease learning_rate by 50% - Increase num_intervals by 50%
5. Re-run search_hyperparams with new configs
## Example
Config 1: penalty=120, c5=0.378 -> EVALUATE Config 2: intervals=400, c5=0.379 -> EVALUATE Config 3: penalty=30, c5=0.381 -> SKIP (too close to current best)
