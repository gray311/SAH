---
name: discovery-optimization
description: "Hyperparameter tuning for Erdos optimizer. The seed already has 15 diverse patterns. Instead of screening patterns, tune the optimizer itself by varying learning rate, penalty strength, interval count, and restarts."
---

# Hyperparameter Tuning Strategy

## Problem
The seed optimizer uses fixed hyperparameters (lr=0.006, penalty=60, intervals=800, restarts=3). These might not be optimal.

## Solution: hyperparameter_sweep Tool

This tool tests 9 configurations by varying:
- num_intervals: 200, 400, 800 (coarseness affects FFT accuracy)
- base_learning_rate: 0.001, 0.006, 0.02 (step size)
- penalty_strength: 30, 60, 120 (constraint enforcement)

## Workflow

1. CALL hyperparameter_sweep (no args, uses sensible defaults)

2. EXAMINE results: each config has analytical c5_estimate based on a quick run

3. PICK the config with lowest c5_estimate that also has reasonable setup

4. CALL edit_solution to update the seed program with winning hyperparameters

5. CALL evaluate_solution ONCE with the tuned config

## Why This Beats Pattern Screening

- Seed already tries 15 patterns - we do not need more candidates
- Hyperparameter tuning directly improves the optimizer's quality
- 9 configs gives diverse coverage of the hyperparameter space
- One evaluation at a time keeps budget efficient

## Expected Results

With tuned hyperparameters, you should find c5_bound < 0.38 (combined_score > 1.0).
