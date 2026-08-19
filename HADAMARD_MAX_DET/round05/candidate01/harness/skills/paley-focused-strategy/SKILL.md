---
name: paley-focused-strategy
description: Focused strategy for n=29 Hadamard optimization using correct Paley construction with simulated annealing refinement.
---

# Focused Paley Hadamard Strategy for n=29

## Core Principle
Start with the mathematically correct Paley construction (n=3 mod 4 case), then refine with simulated annealing.

## Step-by-Step Workflow

### 1. Paley Construction (MUST BE CORRECT)
Quadratic residues mod 29: **{0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}**
For each entry: H[i][j] = 1 if (i-j) mod 29 in residues, else -1

### 2. Simulated Annealing (ONE focused search)
- Iterations: Exactly 50,000 (not 40k, not 60k)
- Initial temperature: T = 10.0
- Cooling rate: 0.9985
- Mutations: Flip one random entry at a time
- Acceptance: Accept all improvements; accept worse moves with probability exp(-delta/T)
- Best tracking: Keep best matrix seen

### 3. Multiple Seeds (3 only, in budget)
Try seeds: [42, 123, 456]
Run separate annealing for each, keep the best result.

### 4. Verify with Tools
- Call verify_paley_residues to ensure your construction is correct
- Call analyze_matrix_structure to assess quality

### 5. Targeted Fine-Tuning (if needed)
If first pass gives |det| < 10^10:
- Use best result as starting point
- 10,000 iterations with T=5.0, cool_rate=0.999
- Same deterministic seed as before

## Budget Discipline
- Total time MUST be < 300 seconds
- 50k iterations with numpy det = ~50 seconds
- 3 seeds = 150 seconds
- Tool calls = ~20 seconds
- Total: ~170 seconds

## Critical Success Factors
- Exactly 50,000 iterations (not more!)
- Exactly 3 seeds (42, 123, 456)
- Correct Paley residues (verify with tool)
- numpy.linalg.det for ALL determinant calls
- No Bareiss, no complex constructions
- Use probe_solution only to compare 2-3 seed variations
- Call evaluate_solution only once on final best

## Example Code Structure
paley_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
palley_base = [[1 if (i-j)%29 in palley_residues else -1 for j in range(29)] for i in range(29)]

def anneal(start_matrix, seed, iterations, temp, cool_rate):
    # Standard SA implementation
    # Use numpy.linalg.det for ALL det calculations
    
for seed in [42, 123, 456]:
    result = anneal(palley_base[:], seed, 50000, 10.0, 0.9985)
    # Track best

return best_result
