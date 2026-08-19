---
name: multi-candidate-search
description: Generate many diverse initializations and screen them with precomputed scores. Evaluate only the best candidates (c5_bound < 0.36).
---

# Multi-Candidate Search Strategy

## Workflow

1. CALL generate_many_candidates(temperature=0.7)

2. EXAMINE all 12 candidates:
   - Check integral (should be ~1.0)
   - Note c5_bound (precomputed analytical score)

3. FILTER candidates:
   - SKIP if integral != 1.0 (constraint violation)
   - SKIP if c5_bound >= 0.36 (too bad)
   - KEEP all with c5_bound < 0.36

4. CALL evaluate_solution on all kept candidates (typically 2-5)

5. If no improvement, CALL generate_many_candidates with temperature=0.9
   for more exploration

## Why This Works

- 12 diverse patterns: random, threshold, bipartite, tri-modal, Golomb, wave
- Precomputed analytical scores: no training needed
- Multiple seeds: each pattern varied with different random seeds
- Budget-efficient: 1 tool call, 2-6 evals max

## Expected Results

With 12 candidates, we expect 2-5 to pass the c5 < 0.36 filter.
This gives us multiple chances to find improvements.
