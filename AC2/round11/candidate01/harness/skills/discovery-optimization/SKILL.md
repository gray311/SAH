---
name: discovery-optimization
description: "Mathematically-grounded C\u2082 optimization using convolution analysis. Use analyze_convolution to diagnose current patterns and propose_sampling tools to implement targeted mutations (asymmetric peaks, smooth transitions, irregular spacing). Probe multiple variants cheaply before full evaluation."
---

# C₂ Maximizer: Convolution-Aware Pattern Discovery

## Core Principle

The seed program's 13 step patterns are locally optimized. Small mutations won't help.
You need CONVOLUTION-AWARE exploration: understand WHY a pattern scores well, then target
its weaknesses systematically.

## Phase 1: Diagnostic Analysis (first iteration)

1. Call analyze_convolution on the current best pattern to understand:
   - Where the L∞ norm peak occurs
   - How the L2 norm is distributed
   - The "inequality gap" (how far from optimal ratio)

2. Use this insight to generate targeted new patterns

## Phase 2: Targeted Pattern Generation

**Target Weakness #1: High L∞ Peak**
- Add asymmetric side peaks to "dilute" the central peak
- Use smooth transitions instead of hard steps
- Try truncated power functions (f(x) ∝ x^(-α) near boundaries)

**Target Weakness #2: Low L2 Norm**
- Widen the support of the function
- Add secondary peaks at strategic distances
- Try exponential tails for better tail energy

**Target Weakness #3: Symmetric Limitations**
- Try asymmetric multi-peaked patterns: [0.4h, 1.6h, 0.5h, 1.4h, 0.3h]
- Try irregular spacing: vary interval widths by 15-30%

**Explore Non-Step Functions:**
- B-spline based functions with optimized knots
- Gaussian mixtures (centered at strategic locations)
- Exponential decay with optimized parameters

## Phase 3: Probe-First Evaluation

For each new pattern class:
1. Generate 2-3 concrete implementations
2. Call probe_solution on ALL of them (cheap, ~10s each)
3. Rank by probe score
4. Call evaluate_solution ONLY on the top 1-2 variants
5. If all fail: call analyze_convolution to diagnose why

## Phase 4: Iterative Refinement

- When a pattern class improves: generate more variants in that class
- When stuck: call analyze_convolution on current best + failed variants
- Always use diagnostic insights to guide next generation

## Key Principles

- ANALYZE before you mutate: understand the convolution structure first
- PROBE before you commit: rank variants cheaply before full evals
- TARGETED mutations: use analysis to guide what to change, not random search
- DIVERSE exploration: if step functions stall, try smooth functions
- LEARN from failures: analyze_convolution on failed patterns reveals why
