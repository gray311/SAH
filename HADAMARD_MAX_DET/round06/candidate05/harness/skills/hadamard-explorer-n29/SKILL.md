---
name: hadamard-explorer-n29
description: Explore Hadamard optimization for n=29 using multiple construction methods. Key insight - Paley alone is insufficient. Try random starts, perturbed Paley. Use probe_solution extensively (30 probes available) to test parameters before full evaluation.
---

# Hadamard Matrix Explorer for n=29

## KEY INSIGHT
The seed program's Paley construction with annealing gets stuck in a local optimum.
You MUST explore beyond this.

## Multiple Construction Methods
ALWAYS try these in parallel:

1. **Paley Construction**
   Residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   H[i][j] = 1 if (i-j)%29 in residues else -1

2. **Random ±1 Matrix**
   Randomly initialize all entries to ±1

3. **Perturbed Paley**
   Start with Paley, flip 5-20 random entries

## Parameter Tuning Strategy
Use probe_solution to test these combinations:

| Parameter | Range |
|-----------|-------|
| Initial T | 1.0, 2.5, 5.0, 10.0 |
| Cool rate | 0.992, 0.995, 0.997, 0.998, 0.999 |
| Iterations/seed | 10k, 25k, 50k, 75k |
| Num seeds | 3, 5, 8, 12 |

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinants during search (NOT Bareiss)
- Complete ALL work within 300 seconds per evaluation
- Use probe_solution FIRST: test 10-20 variants, pick best, then evaluate
- If probe scores are similar, try MORE construction methods or different seeds

## Workflow per Evaluation
1. Implement code with all 3 construction methods
2. Call probe_solution with 15 different (method, T, cool, iters, seeds) combos
3. Pick top 2 variants by probe score
4. Call evaluate_solution on each (if budget allows)
5. Return the absolute best matrix

## Example probe call structure
Test variants with combinations like:
- (Paley, T=5.0, cool=0.997, iters=25k, seeds=6)
- (Random, T=2.5, cool=0.995, iters=50k, seeds=8)
- (Perturbed_Paley, T=10.0, cool=0.992, iters=10k, seeds=4)

## Checkpoints
- ✅ Implemented all 3 construction methods
- ✅ Using numpy.linalg.det (not Bareiss)
- ✅ Using probe_solution for parameter exploration
- ✅ Staying under 300 seconds
- ✅ Returning best matrix across all methods
