---
name: c2-representation-revolution
description: A method playbook for escaping local optima by changing function representations, not just parameters. Focuses on structural diversity using probe-based ranking.
---

# C₂ Representation Revolution Playbook

## Core Insight
The seed program uses piecewise-linear optimization with 300 intervals and 40k steps.
Parameter tuning alone will NOT escape the local optimum. You must CHOOSE DIFFERENT FUNCTION CLASSES.

## Phase 1: Representation Census (probe_solution)

Use probe_solution to test these representation families. Aim for 20-25 probes total across classes.

### A. Piecewise-Constant (Step Functions)
- **Why**: Current record-holder for C₂ (0.8963 baseline). Simple, interpretable.
- **Parameterize**: Array of N bin heights with configurable support positions and heights.
- **Probe variants**:
  * N=10, 20, 50, 100 intervals
  * Symmetric: support [0.25, 0.75]
  * Asymmetric: support [0.2, 0.8], [0.15, 0.55], etc.
  * Multi-level: 2-3 height levels in different intervals
- **Key insight**: Vary support positions and height ratios, not just number of intervals.

### B. Piecewise-Linear (Baseline - Be Careful)
- **Why**: Current seed approach. May be in local optimum.
- **Don't just tune parameters!** Try structural changes:
  * Different node counts (100 vs 300)
  * Symmetric triangular peaks
  * Multi-modal with multiple peaks
  * Different support widths
- **Probe budget**: Limited - prioritize other classes first.

### C. Gaussian Mixture Models
- **Why**: Smooth, convex-like behavior. Often optimal for integral-based problems.
- **Parameterize**: K means, variances (σ²), weights (w). Ensure non-negativity via exp().
- **Probe variants**:
  * K=2, 3, 5, 10
  * Equal variance vs adaptive
  * Means constrained to grid vs continuous
  * Weight constraints (sum to 1, min weight > 0)
- **Key insight**: Start with K=2 (simple), then K=5 (moderate complexity).

### D. Exponential Combinations
- **Why**: Natural decay, positive everywhere, smooth.
- **Parameterize**: Σ w_i * exp(-α_i * |x - μ_i|) with w_i ≥ 0.
- **Probe variants**:
  * Single exponential (baseline)
  * Double exponential with different rates
  * Sum of 2-5 exponentials with different decay rates
  * Mix with polynomial factors
- **Key insight**: Try different decay rate ratios (slow + fast).

### E. B-Spline Basis Functions
- **Why**: Local support, C^k continuity control, flexible shape.
- **Parameterize**: Knot positions + spline coefficients.
- **Probe variants**:
  * Uniform knot placement (n, 2n, 3n)
  * Adaptive knots concentrated in support region
  * Different knot orders (3, 4, 5)
- **Key insight**: Knot placement matters more than coefficient tuning.

### F. Fourier-Space Optimization
- **Why**: Global parameterization, implicit smoothness constraints.
- **Parameterize**: Fourier coefficients with inverse-FFT positivity check.
- **Probe variants**:
  * Low-frequency dominant (first N coefficients)
  * Band-limited with hard cutoff
  * Real-valued symmetric (cosine series)
- **Key insight**: Fewer parameters, strong smoothness prior.

## Phase 2: Multi-Start within Each Class

For the top 2-3 representation classes by probe score:
1. Create 5-10 different initializations per class (different parameters)
2. Each runs a full optimization with different seeds
3. Track best from each class separately

## Phase 3: Hybrid Approaches

- Ensemble: Weighted average of top performers from different classes
- Mixture: Combine components from Gaussian + step + exponential
- Analyze winners: What structural properties do they share?

## Best Practices

- **Probe first, evaluate later**: 15-20 probes per representation family
- **Diversify immediately**: Don't spend evals on piecewise-linear alone
- **Track by class, not by edit**: Remember which function class each score belongs to
- **Reserve 5 evals**: One for each of the top 5 probe performers (different classes)
- **Validate**: Ensure f(x) ≥ 0, ∫f > 0 for all candidates

## When Stuck

- If scores plateau for 5+ iterations: Call scan_function_space, then try a NEW representation class.
- Never tune the same representation class for more than 2 full evaluations without trying another class.
- The goal is to find the RIGHT function class, not the best parameters for the wrong class.
