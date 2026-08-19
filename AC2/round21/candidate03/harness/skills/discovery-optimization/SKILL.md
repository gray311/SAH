---
name: discovery-optimization
description: "Function-space exploration for C2 maximization. Generate hybrid step patterns, use JAX gradients for exact optimization, and search discretization parameters. Avoid fragile string parsing - work directly with JAX arrays."
---

# C2 Maximizer: Function-Space Exploration Protocol

## Core Principle

The seed provides 12 step patterns as heuristic starting points. DO NOT try to parse them by string matching.
Instead, work directly with the C2Optimizer's JAX arrays and use JAX's autodiff capabilities.

## Phase 1: Hybrid Pattern Generation (iterations 1-10)

Step 1: Generate Novel Hybrids
- Call generate_hybrid_functions with current best
- Create combinations: (a) mix patterns 0-2 + 5, (b) patterns 3-4 + 7-8, (c) patterns 9-11 with modified heights
- Vary: peak heights (1.2-2.5), interval widths (15-40%), gap sizes (5-20%)
- Generate 5-6 unique hybrids

Step 2: Probe and Evaluate
- Call probe_solution on ALL 5-6 variants (use full probe budget here)
- Call evaluate_solution on TOP 2 by probe score
- Track: which pattern combinations yield best c2

Step 3: Iterate
- If beats record: continue generating hybrids with refined parameters
- If no improvement after 3 iterations: switch to Phase 2

## Phase 2: JAX Gradient Ascent (iterations 11-20)

Step 1: Compute Exact Gradients
- Use @jax.jit @jax.grad on -c2_ratio (objective_fn in C2Optimizer)
- Get gradient w.r.t. f_values array and optimizer hyperparameters
- Compute gradient norm to detect convergence

Step 2: Generate Gradient Variants
Generate 3 variants:
- Variant 1 (Ascent): new_f = best_f + learning_rate * gradient (lr = 0.05)
- Variant 2 (Momentum): new_f = best_f + 0.1 * previous_step + 0.03 * gradient
- Variant 3 (Multi-scale): Optimize different parameter scales (intervals vs heights)

Step 3: Probe and Evaluate
- Probe all 3, evaluate best
- If gradient norm < 0.001: switch to Phase 3

## Phase 3: Discretization Search (iterations 21-25)

Step 1: Vary num_intervals
- Try: 400, 600, 800, 1000, 1200 intervals
- For each, generate 2 variants:
  - Variant A: Adaptive refinement (denser grid around high peaks)
  - Variant B: Coarsen then refine (start coarse, add detail at edges)

Step 2: Final Evaluation
- Probe and evaluate best variants
- Submit if c2 > 0.8962799441554086 (combined_score > 1.042)

## Key Rules

- WORK DIRECTLY WITH JAX ARRAYS: Use ctx.get_best_program() to get best_f
- USE JAX AUTOGrAD: @jax.grad gives exact gradients for the C2 computation
- AGGRESSIVE PROBING: 5-8 probes before any full eval
- DIVERSIFIED MUTATIONS: Hybrids, gradient steps, discretization changes
- SUBMIT EARLY: If combined_score > 1.042, submit immediately'
