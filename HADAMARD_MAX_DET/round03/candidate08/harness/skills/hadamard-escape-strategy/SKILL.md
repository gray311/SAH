---
name: hadamard-escape-strategy
description: Specialized skill to escape local optima in n=29 Hadamard search. When SA stalls (score < 0.48 or no improvement), switch to structured mutations - row/column flips, 3x3 subblock swaps, column cycles. Always call block_mutation_scramble after SA. Use probe to compare SA vs mutated results before full evaluation.
---

# Escape Local Optima for n=29 Hadamard Matrix

## CRITICAL: We're stuck at 0.510438 - SA alone is not enough

## Detection: Switch to structured mutations when:
- Score < 0.48 after SA runs
- No improvement for 2+ consecutive SA evaluations
- SA result doesn't beat 0.51 (the plateau)

## Structured Mutation Toolkit

### 1. Row/Column Flips
- Flip entire rows: matrix[i] = -matrix[i]
- Flip entire columns: all rows have column j negated
- Flip 2-5 rows/cols simultaneously
- Use sparingly - too aggressive destroys structure

### 2. Subblock Swaps (3x3 or 5x5)
- Extract subblock from row group A
- Swap with subblock from row group B
- Preserves more structure than random flips
- Try positions: (0,0)-(r,r), (5,5)-(r+5,r+5), etc.

### 3. Column Cycles
- Shift all columns cyclically by k positions
- Try shifts: k=1,2,3,5,7,10
- Can create new linearly independent patterns

### 4. Hybrid Approach
- Start with SA result
- Apply block_mutation_scramble
- Pick best variant
- Run SA from that variant for 10k more iterations

## Execution Protocol
1. Run Paley + SA (5 seeds, 25k iters)
2. Call block_mutation_scramble on best SA result
3. Probe all variants (SA + 3 mutations)
4. Pick best, evaluate
5. If score < 0.50, repeat with MORE mutations
6. If score >= 0.50, try more iterations first

## WARNING: Don't over-mutate
- Keep trying SA first (it's faster)
- Only use mutations when clearly stuck
- Always probe before full evaluation
