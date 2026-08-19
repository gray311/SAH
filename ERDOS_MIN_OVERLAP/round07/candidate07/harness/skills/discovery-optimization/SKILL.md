---
name: discovery-optimization
description: "C\u2085 bound via explicit step-function construction. Abandon gradient descent; build discrete candidates directly."
---

# Erdős C₅ Bound: Explicit Construction Strategy

## Why Gradient Descent Fails

This is a DISCRETE OPTIMIZATION problem. The optimal h is likely a simple step function (2-5 intervals), not a complex learned function. Adam optimizer gets stuck in poor local optima on the wrong landscape.

## Mathematical Background

The C₅ bound equals max_k ∫₀² h(x)(1-h(x+k))dx. We want this minimal.

Key insight: Simple step functions with proper alignment can achieve very low overlap.

## Construction Recipes

### Pattern A: Single Mass on [0,1]
- h(x) = 1 for x∈[0,1], h(x) = 0 for x∈(1,2]
- ∫h = 1 ✓
- This gives some baseline C₅

### Pattern B: Two-Step Symmetric
- h(x) = 0.5 for x∈[0,0.5] ∪ [1,1.5], h(x) = 0 elsewhere
- Total measure = 0.5×1 = 1 ✓
- May reduce overlap compared to single mass

### Pattern C: Concentrated at Boundaries
- h(x) = 1 on [0,a] ∪ [2-a, 2], h(x) = 0 elsewhere
- Choose a so total measure = 1: a + a = 1, so a = 0.5
- h(x) = 1 on [0,0.5] ∪ [1.5, 2]

### Pattern D: Three-Interval Balanced
- h(x) = 1/3 on [0,1], h(x) = 0 on [1,2]
- Or variations with different widths

### Pattern E: Shifted Block
- h(x) = 1 on [ε, 1+ε], h(x) = 0 elsewhere (adjust ε for integral=1)
- Small shift from [0,1] might reduce self-overlap

## Execution Strategy

1. **Start with 20-50 intervals** for discretization (not 800)
2. **Use pattern_construction tool** to generate explicit h arrays
3. **Call pattern_construction multiple times** with different parameters
4. **Use probe_solution** to quickly score 10-20 patterns
5. **Pick top 2-3 patterns, call evaluate_solution** on each
6. **If best score still ~1.0, try radically different structures**

## Tool Usage

- **pattern_construction(args)**: Returns explicit h array for a given pattern config
- **probe_solution()**: Quick approximate score (don't use if patterns are already explicit)
- **evaluate_solution()**: Full official score - use sparingly

## Success Criteria

Achieve combined_score > 1.0. Any improvement over 0.999641 is good, but we need c5_bound < 0.38092303510845016.

## Common Mistakes to Avoid

- Don't use gradient-based optimization
- Don't use 800 intervals (overly complex, not what we need)
- Don't rely on random initializations with noise
- DO verify constraints analytically before submitting
DO verify ∫h=1 explicitly
DO ensure all h values are exactly in [0,1] (not [0,1) or (0,1])
