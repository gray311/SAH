---
name: construction-strategy
description: Combinatorial construction strategy for Erdős C₅ problem. Focus on piecewise constant functions, not gradient descent. Use construct_candidate for diverse candidates, evaluate, pick best.
---

# Combinatorial Construction for C₅ Optimization

## Core Insight

This problem rewards clever piecewise constant constructions, not smooth gradient descent. The seed's Adam optimizer gets stuck because the landscape is rugged.

## Construction Types

### 1. Uniform Split (Type A)
Divide [0,2] into n equal intervals. Set h(x) = 2/n for the first n/2 intervals, 0 elsewhere.
- Ensures ∫h = 1

### 2. Concentrated Mass (Type B)
Place mass near endpoints: h(x) = c on [0,a] ∪ [2-a,2], 0 elsewhere.
- Choose c = 1/(2a) to satisfy ∫h = 1

### 3. Symmetric Patterns (Type C)
Create patterns centered at x=1, mirrored around the center.

### 4. Multi-Step Functions (Type D)
k-piece step functions with strategic breakpoints.
- k=2: simple split
- k=3-4: alternating high/low regions

## Execution Strategy

1. **Diversity First**: Call construct_candidate 3-5 times with different (n, style) pairs

2. **Evaluate Strategically**: Each evaluation is precious. Evaluate top 3-4 candidates.

3. **Refine Wisely**: If a candidate shows promise (score > 0.999641 but < 1.0):
   - Increase n_intervals to 400-800
   - Run fewer steps but with the good starting point

4. **Stop Conditions**:
   - combined_score > 1.0: RECORD BROKEN, submit immediately
   - 20+ evals with no improvement: try coarser n_intervals (50-100)

## Critical Reminders

- ∫h must equal EXACTLY 1
- h must be in [0,1] - clip before normalizing
- Coarse discretization (n=50-200) often finds better global optima
- Don't over-optimize: A good construction beats a long gradient run
