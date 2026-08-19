---
name: two-phase-c5-search
description: Phase 1 - Generate diverse patterns with search_patterns, screen with probe_solution. Phase 2 - Refine promising candidates (c5_bound < 0.375) with refine_candidate 2-3 times before evaluation. This avoids wasting full evals on unpromising candidates.
---

# Two-Phase C5 Optimization Strategy

## PHASE 1: Pattern Generation and Screening

1. CALL search_patterns(temperature=0.5)
   - Get 5 candidates with analytical c5_bound

2. CALL probe_solution on each candidate
   - Identify candidates with c5_bound < 0.375

## PHASE 2: Targeted Refinement

3. For EACH candidate with c5_bound < 0.375:
   a. CALL refine_candidate(candidate, focus='smoothing', iterations=2)
   b. CALL refine_candidate(result, focus='sharpening', iterations=2)
   c. Keep the best refined candidate (lowest c5_bound)

4. CALL evaluate_solution on ONLY THE BEST refined candidate
   - If combined_score > 1.0, finish
   - If not, go to Phase 3

## PHASE 3: Alternative Patterns

5. CALL search_patterns(temperature=0.8) with focus on different pattern types
   - Try bipartite-only, multi-peak-only

6. Repeat Phase 2 for promising candidates

## Critical Rules

- NEVER evaluate a candidate without refinement if c5_bound < 0.375
- MAX 3 full evaluations (save eval budget)
- refine_candidate is analytical (cheap, can call 2-3x per candidate)
- If no improvement after 2 temperatures, restart with new patterns
