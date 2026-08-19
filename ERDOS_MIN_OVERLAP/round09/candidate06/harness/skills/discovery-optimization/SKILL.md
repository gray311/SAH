---
name: discovery-optimization
description: "Hyperparameter exploration for Erdos optimization using diverse seed initializations."
---

# Erdos Minimum Overlap - Hyperparameter Exploration

## Why This Strategy Works

The seed program's `_get_best_initialization()` already explores 12 different patterns and picks the best. This gives us 12 diverse starting points.

Instead of trying to design new mathematical constructions (which is hard and error-prone), we should:
1. Keep the seed's initialization as-is
2. Add multiple optimization runs (num_restarts) with varied hyperparameters
3. Use probe_solution to quickly screen many (lr, penalty, steps) combinations
4. Run full evaluations only on the top candidates

## Edit Strategy

### Minimal, Focused Changes:

1. **Add a hyperparameter grid** in Hyperparameters:
   - num_steps: try [10000, 20000, 40000, 60000, 80000]
   - base_learning_rate: try [0.001, 0.005, 0.01, 0.02, 0.05]
   - penalty_strength: try [500, 1000, 2000, 5000, 10000]
   - num_restarts: try [5, 10, 15]

2. **Modify _optimize_single_run** to:
   - Loop over a grid of (lr, penalty, steps)
   - For each combo, run optimization with 3-5 random seeds
   - Track the best result across all combos

3. **Use probe_solution heavily**:
   - After 500-1000 steps of optimization, probe to estimate c5_bound
   - Only run full evaluation on candidates with probe_score > 0.9998

## Example Edit Pattern

```python
# In EVOLVE-BLOCK, add this before optimization:
best_result = {"score": 0, "params": None}
for lr in [0.001, 0.005, 0.01, 0.02]:
    for penalty in [500, 2000, 5000, 10000]:
        for steps in [10000, 30000, 60000]:
            for seed in [0, 1, 2, 3]:
                # Run optimization, probe, and track best
```

## Key Principles
- EXPLORE HYPERPARAMETERS, don't redesign the algorithm
- USE PROBES to screen before spending real evaluations
- The seed's 12-pattern initialization is GOLD - preserve it
- Target: c5_bound < 0.380923 (combined_score > 1.0)
