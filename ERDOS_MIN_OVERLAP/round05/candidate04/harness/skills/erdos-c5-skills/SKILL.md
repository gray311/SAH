---
name: erdos-c5-skills
description: Method playbook for optimizing the Erdős C5 constant. Target - maximize combined_score = 0.380923 / C5 by minimizing max_k ∫h(x)(1-h(x+k))dx. Critical - maintain ∫h=1.0 constraint via sigmoid + penalty. Use quick_eval to screen configs.
---

# Erdős C5 Optimization - Method Playbook
## Problem
Find step function h:[0,2]->[0,1] minimizing C5 = max_k ∫h(x)(1-h(x+k))dx.
Score = 0.380923 / C5 (target > 1.0 means improvement).

## Key Structure
- Discretize h on N intervals, dx=2/N
- Use sigmoid(latent) to ensure h∈[0,1]
- Penalty = penalty_strength * (∫h - 1.0)^2
- Total loss = C5_objective + penalty

## Strategy: Quick_eval → Eval → Iterate
### Step 1: Quick_eval (cheap screening)
- Use quick_eval with reduced N=200
- Test hyperparameters: lr∈{0.001,0.005,0.01,0.02}, penalty∈{500,1000,2000,5000}
- Test optimizers: adam, adamw, rmsprop
- Test steps: 10000, 50000 (quick checks)
- Success criterion: integral within 0.5 of 1.0 AND c5 < 0.40

### Step 2: Evaluate (full scoring)
- Only call after quick_eval shows feasibility
- Use full N=800 (or higher if time permits)
- Run to completion (50000-200000 steps)
- Multi-restart: try 3-10 restarts if time allows

### Step 3: Iterate (build on success)
If score improved:
  - Try increasing num_steps by 2x
  - Try stronger penalty (if constraint barely satisfied)
  - Try different optimizer (adamw↔rmsprop↔adagrad)
  - Try additional initialization patterns (more diverse)

If score unchanged or worse:
  - Try completely different hyperparameter region
  - Try different optimizer
  - Try restructuring _get_best_initialization
  - Try learning rate schedule

## Initialization Pattern Ideas
1. Random normal (seeded)
2. Random uniform in [-2,2]
3. sin/cos combinations with different frequencies
4. Block patterns: where(x<threshold, high, low)
5. Multi-block: where in [0,1/3]: high, [1/3,2/3]: mid, rest: low
6. Multi-scale: sin(2πx) + sin(4πx) + sin(8πx)
7. Sawtooth/triangular waves
8. Exponential decay from edge
9. Piecewise linear functions (triangle, trapezoid)
10. Gaussian-like bumps at strategic locations

## Hyperparameter Guidelines
- Learning rate: Start 0.005-0.01, adjust based on convergence speed
- Penalty: 500-2000 typical; too high (5000+) prevents convergence
- Steps: 50000-200000; more steps = better but risk timeout
- Restarts: 3-10; more = better coverage but more time
- Intervals: 800-2000; higher = more accurate but slower

## Common Errors
- Breaking optimization loop (syntax, missing return)
- Forgetting sigmoid on latent (unbounded h)
- Wrong penalty sign (should add, not subtract)
- num_steps too high (timeout)
- num_intervals too high (timeout)
- Not padding arrays for FFT (corrupted correlation)
- Mixing jax.random key management incorrectly
## Tool Reminder
- quick_eval: Always use first to check feasibility
- evaluate_solution: Only after quick_eval shows promise
- finish: When 2 quick_evals fail OR evals exhausted
