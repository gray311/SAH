---
name: discovery-optimization
description: "Tune hyperparameters and optimizer to find better solutions. Use probes to screen candidates before full evaluation."
---

# Erdos Minimum Overlap - Hyperparameter Optimization Strategy

## Problem

The seed optimizer uses 12 initializations but has FIXED hyperparameters.
To improve, we must systematically VARY these parameters.

## Key Hyperparameters to Tune

### Learning Rate (base_learning_rate)
- Try: 0.001, 0.005, 0.01, 0.02, 0.05
- Too low: slow convergence, stuck in local minima
- Too high: oscillations, constraint violations

### Penalty Strength (penalty_strength)
- Try: 10, 30, 61, 100, 200, 500
- Too weak: integral constraint not satisfied
- Too strong: optimizer struggles, poor C5 bound

### Number of Steps (num_steps)
- Try: 10000, 30000, 59000, 100000, 200000
- Too few: not converged
- Too many: wasted budget, could be better initialization

### Number of Restarts (num_restarts)
- Try: 1, 3, 5, 10
- More restarts = better exploration but uses more eval budget

## Strategy

### Phase 1: Quick Parameter Sweep (Use ALL 30 Probes)

1. Keep other params fixed, VARY ONE hyperparameter at a time
2. For each candidate, call probe_solution to check:
   - Does integral(h) ≈ 1 (within 0.01)?
   - What is estimated c5_bound?
3. Track which parameter values give best probe results

### Phase 2: Full Evaluation

1. Take top 3 candidates from Phase 2 (c5_bound < 0.375 from probe)
2. Call evaluate_solution on each
3. Analyze results - which hyperparameters worked?

### Phase 3: Optimizer Variation

1. If hyperparameter tuning doesn't help, try DIFFERENT optimizers:
   - optax.adamw (weight decay)
   - optax.rmsprop
   - optax.sgd
   - optax.adadelta
2. Change the optimizer in the seed code

### Phase 4: Learning Rate Schedules

1. Add learning rate decay or warmup
2. Use optax schedule functions (e.g., optax.schedule.decay)

## Expected Outcome

- Find hyperparameter combinations that achieve c5_bound < 0.37
- Or discover optimizer strategies that converge better

## Key Insight

The seed's initialization is GOOD (12 diverse patterns).
The optimization is the bottleneck. TUNE IT.
