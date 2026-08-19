---
name: discovery-optimization
description: "Structured initialization + bound_probe filtering for Erd\u0151s C5. Generate diverse initializations (bimodal peaks, triangular, periodic, Golomb), filter by cheap bound_probe, optimize promising candidates, and evaluate only the top ones. This avoids wasting the limited evaluation budget on bad candidates."
---

# Erdős C5 Optimization – Bound-Filtered Search

## Problem
Minimize max_k ∫_0^2 h(x)(1−h(x+k)) dx over step functions h: [0,2]→[0,1] with ∫h=1.
Current best bound: C5 ≤ 0.38092303510845016. Goal: combined_score > 1.0 (c5_bound < 0.380923).

## Why This Strategy
1) The objective depends on the self-convolution of h and 1−h via FFT.
2) A diverse set of principled constructions often outperforms random initialization.
3) Full evaluation is expensive. Use bound_probe() to quickly filter out bad candidates.
4) Optimize only the promising candidates, then evaluate them.

## Workflow (follow this order):
1. Call construct_structured_init() to get 4–6 diverse initializations.
   - Expect keys like: bimodal_tight, triangular_3step, periodic_2, golomb_5, piecewise_const_2, piecewise_const_3
2. For each candidate h (after sigmoid and integral correction to ∫h=1):
   - Call bound_probe(h) to get an approximate c5_bound.
   - If bound_probe(h) ≥ 0.385, discard it (too weak).
   - Else, run optimization from h for 20k–30k steps with adaptive LR/penalty.
3. After optimizing several candidates, call bound_probe again to rank them.
4. Keep the top 2–3 candidates by bound_probe, then run evaluate_solution on them.
5. Report the best combined_score from the full evaluations.

## Constructed Initializations
- bimodal_tight: Two narrow Gaussian-like peaks at x≈0.25 and 0.75.
- triangular_3step: Linear ramps forming a 3-level pattern.
- periodic_2: Alternating high/low on [0,0.5]/[0.5,1] (and repeat on [1,2]).
- golomb_5: Peaks placed at optimal spacing inspired by Golomb rulers.
- piecewise_const_2/3: Simple step functions with k levels, tuned to ∫h=1.

## Bound-Filtered Optimization
- Always call bound_probe BEFORE optimize.
- Do not evaluate fully if bound_probe is not promising.
- If bound_probe stays high after optimization, the candidate is likely non-viable; move on.

## Final Instructions
- Implement bound_probe() as a fast, subsampled FFT evaluator.
- Implement construct_structured_init() to generate diverse starts.
- Use the strategy above to edit the EVOLVE-BLOCK and improve the score.
