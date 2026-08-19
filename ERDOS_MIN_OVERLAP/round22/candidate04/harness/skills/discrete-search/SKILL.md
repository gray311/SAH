---
name: discrete-search
description: Search using discrete step functions with analytical screening. Generate candidates, precompute scores, evaluate best.
---

# Discrete Step Function Search

## Core Idea
DIRECTLY construct step functions satisfying integral constraint by design,
bypassing gradient descent training loop.

## Method
1. Choose N in [30, 100] intervals
2. Choose pattern: bipartite (split), tri-modal (3 regions), golomb (optimal), wave
3. Assign heights, NORMALIZE so integral=1.0
4. Precompute c5_bound analytically (FFT)
5. Filter: |integral-1.0|<0.02 AND c5_bound<0.37
6. Evaluate top 3-5 with evaluate_solution

## Advantages
- No training loop - direct construction
- Integral satisfied by normalization
- Many candidates screened cheaply
- Explores architectures gradient descent misses

## Expected
With 50+ candidates, find 3-5 with c5_bound<0.36, evaluate them. Some should beat seed.
