---
name: discovery-optimization
description: "Replace multi-restart optimization with simpler gradient descent and more restarts."
---

# Simple Gradient Descent for Erdos C5

## Strategy
Make targeted hyperparameter changes to enable more diverse restarts.

## Required Changes
1. num_intervals: 800 -> 200 (faster, sufficient resolution)
2. base_learning_rate: 0.004 -> 0.001 (more stable)
3. num_steps: 120000 -> 50000 (focus on quality)
4. penalty_strength: 61.0 -> 30.0 (less constraint, more exploration)
5. num_restarts: 3 -> 5 (more trials)

## Process
1. Find the Hyperparameters dataclass in the EVOLVE-BLOCK
2. Replace each value with the new value above using SEARCH/REPLACE
3. Ensure the optimizer loop uses updated parameters
4. Edit and evaluate

## Why This Works
- More restarts (5 vs 3) increases chance of finding good initialization
- Lower learning rate avoids divergence
- Fewer steps but more restarts trades speed for diversity
- Lower penalty allows optimizer to explore more freely
