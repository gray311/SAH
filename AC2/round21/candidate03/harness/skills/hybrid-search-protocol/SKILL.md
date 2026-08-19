---
name: hybrid-search-protocol
description: Function-space exploration for C2 maximization. Generate hybrid step patterns, use JAX gradients for exact optimization, and search discretization parameters. Focus on exploring diverse function families rather than parameter refinement.
---

# Hybrid Search Protocol for C2 Maximizer

## Core Principle

The seed provides 12 step patterns as heuristic starting points. DO NOT rely on
string-based parameter extraction. Instead, use generate_hybrid_functions to
create novel pattern combinations and JAX autodiff for exact gradients.

## Phase 1: Hybrid Pattern Exploration (iterations 1-10)

Step 1: Generate Hybrids
- Call generate_hybrid_functions to create 5-6 novel combinations
- Vary: pattern mixes, peak heights (1.2-2.5), interval widths, gap sizes
- Ensure diversity: different peak counts, asymmetric arrangements, wide bases

Step 2: Aggressive Probing
- Call probe_solution on ALL 5-6 hybrids (use full probe budget here)
- Rank by probe score
- Call evaluate_solution on TOP 2 by probe score

Step 3: Track Patterns
- Record which pattern combinations work best
- Use successful hybrids as seeds for next iteration

## Phase 2: JAX Gradient Ascent (iterations 11-20)

Step 1: Compute Exact Gradients
- Use @jax.jit @jax.grad on -c2_ratio
- Get gradient w.r.t. f_values array
- Compute gradient norm to detect convergence

Step 2: Generate Gradient Variants
- Variant 1: new_f = best_f + 0.05 * gradient (ascent)
- Variant 2: new_f = best_f + 0.03 * gradient (smaller step)
- Variant 3: Multi-scale optimization (different learning rates per region)

Step 3: Probe and Evaluate
- Probe all 3, evaluate best
- If gradient norm < 0.001: switch to Phase 3

## Phase 3: Discretization Search (iterations 21-25)

Step 1: Vary num_intervals
- Try: 400, 600, 800, 1000, 1200 intervals
- For each, generate 2 variants with adaptive refinement

Step 2: Final Evaluation
- Probe and evaluate best variants
- Submit if c2 > 0.8962799441554086

## Key Rules

- WORK DIRECTLY WITH JAX ARRAYS: Use ctx.get_best_program() for best_f
- USE JAX AUTOGrAD for exact gradients
- AGGRESSIVE PROBING in Phase 1: 5-6 probes before evals
- DIVERSIFIED MUTATIONS: hybrids, gradients, discretization
- SUBMIT EARLY: If combined_score > 1.042, submit immediately'
