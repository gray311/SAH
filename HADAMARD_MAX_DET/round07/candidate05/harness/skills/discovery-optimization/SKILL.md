---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Multi-construction pipeline: build 3-5 matrices via\nPaley, random, and block patterns; refine each with row swaps and 2x2 block flips;\npick best. DO NOT use SA with many iterations. Use numpy.linalg.det for all scoring."
---

# Hadamard Matrix Construction Pipeline - Multi-Strategy Approach
## Problem
Maximize |det(H)| for 29x29 matrix with entries ±1.

## Why SA Fails
- SA makes tiny random flips (one element at a time)
- 10M flips needed to escape local optimum
- Waste of time when we have 20 evals

## Better Approach: Multi-Construction Pipeline

### Strategy 1: Paley Construction (seed's approach)
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For H[i][j]: diff = (i-j) mod 29; H[i][j] = 1 if diff in residues else -1

### Strategy 2: Random Construction
Generate 29x29 matrix with random ±1 entries.

### Strategy 3: Block-Pattern Construction  
Create base 4x4 pattern, repeat and adapt to 29x29.

### Strategy 4: Permuted Paley
Take Paley matrix, permute rows/columns randomly, then refine.

## Refinement Operations (apply to EACH construction)

Operation A: Row/Column Swap
- Swap row i with row j; swap col i with col j
- Preserves |det| exactly
- Breaks local patterns

Operation B: 2x2 Block Flip
- Flip 4 elements in a 2x2 block: H[r,c], H[r+1,c], H[r,c+1], H[r+1,c+1]
- Changes det but respects local structure
- Try at 10 different positions

Operation C: Cyclic Row Shift
- Shift all rows cyclically by k positions
- Breaks symmetry

## Algorithm

Build 4 different constructions. For each:
- Apply 50 refinement steps using random operations from {A, B, C}
- Track best determinant

Total: 4 constructions × 50 refinements = 200 operations
Time: 200 × 0.001s per det + overhead ≈ 30s, well under 350s budget

DO NOT use simulated annealing with 10k+ iterations.
DO NOT use Bareiss during search (causes timeout).
Use numpy.linalg.det for ALL determinant calculations.

Return the single best matrix across all constructions.
