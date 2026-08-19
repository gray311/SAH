---
name: discovery-optimization
description: "Optimize hyperparameters of a pre-tuned mathematical optimization program. Use perturb_params\nfor safe, bounded changes. Use probe_solution to screen before full evaluation. Preserve the\nseed's sophisticated structure \u2014 only tweak numerical parameters."
---

# Hyperparameter Optimization Strategy for Math Discovery Tasks

## Phase 1: Establish Baseline
- Call evaluate_solution on the current code FIRST. Record this as your baseline.
- If you don't have a confirmed baseline, do NOT edit. The seed may already be optimal.

## Phase 2: Safe Parameter Perturbation
- Try perturb_params with small changes:
  * learning_rate: ±0.01 to ±0.05
  * num_intervals: ±50 to ±100 (check for memory limits)
  * num_steps: ±5000 to ±10000
  * best_c2: ±0.001 (affects reinitialization threshold)
- Always change ONE parameter at a time to isolate effects.

## Phase 3: Screening with Probes
- Call probe_solution to quickly rank 3-5 parameter variations.
- Only run evaluate_solution on the top 1-2 variants that show improvement.
- Save probes in your scratch space to track what works.

## Phase 4: Iterative Refinement
- If a perturbation improves the probe score, test it with evaluate_solution.
- If it confirms improvement, make a SMALL refinement (e.g., learning_rate += 0.005).
- If it regresses, try the opposite direction or a different parameter.

## Phase 5: Structural Changes (Last Resort)
- Only if parameter tuning exhausts progress, consider changing ONE line of logic.
- Example: num_intervals = 500 → 550 (increase resolution)
- Use SEARCH/REPLACE with exact line matching. Comment your change.

## Critical Rules
- NEVER rewrite the whole EVOLVE-BLOCK unless you must.
- NEVER change imports or the entry function.
- If probe is not available, skip to Phase 4.
- Track all your experiments in a summary for finish().
- Remember: combined_score = c2 / 0.8962799441554086; maximize c2 to maximize combined_score.

## Parameter Interpretation
- learning_rate: Controls step size in optimization. Too high → unstable. Too low → slow convergence.
- num_intervals: Discretization resolution. Higher = more accurate but slower.
- num_steps: Total optimization iterations. More steps = more refinement time.
- best_c2: Threshold for reinitialization. Lower = more aggressive restarts.
