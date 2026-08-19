---
name: bound-filtered-search
description: Structured initialization with bound-probe filtering for Erdős C5. Generate diverse starts, filter by cheap bound_probe, optimize promising candidates, evaluate only top ones. Avoid wasting evaluations on weak candidates.
---

# Bound-Filtered Search for Erdős C5

## Overview
1. Generate diverse initializations using construct_structured_init().
2. For each candidate, call bound_probe() to get a fast approximate c5_bound.
3. If bound_probe >= 0.385, discard it (too weak).
4. Else, run optimization from this candidate for 20k–30k steps.
5. After optimizing several, call bound_probe again to rank candidates.
6. Keep the top 2–3 candidates and run evaluate_solution on them.
7. Report the best combined_score.

## Why This Works
- bound_probe is ~10x faster than evaluate_solution and does not consume the limited evaluation budget.
- Random/unstructured candidates waste evaluations. Filter them out first.
- Optimizing from bad starts often converges to worse local minima.

## Initializations to Generate
- bimodal_tight: Two narrow peaks at 0.25 and 0.75.
- triangular_3step: 3-level linear ramps.
- periodic_2: Alternating pattern on [0,0.5]/[0.5,1] (repeat on [1,2]).
- golomb_5: Peaks at optimal spacing from Golomb ruler.
- piecewise_const_2/3: Simple step functions with k levels, integral normalized to 1.

## Optimization Tips
- Use adaptive learning rate and penalty: start with lr=0.02, penalty=5000; later lr=0.003, penalty=15000.
- If bound_probe stays high after optimization, the candidate is likely non-viable; move on.
- Always call bound_probe BEFORE optimize and AFTER optimization.

## Final Instructions
- Implement bound_probe() and construct_structured_init() in the EVOLVE-BLOCK.
- Follow the bound-filtered search workflow to improve the score.
