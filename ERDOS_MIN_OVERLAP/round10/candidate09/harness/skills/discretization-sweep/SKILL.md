---
name: discretization-sweep
description: Systematic discretization sweep for Erdos optimizer.  Test num_intervals across wide range, screen with probe, evaluate winners. Use construct_structured_init if standard patterns fail.
---

# Discretization-First Strategy for Erdos Optimizer

## Core Insight
The seed's 800-interval discretization is likely suboptimal. 
The optimal step function requires precise feature placement that 
coarse grids cannot capture.

## Phase 1: Wide Discretization Sweep

### Test Range
Try: 200, 400, 600, 800, 1200, 1600, 2400, 3200, 4800, 6400, 8000

### For Each Discretization:
1. Edit num_intervals to the target value
2. Test learning_rates: 0.001, 0.005, 0.01, 0.02, 0.05, 0.1
3. Use probe_solution to check:
   - Integral ≈ 1.0 (within 0.01)
   - h values in [0, 1]
4. Call evaluate_solution only if probe passes and constraint is good

### Track Best
For each discretization, track:
- Best combined_score
- Best learning_rate
- Whether constraint is satisfied

## Phase 2: Structured Initialization

If Phase 1 yields no improvement:
1. Call construct_structured_init
2. For each construction (bimodal_tight, golomb_5, etc.):
   - Edit initial_latent to use the construction
   - Sweep hyperparameters again
   - probe first, then evaluate

## Phase 3: Fine-Tuning

If close to target (combined_score ≈ 0.95-0.99):
- Reduce learning_rate to 0.001-0.003
- Increase num_steps to 100000-300000
- Fine-tune penalty_strength for constraint satisfaction

## Budget Management
- Use probe_solution liberally (30 probe budget)
- Call evaluate_solution only on promising variants (≤10 full evals)
- Focus: Find ONE discretization that works, then optimize it
