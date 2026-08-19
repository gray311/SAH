---
name: architecture-escape-protocol
description: Escape local optima by generating and testing diverse function architectures in parallel. Use probes to screen, evaluate top candidates.
---

# Architecture Escape Protocol

## Problem
Parameter tuning is STUCK. The seed step pattern is a local optimum.

## Solution
Generate diverse architectures, test in parallel with probes, commit to best.

## When to Use
- At iteration 1: Always start with architecture diversity
- At iteration 8: If no improvement after 7 iterations
- At iteration 20: Final escape attempt

## Procedure
1. Call explore_architectures or reinitialize_with_architectures
2. Generate 5-8 diverse candidates
3. Probe ALL on 10% subsample (cheap!)
4. Rank by probe score
5. Evaluate top 1-2
6. If beats seed: refine that architecture
7. If fails: try different architecture class

## Architecture Classes
- Multi-modal: 2+ peaks with different widths
- Asymmetric: mass concentrated on one side
- Adaptive-resolution: coarse tails, fine peaks
- Boundary-optimized: mass at domain edges
- Triangular: linear rise/fall instead of flat tops
- Piecewise-linear: continuous slopes instead of steps

## Success Criteria
- c2 > 0.8962799441554086
- combined_score > 1.0
