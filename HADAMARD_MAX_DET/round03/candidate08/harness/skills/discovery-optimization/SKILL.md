---
name: discovery-optimization
description: "Optimize 29\u00d729 Hadamard-like matrix for max |det|. n=29\u22613 mod 4, use Paley construction.\nCRITICAL: Standard SA is stuck at 0.510438. When SA stalls, use BLOCK mutations,\nSUBBLOCK swaps, and COLUMN cycles. Call block_mutation_scramble after each SA run.\nIf SA result < 0.48, immediately try structured mutations instead.\nAlways probe 2-3 variants before full evaluation. Use numpy.linalg.det exclusively."
---

# Advanced Hadamard Optimization for n=29 (Escape Local Optima)

## Problem: We're stuck at 0.510438 - SA is trapped in local optima

## Solution: Multi-strategy with structured mutations

### Strategy 1: Enhanced Paley + Simulated Annealing (Baseline)
- Correct Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- numpy.linalg.det for all iterations (fast ~0.001s per matrix)
- 25,000 iterations per seed, 5 seeds, 3 cooling schedules
- BUT this alone gives only 0.510438 - we need more!

### Strategy 2: BLOCK Mutations (when SA stalls)
- Flip ENTIRE rows: current_matrix[i] = -current_matrix[i]
- Flip ENTIRE columns: for all i, current_matrix[i][j] = -current_matrix[i][j]
- Why this works: Preserves some structure while making larger jumps

### Strategy 3: SUBBLOCK Swaps
- Extract 3x3 or 5x5 subblocks from different rows
- Swap these subblocks between row groups
- Creates new patterns without completely randomizing

### Strategy 4: COLUMN CYCLES
- Cyclically shift columns: col[j] → col[(j + k) mod n]
- Test shifts k=1,2,3,...,10 to find improving shifts

### Execution Flow
1. Start with Paley + SA (5 seeds, 25k iters each)
2. Run block_mutation_scramble on the best SA result
3. Compare SA result vs scrambled result via probe
4. If scrambled > SA, continue from scrambled
5. If neither improves, try: more iterations OR subblock swaps OR column cycles
6. ALWAYS use probe before evaluate
7. If score < 0.48, immediately switch to structured mutations

### When to use block_mutation_scramble
- After each SA run (as a diversification step)
- When SA result < 0.48 (clearly stuck)
- When you need to escape local optima without random restart

### Tool: block_mutation_scramble
- Flips random rows/columns (2-5 at a time)
- Flips random 3x3 subblocks
- Applies random column cycles (shifts 1-5)
- Returns 3 variants to choose from

### Budget Management
- Total time: MUST be < 180 seconds
- SA (5 seeds × 25k): ~15 seconds
- block_mutation_scramble: ~3 seconds
-留出 50 seconds for more complex mutations if needed
