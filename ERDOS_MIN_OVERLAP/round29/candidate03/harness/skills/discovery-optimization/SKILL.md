---
name: discovery-optimization
description: "Phase 1: Generate diverse patterns with search_patterns. Phase 2: Use refine_candidate to iteratively improve promising candidates before evaluation. Focus on peak-sharpening and noise reduction for candidates with c5_bound < 0.375."
---

# Erdos C5 Two-Phase Optimization

## PHASE 1: Pattern Generation (Once at start)

1. CALL search_patterns(temperature=0.5)
   - Generates 5 diverse initializations with analytical c5_bound
   - All satisfy integral=1, h in [0,1]

2. SCREEN with probe_solution on each candidate
   - Keep candidates with c5_bound < 0.375
   - Discard others (waste of eval budget)

## PHASE 2: Targeted Refinement (For promising candidates only)

3. For each candidate with c5_bound < 0.375:
   - CALL refine_candidate(candidate, iterations=2)
     - Applies Gaussian smoothing, peak sharpening, noise reduction
     - Each iteration returns refined candidate with new c5_bound
     - Use analytical c5 (no full optimization needed)
   - Keep the best refined candidate (lowest c5_bound)

4. CALL evaluate_solution on BEST refined candidate only
   - If combined_score > 1.0, finish with summary
   - If combined_score <= 1.0, go to step 1 with different temperature

## PHASE 3: Alternative Patterns (If Phase 1+2 fails)

5. Try search_patterns(temperature=0.8) with different pattern focus:
   - bipartite_only: Generate only threshold patterns
   - multi_peak_only: Generate only multi-peak patterns

6. For promising candidates from phase 3, repeat refinement and evaluation

## Critical Rules

- ALWAYS refine candidates with c5_bound < 0.375 BEFORE evaluation
- NEVER evaluate more than 3 candidates (save eval budget)
- Use probe_solution for screening, refine cheaply, evaluate once
- If stuck, try different temperatures or pattern types in Phase 3
- Maximum 3 refine_candidate calls per promising candidate (cheap, iterative)
