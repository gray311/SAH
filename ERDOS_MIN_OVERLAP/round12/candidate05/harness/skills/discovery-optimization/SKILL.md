---
name: discovery-optimization
description: "Generate and evaluate piecewise-constant step functions for the Erdos minimum overlap problem.\nSearch over discrete configurations of jump locations and levels to find h with integral=1\nminimizing max_k integral h(x)(1-h(x+k)) dx."
---

# Erdos Minimum Overlap - Step Function Construction Strategy

## Core Idea
Optimal h is a TRUE STEP FUNCTION (piecewise constant with jumps), not smooth.
The seed's smooth initializations via sigmoid produce suboptimal results.

## Construction Method
1. Choose number of pieces k (2 to 16)
2. Generate k-1 random jump positions in (0, 2): 0 < t_1 < t_2 < ... < t_{k-1} < 2
3. Assign levels h_i in [0,1] to each piece such that integral(h)=1
   - For binary: levels are 0 and 1; solve for proportions to get integral=1
   - For multi-level: use fractions like 0.25, 0.5, 0.75, 1.0
4. Compute h(x) = sum_i h_i * indicator(x in [t_{i-1}, t_i))
5. Evaluate C5 bound and check constraints

## Search Strategy
- Start with k=2,3,4 simple cases
- Systematically vary k and random seeds
- Use probe_solution to quickly filter candidates violating integral constraint
- Only full evaluate on feasible candidates
- Track best h and report combined_score

## Success criteria
combined_score > 1.0 means c5_bound < 0.38092303510845016
