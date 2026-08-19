---
name: discovery-optimization
description: "Construct near-Hadamard matrices for n=29 using mathematical constructions (Paley, quadratic\nresidues) and local optimization, with probe_solution to quickly rank variants before full evaluation."
---

# Hadamard Matrix Optimization for n=29

## Understanding the Problem
You're creating a 29×29 matrix with ±1 entries to maximize |det(H)|. Since 29 is not of form 4k,
no perfect Hadamard matrix exists, but we can construct near-Hadamard matrices with high determinants.

## Known Constructions to Try
1. **Paley Construction (for prime p=29)**: Use quadratic residues mod 29.
   - QR mod 29 = {1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   - Set H[i,j] = 1 if (i-j mod 29) in QR, else -1
 
2. **Seeded Random Initialization**: Create random ±1 matrix, then optimize.
 
3. **Hybrid Approaches**: 
   - Start with structured initialization (QR-based or from known Hadamard matrices)
   - Apply local search (flip entries to increase |det|)
   - Use simulated annealing or randomized hill climbing with many iterations
 
4. **Parameter Variations**:
   - Try different random seeds for initialization
   - Vary the number of local search iterations (within 350s time limit)
   - Adjust annealing schedule
 
## Use probe_solution Strategically
- probe_solution gives a FAST approximate score (sampled determinant) without consuming your evaluation budget.
- Use it to quickly compare construction strategies, seeds, or parameter settings.
- Only call evaluate_solution when probe_solution indicates a promising variant.
- With 20 evaluation budget, you can't afford to evaluate every variant—use probes to prune.

## Evaluation Workflow
1. Edit EVOLVE-BLOCK with a construction strategy.
2. Call probe_solution immediately to check if this strategy is promising.
3. If probe_score is reasonable, call evaluate_solution for full score.
4. Based on feedback, try variations or completely new strategies.
5. Keep track of the best score; you can revert to it automatically.
6. When out of evaluations or no improvements possible, call finish.

## Time Budget Considerations
- Each evaluation has 350s limit. Your code must complete within this.
- Expensive operations: computing full determinant 1000+ times will TLE.
- Prefer: good initialization + moderate local search, or fast scoring strategies.
- Use probe_solution to validate that your approach is directionally correct before spending evaluation budget.

## Remember
- The evaluator checks validity (matrix is 29×29, all entries ±1) and returns combined_score.
- Higher |det| is better. For n=29, expect |det| in range 10^14 to 10^17.
- Use probe_solution to filter: if your construction gives very low probe_score, try something different.
