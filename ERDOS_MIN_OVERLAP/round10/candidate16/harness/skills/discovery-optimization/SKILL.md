---
name: discovery-optimization
description: "Construct piecewise-constant step functions with exact integral constraint for Erdos problem."
---

# Step Function Construction for Erdos Minimum Overlap

## Core Insight
The seed optimizer uses sigmoid(latent) which produces smooth functions.
For the Erdos problem, EXACT step functions (values in {0, 0.5, 1}) can achieve lower bounds.

## Constraint
- Grid: N intervals, dx = 2/N
- Must have: sum(h) * dx = 1 → sum(h) = N/2
- For N=800: exactly 200 ones, 400 halves, 200 zeros

## Construction Patterns

### Pattern 1: Edge Blocks (Bimodal)
h = [1.0]*200 + [0.5]*400 + [1.0]*200

### Pattern 2: Golomb-Inspired  
Use optimal Golomb ruler positions [0, 0.25, 0.625, 0.9375, 1.0] scaled to indices
Place 1s at these positions, fill rest with 0.5s.

### Pattern 3: Alternating
h[i] = 1 if i % 4 < 2 else 0.5

### Pattern 4: Concentrated
h = [1.0]*150 + [0.5]*400 + [1.0]*50

## Editing
Replace _get_best_initialization() to return step patterns directly.
Verify: np.sum(h) * dx ≈ 1.0 before evaluation.
