---
name: diversity-first-search
description: Use generate_candidates to create diverse step functions, probe to screen, then evaluate the best. Focus on structural diversity rather than hyperparameter tuning.
---

# Diversity-First Search for Erdos C5

## Workflow

1. CALL generate_candidates (once per iteration)
   - Creates 5 diverse step function structures
   - Each satisfies: values in [0,1], integral = 1

2. CALL probe_solution on each candidate
   - Screen for c5_bound < 0.381
   - Keep top 3-5 candidates

3. CALL evaluate_solution on best 2-3 candidates
   - If combined_score > 1.0, CALL finish

4. If no improvement, repeat from Step 1

## Key Points

- generate_candidates handles constraint satisfaction (integral=1, values in [0,1])
- Use probe to efficiently screen many candidates
- Focus on structural diversity (bipartite, trimodal, piecewise, etc.)
- Don't waste evaluations on candidates with c5_bound >= 0.381
