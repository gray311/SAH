---
name: discovery-optimization
description: "Iteratively optimize an expert parallelism load balancer algorithm to maximize combined_score (balance + efficiency) under a fixed evaluation budget."
---

# EPLB Optimization Strategy

This task requires improving the expert rearrangement algorithm for Mixture-of-Expert models. The algorithm must:
1. Achieve better load balancing across experts
2. Be more efficient (faster execution)

## Scoring
- combined_score is higher-is-better
- The evaluator checks both balance and efficiency
- Validity=0 if constraints are violated or the program errors

## Method
1. **Analyze the seed**: Understand the current algorithm's structure and identify which part needs improvement.

2. **Propose ONE structural change**: 
   - Change the packing heuristic in `balanced_packing`
   - Modify the replication logic in `replicate_experts`
   - Alter the hierarchical arrangement in `rebalance_experts_hierarchical`
   - Try different sorting strategies or data structures

3. **Implement with targeted diff**: 
   - Use SEARCH/REPLACE for small changes
   - Use full rewrite only for structural changes
   - Keep the fixed entry function and imports identical

4. **Evaluate once per idea**: 
   - `evaluate_solution` returns combined_score, validity, and error
   - If improved, build on it. If errored, fix the specific cause. If regressed, try a different direction.

5. **Budget management**: 
   - You have 20 evaluations. Spend wisely.
   - When `evaluations_left < 5`, consolidate on the best idea.

6. **Restart when stalled**: 
   - If no improvement after 3 tries, try a genuinely different approach.
   - Do not tune the same losing idea.

7. **Finish**: 
   - When budget exhausted or no improvement possible, call finish with a summary of the winning approach and score.

## Common Pitfalls
- Editing only cosmetics (whitespace, comments) without algorithmic change
- Running the same idea multiple times without learning
- Violating the fixed entry function signature
- Fabricating scores (only returned evaluate_solution results count)
