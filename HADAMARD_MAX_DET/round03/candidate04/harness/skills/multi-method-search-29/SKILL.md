---
name: multi-method-search-29
description: Protocol for 29x29 Hadamard optimization. Must try - Paley, Random, Block, Genetic, Permutation. Per eval - test 3-5 variants across DIFFERENT constructions. Probe 5+ before evaluate. Rotate methods each eval. Return global best.
---

# Multi-Method Hadamard Search for n=29

## Why Seed Fails
- Only Paley construction
- Single-entry SA mutations (tiny steps)
- 50k iterations insufficient for 2^58 space

## Required Methods (try ALL 5)

1. PALEY CONSTRUCTION
   residues = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   H[i][j] = 1 if (i-j)%29 in residues else -1
   Try iterations: 30k, 50k, 70k

2. RANDOM + SA
   start = np.random.choice([-1,1], (29,29))
   Try iterations: 30k, 50k, 70k

3. BLOCK CONSTRUCTION
   Divide into H11(14x14), H12(14x15), H21(15x14), H22(15x15)
   Optimize each block, then assemble
   OR flip entire 2x2/3x3 blocks

4. GENETIC ALGORITHM
   pop = 10 matrices
   10 generations:
     - sort by det, keep top 5 (elite)
     - crossover: swap 5-10 rows
     - mutate: flip entries (rate 0.01)
     - keep best 10

5. PERMUTATION SEARCH
   build base matrix
   try 1000 random row permutations
   for each: det + 1k SA if > best

## Protocol

Per evaluation:
- Step 1: Pick 1 construction method
- Step 2: Test 3 parameter sets (e.g., iterations: 30k/50k/70k)
- Step 3: Probe all 3, evaluate best
- Step 4: Pick NEXT construction method (different from before!)
- Step 5: Repeat for all 5 methods

Time: 350s total. If method >180s, abort and try next.

## Rules
- MUST vary CONSTRUCTION across evals
- MUST use numpy.linalg.det for search
- MUST probe 3+ variants before evaluate
- MUST return global best across all methods
- NEVER use Bareiss during search

## Example Schedule
Eval 1: Paley (3 params), probe all, eval best
Eval 2: Random (3 params), probe all, eval best
Eval 3: Block (3 params), probe all, eval best
Eval 4: Genetic (3 params), probe all, eval best
Eval 5: Permutation (3 params), probe all, eval best
