---
name: discovery-optimization
description: "Explore novel function families for C\u2082 optimization. Systematically test splines, polynomials, Fourier mixes, and asymmetric patterns. Use probes to benchmark entire families before committing eval budget to full evaluation."
---

# C₂ Function Discovery Strategy

## Core Principle
The seed's step functions achieve 0.8962799441554086. To beat this, we must explore FUNCTION CLASSES beyond step functions, not just tune step parameters.

## Function Families to Explore (in priority order)

1. **C³ Continuous Splines**
   - Use cubic splines with optimized knot positions
   - Ensure C³ continuity for smoothness benefits
   - Test 5-7 knot configurations

2. **Piecewise Polynomial Functions**
   - Quadratic or cubic pieces with optimized coefficients
   - Test 3-5 pieces with varying widths
   - Preserve non-negativity constraint

3. **Fourier-Based Representations**
   - Optimize Fourier coefficients with positivity constraints
   - Test different frequency combinations
   - Use IFFT to reconstruct real-valued functions

4. **Gaussian Mixture Models**
   - Sum of Gaussians with optimized means, variances, weights
   - Test 2-5 components
   - Exploit smoothness advantages

5. **Asymmetric Multi-Level Steps**
   - Beyond symmetric peaks: try left/right asymmetric patterns
   - Test plateau variants with sloped transitions
   - Consider non-uniform step heights

## Search Protocol

### Phase 1: Family Benchmarking (Probes Only)
- For each new family, implement 3-5 variants
- Probe all variants (cheap, ~10s each)
- Track best probe score per family
- Identify families with promise (>1.02 combined_score)

### Phase 2: Commitment (Full Evaluations)
- Pick top 2 families by probe performance
- Implement 2-3 refined variants per family
- Full evaluate these candidates
- Re-rank by actual scores

### Phase 3: Iteration
- Build on successful families
- If stall for 8 iterations: abandon current family, try next
- Budget ending (<5 evals): try one last family-wide search

## Mutation Guidelines by Family

### Splines
- Move knots by ±5% of domain
- Adjust piece heights by ±10%
- Test knot spacing ratios: [0.2,0.4,0.6], [0.25,0.5,0.75], etc.

### Polynomials
- Test degrees 2-4
- Vary piece widths: [30%,40%,30%], [25%,50%,25%], etc.
- Optimize coefficients with initial guess from step function

### Gaussian Mixtures
- Test 2, 3, 4 component combinations
- Vary width ratios: [0.5,1.5], [1.0,2.0], [1.0,1.5,1.0]
- Optimize mean spacing

## When to Abandon a Family
- After probing 5+ variants with no >1.02 score
- After 2 full evaluations with no improvement
- After 10 total iterations without progress

## Success Criteria
- Combined score > 1.04 (C₂ > 0.935)
- Or >5% improvement over seed (combined > 1.085)
- New function class discovered with publishable C₂ value
