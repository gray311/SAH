---
name: discovery-optimization
description: "Hadamard optimization for n=29. Paley construction from residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}. Apply SA, greedy, random perturbations. Use numpy.linalg.det. 5-8 seeds. Probe before evaluate."
---

Hadamard Optimizer for n=29.
Step 1: Paley Construction
Residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For (i,j): diff = (i-j) mod 29; H[i,j] = 1 if diff in residues else -1

Step 2: Multiple Strategies (run in parallel)
A) SA: T=3.0, cool=0.997, 25k iters. DO NOT undo flips.
B) Greedy: Try all 29x29 neighbors, pick best improvement.
C) Random: Flip 3-8 positions, accept if better.

Step 3: Try 5-8 seeds from [42,123,456,789,2024,2025,2026,2027]

Step 4: Use numpy.linalg.det for search (never Bareiss)

Step 5: Time < 180s, probe before evaluate.

Expected: exceed seed score 0.545692.
