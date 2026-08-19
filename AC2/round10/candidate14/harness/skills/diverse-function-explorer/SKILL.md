---
name: diverse-function-explorer
description: A playbook for exploring function space beyond the current step function optimum. When to use - when step functions plateau or you need fresh ideas.
---

# Diverse Function Space Exploration Playbook

## Why Step Functions May Be a Local Optimum

The current best (1.03492) uses multi-level step functions. This is a local optimum
in a restricted search space. To find better solutions, we need to:
1. Explore different mathematical families
2. Change the structural complexity
3. Mix successful elements from different approaches

## Exploration Strategy

### Step 1: Baseline Confirmation
- Verify step function parameters are truly optimized
- Try: finer intervals (500-600), slightly different heights (1.35-1.65)
- If no improvement after 3 evals, move to Step 2

### Step 2: Smooth Variants
- Add smooth transitions at step boundaries (linear ramps of width 0.02-0.05)
- Try: smoothed step, Gaussian-windowed step, cosine-transitioned step
- Compare: does smoothing hurt or help the L² norm?

### Step 3: Alternative Families
Test these in order of computational efficiency:

**Gaussian Mixtures**:
- 2-5 Gaussians with random means on [0,1]
- Vary: num_components (2-5), sigma diversity (0.1-0.4), weight distributions
- Key: enforce non-negativity naturally (Gaussians are always positive)

**Cubic Splines**:
- 20-50 B-spline basis functions
- Optimize: knot positions (use quantiles), coefficients (non-negative constraints)
- Key: splines can capture curvature that steps cannot

**Hybrid Approaches**:
- Step core with smooth tails (e.g., step function multiplied by Gaussian envelope)
- Multiple peaks with smooth connections
- Plateau regions with asymmetric sides

### Step 4: Systematic Combination
- Take best element from each successful class
- Combine: e.g., Gaussian-mixture-inspired step heights, spline-like transitions
- Iterate: refine the hybrid, don't restart from scratch

## Evaluation Discipline

- Each class: test 3-5 variants, pick best, evaluate ONCE
- If a class beats steps: expand search in that direction (5+ evals)
- If a class underperforms: abandon quickly (don't waste 5+ evals)
- Track: which class achieved what score, what parameters mattered

## Breaking Through Checklist

[ ] Tested 3+ diverse function classes
[ ] Each class tested with 3-5 variants
[ ] At least one class outperformed step baseline
[ ] If none succeeded: reset to random exploration or try completely new approach
