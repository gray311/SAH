---
name: fast-candidate-screening
description: Generate many fast candidates (N=400) and screen them with precomputed analytical scores. Only evaluate candidates with c5_bound < 0.375 to beat current best.
---

# Fast Candidate Screening Strategy

## Problem
Current best: C5 <= 0.380923. We need many cheap candidates to find promising ones.

## Solution: generate_fast_candidates (N=400) + analytical screening

## Workflow

1. CALL generate_fast_candidates(temperature=0.7)

2. EXAMINE all 12 candidates:
   - Check integral (should be ~1.0)
   - Note c5_bound (precomputed analytical score)

3. FILTER candidates:
   - SKIP if integral != 1.0
   - SKIP if c5_bound >= 0.375
   - KEEP if c5_bound < 0.375

4. CALL evaluate_solution on ALL kept candidates (typically 3-6)

5. If best beats seed, refine with N=800 intervals

## Why This Works
- N=400 is 5x faster than N=800 for analytical evaluation
- Analytical c5_bound is exact (not approximate)
- Screen 12x more candidates in same budget
- Only evaluate promising ones in full precision

## Expected Results
With 12 candidates, expect 2-5 to pass c5 < 0.375 filter.
This gives multiple chances to find improvements.
Budget: ~3-6 full evaluations max.
