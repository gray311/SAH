---
name: discovery-optimization
description: "C\u2082 maximization via convolution structure analysis. Use analyze_convolution_structure to find where ||f\u2605f||\u221e is concentrated vs where ||f\u2605f||\u2082\u00b2 can be increased, then generate mathematically-grounded function modifications. Explore step patterns first, then switch to spline/continuous representations if needed."
---

# C₂ Maximizer: Convolution-Aware Pattern Discovery

## Phase 1: Analyze Current Best (MANDATORY FIRST STEP)

1. Call analyze_convolution_structure on the current best function
2. Note: Where is the convolution's infinity norm achieved? What's the shape of the L2 norm distribution?
3. Identify: Can we reduce the peak by spreading mass? Can we boost the L2 norm by concentrating mass in high regions?

## Phase 2: Generate Modifications

**Option A: Step Pattern Restructuring** (if current best is a step pattern)

Use the analysis to:
- Adjust heights: Reduce tall peaks that dominate ||f★f||∞, boost heights where convolution is already high
- Reposition intervals: Shift intervals to avoid constructive interference at the infinity norm location
- Add asymmetric peaks: Break symmetry to spread convolution mass

**Option B: Switch to Continuous Functions** (if step patterns stagnate)

Try these representations:
- Exponential decay: f(x) = exp(-α|x - μ|) with optimized α, μ
- Quadratic splines: Piecewise quadratic with optimized breakpoints
- Gaussian mixture: Sum of Gaussians with optimized weights, means, std devs
- Polynomial decay: f(x) = x^(-α) for x > 0, symmetric extension

## Phase 3: Evaluation

- Each new function: Call evaluate_solution ONCE
- If score improves: Drill deeper into that representation class
- If score decreases: Analyze with analyze_convolution_structure again and adjust

## Key Principles

- Analysis before modification: Never edit blindly
- New architectures over tweaks: Completely new function classes beat parameter tuning
- One evaluation at a time: Learn from each result before trying another
- Mathematical reasoning: Understand WHY a modification should help
