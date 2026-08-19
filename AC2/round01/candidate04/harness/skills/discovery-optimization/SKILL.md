---
name: discovery-optimization
description: "Mathematical function discovery and optimization. Test different function families (splines, mixtures, piecewise) to maximize C\u2082 constant. Each evaluation should explore a genuinely different construction approach."
---

# Mathematical Function Discovery

## Objective
Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞})
Target: surpass 0.8962799441554086

## Strategy
With limited evaluations (~20 total), each must test a **different mathematical construction**.

### Function Families to Explore

1. **Multi-modal Piecewise Functions**
   - Multiple linear segments with different slopes
   - Design peaks/valleys to concentrate autocorrelation energy
   - Ensure continuity and non-negativity

2. **Spline-Based Constructions**
   - B-splines with optimized knot positions
   - Can create smooth multi-modal functions

3. **Weighted Basis Mixtures**
   - Sum of Gaussians: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))
   - Sum of exponentials with different decay rates
   - Combine different function shapes

4. **Symmetric Constructions**
   - Exploit even symmetry: f(x) = f(-x)
   - Reduces optimization complexity

5. **Multi-scale Approaches**
   - Coarse grid optimization, then refine
   - Focus optimization on promising regions

## Implementation Guidelines

- **Full Rewrites**: For new function families, write COMPLETE new code in EVOLVE-BLOCK
- **Constraints**: f(x) ≥ 0, use softplus/exp transformations if needed
- **Performance**: JIT compile (numba/jax), keep discretization 50-200 intervals
- **Diversity**: Each evaluation should be a DIFFERENT construction type

## Evaluation Discipline

1. Pick ONE function family to explore
2. Write COMPLETE implementation (not incremental edits)
3. Evaluate
4. If promising, refine that family. If not, try a DIFFERENT family.
5. With ~20 evals, test 8-10 different constructions

## Common Pitfalls

- Don't just tune parameters of the same function
- Don't keep making small edits - step back and try new families
- Ensure all constraints (non-negativity, integrability) are satisfied
- Use deterministic seeds for reproducibility

## Scoring

- combined_score > 1.0 means C₂ > 0.8962799441554086 (new record!)
- The evaluator is fast; you have budget for systematic exploration
