---
name: architectural-exploration-playbook
description: Playbook for discovering new function architectures beyond step functions.
---

# Architectural Exploration Playbook for C₂ Maximization

## Core Philosophy
The seed''s step patterns are LOCAL optima. To break free, you need NEW ARCHITECTURES.

## When to Use This Playbook
- After trying 2-3 step pattern mutations without improvement
- When you sense you''re stuck in local optimization
- For mid-game exploration (evals 10-20 out of 30)

## Function Class Taxonomy

### 1. Spline-Based Functions
- **Why**: Smooth transitions reduce Gibbs phenomenon
- **How**: Cubic B-splines with 10-20 basis functions
- **Key parameters**: Knot positions, basis coefficients
- **Implementation**: Use scipy.interpolate.BSpline or numpy polynomial basis

### 2. Gaussian Mixture Models
- **Why**: Flexible shape control with smooth components
- **How**: Weighted sum of Gaussians with varying μ, σ, weights
- **Key parameters**: Number of components (3-5), means, variances, mixing weights
- **Implementation**: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))

### 3. Smoothed Step Functions
- **Why**: Near-optimal of step functions with continuity
- **How**: Use sigmoid/sigmoid-like functions (tanh, expit) with steepness parameter
- **Key parameters**: Step positions, smoothing width (steepness)
- **Implementation**: f(x) = Σ w_i * σ((x - μ_i)/ε) where σ is sigmoid

### 4. Piecewise Polynomials
- **Why**: More flexible than steps, analytically tractable
- **How**: Define polynomial segments with continuity constraints
- **Key parameters**: Segment boundaries, polynomial coefficients
- **Implementation**: f(x) = Σ p_i(x) * I(x ∈ segment_i)

### 5. Multi-Modal Functions
- **Why**: Separated peaks may optimize L2/∞ tradeoff
- **How**: Multiple narrow peaks (Gaussian, Lorentzian, or spline-based)
- **Key parameters**: Peak positions, widths, relative heights
- **Implementation**: f(x) = Σ h_i * g((x-μ_i)/σ_i)

## Execution Strategy

### Phase 1: Diagnosis (evals 0-3)
- Try 1-2 step mutations
- If no improvement: STOP step exploration, go to Phase 2

### Phase 2: Structural Exploration (evals 4-15)
- Call structural_explorer to get new architectures
- Implement 3-4 distinct classes
- Evaluate each, keep the best

### Phase 3: Refinement of Best (evals 16-25)
- Take best new architecture
- Apply small parameter perturbations
- Try local optimization

### Phase 4: Final Push (evals 26-30)
- Small refinements on best candidate
- Report result

## Red Flags
- X: Spending 10+ evals on step pattern mutations
- X: Repeatedly returning to same architecture without improvement
- X: Ignoring structural_explorer recommendations
- X: Making edits that are too small to change the function meaningfully
