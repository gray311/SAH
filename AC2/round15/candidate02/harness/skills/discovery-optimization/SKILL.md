---
name: discovery-optimization
description: "Hybrid internal search + diverse exploration protocol. Use local_search_optimizer to thoroughly explore neighborhoods of promising candidates before spending full evaluations. Never refine the same pattern class >5 times without trying internal search first."
---

# Hybrid C₂ Maximization Protocol

## Phase 1: Internal Search Initialization (Iteration 1)

1. Call local_search_optimizer ONCE with the seed program.
   - This tool generates 5-10 variants internally by perturbing the seed
   - It uses probe_solution (30 probe budget) to rank them
   - Returns the best internal variant with probe score
2. If the returned variant has probe score > current best (1.03896), call evaluate_solution ONCE to confirm.
3. If this confirms improvement: refine it slightly with 1-2 more internal searches.
4. If no improvement: proceed to Phase 2.

## Phase 2: Diverse Exploration

1. Call generate_candidates to get 3-5 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Asymmetric multi-level steps

2. For EACH proposal:
   - Call local_search_optimizer to generate 3-5 internal variants
   - Probe all internal variants (30 probe budget total for this phase)
   - Select the best internal variant by probe score
   - Call evaluate_solution ONCE if probe score > current best

3. If ANY proposal beats the record: refine it with 1-2 more internal searches.
4. If none beat the record: try completely new families in next iterations.

## Phase 3: Stalled Recovery

If stuck after 10 iterations:
- Call local_search_optimizer on the current best with different perturbation strategies
- OR call generate_candidates with new families
- NEVER refine the same variant >3 times without internal search

Key Rule: INTERNAL SEARCH beats random exploration. Always use local_search_optimizer to refine promising candidates before full evaluation.
