---
name: discovery-optimization
description: "Multi-phase Hadamard optimizer for n=29. Use 4 construction methods (Paley, random, perturbed Paley, Hadamard(28)+1). For each: 3-stage coarse-to-fine search (5k/10k/20k iters with temp 10\u21923\u21921). Run with 4 seed families. Add targeted escape patterns. Always probe 3-5 variants before evaluate. Total must be <300s."
---

# Multi-Phase Hadamard Optimization for n=29

## Task
Maximize |det(H)| for 29×29 ±1 matrix. n=29 ≡ 3 mod 4.

## 4 CONSTRUCTION METHODS (try ALL)

### Method A: Paley Construction
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For H[i][j]: diff=(i-j) mod 29, H[i][j]=1 if diff∈residues else -1

### Method B: Random ±1 Matrix
Random initialization with fixed seed, entries ±1 uniformly.

### Method C: Perturbed Paley
Start with Paley, then flip checkerboard pattern: flip where (i+j) mod 4 == 0

### Method D: Hadamard(28)+1 Block
Use known optimal Hadamard for n=28, extend to 29 with careful last row/column

## 3-STAGE COARSE-TO-FINE SEARCH (per method, per seed)

### Stage 1: Broad Exploration
- Iterations: 5,000
- Initial temp: 10.0
- Cool rate: 0.999
- Goal: Escape obvious local minima

### Stage 2: Medium Refinement
- Iterations: 10,000
- Initial temp: 3.0
- Cool rate: 0.997
- Goal: Fine-tune from Stage 1 best

### Stage 3: Fine Tuning
- Iterations: 20,000
- Initial temp: 1.0
- Cool rate: 0.995
- Goal: Local optimization to convergence

**Keep the BEST result from all 3 stages.**

## 4 SEED FAMILIES (for diversity)

### Family 1: Small seeds
[42, 123, 456, 789]

### Family 2: Year-based seeds
[2024, 2025, 2026, 2027]

### Family 3: Distinct pattern seeds
[9999, 8888, 7777, 6666]

### Family 4: Large seeds
[1000000, 2000000, 3000000, 4000000]

## 3 TARGETED ESCAPE PATTERNS

From each Phase 3 best, run 3 targeted mutations:

### Escape Pattern A: Checkerboard Flip
Flip all positions where (i+j) mod 4 == 0, then run 10,000 iterations with temp=5.0

### Escape Pattern B: Corner Submatrix
Select a 7×7 corner (top-left), flip all entries, run 10,000 iterations with temp=5.0

### Escape Pattern C: Aggressive Random
Flip 50% of positions randomly, run 10,000 iterations with temp=8.0

## IMPLEMENTATION CHECKLIST

1. ✓ Implement ALL 4 construction methods
2. ✓ Implement 3-stage search per method
3. ✓ Use 4 seed families
4. ✓ Implement 3 escape patterns
5. ✓ Use numpy.linalg.det for ALL iterations (NEVER Bareiss during search)
6. ✓ Total iterations: ~4 methods × 4 seeds × (5k+10k+20k) + escapes = ~480,000 flips
   Expected time with numpy: ~480k × 0.001s ≈ 480s → TOO LONG!
   **OPTIMIZATION**: Reduce to 2 seed families, or 3 methods, or reduce stage 1 to 2k iters
   **RECOMMENDED**: 3 methods × 2 seed families × 3 stages = 18 searches × 35k iters = 630k iters
   Actually: Use subsampling in probe, and be selective. Run FULL only on top 8 variants.

## BUDGET MANAGEMENT (CRITICAL)

- Time budget: 350 seconds per evaluation
- numpy det on 29×29: ~0.001s per call
- 50,000 iterations: ~50 seconds
- You can comfortably run: 7 full searches × 50k iters = 350 seconds
- OR: 14 searches × 25k iters = 350 seconds

**RECOMMENDED CONFIG**: 4 construction methods × 1-2 seed families each, 3-stage search (reduced stages to 2k/10k/20k), then escape on top 2.

## WORKFLOW
1. Implement multi-method search with 2-3 seed families, 2-stage (or 3-stage with reduced Stage 1)
2. Call edit_solution with full working code
3. Call probe_solution on variants with different: (a) number of seed families, (b) which methods, (c) cooling schedules
4. Call evaluate_solution on the SINGLE best probe variant
5. If score improves, expand search space. If not, try different construction methods.

## COMMON MISTAKES
- ❌ Using only Paley construction
- ❌ Single cooling schedule instead of coarse-to-fine
- ❌ Fewer than 3 seed families
- ❌ No escape patterns
- ❌ Using Bareiss during search (causes timeout!)
- ❌ Running more than ~7 full searches per evaluation
- ❌ Not using probe_solution to pre-rank variants
