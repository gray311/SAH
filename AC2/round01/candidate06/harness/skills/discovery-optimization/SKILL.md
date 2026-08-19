---
name: discovery-optimization
description: "Multi-strategy C2 optimization harness. Combines gradient-based refinement with explicit piecewise/step function construction to break through the 0.8962799441554086 barrier. Uses probes for variant ranking."
---

# C2 Barrier-Breaking Strategy

## Objective
Surpass C2 = 0.8962799441554086. Current best in session: 0.999789xrecord.

## Why We Are Stuck
Pure gradient descent on continuous representations gets trapped. The record-holder used step functions.

## Multi-Strategy Playbook

### Strategy 1: Adaptive Gradient Refinement
- Reduce learning rate by 10x if loss plateauing
- Use warmup + cosine decay with extended decay phase
- Add gradient clipping (max norm 1.0) for stability

### Strategy 2: Explicit Piecewise Construction (PRIORITY)
Construct f(x) as piecewise-linear segments explicitly:
breakpoints = jnp.array([...] ) # e.g., [-5, -3, -1, 1, 3, 5]
values = jnp.array([...])         # f(breakpoints), ensure >= 0
This gives the optimizer discrete control over function shape.

### Strategy 3: Step-Function Hybrids
Start with a Gaussian: f(x) = exp(-x^2/(2*sigma^2))
Then modify to add flat regions (step-like) at the tails:
f = jax.nn.relu(exp(-x**2/(2*sigma**2)) * (1 + step_mask))
This combines smooth center (good for convolution peak) with step wings (like record-holder).

### Strategy 4: Fourier-Space Optimization
Optimize FFT coefficients directly, then IFFT to get f:
fft_coeffs = ...  # Initialize with Gaussian in frequency domain
f = jnp.fft.ifft(fft_coeffs).real
Enforce positivity: f = exp(softplus(log(f + eps)))

## Probe-Based Iteration Loop
1. Pick a strategy
2. Generate 5-10 variants using probe_solution (cheap, ~10s each)
3. Rank by probe score
4. Pick top 1-2, call evaluate_solution (full score, ~minutes)
5. If beaten best_so_far, escalate to more variants

## Tool Usage
- edit_solution: Implement ONE strategy variant. Use SEARCH/REPLACE for targeted changes.
- probe_solution: Test 5-10 variants before full evaluation. Use subsampled discretization (fewer intervals).
- evaluate_solution: Only for variants with strong probe promise. Budget: ~20 evals total.
- finish: When best_so_far >= 1.0005xrecord or out of evaluations.

## Critical Success Factors
- Diversity: Try fundamentally different function representations (continuous, piecewise, step-based)
- Convergence: Use smaller steps near 0.999789 to fine-tune
- No Wasting: Each evaluation must encode a fresh hypothesis

## Known Patterns from Literature
- AlphaEvolve record: step functions (piecewise constant)
- Symmetry: Even functions (f(x) = f(-x)) reduce complexity
- Normalization: int f appears in denominator, so scale matters
