---
name: direct-construction-playbook
description: Generate explicit step function candidates for the Erdős overlap problem. Focus on piecewise constant functions with few breakpoints that satisfy ∫h=1. These often beat gradient-based optimization from random starts.
---

# Direct Construction Playbook for C₅ Bound

## Why Construction Works
Gradient descent on high-dimensional latent spaces gets trapped in local optima.
Explicit piecewise constant constructions with known structure can escape these.

## Key Construction Patterns

### Pattern 1: Single Step (h=1 on [0,1])
- h(x) = 1 for x∈[0,1], h(x)=0 for x∈[1,2]
- Integral = 1 ✓
- Creates concentration at the beginning

### Pattern 2: Double Step (symmetric half-height)
- h(x) = 0.5 for x∈[0,0.5]∪[1.5,2], h(x)=0 elsewhere
- Integral = 0.5×0.5 + 0.5×0.5 = 0.5... need to scale!
- Correct: h=1 on [0,0.5] and [1.5,2]
- Creates separation with gaps in between

### Pattern 3: Three-Part Symmetric
- h=1 on [0,1/3], h=0.5 on [1/3,2/3], h=0 on [2/3,2]
- Integral = 1/3 + 1/6 + 0 = 0.5... need adjustment
- Better: optimize the heights programmatically

### Pattern 4: Edge Concentration
- High values at both ends [0,a] and [2-a,2]
- Creates "spread out" mass to reduce overlap

### Pattern 5: Uniform with Offset
- h = constant + small perturbation
- Smooth but constrained variants

## Execution Strategy
1. Generate 5-10 candidates using the new tool
2. Verify integral constraint for each
3. Evaluate the top 3-5 candidates
4. Pick best and refine with gradient descent
5. Try different parameter variations on the winner

## Critical Checks
- ∫_0^2 h(x) dx MUST equal 1 (within numerical tolerance)
- 0 ≤ h(x) ≤ 1 for all x
- Use coarse discretization (100-200 intervals) for fast prototyping
- Don't waste evaluations on invalid candidates

## Mathematical Intuition
The overlap integral max_k ∫ h(x)(1-h(x+k)) dx is minimized when h is "spread out"
but not too concentrated. The single-step h=1 on [0,1] has significant overlap with
itself shifted by small k. Splitting the mass and creating gaps reduces this overlap.
