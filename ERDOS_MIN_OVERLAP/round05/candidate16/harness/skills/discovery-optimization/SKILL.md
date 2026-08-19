---
name: discovery-optimization
description: "Mathematical optimization with constrained gradient descent. Use for discovery tasks requiring parameter tuning and constraint satisfaction."
---

Mathematical Optimization Playbook

This task optimizes a step function h on [0,2] to minimize overlap integrals. The evaluator computes combined_score = target_bound / found_bound, where higher is better.

Core Principles:
1. Respect the architecture: The seed program's design (800 intervals, FFT-based evaluation, multi-restart) is sound. Do not simplify it excessively.
2. Constraint satisfaction is critical: The integral of h must equal exactly 1.0. This is enforced by penalty_strength * (integral(h) - 1.0)^2. Watch for constraint_loss in evaluations.
3. Gradual improvement: Make small hyperparameter changes. Large structural changes rarely help this mathematical optimization task.
4. Use the full budget: 30 evaluations allow multiple iterations. Plan: 5-7 evaluations max per harness run.

Optimization Strategies:
Strategy A: Fine-tune learning rate
If optimization converges slowly:
- Try base_learning_rate: 0.004, 0.006, 0.008
- Monitor: Does c5_bound decrease monotonically?

Strategy B: Adjust penalty strength
If constraint violation is suspected (validity=0 or high constraint_loss):
- Try penalty_strength: 1200, 1500, 1800
- Too high: optimization stalls. Too low: constraints violated.

Strategy C: Increase optimization steps
The FFT evaluation is fast (~10ms). You can afford:
- num_steps: 65000, 70000
- This gives more time for convergence without timeout risk.

Strategy D: Add diversity via more restarts
- num_restarts: 5, 7
- Helps escape local minima in this non-convex landscape.

Strategy E: Pattern-based initialization
The _get_best_initialization tries 12 patterns including: random normal, sinusoidal, step functions.
All are transformed via sigmoid to [0,1] then normalized.
Do not remove patterns - diversity helps escape local minima.

Editing Guidelines:
- Use SEARCH/REPLACE diffs when making small changes
- Only modify the EVOLVE-BLOCK region
- Keep imports and dataclass definitions intact
- Preserve the optimizer's JIT compilation

Evaluation Interpretation:
- combined_score > 1.0: SUCCESS (new upper bound found)
- combined_score ~ 1.0: similar to seed (acceptable)
- combined_score < 1.0: worse than seed (need better approach)
- validity=0: constraint violated or program error

Decision Tree:
If combined_score > 1.0 but < best_so_far:
  Keep the approach, try to improve further

If combined_score < 1.0 or validity=0:
  Diagnose: was it learning rate? penalty? or architecture change?
  Revert to best_so_far and try different parameter

If all 30 evaluations used without > 1.0 score:
  Call finish with summary of what was tried
