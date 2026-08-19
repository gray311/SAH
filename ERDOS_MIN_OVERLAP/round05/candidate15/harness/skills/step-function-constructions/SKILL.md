---
name: step-function-constructions
description: Build step function candidates for Erdős C5 problem. Use structured patterns - uniform blocks, triangular functions, sine-based initializations. Always normalize to ∫h=1. Test multiple restarts with diverse seeds. Prefer coarser discretizations (100-400 intervals) with stronger penalties over fine-grained gradient descent.
---

# Step Function Construction Guide for Erdős C5

## Goal
Build step functions h: [0,2]→[0,1] that minimize max_k ∫ h(x)(1-h(x+k))dx.
Target: c5_bound < 0.38092303510845016 (score > 0.999641).

## Construction Patterns

### 1. Uniform Block Functions
Create h(x) as piecewise constant:
- 2-block: h(x)=0.5 for x in [0,2], 0 otherwise → ∫h=1 ✓
- 3-block: h(x)=a in [0,a], 1-a in [a,2-a], a in [2-a,2] where a=1/3
  This concentrates mass in the center
- Alternating: h(x) alternates between high/low values across intervals

### 2. Sine-Based Initialization
h(x) = sigmoid(k*sin(π*x) + c) for various k, c
- Controls asymmetry via phase shift c
- Controls steepness via k
- Try k in [1,5], c in [-1,1]

### 3. Concentrated Mass Patterns
Put most of h's mass in one region:
- h(x) ≈ 1 for x in [0.2, 0.8], ≈ 0 elsewhere
- h(x) ≈ 1 for x in [0.1, 0.1+L] where L chosen to get ∫h=1

### 4. Multi-Restart Strategy
Run 5-10 optimizations with different seeds:
- Pattern A: Random normal initialization
- Pattern B: Uniform in [-2,2]
- Pattern C: Sin/cos mix
- Pattern D: Block function
- Pattern E: Triangular function

## Optimization Tips

- Start with coarse discretization (100-300 intervals) for faster exploration
- Use penalty_strength=500-2000 to enforce ∫h=1
- Use learning_rate=0.005-0.012
- Monitor c5_bound during optimization (not just final loss)
- If stuck, change initialization pattern or interval count

## Validation

Always check: ∫h(x)dx = 1 (within tolerance), h(x) in [0,1], no NaNs.
Use probe_solution to quickly check feasibility before full evaluation.

## Key Insight

The optimal function likely has a simple structure (few steps, symmetric or nearly symmetric). Avoid overly complex patterns. Coarse-to-fine strategy: test 100 intervals first, then 300, then 500 if needed.
