---
name: orthogonal-exploration-protocol
description: Strategy for exploring diverse function families before refining. Use orthogonal directions to escape local optima.
---

# Orthogonal Exploration Protocol for C2 Maximization

## Core Principle

The seed's step function patterns are locally optimized. Incremental mutations won't escape the local optimum. You MUST explore fundamentally different function families first.

## Phase 1: Diversity Exploration (First 10 evals)

1. Call generate_function_class ONCE to get 5-7 complete function definitions from diverse families:
   - Smooth spline (C2 continuous piecewise polynomial)
   - Gaussian mixture (2-4 components)
   - Fourier-based construction (optimized frequency coefficients)
   - Piecewise polynomial (cubic splines with optimized knots)
   - Rational function construction
   - Smoothed step (sigmoid-based transition)
   - B-spline construction

2. For each function class:
   - Call edit_solution to implement the COMPLETE definition
   - Call evaluate_solution (ONE eval per class)
   - Record the score and function class name

3. Decision rule:
   - If ANY class beats 1.03841: STOP generating new classes, refine that winner
   - If ALL classes underperform: Generate new classes, continue until budget exhausted

## Phase 2: Systematic Refinement

Only after finding a promising function class:
- Focus refinement on THAT class only
- Use targeted mutations appropriate to the class:
  * Splines: Adjust knot positions (+/-0.05 of domain), optimize polynomial coefficients
  * Gaussian mixtures: Adjust means (+/-0.1), variances (+/-0.3), weights (maintain sum=1)
  * Fourier-based: Adjust frequency weights, optimize amplitude spectrum
  * Piecewise: Adjust boundary positions, optimize piece coefficients

## Critical Success Factors

1. DIVERSITY FIRST: Spend first 10 evals exploring different function families, not refining one
2. COMPLETE DEFINITIONS: Each edit must be a complete, runnable function - no dependencies
3. NO PROBE SOLUTION: Use evaluate_solution directly - probe scores are unreliable for this task
4. ONE WINNER FOCUS: Don't spread efforts across multiple classes; focus on the best performer

## Why This Works

Each function family exploits different mathematical properties:
- Splines: Smooth, high-approximation power, many free parameters
- Gaussian mixtures: Analytic convolution, naturally non-negative
- Fourier-based: Frequency-domain optimization, L1/L2 norm easy to compute
- Piecewise: Local control with smooth transitions

A fundamentally different family may have a completely different path to the global optimum.

## Failure Modes to Avoid

- X: Refining step functions before exploring other classes
- X: Generating 3+ variants of the same class before trying new classes
- X: Using probe_solution (unreliable, wastes budget)
- X: Incomplete function definitions that fail to evaluate
