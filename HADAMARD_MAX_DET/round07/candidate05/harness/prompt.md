You are optimizing a 29x29 ±1 matrix to maximize |det(H)|.

### CRITICAL INSIGHT
The seed program's SA approach (10M flips over 500 seeds) is inefficient. SA makes tiny
improvements but gets stuck. Instead, use a **multi-construction pipeline**:

1. **Construct**: Build 3-5 different starting matrices using:
   - Paley construction (seed is correct)
   - Random ±1 matrix
   - Block-pattern construction (4x4 repeating blocks)
   - Permutation-based construction

2. **Refine each with STRUCTURED operations** (not random flips):
   - Swap entire rows/columns (preserves determinant magnitude)
   - Flip 2x2 blocks: flip H[i,j], H[i+1,j], H[i,j+1], H[i+1,j+1] together
   - "Cyclic shift" rows to break local patterns

3. **Evaluate** each refined matrix directly (no SA loop needed)

4. **Return** the matrix with highest |det|

### Time budget
- 20 evals available, 350s per eval
- With 3 constructions × ~50 refinement steps × det(~0.001s), total ~15-30s per eval
- Well under budget

### DO NOT use SA
- SA with 10k+ iterations wastes budget
- Random flips don't respect Hadamard structure
- Better to try different CONSTRUCTIONS and pick best

### Tool usage
- edit_solution: Provide FULL working code with multi-construction pipeline
- probe_solution: Test 2-3 construction types quickly (10 iterations each)
- evaluate_solution: Run full pipeline and return best matrix
