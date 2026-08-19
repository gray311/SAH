---
name: golomb-refinement
description: Optimize Golomb ruler mark placements using optimize_golomb_marks, then edit the code to use the new marks.
---

# Golomb Ruler Refinement for Erdos Problem

## Strategy

The seed program has a working 5-mark Golomb ruler construction with marks at [0.0, 0.4, 0.8, 1.2, 1.6].
To improve, call optimize_golomb_marks to find BETTER mark placements, then EDIT the code to use those marks.

## Workflow

1. CALL optimize_golomb_marks(num_marks=5)
   - Returns: marks (list of 5 floats in [0,2]), c5_bound (analytical)

2. EDIT the seed's _get_best_initialization method:
   - Find the Golomb ruler pattern (pattern == 12)
   - Replace the hardcoded marks [0.0, 0.4, 0.8, 1.2, 1.6] with the optimized marks
   - Keep the rest of the pattern unchanged

3. SET hyperparameters: num_restarts=1, seed_start=0 (single-candidate test)

4. CALL evaluate_solution ONCE

5. If combined_score > 1.0, call finish. Otherwise, try num_marks=4, 6, 7.

## Why This Works

- The seed already has correct Golomb ruler implementation - just needs better marks
- optimize_golomb_marks does cheap greedy search (no training)
- Only 1 eval needed per candidate
- Hill-climbing on 200 buckets finds local optimum quickly
