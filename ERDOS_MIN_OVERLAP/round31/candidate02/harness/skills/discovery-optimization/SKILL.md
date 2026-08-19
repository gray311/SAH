---
name: discovery-optimization
description: "Use get_correlation_profile to identify high-overlap shifts, then targeted_h_optimizer to create mutations reducing overlap at those shifts. Always call probe before full eval."
---

# Erdos C5 Optimization - Targeted Mutation Strategy

## Phase 1: Get Correlation Profile

1. CALL get_correlation_profile on the current best program
   - This computes overlap for all shifts k
   - Returns top 3 problematic k values where overlap is highest

2. EXAMINE the problematic shifts
   - These k values have max h(x)(1-h(x+k))
   - We need to reduce this by modifying h

## Phase 2: Targeted Optimization

1. CALL targeted_h_optimizer with:
   - problematic_k: the top 3 k values from correlation profile
   - strategy: "spread_peaks" (create separated narrow peaks)
   - or strategy: "asymmetric" (create asymmetric step function)

2. The tool generates new h arrays that:
   - Reduce overlap at the specified k values
   - Maintain integral(h) = 1
   - Keep h in [0,1]

## Phase 3: Screening and Evaluation

1. CALL probe_solution on each mutation candidate
   - Keep candidates with c5_bound < 0.375

2. CALL evaluate_solution on the best 1-2 candidates
   - If combined_score > 1.0, call finish

## If No Improvement

Try different strategies in targeted_h_optimizer:
- "spread_peaks": Multiple narrow peaks separated by ~0.5-1.0
- "asymmetric": Step function with different thresholds left/right
- "bimodal": Two distinct peaks

NEVER do random mutations without analyzing correlation first.
