---
name: discovery-optimization
description: "n=29 Hadamard optimizer. Start with correct Paley base, run 5 different cooling schedules (50k-60k iters each, various temps), pick best. Use numpy det for search, Bareiss only for final check. Optional escape: flip checkerboard pattern. Total time <200s."
---

# Hadamard Optimization n=29 (Focused Strategy)

## Task
Maximize |det(H)| for 29×29 ±1 matrix. n≡3 (mod 4).

## BASE CONSTRUCTION (Don't Change!)
Use the SEED's Paley construction with quadratic residues:
QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For H[i][j]: diff = (i-j) mod 29; H[i][j] = 1 if diff in QR else -1

## STRATEGY: 5 COOLING SCHEDULES (Depth over Breadth)
Run simulated annealing on the SAME base matrix with 5 different cooling schedules:

Schedule A: 50000 iterations, temp=5.0, cool_rate=0.998
Schedule B: 50000 iterations, temp=4.0, cool_rate=0.9975
Schedule C: 60000 iterations, temp=3.0, cool_rate=0.9965
Schedule D: 40000 iterations, temp=2.0, cool_rate=0.997
Schedule E: 50000 iterations, temp=1.5, cool_rate=0.9985

Keep the BEST result across all 5 schedules.

## OPTIONAL ESCAPE (Only if time permits)
From the best schedule result:
- Flip all positions where (i+j) % 4 == 0
- Run 20000 iterations with temp=10.0, cool_rate=0.999

## DETERMINANT
- SEARCH: numpy.linalg.det (~0.001s per 29×29 matrix)
- FINAL VALIDATION: Bareiss (exact integer arithmetic)
- NEVER use Bareiss during hill climbing (timeout!)

## IMPLEMENTATION
- Import numpy, random
- Implement ONE construct_paley_base() function
- Implement ONE simulate_annealing(matrix, iterations, temp, cool_rate) function
- Call simulate_annealing 5 times with different params
- Track best result across all 5 runs
- Optionally add escape pattern
- Return the best matrix

## TIMING CHECK
- 200k total iterations × 0.001s = 200 seconds
- Plus setup/overhead: <5 seconds
- Total: <205 seconds (well under 350s budget)
