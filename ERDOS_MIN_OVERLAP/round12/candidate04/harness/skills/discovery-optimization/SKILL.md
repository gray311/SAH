---
name: discovery-optimization
description: "Direct step function construction for Erd\u0151s overlap minimization with structural innovation."
---

# Erdős Minimum Overlap - Structural Innovation Strategy

## Problem
Minimize max_k ∫ h(x)(1-h(x+k)) dx for h: [0,2]→[0,1], ∫h=1.

## Key Insight
The optimal solution likely involves SHARP step functions with specific transition points,
not smooth sigmoidal functions. The seed's 12 patterns all use sigmoid(latent) which creates
overly smooth transitions.

## Phase 1: Direct Step Function Construction
1. Use construct_piecewise to directly build step functions with:
   - Varying numbers of steps (2, 3, 4, 5, 6)
   - Different step locations (based on mathematical intuition: 0.25, 0.5, 0.75, etc.)
   - Different step heights (not all from sigmoid of uniform latent)

2. Test each construction DIRECTLY with evaluate_solution (probe for constraint only).

## Phase 2: Sharp Sigmoid Variants
If direct construction fails, modify the EVOLVE-BLOCK to:
- Replace sigmoid(latent) with sigmoid(latent * SCALE) where SCALE ∈ {5, 10, 20}
- This creates SHARPER transitions while keeping the same optimizer structure

## Phase 3: Transition Point Optimization
For the best structures:
- Edit step locations: try [0.2, 0.5, 0.8], [0.25, 0.75], [1/3, 2/3], etc.
- Optimize peak widths: [0.1, 0.9], [0.15, 0.15, 0.7], etc.

## Phase 4: Multi-restart with NEW Patterns
Add to _get_best_initialization():
- Step-function pattern: direct specification of steps at mathematical points
- Large-scale sigmoid: latent with coefficient 10-20 to force sharp transitions
- Asymmetric patterns: peaks not centered at 0.5

## Budget Management
- Use all 30 evals efficiently: test 3-5 diverse structures first
- Deep dive into promising structure (5-10 iterations refining transitions)
- Finish with best structure even if score≈1.0
