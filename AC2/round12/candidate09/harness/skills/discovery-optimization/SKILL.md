---
name: discovery-optimization
description: "C2 maximization through orthogonal exploration. Generate diverse function families (spline, Gaussian mixture, Fourier, piecewise polynomial) before refining. Exploit different mathematical structures to escape local optima of step function patterns."
---

# C2 Maximizer: Orthogonal Function Class Exploration

## Core Principle

The seed's step function patterns are locally optimized. Don't refine them incrementally. Instead, explore ENTIRELY DIFFERENT function families that exploit different mathematical properties.

## Phase 1: Diversity Exploration

1. Call generate_function_class ONCE to get 5-7 function candidates from diverse families:
   - Smooth spline (C2 continuous piecewise polynomial)
   - Gaussian mixture (2-4 components, different variances)
   - Fourier-based (optimized frequency coefficients with inverse transform)
   - Piecewise cubic polynomial
   - Rational function construction
   - Smoothed step (sigmoid-based transition)
   - B-spline construction

2. For each candidate:
   - Call edit_solution to implement the COMPLETE function definition
   - Call evaluate_solution (ONE eval per candidate)
   - Track which function CLASS gives best score

3. Stop generating new classes once you find ONE that outperforms the seed (1.03841)

## Phase 2: Systematic Refinement

Only after finding a promising function class:
- Refine that specific class using targeted mutations
- Keep other classes frozen as baselines

## Critical Success Factors

1. DIVERSITY FIRST: Spend first 10 evals exploring different function families
2. COMPLETE DEFINITIONS: Each edit must be a complete, runnable function
3. EVALUATE EARLY: If a class underperforms after 1-2 variants, abandon it
4. ONE WINNER: Focus refinement on the best-performing class

## Known Function Families & Properties

- Splines: C2 continuous, excellent for smooth optimization, many free parameters
- Gaussian mixtures: Analytic convolution, easy to optimize, naturally non-negative
- Fourier-based: L1/L2 norms easy to compute in frequency domain
- Piecewise cubic: Smooth transitions, good balance of complexity and control

## Failure Modes to Avoid

- X: Refining step functions before exploring other classes
- X: Generating multiple variants of the same class before trying new classes
- X: Using probe_solution (unreliable for this task)
- X: Incomplete function definitions that fail to evaluate
