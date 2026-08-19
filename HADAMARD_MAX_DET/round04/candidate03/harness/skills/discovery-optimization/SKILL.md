---
name: discovery-optimization
description: "Paley-based Hadamard optimizer for n=29. Single method focus. 10 seeds with 15k iterations each. T=8.0, cool=0.9975. numpy.det only. Total <200s."
---

# Hadamard Optimization for n=29 (Paley-focused)

## The Paley Construction (n ≡ 3 mod 4)
Quadratic residues mod 29: QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

Build base matrix: H[i][j] = 1 if (i-j) mod 29 ∈ QR else -1

## Optimized Simulated Annealing
Parameters (TUNED for 350s budget):
- Iterations: 15,000 per seed
- Seeds: 10 (42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021)
- Initial temperature: 8.0
- Cooling rate: 0.9975
- Determinant: numpy.linalg.det (fast)

Algorithm:
1. For each seed:
   a. Copy Paley base to current matrix
   b. For iteration in 1..15000:
      - Pick random cell (i,j)
      - Flip sign: current[i][j] *= -1
      - new_det = abs(numpy.linalg.det(current))
      - old_det = best_det_from_this_seed
      - delta = new_det - old_det
      - If delta > 0: accept
      - Else if T > 1e-10 and rand() < exp(delta/T): accept with probability
      - If accepted: update best for this seed, old_det = new_det
      - T *= cool_rate
   c. Keep best matrix from this seed
2. Return best across all 10 seeds

## CRITICAL RULES
- ONLY use numpy.linalg.det during search (Bareiss causes timeout)
- Total iterations: 150,000 flips → ~150 seconds
- Start immediately; no intermediate validation
- Return the single best 29×29 ±1 matrix
