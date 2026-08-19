---
name: discovery-optimization
description: "Immediately switch from piecewise-linear to step functions using convert_to_step_functions.\nEvaluate quickly with full evals rather than excessive probing. If step functions fail, try Gaussian mixtures.\nBudget is 20 evals - use them wisely for major representation changes, not small probes."
---

# C2 Optimization: Step Function Switch Strategy

## Objective
Maximize C2 > 1.026. Current baseline: 1.02665 (piecewise-linear). 
RECORD HOLDER is step functions at 0.8963 - switch to them FIRST.

## Critical Insight
The seed program optimizes piecewise-LINEAR functions. This is suboptimal - step (piecewise-CONSTANT)
functions achieved the theoretical best in literature. DO NOT continue optimizing linear functions.

## Phase 1: Immediate Switch to Step Functions
1. Call convert_to_step_functions IMMEDIATELY
   - This rewrites the EVOLVE-BLOCK to use pure step functions
   - Creates 2-5 rectangular pulses with optimized parameters
   - Ensures non-negativity and proper convolution handling

2. Call probe_solution ONCE to see approximate score

3. Call evaluate_solution to confirm - this is your budget decision point

4. If step functions work (score > 1.02665): 
   - Continue optimizing step widths, heights, positions
   - Try 2 pulses, 3 pulses, 5 pulses configurations
   - Each change: probe once, then eval

5. If step functions FAIL (score <= 1.02665):
   - Call mutation_probe to get Gaussian mixture variants
   - Switch representation completely (not parameter tuning)

## Phase 2: Alternative Representations
### Gaussian Mixtures
- Combine 2-5 Gaussians with varied means and sigmas
- Use softplus for non-negativity
- Cluster in center for better convolution peaks

### B-Splines  
- 5-15 knots with adaptive spacing
- Emphasize center region

### Exponential Combinations
- Double/triple exponentials with decay rates
- Create plateau-like behavior

## Phase 3: Deep Optimization
Within each successful representation:
1. Modify 1-2 key parameters (widths, heights, number of components)
2. Probe once
3. Evaluate
4. Repeat with different parameters if improved

## Budget Discipline
- 20 total evals - use each one to confirm a REPRESENTATION SWITCH
- Max 2 probes per variant before evaluating
- Never spend 5+ probes on one family
- If stuck after 3 evals per representation: SWITCH REPRESENTATION

## Key Rules
- convert_to_step_functions FIRST - do not waste evals on linear optimization
- Evaluate major representation changes immediately
- Probe max 1-2 times per variant
- Switch representation after 3 evals with no improvement
- Track: which representation achieved what score
