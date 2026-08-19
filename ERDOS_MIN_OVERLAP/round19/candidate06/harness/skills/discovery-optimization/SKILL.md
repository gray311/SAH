---
name: discovery-optimization
description: "Generate analytical, pattern-based initializations for Erdos optimization.\nThese patterns are NOT gradients of current solutions; they are standalone constructions\nfrom combinatorial design theory that may achieve lower C5 bounds."
---

# Analytical Pattern Generation for Erdos C5 Optimization

## Core Insight
The seed optimizer's gradient descent method produces candidates very close to the seed
(c5_bound ~0.3809). It STALLS because it cannot escape the local minimum.

We need COMPLETELY DIFFERENT initializations that are NOT gradients.

## Pattern Library (12 types, standalone)

1. **Golomb ruler (5 marks)**: h(x) = sum of 5 narrow peaks at [0, 0.4, 0.8, 1.2, 1.6]
   This spacing minimizes pairwise overlaps.

2. **Golomb ruler (7 marks)**: h(x) = sum of 7 narrow peaks at [0, 1/7*0.5, 2/7*0.5, ...]

3. **Bipartite**: h(x) = high on [0, 1], low on [1, 2] (or vice versa)
   Creates separated support, reducing max overlap.

4. **Tri-modal (3 peaks)**: h(x) = 3 narrow Gaussians at [0.4, 1.0, 1.6]

5. **Bi-modal (2 peaks)**: h(x) = 2 narrow Gaussians at [0.6, 1.4]

6. **Sparse peaks (3 peaks)**: h(x) = 3 narrow peaks at [0.25, 0.75, 1.25, 1.75]

7. **Uniform flat**: h(x) = 0.5 everywhere (integral = 1 exactly)

8. **Step function**: h(x) = 1 on [0, 1), 0 on [1, 2]

9. **Sinusoidal + offset**: h(x) = 0.5 + 0.3*sin(2*pi*x)

10. **Piecewise constant**: h(x) = [1.0, 0.0, 0.0, 0.0, 0.0, 0.5] in 5-bins

11. **Threshold shifted**: h(x) = 1 on [0.3, 0.7], 0 elsewhere (needs scaling)

12. **Multi-scale**: combine a broad Gaussian with narrow spikes

## Workflow

1. CALL generate_structured_patterns(type=golomb_5) for first batch

2. For each candidate:
   - Check: integral must be ~1.0 (within 5%)
   - Check: c5_bound must be < 0.375 to be promising
   - Call evaluate_solution on all passing candidates

3. If NO candidate passes (c5_bound < 0.375):
   - Try DIFFERENT pattern types (not new seeds)
   - Try golomb_7, bi-modal, sparse, uniform, etc.

4. After EACH full evaluation:
   - If any candidate beats seed, KEEP IT as the new baseline
   - Generate a NEW pattern (not gradient of current)

5. NEVER call edit_solution with gradient descent. We are doing pattern search.

## Why This Works

- Standalone patterns: not gradients, so they explore different regions
- Analytical constructions: from combinatorial design theory, may have lower overlap
- Pattern diversity: 12 different structures to explore
- Direct evaluation: each pattern is a complete candidate, no refinement needed

## Expected Results

With 12 diverse patterns per batch and 2-3 evals, we can explore 30+ unique candidates.
Even if only 5% have c5_bound < 0.375, that's 1-2 promising candidates per batch.
