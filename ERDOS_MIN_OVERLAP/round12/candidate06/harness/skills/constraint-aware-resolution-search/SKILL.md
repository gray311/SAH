---
name: constraint-aware-resolution-search
description: Prioritize higher num_intervals (1600-6400) with strict probe-based constraint filtering. Only evaluate programs where |integral(h)-1|<0.05. Use probe to rank valid variants.
---

# Constraint-Aware Resolution-First Search

## Core Strategy
The seed program score of 0.999855 indicates it is well optimized for num_intervals=800.
To find a NEW upper bound (combined_score > 1.0), we MUST explore higher resolutions.

## The Waste Problem
Many hyperparameter variants violate the constraint integral(h)=1.
Evaluating such programs wastes precious eval budget.

## Solution: Probe-Based Filtering
probe_solution returns approximate integral(h) and c5_bound.
Use it to:
1. FILTER: Discard any variant with |integral(h) - 1| >= 0.05
2. RANK: Order valid variants by c5_approx
3. EVALUATE: Only call evaluate_solution on top 1-2 valid variants

## Resolution Sweep (Primary Search)
Order: 1600, 3200, 4000, 6400

For each resolution:
1. EDIT num_intervals to target
2. PROBE to check integral, record c5_approx
3. If |integral - 1| < 0.05:
   - If c5_approx is promising (better than or close to best probe), EVALUATE
   - Keep best full-eval result
4. If constraint fails, try different base_learning_rate or penalty_strength

## Learning Rate and Penalty Tuning
After finding a resolution that passes constraint:
- Try 2-3 LR values: 0.001, 0.003, 0.007, 0.01
- Try penalty_strength: 30, 100, 200, 500
- Always probe first to filter

## When to Expand Initialization
Only if resolution sweep fails:
- Add ONE new pattern to _get_best_initialization():
  - Four-peak Gaussian: centers at 0.25, 0.5, 0.75, 1.0, width=0.12
  - Code: latent = sum([4 * np.exp(-((x-c)/0.12)**2 * 15) for c in [0.25,0.5,0.75,1.0)])
- Restart resolution sweep
