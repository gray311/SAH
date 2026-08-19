---
name: discovery-optimization
description: "Paley-only optimizer for n=29. Quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}. Build Paley matrix, run 100 restarts with Schedule A (temp=8.0, cool=0.996) and Schedule B (temp=2.0, cool=0.997), each 15k iters. Apply checkerboard perturbation (flip where (i+j)%4==0) then 10k iters with temp=5.0. Total ~16k iters, <20 seconds."
---

# Paley-Only Hadamard Optimizer for n=29

## Task
Maximize |det(H)| for 29×29 ±1 matrix.

## Construction: Paley (CORRECT)
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For each H[i][j]: diff=(i-j) mod 29, H[i][j]=1 if diff in residues else -1

## Hill Climbing Parameters

### Schedule A (High initial temp)
- Initial temperature: 8.0
- Cool rate: 0.996
- Iterations: 15,000
- Purpose: Broad exploration

### Schedule B (Low initial temp)
- Initial temperature: 2.0
- Cool rate: 0.997
- Iterations: 15,000
- Purpose: Fine refinement

### Checkerboard Perturbation (Escape local minima)
- Flip all positions where (i+j) % 4 == 0
- Then run: temp=5.0, cool_rate=0.995, iterations=10,000

## Workflow (EXACT ORDER)
1. Build Paley matrix
2. Run 100 restarts with Schedule A, keep best
3. Run 100 restarts with Schedule B, keep best
4. Apply checkerboard perturbation to the BETTER of step 2/3
5. Run checkerboard escape on the result
6. Return the matrix with highest |det|

## Timing Check
- 200 restarts × 15k iters = 3M flips
- Checkerboard: 10k iters
- Total: ~3.01M flips
- numpy det: ~0.001s per matrix
- Expected time: 3M × 0.001s = 3 seconds << 350s budget

## CRITICAL RULES
- ONLY use numpy.linalg.det during search
- NEVER use Bareiss or integer arithmetic during hill climbing
- Run ALL 200 restarts before any perturbation
- Do NOT add extra construction methods
- Total iterations MUST be under 5M (gives ~3.5s computation time)
