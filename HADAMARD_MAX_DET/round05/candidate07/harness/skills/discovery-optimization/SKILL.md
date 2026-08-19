---
name: discovery-optimization
description: "29x29 Hadamard optimizer using ONLY Paley construction. 3 cooling schedules (8.0/3.0/1.0), 3 seeds per schedule, 2 escape patterns. Total ~11 searches, <250s runtime. Probe cooling schedules before evaluate."
---

# 29x29 Hadamard Matrix Optimization

## Task
Maximize |det(H)| for 29×29 ±1 matrix using Paley construction.

## CORRECT PALEY CONSTRUCTION
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For H[i][j]: diff = (i - j) % 29; H[i][j] = 1 if diff in residues else -1

## WORKFLOW (11 searches, ~240s total)

### PHASE 1: Three Cooling Schedules (9 searches)
For EACH of 3 schedules, run 3 seeds:

Schedule A (Broad): T=8.0, cool_rate=0.995, iterations=5000
Schedule B (Medium): T=3.0, cool_rate=0.997, iterations=15000
Schedule C (Fine): T=1.0, cool_rate=0.998, iterations=20000

Seeds per schedule: [42, 12345, 9998877]

Track best_det and best_matrix across all 9 searches.

### PHASE 2: Two Escape Attempts (2 searches)
From best_matrix above:

Escape A: Flip 100 random positions → run hill climb T=10.0, cool_rate=0.999, iters=5000
Escape B: Flip checkerboard where (i+j)%4==0 → run hill climb T=5.0, cool_rate=0.997, iters=5000

### PHASE 3: Selection
Return the matrix with highest |det| across all 11 searches.

## IMPLEMENTATION DETAILS

- Use numpy.linalg.det for ALL determinant calculations (fast, ~0.001s per call)
- Total iterations: ~9×20000 + 2×5000 = 190000 flips
- Expected time: ~12-14 searches × 20s = 240s (within 250s budget)
- Print "Completed search N/M" every 5000 iterations for progress tracking
- Use random.seed(seed) for reproducibility

## PROBE STRATEGY
Before full evaluation:
1. Call probe_solution with 3 variants: (A) Schedule A only, (B) Schedule B only, (C) Schedule C only
2. Pick best probe result
3. Run full evaluation on that variant

## CRITICAL CONSTRAINTS
- Total runtime MUST be <250 seconds
- Use ONLY Paley construction (no random initialization)
- numpy.linalg.det for all iterations (never Bareiss during search)
- Complete all 11 searches before returning
- Print progress every 5000 iterations
