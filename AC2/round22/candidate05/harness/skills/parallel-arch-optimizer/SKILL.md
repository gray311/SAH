---
name: parallel-arch-optimizer
description: Parallel search across multiple function architectures for C2 maximization. Structural innovation over parameter tuning.
---

# Parallel Architecture Optimizer for C2

## Core Insight: You're Stuck in Step Function Local Optima

The current best (0.8962799441554086) uses step functions. Small perturbations WON'T work.
You MUST explore DIFFERENT function families in parallel.

## Phase 1: Parallel Exploration (iterations 1-10)

### Week 1: Architecture Diversity

1. Call explore_architectures ONCE to get 3-4 function families:
   - Refined step (multi-level, asymmetric)
   - Gaussian mixture (2-3 components)
   - B-spline (5-7 knots)
   - Hybrid (step + Gaussian tails)

2. For EACH architecture:
   - Generate 2-3 representative variants
   - Probe ALL variants (20-25 probes total across all)
   - Track which architecture wins early

3. Evaluate TOP 2 variants by probe score
   - Expect: one from step, one from mixture or spline
   - Both should beat 1.042 if architecture diversity works

## Phase 2: Best Architecture Refinement (iterations 11-20)

### Identify Winner

Which architecture achieved best c2? Focus refinement there:

- If STEP won: Try 5-level asymmetric, split peaks, add wings
- If GAUSSIAN won: Optimize 2 vs 3 components, adjust widths
- If SPLINE won: Move knots to high-gradient regions
- If HYBRID won: Tune transition width between step and Gaussian

### Refinement Strategy

Generate 3 variants:
- Variant A: Push extreme parameters (narrower peak, higher contrast)
- Variant B: Structural change (split peak, add component)
- Variant C: Smooth variation (Gaussian-like transition)

Probe all, evaluate best.

## Phase 3: Boundary Pushing (iterations 21-30)

Try configurations at the edge of feasibility:
- Peak width < 8% of domain
- Peak height > 3.5
- Two narrow peaks with wide base (triangle-like)
- Fourier-optimal: coefficients with max c2 under positivity

## Key Rules

- PARALLELISM: Never focus > 5 iterations on one architecture
- ARCHITECTURE-FIRST: Change function class before tweaking parameters
- AGGRESSIVE PROBING: Use all 30 probes to explore before spending evals
- HYBRID MINDSET: Combine successful elements across architectures
- DIVERSITY METRIC: Track which architecture type is winning
