---
name: math-functional-exploration
description: Playbook for exploring mathematical function classes beyond step functions. Focus on splines, Fourier, and neural-based representations with C2 optimization.
---

# Mathematical Function Exploration

## Goal
Discover functions that beat the step function record of C2 = 0.8962799441554086.

## Function Classes to Explore

### 1. B-Splines
- Use cubic B-splines with optimized knot positions
- Knots can be learned or strategically placed
- Ensure non-negativity via convex combination with non-negative B-spline basis
- Pros: Smooth, flexible, computationally efficient

### 2. Fourier Series with Positivity
- Represent f(x) as truncated Fourier series
- Positivity constraint: f(x) = Re(fourier_coeffs * exp(i*...)) >= 0
- Can use softened constraints: f(x) = exp(Re(fourier_coeffs * exp(i*...)))
- Pros: Exploits periodicity, efficient FFT-based convolution

### 3. Neural Networks with Mathematical Priors
- Single hidden layer with softplus activation for positivity
- Or: tanh(Net) to ensure boundedness plus positivity
- Input: x; Output: softplus(W*x + b)
- Pros: Universal approximator, automatic differentiation

### 4. Piecewise Polynomials
- Different polynomial on each interval
- Optimize coefficients and boundary points
- Can use Bernstein polynomials for guaranteed positivity
- Pros: Local control, flexible

### 5. Mixture Models
- Convex combination of 2-5 simple functions
- Each component: Gaussian, exponential, uniform, triangular
- Optimize weights, parameters, and centers
- Pros: Interpretable, builds on step function success

## Search Protocol
1. Select one function class above
2. Design a bounded internal search (<=2000 iterations)
3. Generate 5-10 candidate functions
4. Use probe_solution to rank them cheaply
5. Call evaluate_solution on top 2-3 candidates
6. If no improvement, try different function class

## Implementation Tips
- Use JAX for automatic differentiation if optimizing parameters
- Use numba JIT for speed in internal loops
- Keep per-evaluation time < 30s by limiting internal iterations
- Return structured output: best_c2, function_representation, method_used
- Always enforce f(x) >= 0 and integral(f) > 0
