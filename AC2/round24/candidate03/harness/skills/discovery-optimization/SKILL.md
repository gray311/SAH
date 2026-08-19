---
name: discovery-optimization
description: "Explore diverse function families (splines, mixtures, learned) to beat the step-function record. Avoid parameter-only refinement."
---

# C2 Maximizer: Function Family Exploration Protocol
## Core Principle Step functions achieve 0.89628 but may not be optimal. To beat this, explore DIFFERENT mathematical representations entirely.
## Phase 1: Family Discovery (iterations 1-10)
### Step 1: Choose a New Family Call explore_function_family with ONE of: - family_type="spline": B-spline with 5-10 knots, optimize knot positions and weights - family_type="mixture": Weighted sum of 3-5 Gaussians/exponentials (with softplus for positivity) - family_type="learned": Neural-network-prior function (small MLP with smooth activation) - family_type="hybrid": Step base with spline peaks
### Step 2: Generate Representative The tool returns a complete function implementation. Edit your EVOLVE-BLOCK to replace the current optimizer with the new representation.
### Step 3: Probe and Evaluate - Call probe_solution on 2-3 variants from DIFFERENT families - Rank by probe score - Call evaluate_solution on top 1
## Phase 2: Hybrid Design (iterations 11-20)
If best probe beats record: 1. Try hybrid approaches: e.g., step-function base with spline-refined peaks 2. Generate 3 hybrids: (a) spline base with step edges, (b) mixture with step outer regions, (c) learned base with step constraints 3. Probe all 3, evaluate best
## Phase 3: Aggressive Search (iterations 21-25)
If still below record: 1. Try "learned" family only (neural-network-prior) 2. Probe 4 variants, evaluate best
## Key Innovation Points - SPLINE: Use scipy.interpolate.BSpline or manual B-spline basis - MIXTURE: sum of exp(-(x-mu)**2/sigma) with optimized mu, sigma, weights - LEARNED: Small MLP: f(x) = ReLU(W2@tanh(W1*x + b2)) or similar - KEY: Always ensure f(x) >= 0 (use softplus, exp, or squared terms) - NEVER: Just tweak step heights - try new representations!
