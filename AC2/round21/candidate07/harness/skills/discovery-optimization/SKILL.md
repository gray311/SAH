---
name: discovery-optimization
description: "Function-family diversity exploration with gradient refinement. Try multiple representations (steps, splines, polynomials) before committing to one. Use gradients only within promising families."
---

# C2 Maximizer: Function Family Diversity Protocol
## Core Principle
Step functions are a LOCAL optimum. You MUST explore multiple function families before refining. Try steps, splines, polynomials, exponential-plateau, and mixtures. Use gradients only within a promising family.
## Phase 1: Broad Family Exploration (iterations 1-10)
Step 1: Analyze Current Structure
- Call analyze_function_family to understand what you're working with
- Note: Is it pure steps? Smooth? Piecewise?
Step 2: Generate 4 Family Variants
Generate EXACTLY 4 variants from DIFFERENT families:
Variant A (Multi-level Steps): - 5-7 levels with asymmetric heights - Heights: vary between 0.5 and 2.5 - Widths: vary between 10% and 40% of domain
Variant B (B-Splines): - 5-7 basis functions - Smooth transitions (no jumps) - Coefficients sum to positive constant
Variant C (Piecewise Polynomial): - 3-5 polynomial segments - Use linear or cubic splines - Ensure C1 or C2 continuity
Variant D (Exponential-Plateau): - Exponential rise: exp(-k*x) for x < x0 - Flat plateau: constant value for |x| < w - Exponential decay: exp(-k*x) for x > x0
Step 3: Probe and Evaluate
- Call probe_solution on ALL 4 variants (4 probes)
- Rank by probe score
- Call evaluate_solution on TOP 2 only
- If BOTH score <= 1.0: try Variant E (Gaussian Mixture) - Sum of 3-5 Gaussians with different widths - Ensure non-negativity
Step 4: Select Winning Family
- Continue with family that scored highest
- If all families similar: switch to next best
## Phase 2: Gradient Refinement (iterations 11-20)
Step 1: Compute Gradients for Current Family
- Use JAX autodiff on the appropriate parameter set
- For steps: gradients on interval boundaries and heights - For splines: gradients on knot positions and B-spline coefficients - For polynomials: gradients on segment coefficients
Step 2: Gradient Ascent
- Take step: new_param = param + learning_rate * gradient - learning_rate = 0.05 initially, decay to 0.01 - Clip to valid range
Step 3: Generate 3 Variants
- Variant 1: Follow positive gradient - Variant 2: Perturb in orthogonal direction - Variant 3: Combine gradient step with small random noise
Step 4: Probe and Evaluate
- Probe all 3, evaluate best - If gradient norm < 0.001: switch to Phase 3
## Phase 3: Hybrid Approaches (iterations 21-25)
Step 1: Mix Best Candidates
- Try smoothing the best step-function (convolve with narrow Gaussian) - Try adding polynomial tail to best spline - Try weighted ensemble of top 2 from different families
Step 2: Final Evaluation
- Probe 3 hybrids, evaluate best - Submit if c2 > 0.8962799441554086
## Key Rules
- TRY AT LEAST 3 DIFFERENT FAMILIES before Phase 2 - Use gradients ONLY within a family - Probe 4-6 variants before ANY full eval - If stuck at iteration 10+: call reinitialize_with_diversity to switch families
