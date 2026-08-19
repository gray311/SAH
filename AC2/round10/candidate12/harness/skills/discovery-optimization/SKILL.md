---
name: discovery-optimization
description: "Discover novel function classes beyond step functions. Use generate_diverse_init for structural diversity, multi-scale refinement, and rigorous probe filtering."
---

# C₂ Function Discovery Strategy

## Phase 1: Diversity Injection
1. Call generate_diverse_init to get a new function representation (spline, mixture, asymmetric, etc.)
2. Start with coarse discretization (100-200 intervals) for fast initial search
3. Generate 10-15 variants with different parameters

## Phase 2: Probe-Driven Selection
1. Evaluate all 10-15 variants with probe_solution (cheap, separate budget)
2. Rank by probe score, keep top 2
3. If top probe score < current best by 0.001, discard this class

## Phase 3: Refinement
1. For promising classes, refine to 400+ intervals
2. Apply targeted mutations (±5% parameter changes)
3. Continue probe→eval loop until stagnation

## Phase 4: Class Switching
1. If no improvement after 3 successful evals in current class, switch representation
2. Reset to best known score as baseline
3. Explore next class from generate_diverse_init

## Function Representations

### Spline-based
- B-splines with optimized knots
- Cubic segments with continuity constraints
- Adaptive knot placement (denser where gradients high)

### Mixture Models
- Weighted sum of Gaussians: Σ w_i * exp(-(x-μ_i)²/(2σ_i)²)
- Exponential mixtures: Σ w_i * exp(-|x-μ_i|/λ_i)
- Trigonometric mixtures: Σ w_i * cos(k_i*x) * exp(-|x|/λ_i)

### Asymmetric Patterns
- Left-heavy steps: more mass on left side
- Right-heavy steps: more mass on right side
- Irregular width steps: non-uniform segment lengths
- Single high peak with asymmetric tails

### Key Principles
- Start simple (few parameters), increase complexity only if needed
- Enforce f(x) ≥ 0 via softplus, exp, or squared transformations
- Use FFT-based convolution for efficiency
- Log all variants with parameters for reproducibility

## When to Stop
- Budget exhausted (30 evals)
- 5 consecutive evals with no improvement
- Best score > 1.05 (breakthrough achieved)
