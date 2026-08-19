---
name: discovery-optimization
description: "Maximize C\u2082 by exploring diverse function classes beyond step functions.\nFocus on structural changes (splines, Gaussians, hybrids) and systematic pattern discovery.\nUse evaluator efficiently: one coherent class per evaluation."
---

# C₂ Optimization: Breaking Through the Step Function Plateau

## Phase 1: Exploratory Diversity

### Try These Function Classes (in order):

1. **Step Functions (baseline)**: 
   - Variations on seed patterns: adjust heights by ±0.05, widths by ±5%
   - Try 3-5 variants, pick best for full evaluation

2. **Smoothed Steps**: 
   - Step functions with linear transitions at boundaries
   - Parameters: transition width (0.01-0.05 of domain), same step positions

3. **Gaussian Mixtures**:
   - Sum of 2-5 Gaussians: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))
   - Parameters: means (uniform on [0,1]), sigmas (0.05-0.3), weights (sum to 1)
   - Enforce non-negativity (automatic with Gaussians)

4. **Cubic Splines**:
   - B-spline basis with optimized coefficients
   - Parameters: knot positions (quantiles of [0,1]), coefficients (non-negative)
   - Use 20-50 knots for flexibility

5. **Hybrid Functions**:
   - Step core with smooth tails
   - Parameters: step start/end positions, tail decay rates

## Phase 2: Structural Optimization

Once you identify a promising class:
1. Fix the function family
2. Systematically optimize parameters using the reinit mechanism
3. Try different interval counts (coarse→fine or fine→coarse)
4. Explore symmetry: even functions (f(x)=f(-x)) reduce complexity

## Phase 3: Breaking Through

If no improvement after 10 evals:
- Reset to completely new function class
- Try asymmetric patterns more aggressively
- Increase complexity: more peaks, more parameters
- Combine successful elements from multiple runs

## Evaluation Discipline

- Each evaluation is precious: spend wisely
- If a class doesn't show promise in 2 probe attempts, abandon it
- Build on successes: if Gaussian mixtures beat steps, expand that search
- Document what works: heights that succeed, widths that matter

## Recovery Strategies

- Stalled: switch function family immediately
- Score drops: revert to previous best, try different parameterizations
- Budget ending (<5 evals): commit to one promising direction or finish
