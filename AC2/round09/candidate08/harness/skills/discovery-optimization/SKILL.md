---
name: discovery-optimization
description: "Mathematical discovery: Explore diverse function families (splines, Fourier, mixtures, splines) to find novel constructions that surpass the step-function champion for the second autocorrelation inequality constant C2."
---

# Mathematical Discovery Strategy
## Objective Maximize C2 = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}) by discovering novel function families beyond the current step-function champion.
## Core Principle The seed's step functions achieve 0.8962799441554086. To beat this, you need function families with fundamentally different properties: - **Smoother transitions**: Reduce oscillations in convolution - **Multi-scale features**: Balance local and global mass distribution - **Asymmetric designs**: Exploit non-symmetric optimal configurations
## Strategy: Diversity Over Incrementalism Each evaluation costs precious budget. Do NOT make small incremental edits. Instead:
1. **Experiment 1: Spline-based functions** - Replace step heights with cubic spline coefficients - Use scipy.interpolate.CubicSpline for smooth transitions - Optimize 5-10 spline control points instead of hundreds of step levels
2. **Experiment 2: Fourier optimization** - Optimize Fourier coefficients directly - Enforce positivity in spatial domain via phase constraints - Use only 10-20 Fourier modes for efficiency
3. **Experiment 3: Gaussian mixture** - Construct f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²)) - Optimize weights, centers, and widths - Start with 3-5 components, refine to 8-12
4. **Experiment 4: Piecewise polynomial** - Instead of constant steps, use quadratic or cubic segments - Ensure C² continuity at boundaries - Optimize breakpoints and coefficients
## Implementation Guidelines - Always use jax.jit for convolutions - Keep discretization at ~400 intervals (seed's choice) - Use jax.nn.softplus for positivity constraints - Parallelize experiments internally if possible - Report actual c2 values in comments
## Success Criteria Any c2 > 0.8962799441554086 is a breakthrough. Aim for combined_score > 1.02.
