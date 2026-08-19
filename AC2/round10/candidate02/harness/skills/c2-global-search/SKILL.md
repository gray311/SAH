---
name: c2-global-search
description: Systematic exploration of function classes for C₂ optimization. When scores plateau, switch to a new function family.
---

# C₂ Global Search Protocol

## When to Use
- At iteration 0 or when no improvement after 5 iterations
- When probe scores are not exceeding current best
- When stuck in the same function family

## Protocol
1. **Call explore_function_classes** with diversity_mode="balanced" and num_candidates=80
   - This explores: step variants, sigmoid functions, mixtures, asymmetric patterns, high-resolution discretizations

2. **Probe top candidates**: Call probe_solution on the 10 suggested indices
   - Rank by probe score
   - Keep top 3 for potential evaluation

3. **Evaluate best**: If top probe > current best by >2%, call evaluate_solution

4. **Refine or pivot**:
   - If eval improves: refine the winner with 5 targeted mutations
   - If no improvement after 3 evals: go back to step 1 with diversity_mode="smooth_only" or "asymmetric_only"

## Diversity Modes
- "balanced": Mix of all function classes (recommended at start)
- "steps_only": Only step function variants
- "smooth_only": Sigmoid/gaussian-like smooth functions
- "mixture_only": Weighted combinations of base functions
- "asymmetric_only": Peaks shifted off-center
- "high_res": Fine-grained discretization (600-1000 intervals)

## Key Insight
The seed program's step functions may be a local optimum. Smooth functions, mixtures, or asymmetric patterns may achieve higher C₂.
Don't get stuck refining one pattern class - systematically explore alternatives.
