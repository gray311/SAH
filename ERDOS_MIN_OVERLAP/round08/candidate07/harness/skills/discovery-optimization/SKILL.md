---
name: discovery-optimization
description: "C5 bound optimizer. Must escape local optima via coarse-to-fine search and explicit structural enumeration. Target combined_score > 1.0."
---

# C5 Bound Optimization - Escaping Local Optima

## Why Gradient Descent Fails

The seed's Adam optimizer finds good local optima but cannot discover the global optimum because:
- The landscape is highly non-convex with many basins
- The optimal solution likely has a specific combinatorial structure
- 800-point random initialization explores "noise" not structure

## Winning Strategies

### Strategy 1: Coarse Discretization First

- Start with num_intervals=50-100 (fewer degrees of freedom)
- Use stronger regularization to enforce piecewise constant structure
- Find a pattern that beats seed
- Only THEN refine to higher resolution

### Strategy 2: Explicit Combinatorial Search

Instead of random gradient descent, enumerate specific structures:
- 3-point step functions: h=1 on [0,a], h=0.5 on [a,b], h=0 elsewhere
- 4-point symmetric patterns
- Periodic patterns with small periods

For each structure, use gradient descent ONLY to tune the breakpoint positions.

### Strategy 3: Evolutionary / Multi-Strategy

- Run 3-5 independent optimizations with DIFFERENT strategies in parallel
- Each run uses a fundamentally different initialization/optimizer
- Track best across all runs

## Concrete Edits to Try

1. Change num_intervals from 800 to 50, increase penalty_strength to 5000
2. Replace 12 random patterns with 3-4 carefully designed step functions
3. Add evolutionary strategies: restart with top 1 from previous generation
4. Try CMA-ES or differential evolution instead of Adam
5. Use the probe tool to rank 5+ structural variants before full eval

## Execution Plan

- Eval 1: Coarse version (50 intervals, strong penalty)
- Eval 2-5: Enumerate 4-5 explicit step function structures
- Eval 6-10: Refine best structure with higher resolution
- Remaining evals: Explore additional strategies

**KEY**: Be bold. The seed is clever but stuck. You need a fundamentally different approach.
