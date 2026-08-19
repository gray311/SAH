---
name: discovery-optimization
description: "Systematically search for better optimizer hyperparameters using probe screening."
---

# Hyperparameter Search Strategy for Erdos Optimizer

## Problem
The seed optimizer already has good initialization diversity (12 patterns) and multi-restart strategy.
Improvements come from better optimizer settings, not changing the search strategy.

## Workflow

### Phase 1: Probe-Based Hyperparameter Screening

Create EDIT versions of the seed with different hyperparameters:

- **penalty_strength**: Critical! Try values from 5 to 200
  - Too low (5-10): constraint violation
  - Too high (100+): slow convergence, over-penalized
  - Optimal likely in 20-80 range

- **num_intervals**: Finer discretization = more accurate c5_bound
  - Try 200, 400, 600, 800, 1200, 1600
  - More intervals = better but slower

- **num_steps**: More optimization steps = better convergence
  - Try 10000, 20000, 50000, 100000, 200000
  - Diminishing returns after 100k steps

- **base_learning_rate**: Try 0.001, 0.003, 0.005, 0.007, 0.01, 0.02

### Phase 2: Probe Screening

For each hyperparameter combination:
1. EDIT the seed to only change those hyperparameters
2. Call probe_solution immediately (don't run full training)
3. Check: c5_bound from probe < 0.375

### Phase 3: Full Evaluation

Call evaluate_solution on top 3-5 candidates from Phase 2.

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Most promising: c5_bound < 0.35

## Tip
The penalty_strength is the most important hyperparameter. Start by trying values 20, 40, 61, 80, 100 with num_steps=59000 and num_intervals=800.
