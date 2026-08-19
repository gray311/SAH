---
name: discovery-optimization
description: "Optimize the Erdos optimizer by modifying hyperparameters and initialization strategies.\nTarget: c5_bound < 0.380923 (combined_score > 1.0)."
---

# Optimization Strategy for Erdos Min-Overlap

## Understanding the Problem

We minimize: max_k integral_0^2 h(x)(1-h(x+k))dx

The seed program uses 15 pattern initializations, trains for 59000 steps each,
with num_intervals=800, learning_rate=0.0062, penalty=61.0.

## Key Failure Modes to Address

1. **Insufficient exploration**: The optimizer may be stuck in a local minimum.
   - Try increasing num_intervals to capture finer structure
   - Try different learning rates (0.003, 0.01) for different convergence dynamics

2. **Poor initialization**: The 15 patterns may not explore the right region.
   - Add bias to latent (shift sigmoid output)
   - Try smaller/noise patterns (latent*0.5 instead of full range)

3. **Constraint violation**: integral(h) != 1.0 hurts quality.
   - Increase penalty_strength (100, 200) to enforce constraint harder
   - Use num_restarts=1 to focus on single good path

## Edit Strategy

### Single-Parameter Edits ( safest )
- num_intervals: 800 -> 1600 or 3200 (finer discretization)
- base_learning_rate: 0.0062 -> 0.003 or 0.01
- penalty_strength: 61.0 -> 30.0 or 100.0
- num_restarts: 3 -> 1 or 5

### Structural Edits (risky but potentially effective)
- In _get_best_initialization: modify latent scaling
  - latent + noise*0.5 instead of noise*0.3-1.0
  - Add bias: latent + 1.0 or latent - 0.5

## Workflow

1. Call probe_solution on current code (if available)
2. Propose ONE specific edit to hyperparameters or initialization
3. Call evaluate_solution on the edited version
4. Analyze: c5_bound improved? If yes, commit. If no, try different edit.
5. Repeat until c5_bound < 0.380923 or 20 evals used.

## Critical Notes

- The EVOLVE-BLOCK is in the class definition; edits are structural.
- Small hyperparameter changes are safer than rewriting logic.
- probe_solution can approximate c5_bound before full eval.
- If stuck, try num_intervals=3200 with different learning rate.
