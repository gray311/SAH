---
name: optimizer-tuning
description: Tune Erdos optimizer hyperparameters and initialization for better c5_bound.
---

# Optimizer Tuning for Erdos Min-Overlap

## The Challenge

The seed program uses:
- num_intervals=800 (discretization)
- base_learning_rate=0.0062
- penalty_strength=61.0
- num_restarts=3
- 15 pattern initializations

Current best c5_bound: 0.380923
Goal: c5_bound < 0.380923

## Why Current Fails

The optimizer converges quickly to local minima with the current hyperparameters.
The 15 patterns may not explore the right region of function space.

## Tuning Strategy

### Hyperparameter Adjustments

1. **num_intervals**: Increase from 800 to 1600 or 3200
   - Finer discretization captures more structure
   - May find better step functions

2. **base_learning_rate**: Try 0.003, 0.01, or 0.005
   - Lower LR: more stable convergence, might escape local minima
   - Higher LR: faster exploration, might find better regions

3. **penalty_strength**: Try 30, 100, or 200
   - Higher penalty: stricter integral=1 constraint
   - Lower penalty: more flexibility in function shape

4. **num_restarts**: Try 1 (focused) or 5 (more diversity)
   - Fewer restarts: commit to single optimization path
   - More restarts: explore multiple starting points

### Initialization Modifications

5. **Latent bias**: Add +1.0 or -0.5 bias to latent
   - Shifts sigmoid output toward higher or lower values
   - May create better h(x) distributions

6. **Noise scaling**: Reduce noise from 0.3-1.0 to 0.1-0.5
   - Smoother initializations, might converge better

## Using the mutate_optimizer Tool

Call mutate_optimizer with:
- parameter: "num_intervals"
  value: 1600

or

- parameter: "base_learning_rate"
  value: 0.003

or

- parameter: "latent_bias"
  value: null  # triggers bias addition

After mutation, evaluate and check if c5_bound improved.

## Success Criteria

- c5_bound < 0.380923 (combined_score > 1.0)
- integral(h) ≈ 1.0 (within 1%)
- Use probe_solution to screen before full eval
