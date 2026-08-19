---
name: extended-restart-strategy
description: Generate diverse restarts beyond seed patterns. Merge, optimize with more restarts.
---

# Extended Restart Strategy for Erdos Problem

## Problem
The seed optimizer has 15 patterns and 3 restarts. But the search space is vast.

## Solution: generate_extra_restarts Tool

This tool generates 10 ADDITIONAL patterns beyond the seed's 15:
- Piecewise constant (2-3 blocks)
- Piecewise linear ramps
- Random block placements
- Delta-like narrow peaks
- Checkerboard patterns
- Sparse Golomb variants
- Quadruple-modal patterns
- Plateau with dips
- Valley patterns

## Workflow

1. CALL generate_extra_restarts(temperature=0.8, num_patterns=10)

2. Analyze the 10 new candidates:
   - Check integral: should be ~1.0 (may vary slightly)
   - Check c5_bound: analytical estimate (may differ from full eval)
   - ACCEPT all candidates for merging

3. Merge with seed's best 15 initializations:
   - Run seed's _get_best_initialization for 15 seeds
   - Combine with the 10 new candidates
   - Take the BEST 15 by analytical c5_bound

4. EDIT solution with num_restarts=5, num_steps=50000

5. CALL evaluate_solution on the SINGLE BEST candidate (lowest c5_bound < 0.365)

6. If no improvement after 1-2 evals, repeat with temperature=1.0

## Why Extended Restarts Work

- Seed patterns: sine/cosine modulations, classic Golomb, bipartite, tri-modal
- Extra patterns: piecewise constructions, random placements, delta bumps, checkerboards
- Different "geometry" of h(x) explores different correlation structures
- More restarts = better chance of escaping local minima
- Analytical screening still saves budget

## Expected Outcome

With 25+ diverse initializations and 5 restarts, we can find better C5 bounds than seed's 15 patterns + 3 restarts.
