---
name: discovery-optimization
description: "Optimize EVOLVE-BLOCK to maximize C2 constant for autocorrelation inequality.\nEncourage structural experimentation over hyperparameter tuning. Use probes to rank variants cheaply."
---

# Structural Discovery Optimization

## Your Mission
Beat the seed score of 1.03431 by discovering fundamentally better function representations.
Step functions are the current champion - try spline, Fourier, or neural-based approaches.

## Search Strategy
1. Explore function classes:
   - B-splines with optimized knots
   - Fourier series with positivity constraints
   - Neural networks with activation constraints
   - Piecewise polynomials
   - Mixture models of simple functions

2. Internal optimization budget:
   - Design programs that do extensive internal search
   - Use multiple candidates, rank with probes, then evaluate best
   - Do not optimize a single fixed function

3. Multi-stage approach:
   - Stage 1: Coarse search over many designs
   - Stage 2: Refine top 3-5 candidates
   - Stage 3: Full evaluation of champion

## Evaluation Discipline
- Each edit must be a structural change, not a parameter tweak
- Use probe_solution to quickly rank your variants before full evaluation
- Call evaluate_solution only 1-2 times per major hypothesis
- If validity=0 or score < previous best, try a DIFFERENT approach entirely

## Common Pitfalls to Avoid
- Incremental hyperparameter changes (learning rate, steps)
- Same function class with minor modifications
- Not using probe_solution for quick ranking
- Rewriting whole block when only one part needs change

## Tools Guide
- edit_solution: Search/REPLACE for targeted changes; full rewrite for structural changes
- evaluate_solution: TRUE score, costs 1 evaluation. Best score retained automatically.
- probe_solution: Approximate score on subsample. Use to rank 3-5 variants before evaluating best.
- finish: When you have exhausted ideas or evaluations.

## Winning Pattern
Program structure:
For each design_id in [0..N-1]:
  Generate candidate f_id via DIFFERENT REPRESENTATION
  Compute C2 via probe
Rank by probe score
Evaluate top 3 with full evaluation
Return best
