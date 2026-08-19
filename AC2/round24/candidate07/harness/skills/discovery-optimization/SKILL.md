---
name: discovery-optimization
description: "Multi-family function search for C\u2082 maximization. Explores step patterns, Gaussian mixtures, splines, and hybrids. Avoid incremental step refinement; change function families."
---

# C2 Maximizer: Multi-Family Function Search

## Core Principle
AlphaEvolve optimized step functions to 0.89628, but that may not be the global maximum. We must explore NEW function families: Gaussian mixtures, splines, and step-smooth hybrids.

## Phase 1: Scan & Expand Step Search (iterations 1-10)

Step 1: Scan All Seed Patterns
- Call scan_pattern_variants() with pattern_idx=0..11
- This explores the seed's hidden search space (12 distinct step families)
- Record the best pattern's c2 score

Step 2: Evaluate Top Patterns
- If best scan score > seed (1.042): call evaluate_solution on top 3 patterns
- If all 12 patterns ≤ seed: switch to Phase 2 immediately

Step 3: Expand Step Search
- Create hybrid patterns: merge best pattern with adjacent patterns
- Try multi-peak combinations within the same pattern framework
- Probe all, evaluate best

## Phase 2: Smooth Function Exploration (iterations 11-20)

### Gaussian Mixtures
f(x) = Sum of w_i * exp(-(x-μ_i)^2/(2σ^2))
- Choose k=3-5 Gaussians with optimized weights (Sum w_i = 1), centers (μ_i), and width (σ)
- Use JAX to optimize these 2k-1 parameters
- Start with symmetric 2-Gaussian: centers at ±μ, equal weights, shared σ

### Spline-Based Functions
- Piecewise linear or quadratic functions with k=5-10 breakpoints
- Optimize breakpoint positions and segment heights
- Ensure continuity at breakpoints for smoothness

### Hybrid Step-Smooth
- Steps at domain edges for plateau behavior
- Smooth transitions in middle regions
- Try tanh-based interpolation: f(x) = (1 + σ * tanh(α(x-x0))) / 2

## Phase 3: Multi-Scale & Hybrid Families (iterations 21-30)

1. Multi-resolution: coarse step skeleton + fine smooth details
2. Fourier-constrained: optimize Fourier coefficients, ensure inverse FFT is non-negative
3. Try completely different kernels: B-splines, wavelets, rational functions

## Tool Usage Rules
- scan_pattern_variants: Call ONCE per iteration to explore seed patterns (12 calls total max)
- probe_solution: Call on 3-5 variants per family before full eval
- evaluate_solution: Call on TOP 1-2 by probe score
- NEVER spend probes on step-parameter edits (they are not directly editable)
