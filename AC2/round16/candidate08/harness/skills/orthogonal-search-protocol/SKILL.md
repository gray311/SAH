---
name: orthogonal-search-protocol
description: Systematically explore mathematically orthogonal function spaces without probe-based filtering. Exhaust each space before moving to the next. NEVER use unreliable probes.
---

# Orthogonal Search Protocol for C₂ Maximization

## Core Principle

Step functions are local optima in a specific function space. To beat them, you MUST work in SPACES that are mathematically orthogonal to steps - not smooth steps, but fundamentally different representations.

## The Function Space Hierarchy

Work through these spaces sequentially, exhausting each before moving on:

### 1. Fourier Eigenfunction Space
- Represent f as linear combination of sine/cosine eigenfunctions
- Optimize coefficients, not positions of "steps"
- Key insight: Convolution becomes multiplication in Fourier space

### 2. Laguerre Polynomial Space
- Natural for functions with exponential decay
- Orthogonal basis for weighted L² spaces
- Try: f(x) = sum a_n * L_n(alpha*x²) * exp(-alpha*x²/2)

### 3. Variational Trial Space
- Use ansatz functions from calculus of variations
- Example: f(x) = (1 + alpha*cos(beta*x))^n * exp(-gamma*|x|)
- These satisfy optimality conditions for certain energy functionals

### 4. Hermite-Gaussian Space
- Eigenfunctions of the Fourier transform
- Natural for convolution-optimized functions
- Try: f(x) = sum a_n * H_n(sqrt(alpha)*x) * exp(-alpha*x²/2)

### 5. Dense-Sparse Hybrid Space
- Smooth envelope with localized feature bumps
- NOT step functions - bumps have smooth transitions
- Try: base_exp(x) + sum b_j * exp(-((x-x_j)/sigma_j)²)

## Execution Protocol

1. Pick ONE function space from the hierarchy
2. Generate 2-3 concrete implementations in that space
3. Evaluate EACH with evaluate_solution (NO PROBES)
4. If no improvement after 3 evals: switch to next space
5. Track which space is most promising
6. After exhausting all 5 spaces, consider mixed-space candidates

## Critical Rules

- NEVER use probe_solution - it is UNRELIABLE and will mislead
- NEVER refine a step pattern - completely abandon that space
- NEVER stay in one space for more than 3 evals
- ALWAYS try a mathematically distinct space when stalling
- Use temperature >= 1.0 for broad exploration

## Mathematical Intuition

The C₂ constant is tied to spectral properties. Functions whose Fourier transforms have specific structures (band-limited, sparse, etc.) may achieve better ratios. Think in terms of SPECTRAL SHAPES, not real-space steps.
