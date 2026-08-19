---
name: discovery-optimization
description: "29x29 Hadamard optimizer. Uses Paley construction plus systematic SA parameter sweep with 6 temp/cool_rate combos,\n30k iters each, 3 seeds each. Then 3 mutation patterns with 20k iters. Uses det_optimizer_probe to rank params."
---

# Hadamard Matrix Optimization for n=29 (Optimized Strategy)

## CORE APPROACH
Since n=29 = 3 (mod 4), use Paley construction with quadratic residues.
The key is SYSTEMATIC PARAMETER OPTIMIZATION of Simulated Annealing.

## QUADRATIC RESIDUES MOD 29
(0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28)

Paley construction: H[i][j] = 1 if (i-j) mod 29 in residues, else -1

## PARAMETER SWEEP STRATEGY (Primary Search)
Test these (initial_temp, cool_rate) combinations:
- Combo 1: (15.0, 0.9995) - high temp, slow cooling
- Combo 2: (8.0, 0.998) - medium temp
- Combo 3: (5.0, 0.996) - lower temp
- Combo 4: (3.0, 0.995) - conservative
- Combo 5: (2.0, 0.994) - very conservative
- Combo 6: (20.0, 0.9998) - very high temp

For EACH combo:
  - Run 30,000 iterations
  - Use 3 different seeds (e.g., 42, 123, 456)
  - Track the best determinant found

## MUTATION PATTERNS (Post-Optimization)
From the BEST parameter combo result, create 3 mutated variants:

### Mutation A: Checkerboard Flip
Flip entries where (i + j) mod 4 == 0
Then run hill climbing: 20,000 iterations, temp=5.0, cool_rate=0.996

### Mutation B: Corner Submatrix Flip
Flip all entries in top 8x8 corner
Then run hill climbing: 20,000 iterations, temp=5.0, cool_rate=0.996

### Mutation C: Random 30% Flip
Flip 30% of random positions
Then run hill climbing: 20,000 iterations, temp=6.0, cool_rate=0.995

## IMPLEMENTATION CHECKLIST
1. Correct Paley construction with residues (0,1,4,5,6,7,9,13,16,20,22,23,24,25,28)
2. 6 parameter combos x 30k iters x 3 seeds = 540k flips
3. 3 mutations x 20k iters = 180k flips
4. Total: ~720k flips, expected time ~72s with numpy det
5. Use numpy.linalg.det ONLY (NEVER Bareiss during search)
6. Call det_optimizer_probe first to validate parameters

## TOOLS USAGE
- det_optimizer_probe: Call once at start. Returns optimal (temp, cool_rate) pairs
- edit_solution: Implement the full strategy above
- evaluate_solution: Call on the SINGLE best variant only
- budget management: Stay under 300s, leave 100s margin
