---
name: discovery-optimization
description: "Iterate on initialization patterns and hyperparameters. Train multiple candidates in parallel."
---

# Multiple Training Strategy

## Problem
The seed optimizer trains for 59000 steps per candidate. We need diverse initializations.

## Solution: Multiple Parallel Training

1. EDIT the seed to change: num_restarts, base_learning_rate, num_steps, seed_start

2. SUBMIT and evaluate EACH variant completely

3. Try these modifications:
   - num_restarts: 1, 3, 5, 10
   - base_learning_rate: 0.001, 0.006, 0.01, 0.05
   - num_steps: 29000, 59000, 88000
   - seed_start: different seeds
   - num_intervals: 800, 1600, 3200

4. When combined_score > 1.0, finish immediately

## Why This Works

- The optimizer can IMPROVE poor initializations
- Train multiple candidates with different configs
- Use full budget (30 evals) to explore parameter space
- Don't rely on pre-computed scores

## Example edits

Edit num_restarts from 1 to 3, base_learning_rate from 0.006 to 0.01.
