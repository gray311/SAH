---
name: structure-preserving-search
description: Specialized skill for Hadamard n=29. Focus on structure-preserving mutations (row/col flips, swaps) rather than random single flips. Test 5 cooling schedules via probe. Use numpy.linalg.det for fast search. Total <300s.
---

# Structure-Preserving Hadamard Search for n=29

## Core Insight
For Hadamard-like matrices, random single flips are inefficient.
Structure-preserving mutations (entire row/col flip, row/col swap)
maintain the +/-1 structure better and often escape local minima more effectively.

## Mutation Operators
### Row Flip: Multiply all entries in one row by -1
### Column Flip: Multiply all entries in one column by -1  
### Row Swap: Exchange two rows (det changes sign, |det| unchanged)
### Column Swap: Exchange two columns (|det| unchanged)

## Cooling Schedules (test 3-5 via probe_solution)
1. T=3.0, cool_rate=0.996, iters=30000
2. T=5.0, cool_rate=0.995, iters=40000
3. T=8.0, cool_rate=0.993, iters=45000
4. T=12.0, cool_rate=0.992, iters=50000
5. T=2.0, cool_rate=0.997, iters=35000

## Workflow
1. Build Paley matrix with residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
2. Call structure_mutation_analyzer for mutation recommendations
3. For each cooling schedule: run SA with structure-preserving mutations
4. Probe 3-5 variants, pick best
5. Full eval on winner
6. If no improvement, emphasize swaps over flips

## Budget
- Per evaluation: <300 seconds
- numpy.linalg.det is fast (~0.001s per 29x29)
- 50k iterations with structure-preserving flips: ~50s
- 5 cooling schedules x 50s = 250s (leaves 100s margin)
