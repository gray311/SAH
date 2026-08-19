---
name: discrete-c5-search
description: Method playbook for discrete combinatorial search on Erdős C5 problem. Do NOT use gradient descent. Use discrete step function representations and mutations.
---

# Discrete C5 Search Method

## PROBLEM TYPE
This is a DISCRETE COMBINATORIAL optimization problem, NOT gradient optimization.
The optimal solutions are step functions with rational jump points.
GRADIENT DESCENT FAILS - use discrete mutations instead.

## REPRESENTATION
Step function h defined by:
- h_values: array of values (0≤h≤1) for each interval
- break_points: sorted array of interval boundaries
Constraint: sum(h_values) × (domain / num_intervals) = 1

## MUTATION OPERATORS
Apply these to explore configuration space:

1. **swap_breakpoints**: Exchange two break points, swap their h_values
   - Use when peaks need repositioning
   - Try pairs: (1,3), (2,4), (3,5), etc.

2. **adjust_value**: Change one interval's value by Δ, rebalance others
   - Δ ∈ [-0.3, 0.3]
   - Rebalance by spreading the delta across remaining intervals
   - Use when you want to make a peak taller or shallower

3. **split_interval**: Take one interval, split at midpoint
   - Doubles num_intervals in one region
   - Use to add local detail around promising regions

4. **merge_intervals**: Combine two adjacent intervals, average values
   - Reduces num_intervals, smoothes the function
   - Use when you've over-segmented

5. **shift_peak**: Move a peak by shifting break points
   - Change break_points[i] → break_points[i] + δ
   - Keep relative spacing, shift position

6. **bimodal_shift**: Move both peaks together
   - Shift all break points in the peak regions by same δ

## SEARCH STRATEGY
1. Start with one of: bimodal_narrow, bimodal_wide, periodic_1, triangular
2. For 5-10 iterations per evaluation:
   a. Generate 3-5 mutations from current best
   b. For each, compute c5_bound analytically (FFT)
   c. Keep best 2 candidates
3. On final iteration: evaluate_best_candidate on your absolute best
4. Return best combined_score

## KEY INSIGHTS
- Peaks should be narrow but tall (high h, low overlap)
- Two peaks separated by ~0.5 work better than one wide peak
- Symmetric configurations around x=1 often work well
- Break points at rational values (1/4, 1/3, 1/2, 2/3, 3/4) are promising
- Avoid too many intervals - more than 500 is usually unnecessary
- The FFT computation is exact and fast - use it for search, not evals
- Evaluate only once per search, on your single best candidate
- Max 2 full evaluations total for this harness
