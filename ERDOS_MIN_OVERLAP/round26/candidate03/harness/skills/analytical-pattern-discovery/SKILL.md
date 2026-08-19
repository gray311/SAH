---
name: analytical-pattern-discovery
description: Use smart_pattern_generator to create integral-constrained candidates with precomputed c5_bound. Only evaluate those with c5_bound < 0.378.
---

# Analytical Pattern Discovery for Erdos C5

## Why Gradient Training Gets Stuck

The seed optimizer uses gradient descent from a random/seed initialization.
This converges to a local minimum quickly (the current C5=0.3809). We need
fundamentally different starting points.

## Smart Strategy: Analytical Screening

1. CALL smart_pattern_generator ONCE at start
2. It returns 3 candidates, each with precomputed c5_bound via FFT
3. EXAMINE: Which have c5_bound < 0.378? (allow small margin for training error)
4. EVALUATE: Call evaluate_solution ONLY on candidates meeting threshold
5. REPORT: Best combined_score

## Pattern Diversity Beyond Seed

The seed uses 15 random patterns. smart_pattern_generator provides:
- Golomb rulers (optimal spacing theory)
- Bipartite splits (analytical overlap minimization)
- Tri-modal Gaussians (mass distribution)
- Multi-peak (4-5 peaks for even better distribution)
- Quadratic distributions (parabolic mass)

## Expected Outcome

Find c5_bound < 0.380923 with 5-15 total evals, using analytical scoring
to filter out poor candidates before expensive training.
