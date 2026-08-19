---
name: discovery-optimization
description: "Discover novel function families for C\u2082 maximization. Prioritize structural innovation over parameter tuning. Use probes to compare diverse function shapes, then evaluate promising new families."
---

# C₂ Function Discovery - Structural Innovation
## Core Philosophy The current best (1.03431) is a LOCAL optimum. You must find GLOBAL improvements through STRUCTURAL changes, not parameter tweaks.
## Phase 1: Diversify (First 10 iterations) Generate completely different function FAMILIES: - Splines: Smooth B-splines with optimized knot positions - Mixtures: Weighted combinations (e.g., 0.6*step + 0.4*exponential) - Fourier hints: Sinusoidal modulations of base shapes - Polynomial decay: f(x) = a*x^{-b} with constraint enforcement - Asymmetric peaks: Shift the high plateau off-center - Multi-scale: Fine details on coarse base
Use probe_solution to test 5-10 diverse candidates, picking the BEST probe score for eval.
## Phase 2: Evolve Promising Directions If probe reveals a promising family (e.g., splines beat step), then: - Within that family, do small refinements - Try variations: different knot placements, mixture weights - ONLY then use evaluate_solution
## Phase 3: Basin Hopping After each eval: - Make a MAJOR structural change (different family, symmetry break, interval count change) - Probe the new direction - If probe improves, eval it - If not, try another radical change
## Key Mutations to Try - Interval count: 200-600 (not just 450) - Function family: Completely different mathematical form - Symmetry: f(x) != f(-x), asymmetric peaks - Number of modes: 2-8 peaks (not just 1 central plateau) - Smooth transitions: Replace sharp steps with smooth splines
## When to Probe vs Eval - Probe: Always test new FUNCTION FAMILIES before eval - Eval: Only after probe confirms a family beats current best - Recovery: If stuck, reset to random diverse seed
## Success Criteria - combined_score > 1.035 (break through the local optimum) - Prefer structural diversity over parameter precision - Don't get stuck refining a failing direction
