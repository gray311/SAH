---
name: analytical-screening
description: Use generate_ready_candidates for cheap integral-constrained initialization screening.
---

# Analytical Screening for Erdos Problem

## Workflow

1. CALL generate_ready_candidates(temperature=0.5)

2. EXAMINE the 3 returned candidates:
   - Each has precomputed integral and c5_bound
   - Candidates are already sigmoid-scaled (h in [0,1])
   - Candidates are integral-normalized (sum ~ 1)

3. FILTER candidates:
   - SKIP if integral != 1.0 (constraint violation)
   - SKIP if c5_bound >= 0.375 (too bad for full eval)
   - KEEP if c5_bound < 0.37

4. CALL evaluate_solution on ALL kept candidates

5. If no improvement, repeat with temperature=0.8

## Why Analytical Screening Works

- No training needed: c5_bound computed via FFT (analytical)
- Integral check: exact, no approximation
- Fast: generates all 3 in one tool call
- Budget-efficient: 1 tool call, 2-3 evals max

## Expected Results

With this tool, you should find c5_bound < 0.37 candidates quickly,
then spend only 2-3 evals to confirm improvements.
