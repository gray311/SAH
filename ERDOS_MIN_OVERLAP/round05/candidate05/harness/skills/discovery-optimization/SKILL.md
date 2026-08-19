---
name: discovery-optimization
description: "Optimize step functions for the Erdos minimum overlap problem. Use coarse-to-fine discretization, pattern-based constructions, and structural simplification to find functions with lower C5 bounds. Budget: 30 evaluations."
---

# Erdos C5 Optimization Strategy

## Problem
Find step function h: [0,2] -> [0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral h(x)dx = 1 exactly.

## Key Insights for This Task
1. The seed's gradient-based approach with 8000 intervals may be over-parameterized and stuck in local optima
2. Step functions have intrinsic discreteness - exploit this with:
   - Fewer intervals optimized carefully
   - Quantized value ranges
   - Boundary optimization instead of point-wise optimization
3. Good starting points: explicit pattern functions, then refine

## Strategy Options

### A. Coarse-to-Fine Discretization
- Start with 16-32 intervals, optimize, then progressively refine to 128, 256, 512
- Train on coarse, evaluate on fine for transfer

### B. Structured Patterns
- Try explicit piecewise-constant functions with specific boundary choices
- E.g., h(x) = a for x < c1, b for c1 <= x < c2, etc.
- Optimize: (a, b, c1, c2, ...) rather than all interval values

### C. Quantization Approach
- Assume h takes values from discrete set {v1, v2, ..., vk}
- Optimize only the boundaries and value assignments
- This is combinatorial but search space is manageable

### D. Multi-Stage Refinement
- Stage 1: Find good boundary locations (use gradient-free if needed)
- Stage 2: Given boundaries, optimize interval values
- Stage 3: Fine-tune both

## Editing Guidelines
- Complete rewrites are welcome and encouraged when changing paradigms
- If rewriting the optimizer: keep the class structure but change _get_best_initialization and/or _optimize_single_run substantially
- Consider replacing _objective_fn with a constraint-handling approach that's less punitive

## Evaluation Discipline
- Each of 30 evaluations counts heavily
- If seed score is 0.999641 (barely beating the 1.0 baseline), you need significant improvement
- combined_score > 1 means new record; aim for > 1.05 (at least 5% improvement)

## Common Pitfalls
- Don't just tweak hyperparameters; the seed's approach may be fundamentally misaligned
- Don't use 8000 intervals from the start - it's too coarse for gradient methods
- The constraint integral h = 1 is critical - ensure your approach respects or penalizes it strongly
