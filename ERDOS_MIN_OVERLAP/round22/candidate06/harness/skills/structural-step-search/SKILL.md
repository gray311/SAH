---
name: structural-step-search
description: Search for TRUE STEP FUNCTIONS using coarse discretization and hard thresholds. Generate 5-8 structural patterns, evaluate best with full eval.
---

# Structural Step Function Search

## Workflow

1. CALL generate_step_functions(grid_size=30)

2. EXAMINE all candidates:
   - Check c5_bound (precomputed analytical score)
   - Look for c5_bound < 0.37 (promising step function)

3. CALL evaluate_solution on candidates with c5_bound < 0.37

4. If no success, TRY COARSER GRID:
   CALL generate_step_functions(grid_size=20)
   or grid_size=40

5. Try different step PATTURNS:
   - Binary steps (jump at different locations)
   - Uniform steps (constant height)
   - Multi-level steps (2-3 different values)
   - Asymmetric steps

## Why This Works

- Coarse grids force step-function structure
- Hard thresholds (not sigmoids) capture true steps
- Direct c5 computation avoids optimization waste
- Multiple structural patterns increase discovery chances

## Expected Results

With 5-8 step patterns, expect 2-4 to pass c5 < 0.37 filter.
Full evaluation should find step functions beating smooth curves.
