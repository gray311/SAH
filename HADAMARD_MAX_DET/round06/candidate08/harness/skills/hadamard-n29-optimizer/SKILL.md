---
name: hadamard-n29-optimizer
description: Specialized skill for n=29 Hadamard optimization. n=29 ≡ 3 mod 4, so Paley construction applies. Use correct Paley construction, numpy det for fast search, 25k+ iterations, 5 seeds, 3 cooling schedules. Always probe before evaluate.
---

# Hadamard Matrix Optimization for n=29 (Specialized)

## Task
Maximize |det(H)| for a 29×29 matrix with entries ±1.
Since 29 ≡ 3 (mod 4), true Hadamard matrices don't exist, but we can find near-optimal solutions.

## CRITICAL: Correct Paley Construction
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

For each entry H[i][j]:
  diff = (i - j) mod 29
  H[i][j] = 1 if diff in quadratic_residues else -1

This construction is mathematically sound for n ≡ 3 mod 4.

## Determinant Calculation Strategy
- SEARCH PHASE: Use numpy.linalg.det (fast, ~0.001s per 29×29 matrix)
- VALIDATION PHASE: Use Bareiss only on final candidates to confirm exact integer det
- NEVER use Bareiss during hill climbing (causes timeout)

## Recommended Parameters
- Iterations per seed: 25,000 (not 10,000)
- Number of seeds: 5 (not 3-4)
- Total flips: 125,000
- Expected time with numpy: ~15 seconds (well under 350s budget)
- Cooling schedules to try:
  1. T=2.5, cool_rate=0.995
  2. T=1.0, cool_rate=0.998
  3. T=5.0, cool_rate=0.992

## Multi-Method Search
Try these constructions in parallel:
A. Paley + hill climbing (5 seeds, 25k iters each)
B. Random matrix + hill climbing (3 seeds, 10k iters each)
C. Perturbed Paley (3 seeds, 10k iters each)

Pick the BEST result across all methods.

## Budget Management
- Total time per evaluation: MUST be < 180 seconds
- If any method exceeds 60s, immediately reduce iterations
- Use probe_solution to test 2-3 parameter variations BEFORE evaluate_solution

## Workflow
1. Start with correct Paley construction
2. Replace Bareiss with numpy.linalg.det for search
3. Set: iterations=25000, seeds=5, 3 cooling schedules
4. Call edit_solution with full working code
5. Call probe_solution on variants with different cooling schedules
6. Call evaluate_solution on the probe winner
7. If score improves, try: more iterations, different seed range
8. If score doesn't improve, try: random starts, perturbations
9. Repeat until budget exhausted or clear plateau

## Checkpoints
- ✅ Paley residues correct: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
- ✅ Using numpy.linalg.det for search
- ✅ 25,000 iterations per seed
- ✅ 5 seeds per evaluation
- ✅ 3 cooling schedules tried
- ✅ probe_solution used before evaluate_solution
- ✅ Total time < 180s
