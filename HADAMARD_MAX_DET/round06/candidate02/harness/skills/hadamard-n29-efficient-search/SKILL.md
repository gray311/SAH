---
name: hadamard-n29-efficient-search
description: Efficient search for n=29 Hadamard near-optimal matrices. Use 6 parallel hill climbs of 15k iters, T=3.0, cool=0.997. Always use probe_solution before evaluate_solution. Total time < 180s, numpy.det only.
---

# Efficient Hadamard Search for n=29

## Construction
Build Paley matrix from quadratic residues mod 29:
{0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

## Search Strategy
Run 6 parallel hill climbs:
- Start from 6 different random seeds for construction
- Each: 15,000 iterations, T=3.0, cool_rate=0.997
- Use numpy.linalg.det for ALL determinant calculations

## Perturbation Phase
- Take best result from parallel searches
- Apply 100 random ±1 flips
- Run additional 5,000 iterations with T=2.0, cool_rate=0.998

## Budget Discipline
- Total runtime MUST be < 180 seconds
- Call probe_solution to test parameter variations before evaluate_solution
- NEVER use Bareiss during search (causes timeout)
- Use exactly 6 starting seeds

## Workflow
1. Construct 6 Paley bases with seeds [1,2,3,4,5,6]
2. Run parallel hill climbs (15k iters each)
3. Apply perturbation to best result
4. Use check_hadamard_quality on bases if available
5. Call probe_solution on different parameter variants
6. Call evaluate_solution on the best variant
7. Iterate with more seeds/iterations if budget allows
