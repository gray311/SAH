---
name: hyperparameter-tuning-guide
description: Guide for Erdős C5 optimization - tune penalty_strength [500-2000], learning_rate [0.001-0.01], num_intervals [400-1600]. Preserve sigmoid, FFT, integral constraint.
---

# Hyperparameter Tuning for Erdős C5

## Never Change
- sigmoid(latent) activation
- FFT correlation computation
- integral constraint: (integral_h - 1.0)²
- The 12 initialization patterns

## Tune These
1. **penalty_strength**: 500-2000
   - Too low: constraint violation
   - Too high: over-constrained, local minima
   - Try: 800, 1200, 1600

2. **base_learning_rate**: 0.001-0.01
   - Start at 0.0053, try 0.003, 0.008
   - Too high: oscillation
   - Too low: slow convergence

3. **num_intervals**: 400-1600
   - Affects discretization accuracy
   - Try: 600, 1000, 1200

4. **num_restarts**: 1-6
   - More restarts = better chance of good init
   - Try: 2, 4, 5

5. **seed_start**: 0-10
   - Use different seeds for initialization

6. **num_steps**: 30000-80000
   - More steps = more refinement
   - Try: 40000, 60000

## Edit Strategy
Change ONE parameter at a time. Keep SEARCH/REPLACE blocks focused on single lines.
If constraint fails, revert immediately.
