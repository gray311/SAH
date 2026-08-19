---
name: discovery-optimization
description: "Search Erdos C5 with diverse structural mutations including peak_spacing asymmetric_bipartite multi_scale gap_strategy and frequency_shifted. Use probe to screen then evaluate for final scoring."
---

# Erdos C5 - Diverse Structural Search

## Strategy
Avoid the seed's patterns which may be locally optimal. Try structurally different functions.

## Mutation Types to Try

### 1. Peak Spacing (non-harmonic)
PEAK POSITIONS that avoid simple fractions:
- [0.3, 0.7, 1.3, 1.7] (offset from 0.5, 1.0)
- [0.25, 0.75, 1.25, 1.75]
- [0.27, 0.54, 0.81, 1.08, 1.35, 1.62, 1.89] (1/4 spacing)

Why: Current seed may be optimized for k=0.5, k=1.0 overlaps. Break this symmetry.

### 2. Asymmetric Bipartite
Single threshold at NON-SYMMETRIC points:
- threshold at x = 0.3: h=1 on [0, 0.3], h=0 on (0.3, 2]
  Scale to integral=1: h=1 on [0, 0.5] (since integral over [0,2] = 2*a = 1 => a=0.5)
  Try a = 0.4, 0.45, 0.35, 0.55

### 3. Multi-Scale (coarse + fine)
Base structure + small perturbations:
- h_base = sigmoid(pairs_step_function)
- h = h_base + 0.1*sin(8*pi*x)  (high frequency ripple)
- Ensure h stays in [0,1] by clipping

### 4. Gap Strategy (zeros allowed)
Create hard zeros:
- h(x) = 1 on [0, 0.333] U [1.333, 2.0], 0 elsewhere
  This gives peaks with gaps where overlap is zero

### 5. Frequency Shifted
Use higher or different frequency:
- h(x) = sigmoid(2*pi*x - pi)  (period 1, shifted)
- h(x) = sigmoid(4*pi*x - 2*pi) (period 0.5, shifted)

## Implementation Steps
1. Decide mutation type
2. Write EVOLVE-BLOCK code implementing h(x)
3. Ensure integral(h) = 1 (adjust accordingly)
4. Ensure h in [0,1]
5. If probe_solution available, call it first
6. Call evaluate_solution on promising candidates
7. If combined_score > 1.0, finish()

## Key Insight
The seed program's 15 patterns are all variations on similar themes.
Try fundamentally different structures that the seed hasn't explored.
