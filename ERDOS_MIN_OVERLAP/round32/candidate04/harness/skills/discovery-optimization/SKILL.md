---
name: discovery-optimization
description: "Use SIMPLE initializations: bipartite (single threshold), trimodal (3 peaks), or symmetric functions. \nCall probe_solution to screen candidates before full evaluation. Focus on structurally different h(x)."
---

# Erdos C5 - Simplified Strategy

## Phase 1: Generate Diverse Simple Functions

1. Generate BIPARTITE functions: h(x) = sigmoid(p*(x-a)) for different a values
   - This creates a single step function
   - Try a=0.5, 0.75, 1.0, 1.25, 1.5
   - Adjust to ensure integral(h) ≈ 1

2. Generate TRIMODAL functions: 3 Gaussian-like peaks
   - Place peaks at different configurations
   - E.g., peaks at (0.3, 1.0, 1.7), (0.4, 0.8, 1.6), etc.
   - Scale heights to satisfy integral constraint

3. Generate SYMMETRIC functions: h(x) = h(2-x)
   - Mirror symmetry might reduce overlap at certain k values
   - Try triangular, trapezoidal, or multi-peak symmetric shapes

## Phase 2: Screening

1. Call PROBE_SOLUTION on each candidate
2. Keep only those with c5_bound < 0.382
3. Evaluate the top 2-3 candidates

## Phase 3: Refinement

If simple functions don't work:
- Try LOCALIZED modifications: modify h in specific regions
- Try STEPPED functions: piecewise constant with 3-5 steps
- Adjust penalty_strength to 80-120 to enforce integral constraint

## Key Rules
- Focus on STRUCTURALLY DIFFERENT functions from the seed
- Use PROBE before full evaluation
- Enforce integral(h) = 1 with strong penalty
- Never copy the seed's multi-pattern approach
