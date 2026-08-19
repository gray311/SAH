---
name: discovery-optimization
description: "Mathematical function optimization for second autocorrelation inequality. Maximizes C2 by exploring piecewise-constant functions with bounded parameter search. Uses the EVOLVE-BLOCK for targeted edits and 30 evaluation budget efficiently."
---

# C2 Maximization Strategy

## Initial Exploration (Evals 1-5)
Generate 5 completely different function pattern classes:
1. Symmetric pyramid with 3 levels
2. Asymmetric 4-level function
3. Bimodal function (two peaks)
4. Narrow high peak (width ~30%)
5. Wide plateau with small bump

For each, create a complete function definition with heights/positions chosen from successful patterns.

## Local Search (Evals 6-25)
For the top 2 patterns from initial exploration:
1. Modify heights by ±0.05 (try 5 variations per height)
2. Adjust widths by ±2% of total range
3. Shift centers by ±10% of interval
4. Keep the BEST variant and refine further

Use targeted edits: only change the height array or width parameters, not the overall structure.

## Final Confirmation (Evals 26-30)
Take top 3 candidates and:
1. Run local optimization with optimal learning rate (0.15-0.25)
2. Run for max iterations (5000-7000)
3. Evaluate final scores

Call finish with summary of winning pattern class and key parameter values.

## Critical Edits
- Height modifications: Change f_values array, ensure non-negativity
- Width modifications: Change start/end indices proportionally
- Pattern changes: Rewrite the entire function construction block

NEVER break the convolution computation or norm calculations.
