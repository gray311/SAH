---
name: discovery-optimization
description: "Analytical pattern generation for Erdos C5. Call smart_pattern_generator to create\nintegral-constrained candidates with precomputed scores. Only evaluate those with\nc5_bound < 0.378. Use analytical FFT scoring to avoid wasting evals on poor patterns."
---

# Erdos C5 Pattern Discovery Strategy

## The Problem
Gradient-based optimization from a single seed gets stuck. We need diverse,
high-quality initializations discovered analytically.

## Core Strategy: Analytical Screening

1. CALL smart_pattern_generator ONCE at start
2. EXAMINE all 3 candidates - each has h (latent), integral (should=1.0), c5_bound
3. FILTER: Only keep candidates with integral ~ 1.0 AND c5_bound < 0.378
4. EVALUATE: CALL evaluate_solution on each kept candidate
5. REPORT: Submit best combined_score

## Pattern Families Implemented in Tool

### Golomb Ruler Patterns
- 5 marks: [0.0, 0.4, 0.8, 1.2, 1.6] - maximizes minimum spacing
- 4 marks: [0.0, 0.5, 1.0, 1.5] - simpler, may work better

### Bipartite Patterns  
- Split at a=0.45: high on [0,0.45), low on [0.45,2)
- Tunable: a=0.4, 0.45, 0.5, 0.55, 0.6

### Tri-Modal Patterns
- Three narrow Gaussian peaks at [0.4, 1.0, 1.6]
- Alternative: [0.3, 1.0, 1.7], [0.45, 1.0, 1.55]
- Width parameter tuned for optimal overlap minimization

### Quadratic Patterns
- Parabolic mass: h(x) = a + b*x + c*x^2, normalized to integral=1
- Inverted parabola: concentrated at edges

### Multi-Peak Patterns
- 4-5 narrow peaks at strategic positions
- Goal: distribute mass to minimize pairwise overlaps

## Why This Works

- **No training overhead**: c5_bound computed via FFT in milliseconds
- **Integral guaranteed**: All candidates normalized to sum(h)*dx = 1
- **Budget efficient**: 1 tool call + 2-3 evals max, vs 35+ wasted evals
- **Diversity**: 5+ distinct pattern families, not just gradient perturbations

## Expected Outcome

Find c5_bound < 0.380923 with 5-10 total evals (vs 35+ that failed before).
