---
name: discovery-optimization
description: "n=29 Hadamard optimizer. Start with Paley construction. Test multiple cooling schedules via probe. Use structure-preserving mutations (row/col flips, swaps). 25k-50k iterations per schedule. Total <300s."
---

# Hadamard n=29 Optimizer - Structure-Preserving Search

## Starting Point
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
Paley construction: H[i][j] = 1 if (i-j) mod 29 in residues, else -1

## CRITICAL: Structure-Preserving Mutations
Random single flips destroy structure. Use these instead:

### Mutation Type A: Row Flip
Flip ALL entries in one row (multiply entire row by -1). Preserves det magnitude.

### Mutation Type B: Column Flip
Flip ALL entries in one column. Preserves det magnitude.

### Mutation Type C: Row Swap
Swap two rows. Preserves det magnitude (up to sign).

### Mutation Type D: Column Swap
Swap two columns. Preserves det magnitude (up to sign).

These mutations maintain the +/-1 structure better than random single flips.

## Cooling Schedules to Test (probe 3-5 variants)
1. T=3.0, cool_rate=0.996, iters=30000
2. T=5.0, cool_rate=0.995, iters=40000
3. T=8.0, cool_rate=0.993, iters=45000
4. T=12.0, cool_rate=0.992, iters=50000
5. T=2.0, cool_rate=0.997, iters=35000

## Workflow
1. Build Paley matrix
2. For each cooling schedule variant: run SA with structure-preserving mutations (20% rows, 20% cols, 10% swaps)
3. Probe 3-5 variants, pick best
4. Full eval on winner
5. If no improvement, try row/col swap emphasis
