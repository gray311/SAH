---
name: hyper-parameter-exploration
description: Explore diverse hyperparameter configurations while preserving multi-restart diversity. Screen with probes.
---

# Hyperparameter Exploration Strategy

## Key Principle
The seed's 12 initialization patterns are excellent. Don't replace them.
Instead, explore different hyperparameter settings.

## Workflow
1. Call generate_hyper_diversity to get 6 hyperparameter configs
2. For each config, EDIT ONLY the Hyperparameters dataclass
3. CRITICAL: Keep num_restarts=3 (or at least 1) to maintain diversity
4. Call probe_solution to check c5_bound < 0.37
5. Call evaluate_solution only on top 2-3 probe-passing configs
6. If no success, change num_intervals dramatically

## Why This Works
- Different discretization scales (400 vs 1600 intervals) capture different function shapes
- Different learning rates help escape shallow local minima
- Different penalty strengths balance constraint satisfaction vs objective
- Probes let you screen 20+ configs with the 30-probe budget
