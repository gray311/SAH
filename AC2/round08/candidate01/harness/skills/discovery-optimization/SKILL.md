---
name: discovery-optimization
description: "C2 maximization via novel function architectures. Use fourier_space_probe to analyze frequency properties, explore mixtures and multi-scale approaches."
---

# C2 Maximization: Novel Function Architectures

## Critical Insight

The seed program already creates TRUE step functions with score 1.03431. The challenge is exploring NOVEL architectures:
- Fourier-space optimized functions
- Mixture models (weighted combinations)
- Multi-scale refinements
- Spline-based approaches

## Step 1: Fourier Analysis

Call fourier_space_probe FIRST to understand frequency characteristics:
- Look at dominant frequency bands
- Check spectral energy distribution
- Identify frequency-domain patterns

## Step 2: Architecture Exploration

Try different function classes:

### Mixture Models
- Combine multiple basis functions with learned weights
- Example: f(x) = w1*gaussian1 + w2*gaussian2 + w3*step

### Multi-Scale Optimization
- Start on coarse grid, refine around promising regions
- Use adaptive discretization

### Fourier-Space Optimization
- Optimize in frequency domain with positivity constraints
- Use FFT for efficient convolution

## Step 3: Probe & Rank

- Use fourier_space_probe to compare spectral properties
- Use probe_solution to rank variants cheaply (~10s each)
- Only evaluate TOP 2-3 candidates

## Step 4: Verify and Evaluate

- Only call evaluate_solution if probing shows promise
- Track which architectures work best
- Iterate on successful patterns

## Architecture Templates

### Template A: Gaussian Mixture
f(x) = sum(w_i * exp(-((x - mu_i)/sigma_i)^2))

### Template B: Step Mixture  
f(x) = sum(w_i * I(x in [a_i, b_i]))

### Template C: Spline-Based
Use cubic splines with optimized knot positions

### Template D: Fourier-Optimized
Optimize Fourier coefficients with inverse FFT for positivity
