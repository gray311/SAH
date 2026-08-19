---
name: c2-family-exploration
description: Playbook for discovering new function families that beat the current C₂ record.  Use this when - progress stalls, seed is already optimized, or you need to explore beyond step functions.  Key principle - Systematic family exploration beats random parameter tuning.
---

# C₂ Function Family Discovery Playbook

## Why This Matters
The seed achieves 0.8962799441554086 using step functions. To beat this, we must find NEW function classes.

## Step 1: Analyze Current Patterns
Use analyze_seed_patterns to understand:
- What heights work best
- Symmetric vs asymmetric patterns
- Current interval usage

## Step 2: Probe-Based Family Benchmarking
For each candidate family, implement 3-5 variants and probe ALL of them.

Example families:
- Splines: 5, 7, 9 knots at different positions
- Polynomials: degree 2, 3, 4 pieces
- Gaussian mixes: 2, 3, 4 components
- Asymmetric steps: left=1.2, right=1.8; left=0.8, right=2.0

## Step 3: Commit to Full Evaluation
After probing:
- Pick top 2 families
- Implement 2-3 refined variants each
- Full evaluate these candidates
- Re-rank by actual scores

## Step 4: Iterate Within Best Family
Once you find a promising family:
- Refine parameters systematically
- Try boundary conditions
- Explore asymmetric variants
- Only abandon after 2-3 failed attempts

## When to Switch Families
- After 10 iterations with no improvement
- If best probe score < 1.02 for current family
- If 2 full evals fail to improve

## Success Metrics
- Combined score > 1.04
- New C₂ record > 0.935
- Publishable function class

## Key Insight
Random mutation within a family has diminishing returns. **Family exploration** is the breakthrough strategy.
