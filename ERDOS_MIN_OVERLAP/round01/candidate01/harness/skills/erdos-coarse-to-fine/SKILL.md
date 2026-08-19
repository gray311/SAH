---
name: erdos-coarse-to-fine
description: Coarse-to-fine exploration strategy for Erdos minimum overlap. Start with coarse discretization to find ballpark solutions quickly, then refine with higher resolution. Use SEARCH/REPLACE to incrementally increase num_intervals.
---

# Coarse-to-Fine Optimization for Erdos Problem

## Why coarse-to-fine works:
- Coarse configs (50-100 intervals) converge faster and may find good local minima
- Fine configs (200-500 intervals) refine the solution but take longer
- Trying coarse first is less risky than starting too fine

## Implementation pattern:

1. **Coarse phase**: Set num_intervals = 50 or 100
   - Test this first with evaluate_solution
   - Record the combined_score
   - Use targeted SEARCH/REPLACE

2. **Refine phase**: If coarse works (validity=1, reasonable score):
   - Change num_intervals to 200 (current seed level)
   - Evaluate again
   - If needed, go to 300, 400, 500

3. **Alternative paths**:
   - If coarse fails badly, try different penalty_strength
   - If 200 fails, try 150 or 250
   - Try different random seeds (PRNGKey(123), PRNGKey(456))

## SEARCH/REPLACE pattern:

Find: `num_intervals: int = 200`
Replace with: `num_intervals: int = 50`

Then after evaluating, if successful, change back to 200 and then 500 for refinement.
