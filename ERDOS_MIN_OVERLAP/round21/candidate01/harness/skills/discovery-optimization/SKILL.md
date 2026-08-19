---
name: discovery-optimization
description: "Generate diverse step function initializations for Erdos optimization using small intervals (N=400) for fast analytical screening."
---

# Fast Candidate Generation Strategy

## Problem
We need to find a step function h: [0,2]->[0,1] with integral=1 minimizing max_k ∫h(x)(1-h(x+k))dx.

## Solution: Generate many fast candidates (N=400 intervals) and screen analytically

## Workflow

1. CALL generate_fast_candidates(temperature=0.7)

2. EXAMINE all 12 candidates:
   - Check integral (should be ~1.0)
   - Note c5_bound (precomputed analytical score)

3. FILTER candidates:
   - SKIP if integral != 1.0 (constraint violation)
   - SKIP if c5_bound >= 0.375 (too bad, won't beat current best)
   - KEEP all with c5_bound < 0.375

4. CALL evaluate_solution on all kept candidates (typically 3-6)

5. If best evaluation beats seed, CALL generate_refine_candidates with best N=400 result

6. Continue until evals exhausted or c5_bound < 0.380923

## Mathematical Patterns Used
- Bipartite: h(x) ≈ 1 for x < a, 0 otherwise (separated support)
- Tri-modal: three narrow peaks at different locations
- Random perturbations of deterministic patterns
- Golomb ruler-like spacing

## Why Fast Intervals Work
- N=400 gives 5x faster analytical evaluation than N=800
- Analytical c5_bound is exact (not approximate)
- Can screen 12x more candidates in same budget
- Only evaluate promising ones in full precision

## Expected Results
With 12 fast candidates, expect 2-5 to pass c5 < 0.375 filter.
Evaluate 3-5, refine best with N=800 if promising.
