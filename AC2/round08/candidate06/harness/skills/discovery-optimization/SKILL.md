---
name: discovery-optimization
description: "Diverse exploration of C2 maximization strategies. Move beyond the seed's stuck local optimum by trying evolutionary search, alternative representations, and coarse-to-fine approaches."
---

# C2 Maximization: Diverse Strategy Exploration

## Critical: The Seed is Stuck!

The seed program achieves C2 approx 0.925 (combined_score 1.03431), which is already 2.7% above the historical best of 0.8963.

BUT: The seed is USING GRADIENT-BASED OPTIMIZATION on step functions and has converged to a LOCAL OPTIMUM.

Your job is NOT to "verify step functions" - they're already there.
Your job is to FIND BETTER solutions through DIFFERENT strategies.


## Strategy 1: Evolutionary Search (Try First!)

- Create a population of 5-10 step function patterns
- Each pattern: define by intervals and heights (not gradient optimization)
- Mutation: change heights by +/-10-20%, shift interval boundaries
- Selection: keep top performers, combine/diversify
- Run for 10-20 generations with probing

## Strategy 2: Alternative Representations

- Spline-based: Use cubic B-splines with optimized control points
- Gaussian mixture: f(x) = sum w_i * exp(-((x-mu_i)/sigma_i)^2)
- Hybrid: Step function base + small spline perturbations

## Strategy 3: Coarse-to-Fine Refinement

- Start with 50 intervals, optimize to ~0.90
- Refine to 200 intervals, optimize further
- This can escape local minima

## Strategy 4: Evolutionary Local Search

- Start from seed's best pattern
- Apply targeted mutations: height increases, interval shifts
- Keep variations that improve even slightly
- Use probes to rank ~10-15 variants before eval

## Workflow

1. IMMEDIATELY try evolutionary search with diverse initial patterns
2. Use probe_solution to rapidly rank ~10-15 variants
3. Evaluate only top 2-3
4. If no improvement, try alternative representation (spline/Gaussian)
5. Use coarse-to-fine if stuck
6. Never optimize the same approach for 20 evals - diversify!


## Why the Seed Fails

- Gradient-based optimization gets stuck in local minima
- The step function search space is discrete and rugged
- 37000 steps with learning rate 0.22 is TOO much - overshot or plateaued

## Success Criteria

- Any C2 > 0.925 beats the seed
- Target: C2 > 0.93 (combined_score > 1.04)
- You have 20 evaluations - spend them wisely on DIVERSE candidates
