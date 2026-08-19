---
name: bipartite-first-strategy
description: Generate bipartite candidates, probe all, evaluate best 2. Bipartite functions are the best bet for Erdos C5.
---

# Bipartite-First Strategy for Erdos C5

## Core Principle
The optimal solution for the Erdos C5 problem is likely a BIPARTITE STEP FUNCTION (two levels: 1 and 0).

## Why This Works
- Bipartite functions h(x) = 1 for x < t, 0 for x >= t have minimal self-overlap
- The correlation structure is simple: correlation decays monotonically with shift k
- This avoids the complex patterns that cause high overlap in random functions

## Step-by-Step Workflow

1. CALL bipartite_searcher with num_thresholds=10, threshold_range=[0.7, 1.3]
   - Generates 10 bipartite functions with different thresholds
   - t=1.0 gives integral(h)=1.0 (satisfies constraint)
   - t in [0.7, 1.3] explores around the constraint

2. CALL probe_solution on EACH of the 10 candidates
   - Screen all candidates cheaply (~10 seconds each vs minutes for full eval)
   - Keep candidates with combined_score > 0.98 (c5_bound < 0.375)

3. CALL evaluate_solution on the top 2 candidates
   - Full evaluation confirms if we beat the record
   - If combined_score > 1.0, finish

4. If no improvement after 2 full evals:
   - Try multi-modal: three peaks at x = 0.3, 1.0, 1.7
   - Try asymmetric: h(x) = 1 for x in [0, 0.5] U [1.5, 2.0]

## Key Rules
- ALWAYS start with bipartite_searcher (10 candidates)
- PROBE ALL candidates before any full evaluation
- Evaluate only top 2-3 candidates
- BIPARTITE is your best bet - don't waste evals on random patterns
