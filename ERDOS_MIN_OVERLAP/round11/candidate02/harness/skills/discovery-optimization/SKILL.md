---
name: discovery-optimization
description: "Systematic hyperparameter tuning for Erdos optimizer with probe-based screening."
---

# Erdos Minimum Overlap - Hyperparameter Sweep Strategy

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx subject to integral(h)=1 and h in [0,1].

## Why Hyperparameter Tuning Works
The seed optimizer tries 12 initialization patterns but uses fixed hyperparameters.
Small changes to learning rate, penalty strength, or discretization can dramatically
affect whether the optimizer escapes local minima.

## Strategy

### Phase 1: Hyperparameter Sweep (Use All 30 Evals)
1. Start with SEED program
2. For each hyperparameter to tune, create variants:
   - Change ONE parameter at a time
   - Use probe_solution for quick screening (check constraint satisfaction)
   - Call evaluate_solution only on variants that pass probe screening

### Hyperparameters to Systematically Vary:
- num_intervals: 400, 800, 1600, 3200 (affects resolution)
- base_learning_rate: 0.001, 0.005, 0.01, 0.02, 0.05
- penalty_strength: 100, 500, 1000, 2000, 5000, 10000
- num_steps: 20000, 50000, 80000, 100000, 150000
- num_restarts: 1, 3, 5, 10, 20

### Phase 2: If Phase 1 Fails, Expand Initialization Patterns
If no hyperparameter sweep yields improvement:
1. Edit _get_best_initialization() to add NEW patterns:
   - Shifted periodic: h(x) = 2.0*(x < 0.5+alpha) - 1.0 for various alpha
   - Asymmetric bimodal: peaks at (1/4+delta, 3/4-delta)
   - Multi-peak: 3-4 narrow peaks with varying widths
   - Wave-based: sin(pi*x) + sin(2*pi*x) + noise
2. Re-run hyperparameter sweep on new patterns

### Phase 3: Fine-tuning
If close to target but not quite there:
- Use smaller learning rate (0.001-0.003) for final refinement
- Increase num_steps (200000+) for better convergence
- Fine-tune penalty_strength for constraint satisfaction

## Success Criteria
- combined_score greater than 1.0 (c5_bound less than 0.380923)
- Document which hyperparameter combination achieved best result
