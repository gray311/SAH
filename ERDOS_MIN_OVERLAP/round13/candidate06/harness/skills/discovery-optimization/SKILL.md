---
name: discovery-optimization
description: "Tune hyperparameters (learning rate, penalty, intervals, steps) and use probes to screen before full evaluation."
---

# Hyperparameter Tuning Strategy for Erdos Optimizer

## Problem
The seed optimizer has 12 good initialization patterns but fixed hyperparameters.

## Strategy

### Phase 1: Hyperparameter Exploration

Edit the EVOLVE-BLOCK Hyperparameters class to try different settings:

- num_intervals: 400, 600, 800, 1000, 1200 (larger = more precise c5 calculation)
- base_learning_rate: 0.001, 0.003, 0.007, 0.01, 0.02 (wider exploration)
- penalty_strength: 10, 30, 61, 100, 200 (adjust constraint enforcement)
- num_steps: 30000, 59000, 80000, 120000 (more iterations for better optimization)
- num_restarts: 1 (use single run with good initialization)

### Phase 2: Screen with Probes (Use All 30 Probes!)

For each hyperparameter change:

1. EDIT the seed to use num_restarts=1, seed_start=0

2. Call probe_solution to check: constraint satisfaction, c5_bound estimate

3. Skip if probe shows constraint violation or c5_bound >= 0.38

4. Keep candidates with c5_bound < 0.37

### Phase 3: Evaluate Promising Candidates

Call evaluate_solution on top 2-3 candidates from Phase 2.

## Why This Works
- The 12 patterns already provide diversity
- Better hyperparameters lead to better convergence
- Probes let you screen hyperparameter combinations quickly
- Focus on actual optimization quality, not new patterns
