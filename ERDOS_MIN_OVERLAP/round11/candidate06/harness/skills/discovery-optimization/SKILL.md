---
name: discovery-optimization
description: "Construction discovery strategy for Erdos problem: generate novel mathematical step function forms using probe-based screening, focus on structural innovations rather than hyperparameter tuning."
---

# Erdos Minimum Overlap - Construction Discovery Strategy

## Core Insight
The seed optimizer's 12 initialization patterns and hyperparameters are already well-tuned.
Improvement requires DISCOVERING NEW MATHEMATICAL CONSTRUCTIONS, not tuning existing ones.

## Phase 1: Systematic Construction Generation

### Pattern Categories to Explore:

1. **Asymmetric Bimodal**: Place two peaks at asymmetric locations
   - h(x) ~ sigmoid(alpha - beta*x) + sigmoid(gamma - delta*x)
   - Vary alpha, beta, gamma, delta to control peak positions and widths
   - Test alpha in [0.2, 0.8], different width ratios

2. **Multi-Scale Mixtures**: Combine coarse and fine structures
   - Coarse: step function with 2-3 broad regions
   - Fine: superimpose narrow peaks or oscillations
   - Example: base = sigmoid(x - 0.5), fine = 0.1 * sin(10*pi*x) * sigmoid(5*(x-0.5)^2)

3. **Exponential/Decay Patterns**:
   - Single peak: h(x) ~ exp(-lambda * (x - center)^2)
   - Double exponential: asymmetric decay on each side
   - Test different lambda values and center positions

4. **Piecewise Linear Constructions**:
   - Define h(x) with different linear segments
   - Ensure continuity and integral constraint
   - Example: linear rise to peak at x1, linear decay to x2, constant elsewhere

5. **Fourier-Truncated Constructions**:
   - Start with desired frequency content
   - Truncate high frequencies strategically
   - Example: h(x) = 0.5 + sum_{n=1}^{N} a_n * cos(2*pi*n*x/2)

6. **Cantor-Like Recursive Patterns**:
   - Start with uniform distribution
   - Iteratively remove/modify middle portions
   - Create fractal-like step function structures

7. **Sigmoid Mixture Models**:
   - h(x) = sum_{i=1}^{k} w_i * sigmoid(loc_i - scale_i * x)
   - Vary k (number of components), weights, locations, scales
   - Soft clustering of the function into regions

## Phase 2: Probe-Based Screening

### Workflow for Each New Pattern:
1. EDIT EVOLVE-BLOCK to add new initialization pattern
2. CALL probe_solution to check:
   - Is h in [0,1] for all x? (sigmoid output should satisfy this)
   - Is integral(h) approximately 1? (check constraint loss)
   - What's the approximate c5_bound?
3. If probe passes (constraint satisfied, reasonable score):
   - CALL evaluate_solution for exact score
4. If probe fails (constraint violation, terrible score):
   - DISCARD this pattern, move to next
5. Track best variant, continue from there

## Phase 3: Refinement

Once a promising construction is found (probe score suggests improvement):
- Use SMALL learning rate (0.001-0.005) for fine-tuning
- INCREASE num_steps (100000-200000) for better convergence
- Adjust penalty_strength to ensure constraint satisfaction
- Try NUM_RESTARTS = 5-10 for better local search

## Pattern Engineering Tips

### For bimodal patterns:
- Peak separation: try 0.2-0.3 for optimal overlap minimization
- Peak height: adjust so integral = 1
- Asymmetry: test 0.25-0.3 vs 0.7-0.75 placement

### For multi-peak patterns:
- Start with 3 peaks, optimize their positions
- Ensure peaks don't overlap too much
- Adjust widths so integral = 1

### Constraint satisfaction check:
- After editing, verify integral(h) is close to 1 in probe
- Use penalty_strength = 1000-5000 for final refinement
- If constraint violated, reduce learning rate or adjust pattern

## Budget Management

- MAX 30 evaluations total
- Use probe_solution for ALL new patterns (don't waste full evals)
- Call evaluate_solution only on top 2-3 promising variants
- If no improvement after 10 evals, try fundamentally different approach
