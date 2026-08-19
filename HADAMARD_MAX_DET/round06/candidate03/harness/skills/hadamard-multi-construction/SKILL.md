---
name: hadamard-multi-construction
description: Specialized skill - Test multiple constructions (Paley, random, perturbed), use numpy.det for fast search, probe before evaluate, focus on hill-climbing.
---

# Hadamard Matrix Multi-Construction Optimizer for n=29

## Key Insight
Since n=29 ≡ 3 (mod 4), true Hadamard matrices don't exist.
Best strategy: test multiple construction methods + hill climb.

## Construction Methods to Test

1. PALEY CONSTRUCTION (mathematically grounded)
   Residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   H[i][j] = 1 if (i-j) mod 29 in residues, else -1

2. RANDOM INITIALIZATION
   Fill matrix with random ±1 entries

3. PERTURBED PALEY
   Start with Paley, flip 10-20% of entries randomly

## Hill Climbing Strategy
For EACH construction method:
  - Run 3-5 different random seeds
  - Per seed: 5,000-10,000 simulated annealing iterations
  - Temperature: 2.0-5.0, cool rate: 0.995-0.997
  - Use numpy.linalg.det for ALL determinants during search
  - Accept if delta > 0, or with prob exp(delta/T)

## Workflow (CRITICAL ORDER)
1. Implement multi-construction code with above methods
2. Call probe_solution on 3-5 variant configurations
3. Pick the best from probe results
4. Call evaluate_solution on the winner
5. If no improvement, try: more iterations, different seeds

## Time Budget
- Total per evaluation: < 300 seconds
- Iterations per variant: 5,000-10,000 (NOT 100,000!)
- Use probe to avoid wasting evaluate budget on poor variants

## Determinant Calculation
- SEARCH PHASE: ALWAYS use numpy.linalg.det (fast)
- NEVER use Bareiss during hill climbing (causes timeout)
- Bareiss only acceptable for final validation if needed
