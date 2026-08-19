---
name: barrier-breaking-c2
description: Strategy for surpassing C2 = 0.8962799441554086 using multi-method exploration. Combines gradient refinement with explicit step/piecewise constructions.
---

# Barrier-Breaking C2 Strategy
## Current State
- Best achieved: 0.999789xrecord (approx 0.89627)
- Target: > 1.0000xrecord (> 0.8962799441554086)

## Why Gradient Descent Alone Fails
- Continuous representations smooth out the sharp features that achieve the record
- The record-holder (AlphaEvolve) used step functions
- Need to explicitly construct or discover step-like behavior

## Actionable Strategies
### 1. Explicit Piecewise Construction
Replace continuous function with explicit breakpoints/heights:
- Use SEARCH/REPLACE to change the function definition
- Test with 10-20 breakpoints (adjustable)
- Probes: 5 variants with different breakpoint distributions

### 2. Hybrid Gaussian-Step
Combine smooth center with step wings:
- Start: f(x) = exp(-x^2/(2*sigma^2))
- Modify: f(x) = max(gaussian, step_height) for |x| > step_width
- Parameters: sigma in [0.5, 2.0], step_width in [1.0, 3.0], step_height in [0.1, 1.0]

### 3. Fourier-Positivity Optimization
- Initialize FFT coefficients from a Gaussian in frequency domain
- Enforce positivity after IFFT: f = exp(softplus(log(f + eps)))
- Optimizes coefficients directly

### 4. Learning Rate Adaptation
If stuck: reduce LR by 10x, extend warmup to 2000 steps
- Use: optax.chain(optax.scale(0.1), optax.adam(learning_rate=...))

## Evaluation Protocol
1. Pick a strategy
2. Generate 5-10 variants with probe_solution
3. Rank by probe score
4. Evaluate top 1-2 with evaluate_solution
5. If no improvement after 3 full evals, change strategy

## Success Metrics
- combined_score > 1.0000 (definitive improvement)
- combined_score > 1.0005 (safe margin)
