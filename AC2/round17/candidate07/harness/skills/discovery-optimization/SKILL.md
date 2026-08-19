---
name: discovery-optimization
description: "Parallel family exploration: generate diverse function families (Gaussian, B-spline, oscillatory) in iteration 1, use probes to filter, evaluate top 3, cycle until budget exhausted. Prioritize diversity over sequential refinement."
---

# C₂ Record Breaker: Parallel Family Exploration

## Phase 1: Diverse Generation (Iteration 1)

1. Call generate_candidates to obtain 5 diverse function families:
   - Gaussian mixtures: f(x) = Σ w_i * exp(-((x-μ_i)²)/(2σ_i²))
   - B-spline: 30-50 control points with softplus positivity
   - Oscillatory decay: (1 + α cos(βx)) * exp(-γ|x|)
   - Multi-level asymmetric steps: finer than seed's 5 patterns
   - Piecewise-polynomial: higher-order smooth transitions

2. For EACH family, create 2 variants with different hyperparameters
   - Gaussian: vary μ positions, σ values, and weights
   - B-spline: vary control point distribution, knot spacing
   - Oscillatory: vary α (0.1-0.5), β (2-8), γ (0.5-1.2)
   - Multi-level: vary number of levels (8-16) and height assignments

3. Total: 10 variants to explore

## Phase 2: Probe-Based Filtering

1. Call probe_solution on ALL 10 variants
   - This uses 10 of your 30 probes
   - Probes are fast and don't consume evaluation budget

2. Sort variants by probe score (descending)

3. Call evaluate_solution on the TOP 3 by probe score
   - Only 3 full evaluations out of 30 budget
   - If probe < 1.04199, SKIP full evaluation

## Phase 3: Iteration or Restart

1. If ANY evaluation beats 1.04199:
   - Slightly refine that variant (small parameter tweaks)
   - Do NOT exhaust this family; continue exploring others
   - Generate new families to explore orthogonal regions

2. If NO evaluation beats 1.04199:
   - Generate a NEW set of candidates from a DIFFERENT angle
   - Example: if first set tried smooth functions, try sharper ones
   - Try completely new families not yet attempted

## Key Principles

- **DIVERSITY FIRST**: The seed's step patterns are a local optimum. Escape by exploring ORTHOGONAL function classes.
- **PROBE TO FILTER**: Never waste a full evaluation on a variant that probes below current best.
- **PARALLEL EXPLORATION**: In iteration 1, explore ALL major families. Don't refine one type for many iterations.
- **CYCLE UNTIL BUDGET**: Each iteration should complete: generate → probe → evaluate top → generate new.
- **FAST ITERATIONS**: Complete 1 full cycle in 2-3 iterations. You have 60 iterations for ~20-25 cycles.

## Family-Specific Guidance

**Gaussian mixtures**: 
- Start with 3-5 Gaussians centered at different locations
- Weights should sum to 1
- σ values control smoothness; try both sharp (σ<0.3) and smooth (σ>0.8)

**B-spline**:
- Use scipy.interpolate.splev/splrep
- Knots: uniform or clustered around expected peaks
- Control points: optimize with softplus to ensure positivity

**Oscillatory decay**:
- α controls oscillation amplitude (0.1-0.5)
- β controls frequency (2-8)
- γ controls decay rate (0.5-1.2)

**Multi-level asymmetric steps**:
- Use 8-16 levels instead of seed's 5
- Asymmetric heights: don't mirror left/right
- Position levels non-uniformly (e.g., more levels in center)

## Budget Management

- Probes: 30 total. Use ~10 per cycle to filter 10 variants
- Evaluations: 30 total. Only evaluate top 3 per cycle
- If stuck after 2 cycles: generate new families from scratch
- Aim to beat 1.04199 by iteration 10-15
