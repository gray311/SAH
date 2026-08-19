---
name: discovery-optimization
description: "Optimize a JAX-based harmonic analysis solver for the Erd\u0151s minimum overlap problem.\nPreserve constraint satisfaction (integral=1.0, values in [0,1]) and FFT correlation logic.\nFocus on hyperparameter tuning: learning_rate, penalty_strength, num_intervals, seed variations."
---

# Erdős C5 Optimization Harness

## Core Objective
Maximize combined_score = 0.38092303510845016 / c5_bound by finding h that minimizes max overlap.

## Critical Constraints
1. h = sigmoid(latent) → values in (0,1)
2. ∫ h(x)dx = 1.0 (checked via penalty_strength * (integral - 1.0)²)
3. FFT-based correlation computation must remain unchanged
4. num_intervals = 800 (discretization)

## Strategy
**DO NOT** rewrite the sigmoid, FFT, or constraint handling code. Only tune:
- penalty_strength: try values in [500, 2000]
- base_learning_rate: try [0.001, 0.01]
- num_intervals: try [400, 1600]
- seed_start/num_restarts: [0, 10] × [1, 6]
- num_steps: try [30000, 80000]

## Edit Protocol
1. Call analyze_constraint() to baseline current state
2. Change ONE hyperparameter at a time
3. Keep all 12 initialization patterns intact
4. Use SEARCH/REPLACE for targeted edits
5. Never touch: sigmoid(), jnp.fft, _compute_c5_bound, constraint_loss formula

## Recovery
If validity=0 or constraint fails: revert to previous working code. Try different hyperparameter instead.
Use best_so_far score as guide — only change if you preserve structure.
