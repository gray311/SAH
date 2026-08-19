---
name: hyperparameter-search
description: Systematically explore hyperparameter space for the Erdos optimizer. Focus on - num_intervals, learning_rate, penalty_strength, num_steps, num_restarts.
---

# Hyperparameter Search Strategy

## Problem
The seed optimizer (59k steps, 3 restarts) is expensive. We need to find better
hyperparameters that give lower c5_bound with the same budget.

## Key Hyperparameters to Tune:

1. **num_intervals**: Current=800. Try 1000-1200 for better FFT accuracy.
   Finer discretization may capture the optimal h(x) shape better.

2. **learning_rate**: Current=0.0062. Try 0.004 (more precise) or 0.01 (faster).
   Lower LR may find better minima.

3. **penalty_strength**: Current=61.0. Try 80-120 for stronger constraint.
   Stronger penalty ensures integral(h)=1 more strictly.

4. **num_steps**: Current=59000. Try 30000-40000 for faster iterations.
   More iterations per eval = more evals used, but each eval is faster.

5. **num_restarts**: Current=3. Try 5-7 for more diverse solutions.

## Workflow:

1. Generate 5-10 candidates with generate_10_candidates

2. Probe with probe_solution, rank by c5_bound

3. Evaluate top 2-3 with lowest c5_bound

4. If no improvement, call analyze_results with current_best_score

5. Apply suggested mutations to create new candidate set

6. Repeat until eval budget exhausted or c5_bound < 0.380923

## Expected Outcome:

Find a combination of hyperparameters that gives c5_bound significantly
below 0.380923, beating the current best.
