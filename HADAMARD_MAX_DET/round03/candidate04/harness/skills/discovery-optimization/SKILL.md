---
name: discovery-optimization
description: "Optimize 29x29 +/-1 matrix. Seed stuck at |det|~80. Must try: Paley, Random, Block, Genetic, Permutation constructions.\nProtocol: 3-5 variants per eval across DIFFERENT constructions. Probe 5+ before evaluate. Rotate methods each eval."
---

# Hadamard-like Matrix Optimization for n=29

## Critical mathematical fact
True Hadamard matrices exist only for n = 1, 2, or n ≡ 0 mod 4.
For n=29 (which is 3 mod 4), the best we can do is approximate the theoretical max of n√n ≈ 155.5.
The seed program's score of 0.456713 suggests it's NOT achieving good determinants — likely due to:
- Buggy or slow Bareiss determinant causing timeouts or incorrect results
- Insufficient search (only 10,000 iterations × 10 seeds = 100,000 total flips)
- Suboptimal cooling schedule

## RECOMMENDED APPROACH: Fast Search with Correct Paley Construction

### Step 1: Correct Paley Construction for n=29
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For i, j in 0..28:
  diff = (i - j) mod 29
  H[i][j] = 1 if diff in residues else -1

### Step 2: Fast Determinant Calculation
- Use numpy.linalg.det for all iterations (fast, approximate, good for search)
- Only use Bareiss on final candidates to confirm
- This avoids timeouts and allows more iterations

### Step 3: Extended Search Parameters
- Iterations: 20,000-30,000 per seed (not 10,000)
- Seeds: 3-5 different starting seeds (not just 10 total across all methods)
- Cooling schedule: Try multiple schedules:
  * Schedule A: T = 2.5, cool_rate = 0.995
  * Schedule B: T = 1.0, cool_rate = 0.998
  * Schedule C: T = 5.0, cool_rate = 0.992
- Total operations: 3 seeds × 25,000 iterations = 75,000 flips → ~15 seconds with numpy

### Step 4: Multiple Construction Methods
Try these in parallel or sequence:
A. Correct Paley construction + hill climbing (3 seeds, 25k iters each)
B. Random matrix (seed-based) + hill climbing (3 seeds, 10k iters each)
C. Perturb Paley with random ±1 flips (3 seeds, 10k iters each)
Pick the BEST result across all methods.

### Step 5: Budget Management
- Total time per evaluation: MUST be < 180 seconds
- If any method exceeds 60s, reduce iterations and try again
- Use probe_solution to test 2-3 parameter variations before full evaluation

### Step 6: Implementation Checklist
1. Implement correct Paley construction (use quadratic residues list above)
2. Replace Bareiss with numpy.linalg.det for search phase
3. Set iterations = 25000, seeds = 5, total flips = 125,000
4. Try 3 cooling schedules
5. Wrap everything in try-except with timeout guard
6. Call edit_solution with full working code
7. Call probe_solution on 2-3 variants, then evaluate_solution on the winner

### Common Pitfalls to Avoid
- ❌ Using Bareiss for all iterations (causes timeout)
- ❌ Only trying 1-2 seeds (insufficient exploration)
- ❌ Using only one cooling schedule
- ❌ Running searches longer than 180s total
- ❌ Not implementing Paley correctly (check quadratic residues)
- ❌ Not using probe_solution to pre-filter variants

### Workflow
1. Write code with correct Paley + numpy det + 25k iters + 5 seeds + 3 cooling schedules
2. Call edit_solution
3. Call probe_solution on variants with different cooling schedules
4. Call evaluate_solution on the probe winner
5. If score improves, try: more iterations, different seed range, etc.
6. If score doesn't improve, try: random starts, perturbations, different constructions
7. Repeat until budget exhausted or clear improvement
