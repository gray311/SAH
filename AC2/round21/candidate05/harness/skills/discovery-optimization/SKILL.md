---
name: discovery-optimization
description: "Diverse architecture search for C2 maximization. Generate structurally different step functions\n(varying intervals, multi-peak configs, asymmetries), probe to screen, then gradient-tune winners.\nStructural innovation beats parameter refinement."
---

# C2 Maximizer: Diverse Architecture Search Protocol

## Core Principle
The seed step patterns are trapped in local optima. You must GENERATE new architectures,
not just refine existing ones. Vary interval counts, peak configurations, and asymmetries.

## Phase 1: Architectural Diversity (iterations 1-10)

Step 1: Generate Diverse Variants
- Call generate_step_variants to create 4-6 structurally different functions
- Vary: number of intervals (200/400/800/1200), peak count (1/2/3), asymmetry (left/right/center)
- Try combining patterns: e.g., pattern 9 (asymmetric multi-level) + pattern 10 (wide base)

Step 2: Aggressive Probing
- Call probe_solution on ALL 4-6 variants (this is your opportunity to screen diversity)
- You have 30 probes - use them to evaluate many architectural choices
- Rank by probe score

Step 3: Select and Evaluate
- Evaluate top 2 variants by probe score
- If both underperform record: generate different architectural styles

## Phase 2: Gradient-Fine Tuning (iterations 11-20)

Step 1: Take Best Architecture
- Use the highest-scoring variant from Phase 1
- Compute gradients: @jax.grad(-c2_ratio)

Step 2: Gradient Ascent
- Variant A: Follow positive gradient (param = param + 0.05 * gradient)
- Variant B: Try orthogonal perturbation (random 10% of params, add Gaussian noise)

Step 3: Probe and Evaluate
- Probe both, evaluate best
- Continue refinement or switch to Phase 3 if stuck

## Phase 3: Hybrid Constructions (iterations 21-30)

Step 1: Try Advanced Combinations
- Step + envelope: Multiply step function by Gaussian: f(x) * exp(-x^2/100)
- Multi-scale: Fine-grained step on coarse support
- Spline approximation: Fit B-spline to optimal step pattern

Step 2: Generate and Screen
- Create 3 hybrid variants
- Probe all, evaluate best
- Submit if beats record

## Key Rules
- generate_step_variants creates STRUCTURAL diversity, not small mutations
- probe_solution: screen MANY variants (10-15) before any full eval
- Never settle for parameter refinement alone - architectures matter
- If stuck at iteration 10+: try completely different interval counts and peak configurations
- Use all 30 probe budget to maximize exploration
