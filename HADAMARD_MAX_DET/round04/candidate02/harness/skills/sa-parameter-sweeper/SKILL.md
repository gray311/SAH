---
name: sa-parameter-sweeper
description: Specialized skill for Simulated Annealing parameter optimization on Hadamard matrices. Systematically test different (temp, cool_rate) combinations to find the best SA schedule. Focus on the 6-parameter sweep strategy with 30k iters per combo.
---

# Simulated Annealing Parameter Sweeper for Hadamard Matrices

## Objective
Find optimal (initial_temp, cool_rate) parameters for SA optimization of 29x29 +/-1 matrix.

## Parameter Sweep Protocol

### Phase 1: Broad Exploration (Quick Tests)
Test these parameter combinations with 5,000 iterations each:
- High energy: (20.0, 0.9998), (15.0, 0.9995), (10.0, 0.999)
- Medium energy: (8.0, 0.998), (6.0, 0.997), (5.0, 0.996)
- Low energy: (4.0, 0.9965), (3.0, 0.995), (2.0, 0.994)

### Phase 2: Full Optimization (Best Performers)
For top 3 performing parameter combinations:
- Run 30,000 iterations with 3 different seeds
- Track best determinant found

### Phase 3: Mutation Enhancement
From the best result, apply these mutations with 20k iterations each:
- Checkerboard flip: (i+j) mod 4 == 0
- Corner flip: 8x8 top-left submatrix
- Random 30% flip: Flip 30% of random positions

## Critical Rules
- Use numpy.linalg.det for ALL iterations (fast, ~0.001s per matrix)
- NEVER use Bareiss during search (causes timeout)
- Keep total time < 300 seconds
- Call det_optimizer_probe tool FIRST to validate your parameters

## Expected Performance
- Paley construction baseline: ~170-180
- Optimized SA: ~180-200+
- With mutations: Potentially 200+

## Implementation Checklist
[ ] Correct Paley residues: (0,1,4,5,6,7,9,13,16,20,22,23,24,25,28)
[ ] 6 parameter combos tested in Phase 1
[ ] Top 3 expanded to 30k iters in Phase 2
[ ] 3 mutations applied in Phase 3
[ ] numpy.linalg.det used exclusively
[ ] Total iterations: ~720k (expected time ~72s)
