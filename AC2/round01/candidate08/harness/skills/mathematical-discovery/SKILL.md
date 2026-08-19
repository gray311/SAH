---
name: mathematical-discovery
description: Strategy for optimizing mathematical constants - explore multiple function representations (piecewise, Fourier, splines), use coarse-to-fine optimization, employ probe-driven variant ranking, and test diverse optimization strategies (gradient, coordinate descent, evolutionary).
---

# Mathematical Discovery for C2 Optimization

## Objective
Maximize C2 = ||f★f||₂² / (||f★f||₁ ||f★f||_∞) for non-negative f: ℝ → ℝ
Target: beat 0.8962799441554086 (seed), current best ~0.999789

## Key Strategies

### 1. Multi-Representation Exploration
Try these function representations, testing each separately:
- **Piecewise constant/linear**: Current approach; refine num_intervals (20→50→100→200)
- **Fourier truncation**: Optimize Fourier coefficients with non-negativity in spatial domain
- **B-splines**: Smooth piecewise polynomials with optimized knot positions
- **Gaussian mixtures**: Sum of Gaussians with learnable centers, widths, amplitudes
- **Step functions**: Known to achieve ~0.896; try many breakpoint configurations
- **Exponential decay variants**: exp(-x^α), asymmetric decays
- **Mixture models**: Weighted combinations of the above

### 2. Optimization Strategy Diversity
For each representation, try:
- **Adam with warmup**: Current default; good for early exploration
- **L-BFGS-B**: Quasi-Newton with bounds; good for final refinement
- **Coordinate descent**: Optimize one parameter at a time
- **Simulated annealing**: Global search with cooling schedule
- **Genetic algorithms**: Crossover/mutation on function parameters
- **Multi-scale**: Coarse optimization → fine refinement

### 3. Coarse-to-Fine Strategy
- Start with low resolution (num_intervals=20-30)
- Optimize for 5000-10000 steps
- Increase resolution to 50, 100, 200
- Fine-tune with 10000-20000 steps at highest resolution
- Keep track of best result at each resolution

### 4. Probe-Driven Workflow
With 20 evals and ~36 iterations:
- Each iteration: Call probe_solution 3-5 times on variants
- Pick top 1-2 variants by probe score
- Call evaluate_solution ONCE on the best variant
- Analyze result, generate next round of variants
- Repeat until evals exhausted or plateau

### 5. Parameter Systematic Search
- num_intervals: [20, 30, 50, 100, 200] (test in stages)
- learning_rate: [0.001, 0.01, 0.05, 0.1] (adaptive schedules)
- num_steps: [5000, 10000, 15000, 20000] (per resolution)
- Try cosine decay, linear decay, constant schedules

### 6. Positivity Enforcement
Use jax.nn.relu, exp, softplus to ensure f(x) ≥ 0
This is critical for validity; violations cause combined_score = 0

### 7. Early Stopping & Diversity
- If one representation plateaus for 2 iterations, try a different representation
- Maintain diversity: don't modify the best-scoring version directly
- Save promising candidates, not just the current best

## Tool Usage
- probe_solution: Generate 3-5 variants, probe all, pick winner → full eval
- evaluate_solution: Only after probing; this is your precious budget
- edit_solution: Use SEARCH/REPLACE for targeted changes; preserve working code
- finish: When evals exhausted or no improvement in 5 iterations

## Common Pitfalls
- Don't rewrite working code unnecessarily
- Don't trust probe scores as absolute; use them for relative ranking only
- Don't exceed time budget (use JAX JIT, FFT, subsampling)
- Don't forget f(x) ≥ 0 constraint
- Don't use the same approach twice without learning from results
