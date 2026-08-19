---
name: discovery-optimization
description: "Edit optimizer algorithm structure. Test small changes with probe_solution. Focus on algorithm-level changes (optimizer type, learning schedule, discretization), not pattern variations."
---

# Structural Algorithm Editing Strategy

## Problem
The seed optimizer uses gradient descent with 15 pattern variations but STUCK at seed score.
Adding MORE pattern variations won't help - they all use the same flawed optimization approach.

## Solution: Structural Algorithm Changes

### What to Edit

1. Hyperparameters: Test each one individually with probe:
   - num_intervals: 800 -> 400, 1600 (coarser/finer)
   - base_learning_rate: 0.0062 -> 0.01, 0.001, 0.05
   - penalty_strength: 61.0 -> 100.0, 10.0, 200.0
   - num_restarts: 3 -> 1, 5, 10

2. Optimizer changes: Edit the optimizer class to try:
   - Different optimization algorithms
   - Different initialization strategies
   - Constraint enforcement methods

3. Architecture changes: 
   - Change how h is constructed from latent
   - Modify the correlation computation
   - Add preprocessing/postprocessing steps

### Workflow

1. PROBE one hyperparameter change (e.g., num_intervals=1600)
   - Use probe_solution to test
   - Check if c5_bound changes from seed value

2. If probe shows improvement: EDIT the program to make that change permanent

3. If probe shows no change: EDIT a different hyperparameter

4. If all hyperparams fail: EDIT the optimizer class structure

5. After successful edit: EVALUATE to confirm improvement

6. Repeat with next change

## Why This Works

- probe_solution is fast (~500 intervals), lets us iterate quickly
- Structural changes (algorithm, not patterns) can genuinely improve results
- One change at a time isolates what works
- Don't waste evals on unproven changes

## Expected Flow

1. Probe: num_intervals=1600 -> c5=0.379 -> EDIT (PERMANENT)
2. Probe: base_learning_rate=0.01 -> c5=0.378 -> EDIT
3. Evaluate solution with both changes -> score > 1.0
4. If successful, submit

## Tools

- probe_solution: Fast test of single change
- edit_solution: Make change permanent
- evaluate_solution: Full evaluation only after edits confirm improvement
