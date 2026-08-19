---
name: discovery-optimization
description: "C5 optimization harness. Target: combined_score > 1.0 via discrete pattern search + coarse-to-fine refinement.\nUse generate_pattern_candidates to create diverse step functions. Start coarse (200 intervals), refine to 800."
---

# C₅ Bound Optimization Strategy

## The Problem
Minimize max_k ∫_0^2 h(x)(1-h(x+k))dx subject to h∈[0,1], ∫h=1.
Current best: C₅ ≤ 0.38092303510845016.

## Why Standard Optimization Fails
The seed uses Adam on 800 continuous parameters. This non-convex problem has many local optima.
Gradient methods get stuck because small perturbations from good solutions increase the objective.

## Winning Strategy: Discrete Pattern Search

### Step 1: Generate Concrete Patterns (Use generate_pattern_candidates)
Instead of random initializations, try THESE specific constructions:

1. **Single Block**: h=1 on [0,1], h=0 elsewhere

2. **Two Equal Blocks**: h=0.5 on [0,0.5] and [1.5,2]

3. **Uniform**: h=0.5 everywhere (with slight perturbations to vary)

4. **Symmetric Wave**: h = 0.5 + 0.5*sin(πx)

5. **Three-Block**: h=0.75 on [0,1/3]∪[2/3,2], h=0.25 on middle

### Step 2: Coarse-to-Fine Discretization
- Start with num_intervals=200 (coarse grid)
- Find promising patterns
- Refine to num_intervals=800 (finer grid)
- This escapes local optima by finding global structure first

### Step 3: Evaluate Patterns Directly
- Generate concrete patterns
- Compute their c5_bound directly before any optimization
- Pick best pattern, then optimize from there

### Step 4: Alternative Optimization
If Adam fails, try:
- Coordinate descent on interval parameters
- Derivative-free optimization

## Execution Plan

1. **Baseline**: Eval seed (1 eval)

2. **Pattern Generation**: Use generate_pattern_candidates with num_intervals=200

3. **Pattern Selection**: Evaluate 5-10 patterns directly

4. **Refinement**: For best patterns, increase to 800 intervals

5. **Ablation**: Try different penalty strengths, learning rates

## Important

- Each evaluation is precious (~30 total). Use them strategically.
- Concrete patterns beat random initialization.
- Coarse-to-fine is critical.
- Goal: combined_score > 1.0 (c5_bound < 0.380923).
