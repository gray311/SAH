---
name: discovery-optimization
description: "Search for discrete step functions that directly satisfy constraints.\n\nGenerate candidates as piecewise constant functions with integer/simple fractional heights.\nEach candidate has precomputed integral and c5_bound (analytical, no training).\n\nStrategy: Create 50-100 discrete candidates with varying intervals (30-80),\npatterns (bipartite, tri-modal, Golomb, wave). Filter by integral=1.0 (within 1%), c5_bound < 0.37.\nExpected: Discrete constructions find valid solutions faster than gradient descent."
---

# Discrete Step Function Search

## Strategy
The Erdos minimum overlap problem benefits from DIRECT step function construction
rather than gradient-based optimization. Construct h as piecewise constant with few intervals,
assign heights directly, and verify constraints.

## Candidate Generation
1. Choose N in [30, 80] intervals
2. Choose pattern: bipartite (split domain), tri-modal (3 regions), Golomb (optimal spacing), wave
3. Assign heights, then NORMALIZE so integral(h) = 1.0
4. Precompute c5_bound using analytical formula (FFT)
5. Filter: keep if c5_bound < 0.37

## Workflow
1. Generate 100 candidates with varying N, patterns, seeds
2. Precompute integral and c5 for each
3. Filter to |integral-1.0|<0.01 AND c5_bound < 0.37
4. Evaluate top 5 with evaluate_solution
5. If no improvement, try N in [100, 200]

## Example
Bipartite N=50: set 25 intervals to height=2, 25 to height=0
integral = 25*2*dx + 25*0*dx = 50*dx = 1.0 ✓ (with dx=0.04)
This DIRECTLY constructs valid step functions without training.
